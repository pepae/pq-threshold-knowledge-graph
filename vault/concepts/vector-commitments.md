---
id: vector-commitments
type: technique
title: Vector commitments
aliases: ["VC"]
family: commitment
---

A short commitment to a vector, with openings to individual positions. In the
batched threshold setting the commitment publicly *fixes* the batch, which is what
makes "only the included ciphertexts get decrypted" well defined.

[[tacet]]'s audit records a useful correction here: only-included security does
not come from the commitment gating membership. It comes from the committee scoping
partial decryption to the included positions; the commitment's job is to fix the
set publicly. No puncturing is needed for that part.
