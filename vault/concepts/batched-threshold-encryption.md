---
id: batched-threshold-encryption
type: technique
title: Batched threshold encryption
aliases: ["BTE"]
family: primitive
---

The primitive introduced by [[cgpp-bte]]: a committee decrypts a chosen batch of
B ciphertexts out of a larger pool, with communication independent of or sublinear
in B, while ciphertexts outside the batch stay private.

The naive alternative costs O(nB) communication for n parties, which is what makes
this a primitive rather than an optimization. The properties it must then acquire
to be deployable are [[D14]] (epoch-free) and [[D7]] (rogue ciphertexts).
