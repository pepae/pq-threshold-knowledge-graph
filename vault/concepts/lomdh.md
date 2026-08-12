---
id: lomdh
type: assumption
title: Linear one-more Diffie-Hellman
aliases: ["LOMDH", "linear one-more Diffie-Hellman"]
pq: false
falsifiable: true
family: discrete log
source_depth: full-text
---

A falsifiable complexity assumption introduced by [[bbnrs-context-dependent]],
which its authors describe as essentially the same assumption used to analyse
high-threshold BLS signatures.

The "one-more" shape is what suits it to threshold analysis: it asks that an
adversary given a budget of oracle interactions cannot produce one more valid
output than that budget allows, which is the algebraic content of "fewer than t
shares must not decrypt". Its falsifiability is worth noting against the [[ggm]]
proofs elsewhere in this KB: a q-type or one-more assumption can at least be
attacked directly, where a generic group proof only rules out generic attacks.
