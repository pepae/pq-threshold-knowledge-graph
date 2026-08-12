---
id: sublinear-pq-batch-decryption
type: open-problem
title: Sublinear post-quantum batch decryption
state: partially-resolved
pq: true
opened_by: [wagner-desiderata]
---

## Statement

Post-quantum batch decryption where the communication needed to open a batch of B
ciphertexts is sublinear in B, at parameters that actually run.

## Where we stand

**Classically this is solved and cheap.** 80 bytes per party for a whole batch in
[[cgpp-bte]], 48 in [[choudhuri-garg-policharla-wang-onetime]], a single group
element in [[beat-mev]]. All independent of B.

**The obvious lattice analogue is impossible.** On the linear lattice route a
constant-size opening cannot exist, because the opener would have to encode |B|
independent values in one ring element: see
[[linear-route-opening-impossibility]]. So opening is O(|B|) on that route.

**A different route does achieve succinctness, on paper.**
[[blt-batch-ibe]] gets a pre-decryption key polylog in batch length, via lattice IBE
composed with a shifted multi-preimage trapdoor sampler. At lambda = 128 and batch
4096 the key is about five orders of magnitude smaller than the batch.

**But those parameters do not run.** [[blt25-implementation]] reports that provably
secure parameters need matrices with on the order of 10^9 columns at lambda = 128, so
the reference implementation runs at toy parameters with no security. Meanwhile the
one measured post-quantum batched scheme,
[[beatmev-pq-implementation]], is linear in the batch and pays 1.9 MB ciphertexts,
50 s partial decryption and 327 s to combine at batch 512.

## What needs to be solved

The gap is entirely concrete. Either:

1. Bring the trapdoor-sampler route's parameters down by orders of magnitude, which
   probably means a fundamentally cheaper sampler than [[klein-sampler]]; or
2. Find a succinct opener outside both the linear route and the trapdoor route.

## Why "partially resolved"

Asymptotic succinctness exists. Nobody has run it. Since the whole point of batching
is a concrete communication saving, an asymptotic result at unrunnable parameters
does not settle the problem.
