# Contributing

Frontmatter is the single source of truth for the graph. Prose is for humans. An
edge that exists only in prose does not exist.

`graph/schema.json` defines every legal node type, field and edge type. The
scripts read it, so adding a field there is what makes it legal in a note. Nothing
is hardcoded.

## Setup

```bash
pip install -r requirements.txt
```

Python 3.11+, PyYAML for the build, `markdown` for the site, `pypdf` only if you
want `add_paper.py` to prefill from a PDF.

## Adding a node

```bash
python3 scripts/add_paper.py --eprint 2026/1234 --type scheme --id some-scheme
```

This writes a note with the right required fields for its type and `TODO` markers
where you have to decide something. Then:

1. Edit the note. Resolve every `TODO`.
2. Set the edges in frontmatter, not in prose.
3. Run the checks below.

Doing it by hand is fine too. The filename stem must equal the `id`, and the note
must live in the directory its type declares (`schemes/`, `papers/`, `concepts/`,
`people/`, `desiderata/`, `open-problems/`, `implementations/`, `attacks/`). The
build enforces both.

## Running the checks

```bash
python3 scripts/build_graph.py        # rebuild graph/graph.json
python3 scripts/validate.py           # links, quality bar, orphans, citations
python3 scripts/check_pdfs.py --write # regenerate papers/WANTED.md
python3 scripts/test_kb.py            # self-tests, if you changed the scripts
```

Commit `graph/graph.json` and `papers/WANTED.md` along with your note. CI asserts
both are current.

`build_graph.py` **hard-fails** on: unknown ids, edges to nonexistent nodes,
unknown node types, unknown frontmatter keys, domain or range violations,
duplicate ids, self-edges, a filename that disagrees with its id, a note in the
wrong directory, bad enum values, and wrong value types.

`validate.py` additionally **errors** on: a wikilink that resolves to nothing, a
scheme with no assumption edge, a scheme with no desideratum edge, a scheme with no
status, and a malformed eprint number. It **warns** about orphan nodes, desiderata
nothing points at, unsourced records, and schemes with `assumptions_pending`.
Warnings are a work queue, not a failure. `--strict` turns them into errors.

## House rules

These are the things that make the KB trustworthy rather than merely large.

- **No invented citations.** If you cannot verify an eprint number, set
  `unverified: true`. Never guess one to fill a field.
- **The paper wins.** Where a draft, a conversation, or a secondary source
  conflicts with the published paper, the paper is right. Do not silently pick a
  side: record the disagreement in `disputes`.
- **Do not state numbers your source does not give.** If only the abstract was
  available, set `source_depth: abstract` and keep the note to what the abstract
  says. An honest thin note beats a rich invented one.
- **Explain every partial rating.** `partially_satisfies` with no prose saying
  which part fails is an incomplete note.
- **Terse and factual.** No filler, no hedging, no restating the title.
- **Wikilink generously.** `[[wikilinks]]` in prose are checked by CI and are how
  the vault reads in Obsidian.
- Add wanted papers to `papers/wanted.yml`. `papers/WANTED.md` is generated.

## The quality bar for a scheme note

Enforced by `validate.py`:

- at least one `assumes` edge, or `assumptions_pending: true` with the paper listed
  in `papers/wanted.yml`
- at least one desideratum edge (`satisfies`, `partially_satisfies` or `fails`)
- a `status`

Expected by convention, not machine-checked:

- a one-paragraph summary
- a *Key mechanism* section
- *Desiderata*, saying **why** for each rating
- concrete numbers, if the source publishes them
- known attacks or limitations
- a *Relevance to encrypted mempools* section

## Frontmatter reference

`graph/schema.json` is authoritative. This is the working summary.

### Every node

| field | type | notes |
|---|---|---|
| `id` | string | required, lowercase-kebab; must equal the filename stem |
| `type` | string | required, one of the node types below |
| `title` | string | required |
| `aliases` | list | extra names wikilinks and search resolve |
| `tags`, `summary`, `notes` | | free text |
| `url`, `doi` | string | |
| `source_depth` | enum | `full-text`, `abstract`, `repo`, `mixed` |
| `unverified` | bool | the record itself is unconfirmed |
| `disputes` | list of strings | how sources disagree |

