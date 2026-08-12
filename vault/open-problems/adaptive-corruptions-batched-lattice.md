---
id: adaptive-corruptions-batched-lattice
type: open-problem
title: Adaptive corruptions for batched lattice threshold schemes
state: open
pq: true
opened_by: [wagner-desiderata]
---

## Statement

Achieve security under adaptive corruptions ([[D6]]) for a *batched* lattice
threshold decryption scheme.

## Where we stand

The two halves exist separately and neither implies the other.

**Adaptive, not batched.** [[sjtu-adaptive-threshold-decryption]] gets adaptive CCA
security at polynomial modulus, using a min-entropy analysis of shares conditioned on
linear matrix hints. [[nguyen-adaptive-hint-mlwe]] appears to attack the same target
from the assumption side. [[devevey-libert-nguyen-peters-yung]] had the standard-model
result at superpolynomial modulus.

**Batched, not adaptive.** [[blt-batch-ibe]] is the post-quantum batched scheme, and
its security is not adaptive.
[[hall-andersen-simkin-wagner-silent]] offers one-shot adaptive corruptions, a model
between static and fully adaptive, but is not batched.

## What needs to be solved

The technical obstacle is that batching and adaptivity pull the same lever in
opposite directions. Adaptive corruption arguments in the lattice setting work by
bounding the residual entropy of the shares given what the adversary already knows.
Batching *deliberately* publishes a single short value that opens many ciphertexts,
which is exactly a large, structured hint about the shared key. Combining them means
either an entropy argument that survives a succinct opener, or a batching mechanism
whose opener leaks less than it appears to.

## How to tell if it is solved

A scheme with `satisfies: [D6, D14]` and `pq: true`. Query it directly:

```
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D6 --satisfies D14
```

Wagner grades [[D6]] as "both seems fine, adaptive preferred", so this is a
strengthening rather than a blocker for deployment.
