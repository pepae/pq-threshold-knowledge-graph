---
id: rom
type: assumption
title: Random Oracle Model
aliases: ["ROM"]
pq: false
falsifiable: false
family: idealization
---

Hash functions modelled as truly random functions. Standard, widely accepted,
and still an idealization. [[champion-wu-monotone-dnf]] needs it; the plain-model
variants in [[champion-wu-optimal-dnf]] pay for dropping it with a larger
ciphertext or weaker security.
