---
id: boudgoust-scholl
type: scheme
title: Boudgoust-Scholl threshold FHE at polynomial modulus
aliases: ["Boudgoust-Scholl", "BS23"]
eprint: "2023/016"
venue: ASIACRYPT 2023
year: 2023
status: published
peer_reviewed: true
source_depth: full-text
pq: true
modulus: polynomial
assumptions: [lwe]
techniques: [polynomial-noise-flooding, renyi-divergence-analysis, noise-flooding]
satisfies: [D3, D8]
partially_satisfies: [D5]
fails: [D2, D14]
builds_on: [bendlin-damgard]
authors: [katharina-boudgoust, peter-scholl]
---

The paper that broke the superpolynomial-modulus assumption for lattice threshold
decryption, by changing the measure rather than the construction.

## Key mechanism

Replace statistical distance with [[renyi-divergence-analysis]] when arguing that
a flooded partial decryption hides the key share. Renyi divergence tolerates far
smaller flooding noise, so the modulus can be polynomial. The technical work is in
using a divergence-based argument inside a *decisional* security proof, which is
not where such arguments naturally live.

The result is delivered in two steps: first a threshold scheme with one-way
security, then a transformation to selective indistinguishability-based security.

## What it does not give

Simulation security. A Renyi argument yields probability preservation, which
suffices for search and decision games but not for a simulator that must produce
decryption shares without the key. That gap is exactly what
[[micciancio-suhl]] closes, and it is the reason both papers exist.

## Desiderata

Satisfies [[D3]] and [[D8]], and the polynomial modulus is what makes [[D11]] and
[[D13]] plausibly affordable downstream. Partially [[D5]]: the end result is
selective indistinguishability. Fails [[D2]] and [[D14]].

## Relevance to encrypted mempools

First of the three polynomial-modulus routes catalogued under
[[polynomial-noise-flooding]]. If a mempool scheme only needs game-based
security, this is the cheapest of them.
