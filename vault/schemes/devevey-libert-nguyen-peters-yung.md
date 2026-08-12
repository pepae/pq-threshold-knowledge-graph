---
id: devevey-libert-nguyen-peters-yung
type: scheme
title: Non-interactive CCA2 threshold cryptosystems without pairings
aliases: ["Devevey et al.", "DLNPY21"]
eprint: "2021/630"
venue: PKC 2021
year: 2021
status: published
peer_reviewed: true
source_depth: full-text
pq: false
assumptions: [dcr, lwe]
techniques: [shamir-secret-sharing]
satisfies: [D3, D4, D6]
fails: [D2, D14]
opens: [devevey-adaptive-poly-modulus]
authors: [julien-devevey, benoit-libert, khoa-nguyen, thomas-peters, moti-yung]
---

Devevey, Libert, Nguyen, Peters and Yung achieve non-interactive, adaptively
secure, CCA2 threshold decryption in the standard model without pairings, from
[[dcr]] and from [[lwe]].

## Why it matters here

Before this, the combination of all three requirements at once (CCA2, adaptive
corruptions, non-interactive, standard model, no random oracle) was only known
from pairings. It is the definitional high-water mark that later lattice work
measures against.

## The open problem it leaves

The LWE instantiation needs a superpolynomial approximation factor. The authors
state the gap explicitly:

> It remains an open problem to prove adaptive security under a more common LWE
> assumption with polynomial approximation factor.

That is [[devevey-adaptive-poly-modulus]], resolved by
[[sjtu-adaptive-threshold-decryption]].

## Desiderata

Satisfies [[D3]], [[D4]] and [[D6]], the last of which is what makes it notable.
Not post-quantum in the DCR instantiation, and the LWE instantiation's parameters
are the problem the follow-up work fixes. Fails [[D2]] and [[D14]].
