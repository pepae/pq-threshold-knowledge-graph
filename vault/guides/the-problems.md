---
id: the-problems
type: guide
title: "The problems: what breaks, and what is still open"
aliases: ["The problems", "Open problems overview", "What is broken"]
angle: problems
order: 3
audience: researchers looking for what to work on
reading_time: 15 minutes
covers: [index-collision-censorship, identity-tag-replication, harvesting-attack, linear-route-opening-impossibility, flooding-underestimate-ring-setting, sublinear-pq-batch-decryption, silent-pq-threshold-t-of-n, adaptive-corruptions-batched-lattice, low-norm-small-share-large-t, remove-query-bound-poly-modulus, post-inclusion-ordering, devevey-adaptive-poly-modulus, beatmev-pq-implementation, blt25-implementation]
---

This page is the pessimist's tour. It starts from concrete failures, moves through
two impossibility results, and ends at the seven open problems with what would count
as solving each.

If you are looking for something to work on, the short answer is
[[sublinear-pq-batch-decryption]], and the rest of this page explains why.

## Layer 1: the attacks that exist

**[[index-collision-censorship]]** is the most instructive failure here, because
nothing is decrypted and the system still loses.

Index-dependent batch schemes need each ciphertext in a decryptable group to carry a
distinct index, and encryptors do not coordinate. The standard fix is sub-batches:
group the distinct ones and publish a key per group. So an attacker submits
Omega(log l) ciphertexts all carrying the *same* index. The system now must either
produce Omega(log l) sub-batches and keys, inflating everything, or exclude most
transactions sharing that index. That second option is censorship of honest users
who merely collided.

It affects [[beat-mev]] and index-dependent schemes built on it, including
[[weighted-bte]], whose tunable collision handling moves the operating point without
removing the vector. Note the naming: Wagner's survey calls this a "succinctness
vulnerability", while the source paper frames it as censorship arising from the
succinctness trade-off. It is not a break of confidentiality. This knowledge base
uses the paper's framing and records the disagreement.

Why it matters beyond itself: an encrypted mempool exists to stop transaction-level
manipulation. An attack that cheaply forces honest transactions out of blocks defeats
that goal without decrypting anything, and **no desideratum in D1-D15 captures it**.

**[[identity-tag-replication]]** is the sibling failure for schemes that use tags
instead of indices. An adversary copies an honest user's identity tag and submits a
dummy ciphertext under the same tag. Moving from indices to tags trades one
adversarial handle for another; index-independence is not a free fix.

**[[harvesting-attack]]** is the fork attack. Collect fewer than t shares under one
block anchor, fewer than t under a competing fork's anchor, and combine them: the
total exceeds t and you decrypt something no quorum authorised on either fork. The
defence is context binding, defined by [[bbnrs-context-dependent]], which also gives
a generic transform adding context to any CCA-secure threshold scheme. This is the
attack that makes [[D9]] a requirement, and it is a *consensus* problem that pure
cryptography would not have produced.

## Layer 2: the two impossibility results

These are more valuable than the attacks, because they tell you where not to look.

**[[linear-route-opening-impossibility]]**: on the obvious lattice route, a
constant-size batch opening cannot exist. To recover position j of a batch a
decapsulator needs the value `s^T u_j`, and for a batch B those are |B| independent
values. One ring element cannot encode |B| independent values. So opening on that
route is O(|B|), one element per ciphertext.

This explains in one line why the thing pairings give away almost free (a single
group element opens a whole block in [[beat-mev]], 48 to 80 bytes per party in
[[cgpp-bte]] and [[choudhuri-garg-policharla-wang-onetime]]) does not transfer to
the natural lattice analogue. Succinct lattice batch opening needs a different
mechanism entirely, which is what [[blt-batch-ibe]] supplies with a trapdoor sampler
and why its parameters are what they are.

Caveat on status: this is recorded from an unpublished project's audit log, not a
reviewed theorem. The argument is elementary and reproduced so it can be checked.

**[[flooding-underestimate-ring-setting]]** is a security bug, and it is here
because the mistake is easy to repeat. A draft used the plain-LWE smudging bound for
flooding noise in a *ring* setting. In the ring case the Renyi divergence multiplies
over all N ciphertext coordinates, so the bound is short by a factor of sqrt(N). At
the value used, the flooding divergence came out at exp(N/2) = 2^185, meaning the
flooding hid nothing whatsoever.

Three general lessons. A flooding bound derived for [[lwe]] does not transfer to
[[mlwe]] unchanged. The bug was **invisible to correctness tests**: decryption
succeeded, the noise budget closed, the failure rate was unchanged, and only
building the simulator exposed it. And the same audit found a related error, treating
the Renyi divergence in the flooding hop as 1+o(1) when it is a multiplicative
constant of about e^(1/2).

## Layer 3: the measured wall

Two implementations turn "expensive" into numbers, and the numbers are the real
state of the field.

