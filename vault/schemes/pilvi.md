---
id: pilvi
type: scheme
title: Pilvi
eprint: "2025/1691"
venue: ASIACRYPT 2025
year: 2025
doi: 10.1007/978-981-95-5119-4_17
status: published
peer_reviewed: true
source_depth: full-text
pq: true
modulus: polynomial
ciphertext_size: 14 to 58 KB
share_size: 1 to 4 KB
assumptions: [lwe, threshold-lwe]
techniques: [shamir-secret-sharing, polynomial-noise-flooding, low-norm-secret-sharing]
satisfies: [D3, D8]
partially_satisfies: [D5, D13]
fails: [D2, D14]
builds_on: [micciancio-suhl, boudgoust-scholl]
authors: [valerio-cini, russell-lai, ivy-woo]
---

A thresholdized variant of Regev encryption that gets small decryption shares and
strong simulation-based security together, under [[lwe]].

## Key mechanism

Shamir-share the LWE secret at *carefully chosen evaluation points*, so the
algebraic structure of those points keeps the recovery coefficients manageable.
The reusable abstraction is the [[threshold-lwe]] assumption, which the authors
prove follows from plain LWE and which captures this recurring proof step. As a
second application they build distributed PRFs from it.

## Concrete numbers

Decryption shares are t log K poly(lambda). At 128-bit security the paper reports
ciphertexts of 14 to 58 KB and decryption shares of 1 to 4 KB, with a polynomial
modulus under a bounded number of queries.

Read those against the alternatives: the prior lattice art had share sizes
polynomial in K and in some cases exponential in t, so this is the paper that made
lattice share size look survivable. Read against pairings it is still four orders
of magnitude off the 48 to 80 bytes per party of [[cgpp-bte]] and
[[choudhuri-garg-policharla-wang-onetime]].

## Desiderata

Satisfies [[D3]] and [[D8]]. Partially [[D13]]: small *for a lattice scheme*, not
small in absolute terms. Partially [[D5]]: the polynomial modulus holds under an
a priori bound on decryption queries, which is the constraint tracked in
[[remove-query-bound-poly-modulus]]. Fails [[D2]] and [[D14]].

## Relevance to encrypted mempools

The current reference point for lattice decryption share size. Its bounded-query
caveat is the thing to check before deploying: a public mempool decryption service
is precisely a setting where the adversary controls the query count.
