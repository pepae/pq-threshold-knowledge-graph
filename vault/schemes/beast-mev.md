---
id: beast-mev
type: scheme
title: BEAST-MEV
eprint: "2025/1419"
year: 2025
status: preprint
peer_reviewed: false
source_depth: abstract
pq: false
batched: true
epoch_free: true
silent_setup: true
assumptions: [ggm]
techniques: [silent-setup, batched-threshold-encryption]
builds_on: [gkpw-silent-setup, beat-mev, cgpp-bte]
supersedes: [beat-mev]
satisfies: [D2, D3, D4, D14]
partially_satisfies: [D7, D15]
fails: [D1, D8, D10]
authors: [jan-bormet, arka-rai-choudhuri, sebastian-faust, sanjam-garg, hussien-othman, guru-vamsi-policharla, ziyan-qu, mingyuan-wang]
---

The first batched threshold encryption scheme with silent setup. Eight authors from
both the Darmstadt [[beat-mev]] team and the Berkeley [[gkpw-silent-setup]] and
[[cgpp-bte]] teams, which is itself informative: it is the merge of the two lines.

## Why both properties at once

Silent setup ([[D2]], from GKPW) and batched decryption ([[D14]], from CGPP) had
been achieved independently. The paper's argument is that a decentralised encrypted
mempool at Ethereum scale needs both simultaneously, and neither prior line gives
the other for free.

## Key mechanism

Make [[gkpw-silent-setup]] additively homomorphic, which lets batch decryption
material be aggregated the way BEAT-MEV aggregates PRF keys. Pairing-based, with
formal definitions for the primitive and security proved in the [[ggm]].

## Desiderata

Satisfies [[D2]], [[D3]], [[D4]] (CCA-secure under static corruptions) and
[[D14]]. Partially [[D7]] and [[D15]]: Wagner's survey notes the concretely
efficient variant evaluated is the CPA one, so read the reported performance as the
CPA scheme's. Fails [[D1]] (trusted setup), [[D8]], and [[D10]] (large keys).

## Relevance to encrypted mempools

The strongest classical answer in the KB: silent, batched, epoch-free, CCA under
static corruptions. It is the target a post-quantum construction has to match, and
nothing lattice-based comes close. That gap is [[silent-pq-threshold-t-of-n]].
