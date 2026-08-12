---
id: replicated-secret-sharing
type: technique
title: Replicated secret sharing
aliases: ["RSS"]
family: sharing
uses: [low-norm-secret-sharing]
---

Give each authorized set its own additive share. Recovery coefficients are 0/1,
which is ideal for a lattice noise budget, but each party holds C(n-1, t-1)
values, so it only works for small committees.
