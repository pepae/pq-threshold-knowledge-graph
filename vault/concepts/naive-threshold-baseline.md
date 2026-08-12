---
id: naive-threshold-baseline
type: technique
title: Naive threshold baseline
aliases: ["folklore baseline", "naive scheme"]
family: baseline
---

The folklore construction every large-committee scheme measures itself against:
encrypt the message once per party (or per authorized set) and attach the
resulting ciphertexts, so the ciphertext grows linearly with the committee, or
worse, with the number of authorized sets.

It is worth an explicit node for two reasons. It is the baseline that makes
"ciphertext size independent of n" a meaningful claim, and it is frequently
conflated with the schemes that *start* from it.
[[hall-andersen-simkin-wagner-silent]] is not the naive scheme: it is a generic
construction from key-anonymous PKE whose ciphertext and public key sizes are
independent of n, and which introduces soft thresholds and one-shot adaptive
corruptions. Do not cite it as the folklore baseline.
