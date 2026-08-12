---
id: bgg-universal-thresholdizer
type: scheme
title: Universal thresholdizer from threshold FHE
aliases: ["BGG+18", "universal thresholdizer scheme"]
eprint: "2017/956"
venue: CRYPTO 2018
year: 2018
status: published
peer_reviewed: true
source_depth: abstract
pq: true
assumptions: [lwe]
techniques: [universal-thresholdizer, noise-flooding]
satisfies: [D3, D8]
partially_satisfies: [D4]
fails: [D1, D2, D14, D15]
authors: [dan-boneh, rosario-gennaro, steven-goldfeder, aayush-jain, sam-kim, peter-rasmussen, amit-sahai]
---

Boneh, Gennaro, Goldfeder, Jain, Kim, Rasmussen and Sahai construct threshold
fully homomorphic encryption from [[lwe]], then abstract it into a *universal
thresholdizer*: a compiler that adds threshold functionality to a large class of
schemes, including CCA-secure PKE, signatures and PRFs.

## Why it is in this KB

It is the reason "post-quantum threshold decryption is possible" has been true
since 2018, and the reason it is nonetheless not deployed. The construction needs
a setup, and it inherits threshold FHE's cost plus [[noise-flooding]] at a large
modulus. It is the generic answer that every concrete scheme in this KB exists to
beat.

## Desiderata

Satisfies [[D3]] and [[D8]]. Partially [[D4]]: it can thresholdize a CCA-secure
PKE, so CCA2 is reachable, but through a generic and expensive route. Fails
[[D1]] (needs a setup), [[D2]], [[D14]] and [[D15]] on cost grounds.

## Relevance to encrypted mempools

Use it as the reference point for what "PQ threshold with setup" costs. Any
concrete scheme that does not clearly beat it on [[D11]], [[D13]] and [[D15]] is
not worth the added complexity.
