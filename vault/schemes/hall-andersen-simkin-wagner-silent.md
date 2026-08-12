---
id: hall-andersen-simkin-wagner-silent
type: scheme
title: Silent threshold encryption with one-shot adaptive security
aliases: ["HSW25", "one-shot adaptive"]
eprint: "2025/1384"
year: 2025
status: preprint
peer_reviewed: false
source_depth: mixed
pq: true
silent_setup: true
batched: false
ciphertext_size: 1 MB message gives 1.072 MB ciphertext, or 1.431 MB post-quantum, at t < n/3
assumptions: [rom]
techniques: [silent-setup, naive-threshold-baseline, key-anonymous-pke]
satisfies: [D2, D3, D10, D11]
partially_satisfies: [D6, D8]
fails: [D14]
authors: [mathias-hall-andersen, mark-simkin, benedikt-wagner]
---

Hall-Andersen (ZKSecurity), Simkin (Flashbots, Aarhus) and Wagner (Ethereum
Foundation). Ciphertext and public key sizes independent of n, generically from any
key-anonymous PKE.

## Not the naive baseline

This scheme is frequently misattributed as the folklore construction it improves
on. It is not; see [[naive-threshold-baseline]] for the actual baseline. Wagner's
own survey labels this one "HSW25 One-Shot Adaptive".

## Two ideas

**Soft thresholds.** Parameters c and epsilon, where any (c - epsilon)n parties
cannot decrypt and any (c + epsilon)n parties can. Relaxing the exact threshold to a
band is what buys sizes independent of n, and for a large committee a band is
usually operationally acceptable.

**One-shot adaptive corruptions.** A corruption model strictly between static and
fully adaptive. A genuine advance on [[D6]] without claiming full adaptivity, which
is the honest framing.

## Assumptions

Generic: it needs no new hardness assumption of its own, only a
[[key-anonymous-pke]], and it uses the [[rom]]. That genericity is the reason it is
plausibly post-quantum, since a post-quantum PKE plugs straight in, and the reason
it avoids strong tools such as indistinguishability obfuscation.

The paper is candid about the trade against the pairing-based alternatives: the
Waters-Wu line ([[waters-wu-silent]]) gets smaller ciphertexts and avoids random
oracles, at the cost of a trusted setup, large individual keys and a large CRS. It
also notes that the subsequent lattice constructions
([[champion-wu-monotone-dnf]], [[rishab-dme]]) are plausibly post-quantum from
[[decomposed-lwe]] with compact keys and a transparent setup, but in the [[rom]].

## Concrete numbers

At t < n/3, encrypting 1 MB gives a 1.072 MB ciphertext, or 1.431 MB for the
post-quantum instantiation. The overhead is a small multiplicative factor on the
payload rather than a fixed large ciphertext, a different cost shape from the
lattice batched schemes.

## Desiderata

Satisfies [[D2]], [[D3]], [[D10]] and [[D11]] (both independent of n). Partially
[[D6]] (one-shot adaptive) and [[D8]] (plausibly post-quantum, and it avoids strong
assumptions such as indistinguishability obfuscation). Fails [[D14]]: not batched.

## Relevance to encrypted mempools

The most promising *non-batched* route to a large rotating committee, and the scheme
to reach for if the deployment tolerates a soft threshold. It does not address
batching, so it does not solve the block-opening problem on its own.
