---
id: qrom
type: assumption
title: Quantum Random Oracle Model
aliases: ["QROM"]
pq: true
falsifiable: false
family: idealization
reduces_to: [rom]
---

The random oracle model against an adversary that can query the oracle on
superpositions. The right idealization for a post-quantum scheme: a ROM proof does
not automatically carry over.

Getting lattice proofs into the QROM is exactly what the
[[katsumata-transform]] is for. [[tacet]]'s silent variant is IND-CCA proven in
the QROM.
