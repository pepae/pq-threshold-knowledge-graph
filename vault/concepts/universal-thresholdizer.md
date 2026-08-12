---
id: universal-thresholdizer
type: technique
title: Universal thresholdizer
aliases: ["universal thresholdizer"]
pq: true
family: primitive
---

A compiler that adds threshold functionality to a wide class of schemes, built
from threshold fully homomorphic encryption
([[bgg-universal-thresholdizer]]). It is the reason "post-quantum threshold
decryption" has been possible for years, and also the reason it is not deployed:
it needs a setup, and it inherits the cost of threshold FHE plus
[[noise-flooding]] at superpolynomial modulus.
