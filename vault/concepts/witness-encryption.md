---
id: witness-encryption
type: technique
title: Witness encryption
aliases: ["WE"]
family: primitive
---

Encrypt to a statement so that anyone holding a witness can decrypt. Silent
setup is naturally expressed this way: [[gkpw-silent-setup]] builds a special
purpose witness encryption scheme for the statement "at least t parties signed
this message".

General witness encryption is not a falsifiable assumption, which is why the
lattice line ([[champion-wu-monotone-dnf]] from [[decomposed-lwe]]) is a real
advance over the prior witness-encryption-based constructions.
