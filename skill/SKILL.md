---
name: pq-threshold-kb
description: >-
  Knowledge base on post-quantum threshold encryption for encrypted mempools.
  Use when asked about threshold encryption schemes, encrypted mempools, MEV
  protection via encryption, batched threshold decryption, silent setup, lattice
  threshold decryption, noise flooding, the D1-D15 encrypted-mempool desiderata,
  or which open problems in this area are still open. Answers "which scheme
  satisfies X", "what is the state of the art for Y", "who wrote Z", and "what
  still needs to be solved".
---

# PQ threshold encryption for encrypted mempools

A knowledge graph plus wiki covering threshold encryption schemes evaluated
against the requirements of an Ethereum-style encrypted mempool.

## What is in here

178 nodes, 566 typed edges.

| type | count | what it is |
|---|---|---|
| `guide` | 6 | narrative explainers, one per angle: orientation, goals, problems, history, decisions, vocabulary |
| `scheme` | 27 | named constructions, from Bendlin-Damgard 2010 to 2026 preprints |
| `person` | 63 | authors, public information only |
| `technique` | 27 | building blocks: noise flooding, KH-PPRF, zero-sharing masks, vector commitments |
| `assumption` | 21 | LWE, Module-LWE, decomposed LWE, l-succinct LWE, q-SDH, q-SBDHT, DBDH, LOMDH, GGM, AGM, ROM, QROM |
| `desideratum` | 15 | D1-D15, the encrypted-mempool requirements |
| `open-problem` | 7 | with explicit "where we stand" and "what needs solving" |
| `attack` | 5 | concrete attacks and impossibility results |
| `paper` | 4 | bibliographic records for artifacts cited as papers |
| `implementation` | 3 | codebases, with measured numbers |

**The D1-D15 desiderata** come from Benedikt Wagner's Ethereum Foundation note.
That note has no numbered list; the numbering here is a documented flattening.
Read `vault/desiderata/_wagner-mapping.md` before relying on a specific number,
and note that D14 means *epoch-free batching* and D8 means *post-quantum*.

## Answering a broad question: read a guide

For open-ended questions ("what is this field about", "what should I build on",
"what is still unsolved", "how did we get here"), the guides already contain the
synthesis and are cheaper and more accurate than assembling one from the graph:

| guide | use it for |
|---|---|
| `start-here` | the problem in plain language, and the honest state of the art |
| `the-goals` | D1-D15 explained, plus the five real tensions between them |
| `the-problems` | attacks, the two impossibility results, all 7 open problems |
| `the-history` | why the schemes look the way they do, 2010 to 2026 |
| `choosing-a-scheme` | comparison tables and a recommendation per deployment shape |
| `glossary` | one-line definitions, for explaining a term to a non-specialist |

```bash
python3 skill/scripts/query.py filter --type guide      # list them
python3 skill/scripts/query.py node start-here          # then read vault/guides/start-here.md
```

Every non-guide node has incoming `covers` edges naming the guides that explain it,
so you can always find the narrative a deep node belongs to:

```bash
python3 skill/scripts/query.py neighbors beat-mev --edge-type covers --direction in
```

If the user asks a plain-language question, prefer the guides' framing over
inventing your own: they are written to be correct about the caveats, especially
around what is post-quantum and what only looks it.

## Two ways in, and when to use each

**Query the graph** when the question is structural: which schemes satisfy a
property, what does this rest on, what superseded what, who wrote what, is this
still open. The graph is complete and typed, so a query gives you a definitive
answer.

**Read the vault note** when the question is *why*. Frontmatter records that
BEAT-MEV partially satisfies D4; only the note says the evaluated variant is the
CPA one. Every non-obvious rating is explained in prose, and the notes carry the
concrete numbers, the caveats, and the disagreements.

Rule of thumb: for a broad question read the relevant guide; for a specific
structural question query the graph; for a "why" question read the scheme note.
Do not try to answer a "why" question from `graph.json` alone.

## Running queries

`skill/scripts/query.py` uses only the standard library. No install step.

```bash
python3 skill/scripts/query.py stats                       # what is in the graph
python3 skill/scripts/query.py node beat-mev               # one node and all its edges
python3 skill/scripts/query.py neighbors pilvi --edge-type assumes
python3 skill/scripts/query.py path bendlin-damgard tacet  # shortest connection
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
python3 skill/scripts/query.py open-problems
python3 skill/scripts/query.py desiderata                  # D1-D15 coverage tally
python3 skill/scripts/query.py search flooding
```

Add `--json` to any subcommand for machine-readable output. Node references
accept an id, a title, an alias, or a unique substring, case-insensitively, so
`node BEAT-MEV` and `node beat-mev` both work.

Useful flags on `filter`: `--type`, `--status`, `--pq true|false`,
`--satisfies D`, `--partially-satisfies D`, `--fails D`,
`--satisfies-or-partial D`, `--assumes ID`, `--uses ID`. Repeat a flag to AND
conditions.

Loading `graph/graph.json` directly is also fine. Its shape:

