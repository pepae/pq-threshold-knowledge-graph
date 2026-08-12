---
id: tacet-silent
type: scheme
title: TACET silent variant
aliases: ["TacetQSilent", "TACET Stage 2"]
status: draft
peer_reviewed: false
maturity: experimental
self_assessed: true
source_depth: full-text
pq: true
silent_setup: true
batched: true
epoch_free: true
url: https://github.com/pepae/pq-threshold
assumptions: [l-succinct-lwe, decomposed-lwe, qrom, mlwe]
techniques: [silent-setup, wee-matrix-commitment, distributed-broadcast-encryption, zero-sharing-masks]
implemented_by: [pq-threshold]
builds_on: [tacet, champion-wu-dbe]
satisfies: [D1, D2, D3, D8, D9, D11, D14]
partially_satisfies: [D5, D6, D13]
disputes:
  - "Unpublished and unreviewed, same caveat as the TACET core note. Claims here are self-assessed."
---

> Same caveat as [[tacet]]: unpublished, unreviewed, self-assessed.

The same construction with the one-time DKG replaced by a silent, dealerless setup,
and with a constant-size ciphertext that does not grow with the committee.

## Key mechanism

Each keyper generates and posts its own key; the joint encryption key is a
deterministic public function of the posted keys, following the
[[champion-wu-dbe]] line from [[l-succinct-lwe]]. The constant-size ciphertext
comes from a [[wee-matrix-commitment]], with the commitment relation checked
exactly. The project reports a three-element ciphertext independent of committee
size, and measures it flat as the committee grows.

## Why a silent variant is not automatically worth it

The project's own framing is worth preserving because it is the honest answer to
[[D2]]: silent setup costs a stronger (though still falsifiable) assumption and
selective security, and only pays off in the right deployment. For a fixed small
keyper set, a one-time DKG under plain [[mlwe]] is simpler and sufficient. Silent
earns its keep when the committee is a small *rotating* subset of a large validator
pool, where re-running a DKG per rotation is the real cost. That is precisely
Wagner's conditional phrasing of [[D2]].

## Desiderata

Claims [[D1]], [[D2]], [[D3]], [[D8]], [[D9]], [[D11]] and [[D14]], with [[D5]],
[[D6]] and [[D13]] partial. The committee-size ceiling from
[[low-norm-secret-sharing]] applies here exactly as it does to the core, since it
comes from the sharing and not the setup.

## Relevance to encrypted mempools

If the claims hold, this is the only implemented artifact in the KB that targets
post-quantum silent setup and batching at once, which is
[[silent-pq-threshold-t-of-n]]. Given its status, treat it as evidence that the
combination is buildable, not that it is solved.
