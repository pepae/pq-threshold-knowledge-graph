---
id: aptos-batched-ibe
type: scheme
title: APTOS batched threshold IBE
eprint: "2024/1575"
year: 2024
status: preprint
peer_reviewed: false
unverified: true
source_depth: abstract
pq: false
batched: true
assumptions_pending: true
techniques: [threshold-ibe, batched-threshold-encryption]
satisfies: [D12, D14]
fails: [D2, D8]
---

Agarwal, Fernando and Pinkas. Pairing-based batched threshold IBE with a DKG rather
than silent setup.

## Status of this note

Recorded from Wagner's survey only; neither the abstract page nor the PDF has been
read, so `unverified: true` and the desiderata edges are provisional. It is listed
in `papers/WANTED.md`. The reason to keep the node despite that is structural: it is
one of only two batched threshold IBE constructions in the KB, so [[blt-batch-ibe]]
would otherwise look unique when it is not.
