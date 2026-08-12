---
id: blt-batch-ibe
type: scheme
title: BLT threshold batch IBE without epochs
aliases: ["BLT", "BLT25", "Boneh-Laufer-Tas"]
eprint: "2025/1254"
year: 2025
status: preprint
peer_reviewed: false
source_depth: full-text
pq: true
batched: true
epoch_free: true
silent_setup: false
share_size: pre-decryption key polylog in batch length; about 5 orders of magnitude smaller than the batch at lambda=128, batch 4096
assumptions: [lwe, rom, l-succinct-lwe]
techniques: [threshold-ibe, gaussian-preimage-sampling, klein-sampler, batched-threshold-encryption]
satisfies: [D8, D12, D13, D14]
partially_satisfies: [D3]
fails: [D2]
opens: [sublinear-pq-batch-decryption]
implemented_by: [blt25-implementation]
authors: [dan-boneh, evan-laufer, ertem-nusret-tas]
---

Boneh, Laufer and Tas: epochless batch IBE with a succinct public key, ciphertext
and pre-decryption key, plus the threshold version. The most important post-quantum
entry in the batched line.

## The primitive

Alice holds an IBE master secret key. For a set of identities she publishes one
short pre-decryption key that opens ciphertexts under any identity in the set and
nothing else. Secret-share the master key and it becomes threshold batch IBE.
Applied to an encrypted mempool the identities are the transactions in a block, so
the pre-decryption key *is* the block opener. This is the route Wagner's note calls
ideal for [[D12]].

## Three constructions

* **Lattice, from [[lwe]] in the [[rom]]** (the main one): a composition of a
  lattice IBE with a shifted multi-preimage trapdoor sampler, extended to d-bit
  labels. Plausibly post-quantum.
* **Generically from KP-ABE**, which needs the ABE key for the set function to be
  short; several existing ABE schemes qualify. The paper notes it is unclear how to
  thresholdize the KP-ABE-based constructions.
* **From a trilinear map**, for completeness, building on aggregate IBE.

There is also a plain-model lattice batch IBE from [[l-succinct-lwe]].

## Thresholdizing is the hard part

It requires thresholdizing a lattice trapdoor and a *two-round* decryption protocol
for secret-shared [[gaussian-preimage-sampling]]. That second round is why [[D3]]
is only partially satisfied: decryption is no longer one message per party.

## The attack it contributes

The paper identifies [[index-collision-censorship]], a censorship vector against
index-dependent batch encryption schemes including [[beat-mev]] and those built on
it, and separately an identity-tag replication issue against tag-based schemes.
This is the finding Wagner's survey records as a "succinctness vulnerability"; the
paper frames it as censorship arising from the succinctness trade-off, not as a
break of confidentiality.

## The PQ BEAT-MEV appendix

Appendix A.4 estimates a lattice BEAT-MEV built on the BLMR key-homomorphic
puncturable PRF, with Regev encryption for the PRF keys (chosen to preserve their
structure), thresholdized via threshold Regev citing [[bendlin-damgard]]. The
estimates:

* public key `O_lambda(1)`, since the PRF matrices come from a seed and Regev
  public keys are constant-size in lambda
* ciphertext `k*m*log(p') = O(k^3 * n * log n * (log k + log n)) = O_lambda(k^3)`
* pre-decryption key `m*log q = O(k^2 * n * log^2 n) = O_lambda(k^2)`

This is an independent theoretical cross-check on
[[beatmev-pq-implementation]], which instantiates the same BLMR-plus-Regev design
and measures it. The appendix predicts the shape; the implementation supplies the
constants.

## Desiderata

Satisfies [[D8]], [[D12]], [[D13]] (a pre-decryption key polylog in batch length is
the strongest succinctness claim in the KB) and [[D14]]. Partially [[D3]] (two
rounds). Fails [[D2]].

## Relevance to encrypted mempools

The best answer to "can post-quantum batch decryption be succinct". The catch is
concrete: see [[blt25-implementation]] for why the provably secure parameters do
not run.
