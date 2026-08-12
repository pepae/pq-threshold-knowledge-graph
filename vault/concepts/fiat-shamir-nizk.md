---
id: fiat-shamir-nizk
type: technique
title: Fiat-Shamir NIZKs
aliases: ["Fiat-Shamir"]
family: proof
---

Non-interactive proofs from interactive ones via a hash.

Two refinements matter here. *Straight-line simulation-extractability* is what
batched schemes need for rogue-ciphertext security ([[D7]]) and ciphertext
adaptivity ([[D5]]); [[beat-mev]] requires it and instantiates it in the [[agm]].
And plain Fiat-Shamir is not automatically secure against a quantum adversary,
which is what the [[katsumata-transform]] addresses.
