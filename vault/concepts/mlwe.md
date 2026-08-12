---
id: mlwe
type: assumption
title: Module-LWE
aliases: ["MLWE", "Module Learning With Errors"]
pq: true
falsifiable: true
family: lattice
reduces_to: [lwe]
---

The module variant of [[lwe]], over a polynomial ring. Better concrete
efficiency than plain LWE at comparable security, which is why deployed lattice
KEMs use it.

The ring structure is not free in the threshold setting: [[tacet]]'s audit found
that a Renyi divergence multiplies over the N ciphertext coordinates in the ring
case, so a flooding bound derived for plain LWE is short by a factor of sqrt(N).
See [[flooding-underestimate-ring-setting]].
