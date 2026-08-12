---
id: ddh
type: assumption
title: Decisional Diffie-Hellman
aliases: ["DDH"]
pq: false
falsifiable: true
family: "discrete log"
---

Standard, long-established, and not post-quantum. Shor's algorithm breaks it.

Its presence in a scheme is a decisive [[D8]] failure, but it is otherwise the
best-understood assumption in the list: falsifiable, decades of cryptanalysis, no
idealized model required. [[beat-mev]] rests on DDH plus a NIZK.
