---
id: remove-query-bound-poly-modulus
type: open-problem
title: Removing the a priori query bound at polynomial modulus
state: open
pq: true
opened_by: [wagner-desiderata]
---

## Statement

Lattice threshold decryption at polynomial modulus without an a priori bound Q on
the number of decryption queries.

## Where we stand

Every polynomial-modulus result in the KB buys the small modulus with a bound on
queries, because the flooding noise is sized against Q.
[[pilvi]] states a polynomial modulus "with bounded queries".
[[sjtu-adaptive-threshold-decryption]] carries Q explicitly, and
[[tacet]] reads its query bound as Q = 2^12 in order to close its budget.
[[boudgoust-scholl]] and [[micciancio-suhl]] reduce the flooding requirement
dramatically but the dependence on the query count does not vanish.

## Why it matters specifically for encrypted mempools

In most threshold settings a query bound is a modelling formality. Here it is not.
The decryption oracle is a public, permissionless service: the committee decrypts
whatever appears in a block, forever. Q is therefore a function of chain lifetime and
adversarial spam, not of a security parameter chosen at design time. A scheme whose
modulus must be sized against Q needs an answer to "what happens at query Q+1", and
"re-key the committee" is an operational answer with its own costs.

## What needs to be solved

Either a flooding analysis whose noise requirement is independent of the query count,
or a scheme that refreshes the relevant randomness per batch so that each batch
carries its own small Q. The second is more plausible and connects to
[[D9]]: if shares are already bound to a per-block context, the natural question is
whether the query budget can be made per-context too.
