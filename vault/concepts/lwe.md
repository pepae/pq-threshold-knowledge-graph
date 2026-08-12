---
id: lwe
type: assumption
title: Learning With Errors
aliases: ["LWE"]
pq: true
falsifiable: true
family: lattice
---

The workhorse post-quantum assumption. Distinguishing (A, As+e) from uniform for
short e.

For threshold decryption the parameter that matters is the modulus. A
superpolynomial modulus is the classical price of noise flooding, and it is
expensive concretely. Getting simulation security at *polynomial* modulus is the
thread running through [[boudgoust-scholl]], [[micciancio-suhl]], [[pilvi]] and
[[sjtu-adaptive-threshold-decryption]].
