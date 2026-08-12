---
id: the-goals
type: guide
title: "The goals: what a good scheme would look like"
aliases: ["The goals", "Requirements", "D1-D15 explained"]
angle: goals
order: 2
audience: readers who want the evaluation framework
reading_time: 15 minutes
covers: [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, wagner-desiderata, brzuska-klooss-woo, hybrid-encryption-associated-data]
---

There are fifteen requirements in this knowledge base, D1 to D15, taken from
[[wagner-desiderata]]. Listed flat they read as a shopping list. They are not.
They fall into five groups, several of them pull against each other, and knowing
which tensions are real is most of the expertise.

This page walks the groups in plain language, then names the tensions.

> **On the numbering.** Wagner's note has no numbered list; its criteria are an
> unnumbered nested bullet list. The D1-D15 identifiers are a documented flattening,
> and one of Wagner's top-level bullets (*hardness assumptions and idealizations*)
> gets no number at all. See `vault/desiderata/_wagner-mapping.md`. Do not treat the
> numbering as canonical outside this repository.

## Group 1: who do you have to trust? (D1, D2)

[[D1]] **No trusted setup.** Nobody should hold a secret that would break the
system if kept. Some schemes need a ceremony producing public parameters, where a
value used during the ceremony must be destroyed afterwards. If it survives, it is a
permanent, untraceable backdoor. The sharpest version of this problem is a setup
where the ceremony's secret *is* the decryption key.

[[D2]] **Silent setup.** Can the committee form without talking to each other? The
classical approach is a DKG, an interactive protocol among all n parties. Silent
setup means each party posts a key independently and the joint key is a public
function of the posted keys.

Note that Wagner phrases D2 *conditionally*: avoid a DKG **if the number of parties
is large**. This is the one requirement on the list that is a deployment question
rather than an absolute good. For a fixed committee of thirteen, a one-time DKG is
simpler and entirely adequate. Silent setup earns its cost when the committee is a
small rotating subset of a large validator set, because then you would otherwise
re-run the DKG on every rotation.

D1 and D2 are independent and get confused constantly. D1 is about *trapdoors*, D2
is about *interaction*. A scheme can be transparent but need a DKG, or silent but
still need a ceremony. [[gkpw-silent-setup]] is exactly the second case.

## Group 2: is it actually secure? (D4, D5, D6, D7)

[[D4]] **CCA2, with associated data.** CPA security means safe against an attacker
who can encrypt. CCA2 means safe against one who can also get things decrypted. For
a mempool that is not a theoretical nicety: the committee is a *public decryption
service* that will decrypt whatever appears in a block. Attacker-chosen ciphertexts
and a decryption oracle are the actual operating conditions.

Wagner attaches a specific trap. Real systems get short ciphertexts by encrypting a
symmetric key and the payload separately (hybrid encryption). If the threshold KEM
does not bind **associated data**, that composition loses CCA2 even when the KEM is
CCA2 on its own. See [[hybrid-encryption-associated-data]].
[[brzuska-klooss-woo]] is the reference for what it takes to get from CPA to CCA
properly, and it also proves a counterintuitive separation: security at the maximum
number of corruptions does *not* imply security at fewer.

[[D5]] **Adaptive with respect to ciphertext.** Can the attacker pick its target
after watching the system, or must it commit up front? Selective security models an
attacker who chooses a victim before seeing the chain. Real front-runners do the
opposite: they watch, then choose.

[[D6]] **Adaptive with respect to corruptions.** Does the attacker fix which
committee members it controls in advance, or corrupt them as it learns? Wagner
grades this one "both seems fine, adaptive preferred", which makes it the most
relaxable item on the list. It is a genuine modelling gap and not a deployment
blocker.

[[D7]] **Rogue ciphertext security.** Batching-specific. Because one short value
opens a whole batch, everything in a batch shares fate. An attacker who can place a
chosen ciphertext next to a victim's gets leverage unless the scheme prevents it.
The standard defence is a well-formedness proof attached to each ciphertext, checked
before admission to the batch.

## Group 3: will it survive a quantum computer? (D8)

[[D8]] **Post-quantum.** Every pairing-based scheme here fails outright.

Read the threat carefully, because the obvious version is the weaker one. A
transaction is secret for about one block, so an adversary who records ciphertexts
now to decrypt later gains very little. The real exposure is the **committee's
long-lived key material**, which does not rotate per block. That is what makes D8
urgent rather than speculative.

D8 is also where Wagner's unnumbered bullet, *hardness assumptions and
idealizations (want to use established ones)*, has to live. Two schemes both marked
post-quantum can rest on very different footings, and two schemes both marked
classical can too. In this knowledge base that is represented structurally instead
of by a number: follow the `assumes` edges. [[batched-abe-pairings]] on standard
[[dbdh]], [[beat-mev]] on [[ddh]], [[btx]] on a [[q-type-pairing]] assumption, and
[[gkpw-silent-setup]] proven only in the [[ggm]] are four different levels of
confidence that the performance tables do not show.

