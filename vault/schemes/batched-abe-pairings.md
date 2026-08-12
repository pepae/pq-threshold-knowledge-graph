---
id: batched-abe-pairings
type: scheme
title: Batched attribute-based encryption from bilinear pairings
aliases: ["TB-ABE"]
eprint: "2026/1454"
year: 2026
status: preprint
peer_reviewed: false
source_depth: full-text
pq: false
batched: true
authors: [ramprasad-sarkar, shayeef-murshid, mriganka-mandal]
assumptions: [dbdh, rom]
techniques: [batched-threshold-encryption, shamir-secret-sharing]
satisfies: [D14]
partially_satisfies: [D5]
fails: [D2, D6, D8]
---

Sarkar, Murshid and Mandal (Indian Statistical Institute Kolkata). Batched
attribute-based encryption from bilinear pairings, plus the first *threshold*
batched ABE (TB-ABE).

## Why it is in this KB

It appears in Wagner's survey only under "TODO / not yet categorized", but its own
keywords list encrypted mempools, so it is squarely in scope rather than adjacent.
It generalises the batched-key-issuance idea from identities to attributes, which
is the direction [[blt-batch-ibe]] gestures at in its KP-ABE construction.

## Key mechanism

Batched key issuance for ABE, with the master secret distributed among L
authorities via [[shamir-secret-sharing]], so any threshold T of authorities can
issue. Security is against static corruption of up to T-1 authorities together
with *adaptive key-share queries*.

## Assumptions

Proven under the standard [[dbdh]] assumption in the [[rom]]. Worth noting: that is
a weaker and more standard assumption than most pairing-based schemes here use.
[[gkpw-silent-setup]] and [[beast-mev]] are [[ggm]] proofs, and
[[waters-wu-silent]] and [[btx]] rest on [[q-type-pairing]] assumptions. On
assumption quality alone this is the best-founded pairing scheme in the KB.

## Desiderata

Satisfies [[D14]] via batched key issuance. Partially [[D5]] (adaptive key-share
queries). Fails [[D2]] (the master secret is shared out, not silently derived),
[[D6]] (static corruptions) and [[D8]] (pairings).

## Relevance to encrypted mempools

Attribute policies are more expressive than a block needs, so the interesting
question is whether the extra generality costs anything against a plain threshold
batch IBE like [[blt-batch-ibe]]. Comparing the two on ciphertext and key-issuance
size is the obvious next piece of reading.
