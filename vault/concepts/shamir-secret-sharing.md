---
id: shamir-secret-sharing
type: technique
title: Shamir secret sharing
aliases: ["Shamir"]
family: sharing
---

Threshold sharing by polynomial interpolation. Compact (one field element per
party) and the default choice, but its recovery coefficients are not small, which
is the problem in the lattice setting: reconstruction multiplies share noise by
those coefficients and the noise budget has to absorb it.

That tension is why lattice thresholds reach for [[low-norm-secret-sharing]] or
[[replicated-secret-sharing]] instead, and why [[sjtu-adaptive-threshold-decryption]]
supporting Shamir at polynomial modulus (its TD2) matters for large committees.
[[pilvi]] keeps Shamir but chooses the evaluation points carefully; see
[[threshold-lwe]].
