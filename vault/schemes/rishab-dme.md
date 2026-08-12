---
id: rishab-dme
type: scheme
title: Distributed monotone-policy encryption from l-decomposed LWE
eprint: "2026/372"
year: 2026
status: preprint
peer_reviewed: false
source_depth: mixed
pq: true
silent_setup: true
assumptions: [decomposed-lwe, rom]
techniques: [monotone-policy-encryption, silent-setup]
satisfies: [D1, D2, D8]
partially_satisfies: [D5]
fails: [D14]
---

A second lattice route to distributed monotone-policy encryption, selective and
static under l-decomposed LWE with a transparent setup.

## Position in the literature

Concurrent with [[champion-wu-monotone-dnf]]: two independent lattice routes to
distributed monotone-policy encryption, both in the [[rom]], both with compact
individual public keys and a transparent setup, both plausibly post-quantum from a
decomposed-LWE style assumption.
[[hall-andersen-simkin-wagner-silent]] describes both as subsequent to its own work
and summarises the trade the same way: compact keys and transparent setup, at the
price of the random oracle model.

That two groups arrived here at once is the signal worth recording. Post-quantum
silent setup stopped being speculative in 2026.

## Still to extract

The concrete parameters and the exact form of the l-decomposed LWE assumption have
not been read out of the PDF yet. Prose above is sourced from the abstract and from
how neighbouring papers characterise it.
