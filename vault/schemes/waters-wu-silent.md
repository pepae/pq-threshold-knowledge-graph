---
id: waters-wu-silent
type: scheme
title: Silent threshold cryptography from pairings
aliases: ["Waters-Wu"]
eprint: "2025/1547"
year: 2025
status: preprint
peer_reviewed: false
source_depth: abstract
pq: false
silent_setup: true
ciphertext_size: 4 group elements plus a short tag
assumptions: [q-type-pairing]
techniques: [monotone-policy-encryption, silent-setup]
satisfies: [D2, D3, D11]
partially_satisfies: [D4]
fails: [D1, D8, D10, D14]
authors: [brent-waters, david-wu]
---

Waters and Wu get silent setup with *expressive* policies, monotone Boolean formulas
rather than just thresholds, in the standard model from a [[q-type-pairing]]
assumption. Ciphertexts are 4 group elements plus a short tag; threshold signatures
are 3 group elements.

## Why it is here

It is the classical upper bound the lattice line is chasing: standard model, no
idealisation, tiny ciphertexts, expressive policies, and it avoids heavy machinery
such as indistinguishability obfuscation. Any post-quantum construction should be
compared against these numbers rather than against the folklore baseline.

## The costs

Per Wagner's survey: a trusted setup in the form of augmented powers of tau with a
hole, large keys and CRS, and tag-based CCA2 security under static corruptions with
semi-honest key generation assumed for corrupted users. That last condition is a
real weakening worth noting.

## Desiderata

Satisfies [[D2]], [[D3]] and [[D11]]. Partially [[D4]] (tag-based CCA2, with the
semi-honest keygen caveat). Fails [[D1]], [[D8]], [[D10]] and [[D14]].
