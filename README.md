# PQ Threshold Encryption Knowledge Base

Canonical knowledge base for **post-quantum threshold encryption for encrypted
mempools**: the schemes, what they assume, which of the D1-D15 encrypted-mempool
requirements each one meets, what has been measured, and what is still open.

178 nodes, 566 typed edges, 27 source PDFs. It works three ways at once.

**New here? Read [`vault/guides/start-here.md`](vault/guides/start-here.md).** It
explains the problem in plain language with no cryptography assumed, then hands you
off to whichever angle you need.

| mode | for | entry point |
|---|---|---|
| **Obsidian vault** | reading and editing as a human | `vault/` |
| **Agent skill** | asking an AI agent questions about the field | `skill/SKILL.md` |
| **Static site** | browsing with an interactive graph | GitHub Pages, built from `webapp/` |

The graph is generated from note frontmatter, so all three modes are the same data.
Frontmatter is the single source of truth; prose is for humans.

---

## 1. Obsidian

```bash
git clone https://github.com/pepae/pq-threshold-knowledge-graph
```

In Obsidian: **Open folder as vault**, and pick the `vault/` directory (not the
repo root). Wikilinks, graph view, backlinks and tags all work natively. No
plugins needed.

Start at `guides/start-here.md`. The `guides/` folder holds six narrative
explainers, each entering the same material from a different direction:

| guide | angle | for |
|---|---|---|
| `start-here` | orientation | the problem in plain language, 10 min, no crypto assumed |
| `the-goals` | goals | D1-D15 explained, and which requirements fight each other |
| `the-problems` | problems | attacks, two impossibility results, the 7 open problems |
| `the-history` | history | 2010 to 2026, so each result answers the previous limitation |
| `choosing-a-scheme` | decisions | comparison tables and a recommendation per deployment |
| `glossary` | vocabulary | every term in one line |

Guides are ordinary nodes with `covers` edges, so any note you land on deep in the
graph tells you which guides explain it.

## 2. Agent skill

The skill teaches an agent what the KB covers, how to query the graph, and when to
read a full note instead. It ships a standard-library-only CLI, so there is no
install step.

**Claude Code**, project scope:

```bash
git clone https://github.com/pepae/pq-threshold-knowledge-graph
mkdir -p .claude/skills
ln -s "$(pwd)/pq-threshold-knowledge-graph/skill" .claude/skills/pq-threshold-kb
```

