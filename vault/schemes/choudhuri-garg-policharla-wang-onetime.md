---
id: choudhuri-garg-policharla-wang-onetime
type: scheme
title: One-time setup batched threshold encryption
aliases: ["CGPW", "Berkeley24-2"]
eprint: "2024/1516"
year: 2024
status: preprint
peer_reviewed: false
source_depth: abstract
pq: false
batched: true
epoch_free: false
share_size: 48 bytes per party for batch decryption
timings: enc about 8.5 ms; about 3.2 s per committee member for 500 transactions
assumptions_pending: true
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

Per Wagner's survey: shifted BLS plus witness encryption for polynomial
commitments. Communication is O(1) per epoch once the batch is selected. Wagner
also records that the proof needs a *new interactive assumption*, which is why this
note's assumption edges are pending rather than guessed.

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
