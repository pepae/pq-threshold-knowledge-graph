#!/usr/bin/env python3
"""Build graph/graph.json from vault frontmatter.

Hard-fails on unknown ids, edges to nonexistent nodes, unknown types, and
missing required fields. Output is deterministic, so `--check` can assert the
committed graph is up to date.

    python3 scripts/build_graph.py            # write graph/graph.json
    python3 scripts/build_graph.py --check    # fail if the committed file is stale
"""

from __future__ import annotations

import argparse
import sys

from kb import GRAPH_PATH, VAULT_DIR, build_graph, collect_notes, dump_graph, load_schema


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if graph.json differs from the vault",
    )
    parser.add_argument("--quiet", action="store_true", help="only print errors")
    args = parser.parse_args()

    if not VAULT_DIR.is_dir():
        print(f"error: no vault directory at {VAULT_DIR}", file=sys.stderr)
        return 2

    schema = load_schema()
    notes, issues = collect_notes(schema)
    graph, edge_issues = build_graph(notes, schema)
    issues.extend(edge_issues)

    if issues:
        print(f"build failed with {len(issues)} error(s):\n", file=sys.stderr)
        for issue in sorted(issues, key=lambda i: (i.where, i.message)):
            print(f"  {issue}", file=sys.stderr)
        return 1

    rendered = dump_graph(graph)

    if args.check:
        if not GRAPH_PATH.exists():
            print(
                f"error: {GRAPH_PATH.name} does not exist; run scripts/build_graph.py",
                file=sys.stderr,
            )
            return 1
        if GRAPH_PATH.read_text(encoding="utf-8") != rendered:
            print(
                "error: graph/graph.json is stale. Run scripts/build_graph.py and "
                "commit the result.",
                file=sys.stderr,
            )
            return 1
        if not args.quiet:
            print(
                f"graph/graph.json is up to date "
                f"({graph['metadata']['node_count']} nodes, "
                f"{graph['metadata']['edge_count']} edges)"
            )
        return 0

    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(rendered, encoding="utf-8")

    if not args.quiet:
        meta = graph["metadata"]
        print(f"wrote {GRAPH_PATH.relative_to(GRAPH_PATH.parent.parent)}")
        print(f"  {meta['node_count']} nodes, {meta['edge_count']} edges")
        if meta["node_counts"]:
            for node_type, count in meta["node_counts"].items():
                print(f"    {node_type:<16} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
