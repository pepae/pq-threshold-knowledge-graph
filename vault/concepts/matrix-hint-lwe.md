---
id: matrix-hint-lwe
type: assumption
title: Matrix-Hint LWE
aliases: ["Matrix-Hint LWE"]
pq: true
falsifiable: true
family: lattice
reduces_to: [lwe]
source_depth: abstract
---

An LWE variant where the adversary additionally gets linear matrix hints about
the secret. [[sjtu-adaptive-threshold-decryption]] uses a min-entropy analysis of
secret shares *conditioned on* such hints to drive its polynomial noise flooding.

The pattern generalizes: adaptive corruption in a threshold scheme hands the
adversary exactly this kind of partial information about the shared secret, so
hint-style assumptions are the natural formalism for adaptive lattice thresholds.
Compare [[hint-mlwe]].
