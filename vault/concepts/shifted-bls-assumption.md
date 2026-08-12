---
id: shifted-bls-assumption
type: assumption
title: Shifted BLS assumption
pq: false
falsifiable: true
family: pairing
source_depth: full-text
---

A new assumption introduced by [[choudhuri-garg-policharla-wang-onetime]]
(Definition 1 there) to support its *shifted BLS* construction, where the committee
signs not a commitment `com` but `com` shifted by a public random group element.

The paper shows the assumption reduces to more standard assumptions in the
[[agm]], arguing that the two attack shapes it rules out are the only ways to break
the system. So it is not a bare new assumption, but the reduction is
model-dependent.

This is what Wagner's survey means by "needs new interactive assumption for
security proof". Worth flagging when comparing this scheme against
[[beat-mev]] on [[ddh]] or [[batched-abe-pairings]] on [[dbdh]]: the performance
numbers are close, the assumption footing is not.
