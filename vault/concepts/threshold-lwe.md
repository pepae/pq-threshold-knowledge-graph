---
id: threshold-lwe
type: assumption
title: Threshold-LWE
aliases: ["threshold-LWE"]
pq: true
falsifiable: true
family: lattice
reduces_to: [lwe]
source_depth: abstract
---

Introduced by [[pilvi]] as a general-purpose tool, and proven to follow from
plain [[lwe]]. It captures the recurring core step in security proofs of schemes
that Shamir-share an LWE secret at carefully chosen evaluation points; the
algebraic structure of those points is what makes Pilvi's shares small.

Because it reduces to LWE, it costs nothing in assumption strength. Its value is
proof modularity.
