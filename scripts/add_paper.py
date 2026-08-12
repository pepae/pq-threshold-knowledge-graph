#!/usr/bin/env python3
"""Scaffold a new vault note, so adding a paper is a two-minute job.

Prefills from the local PDF when one is present in papers/pdf/, writes a note
with the right required fields for its type, and leaves TODO markers where a human
or an agent has to decide something.

    python3 scripts/add_paper.py --eprint 2026/1234 --type scheme --id my-scheme
    python3 scripts/add_paper.py --type open-problem --id some-gap --title "Some gap"

Then edit the note, and run:

    python3 scripts/build_graph.py && python3 scripts/validate.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from kb import REPO_ROOT, VAULT_DIR, id_pattern_for, load_schema

PDF_DIR = REPO_ROOT / "papers" / "pdf"

TODO = "TODO"


def pdf_first_page(eprint: str) -> str | None:
    path = PDF_DIR / (eprint.replace("/", "-") + ".pdf")
    if not path.exists():
        return None
    try:
        import pypdf
    except ImportError:
        print("note: pip install pypdf to prefill from the PDF", file=sys.stderr)
        return None
    try:
        text = pypdf.PdfReader(str(path)).pages[0].extract_text() or ""
    except Exception as exc:  # noqa: BLE001 - a bad PDF must not be fatal
        print(f"note: could not read {path.name}: {exc}", file=sys.stderr)
        return None
    return re.sub(r"[ \t]+", " ", text)


def guess_title(page: str) -> str | None:
    for line in (l.strip() for l in page.splitlines()):
        if len(line) > 12 and not line.lower().startswith("cryptology eprint"):
            return re.sub(r"\s+", " ", line)
    return None


def build(args, schema: dict) -> str:
    type_def = schema["node_types"][args.type]
    lines = ["---", f"id: {args.id}", f"type: {args.type}", f"title: {args.title}"]

    if args.eprint:
        lines.append(f'eprint: "{args.eprint}"')
        year = args.eprint.split("/")[0]
        lines.append(f"year: {year}")
    if args.type in ("scheme", "paper", "attack"):
        lines.append(f"status: {args.status}")
        lines.append("peer_reviewed: false")
        lines.append(
            f"source_depth: {'full-text' if args.has_pdf else 'abstract'}"
        )
        lines.append(f"# authors: [{TODO}-person-ids]  # creates `authored` edges")
    if args.type == "scheme":
        lines.append(f"pq: false  # {TODO}: true if plausibly post-quantum")
        lines.append(
            f"assumptions: []  # {TODO}: required, or set assumptions_pending: true"
        )
        lines.append(f"techniques: []  # optional `uses` edges")
        lines.append(f"satisfies: []  # {TODO}: at least one desideratum edge required")
        lines.append("partially_satisfies: []")
        lines.append("fails: []")
        lines.append("# builds_on: []")
        lines.append("# superseded_by: []")
    if args.type == "open-problem":
        lines.append("state: open")
        lines.append("# opened_by: [wagner-desiderata]")
        lines.append("# resolved_by: []")
    if args.type == "implementation":
        lines.append(f"repo: {TODO}")
        lines.append("# implements: []")
    if args.type == "attack":
        lines.append(f"# attacks: [{TODO}-scheme-id]")
    if args.type == "desideratum":
        lines.append(f"short_name: {TODO}")
    if args.type == "person":
        lines.append(f"# affiliation: {TODO}")
    lines.append("---")

    if args.type == "scheme":
        body = f"""
One-paragraph summary. What it is, who wrote it, what it changes.

## Key mechanism

How it works, concretely enough that a reader can tell it apart from its
neighbours.

## Concrete numbers

Sizes, timings, modulus. Only numbers the source actually states. If the full text
was unavailable, say so and leave `source_depth: abstract`.

## Desiderata

Which of D1-D15 it satisfies, partially satisfies and fails, **and why**. The
frontmatter carries the edges; this section carries the reasoning. A partial
rating with no explanation here is an incomplete note.

## Known attacks or limitations

## Relevance to encrypted mempools

Why a reader building an encrypted mempool should care, or should not.
"""
    elif args.type == "open-problem":
        body = """
## Statement

What exactly is open. Quote the source if it was stated in a paper.

## Where we stand

What is known, and which nodes represent it. Distinguish "solved in theory" from
"solved in practice"; that gap is usually the point.

## What needs to be solved

The concrete next step, not a restatement of the problem.
"""
    else:
        body = f"""
{TODO}: prose. Terse and factual. Link related nodes with [[wikilinks]].
"""

    return "\n".join(lines) + "\n" + body


def main() -> int:
    schema = load_schema()
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--id", required=True, help="node id, lowercase-kebab")
    parser.add_argument("--type", required=True, choices=sorted(schema["node_types"]))
    parser.add_argument("--title")
    parser.add_argument("--eprint", help="e.g. 2026/1234")
    parser.add_argument("--status", default="preprint", choices=schema["enums"]["status"])
    parser.add_argument("--force", action="store_true", help="overwrite an existing note")
    args = parser.parse_args()

    pattern = id_pattern_for(args.type, schema)
    if not re.match(pattern, args.id):
        return fail(f"id {args.id!r} must match {pattern} for type {args.type!r}")
    if args.eprint and not re.match(r"^\d{4}/\d{3,4}$", args.eprint):
        return fail(f"eprint {args.eprint!r} must look like 2026/1234")

    page = pdf_first_page(args.eprint) if args.eprint else None
    args.has_pdf = page is not None
    if not args.title:
        args.title = (guess_title(page) if page else None) or f"{TODO} title"
        if page:
            print(f"prefilled title from PDF: {args.title}")

    target = VAULT_DIR / schema["node_types"][args.type]["dir"] / f"{args.id}.md"
    if target.exists() and not args.force:
        return fail(f"{target.relative_to(REPO_ROOT)} already exists (use --force)")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(args, schema), encoding="utf-8")

    rel = target.relative_to(REPO_ROOT)
    print(f"created {rel}")
    if args.eprint and not args.has_pdf:
        name = args.eprint.replace("/", "-") + ".pdf"
        print(f"\nno local PDF. Add papers/pdf/{name} from "
              f"https://eprint.iacr.org/{args.eprint}.pdf, or add an entry to "
              "papers/wanted.yml")
    if page:
        head = " ".join(page.split())[:300]
        print(f"\nPDF first page, to fill in authors and the summary:\n  {head}...")
    print(f"\nnext:\n  1. edit {rel}, resolve every {TODO}\n"
          "  2. python3 scripts/build_graph.py\n"
          "  3. python3 scripts/validate.py\n"
          "  4. python3 scripts/check_pdfs.py --write")
    return 0


def fail(msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
