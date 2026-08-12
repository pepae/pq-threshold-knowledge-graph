---
id: bbnrs-context-dependent
type: scheme
title: Context-dependent threshold decryption
aliases: ["BBNRS", "context-dependent threshold decryption"]
eprint: "2025/279"
year: 2025
status: preprint
peer_reviewed: false
source_depth: full-text
pq: false
assumptions: [lomdh, rom]
techniques: [hybrid-encryption-associated-data]
satisfies: [D3, D4, D9]
fails: [D8, D14]
authors: [dan-boneh, benedikt-buenz, kartik-nayak, lior-rotem, victor-shoup]
---

Boneh, Bunz, Nayak, Rotem and Shoup introduce the *decryption context*: an extra
argument to decryption that isolates shares produced under different contexts.

## The property, stated precisely

Suppose the threshold is t. Fewer than t shares are generated for ciphertext c
under one context, and fewer than t under a different context. Then the union is
insufficient to decrypt c *even though the total exceeds t*. Shares from different
contexts do not compose.

## Why this is a consensus requirement

Competing forks are different contexts. Without context binding, a committee that
partially participates on two forks can leak a decryption it authorised on neither.
This is the anti-harvesting property, and it is why [[D9]] is on Wagner's list at
all. The paper names the encrypted mempool as its primary motivation.

## Two constructions

One based on ElGamal, and one generic: a transform that adds context to *any*
CCA-secure threshold decryption system without changing the encryption algorithm.
The generic transform is the more useful result for this KB, since it means context
can be retrofitted rather than designed in.

## Desiderata

Satisfies [[D3]], [[D4]] and [[D9]], the last of which it defines. Fails [[D8]] and
[[D14]].

## Assumptions

The ElGamal-based construction is proven in the [[rom]] under a falsifiable
assumption the authors introduce and call the **linear one-more Diffie-Hellman**
([[lomdh]]) assumption, essentially the same one used to analyse high-threshold BLS
signatures. The generic construction is what to reach for if that assumption is
unwelcome, since it adds context to any CCA-secure threshold scheme without
touching encryption.

## Relevance to encrypted mempools

The definitional reference for [[D9]]. [[tacet]] targets the same property in the
lattice setting by a different mechanism, and
[[sjtu-adaptive-threshold-decryption]] gets a version of it as a side effect of
binding its ZeroShare mask to (ciphertext, set).
