---
id: index-collision-censorship
type: attack
title: Index-collision censorship in index-dependent batch encryption
aliases: ["censorship vulnerability", "succinctness vulnerability"]
eprint: "2025/1254"
year: 2025
status: preprint
source_depth: full-text
attacks: [beat-mev, weighted-bte]
builds_on: [blt-batch-ibe]
opens: [sublinear-pq-batch-decryption]
disputes:
  - "Wagner's survey calls this a 'succinctness vulnerability'. The source paper frames it as a censorship vulnerability arising from the succinctness trade-off, and it is not a break of confidentiality. This KB uses the paper's framing."
---

Identified by [[blt-batch-ibe]]. A censorship vector, not a confidentiality break,
against batch encryption schemes whose ciphertexts carry an *index*.

## The attack

Index-dependent schemes need every ciphertext in a decryptable group to carry a
distinct index, and encryptors do not coordinate. The standard fix is sub-batches:
split the batch into groups of distinct indices and publish one pre-decryption key
per group.

An attacker chooses its index values adversarially and submits Omega(log l)
ciphertexts to a batch, all with the *same* index. Now the system faces a forced
choice: either produce Omega(log l) sub-batches and pre-decryption keys to
accommodate them, or exclude most transactions sharing that index from the batch.
The first inflates keys and ciphertexts; the second is censorship of honest
transactions that happen to collide.

## Who is affected

[[beat-mev]] and, per the source paper, other index-dependent batch encryption
schemes that build on it. [[weighted-bte]] generalises the collision handling into a
tunable trade-off, which moves the operating point but does not remove the vector.

## Why it matters more than it looks

An encrypted mempool exists to stop transaction-level manipulation. An attack that
lets an adversary cheaply force honest transactions out of a block is a direct
defeat of the goal, even though nothing is decrypted. It is a good example of a
property that no D1-D15 desideratum captures cleanly: censorship resistance is
adjacent to [[D7]] but not the same thing.
