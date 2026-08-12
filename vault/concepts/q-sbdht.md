---
id: q-sbdht
type: assumption
title: q-strong Bilinear Diffie-Hellman Triple
aliases: ["q-SBDHT"]
pq: false
falsifiable: true
family: pairing
source_depth: full-text
---

The q-strong Bilinear Diffie-Hellman Triple assumption, introduced by
[[cgpp-bte]]. A strengthening of [[q-sdh]] in two directions, which the name
records: the adversary is given *additional triples* beyond those in q-SDH, and it
must output a value in the target group.

## Why it was needed

In KZG polynomial commitments, [[q-sdh]] gives *evaluation binding*: an adversary
cannot produce two accepting evaluation proofs for two different values at one
point. The paper explains that this is not sufficient in the batched threshold
setting, where the commitment trapdoor is used constructively rather than merely
assumed hard to find, so a stronger statement about what the adversary can produce
is required.

## How to weigh it

A new q-type assumption introduced for one construction is the weakest link in an
otherwise concretely efficient scheme. Compare [[dbdh]], which is static and
standard, and [[ggm]], which is not falsifiable at all. Ranking the pairing-based
schemes by assumption quality gives a different ordering than ranking them by
performance, which is exactly why Wagner's note asks about assumptions separately.
