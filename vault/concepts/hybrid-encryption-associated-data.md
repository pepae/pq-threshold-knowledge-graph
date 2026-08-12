---
id: hybrid-encryption-associated-data
type: technique
title: Threshold KEM with associated data
aliases: ["thrKEM with AD"]
family: primitive
---

Hybrid encryption on top of a threshold KEM is how a scheme gets a short
decryption key ([[D12]]). Wagner's note flags the trap: the threshold KEM must
bind associated data, or CCA2 is not preserved by the hybrid construction even
when the KEM is CCA2 in isolation. Tracked as part of [[D4]].
