---
id: beatmev-pq-implementation
type: implementation
title: PQ BEAT-MEV implementation
repo: https://github.com/pepae/beatmev-pq-implementation
url: https://github.com/pepae/beatmev-pq-implementation
language: [Python]
runnable: true
source_depth: repo
measured: "batch 512, lambda 128: 1250 ms enc/ct, 1.9 MB ct, 50.2 s partial dec/party, 326.5 s combine, 259 MB public key"
implements: [beat-mev]
uses: [kh-pprf, shamir-secret-sharing, noise-flooding]
---

A lattice instantiation of [[beat-mev]] at concrete 128-bit security. The single most
useful artifact in this KB, because it converts "post-quantum batched threshold
encryption is expensive" into numbers.

## What it instantiates

BLMR matrix-product PRF (a GGM tree over binary matrices, with puncturing) for the
[[kh-pprf]], packed Regev encryption for key transport, and threshold decryption via
Shamir shares with Bendlin-Damgard style [[noise-flooding]]. Exact linear algebra
over CRT-decomposed 26-bit primes, SHAKE-256 hash streams, worst-case noise budgets
and core-SVP estimation.

This is the same design [[blt-batch-ibe]]'s Appendix A.4 sketches theoretically, so
the two can be read against each other: the appendix gives the asymptotic shape
(public key O_lambda(1), ciphertext O_lambda(k^3), pre-decryption key O_lambda(k^2)),
this repository gives the constants.

## Measured, batch 512, lambda = 128

| | classical BEAT-MEV | PQ | factor |
|---|---|---|---|
| encryption per ciphertext | 1.58 ms | 1250 ms | ~790x |
| ciphertext size | 722 B | 1.9 MB | ~2700x |
| partial decryption per party | 295 ms | 50.2 s | ~170x |
| combine | 3.8 to 7.7 s | 326.5 s | ~40-90x |
| public key | a few KB | 259 MB | ~10^5x |

## What to conclude

Three to four orders of magnitude across every axis. Note which numbers hurt most for
an encrypted mempool: the 1.9 MB ciphertext is paid on chain by every user
([[D11]]), and the 327 s combine is on the block critical path
([[D15]]), so it is not merely slow, it is slower than a slot. The 259 MB public key
is a [[D10]] failure of a different kind: a one-time cost, but one every encryptor
must fetch.

These numbers are the reason [[sublinear-pq-batch-decryption]] is the KB's most
consequential open problem.
