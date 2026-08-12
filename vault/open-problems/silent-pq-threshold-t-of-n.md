---
id: silent-pq-threshold-t-of-n
type: open-problem
title: Silent setup for post-quantum t-of-n threshold encryption
state: partially-resolved
pq: true
opened_by: [wagner-desiderata]
---

## Statement

Build a t-of-n threshold encryption scheme with silent setup ([[D2]]) that is
post-quantum ([[D8]]), concretely efficient, and ideally also batched ([[D14]]).

## Where we stand

**Classically, solved.** [[gkpw-silent-setup]] over pairings, and generically from
key-anonymous PKE by [[hall-andersen-simkin-wagner-silent]]. Silent *and* batched is
also solved classically by [[beast-mev]].

**Post-quantum, the theory has arrived.** The lattice route runs through
[[champion-wu-dbe]] (from [[l-succinct-lwe]]) and then
[[champion-wu-monotone-dnf]] and [[champion-wu-optimal-dnf]] (from
[[decomposed-lwe]]). The last of these gets parameters independent of policy size in
the ROM, plus an adaptive broadcast variant in the plain model. Threshold encryption
with silent setup is the threshold-policy special case, so in principle this closes
the existence question.

**What is missing is engineering and composition.** None of those papers is
implemented. [[tacet-silent]] is the only artifact that attempts the composition,
and it is an unreviewed draft.

## What needs to be solved

1. An implementation of the [[decomposed-lwe]] line with concrete parameters, so the
   constants are known rather than asymptotic.
2. Silent setup composed with *batching*, post-quantum. Classically this took
   [[beast-mev]] making a silent scheme additively homomorphic; the lattice analogue
   is unexplored.
3. CCA2 and adaptive corruptions on top, which currently cost either the ROM or
   selective security in every candidate.

## Why it is only partially resolved

The existence question is arguably answered. The deployable-artifact question is not,
and for an encrypted mempool the second is the one that matters.
