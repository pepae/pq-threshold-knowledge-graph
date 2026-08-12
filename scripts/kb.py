"""Shared vault parsing and graph construction for the PQ threshold KB.

build_graph.py and validate.py both import this. graph/schema.json is the single
source of truth for node types, fields, and edge types; nothing here hardcodes a
type name.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_DIR = REPO_ROOT / "vault"
SCHEMA_PATH = REPO_ROOT / "graph" / "schema.json"
GRAPH_PATH = REPO_ROOT / "graph" / "graph.json"

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+?)(?:#[^\]\|]*?)?(?:\|[^\]]*?)?\]\]")


def display_path(path: Path) -> str:
    """Repo-relative when possible, absolute otherwise (tests use temp dirs)."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


@dataclass
class Note:
    path: Path
    id: str
    type: str
    title: str
    fields: dict
    body: str
    wikilinks: list[str] = field(default_factory=list)

    @property
    def rel(self) -> str:
        return display_path(self.path)


@dataclass
class Issue:
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.where}: {self.message}"


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def id_pattern_for(node_type: str, schema: dict) -> str:
    """The id pattern a node of this type must match, honouring per-type overrides."""
    return schema["node_types"][node_type].get("id_pattern", schema["id_pattern"])


def any_id_re(schema: dict) -> re.Pattern:
    """Matches an id legal for *some* node type. Used for reference lists, where
    the referenced type is not known until edges are resolved."""
    patterns = {schema["id_pattern"]}
    for defn in schema["node_types"].values():
        if "id_pattern" in defn:
            patterns.add(defn["id_pattern"])
    stripped = sorted(p.lstrip("^").rstrip("$") for p in patterns)
    return re.compile("^(?:" + "|".join(f"(?:{p})" for p in stripped) + ")$")


# --------------------------------------------------------------------------
# field type checking
# --------------------------------------------------------------------------


def _check_value(key: str, value, spec: str, id_re: re.Pattern) -> list[str]:
    """Return a list of error messages for one frontmatter value."""
    errs: list[str] = []
    if spec == "str":
        if not isinstance(value, str):
            errs.append(f"field '{key}' must be a string, got {type(value).__name__}")
    elif spec == "int":
        if not isinstance(value, int) or isinstance(value, bool):
            errs.append(f"field '{key}' must be an integer, got {type(value).__name__}")
    elif spec == "bool":
        if not isinstance(value, bool):
            errs.append(
                f"field '{key}' must be a boolean (true/false), got {type(value).__name__}"
            )
    elif spec in ("list[str]", "list[id]"):
        if not isinstance(value, list):
            errs.append(f"field '{key}' must be a list, got {type(value).__name__}")
        else:
            for item in value:
                if not isinstance(item, str):
                    errs.append(f"field '{key}' must contain only strings, got {item!r}")
                elif spec == "list[id]" and not id_re.match(item):
                    errs.append(
                        f"field '{key}' contains {item!r}, which is not a valid id "
                        f"(must match {id_re.pattern})"
                    )
    else:  # pragma: no cover - guards against a bad schema edit
        errs.append(f"schema declares unknown field type {spec!r} for '{key}'")
    return errs


def _allowed_fields(node_type: str, schema: dict) -> dict[str, str]:
    """Map every frontmatter key legal on this node type to its value spec."""
    common = schema["common_fields"]
    type_def = schema["node_types"][node_type]

    allowed: dict[str, str] = {}
    for key in common["required"]:
        allowed[key] = "str"
    allowed.update(common["optional"])
    for key in type_def["required"]:
        allowed[key] = type_def["optional"].get(key, "str")
    allowed.update(type_def["optional"])

    for edge_type, edge_def in schema["edge_types"].items():
        for spec in edge_def["frontmatter_keys"]:
            side = "domain" if spec["direction"] == "forward" else "range"
            if node_type in edge_def[side]:
                allowed[spec["key"]] = "list[id]"
    return allowed


