---
id: monotone-policy-encryption
type: technique
title: Distributed monotone-policy encryption
aliases: ["DME"]
family: primitive
uses: [distributed-broadcast-encryption]
---

Encrypt to a set of independently generated public keys together with an access
policy; any satisfying set decrypts. Succinctness, meaning ciphertext sublinear in
the policy description, is the whole difficulty.

It strictly generalizes both threshold encryption with silent setup (threshold
policy) and [[distributed-broadcast-encryption]] (set-membership policy), which is
why the lattice results here are the ones to watch for post-quantum [[D2]].
