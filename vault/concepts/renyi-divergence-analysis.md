---
id: renyi-divergence-analysis
type: technique
title: Renyi divergence analysis
pq: true
family: proof
---

Measure distribution closeness by Renyi divergence rather than statistical
distance. Introduced to threshold lattice encryption by [[boudgoust-scholl]] to
get a polynomial modulus.

The limitation is structural, not technical: Renyi divergence gives
probability-preservation bounds, which suffice for search and decision games but
not for simulation-based definitions. [[micciancio-suhl]] gets simulation security
by a different route for that reason.
