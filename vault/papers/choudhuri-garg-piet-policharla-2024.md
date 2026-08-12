---
id: choudhuri-garg-piet-policharla-2024
type: paper
title: "Mempool Privacy via Batched Threshold Encryption: Attacks and Defenses"
aliases: ["CGPP 2024", "Choudhuri-Garg-Piet-Policharla"]
eprint: "2024/669"
venue: USENIX Security 2024
year: 2024
status: published
peer_reviewed: true
source_depth: abstract
pq: false
authors: [arka-rai-choudhuri, sanjam-garg, julien-piet, guru-vamsi-policharla]
---

The bibliographic record for the paper that introduces batched threshold encryption.
The construction itself is noted separately as [[cgpp-bte]]; this node exists because
later work cites the *paper* (for its attacks and its definitions) as often as it
cites the scheme.

## The two halves

**Attacks.** The paper is titled "Attacks and Defenses" and the attack half is what
makes [[D7]] a desideratum: batching creates shared fate across a batch, so an
adversary who can place a chosen ciphertext alongside a victim's gets leverage
unless the scheme defends against it.

**Defenses.** The batched threshold encryption primitive, with O(n) rather than
O(nB) communication.

## Note on naming

This paper is sometimes referred to as the "MEVade attack paper". That is a
conflation: [[mevade]] is a different paper by different authors, sharing only Julien
Piet. Keep the two distinct.
