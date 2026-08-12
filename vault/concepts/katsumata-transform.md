---
id: katsumata-transform
type: technique
title: Katsumata transform
aliases: ["Katsumata"]
pq: true
family: proof
assumes: [qrom]
---

A simple technique to bootstrap lattice zero-knowledge proofs into QROM-secure
NIZKs (eprint 2021/927). The reason it belongs in this KB: a post-quantum
threshold scheme that attaches a Fiat-Shamir proof to each ciphertext needs that
proof to be sound against a quantum adversary, and a plain ROM argument does not
give that. See [[qrom]].
