---
id: champion-wu-monotone-dnf
type: scheme
title: Distributed monotone-policy encryption for DNFs from lattices
aliases: ["Champion-Wu DNF"]
eprint: "2026/318"
year: 2026
status: preprint
peer_reviewed: false
source_depth: full-text
pq: true
silent_setup: true
ciphertext_size: poly(lambda, log N) for N variables in the DNF
assumptions: [decomposed-lwe, rom]
techniques: [monotone-policy-encryption, silent-setup]
builds_on: [champion-wu-dbe]
superseded_by: [champion-wu-optimal-dnf]
satisfies: [D1, D2, D8, D11]
partially_satisfies: [D5]
fails: [D14]
authors: [jeffrey-champion, david-wu]
---

Distributed monotone-policy encryption for DNF formulas supporting an unbounded
number of users, from [[decomposed-lwe]] in the [[rom]], with a *transparent*
setup and ciphertext size poly(lambda, log N).

## Why it generalises the right way

Distributed monotone-policy encryption strictly generalises both threshold
encryption with silent setup (threshold policy) and
[[distributed-broadcast-encryption]] (set-membership policy). Getting it for DNFs
from a simple falsifiable lattice assumption, where previously only plain witness
encryption sufficed, is the advance.

## Desiderata

Satisfies [[D1]] (transparent setup, no trapdoor), [[D2]], [[D8]] and [[D11]].
Partially [[D5]]: security is (semi-)selective and static. Fails [[D14]].

## Relevance to encrypted mempools

Together with [[champion-wu-optimal-dnf]] this is the most credible route to
post-quantum silent setup, and therefore the literature to watch for
[[silent-pq-threshold-t-of-n]]. Neither paper is implemented.
