---
id: post-inclusion-ordering
type: open-problem
title: Post-inclusion ordering
state: open
pq: false
opened_by: [wagner-desiderata, mevade]
---

## Statement

Once transactions are decrypted, who decides the order they execute in, and what
stops the proposer extracting value at that point?

## Why it belongs in a cryptography KB

Because it bounds what any scheme in this KB can achieve. Threshold encryption hides
transaction *contents* until inclusion is fixed. It says nothing about the *order* of
execution afterwards. A proposer who learns a whole block's contents at decryption
time, and who still controls ordering within the block, retains a substantial part of
the MEV they started with.

[[mevade]] is explicit that hiding contents is only half the design and pairs it with
randomized execution order. Wagner's template has the same shape: decrypt after
block i is fixed, execute in block i+1, which presumes something has already fixed
the order.

## Where we stand

This is a consensus problem, not a cryptographic one, and it is outside the D1-D15
list entirely. Approaches include commit-then-reveal ordering, randomized ordering,
fair-ordering consensus protocols, and enshrining the ordering rule in protocol.
[[bbnrs-context-dependent]] is the closest cryptographic neighbour: fixing a context
per block is what makes "the order was decided before decryption" a checkable
statement rather than a convention.

## What needs to be solved

A statement of what an encrypted mempool guarantees *end to end*, combining a
threshold scheme's confidentiality with an ordering rule, such that the composition
has a security definition. The KB currently has fifteen desiderata for the
cryptography and none for the composition, which is itself the finding.

## What to read next

The fair-message-ordering SoK and EIP-8105, both listed in `papers/WANTED.md`. The
EIP matters because it is encryption-agnostic: it defines the interface an encrypted
mempool must meet, which is where the ordering question has to be answered.
