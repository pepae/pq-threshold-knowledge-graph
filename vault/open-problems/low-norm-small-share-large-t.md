---
id: low-norm-small-share-large-t
type: open-problem
title: Low-norm secret sharing with small shares at large t
state: open
pq: true
opened_by: [wagner-desiderata]
---

## Statement

A secret sharing scheme that is simultaneously low-norm (small reconstruction
coefficients, so a lattice noise budget survives combination) and small-share (per
party material polynomial in the committee size), at large thresholds.

## Where we stand

The two known points on the curve are both bad at scale.

**[[replicated-secret-sharing]]**: recovery coefficients are 0/1, ideal for the
noise budget, but each party holds C(n-1, t-1) values. Exponential in committee size.

**[[shamir-secret-sharing]]**: one element per party, but the recovery coefficients
are large, and reconstruction multiplies share noise by them.

[[pilvi]] gets a genuine improvement by keeping Shamir and choosing the evaluation
points carefully, reaching shares of t log K poly(lambda), abstracted as the
[[threshold-lwe]] assumption.
[[sjtu-adaptive-threshold-decryption]]'s TD2 supports polynomially many users with
Shamir at polynomial modulus. So the frontier has moved, but neither gives low-norm
recovery *and* small shares at large t together.

## Why it is the binding constraint in practice

This is the one open problem in the KB with a measured deployment consequence.
[[tacet]] reports that its noise budget needs low-norm sharing with recovery norm
about sqrt(t), whose C(n-1, t-1) per-party material caps committee size, and that
this cap applies to its DKG core and its silent variant *equally*, because it comes
from the sharing rather than the setup. A reader who concludes "use silent setup to
scale the committee" would be wrong for that reason.

## What needs to be solved

Either a sharing scheme with both properties, or a threshold construction whose
noise budget does not depend on the recovery coefficient norm at all. The second
framing may be the more productive one: the constraint is an artifact of combining
shares linearly over a noisy encryption, not a fact about secret sharing.
