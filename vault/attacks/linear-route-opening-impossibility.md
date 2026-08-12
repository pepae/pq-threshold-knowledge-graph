---
id: linear-route-opening-impossibility
type: attack
title: Constant-size batch opening is impossible on the linear lattice route
status: draft
source_depth: repo
attacks: [tacet]
opens: [sublinear-pq-batch-decryption]
disputes:
  - "Recorded from an unpublished project's own audit log, not from a peer-reviewed impossibility result. The argument is elementary and reproduced here so it can be checked, but it has not been externally reviewed."
---

An impossibility observation from [[tacet]]'s audit log, recorded here because it
generalises past that project.

## The argument

On the linear lattice route, a decapsulator recovering position j of a batch needs
the value `s^T u_j`. For a batch B, those are |B| independent values. A single ring
element cannot encode |B| independent values, so a constant-size (single R_q
element) batch opening is impossible on this route. Opening is therefore O(|B|), one
element per ciphertext.

## Why it matters

It explains, in one line, why the succinct batch opening that pairing-based schemes
get so cheaply (a single group element in [[beat-mev]], 48 to 80 bytes per party in
[[cgpp-bte]] and
[[choudhuri-garg-policharla-wang-onetime]]) does not transfer to the obvious lattice
analogue. Succinct lattice batch opening needs something other than the linear
route, which is what [[blt-batch-ibe]] supplies with a trapdoor-sampler
construction, and why its parameters are what they are.

Together with [[blt25-implementation]]'s measurement that BLT's provably secure
parameters do not run, this bounds the problem from both sides. That is the content
of [[sublinear-pq-batch-decryption]].

## Status

The finding forced a correction in TACET's own size tables and its [[D13]] rating.
Treat the impossibility as a sanity argument to verify rather than a citable
theorem.
