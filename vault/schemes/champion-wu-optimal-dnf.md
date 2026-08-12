---
id: champion-wu-optimal-dnf
type: scheme
title: Optimal distributed monotone-policy encryption for DNFs
eprint: "2026/1464"
year: 2026
status: preprint
peer_reviewed: false
source_depth: full-text
pq: true
silent_setup: true
ciphertext_size: independent of policy size in the ROM; k*L^(1/2) for k-DNF in the plain model; |S|^(2/3) for adaptive broadcast
assumptions: [decomposed-lwe, rom]
techniques: [monotone-policy-encryption, distributed-broadcast-encryption, silent-setup]
builds_on: [champion-wu-monotone-dnf, champion-wu-dbe]
supersedes: [champion-wu-monotone-dnf, champion-wu-dbe]
satisfies: [D1, D2, D8, D11]
partially_satisfies: [D5, D6]
fails: [D14]
disputes:
  - "Records this as superseding 2026/318 and 2024/1417 on the strength of strictly better parameters by the same authors. Neither paper states the relation, so treat the supersedes edges as an editorial judgement rather than an authors' claim."
authors: [jeffrey-champion, david-wu]
---

Champion and Wu again, with three results that together dominate their earlier work.

## The three results

* **Optimal in the ROM.** Public parameters, user public keys and ciphertext are
  all independent of the policy size, for DNF policies from
  [[decomposed-lwe]]. As a corollary, a reusable succinct computational secret
  sharing scheme for DNFs.
* **Plain model, k-DNF.** Ciphertext `k * L^(1/2)` where k bounds min-term size and
  L is the number of min-terms. First such scheme from decomposed LWE without a
  random oracle. Full succinctness is also reachable in the plain model, but only
  under selective security.
* **Adaptive distributed broadcast encryption.** Ciphertext `|S|^(2/3)` under
  decomposed LWE with polynomial modulus-to-noise ratio, in the plain model. The
  first lattice scheme with adaptive security supporting an a priori unbounded
  number of users.

## Desiderata

Satisfies [[D1]], [[D2]], [[D8]] and [[D11]]. Partially [[D6]]: the broadcast
result is adaptive, which is new for lattices, but the fully succinct plain-model
variant is selective only, so which desideratum you get depends on which of the
three constructions you take. Partially [[D5]] for the same reason. Fails [[D14]].

## Relevance to encrypted mempools

The current best lattice route to [[D2]]. Read it together with
[[champion-wu-monotone-dnf]]: this paper is where the parameters become good enough
to argue about deployment rather than existence.