# --------------------------------------------------------------------------
# note parsing
# --------------------------------------------------------------------------


def parse_note(path: Path, schema: dict) -> tuple[Note | None, list[Issue]]:
    issues: list[Issue] = []
    where = display_path(path)
    raw = path.read_text(encoding="utf-8")

    match = FRONTMATTER_RE.match(raw)
    if not match:
        return None, [Issue(where, "missing YAML frontmatter delimited by --- lines")]

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, [Issue(where, f"invalid YAML frontmatter: {exc}")]

    if not isinstance(fm, dict):
        return None, [Issue(where, "frontmatter must be a YAML mapping")]

    body = match.group(2)
    ref_id_re = any_id_re(schema)

    for key in schema["common_fields"]["required"]:
        if key not in fm:
            issues.append(Issue(where, f"missing required field '{key}'"))
    if issues:
        return None, issues

    node_id, node_type, title = fm["id"], fm["type"], fm["title"]

    if node_type not in schema["node_types"]:
        return None, [
            Issue(
                where,
                f"unknown type {node_type!r}; known types: "
                + ", ".join(sorted(schema["node_types"])),
            )
        ]

    own_pattern = id_pattern_for(node_type, schema)
    if not isinstance(node_id, str) or not re.match(own_pattern, node_id):
        return None, [
            Issue(where, f"id {node_id!r} must match {own_pattern} for type {node_type!r}")
        ]
    if not isinstance(title, str) or not title.strip():
        issues.append(Issue(where, "field 'title' must be a non-empty string"))

    if path.stem != node_id:
        issues.append(
            Issue(where, f"filename stem {path.stem!r} must equal id {node_id!r}")
        )

    expected_dir = schema["node_types"][node_type]["dir"]
    actual_dir = path.parent.name
    if actual_dir != expected_dir:
        issues.append(
            Issue(
                where,
                f"type {node_type!r} must live in vault/{expected_dir}/, "
                f"found in vault/{actual_dir}/",
            )
        )

    for key in schema["node_types"][node_type]["required"]:
        if key not in fm:
            issues.append(
                Issue(where, f"type {node_type!r} requires field '{key}'")
            )

    allowed = _allowed_fields(node_type, schema)
    enums = schema["enums"]
    for key, value in fm.items():
        if key not in allowed:
            issues.append(
                Issue(
                    where,
                    f"unknown field '{key}' for type {node_type!r}; add it to "
                    "graph/schema.json if it is intentional",
                )
            )
            continue
        if key in ("id", "type", "title"):
            continue
        if isinstance(value, str) and allowed[key] == "list[id]":
            fm[key] = value = [value]
        for msg in _check_value(key, value, allowed[key], ref_id_re):
            issues.append(Issue(where, msg))
        if key in enums and isinstance(value, str) and value not in enums[key]:
            issues.append(
                Issue(
                    where,
                    f"field '{key}' is {value!r}, must be one of "
                    + ", ".join(enums[key]),
                )
            )

    note = Note(
        path=path,
        id=node_id,
        type=node_type,
        title=title,
        fields=fm,
        body=body,
        wikilinks=sorted(set(m.group(1).strip() for m in WIKILINK_RE.finditer(body))),
    )
    return note, issues


def collect_notes(
    schema: dict, vault_dir: Path = VAULT_DIR
) -> tuple[dict[str, Note], list[Issue]]:
    notes: dict[str, Note] = {}
    issues: list[Issue] = []
    seen: dict[str, str] = {}

    for path in sorted(vault_dir.rglob("*.md")):
        if path.name.startswith("_") or path.name == "README.md":
            continue
        note, note_issues = parse_note(path, schema)
        issues.extend(note_issues)
        if note is None:
            continue
        if note.id in seen:
            issues.append(
                Issue(note.rel, f"duplicate id {note.id!r}, already defined in {seen[note.id]}")
            )
            continue
        seen[note.id] = note.rel
        notes[note.id] = note

    return notes, issues


