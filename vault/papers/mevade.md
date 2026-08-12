---
id: mevade
type: paper
title: "MEVade: An MEV-Resistant Blockchain Design"
venue: IEEE ICBC 2023
year: 2023
status: published
peer_reviewed: true
source_depth: abstract
pq: false
url: https://ieeexplore.ieee.org/document/10174966/
authors: [julien-piet, varun-nair, sriram-subramanian]
---

Piet, Nair and Subramanian. Two Ethereum extensions, one for proof of work and one
for proof of stake, that aim to eliminate most MEV by randomizing execution order
*and* hiding transaction contents until inclusion.

## Why it is in this KB

Two reasons. First, disambiguation: it is frequently conflated with
[[choudhuri-garg-piet-policharla-2024]], which shares only Julien Piet as an author
and is a different paper with a different contribution. Second, and more usefully,
it makes the point that hiding contents is only half of MEV resistance. Ordering is
the other half, which is [[post-inclusion-ordering]].
