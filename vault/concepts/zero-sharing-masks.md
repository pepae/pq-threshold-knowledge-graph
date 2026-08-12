---
id: zero-sharing-masks
type: technique
title: Pseudorandom zero-sharing masks
aliases: ["ZeroShare", "zero-mask"]
pq: true
family: threshold
---

Each party adds a pseudorandom mask to its partial decryption, chosen so that
the masks cancel exactly when a quorum combines under the recovery coefficients,
and do not cancel otherwise.

Keying the mask on a context (a block anchor, say) is what buys
[[D9]]: shares from two different contexts leave an uncancelled pseudorandom
residue, so cross-context combination reduces to PRF pseudorandomness rather than
being prevented by a checkable tag. [[tacet]] uses this, and its audit records why
a naive alternative fails: a plain mask F_k(ctx) added to each share neither
cancels nor is removable, because k is secret, so decryption simply does not
succeed. The masks must sum to zero under the recovery coefficients by
construction.