# --------------------------------------------------------------------------
# graph construction
# --------------------------------------------------------------------------


def build_edges(
    notes: dict[str, Note], schema: dict
) -> tuple[list[dict], list[Issue]]:
    edges: list[dict] = []
    issues: list[Issue] = []
    seen: set[tuple[str, str, str]] = set()

    for note in notes.values():
        for edge_type, edge_def in schema["edge_types"].items():
            for spec in edge_def["frontmatter_keys"]:
                key, direction = spec["key"], spec["direction"]
                values = note.fields.get(key)
                if not values:
                    continue
                for other_id in values:
                    if other_id not in notes:
                        issues.append(
                            Issue(
                                note.rel,
                                f"field '{key}' references unknown id {other_id!r} "
                                "(no vault note defines it)",
                            )
                        )
                        continue
                    if direction == "forward":
                        source, target = note, notes[other_id]
                    else:
                        source, target = notes[other_id], note
                    if source.id == target.id:
                        issues.append(
                            Issue(note.rel, f"field '{key}' creates a self-edge on {note.id!r}")
                        )
                        continue
                    if source.type not in edge_def["domain"]:
                        issues.append(
                            Issue(
                                note.rel,
                                f"edge '{edge_type}' from {source.id!r} is invalid: "
                                f"source type {source.type!r} not in domain "
                                + ", ".join(edge_def["domain"]),
                            )
                        )
                        continue
                    if target.type not in edge_def["range"]:
                        issues.append(
                            Issue(
                                note.rel,
                                f"edge '{edge_type}' to {target.id!r} is invalid: "
                                f"target type {target.type!r} not in range "
                                + ", ".join(edge_def["range"]),
                            )
                        )
                        continue
                    triple = (source.id, edge_type, target.id)
                    if triple in seen:
                        continue
                    seen.add(triple)
                    edges.append(
                        {
                            "source": source.id,
                            "type": edge_type,
                            "target": target.id,
                            "declared_in": note.id,
                        }
                    )

    edges.sort(key=lambda e: (e["source"], e["type"], e["target"]))
    return edges, issues


NON_NODE_FIELDS = {"id", "type", "title"}


def build_nodes(notes: dict[str, Note], schema: dict) -> list[dict]:
    edge_keys = {
        spec["key"]
        for edge_def in schema["edge_types"].values()
        for spec in edge_def["frontmatter_keys"]
    }
    nodes = []
    for note in sorted(notes.values(), key=lambda n: n.id):
        attrs = {
            k: v
            for k, v in note.fields.items()
            if k not in NON_NODE_FIELDS and k not in edge_keys
        }
        nodes.append(
            {
                "id": note.id,
                "type": note.type,
                "title": note.title,
                "path": note.rel,
                "attrs": dict(sorted(attrs.items())),
            }
        )
    return nodes


def build_graph(notes: dict[str, Note], schema: dict) -> tuple[dict, list[Issue]]:
    nodes = build_nodes(notes, schema)
    edges, issues = build_edges(notes, schema)

    node_counts: dict[str, int] = {}
    for node in nodes:
        node_counts[node["type"]] = node_counts.get(node["type"], 0) + 1
    edge_counts: dict[str, int] = {}
    for edge in edges:
        edge_counts[edge["type"]] = edge_counts.get(edge["type"], 0) + 1

    graph = {
        "metadata": {
            "schema_version": schema["schema_version"],
            "generator": "scripts/build_graph.py",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "node_counts": dict(sorted(node_counts.items())),
            "edge_counts": dict(sorted(edge_counts.items())),
            "node_type_colors": {
                name: defn["color"] for name, defn in sorted(schema["node_types"].items())
            },
        },
        "nodes": nodes,
        "edges": edges,
    }
    return graph, issues


def dump_graph(graph: dict) -> str:
    """Deterministic serialization. No timestamps, so CI can diff it."""
    return json.dumps(graph, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
