---
id: the-history
type: guide
title: "The history: how the field got here, 2010 to 2026"
aliases: ["The history", "Timeline", "How we got here"]
angle: history
order: 4
audience: readers who want to know why the schemes look like this
reading_time: 15 minutes
covers: [bendlin-damgard, bgg-universal-thresholdizer, boudgoust-scholl, micciancio-suhl, devevey-libert-nguyen-peters-yung, gkpw-silent-setup, cgpp-bte, choudhuri-garg-policharla-wang-onetime, beat-mev, beast-mev, blt-batch-ibe, pilvi, sjtu-adaptive-threshold-decryption, champion-wu-dbe, champion-wu-monotone-dnf, champion-wu-optimal-dnf, hall-andersen-simkin-wagner-silent, bbnrs-context-dependent, tacet, choudhuri-garg-piet-policharla-2024]
---

Read chronologically, each result arrives as an answer to the previous one's
limitation, and the schemes stop looking arbitrary. This page tells that story.

Two threads run in parallel and only meet at the end: a **lattice thread**, which
has always been post-quantum and always been expensive, and a **pairing thread**,
which has always been efficient and is doomed by quantum computers. The interesting
recent history is each thread acquiring the other's virtues.

## Prehistory: the lattice thread starts (2010)

[[bendlin-damgard]], TCC 2010, is the root. Take Regev's lattice encryption, split
the secret key across parties, have each compute its partial decryption locally, and
add enough extra noise that the partial decryption reveals nothing beyond the
plaintext. Reconstruction is linear, which is why decryption is non-interactive: no
party needs to talk to another.

Two things about this paper still matter. It established [[noise-flooding]] as *the*
technique for lattice threshold decryption, and it is still what practitioners
actually reach for: the post-quantum BEAT-MEV sketch in [[blt-batch-ibe]]
thresholdizes Regev encryption by citing exactly this work, sixteen years later.

Its cost is the thread's original sin. Statistical hiding needs the flooding noise
*superpolynomially* larger than the decryption noise, which forces a large modulus,
which makes everything big. Removing that cost occupies the next fifteen years.

## 2018: the generic answer, and why it is not enough

[[bgg-universal-thresholdizer]] builds threshold FHE from [[lwe]] and abstracts it
into a compiler that adds threshold functionality to almost anything.

So "post-quantum threshold decryption is possible" has been true since 2018. It is
worth being clear about why nobody deployed it: it needs a setup, and it inherits
threshold FHE's cost plus flooding at a superpolynomial modulus. It is the generic
result that every concrete scheme afterwards exists to beat, and the right reference
point for asking whether a new scheme's complexity is buying anything.

## 2021: the definitional high-water mark

[[devevey-libert-nguyen-peters-yung]], PKC 2021, gets non-interactive, adaptively
secure, CCA2 threshold decryption in the standard model without pairings, from
[[dcr]] and from [[lwe]]. Before this, all of those properties at once were known
only from pairings.

Its LWE instantiation needs a superpolynomial approximation factor, and the authors
state the gap explicitly as an open problem. Remember that sentence; it gets resolved
in 2026.

## 2023: the modulus falls

Two papers, one year, same target, different tools. This is the cleanest example in
the field of a technique choice determining what security notion you can reach.

[[boudgoust-scholl]] replaces statistical distance with
[[renyi-divergence-analysis]]. Renyi divergence tolerates much smaller flooding
noise, so the modulus becomes polynomial. But Renyi arguments give
probability-preservation bounds, which support search and decision games and **not**
simulation. So the result is game-based security.

[[micciancio-suhl]] closes that gap by a different route: when both the ciphertext
noise and the flooding noise are Gaussian, simulation goes through even with very
small flooding noise. Simulation security at polynomial modulus. Their claim that
parameters are "roughly comparable to FrodoKEM" is the most useful number in this
part of the literature, because it puts lattice threshold decryption in the same
ballpark as a conservative non-threshold KEM.

The lattice thread now has a reasonable modulus. It still has no batching, no silent
setup, and no answer for large committees.

## 2024, part one: the pairing thread solves batching

[[choudhuri-garg-piet-policharla-2024]], USENIX Security 2024, does two things: it
gives attacks on mempool privacy schemes, which is where [[D7]] comes from, and it
introduces **batched threshold encryption** ([[cgpp-bte]]). A committee decrypts a
chosen batch of B ciphertexts using O(n) communication instead of the naive O(nB),
with ciphertexts outside the batch staying private.

The numbers were the shock: **80 bytes per party to open an entire block**,
independent of block size, and about 2.8 s per member for roughly 500 transactions.
Suddenly an encrypted mempool looked like an engineering project.

The catch is epochs. The scheme needs an expensive interactive setup, in MPC, for
*every batch*, with one decryption key per epoch. So users must encrypt to a
specific future window, and they do not know which block will include them.

## 2024, part two: the pairing thread solves silent setup

[[gkpw-silent-setup]], CRYPTO 2024, independently attacks the other problem. The
committee's joint public key is a deterministic function of individually posted keys.
No DKG. The mechanism is a purpose-built [[witness-encryption]] scheme for the
statement "at least t parties signed this message": encrypting to a committee means
encrypting to that statement, and a quorum's signatures are the witness.

Under 7 ms to encrypt, under 1 ms per partial decryption, under 200 ms to aggregate
for 1024 parties. It still needs a trusted setup on top ([[D1]] and [[D2]] are
independent), individual public keys are linear in committee size, and the proof is
in the [[ggm]].

So by end of 2024, over pairings, batching and silent setup both exist, separately.

## 2024, part three: chipping at the epoch

