---
id: wee-matrix-commitment
type: technique
title: Wee succinct matrix commitment
aliases: ["WW25 commitment", "Wee commitment"]
pq: true
family: commitment
assumes: [l-succinct-lwe]
---

A succinct commitment to a matrix from [[l-succinct-lwe]]. This is the component
that makes a lattice ciphertext constant-size rather than growing with the
committee, and it is what [[champion-wu-dbe]] and [[tacet-silent]] use to get a
committee-independent ciphertext.
