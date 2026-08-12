---
id: glossary
type: guide
title: Glossary
aliases: ["Jargon", "Terms"]
angle: vocabulary
order: 6
audience: anyone hitting an unfamiliar term
reading_time: skim
covers: [batched-threshold-encryption, silent-setup, noise-flooding, kh-pprf, threshold-ibe, lwe, mlwe, ggm, rom, qrom, shamir-secret-sharing, low-norm-secret-sharing, vector-commitments, gaussian-preimage-sampling, naive-threshold-baseline, key-anonymous-pke]
---

One line each, in plain language, roughly from most to least fundamental. Links go
to the full note.

## The setting

**Mempool** - the public waiting area where transactions sit after being broadcast
and before being finalised. Public visibility here is the whole problem.

**MEV** - maximal extractable value. Profit available to whoever can see and order
transactions before they execute.

**Sandwich attack** - placing one order just before a victim's and another just
after, to profit from the price move the victim causes.

**Front-running** - acting on knowledge of a pending transaction before it
executes.

**Encrypted mempool** - a design where transactions stay encrypted until their
inclusion in a block is settled.

**Committee / keypers** - the n parties who jointly hold the decryption capability.

**Proposer** - the party that builds a block. Even with encryption they usually
still choose the order, which is why [[post-inclusion-ordering]] is an open
problem.

## The primitive

**Threshold encryption** - a decryption key split across n parties so any t can
decrypt and any t-1 learn nothing.

**Decryption share / partial decryption** - the one message a committee member
publishes so that shares can be combined into a decryption.

**Combine** - the step that turns t shares into a usable decryption. Often the most
expensive step.

**DKG** (distributed key generation) - an interactive protocol by which the
committee jointly creates a shared key with no single party ever holding it.

**[[silent-setup]]** - the alternative to a DKG: each party posts its own key
independently, and the joint key is a public function of those. No interaction. See
[[D2]].

**Trusted setup / powers of tau** - a one-time ceremony producing public
parameters, where a secret used during the ceremony must be destroyed. If it
survives, it is usually a backdoor. See [[D1]].

**[[batched-threshold-encryption]]** - decrypting a whole chosen batch of
ciphertexts with communication that does not grow with the batch size. See
[[D14]].

**Epoch** - a fixed time window some schemes require, with a setup per window and
one decryption key per window. Epoch-free is better because users cannot know in
advance which block will include them.

**Pre-decryption key / block opener** - the single short value that opens an entire
batch.

**[[threshold-ibe]]** - identity-based encryption with a shared master key, where a
short key for a set of identities opens exactly the ciphertexts under those
identities. A natural fit for opening a block.

**Context binding** - tying a decryption share to the specific block or fork it was
produced for, so shares from competing forks cannot be combined. See [[D9]] and
[[harvesting-attack]].

**KEM** - key encapsulation mechanism. Encrypt a short symmetric key rather than
the message, then encrypt the message under that key. How real systems get short
ciphertexts.

**Associated data** - extra context bound into an encryption. Wagner flags that a
threshold KEM must bind it or the hybrid construction silently loses CCA2 security.
See [[D4]].

## Security vocabulary

**CPA security** - secure against an attacker who can encrypt but not decrypt. The
weak baseline.

**CCA2 security** - secure even against an attacker who can get things decrypted.
The right target for a mempool, because the committee is a public decryption
service. See [[D4]].

**Selective vs adaptive (ciphertext)** - whether the attacker must pick its target
before seeing the system, or can choose after watching. Real front-runners watch
first. See [[D5]].

**Static vs adaptive (corruption)** - whether the attacker fixes which committee
members it controls in advance, or corrupts them as it learns. See [[D6]].

**Rogue ciphertext attack** - injecting malformed or related ciphertexts into a
batch to learn about honest ones. See [[D7]].

**Robustness** - the ability to detect and exclude a committee member that submits
a bad share, rather than just failing.

**Simulation security** - a stronger, composable style of proof where shares can be
produced without the key. Matters when a scheme is used inside a bigger protocol.

**Falsifiable assumption** - one you could in principle disprove by exhibiting an
attack. Contrast with an idealised model.

**[[ggm]] / [[agm]] / [[rom]] / [[qrom]]** - idealised models used in proofs. A
proof in an idealised model rules out a class of attacks rather than all attacks.
QROM is the quantum-aware version of ROM, and a ROM proof does not automatically
carry over to it.

**q-type assumption** - an assumption whose strength is parameterised by how much
the scheme uses it. Weaker footing than a static assumption like [[ddh]].

## The mathematics

**Pairing** - elliptic-curve structure enabling very efficient protocols. Every
pairing-based scheme here is broken by a quantum computer.

**[[ddh]]** - the standard, well-studied elliptic-curve assumption. Not
post-quantum.

**Lattice** - the mathematics behind believed-post-quantum cryptography. Efficient,
but with much larger objects.

**[[lwe]] / [[mlwe]]** - learning with errors, and its module variant. The main
post-quantum assumptions. Everything lattice-based here rests on one of them.

**Noise** - lattice ciphertexts carry deliberate small error. Operations grow it,
and decryption fails if it grows too far. The "noise budget" is the recurring
engineering constraint.

**Modulus q** - the number lattice arithmetic works modulo. Bigger means bigger
everything, so "polynomial modulus" versus "superpolynomial" is a headline result,
not a detail.

**[[noise-flooding]]** - adding large extra noise to a decryption share so it hides
the key share. Classically forced a huge modulus;
[[polynomial-noise-flooding]] is the line of work that fixed that.

**Trapdoor** - secret information making a hard lattice problem easy. Powerful, and
expensive to share among a committee.

**[[gaussian-preimage-sampling]]** - the core trapdoor operation in lattice IBE.
Hard to do jointly, which is why [[blt-batch-ibe]] needs two rounds.

## Building blocks

**[[shamir-secret-sharing]]** - the standard way to split a secret, using
polynomial interpolation. Compact, but its recovery coefficients are large, which
hurts a lattice noise budget.

**[[low-norm-secret-sharing]]** - sharing with small recovery coefficients, kinder
to a noise budget, but with much more material per party. The trade-off in
[[low-norm-small-share-large-t]].

**[[vector-commitments]]** - a short commitment to a list, with openings to
individual positions. Used to publicly fix which transactions are in a batch.

**KZG commitment** - a pairing-based polynomial commitment, used by
[[cgpp-bte]].

**Witness encryption** - encrypt to a statement, so anyone with a proof of that
statement can decrypt. One route to silent setup.

**[[kh-pprf]]** - a pseudorandom function that can be punctured at points and whose
keys add up. The engine of [[beat-mev]].

**NIZK** - a non-interactive zero-knowledge proof. Used to prove a ciphertext is
well formed, which is how schemes get [[D7]].

**[[naive-threshold-baseline]]** - the folklore construction where the ciphertext
grows with the committee. The baseline that makes "size independent of n" a
meaningful claim. Frequently confused with the schemes that improve on it.
