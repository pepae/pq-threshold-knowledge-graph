---
id: tacet
type: scheme
title: TACET
aliases: ["TACET-Q", "TACET core"]
status: draft
peer_reviewed: false
maturity: experimental
self_assessed: true
source_depth: full-text
pq: true
batched: true
epoch_free: true
silent_setup: false
modulus: prime q = 2^31 - 511
assumptions: [mlwe, module-sis]
techniques: [zero-sharing-masks, vector-commitments, low-norm-secret-sharing, replicated-secret-sharing, fiat-shamir-nizk, noise-flooding]
url: https://github.com/pepae/pq-threshold
implemented_by: [pq-threshold]
builds_on: [bendlin-damgard, bbnrs-context-dependent]
satisfies: [D1, D3, D9, D12, D14, D15]
partially_satisfies: [D4, D5, D6, D8, D10, D11, D13]
fails: [D2]
opens: [low-norm-small-share-large-t]
attacked_by: [flooding-underestimate-ring-setting, linear-route-opening-impossibility]
disputes:
  - "Not peer reviewed and not comparable in maturity to the published work in this KB. Every claim here is self-assessed by its own authors and test suite; treat it as an engineering report, not a result."
  - "The headline (t,K)=(67,100) parameter set is declared inconsistent by the project's own README: the cited Pilvi sharing's recovery norm there is about 10^67, not 16.4. The scheme is stated to be deployable at a smaller committee with replicated sharing."
---

> **Read this note differently from the rest of the KB.** TACET is an unpublished
> working draft with no external review. It is included because it is the only
> attempt in the KB to *build and measure* a post-quantum context-anchored batched
> threshold KEM end to end, and because the act of building it produced corrections
> that are useful independently. It is not evidence at the same level as the
> published schemes it sits beside.

A Module-LWE anchored, epoch-free, batched threshold KEM. A transaction is
encrypted to a committee, and only after the block including it is fixed can a
t-of-n quorum recover the key.

## Key mechanism

Partial decryptions are bound to a per-block *anchor*, a
[[vector-commitments]] commitment to the batch, by a context-keyed
[[zero-sharing-masks]] mask. The masks cancel exactly when a quorum acts under one
anchor, and any mixing of two anchors leaves an uncancelled pseudorandom residue,
so fork isolation reduces to PRF pseudorandomness rather than to a checkable tag.
Decryption touches only the committed batch, so excluded transactions stay hidden.

## Honest limitations, as stated by the project

**Committee-size ceiling.** The noise budget needs
[[low-norm-secret-sharing]] with recovery norm about sqrt(t), whose per-party
material is C(n-1, t-1). That keeps committees small, hits the DKG core and the
silent variant equally, and is a property of the sharing rather than of the setup
choice. Scaling to large committees is open: see
[[low-norm-small-share-large-t]].

**One parameter set is inconsistent.** See the `disputes` field.

**No claim to new cryptography.** The project states explicitly that the
assumptions and constructions are the cited ones and that the contribution is the
mempool-specific design, the implementation and the validation.

## Corrections produced by building it

The project's audit log records eight corrections to its own earlier draft. Two are
recorded in this KB as nodes because they generalise beyond TACET:
[[linear-route-opening-impossibility]] and
[[flooding-underestimate-ring-setting]]. The others include a context mask that
neither cancelled nor was removable (fixed by making it a zero-sharing), a
cross-context combinability break, a misattribution of only-included security to
commitment membership gating rather than to the committee scoping partial
decryption, a non-NTT-friendly modulus (q = 2^32 replaced by the prime
q = 2^31 - 511), and a Renyi divergence treated as 1+o(1) when it is a
multiplicative constant of about e^(1/2).

## Desiderata

The project's own scorecard reports 10 pass, 5 partial, 0 fail against D1-D15, each
checked by a runtime test, a measurement, or a named artifact. This note reproduces
that mapping, with `self_assessed: true` recorded in frontmatter so a query can
exclude it. Notably it claims [[D9]] with an executed harvesting test, and [[D1]]
via a public matrix expanded from a seed.

## Relevance to encrypted mempools

Its value to this KB is the measurements and the corrections, not the construction.
It is the only node that answers "what breaks when you actually build this", and the
two audit findings promoted to their own nodes are the reason to keep it.
