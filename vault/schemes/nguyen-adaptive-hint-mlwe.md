---
id: nguyen-adaptive-hint-mlwe
type: scheme
title: Threshold Regev PKE from adaptive Hint-MLWE
eprint: "2026/1585"
year: 2026
status: preprint
peer_reviewed: false
unverified: true
source_depth: abstract
pq: true
assumptions: [hint-mlwe, mlwe]
techniques: [shamir-secret-sharing]
satisfies: [D3, D8]
partially_satisfies: [D6]
fails: [D2, D14]
---

Proves threshold Regev PKE secure from an adaptive Hint-MLWE assumption.

## Status of this note

Title and framing come from a search result and Wagner's TODO list, not from the
paper, hence `unverified: true`. It is in the KB because it is the other current
attempt at the same target as
[[sjtu-adaptive-threshold-decryption]]: adaptive security for a lattice threshold
scheme, reached by assuming a hint variant rather than by conditioning the flooding
analysis on hints. If that framing is right, the two papers are the two natural
answers to the same question and belong side by side. Confirm before relying on it.
