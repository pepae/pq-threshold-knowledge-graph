---
id: kzg-commitments
type: technique
title: KZG polynomial commitments
aliases: ["KZG"]
pq: false
family: commitment
---

Pairing-based polynomial commitments. [[cgpp-bte]] builds its batched threshold
encryption from trapdoors for KZG commitments together with witness encryption for
KZG openings, which Wagner's survey calls an elegant idea. Not post-quantum, and
the trapdoor is what forces the per-epoch setup.
