---
id: champion-wu-dbe
type: scheme
title: Distributed broadcast encryption from lattices
aliases: ["Champion-Wu DBE", "CW24"]
eprint: "2024/1417"
venue: TCC 2024
year: 2024
status: published
peer_reviewed: true
source_depth: full-text
pq: true
silent_setup: true
assumptions: [l-succinct-lwe]
techniques: [distributed-broadcast-encryption, wee-matrix-commitment, silent-setup]
satisfies: [D2, D8]
partially_satisfies: [D5]
fails: [D14]
superseded_by: [champion-wu-optimal-dnf]
authors: [jeffrey-champion, david-wu]
---

The first distributed broadcast encryption from a *falsifiable* lattice assumption,
namely [[l-succinct-lwe]] (Wee, CRYPTO 2024). Users generate their own keys; the
ciphertext is sublinear in the recipient set.

## Why falsifiability is the headline

Prior constructions in this space went through general
[[witness-encryption]], which is not a falsifiable assumption. Moving to a concrete
lattice assumption is what turns silent setup from a plausibility argument into a
candidate for deployment, and it is the reason this line matters for post-quantum
[[D2]].

## Desiderata

Satisfies [[D2]] and [[D8]]. Partially [[D5]]. Fails [[D14]]: this is a
non-batched primitive, generalised in the policy direction rather than the batching
direction.

## Relevance to encrypted mempools

Threshold encryption with silent setup is the threshold-policy special case of this
family, so a lattice DBE is a lattice silent threshold scheme in disguise. It is
the technical root of [[tacet-silent]]'s constant-size ciphertext.
