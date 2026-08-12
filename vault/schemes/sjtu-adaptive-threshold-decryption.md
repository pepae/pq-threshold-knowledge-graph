---
id: sjtu-adaptive-threshold-decryption
type: scheme
title: Adaptively secure threshold decryption at polynomial modulus
aliases: ["TD0", "TD1", "TD2", "ZZHLH26"]
eprint: "2026/1627"
year: 2026
status: preprint
peer_reviewed: false
source_depth: full-text
pq: true
modulus: polynomial
assumptions: [lwe, matrix-hint-lwe, rom]
techniques: [polynomial-noise-flooding, zero-sharing-masks, shamir-secret-sharing]
satisfies: [D3, D8]
partially_satisfies: [D4, D6, D5]
fails: [D2, D14]
builds_on: [devevey-libert-nguyen-peters-yung, micciancio-suhl, boudgoust-scholl]
resolves: [devevey-adaptive-poly-modulus]
authors: [yuxin-zhang, yunxiao-zhou, shuai-han, shengli-liu, xinyi-huang]
---

Zhang, Zhou, Han, Liu and Huang give three threshold decryption schemes that are
secure under *adaptive* corruptions with a polynomial modulus, resolving an open
problem left by [[devevey-libert-nguyen-peters-yung]].

## The three schemes

* **TD0**: adaptively CPA-secure in the asynchronous setting, standard model.
  Modulus is polynomial for a small number of users.
* **TD1**: adaptively CCA-secure with polynomial modulus.
* **TD2**: adaptively CCA-secure, and supports polynomially many users by using
  Shamir secret sharing, which is what lifts the committee-size ceiling.

## Key mechanism

Two pieces.

**Refined polynomial noise flooding** (Lemma 6), based on a min-entropy analysis
of the secret shares *conditioned on linear matrix hints*. Adaptive corruption is
exactly what hands the adversary such hints, so the conditioning is not a
technicality, it is the point. The paper states that a modulus of size O(sqrt(l))
suffices for CCA security of TD2 under this lemma.

**ZeroShare masking**, a pairwise-seed [[zero-sharing-masks]] construction. Party
i holds seeds shared with every other party and computes

    delta_i,S = sum_{j in S\{i}} H(seed_i,j, (ct,S)) - sum_{j in S\{i}} H(seed_j,i, (ct,S))

which sums to zero across S by construction, so the masks vanish on combination.
The partial decryption is then `h_i,S = c^T (lambda_i,S k_i) + y_i,S + delta_i,S`
with `lambda_i,S` the recovery coefficients and `y_i,S` the flooding noise. Note
that the mask is bound to `(ct, S)`, which makes these shares context-dependent in
the sense of [[D9]] as a side effect of the masking design.

## Caveats the abstract does not surface

Because the mask comes from a random oracle, TD2's CCA security relies on the
[[rom]], so this is not a standard-model result throughout. And robustness is
harder than the abstract's mention of publicly verifiable partial decryptions
suggests: the paper says it is quite involved to give a NIZK for well-formedness
of the masked share, and points at recent identifiable-abort work for threshold
signatures as the way forward. Treat robustness for TD2 as open engineering.

## Desiderata

Satisfies [[D3]] and [[D8]]. Partially [[D6]]: this is the strongest adaptive
corruption result in the KB for lattices, but it is not batched, so it does not
settle [[adaptive-corruptions-batched-lattice]]. Partially [[D4]] (CCA in the ROM)
and [[D5]]. Fails [[D2]] and [[D14]].

## Relevance to encrypted mempools

Closes the adaptive-corruption gap for plain threshold decryption. The mempool
setting needs the same result for *batched* schemes, which nobody has.
