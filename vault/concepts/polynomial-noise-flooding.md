---
id: polynomial-noise-flooding
type: technique
title: Polynomial noise flooding
aliases: ["polynomial modulus flooding"]
pq: true
family: lattice
uses: [noise-flooding]
---

[[noise-flooding]] with flooding noise only polynomially larger than the
decryption noise, so the modulus stays polynomial. Three distinct routes:

* **Renyi divergence** instead of statistical distance ([[boudgoust-scholl]]).
  Cheaper, but Renyi arguments support game-based, not simulation-based, security.
* **Gaussian-vs-Gaussian analysis** ([[micciancio-suhl]]): when both the
  ciphertext noise and the flooding noise are Gaussian, simulation goes through
  even with very small flooding noise. This recovers simulation security at
  polynomial modulus.
* **Min-entropy conditioned on hints** ([[sjtu-adaptive-threshold-decryption]]):
  bound the residual entropy of the shares given the adversary's linear matrix
  hints, which is what makes the argument survive *adaptive* corruption.

Two cautions from practice. Renyi divergence in the flooding hop is a
multiplicative constant of about e^(1/2), not 1+o(1). And in the ring setting the
divergence multiplies over all N ciphertext coordinates, so a bound derived for
plain LWE understates the required flooding noise by sqrt(N); see
[[flooding-underestimate-ring-setting]].
