---
id: gaussian-preimage-sampling
type: technique
title: Gaussian preimage sampling
aliases: ["preimage sampling", "SamplePre"]
pq: true
family: lattice
---

Sampling a short preimage under a lattice trapdoor. The core operation of GPV
signatures and of lattice IBE key extraction.

Thresholdizing it is hard: the trapdoor must be secret-shared and the sample must
still be correctly distributed. [[blt-batch-ibe]] needs a two-round protocol for
this, which is why it does not satisfy [[D3]] cleanly. Concretely it is also where
the parameters explode; see [[klein-sampler]] and
[[blt25-implementation]].
