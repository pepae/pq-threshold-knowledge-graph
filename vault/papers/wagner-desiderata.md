---
id: wagner-desiderata
type: paper
title: Encrypted Mempool / Threshold Encryption Literature
aliases: ["Wagner's note", "EF note", "Wagner desiderata"]
status: draft
peer_reviewed: false
source_depth: full-text
url: https://notes.ethereum.org/@b-wagn/SkZxlQEYbg
authors: [benedikt-wagner]
---

Benedikt Wagner's working note collecting threshold encryption literature relevant
to encrypted mempools, together with the criteria this KB numbers D1-D15. The note
describes itself as work in progress and "mostly for my own, to keep track of
literature".

## Why it is the KB's root document

Everything in `vault/desiderata/` derives from its "Criteria / Properties that we
care about" section, and its per-paper annotations are used throughout as a
secondary source where a paper's own text was unavailable. Where a note says
"Wagner's survey records...", this is the source.

## Important: the note contains no numbered desiderata

The criteria are an unnumbered nested bullet list of thirteen top-level items, some
with sub-bullets. The D1-D15 numbering used here is a flattening of that list,
taken from `bench/ef_requirements.py` in the `pepae/pq-threshold` repository so that
the KB and that project's scorecard agree. Each desideratum note carries its source
bullet verbatim in `wagner_bullet`. See `vault/desiderata/_wagner-mapping.md` for
the full mapping, including the one bullet that receives no number.

## Motivation it records

The note frames the problem with a number worth keeping: "About every 30 seconds an
Ethereum user gets sandwiched on average." And it gives the template every scheme in
this KB is trying to fill: user sends a threshold-encrypted transaction, it is
included in block i, a committee decrypts, a short decryption key is revealed, the
transaction executes in block i+1.
