---
id: gkpw-silent-setup
type: scheme
title: Threshold Encryption with Silent Setup
aliases: ["GKPW", "GKPW24"]
eprint: "2024/263"
venue: CRYPTO 2024
year: 2024
status: published
peer_reviewed: true
source_depth: full-text
pq: false
silent_setup: true
batched: false
timings: enc under 7 ms; partial dec under 1 ms; aggregation for 1024 parties under 200 ms
ciphertext_size: about 8x ElGamal
assumptions: [ggm]
techniques: [silent-setup, witness-encryption]
satisfies: [D2, D3, D11, D13, D15]
partially_satisfies: [D10]
fails: [D1, D8, D14]
authors: [sanjam-garg, dimitris-kolonelos, guru-vamsi-policharla, mingyuan-wang]
---

Garg, Kolonelos, Policharla and Wang: the joint public key of a set of parties is a
deterministic function of their locally computed public keys, so setup is silent.

## Key mechanism

A special-purpose [[witness-encryption]] scheme for the statement "at least t
parties have signed a given message". Encrypting to a committee means encrypting to
that statement; a quorum's signatures are the witness. Because the joint key is a
public function of posted keys, setup is asynchronous, supports multiple committees
over the same key material (multiverse), and supports dynamic thresholds.

## Concrete numbers

Encryption under 7 ms, partial decryption under 1 ms, aggregation for 1024 parties
under 200 ms, ciphertexts about 8x an ElGamal ciphertext. Pairing-based, proven in
the [[ggm]].

## Desiderata

Satisfies [[D2]] (the paper that made silent setup concrete), [[D3]], [[D11]],
[[D13]] and [[D15]]. Partially [[D10]]: individual public keys are linear in the
committee size, the standing cost of its silent setup. Fails [[D1]] (a trusted
setup is still required on top of the silent key aggregation), [[D8]] (pairings),
and [[D14]] (not batched). Wagner's survey notes it is not presented as having a
short decryption key, so do not read [[D12]] into it.

## Relevance to encrypted mempools

The reference classical silent-setup scheme, and the base that [[beast-mev]] makes
additively homomorphic to get batching on top. Its GGM proof and trusted setup are
what a lattice replacement would improve on, which is what the
[[champion-wu-dbe]] line is for.
