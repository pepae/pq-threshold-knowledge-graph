---
id: weighted-bte
type: scheme
title: Weighted batched threshold encryption
aliases: ["Weighted BTE"]
eprint: "2025/2115"
year: 2025
status: preprint
peer_reviewed: false
source_depth: mixed
pq: false
batched: true
epoch_free: true
assumptions: [q-sdh, agm]
techniques: [kh-pprf, batched-threshold-encryption]
builds_on: [beat-mev]
satisfies: [D3, D13, D14]
partially_satisfies: [D15]
fails: [D2, D8]
attacked_by: [index-collision-censorship]
authors: [amit-agarwal, kushal-babel, sourav-das, babak-poorebrahim-gilkalaye, arup-mondal, benny-pinkas, peter-rindal, aayush-yadav]
---

Agarwal, Babel, Das, Poorebrahim Gilkalaye, Mondal, Pinkas, Rindal and Yadav
improve [[beat-mev]] in three directions. Note this is a different group from the
BEAT-MEV authors.

## The three improvements

**Quasilinear instead of quadratic.** Replace BEAT-MEV's [[kh-pprf]] with an
FFT-friendly alternative, cutting computational cost from quadratic to quasilinear
in the batch size. About 6x faster at batch 512 with no increase in communication.

**Weighted committees.** Each server carries a weight, such as stake, while
communication stays *independent of the weights*. BEAT-MEV with naive
virtualization (one virtual party per unit of weight) pays communication linear in
total weight. About 50x better for 100 validators with total weight 5000
distributed per the Solana stake distribution.

**Tunable collision handling.** A generalization of BEAT-MEV's sub-batch approach
that trades ciphertext size against server communication for a target failure rate,
rather than fixing one point on that curve.

## Assumptions

[[q-sdh]] and discrete log, in the [[agm]], with security holding under static
corruption. Note the difference from [[beat-mev]], which it improves: BEAT-MEV
rests on [[ddh]], a static assumption, while this scheme moves to a q-type one.
That is a real cost paid for the efficiency gain, and it is invisible in the
performance tables.

## Desiderata

Satisfies [[D3]], [[D13]] and [[D14]]. Partially [[D15]]: quasilinear is the right
asymptotic fix and 6x is the measured gain. Fails [[D2]] and [[D8]].

## Why weighting matters for encrypted mempools

On a proof-of-stake chain the committee is naturally stake-weighted, and
virtualization is the obvious wrong answer. This is the only scheme in the KB that
addresses it directly.

## Inherited limitation

It is index-dependent, so [[index-collision-censorship]] applies. Tunable collision
handling moves the size and communication trade-off but does not remove the
underlying censorship vector.
