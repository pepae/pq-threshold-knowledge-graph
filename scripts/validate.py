#!/usr/bin/env python3
"""Validate the vault: schema, wikilinks, quality bar, orphans.

Runs every check build_graph.py runs, then adds:

  * wikilink resolution, so [[Foo]] in prose always lands on a real note
  * the quality bar (every scheme needs an assumption edge, a desideratum edge,
    and a status)
  * eprint format, and a nudge to set `unverified: true` on unsourced records
  * orphan nodes and desiderata with no incoming edges (reported, not fatal)

Errors exit 1. Warnings are printed and exit 0 unless --strict is passed.

    python3 scripts/validate.py
    python3 scripts/validate.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict

from kb import (
    VAULT_DIR,
    Issue,
    Note,
    build_graph,
    collect_notes,
    load_schema,
)

EPRINT_RE = re.compile(r"^\d{4}/\d{3,4}$")
DESIDERATUM_EDGES = ("satisfies", "partially_satisfies", "fails")


def _resolution_map(notes: dict[str, Note]) -> dict[str, str]:
    """Every string a wikilink may legally use, mapped to a node id."""
    table: dict[str, str] = {}
    for note in notes.values():
        table[note.id.lower()] = note.id
        table[note.title.lower()] = note.id
        for alias in note.fields.get("aliases", []) or []:
            table[alias.lower()] = note.id
    return table


def check_wikilinks(notes: dict[str, Note]) -> list[Issue]:
    table = _resolution_map(notes)
    issues: list[Issue] = []
    for note in sorted(notes.values(), key=lambda n: n.id):
        for link in note.wikilinks:
            if link.lower() not in table:
                issues.append(
                    Issue(
                        note.rel,
                        f"wikilink [[{link}]] does not resolve to any note id, "
                        "title, or alias",
                    )
                )
    return issues


def check_quality_bar(
    notes: dict[str, Note], edges: list[dict], schema: dict
) -> list[Issue]:
    """Every scheme needs >=1 assumption edge, >=1 desideratum edge, a status."""
    outgoing: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        outgoing[edge["source"]].add(edge["type"])

    issues: list[Issue] = []
    for note in sorted(notes.values(), key=lambda n: n.id):
        if note.type != "scheme":
            continue
        kinds = outgoing[note.id]
        if "assumes" not in kinds:
            issues.append(
                Issue(note.rel, "scheme has no assumption edge (set `assumptions:`)")
            )
        if not kinds & set(DESIDERATUM_EDGES):
            issues.append(
                Issue(
                    note.rel,
                    "scheme has no desideratum edge (set `satisfies:`, "
                    "`partially_satisfies:`, or `fails:`)",
                )
            )
        if not note.fields.get("status"):
            issues.append(Issue(note.rel, "scheme has no status field"))
    return issues


def check_citations(notes: dict[str, Note]) -> tuple[list[Issue], list[Issue]]:
    """eprint numbers must be well formed; unsourced records must say so."""
    errors: list[Issue] = []
    warnings: list[Issue] = []
    for note in sorted(notes.values(), key=lambda n: n.id):
        eprint = note.fields.get("eprint")
        if eprint is not None and not EPRINT_RE.match(str(eprint)):
            errors.append(
                Issue(
                    note.rel,
                    f"eprint {eprint!r} is not of the form YYYY/NNN "
                    "(quote it in YAML so 2024/263 is not parsed as a number)",
                )
            )
        if note.type not in ("scheme", "paper", "attack"):
            continue
        has_source = bool(eprint) or bool(note.fields.get("venue"))
        declared = note.fields.get("unverified") or note.fields.get("status") == "draft"
        if not has_source and not declared:
            warnings.append(
                Issue(
                    note.rel,
                    "no eprint and no venue; set `unverified: true` or "
                    "`status: draft` so the record is not read as a real citation",
                )
            )
    return errors, warnings


def check_orphans(notes: dict[str, Note], edges: list[dict]) -> list[Issue]:
    touched: set[str] = set()
    for edge in edges:
        touched.add(edge["source"])
        touched.add(edge["target"])
    return [
        Issue(note.rel, f"orphan node {note.id!r} has no edges in either direction")
        for note in sorted(notes.values(), key=lambda n: n.id)
        if note.id not in touched
    ]


def check_unreferenced_desiderata(
    notes: dict[str, Note], edges: list[dict]
) -> list[Issue]:
    referenced = {
        edge["target"] for edge in edges if edge["type"] in DESIDERATUM_EDGES
    }
    return [
        Issue(
            note.rel,
            f"desideratum {note.id!r} has no incoming satisfies/"
            "partially_satisfies/fails edge from any scheme",
        )
        for note in sorted(notes.values(), key=lambda n: n.id)
        if note.type == "desideratum" and note.id not in referenced
    ]


def _report(label: str, issues: list[Issue], stream) -> None:
    if not issues:
        return
    print(f"\n{label} ({len(issues)}):", file=stream)
    for issue in sorted(issues, key=lambda i: (i.where, i.message)):
        print(f"  {issue}", file=stream)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors"
    )
    args = parser.parse_args()

    if not VAULT_DIR.is_dir():
        print(f"error: no vault directory at {VAULT_DIR}", file=sys.stderr)
        return 2

    schema = load_schema()
    notes, errors = collect_notes(schema)
    graph, edge_errors = build_graph(notes, schema)
    errors.extend(edge_errors)

    if errors:
        _report("schema errors", errors, sys.stderr)
        print(f"\nFAILED: {len(errors)} schema error(s)", file=sys.stderr)
        return 1

    edges = graph["edges"]
    warnings: list[Issue] = []

    errors.extend(check_wikilinks(notes))
    errors.extend(check_quality_bar(notes, edges, schema))
    citation_errors, citation_warnings = check_citations(notes)
    errors.extend(citation_errors)
    warnings.extend(citation_warnings)
    warnings.extend(check_orphans(notes, edges))
    warnings.extend(check_unreferenced_desiderata(notes, edges))

    _report("errors", errors, sys.stderr)
    _report("warnings", warnings, sys.stdout)

    meta = graph["metadata"]
    print(
        f"\nvault: {meta['node_count']} nodes, {meta['edge_count']} edges, "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )

    if errors:
        print("FAILED", file=sys.stderr)
        return 1
    if warnings and args.strict:
        print("FAILED (--strict: warnings are errors)", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