**[[beatmev-pq-implementation]]** instantiates [[beat-mev]] on lattices at 128-bit
security. At batch 512: 1250 ms to encrypt one ciphertext, 1.9 MB per ciphertext,
50.2 s partial decryption per party, 326.5 s to combine, 259 MB public key. Against
the classical scheme that is roughly 790x, 2700x, 170x, 40 to 90x and 10^5x.

Read which of those are fatal rather than merely bad. 1.9 MB per transaction goes on
chain, paid by users ([[D11]]). 327 s to combine is on the critical path
([[D15]]) and is longer than the block it opens. This is not a slow mempool, it is
not a mempool.

**[[blt25-implementation]]** tests the other end. [[blt-batch-ibe]]'s succinctness
claim is real: at lambda 128 and batch 4096 the opener is about five orders of
magnitude smaller than the batch. But secure parameters need matrices with about
10^9 columns, so the prototype runs only at toy sizes with no security, and its own
documentation says so.

Put the two together and the post-quantum batched problem is bounded from both
sides. The easy construction is impossible, the succinct construction does not run,
and the runnable construction is not a mempool.

## Layer 4: the seven open problems

Ordered by how much they matter for actually deploying an encrypted mempool.

**1. [[sublinear-pq-batch-decryption]]** (partially resolved). Post-quantum batch
decryption at parameters that run. Asymptotic succinctness exists and nobody has run
it. Since the entire point of batching is a concrete communication saving, an
asymptotic result at unrunnable parameters does not settle it. *What would solve
it*: bring the trapdoor-sampler route down by orders of magnitude, probably needing a
fundamentally cheaper sampler than [[klein-sampler]], or find a succinct opener
outside both known routes.

**2. [[silent-pq-threshold-t-of-n]]** (partially resolved). Silent setup,
post-quantum, batched, efficient. The existence question is arguably answered:
[[champion-wu-optimal-dnf]] gets parameters independent of policy size, and
threshold encryption with silent setup is the threshold-policy special case. *What is
missing*: an implementation with concrete parameters, and the composition with
batching. Classically that composition took [[beast-mev]] making a silent scheme
additively homomorphic; the lattice analogue is unexplored.

**3. [[low-norm-small-share-large-t]]** (open). Secret sharing that is both low-norm
and small-share at large thresholds. This is the one with a *measured* deployment
consequence: it caps committee size, and it does so identically for DKG-based and
silent schemes because it comes from the sharing rather than the setup. A reader who
concludes "use silent setup to scale the committee" is wrong for this reason. *What
would solve it*: such a sharing scheme, or, more promisingly, a construction whose
noise budget does not depend on recovery coefficient norm at all.

**4. [[remove-query-bound-poly-modulus]]** (open). Every polynomial-modulus result
here buys the small modulus with an a priori bound Q on decryption queries. In most
threshold settings that is a formality. Here it is not: the decryption oracle is a
public permissionless service, so Q is a function of chain lifetime and adversarial
spam, not a design-time choice. *What would solve it*: a flooding analysis
independent of query count, or per-batch randomness refresh so each batch carries its
own small Q, which connects naturally to [[D9]].

**5. [[adaptive-corruptions-batched-lattice]]** (open). The two halves exist
separately: [[sjtu-adaptive-threshold-decryption]] is adaptive but not batched,
[[blt-batch-ibe]] is batched but not adaptive. They pull the same lever in opposite
directions, as described in [[the-goals]]. Wagner grades [[D6]] as relaxable, so
this is a strengthening rather than a blocker.

**6. [[post-inclusion-ordering]]** (open, and not a cryptography problem). Threshold
encryption hides transaction *contents* until inclusion. It says nothing about the
*order* of execution afterwards. A proposer who learns a whole block at decryption
time and still controls ordering retains a substantial part of the MEV.
[[mevade]] is explicit that hiding contents is only half the design. This is outside
D1-D15 entirely, which is itself the finding: fifteen desiderata for the
cryptography, none for the composition.

**7. [[devevey-adaptive-poly-modulus]]** (resolved, kept for the record). Devevey et
al. asked for adaptive security under LWE with polynomial approximation factor.
[[sjtu-adaptive-threshold-decryption]] resolved it with three schemes. Two caveats
survive: TD2's CCA proof needs the [[rom]] because its mask comes from a random
oracle, and the original problem was posed in the standard model; and robustness for
TD2 is explicitly involved, since proving well-formedness of a masked share in zero
knowledge is hard.

## The meta-problem

D1-D15 came out of surveying threshold encryption papers. Two things on this page
sit outside it: censorship resistance, which [[index-collision-censorship]] attacks
directly, and ordering, which [[post-inclusion-ordering]] is about. Both are
properties of the *system*, not of the encryption scheme, and both can be lost while
every one of the fifteen is satisfied.

If you want the most useful unglamorous contribution available: a security definition
for an encrypted mempool end to end, composing a threshold scheme's confidentiality
with an ordering rule and a censorship-resistance requirement.

Next: [[the-history]] for how the field arrived here, or [[choosing-a-scheme]] for
what to do about it today.
