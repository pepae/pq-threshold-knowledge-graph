---
id: identity-tag-replication
type: attack
title: Identity-tag replication against tag-based batch schemes
eprint: "2025/1254"
year: 2025
status: preprint
source_depth: full-text
builds_on: [blt-batch-ibe]
---

The counterpart to [[index-collision-censorship]] for schemes that identify a
ciphertext by an identity *tag* rather than an index, also recorded by
[[blt-batch-ibe]].

## The attack

An adversary observes an honest user's ciphertext in the mempool under identity tag
r, then creates a *dummy* ciphertext encrypted under the same tag r. Because the
pre-decryption key is issued per identity, a dummy admitted to a block under the
victim's tag interferes with the honest ciphertext's handling.

## Status of this note

The mechanism is recorded from the source paper's introduction; the full
consequence and the precise set of affected constructions have not been extracted.
Marked `source_depth: full-text` because the paper is held locally, but the note is
deliberately narrow. The reason to keep it is that it shows index-independence is not
a free fix: moving from indices to tags trades one adversarial handle for another.