## Group 4: how big and how fast? (D10, D11, D12, D13, D15)

These five are the engineering budget, and it matters *who pays* each one.

[[D11]] **Ciphertext size.** Paid on chain by every user, forever. Competes directly
with the throughput the chain is trying to protect. This is where the post-quantum
tax hurts most: 722 bytes classically versus 1.9 MB measured post-quantum.

[[D10]] **Public key size.** Paid by every encryptor, who must fetch the encryption
key. Under silent setup the meaningful measure is the *individual* posted key, since
the PKI carries all of them.

[[D12]] **Short decryption keys.** The value broadcast to open a block, which every
node downloads. This is the quantity that decides whether decryption scales with
block size, and it is why threshold IBE is such a natural fit: a key for a set of
identities *is* a short block opener.

[[D13]] **Decryption share size.** The committee's per-block bandwidth. Paid by
infrastructure rather than users. The pairing-based batched schemes are remarkable
here: 48 to 80 bytes per party for an entire block, independent of block size.

[[D15]] **Fast decryption.** Wagner's parenthetical is the whole content: *this is
on the critical path*. A block cannot execute until it is decrypted, so this
competes with the slot time, not with a user's patience. Distinguish carefully what
is actually on the path: verifying ciphertext well-formedness can usually be done
when a ciphertext first arrives, not at decryption time.

## Group 5: the operational requirements (D3, D9, D14)

These three are what separate a threshold encryption scheme from an
*encrypted-mempool* threshold encryption scheme. They are the ones a
general-purpose cryptography paper is least likely to address.

[[D3]] **Non-interactive decryption.** Each party sends exactly one message. Every
extra round is a consensus round, and a party that must speak twice can stall the
chain by speaking once.

[[D9]] **Context-dependent shares.** Shares must be bound to the block they were
produced for, so shares from competing forks cannot be combined. This is a
*consensus* requirement that pure cryptography would never generate, and it is
where blockchain reality intrudes: fewer than t shares on one fork plus fewer than t
on another must still not decrypt, even when the total exceeds t.

[[D14]] **Epoch-free batching.** Two things at once. Batch decryption: one short key
opens a whole block with communication independent of the block size, without
compromising transactions that were *not* included. And no epochs: no per-batch
setup, and no slot number the user must commit to when encrypting. The second half
is what makes the primitive deployable, because users do not know which block will
include them.

D14 is the single most discriminating requirement in the list. Filtering on it plus
D8 is the fastest way to see the frontier:

```bash
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
```

## The tensions that are real

A list of fifteen goods implies you could get all fifteen. You cannot, and these are
the specific reasons.

**Succinctness versus censorship.** Making the block opener short pushes schemes
toward index-dependent designs, where each ciphertext carries an index and indices
in a group must be distinct. Since encryptors do not coordinate, collisions happen,
and the fix (sub-batches) creates [[index-collision-censorship]]: an attacker floods
one index and forces either many more keys or the exclusion of honest colliding
transactions. Better [[D13]] bought a censorship vector, and *no desideratum on the
list captures that*. Censorship resistance is adjacent to [[D7]] and not the same
thing. This is the clearest evidence the fifteen are not complete.

**Batching versus adaptive corruption.** Adaptive-corruption proofs in the lattice
setting work by bounding how much the shares still hide given what the attacker
knows. Batching deliberately publishes one short value that opens many ciphertexts,
which is a large structured hint about the key. [[D14]] and [[D6]] pull directly
against each other, which is why [[adaptive-corruptions-batched-lattice]] is open.

**Small shares versus lattice noise.** Combining shares multiplies their noise by
the recovery coefficients, so a lattice scheme wants those small. Sharing schemes
with small coefficients hand each party exponentially much material. So [[D13]]
fights committee size, and [[low-norm-small-share-large-t]] is that fight.

**Silent setup versus everything else.** Post-quantum silent setup currently costs
either a random oracle, or selective security, or a stronger assumption. [[D2]]
against [[D5]] and D8's implicit assumption-quality requirement.

**Post-quantum versus all five size and speed goals simultaneously.** Not a subtle
trade. Three to four orders of magnitude on every axis at once. See
[[the-problems]] for the numbers.

## Reading the ratings in this knowledge base

Each scheme note carries `satisfies`, `partially_satisfies` and `fails` edges, and
the prose says *why* for each. A partial rating always has a reason: for
[[beast-mev]], partial [[D15]] records that the concretely efficient variant
evaluated is the CPA one, not the CCA one. Do not read the edges without the note.

```bash
python3 skill/scripts/query.py desiderata          # coverage tally across all 15
python3 skill/scripts/query.py node D14            # who satisfies, partially, fails
```

Next: [[the-problems]] for what is broken, or [[choosing-a-scheme]] if you need to
pick something today.
