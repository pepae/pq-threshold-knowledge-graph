---
id: low-norm-secret-sharing
type: technique
title: Low-norm secret sharing
aliases: ["small-norm sharing"]
pq: true
family: sharing
---

Secret sharing whose reconstruction coefficients have small norm, so combining
shares does not blow up a lattice noise budget.

The cost is share material. The replicated construction gives recovery norm
about sqrt(t) but hands each party C(n-1, t-1) values, which is exponential in the
committee size. That is a hard ceiling on committee size, and it is a property of
the *sharing*, so it applies to a DKG-based scheme and a silent one alike. See
[[low-norm-small-share-large-t]], and [[tacet]] for what it does to a concrete
deployment.
