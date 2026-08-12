---
id: key-anonymous-pke
type: technique
title: Key-anonymous PKE
aliases: ["key anonymity"]
family: primitive
source_depth: full-text
---

A public-key encryption scheme whose ciphertexts hide which public key they were
encrypted under. [[hall-andersen-simkin-wagner-silent]] builds silent threshold
encryption generically from any such scheme, which is why that construction is not
tied to pairings or lattices and is plausibly post-quantum: instantiate the
underlying PKE with a post-quantum one and the threshold scheme inherits it.

Key anonymity is what makes the soft-threshold trick work. If a ciphertext revealed
its intended recipient, an adversary could tell which subset of the committee a
given component was aimed at, and the construction's privacy would collapse.
