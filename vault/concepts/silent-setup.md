---
id: silent-setup
type: technique
title: Silent setup
aliases: ["dealerless setup"]
family: setup
---

Each party posts an independently generated public key; the joint encryption key
is a deterministic public function of the posted keys. No DKG. The property is
[[D2]]; this note is the mechanism.

Classical instantiations: special-purpose [[witness-encryption]]
([[gkpw-silent-setup]]), generic from key-anonymous PKE
([[hall-andersen-simkin-wagner-silent]]), pairings in the standard model
([[waters-wu-silent]]). Post-quantum: the
[[distributed-broadcast-encryption]] and [[monotone-policy-encryption]] line.
