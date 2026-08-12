---
id: dbdh
type: assumption
title: Decisional Bilinear Diffie-Hellman
aliases: ["DBDH"]
pq: false
falsifiable: true
family: pairing
source_depth: full-text
---

A standard, static pairing assumption. Notable in this KB for being the *weakest
kind of pairing assumption used by anything here*: unlike a [[q-type-pairing]]
assumption it does not grow with the scheme's usage, and unlike a [[ggm]] proof it
is falsifiable and standard.

Used by [[batched-abe-pairings]] in the [[rom]]. When comparing pairing-based
schemes, assumption quality varies more than the performance tables suggest, and
this is the good end of that range. Not post-quantum.
