#!/usr/bin/env python3
"""Assemble the static site into dist/.

Notes are prerendered to HTML at build time and wikilinks are rewritten to
in-app navigation, so the shipped bundle needs no markdown parser and no
backend.

    python3 scripts/build_webapp.py [--out dist]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from kb import (
    REPO_ROOT,
    VAULT_DIR,
    WIKILINK_RE,
    build_graph,
    collect_notes,
    dump_graph,
    load_schema,
)

WEBAPP_DIR = REPO_ROOT / "webapp"


def _resolution_map(notes) -> dict[str, str]:
    table: dict[str, str] = {}
    for note in notes.values():
        table[note.id.lower()] = note.id
        table[note.title.lower()] = note.id
        for alias in note.fields.get("aliases", []) or []:
            table[alias.lower()] = note.id
    return table


def rewrite_wikilinks(body: str, table: dict[str, str]) -> str:
    """[[id]] and [[id|label]] become in-app anchors before markdown runs."""

    def repl(match: re.Match) -> str:
        raw = match.group(0)[2:-2]
        target, _, label = raw.partition("|")
        target = target.split("#")[0].strip()
        label = label.strip() or target
        node_id = table.get(target.lower())
        if node_id is None:
            return label
        return f'<a href="#/n/{node_id}" class="wikilink" data-id="{node_id}">{label}</a>'

    return WIKILINK_RE.sub(repl, body)


def render(notes, table) -> dict[str, dict]:
    import markdown

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "admonition"], output_format="html5"
    )
    rendered: dict[str, dict] = {}
    for node_id, note in sorted(notes.items()):
        md.reset()
        html = md.convert(rewrite_wikilinks(note.body, table))
        rendered[node_id] = {
            "id": node_id,
            "type": note.type,
            "title": note.title,
            "path": note.rel,
            "html": html,
            "aliases": note.fields.get("aliases", []) or [],
        }
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="dist", help="output directory (default: dist)")
    args = parser.parse_args()

    out = (REPO_ROOT / args.out).resolve()
    schema = load_schema()
    notes, issues = collect_notes(schema)
    graph, edge_issues = build_graph(notes, schema)
    issues.extend(edge_issues)

    if issues:
        print(f"refusing to build a site from an invalid vault ({len(issues)} error(s)):",
              file=sys.stderr)
        for issue in sorted(issues, key=lambda i: (i.where, i.message)):
            print(f"  {issue}", file=sys.stderr)
        return 1

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for item in sorted(WEBAPP_DIR.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            shutil.copytree(item, out / item.name)
        else:
            shutil.copy2(item, out / item.name)

    pdf_src = REPO_ROOT / "papers" / "pdf"
    if pdf_src.is_dir():
        pdf_out = out / "papers" / "pdf"
        pdf_out.mkdir(parents=True, exist_ok=True)
        for pdf in sorted(pdf_src.glob("*.pdf")):
            shutil.copy2(pdf, pdf_out / pdf.name)

    data = out / "data"
    data.mkdir(exist_ok=True)
    (data / "graph.json").write_text(dump_graph(graph), encoding="utf-8")

    table = _resolution_map(notes)
    rendered = render(notes, table)
    (data / "notes.json").write_text(
        json.dumps(rendered, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (data / "schema.json").write_text(
        json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    total = sum(
        f.stat().st_size for f in out.rglob("*") if f.is_file()
    )
    print(f"built {out.relative_to(REPO_ROOT)}/")
    print(f"  {len(rendered)} notes, {graph['metadata']['edge_count']} edges")
    print(f"  {total / 1024:.0f} KiB total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