Or user scope, available in every project:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/pq-threshold-knowledge-graph/skill" ~/.claude/skills/pq-threshold-kb
```

Copy the directory instead of symlinking if you prefer. Then start Claude Code and
ask something the KB covers, for example *"which post-quantum threshold schemes
give epoch-free batching?"*. Confirm the skill is visible with `/skills`.

Any other agent: point it at `skill/SKILL.md`, which documents the query interface
and the `graph/graph.json` format.

Query it yourself the same way an agent does:

```bash
python3 skill/scripts/query.py stats
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
python3 skill/scripts/query.py node blt-batch-ibe
python3 skill/scripts/query.py path bendlin-damgard sjtu-adaptive-threshold-decryption
python3 skill/scripts/query.py open-problems
python3 skill/scripts/query.py desiderata
```

Add `--json` for machine-readable output. See `skill/SKILL.md` for worked examples.

## 3. Static site

Two panes, Obsidian style: the note on the left, the graph on the right. Dark by
default, with a light theme on the toggle. No backend, no external requests, no
libraries.

The graph is drawn on canvas with a layout that runs to convergence *before* the
first frame, so nothing animates and nothing jitters. Small neighbourhoods get a
plain force-directed layout. The whole graph, 115 visible nodes across nine types,
gets a **clustered** layout instead: each type is packed into its own disc with its
hubs at the centre, the discs sit on a ring sized by population, and only
intra-cluster edges pull. That turns what is otherwise a hairball into nine labelled
neighbourhoods you can read in one glance, with the traffic between them visible.

Build and serve locally:

```bash
pip install -r requirements.txt
python3 scripts/build_webapp.py          # -> dist/
python3 -m http.server 8000 -d dist      # then open http://localhost:8000
```

Live at **<https://pepae.github.io/pq-threshold-knowledge-graph/>**.

CI deploys on every push to the repository's **default branch**, whatever it is
named, so renaming the default branch later will not silently stop deployments. To
enable it on a fork: **Settings > Pages > Source: GitHub Actions**.

Graph controls: click a node to navigate, drag to pan, scroll to zoom, hover to
isolate a node and its neighbours, click a legend entry to show or hide a type.
**Expand** gives the graph the whole window, which is the view worth looking at.
`person` nodes are hidden by default because they are 63 of the 178; re-enable them
from the legend.

Keyboard: `/` focuses search, `g` toggles the whole graph, `e` expands.

Labels are drawn most-important-first and any that would collide is dropped, so the
view stays readable at every zoom level rather than turning into overlapping text.

---

## What is in it

| type | count | notes |
|---|---|---|
| `guide` | 6 | narrative explainers, the way in |
| `scheme` | 27 | Bendlin-Damgard 2010 through 2026 preprints |
| `person` | 63 | public information only |
| `technique` | 27 | noise flooding, KH-PPRF, zero-sharing masks, vector commitments, LaBRADOR |
| `assumption` | 21 | LWE, Module-LWE, decomposed LWE, l-succinct LWE, q-SDH, q-SBDHT, DBDH, LOMDH, GGM, AGM, ROM, QROM |
| `desideratum` | 15 | D1-D15 |
| `open-problem` | 7 | each with *where we stand* and *what needs solving* |
| `attack` | 5 | attacks and impossibility results |
| `paper` | 4 | records for artifacts cited as papers rather than schemes |
| `implementation` | 3 | with measured numbers |

Reading order for a newcomer: `start-here`, then whichever of `the-goals`,
`the-problems`, `the-history` or `choosing-a-scheme` matches why you came.

`papers/pdf/` holds the source PDFs. `papers/WANTED.md` lists what is still
missing and is regenerated by `scripts/check_pdfs.py`, so it cannot go stale.

### On the D1-D15 numbering

The desiderata come from
[Benedikt Wagner's Ethereum Foundation note](https://notes.ethereum.org/@b-wagn/SkZxlQEYbg).
**That note contains no numbered list**: its criteria are an unnumbered nested
bullet list. The D1-D15 identifiers here are a flattening of it, taken from
`bench/ef_requirements.py` in [pepae/pq-threshold](https://github.com/pepae/pq-threshold)
so that the two artifacts agree on what each number means.

`vault/desiderata/_wagner-mapping.md` gives the exact mapping, the four
sub-bullets folded into parents, and the one top-level bullet that receives no
number. Read it before quoting a specific D number.

### How to read a claim

Notes carry their own provenance, so you can tell a verified number from an
inherited one:

- `source_depth` - `full-text` means checked against the paper, `abstract` means
  only the abstract was available, `repo` means from a codebase
- `peer_reviewed: false` - treat as a preprint claim
- `self_assessed: true` - the evaluation is by the authors of the thing evaluated
- `unverified: true` - the record itself is unconfirmed; do not cite it
- `assumptions_pending: true` - assumptions are absent because the source text was
  unavailable, not because the scheme has none
- `disputes` - sources disagree, and the note says how instead of picking a side

**TACET** is an unpublished, unreviewed working draft by this repository's owner.
It is marked `status: draft`, `maturity: experimental`, `self_assessed: true`, and
carries a banner. It is included for its measurements and for two audit findings
that generalise beyond it, not as a peer-reviewed result. Filter it out with
`--status published`.

---

## Local development

```bash
pip install -r requirements.txt

python3 scripts/test_kb.py            # 31 self-tests for the parser and builder
python3 scripts/build_graph.py        # vault frontmatter -> graph/graph.json
python3 scripts/validate.py           # links, schema, quality bar, orphans
python3 scripts/check_pdfs.py --write # reconcile PDFs, regenerate WANTED.md
python3 scripts/build_webapp.py       # -> dist/
```

`build_graph.py` hard-fails on unknown ids, edges to nonexistent nodes, unknown
types, unknown frontmatter keys, domain or range violations, and duplicate ids.
Its output is deterministic, so `--check` asserts the committed graph is current.
CI runs all of the above on every pull request.

## Adding a paper or fixing a claim

```bash
python3 scripts/add_paper.py --eprint 2026/1234 --type scheme --id some-scheme
# edit the note, resolve every TODO, then:
python3 scripts/build_graph.py && python3 scripts/validate.py
```

The scaffolder prefills the title from `papers/pdf/<eprint>.pdf` when it is there.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the frontmatter reference and the house
rules, and `papers/pdf/README.md` for how to add source PDFs.

## Licence

Vault prose and the graph: CC BY 4.0. Scripts and webapp: MIT.
PDFs in `papers/pdf/` remain under their authors' terms; see `papers/SOURCES.md`.
