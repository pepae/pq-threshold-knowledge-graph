---
id: choudhuri-garg-policharla-wang-onetime
type: scheme
title: One-time setup batched threshold encryption
aliases: ["CGPW", "Berkeley24-2"]
eprint: "2024/1516"
year: 2024
status: preprint
peer_reviewed: false
source_depth: mixed
pq: false
batched: true
epoch_free: false
share_size: 48 bytes per party for batch decryption
timings: enc about 8.5 ms; about 3.2 s per committee member for 500 transactions
assumptions: [shifted-bls-assumption, agm, rom]
techniques: [batched-threshold-encryption]
builds_on: [cgpp-bte]
satisfies: [D3, D13]
partially_satisfies: [D15]
fails: [D2, D8, D14]
authors: [arka-rai-choudhuri, sanjam-garg, guru-vamsi-policharla, mingyuan-wang]
---

Choudhuri, Garg, Policharla and Wang remove the per-epoch setup from
[[cgpp-bte]], keeping a single one-time DKG for the n decryption servers.

## Key mechanism

*Shifted BLS*: the committee signs not the commitment `com` but `com` shifted by a
public random group element, which is what removes the per-epoch setup. Combined
with witness encryption for polynomial commitments. Communication is O(1) per epoch
once the batch is selected.

The proof rests on a new assumption ([[shifted-bls-assumption]], Definition 1 in
the paper) which the authors reduce to more standard assumptions in the [[agm]],
plus the [[rom]]. This is what Wagner's survey means by "needs new interactive
assumption for security proof".

## Concrete numbers

Encryption about 8.5 ms, 48 bytes per party for batch decryption, about 3.2 s per
committee member for 500 transactions, under 2x overhead against prior work in the
worst case.

## What it does not fix

Still epoch-based: one decryption key per epoch, so users must encrypt with respect
to an epoch. It is the step between [[cgpp-bte]] and the epoch-free [[beat-mev]],
and worth keeping distinct from both, because "no epoch setup" and "no epochs" are
different claims that get conflated.

## Desiderata

Satisfies [[D3]] and [[D13]] (48 bytes per party, the smallest in the KB).
Partially [[D15]]. Fails [[D2]], [[D8]], and [[D14]]: removing the per-batch setup
is not the same as being epoch-free.
