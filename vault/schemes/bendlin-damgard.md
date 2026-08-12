---
id: bendlin-damgard
type: scheme
title: Bendlin-Damgard threshold Regev
aliases: ["Bendlin-Damgard", "BD10"]
eprint: "2009/391"
venue: TCC 2010
year: 2010
status: published
peer_reviewed: true
source_depth: full-text
pq: true
assumptions: [gapsvp, lwe]
techniques: [noise-flooding, shamir-secret-sharing]
satisfies: [D1, D3, D8]
partially_satisfies: [D6]
fails: [D2, D4, D14]
authors: [rikke-bendlin, ivan-damgard]
---

The root of the linear lattice route to threshold decryption. A variant of Regev's
cryptosystem with a new choice of parameters, proven semantically secure from the
worst-case problem [[gapsvp]] via Peikert's classical reduction, then turned into
a threshold cryptosystem with a very efficient non-interactive decryption
protocol.

## Key mechanism

Secret-share the Regev secret key, have each party compute its partial decryption
locally, and add [[noise-flooding]] noise so the partial decryption reveals
nothing beyond the plaintext. Reconstruction is linear, which is the whole reason
the scheme is non-interactive: no party needs to talk to another.

Security is proven against passive adversaries corrupting all but one party, and
against active adversaries corrupting fewer than one third. The paper also
describes a distributed key generation protocol, and, separately, zero-knowledge
proofs of plaintext knowledge for Regev ciphertexts whose size is a constant
factor times a ciphertext.

## Desiderata

Satisfies [[D1]] (no trapdoor; the setup is a DKG, not a ceremony), [[D3]]
(single-message decryption, and this is the paper that establishes it for
lattices) and [[D8]]. Partially [[D6]]: the active-adversary threshold below n/3
is a robustness statement, not adaptive corruption. Fails [[D2]] (needs a DKG),
[[D4]] (semantic security, not CCA2) and [[D14]] (not batched).

## Why it still matters

Every later lattice threshold scheme is a response to one of its costs. The
flooding noise forces a large modulus, which is what [[boudgoust-scholl]],
[[micciancio-suhl]] and [[sjtu-adaptive-threshold-decryption]] attack. And it is
still the thresholdizing step reached for in practice: the lattice BEAT-MEV
sketch in [[blt-batch-ibe]] thresholdizes Regev encryption by citing exactly this
work, and [[beatmev-pq-implementation]] implements it that way.

## Relevance to encrypted mempools

Not deployable as-is (no batching, no CCA2), but it defines the baseline cost of
post-quantum threshold decryption: linear reconstruction plus enough flooding
noise to hide a share.
