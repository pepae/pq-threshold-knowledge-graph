---
id: q-sdh
type: assumption
title: q-strong Diffie-Hellman
aliases: ["q-SDH"]
pq: false
falsifiable: true
family: pairing
source_depth: full-text
---

The q-strong Diffie-Hellman assumption (Boneh-Boyen). A q-type assumption: the
adversary is handed powers of a secret up to degree q, so the assumption's strength
is parameterised by how much the scheme uses it.

It is the assumption behind KZG polynomial commitments (where it gives evaluation
binding) and is used directly by [[weighted-bte]] in the [[agm]]. Standard and
long-studied for a q-type assumption, but not post-quantum, and strictly stronger
than a static assumption like [[ddh]].

[[cgpp-bte]] explains why q-SDH alone is *not* enough for batched threshold
encryption, and introduces [[q-sbdht]] instead.