```json
{"metadata": {"node_count": 178, "edge_count": 566, "node_counts": {...}},
 "nodes": [{"id": "beat-mev", "type": "scheme", "title": "BEAT-MEV",
            "path": "vault/schemes/beat-mev.md", "attrs": {"pq": false, ...}}],
 "edges": [{"source": "beat-mev", "type": "satisfies", "target": "D14",
            "declared_in": "beat-mev"}]}
```

Edge types: `builds_on`, `supersedes`, `presented_in`, `satisfies`,
`partially_satisfies`, `fails`, `assumes`, `uses`, `reduces_to`, `attacks`,
`breaks`, `implements`, `authored`, `resolves`, `opens`, `covers`. Every edge points one
way only; reverse-direction frontmatter keys are normalized at build time.

## Worked examples

### 1. Which post-quantum schemes give epoch-free batching?

```bash
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
```

Returns `blt-batch-ibe` and TACET. Then read `vault/schemes/blt-batch-ibe.md`,
because the interesting part is not the list: BLT achieves succinctness in theory
while `blt25-implementation` records that its secure parameters need matrices with
about 10^9 columns and do not run. The honest answer is "one published candidate,
not runnable yet, plus one unreviewed draft".

### 2. What is actually blocking a post-quantum encrypted mempool?

```bash
python3 skill/scripts/query.py open-problems
python3 skill/scripts/query.py node sublinear-pq-batch-decryption
```

The open-problem notes are written to answer this directly. Each has a
*Statement*, a *Where we stand* and a *What needs to be solved*. For the sharpest
single answer read `sublinear-pq-batch-decryption`: the cheap lattice route is
impossible, the succinct route does not run, and the one measured post-quantum
batched scheme costs 1.9 MB per ciphertext and 327 s to combine at batch 512.

### 3. How did we get from Regev encryption to a modern scheme?

```bash
python3 skill/scripts/query.py path bendlin-damgard sjtu-adaptive-threshold-decryption
python3 skill/scripts/query.py neighbors polynomial-noise-flooding --edge-type uses --direction in
```

The path shows the lineage. The second query shows the three distinct routes to a
polynomial modulus (Renyi divergence, Gaussian-vs-Gaussian, min-entropy given
hints), which is the actual content of that thread of the literature.

### 4. Which desiderata does nothing satisfy?

```bash
python3 skill/scripts/query.py desiderata
```

The tally per desideratum shows where the field is thin. Combine with a filter to
test a specific combination:

```bash
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D2 --satisfies D14
```

An empty result is the finding: post-quantum, silent setup, and batching together
is [silent-pq-threshold-t-of-n](../vault/open-problems/silent-pq-threshold-t-of-n.md).

## Reading a note correctly

Frontmatter fields that change how much weight a claim carries:

- `status`: `published`, `preprint`, `draft`, `broken`
- `peer_reviewed`: absent or `false` means take it as a preprint claim
- `source_depth`: `full-text` (verified against the paper), `abstract` (only the
  abstract was available), `repo`, `mixed`
- `self_assessed: true`: the evaluation is by the authors of the thing evaluated
- `unverified: true`: the record itself is not confirmed, do not cite it
- `assumptions_pending: true`: assumptions are not recorded because the source
  text was unavailable, rather than because the scheme has none
- `disputes`: sources disagree, and the note says how, instead of picking a side

**TACET is a special case.** It is an unpublished, unreviewed working draft
(`status: draft`, `maturity: experimental`, `self_assessed: true`). Do not present
it alongside published schemes without saying so. Its value is the measurements
and the two audit findings promoted to their own nodes.

To exclude unreviewed material from an answer:

```bash
python3 skill/scripts/query.py filter --type scheme --status published
```

## Keeping the KB current

When a new paper appears, or a claim here turns out to be wrong:

```bash
# 1. scaffold a node (reads papers/pdf/<eprint>.pdf if present, to prefill)
python3 scripts/add_paper.py --eprint 2026/1234 --type scheme --id some-scheme

# 2. edit the note: fill prose, set assumptions/satisfies/builds_on edges,
#    set source_depth, remove the TODO markers

# 3. rebuild and check
python3 scripts/build_graph.py
python3 scripts/validate.py
python3 scripts/check_pdfs.py --write
```

`build_graph.py` hard-fails on unknown ids, edges to nonexistent nodes, unknown
types, unknown frontmatter keys, domain or range violations, and duplicate ids.
`validate.py` additionally checks wikilinks, the scheme quality bar (every scheme
needs an assumption edge, a desideratum edge and a status), eprint format, orphan
nodes, and desiderata with nothing pointing at them. CI runs all of it, so a
malformed contribution cannot land.

Rules to follow when editing:

- Frontmatter is the single source of truth for the graph. Prose is for humans.
  An edge that only exists in prose does not exist.
- Never invent an eprint number. If it cannot be verified, set `unverified: true`.
- If a paper's full text is unavailable, set `source_depth: abstract` and do not
  state numbers the abstract does not give.
- Where the conversation, a draft, or a secondary source conflicts with the
  published paper, the paper wins. Record the disagreement in `disputes` rather
  than silently choosing.
- Add a wanted paper to `papers/wanted.yml`, never to `papers/WANTED.md`, which is
  generated.
