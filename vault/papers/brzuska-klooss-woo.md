---
id: brzuska-klooss-woo
type: paper
title: "Threshold Public-Key Encryption: Definitions, Relations, and CPA-to-CCA Transforms"
aliases: ["BKW", "Brzuska-Klooss-Woo"]
eprint: "2025/1665"
year: 2025
status: preprint
peer_reviewed: false
source_depth: full-text
uses: [hybrid-encryption-associated-data]
authors: [chris-brzuska, michael-klooss, ivy-woo]
---

The first systematic study of threshold PKE confidentiality: which definitions imply
which, across indistinguishability versus simulatability, passive versus active
attacks, and static versus adaptive corruptions.

## The separation that matters most

Security under *maximal* corruptions does not imply security under *fewer*
corruptions, when the adversary has access to partial decryptions of challenge
ciphertexts. This is counterintuitive and directly relevant: a scheme proven secure
at t-1 corruptions is not automatically secure at t-2, so a deployment that
conservatively assumes fewer corrupted parties is not automatically on safer ground.

## Two CPA-to-CCA transforms

* A Naor-Yung style transform, requiring semi-malicious CPA security of the
  underlying scheme.
* A random-oracle transform built on a new primitive, non-interactive proof of
  randomness (NIPoR), constructed from extractable zero-knowledge proofs and
  commitments.

## Why it is a paper node and not a scheme node

Its contribution is definitional. It is the reference to consult when a scheme in
this KB claims CPA and you need to know what it would take to reach [[D4]], and it
is the natural companion to Wagner's warning that hybrid encryption needs a
threshold KEM with associated data.
