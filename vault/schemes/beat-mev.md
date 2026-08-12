---
id: beat-mev
type: scheme
title: BEAT-MEV
eprint: "2024/1533"
venue: USENIX Security 2025
year: 2025
status: published
peer_reviewed: true
source_depth: full-text
pq: false
batched: true
epoch_free: true
silent_setup: false
ciphertext_size: 3 G1 elements plus 1 GT element; 722 B measured at batch 512
share_size: pre-decryption key is a single BLS12-381 G2 element
public_key_size: quadratic in the PRF domain, reducible to linear
timings: enc under 2 ms; under 440 ms to decrypt 512 transactions
assumptions: [ddh, agm]
techniques: [kh-pprf, batched-threshold-encryption, fiat-shamir-nizk]
builds_on: [choudhuri-garg-piet-policharla-2024, cgpp-bte]
superseded_by: [beast-mev]
satisfies: [D3, D7, D11, D13, D14]
partially_satisfies: [D4, D15]
fails: [D2, D8, D10]
attacked_by: [index-collision-censorship]
implemented_by: [beatmev-pq-implementation]
authors: [jan-bormet, sebastian-faust, hussien-othman, ziyan-qu]
---

The first batched threshold encryption scheme without epochs. Bormet, Faust,
Othman and Qu.

## Key mechanism

A [[kh-pprf]], adapted from Dujmovic et al. Each encryptor evaluates the PRF at a
unique index i under an ephemeral key k_i and masks its message:
`gamma_i = m_i + PRF(k_i, i)`. The ciphertext carries three things: the masked
message, an ElGamal encryption of k_i in the exponent, and a punctured key k*_i
punctured at i.

The pre-decryption key for a batch of l indices is computed using ElGamal's
homomorphism and satisfies `PRF(sbk, i) = sum_j PRF(k_j, i)`. Decryption recovers
m_i as

    gamma_i - PRF(sbk, i) + sum_{j != i} PuncturedPRF(k*_j, i)

which works because a punctured key evaluates correctly everywhere except at its
own puncture point. No epoch, and the pre-decryption key is a single BLS12-381 G2
element.

## Costs, precisely

Ciphertext is 3 G1 elements plus 1 GT element. KH-PPRF public keys are quadratic in
the PRF domain, reducible to linear. Decryption needs O(l^2) pairings. Encryption
under 2 ms; under 440 ms to decrypt 512 transactions.

## The index coordination problem

Decryption only succeeds if the PRF keys are punctured at *distinct* indices, and
encryptors do not coordinate. The paper's answer is to split a batch into
sub-batches of distinct indices and publish a pre-decryption key per sub-batch,
which also cuts the O(l^2) pairing cost, at the price of larger keys and
ciphertexts. This is where [[index-collision-censorship]] comes from, and it is
inherited by every index-dependent scheme built on BEAT-MEV.

## Desiderata

Satisfies [[D3]], [[D14]] (the point of the paper), [[D7]] (it requires
straight-line simulation-extractable NIZKs, efficient in the [[agm]], precisely for
rogue ciphertexts), [[D11]] and [[D13]]. Partially [[D4]] and [[D15]]. Fails
[[D2]], [[D8]] and [[D10]]: Wagner's survey records very large keys, and the
measured post-quantum instantiation has a 259 MB public key.

## Relevance to encrypted mempools

The scheme that made epoch-free batching real, and the baseline every later batched
scheme is measured against. [[beast-mev]] adds silent setup, [[weighted-bte]] makes
it quasilinear and weighted, and [[beatmev-pq-implementation]] measures what it
costs post-quantum.
