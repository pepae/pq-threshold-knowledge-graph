#!/usr/bin/env python3
"""Query the PQ threshold encryption knowledge graph.

Standard library only, so it runs anywhere with python3 and no install step.
Reads graph/graph.json, which build_graph.py generates from vault frontmatter.

    python3 skill/scripts/query.py node beat-mev
    python3 skill/scripts/query.py neighbors beat-mev --edge-type assumes
    python3 skill/scripts/query.py path bendlin-damgard tacet
    python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
    python3 skill/scripts/query.py open-problems
    python3 skill/scripts/query.py search flooding
    python3 skill/scripts/query.py desiderata
    python3 skill/scripts/query.py stats

Add --json to any subcommand for machine-readable output.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path

DEFAULT_GRAPH = Path(__file__).resolve().parent.parent.parent / "graph" / "graph.json"

DESIDERATUM_EDGES = ("satisfies", "partially_satisfies", "fails")


class Graph:
    def __init__(self, data: dict):
        self.metadata = data.get("metadata", {})
        self.nodes = {n["id"]: n for n in data.get("nodes", [])}
        self.edges = data.get("edges", [])

        self.out: dict[str, list[dict]] = defaultdict(list)
        self.inc: dict[str, list[dict]] = defaultdict(list)
        for edge in self.edges:
            self.out[edge["source"]].append(edge)
            self.inc[edge["target"]].append(edge)

        self._lower = {node_id.lower(): node_id for node_id in self.nodes}
        for node in self.nodes.values():
            self._lower.setdefault(node["title"].lower(), node["id"])

    @classmethod
    def load(cls, path: Path) -> "Graph":
        if not path.exists():
            sys.exit(
                f"error: {path} not found. Run scripts/build_graph.py first."
            )
        with path.open(encoding="utf-8") as fh:
            return cls(json.load(fh))

    def resolve(self, ref: str) -> str:
        """Accept an id, a title, or any casing of either."""
        if ref in self.nodes:
            return ref
        hit = self._lower.get(ref.lower())
        if hit:
            return hit
        candidates = [
            node_id
            for node_id in sorted(self.nodes)
            if ref.lower() in node_id.lower()
            or ref.lower() in self.nodes[node_id]["title"].lower()
        ]
        if len(candidates) == 1:
            return candidates[0]
        if candidates:
            sys.exit(
                f"error: {ref!r} is ambiguous. Did you mean:\n  "
                + "\n  ".join(candidates[:15])
            )
        sys.exit(f"error: no node matches {ref!r}. Try: query.py search {ref}")

    def label(self, node_id: str) -> str:
        node = self.nodes[node_id]
        return f"{node['title']} [{node['type']}]"

    def targets(self, node_id: str, edge_type: str) -> list[str]:
        return sorted(e["target"] for e in self.out[node_id] if e["type"] == edge_type)


# --------------------------------------------------------------------------
# subcommands
# --------------------------------------------------------------------------


def cmd_node(graph: Graph, args) -> dict:
    node_id = graph.resolve(args.id)
    node = graph.nodes[node_id]
    payload = {
        **{k: v for k, v in node.items()},
        "edges_out": [
            {"type": e["type"], "target": e["target"]} for e in graph.out[node_id]
        ],
        "edges_in": [
            {"type": e["type"], "source": e["source"]} for e in graph.inc[node_id]
        ],
    }
    if args.json:
        return payload

    print(f"{node['title']}")
    print(f"  id       {node['id']}")
    print(f"  type     {node['type']}")
    print(f"  note     {node['path']}")
    for key, value in node["attrs"].items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        print(f"  {key:<8} {value}")

    if graph.out[node_id]:
        print("\n  outgoing:")
        for edge in sorted(graph.out[node_id], key=lambda e: (e["type"], e["target"])):
            print(f"    --{edge['type']}--> {graph.label(edge['target'])}")
    if graph.inc[node_id]:
        print("\n  incoming:")
        for edge in sorted(graph.inc[node_id], key=lambda e: (e["type"], e["source"])):
            print(f"    {graph.label(edge['source'])} --{edge['type']}-->")
    return payload


def cmd_neighbors(graph: Graph, args) -> dict:
    start = graph.resolve(args.id)
    seen = {start: 0}
    queue = deque([start])
    hops: dict[int, list[tuple[str, str, str]]] = defaultdict(list)

    while queue:
        current = queue.popleft()
        if seen[current] >= args.depth:
            continue
        candidates = []
        if args.direction in ("out", "both"):
            candidates += [(e, e["target"], "out") for e in graph.out[current]]
        if args.direction in ("in", "both"):
            candidates += [(e, e["source"], "in") for e in graph.inc[current]]
        for edge, other, way in candidates:
            if args.edge_type and edge["type"] not in args.edge_type:
                continue
            if other in seen:
                continue
            seen[other] = seen[current] + 1
            hops[seen[other]].append((other, edge["type"], way))
            queue.append(other)

    payload = {
        "start": start,
        "depth": args.depth,
        "direction": args.direction,
        "edge_types": args.edge_type or "all",
        "neighbors": [
            {"id": nid, "hop": hop, "via": etype, "direction": way}
            for hop in sorted(hops)
            for nid, etype, way in sorted(hops[hop])
        ],
    }
    if args.json:
        return payload

    print(f"{graph.label(start)}")
    if not hops:
        print("  (no neighbors matching that filter)")
    for hop in sorted(hops):
        print(f"\n  {hop} hop:")
        for nid, etype, way in sorted(hops[hop]):
            arrow = "-->" if way == "out" else "<--"
            print(f"    {arrow} {etype:<20} {graph.label(nid)}")
    return payload


def cmd_path(graph: Graph, args) -> dict:
    start, goal = graph.resolve(args.a), graph.resolve(args.b)
    prev: dict[str, tuple[str, str, str]] = {}
    queue = deque([start])
    seen = {start}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        neighbors = [(e["target"], e["type"], "out") for e in graph.out[current]]
        neighbors += [(e["source"], e["type"], "in") for e in graph.inc[current]]
        for other, etype, way in neighbors:
            if other in seen:
                continue
            seen.add(other)
            prev[other] = (current, etype, way)
            queue.append(other)

    if goal not in prev and goal != start:
        payload = {"from": start, "to": goal, "found": False, "steps": []}
        if not args.json:
            print(f"no path between {start} and {goal}")
        return payload

    steps = []
    cursor = goal
    while cursor != start:
        parent, etype, way = prev[cursor]
        steps.append({"from": parent, "type": etype, "to": cursor, "direction": way})
        cursor = parent
    steps.reverse()

    payload = {
        "from": start,
        "to": goal,
        "found": True,
        "hops": len(steps),
        "steps": steps,
    }
    if args.json:
        return payload

    print(f"{graph.label(start)}")
    for step in steps:
        arrow = "--" if step["direction"] == "out" else "<-"
        print(f"  {arrow}{step['type']}-> {graph.label(step['to'])}")
    print(f"\n{len(steps)} hop(s)")
    return payload


def _bool_flag(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() in ("true", "1", "yes", "y")


def cmd_filter(graph: Graph, args) -> dict:
    hits = []
    for node_id in sorted(graph.nodes):
        node = graph.nodes[node_id]
        if args.type and node["type"] != args.type:
            continue
        if args.status and node["attrs"].get("status") != args.status:
            continue

        want_pq = _bool_flag(args.pq)
        if want_pq is not None and bool(node["attrs"].get("pq", False)) != want_pq:
            continue

        ok = True
        for flag, edge_type in (
            (args.satisfies, "satisfies"),
            (args.partially_satisfies, "partially_satisfies"),
            (args.fails, "fails"),
            (args.assumes, "assumes"),
            (args.uses, "uses"),
        ):
            for wanted in flag or []:
                actual = graph.targets(node_id, edge_type)
                if not any(wanted.lower() == a.lower() for a in actual):
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue

        for wanted in args.satisfies_or_partial or []:
            actual = graph.targets(node_id, "satisfies") + graph.targets(
                node_id, "partially_satisfies"
            )
            if not any(wanted.lower() == a.lower() for a in actual):
                ok = False
                break
        if not ok:
            continue

        hits.append(node_id)

    payload = {
        "count": len(hits),
        "results": [
            {
                "id": nid,
                "title": graph.nodes[nid]["title"],
                "type": graph.nodes[nid]["type"],
                "status": graph.nodes[nid]["attrs"].get("status"),
                "pq": graph.nodes[nid]["attrs"].get("pq"),
                "path": graph.nodes[nid]["path"],
            }
            for nid in hits
        ],
    }
    if args.json:
        return payload

    if not hits:
        print("no matches")
        return payload
    width = max(len(h) for h in hits)
    for nid in hits:
        node = graph.nodes[nid]
        pq = node["attrs"].get("pq")
        marker = "PQ " if pq is True else "   "
        status = node["attrs"].get("status", "")
        print(f"  {marker}{nid:<{width}}  {status:<10} {node['title']}")
    print(f"\n{len(hits)} match(es)")
    return payload


def cmd_open_problems(graph: Graph, args) -> dict:
    problems = []
    for node_id in sorted(graph.nodes):
        node = graph.nodes[node_id]
        if node["type"] != "open-problem":
            continue
        if args.state and node["attrs"].get("state") != args.state:
            continue
        problems.append(
            {
                "id": node_id,
                "title": node["title"],
                "state": node["attrs"].get("state"),
                "opened_by": sorted(
                    e["source"] for e in graph.inc[node_id] if e["type"] == "opens"
                ),
                "resolved_by": sorted(
                    e["source"] for e in graph.inc[node_id] if e["type"] == "resolves"
                ),
                "path": node["path"],
            }
        )

    payload = {"count": len(problems), "open_problems": problems}
    if args.json:
        return payload

    for problem in problems:
        print(f"  [{problem['state']}] {problem['id']}")
        print(f"      {problem['title']}")
        if problem["opened_by"]:
            print(f"      opened by:   {', '.join(problem['opened_by'])}")
        if problem["resolved_by"]:
            print(f"      resolved by: {', '.join(problem['resolved_by'])}")
    print(f"\n{len(problems)} open problem(s)")
    return payload


def cmd_desiderata(graph: Graph, args) -> dict:
    rows = []
    ids = sorted(
        (n for n in graph.nodes.values() if n["type"] == "desideratum"),
        key=lambda n: int(n["id"][1:]),
    )
    for node in ids:
        counts = {
            etype: sorted(e["source"] for e in graph.inc[node["id"]] if e["type"] == etype)
            for etype in DESIDERATUM_EDGES
        }
        rows.append(
            {
                "id": node["id"],
                "short_name": node["attrs"].get("short_name", ""),
                "satisfied_by": counts["satisfies"],
                "partially_satisfied_by": counts["partially_satisfies"],
                "failed_by": counts["fails"],
            }
        )

    payload = {"count": len(rows), "desiderata": rows}
    if args.json:
        return payload

    print(f"  {'id':<5} {'satisfy':>7} {'partial':>7} {'fail':>5}  short name")
    for row in rows:
        print(
            f"  {row['id']:<5} {len(row['satisfied_by']):>7} "
            f"{len(row['partially_satisfied_by']):>7} {len(row['failed_by']):>5}  "
            f"{row['short_name']}"
        )
    return payload


def cmd_search(graph: Graph, args) -> dict:
    needle = args.query.lower()
    hits = []
    for node_id in sorted(graph.nodes):
        node = graph.nodes[node_id]
        haystack = [node_id.lower(), node["title"].lower()]
        haystack += [str(a).lower() for a in node["attrs"].get("aliases", []) or []]
        haystack.append(str(node["attrs"].get("summary", "")).lower())
        if any(needle in h for h in haystack):
            hits.append(
                {"id": node_id, "title": node["title"], "type": node["type"],
                 "path": node["path"]}
            )

    payload = {"count": len(hits), "results": hits}
    if args.json:
        return payload
    for hit in hits:
        print(f"  {hit['id']:<38} [{hit['type']}] {hit['title']}")
    print(f"\n{len(hits)} match(es)")
    return payload


def cmd_stats(graph: Graph, args) -> dict:
    payload = dict(graph.metadata)
    if args.json:
        return payload
    print(f"schema {payload.get('schema_version')}")
    print(f"{payload.get('node_count', 0)} nodes, {payload.get('edge_count', 0)} edges")
    if payload.get("node_counts"):
        print("\nnodes by type:")
        for key, value in payload["node_counts"].items():
            print(f"  {key:<16} {value}")
    if payload.get("edge_counts"):
        print("\nedges by type:")
        for key, value in payload["edge_counts"].items():
            print(f"  {key:<22} {value}")
    return payload


# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="query.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    sub = parser.add_subparsers(dest="command", required=True)

    p_node = sub.add_parser("node", help="show one node and all its edges")
    p_node.add_argument("id")
    p_node.set_defaults(func=cmd_node)

    p_nb = sub.add_parser("neighbors", help="walk outward from a node")
    p_nb.add_argument("id")
    p_nb.add_argument(
        "--edge-type", action="append", help="restrict to this edge type (repeatable)"
    )
    p_nb.add_argument("--direction", choices=["in", "out", "both"], default="both")
    p_nb.add_argument("--depth", type=int, default=1)
    p_nb.set_defaults(func=cmd_neighbors)

    p_path = sub.add_parser("path", help="shortest path between two nodes")
    p_path.add_argument("a")
    p_path.add_argument("b")
    p_path.set_defaults(func=cmd_path)

    p_filter = sub.add_parser("filter", help="find nodes by type, flags, and edges")
    p_filter.add_argument("--type")
    p_filter.add_argument("--status")
    p_filter.add_argument("--pq", help="true or false")
    p_filter.add_argument("--satisfies", action="append", metavar="D")
    p_filter.add_argument("--partially-satisfies", action="append", metavar="D")
    p_filter.add_argument("--fails", action="append", metavar="D")
    p_filter.add_argument(
        "--satisfies-or-partial",
        action="append",
        metavar="D",
        help="satisfied fully or partially",
    )
    p_filter.add_argument("--assumes", action="append", metavar="ID")
    p_filter.add_argument("--uses", action="append", metavar="ID")
    p_filter.set_defaults(func=cmd_filter)

    p_op = sub.add_parser("open-problems", help="list open problems")
    p_op.add_argument("--state", choices=["open", "partially-resolved", "resolved"])
    p_op.set_defaults(func=cmd_open_problems)

    p_des = sub.add_parser("desiderata", help="D1-D15 with a coverage tally")
    p_des.set_defaults(func=cmd_desiderata)

    p_search = sub.add_parser("search", help="substring search over ids and titles")
    p_search.add_argument("query")
    p_search.set_defaults(func=cmd_search)

    p_stats = sub.add_parser("stats", help="node and edge counts")
    p_stats.set_defaults(func=cmd_stats)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    graph = Graph.load(args.graph)
    result = args.func(graph, args)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
