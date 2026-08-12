---
id: aptos-batched-ibe
type: scheme
title: APTOS batched threshold IBE
eprint: "2024/1575"
year: 2024
status: preprint
peer_reviewed: false
source_depth: mixed
pq: false
batched: true
assumptions: [ggm]
techniques: [threshold-ibe, batched-threshold-encryption]
satisfies: [D12, D14]
fails: [D2, D8]
---

Agarwal, Fernando and Pinkas. Pairing-based batched threshold IBE with a DKG rather
than silent setup.

## Key mechanism

A batched IBE construction over Type-3 pairings, building on the identity-based
encryption scheme of Boneh et al. (Asiacrypt 2001), proven secure in the [[ggm]].
The paper states the blockchain application directly: encrypt transactions to a
block and open only the transactions that were included.

## Why it matters next to BLT

It is one of only two batched threshold IBE constructions in the KB, so
[[blt-batch-ibe]] should not be read as unique. The instructive contrast is the
cost of being post-quantum: this scheme is concretely efficient over pairings with
a GGM proof, while BLT is plausibly post-quantum from [[lwe]] and cannot be run at
secure parameters. Same primitive, opposite trade.
