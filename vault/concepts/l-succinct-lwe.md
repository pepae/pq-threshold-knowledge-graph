---
id: l-succinct-lwe
type: assumption
title: l-succinct LWE
aliases: ["ell-succinct LWE"]
pq: true
falsifiable: true
family: lattice
source_depth: abstract
---

Introduced by Wee (CRYPTO 2024). A falsifiable lattice assumption strong enough
to give succinct commitments to matrices, and the basis of the first lattice
distributed broadcast encryption, [[champion-wu-dbe]].

It is falsifiable, which is the point: the prior route to these primitives went
through plain witness encryption, which is not.
