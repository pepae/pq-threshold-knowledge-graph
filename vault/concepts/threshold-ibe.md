---
id: threshold-ibe
type: technique
title: Threshold batch IBE
aliases: ["thrIBE", "batched threshold IBE"]
family: primitive
---

Identity-based encryption with a secret-shared master key, where a short
pre-decryption key opens every ciphertext under any identity in a chosen set.

Wagner's note calls threshold IBE ideal for the short-decryption-key setting
([[D12]]), and the reason is direct: a pre-decryption key for the set of
identities in a block *is* a short batch opener, with no epoch and no slot number.
That is the route [[blt-batch-ibe]] and [[aptos-batched-ibe]] take.
