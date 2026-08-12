---
id: harvesting-attack
type: attack
title: Cross-context share harvesting
aliases: ["harvesting", "cross-fork share combining"]
status: published
unverified: true
source_depth: mixed
attacks: [tacet]
builds_on: [bbnrs-context-dependent]
---

> This node is a synthesis, not a single citation: the property is defined by
> [[bbnrs-context-dependent]] and a concrete instance is recorded in
> [[tacet]]'s audit log. `unverified: true` marks that there is no one paper to
> cite for "the harvesting attack" as such.

The attack that motivates [[D9]]. Sub-threshold sets of decryption shares gathered
under two different contexts are combined to reach the threshold, decrypting
something no quorum ever authorised under either context.

## Why forks make this concrete

In a consensus setting the natural context is the block or batch anchor, and
competing forks are different contexts. A committee that partially participates on
two forks (which is normal behaviour, not misbehaviour) can leak a decryption if
shares compose across contexts. Fewer than t shares on fork A plus fewer than t on
fork B can exceed t in total.

## Defences

[[bbnrs-context-dependent]] defines the property that rules this out and gives a
generic transform adding context to any CCA-secure threshold decryption scheme.
[[sjtu-adaptive-threshold-decryption]] gets a version of it by binding its ZeroShare
mask to (ciphertext, decryptor set).

## As a real finding

[[tacet]]'s audit records an explicit harvesting attack against its own earlier
draft: without genuine context binding, threshold-Regev shares were cross-context
combinable, breaking the intended context-isolation property. The fix was to make
the mask a [[zero-sharing-masks]] construction whose residue on any cross-context
combination is unremovable, so isolation reduces to PRF pseudorandomness rather than
to a checkable tag. That progression is the useful part: a tag you can check is not
the same as an algebraic obstruction.
