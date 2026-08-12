---
id: noise-flooding
type: technique
title: Noise flooding
aliases: ["smudging", "noise smudging"]
pq: true
family: lattice
---

Add noise large enough to statistically drown the secret-dependent part of a
partial decryption, so a share can be simulated without the key.

The classical cost is a superpolynomial modulus, because statistical distance
needs the flooding noise superpolynomially larger than the decryption noise. That
cost is what makes naive post-quantum thresholds impractical, and removing it is
the point of [[polynomial-noise-flooding]].

The technique dates to [[bendlin-damgard]] and is the mechanism behind
[[bgg-universal-thresholdizer]].
