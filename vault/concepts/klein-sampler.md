---
id: klein-sampler
type: technique
title: Klein/GPV sampler
aliases: ["Klein sampler", "GPV sampler"]
pq: true
family: lattice
uses: [gaussian-preimage-sampling]
---

The standard trapdoor Gaussian sampler. Its concrete cost is the reason
provably secure parameters for lattice batch IBE are not runnable:
[[blt25-implementation]] reports matrices on the order of 10^9 columns at
lambda = 128, so the reference implementation runs at toy parameters that carry no
security.
