---
id: btx
type: scheme
title: BTX
aliases: ["BTX", "Batch Threshold Encryption"]
eprint: "2026/754"
year: 2026
status: preprint
peer_reviewed: false
source_depth: abstract
pq: false
batched: true
epoch_free: true
silent_setup: false
assumptions: [q-type-pairing]
techniques: [batched-threshold-encryption, fiat-shamir-nizk]
satisfies: [D3, D11, D14]
partially_satisfies: [D4]
fails: [D1, D2, D8]
disputes:
  - "Wagner's survey records eprint 2026/754 and 2026/760 as identical schemes. Only 2026/754 is held locally, so this note is written from it; the claim of identity is Wagner's, not verified here."
authors: [amit-agarwal, sourav-das, babak-poorebrahim-gilkalaye, peter-rindal, victor-shoup]
---

"BTX: Simple and Efficient Batch Threshold Encryption", by Agarwal, Das,
Poorebrahim Gilkalaye, Rindal and Shoup. Batched, epoch-free, CCA-secure under
static corruptions.

## Shape of the trade

Per Wagner's survey: a q-type assumption in pairing groups, a powers-of-tau with a
hole MPC setup where tau *is* the secret key, secret keys linear in the batch size,
a generic simulation-sound NIZK for CCA security, and FFT to speed up decryption.
In exchange, very small encryption keys and ciphertexts.

The setup is the thing to weigh: when tau is the secret key, the ceremony is not
merely a parameter-generation step, it is the key generation, so [[D1]] fails in the
strongest sense.

## Desiderata

Satisfies [[D3]], [[D11]] and [[D14]]. Partially [[D4]]. Fails [[D1]], [[D2]] and
[[D8]].
