---
id: cgpp-bte
type: scheme
title: CGPP batched threshold encryption
aliases: ["CGPP", "Berkeley24-1"]
eprint: "2024/669"
venue: USENIX Security 2024
year: 2024
status: published
peer_reviewed: true
source_depth: abstract
pq: false
batched: true
epoch_free: false
share_size: 80 bytes per party per batch, independent of batch size
timings: enc under 6 ms; about 2.8 s per committee member for roughly 500 transactions
assumptions_pending: true
techniques: [batched-threshold-encryption, kzg-commitments, witness-encryption]
presented_in: [choudhuri-garg-piet-policharla-2024]
satisfies: [D3, D13]
partially_satisfies: [D15]
fails: [D2, D8, D14]
authors: [arka-rai-choudhuri, sanjam-garg, julien-piet, guru-vamsi-policharla]
---

The paper that introduced batched threshold encryption as a primitive. A committee
decrypts a chosen batch of B ciphertexts out of a larger pool using O(n)
communication instead of the naive O(nB), while ciphertexts outside the batch stay
private.

## Key mechanism

Trapdoors for [[kzg-commitments]] plus [[witness-encryption]] for KZG openings.
The batch is identified by a polynomial commitment; the committee releases material
that opens exactly the committed positions.

## Concrete numbers

Encryption under 6 ms, and 80 bytes per party to decrypt an entire batch regardless
of how many transactions it contains. For Ethereum's roughly 500 transactions per
block, about 2.8 s per committee member single-threaded.

## The epoch cost

The scheme progresses in epochs and needs an expensive interactive setup, in MPC,
for every batch, with only one decryption key per epoch. That is the limitation
[[beat-mev]] removes, and the reason [[D14]] exists as a desideratum rather than
being folded into [[D13]].

## Desiderata

Satisfies [[D3]] and [[D13]] (80 bytes per party is the number the field quotes).
Partially [[D15]]. Fails [[D2]], [[D8]] and [[D14]].

## Assumptions

Recorded as pending: the abstract does not state the underlying pairing assumption
and the KB will not guess it. See `papers/WANTED.md`.

## Relevance to encrypted mempools

The origin of the primitive and still the cleanest statement of why batching is
necessary. Every later scheme in this line responds to its epoch setup.
