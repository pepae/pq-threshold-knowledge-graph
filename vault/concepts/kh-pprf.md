---
id: kh-pprf
type: technique
title: Key-homomorphic puncturable PRF
aliases: ["KH-PPRF", "key-homomorphic PPRF"]
pq: true
family: prf
---

A puncturable PRF that is also key-homomorphic, so parties holding shares of the
PRF key can each evaluate locally and have the contributions combine.

This is the engine of [[beat-mev]]: puncturing at the batch's indices is what lets
one short opening decrypt exactly the included ciphertexts and nothing else, with
no epoch setup. The cost in BEAT-MEV is very large keys, and quadratic work in the
batch size. [[weighted-bte]] replaces it with an FFT-friendly alternative to get
quasilinear work.

Lattice-based key-homomorphic PRFs exist (the BLMR matrix-product PRF), which is
how [[beatmev-pq-implementation]] instantiates the scheme post-quantum, at three
to four orders of magnitude overhead.