Desiderata are the one exception to the id pattern: they use `D1` to `D15`, via a
per-type `id_pattern` in the schema.

### Node types

| type | directory | required beyond the common fields |
|---|---|---|
| `scheme` | `schemes/` | `status` |
| `paper` | `papers/` | `status` |
| `attack` | `attacks/` | `status` |
| `person` | `people/` | none |
| `assumption` | `concepts/` | none |
| `technique` | `concepts/` | none |
| `desideratum` | `desiderata/` | `short_name` |
| `open-problem` | `open-problems/` | `state` |
| `implementation` | `implementations/` | `repo` |

Notable optional fields: `eprint` (as `"2024/263"`), `venue`, `year`, `authors`,
`pq`, `peer_reviewed`, `status`, `maturity`, `self_assessed`,
`assumptions_pending`, `silent_setup`, `batched`, `epoch_free`, `modulus`,
`ciphertext_size`, `share_size`, `public_key_size`, `timings`, `falsifiable`,
`family`, `state`, `runnable`, `measured`, `language`, `affiliation`,
`wagner_bullet`.

Enums: `status` is `published | preprint | draft | broken`; `state` is
`open | partially-resolved | resolved`; `maturity` is
`experimental | prototype | mature`.

### Edges

Write the frontmatter key; the build normalizes direction. Reverse-direction keys
exist so an edge can be declared on whichever note it reads naturally on.

| key | edge | direction | domain -> range |
|---|---|---|---|
| `builds_on` | `builds_on` | forward | scheme, paper, attack -> scheme, paper |
| `supersedes` | `supersedes` | forward | scheme, paper -> scheme, paper |
| `superseded_by` | `supersedes` | reversed | |
| `presented_in` | `presented_in` | forward | scheme -> paper |
| `satisfies` | `satisfies` | forward | scheme -> desideratum |
| `partially_satisfies` | `partially_satisfies` | forward | scheme -> desideratum |
| `fails` | `fails` | forward | scheme -> desideratum |
| `assumptions`, `assumes` | `assumes` | forward | scheme, technique, paper -> assumption |
| `techniques`, `uses` | `uses` | forward | scheme, implementation, technique, paper -> technique |
| `reduces_to` | `reduces_to` | forward | assumption -> assumption |
| `attacks` | `attacks` | forward | attack -> scheme |
| `attacked_by` | `attacks` | reversed | |
| `breaks`, `broken_by` | `breaks` | forward, reversed | attack -> scheme |
| `implements`, `implemented_by` | `implements` | forward, reversed | implementation -> scheme |
| `authors` | `authored` | reversed | person -> paper, scheme, attack |
| `resolves`, `resolved_by` | `resolves` | forward, reversed | paper, scheme -> open-problem |
| `opens`, `opened_by` | `opens` | forward, reversed | paper, scheme, attack, implementation -> open-problem |

So `authors: [dan-boneh]` on a scheme creates `dan-boneh --authored--> scheme`, and
`superseded_by: [beast-mev]` on BEAT-MEV creates
`beast-mev --supersedes--> beat-mev`. Only the forward form appears in
`graph.json`.

### Example

```yaml
---
id: beat-mev
type: scheme
title: BEAT-MEV
eprint: "2024/1533"
venue: USENIX Security 2025
year: 2025
status: published
peer_reviewed: true
source_depth: full-text
pq: false
epoch_free: true
authors: [jan-bormet, sebastian-faust, hussien-othman, ziyan-qu]
assumptions: [ddh, agm]
techniques: [kh-pprf, batched-threshold-encryption]
satisfies: [D3, D7, D11, D13, D14]
partially_satisfies: [D4, D15]
fails: [D2, D8, D10]
superseded_by: [beast-mev]
attacked_by: [index-collision-censorship]
---
```

## Changing the schema

Editing `graph/schema.json` changes what is legal everywhere. Add a field or edge
type there first, then use it. Run `python3 scripts/test_kb.py` afterwards: the
tests assert the checks still fire.

Renumbering the desiderata is a breaking change. The ids appear in edges across 27
scheme notes and in `bench/ef_requirements.py` in a separate repository. If you
change them, change both, or the two will silently disagree about what D14 means.
