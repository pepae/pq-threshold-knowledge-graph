---
id: micciancio-suhl
type: scheme
title: Micciancio-Suhl simulation-secure threshold PKE
aliases: ["Micciancio-Suhl", "MS24"]
eprint: "2023/1728"
venue: IACR Communications in Cryptology 1(4)
year: 2025
doi: 10.62056/a0zogy4e-
status: published
peer_reviewed: true
source_depth: full-text
pq: true
modulus: polynomial
assumptions: [lwe]
techniques: [polynomial-noise-flooding, noise-flooding]
satisfies: [D3, D8]
fails: [D2, D14]
builds_on: [boudgoust-scholl, bendlin-damgard]
authors: [daniele-micciancio, adam-suhl]
---

The first lattice threshold PKE that is simulation-secure *and* has a polynomially
bounded modulus. Before it, you could have one or the other.

## Key mechanism

The construction is deliberately standard; the contribution is the analysis. When
both the ciphertext noise and the flooding noise are Gaussian, simulation goes
through even with very small flooding noise. That removes the superpolynomial
flooding that simulation security had appeared to require, without falling back on
a [[renyi-divergence-analysis]] that cannot support simulation.

As part of the proof they show [[lwe]] remains hard in the presence of certain
kinds of leakage, a result the authors flag as reusable anywhere noise flooding
appears.

## Concrete parameters

The paper states its modulus is small not only asymptotically but concretely,
giving parameters roughly comparable to highly optimized non-threshold schemes
such as FrodoKEM. That claim is the single most useful number in the
polynomial-modulus literature, because FrodoKEM is a known quantity: it puts
lattice threshold decryption in the same ballpark as a conservative non-threshold
KEM rather than orders of magnitude away.

## Desiderata

Satisfies [[D3]] and [[D8]]. Simulation security is what makes it composable, so
this is the natural building block when a larger protocol needs to simulate
decryption shares. Fails [[D2]] and [[D14]].

## Relevance to encrypted mempools

The strongest general-purpose lattice threshold PKE for the non-batched setting,
and the right starting point if you need a scheme whose shares can be simulated
inside a bigger proof. It does not address batching, which is where the encrypted
mempool cost actually sits.
