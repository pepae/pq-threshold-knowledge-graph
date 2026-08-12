---
id: devevey-adaptive-poly-modulus
type: open-problem
title: Adaptive security from LWE with polynomial approximation factor
state: resolved
pq: true
---

## Statement

Stated by [[devevey-libert-nguyen-peters-yung]] (PKC 2021), verbatim:

> It remains an open problem to prove adaptive security under a more common LWE
> assumption with polynomial approximation factor.

Their non-interactive, adaptively secure, CCA2 threshold cryptosystem in the standard
model needed a superpolynomial approximation factor for its LWE instantiation. The
source paper of the resolution also records that this was identified elsewhere as a
particularly challenging task.

## Resolution

Resolved by [[sjtu-adaptive-threshold-decryption]], which gives three adaptively
secure (t, N) threshold decryption schemes from LWE with polynomial modulus: TD0
(adaptive CPA, asynchronous, standard model, polynomial modulus for a small number of
users), TD1 (adaptive CCA, polynomial modulus), and TD2 (adaptive CCA for
polynomially many users via Shamir secret sharing).

The mechanism is a refined polynomial noise flooding lemma based on a min-entropy
analysis of secret shares conditioned on linear matrix hints, plus ZeroShare masking.
See [[polynomial-noise-flooding]] and [[zero-sharing-masks]].

## What the resolution does not cover

Two caveats worth carrying forward. TD2's CCA security relies on the [[rom]], because
its mask is derived from a random oracle, so this is not a standard-model result
throughout, and the original open problem was posed in the standard model. And
robustness for TD2 is left as involved: proving well-formedness of a masked share in
zero knowledge is hard. Neither caveat is batching, so
[[adaptive-corruptions-batched-lattice]] remains open.
