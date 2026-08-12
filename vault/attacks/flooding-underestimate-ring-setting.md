---
id: flooding-underestimate-ring-setting
type: attack
title: Flooding-noise underestimate in the ring setting
status: draft
source_depth: repo
attacks: [tacet]
disputes:
  - "Recorded from an unpublished project's own audit log. It is a bug found in that project's draft, fixed there, and is included as a reusable warning rather than as a result about any published scheme."
---

A security bug found in [[tacet]]'s draft and recorded because the underlying
mistake is easy to repeat.

## The mistake

The draft set the flooding noise using the plain-LWE smudging bound
`sigma_fl = sigma_dec * sqrt(2*pi*a*Q)`. In the *ring* setting the Renyi divergence
multiplies over the N ciphertext coordinates, so that bound is short by a factor of
sqrt(N). At the draft's value the flooding divergence came out at exp(N/2) = 2^185,
which is to say the flooding hid nothing at all.

The fix was `sigma_fl = sigma_dec * sqrt(2*pi*a*Q*N)`, with the query bound read as
Q = 2^12 so that the flooding noise, total noise, modulus and failure rate stayed
unchanged while the flooding became genuinely secure.

## Why it is worth a node

Three reasons, all general.

First, a flooding bound derived for plain [[lwe]] does not transfer to [[mlwe]]
unchanged. Anyone thresholdizing a ring-based scheme by citing a plain-LWE smudging
lemma should check the dimension count.

Second, it was invisible to correctness tests. Decryption succeeded throughout: the
noise budget still closed, the failure rate was unchanged. Only building the
*simulator* exposed it. That is an argument for validating the security proof's
objects, not just the scheme's functionality.

Third, the same audit found the related error of treating the Renyi divergence in
the flooding hop as 1+o(1) when it is a multiplicative constant of about e^(1/2).
See [[polynomial-noise-flooding]].
