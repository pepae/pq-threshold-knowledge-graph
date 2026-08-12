---
id: blt25-implementation
type: implementation
title: BLT25 implementation
repo: https://github.com/pepae/blt25-implementation
url: https://github.com/pepae/blt25-implementation
language: [Python]
runnable: false
source_depth: repo
measured: "provably secure parameters need matrices with about 10^9 columns at lambda 128; runs only at toy parameters with no security"
implements: [blt-batch-ibe]
uses: [gaussian-preimage-sampling, klein-sampler, threshold-ibe]
opens: [sublinear-pq-batch-decryption]
---

A research-prototype implementation of [[blt-batch-ibe]], covering the paper's
constructions: the lattice batch IBE, two-round threshold Gaussian preimage sampling
and threshold batch IBE, threshold GPV signatures, the KP-ABE-based batch IBE with a
BGG+14-style instantiation, and the trilinear-map scheme in a simulated generic
group, plus the supporting explainable-SampleLeft machinery and the shifted
multi-preimage sampler with d-bit labels.

## The finding

The provably secure parameters are computationally impractical: matrices with on the
order of 10^9 columns at lambda = 128. The prototype therefore runs at toy-sized
parameters, and its own documentation is explicit that those provide no cryptographic
security, that the code is not constant-time, and that it does not manage secrets.

## Why this is the important result

BLT's succinctness claim is genuine and strong: at lambda = 128 and batch 4096 the
pre-decryption key is about five orders of magnitude smaller than the batch. This
repository is the check on what that costs. Succinct post-quantum batch decryption
exists asymptotically and cannot currently be run, and the bottleneck is concretely
located in the trapdoor sampler ([[klein-sampler]]).

Read together with [[linear-route-opening-impossibility]], which rules out the cheap
route, this bounds [[sublinear-pq-batch-decryption]] from both sides: the easy
construction is impossible, and the possible construction does not run.