[[choudhuri-garg-policharla-wang-onetime]] removes the *per-epoch* setup, keeping one
one-time DKG, via a shifted BLS trick: the committee signs a commitment shifted by a
public random element. 48 bytes per party, the smallest in this knowledge base.

It is still epoch-based. Worth keeping distinct from what comes next, because "no
epoch setup" and "no epochs" are different claims and get conflated constantly. The
proof also needs a new assumption ([[shifted-bls-assumption]]), reduced to standard
ones only in the [[agm]].

## 2025, part one: epochs die

[[beat-mev]], USENIX Security 2025, gets epoch-free batching, and the mechanism is
elegant enough to state. Use a [[kh-pprf]]: a pseudorandom function that can be
punctured at a point and whose keys add. Each encryptor masks its message with the
PRF at a unique index under an ephemeral key, and ships the masked message, an
ElGamal encryption of the key, and the key punctured at its own index. ElGamal's
homomorphism lets the committee combine the encrypted keys into one pre-decryption
key, a single group element, and the puncturing is what makes it open exactly the
included ciphertexts.

Under 2 ms to encrypt, under 440 ms for 512 transactions, and it rests on plain
[[ddh]] rather than a q-type assumption.

The residual problem is beautiful in a bad way. Decryption only works if indices are
distinct, and encryptors do not coordinate. The fix is sub-batches, and the fix
creates [[index-collision-censorship]]. Solving one desideratum manufactured an
attack outside the list.

## 2025, part two: the threads converge over pairings

[[beast-mev]] gets batching *and* silent setup at once, by making
[[gkpw-silent-setup]] additively homomorphic so batch material aggregates the way
BEAT-MEV's PRF keys do. Eight authors, drawn from both the Darmstadt BEAT-MEV team
and the Berkeley GKPW and CGPP teams, which tells you exactly what happened: the two
lines merged.

Silent, batched, epoch-free, CCA under static corruptions. This is the strongest
classical answer in this knowledge base, and it is the target a post-quantum
construction has to match.

Also in 2025, two papers fill in what an encrypted mempool needs beyond raw
performance. [[bbnrs-context-dependent]] defines context-dependent decryption
([[D9]]), the fork-safety property that pure cryptography would never have generated.
And [[brzuska-klooss-woo]] does the definitional work on what CCA2 even means for
threshold PKE, proving among other things that security at maximal corruptions does
not imply security at fewer.

## 2025, part three: the lattice thread reaches for batching

[[blt-batch-ibe]] is the most important post-quantum entry. The insight is to reach
for [[threshold-ibe]]: a short pre-decryption key for a *set of identities* opens
exactly the ciphertexts under those identities, and if the identities are a block's
transactions then that key *is* the block opener. No epoch, no slot number.

The main construction composes a lattice IBE with a shifted multi-preimage trapdoor
sampler, and the opener is polylog in batch length, about five orders of magnitude
smaller than the batch. On paper the lattice thread has just acquired succinct
batching.

Two costs. Thresholdizing needs a *two-round* protocol for secret-shared
[[gaussian-preimage-sampling]], so [[D3]] is only partially satisfied. And at secure
parameters it does not run: see [[blt25-implementation]].

The paper also contributes the analysis of [[index-collision-censorship]], and an
appendix estimating a lattice BEAT-MEV, which is the theoretical companion to the
measurements in [[beatmev-pq-implementation]].

Alongside it, [[pilvi]] attacks lattice share size directly, Shamir-sharing the LWE
secret at carefully chosen evaluation points and abstracting the recurring proof step
as the [[threshold-lwe]] assumption. 1 to 4 KB shares: enormous next to 48 bytes,
and a large improvement on prior lattice art.

And [[hall-andersen-simkin-wagner-silent]] takes the non-batched route to large
committees, generically from any [[key-anonymous-pke]], with soft thresholds and a
new one-shot adaptive corruption model between static and fully adaptive.

## 2026: post-quantum silent setup arrives

The lattice thread finally gets [[D2]], and from falsifiable assumptions.

[[champion-wu-dbe]] (TCC 2024) opened the route with distributed broadcast encryption
from [[l-succinct-lwe]], replacing general witness encryption, which is not
falsifiable, with a concrete lattice assumption. Then
[[champion-wu-monotone-dnf]] generalises to monotone-policy encryption for DNFs from
[[decomposed-lwe]] with a transparent setup, and
[[champion-wu-optimal-dnf]] makes the parameters independent of policy size, adds a
plain-model variant, and gets the first lattice adaptive scheme with unboundedly many
users. [[rishab-dme]] arrives concurrently by a similar route.

Two independent groups reaching here at once is the signal. Post-quantum silent setup
stopped being speculative.

Separately, [[sjtu-adaptive-threshold-decryption]] resolves the 2021 open problem:
three adaptively secure threshold decryption schemes from LWE at polynomial modulus,
via a refined flooding lemma conditioned on linear matrix hints, plus ZeroShare
masking. Its TD2 supports polynomially many users with Shamir sharing, which is what
lifts the committee-size ceiling.

## Where the story stops

Every individual property has now been achieved post-quantum. None of them have been
achieved *together*, and none of the post-quantum silent-setup papers has been
implemented. The only artifact attempting the composition is [[tacet]], an
unpublished and unreviewed draft.

The pattern across sixteen years is worth naming. Each result solved one desideratum
and revealed the next constraint: flooding gave a huge modulus, Renyi gave a small
modulus but no simulation, batching gave epochs, epoch-free gave index collisions,
succinctness gave censorship, silent setup gave selective security. The remaining
open problems in [[the-problems]] are the current edge of that same process.

Next: [[choosing-a-scheme]] if you have to build something, or [[the-goals]] for the
framework these results are all being measured against.
