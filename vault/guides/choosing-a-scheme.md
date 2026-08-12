---
id: choosing-a-scheme
type: guide
title: "Choosing a scheme: what to build on today"
aliases: ["Choosing a scheme", "Decision guide", "Comparison"]
angle: decisions
order: 5
audience: engineers and protocol designers making a choice
reading_time: 12 minutes
covers: [beast-mev, beat-mev, cgpp-bte, choudhuri-garg-policharla-wang-onetime, weighted-bte, btx, blt-batch-ibe, gkpw-silent-setup, waters-wu-silent, hall-andersen-simkin-wagner-silent, champion-wu-optimal-dnf, micciancio-suhl, pilvi, bbnrs-context-dependent, tacet, beatmev-pq-implementation, D2, D8, D14]
---

Opinionated, and explicit about what each choice costs. The comparison tables are
built from the same frontmatter the graph is, so they can be regenerated and
checked.

## The short answer

**If you are deploying now and can accept classical security:** build on
[[beast-mev]]. It is the only scheme with silent setup, batching and epoch-freedom at
once, CCA-secure under static corruptions. Add context binding from
[[bbnrs-context-dependent]] if your chain has forks worth worrying about, which it
does.

**If you need post-quantum security now:** you cannot have this, and you should plan
accordingly rather than pick the least-bad option. The measured cost is 1.9 MB per
ciphertext and 327 s to open a block. Design your system so the encryption scheme is
swappable, and follow [[sublinear-pq-batch-decryption]].

**If you are choosing what to research:** [[the-problems]] ranks the seven open
problems. The top one is post-quantum batch decryption at runnable parameters.

## First, answer four questions about your deployment

The right scheme depends far more on these than on any performance table.

**1. How large is the committee, and does it rotate?** If it is small and fixed, say
thirteen keypers, a one-time DKG is simpler and adequate and you do not need
[[D2]] at all. If it is a small rotating subset of a large validator set, silent
setup earns its cost because you would otherwise re-run a DKG per rotation. This is
Wagner's own conditional phrasing, and it is the most commonly over-applied
requirement in the field.

**2. Do you need to open a whole block with one value?** Almost certainly yes, and
that means [[D14]]. If a committee member must broadcast per transaction, bandwidth
is committee size times block size. This single requirement eliminates most of the
threshold encryption literature.

**3. Is your committee weighted?** On a proof-of-stake chain it naturally is.
Virtualizing (one virtual party per unit of stake) makes communication linear in
total weight, which is the obvious wrong answer. [[weighted-bte]] is the only scheme
here that addresses weighting directly.

**4. What is your quantum threat model?** Be precise, because the obvious version is
the weaker one. Transactions are secret for one block, so record-now-decrypt-later
buys an adversary very little. The exposure is the **committee's long-lived keys**. If
your committee keys rotate frequently, your post-quantum urgency is lower than it
first appears.

## The classical batched schemes

All four give you a short opener for a whole block. None is post-quantum.

| scheme | silent setup | epoch-free | share size | assumption | note |
|---|---|---|---|---|---|
| [[cgpp-bte]] | no | no | 80 B/party | [[q-sbdht]] + [[rom]] | per-batch MPC setup |
| [[choudhuri-garg-policharla-wang-onetime]] | no | no | 48 B/party | new, [[agm]] + [[rom]] | one-time DKG, still epochs |
| [[beat-mev]] | no | **yes** | 1 group element | [[ddh]] + [[agm]] | index collisions |
| [[beast-mev]] | **yes** | **yes** | not reported here | [[ggm]] | the merge of both lines |
| [[weighted-bte]] | no | yes | as BEAT-MEV | [[q-sdh]] + [[agm]] | weighted, quasilinear |
| [[btx]] | no | yes | linear in batch (sk) | [[q-type-pairing]] | tau *is* the secret key |

Reading this table by performance alone is a mistake. Rank by assumption instead and
the order changes: [[beat-mev]] on static [[ddh]] is better founded than
[[beast-mev]], whose proof is in the generic group model, and both are better founded
than [[btx]], whose setup ceremony's secret is the decryption key.

**Recommendation.** [[beast-mev]] if you want silent setup, [[beat-mev]] if you want
the cleanest assumption and can run a DKG, [[weighted-bte]] if your committee is
stake-weighted. Note that all three of the epoch-free ones inherit
[[index-collision-censorship]], so budget for it: it is a censorship vector, not a
confidentiality break, but it is cheap for an attacker to trigger.

## The non-batched classical schemes

If you genuinely do not need batching, the field is much better.

| scheme | silent | ciphertext | assumption | notable |
|---|---|---|---|---|
| [[gkpw-silent-setup]] | yes | ~8x ElGamal | [[ggm]] | multiverse, dynamic thresholds |
| [[waters-wu-silent]] | yes | 4 group elements + tag | [[q-type-pairing]], standard model | expressive policies, no idealisation |
| [[hall-andersen-simkin-wagner-silent]] | yes | payload + 7% | [[rom]], generic | soft thresholds, one-shot adaptive, plausibly PQ |

[[waters-wu-silent]] is the strongest here on paper: standard model, tiny
ciphertexts, monotone Boolean formulas rather than just thresholds. Its costs are a
trusted setup (augmented powers of tau with a hole), large keys and CRS, and
semi-honest key generation assumed for corrupted users, which is a real weakening.

[[hall-andersen-simkin-wagner-silent]] is the interesting one for large committees,
because its ciphertext overhead is a small multiplicative factor on the payload
rather than a fixed cost, and it is generic enough to instantiate post-quantum.

## The post-quantum options, honestly

| scheme | batched | silent | status | why you cannot use it |
|---|---|---|---|---|
| [[blt-batch-ibe]] | yes | no | preprint | secure parameters need ~10^9-column matrices |
| [[beat-mev]] PQ instantiation | yes | no | measured | 1.9 MB ct, 327 s combine |
| [[champion-wu-optimal-dnf]] | no | yes | preprint | not implemented |
| [[micciancio-suhl]] | no | no | published | no batching; but FrodoKEM-scale params |
| [[pilvi]] | no | no | published | no batching; 1-4 KB shares |
| [[sjtu-adaptive-threshold-decryption]] | no | no | preprint | no batching; adaptive, poly modulus |
| [[tacet]] | yes | yes (variant) | **unreviewed draft** | unpublished, self-assessed |

The honest reading: post-quantum *threshold decryption* is solved and reasonable, and
[[micciancio-suhl]] is the scheme to reach for if you do not need batching.
Post-quantum *batched* threshold decryption is not solved at any usable parameters.

**On [[tacet]]:** it is an unpublished, unreviewed working draft by this repository's
owner. It is the only artifact attempting the full composition, and it reports a
scorecard of 10 pass, 5 partial, 0 fail against D1-D15, self-assessed by its own test
suite. Treat it as evidence the combination is buildable, not that it is solved, and
do not cite it beside peer-reviewed work without saying which it is.

## What no scheme gives you

Two properties you must handle outside the encryption scheme, because none of the
fifteen desiderata covers them.

**Censorship resistance.** [[index-collision-censorship]] shows an attacker can force
honest transactions out of blocks without decrypting anything. Every epoch-free
index-dependent scheme is exposed.

**Ordering.** Encryption hides contents until inclusion. It says nothing about
execution order afterwards, so a proposer who learns the block at decryption time and
still orders it keeps a substantial part of the MEV. See
[[post-inclusion-ordering]]. Any real deployment needs an ordering rule, and that is
a consensus design decision, not a cryptographic one.

## Building it so you can swap later

Given that the post-quantum answer does not exist yet, the highest-value design
decision is to not marry the scheme you pick.

- Depend on an interface, not a construction. The relevant EIP is explicitly
  encryption-agnostic and supports arbitrary decryption key providers.
- Assume ciphertext size will change by three orders of magnitude. Anything that
  hardcodes a transaction size budget will need rewriting.
- Assume the opener may become linear in batch size rather than constant, since
  [[linear-route-opening-impossibility]] rules out the constant-size lattice version
  on the obvious route.
- Bind context from day one, per [[bbnrs-context-dependent]]. Retrofitting fork
  safety is harder than designing it in, and the generic transform means it costs
  you little now.
- Keep the committee small and fixed if you can. It sidesteps [[D2]] entirely and
  avoids the committee-size ceiling in [[low-norm-small-share-large-t]] that a
  lattice scheme will eventually impose.

## Checking these claims yourself

Every row above comes from frontmatter you can query:

```bash
python3 skill/scripts/query.py filter --type scheme --satisfies D2 --satisfies D14
python3 skill/scripts/query.py filter --type scheme --pq true --status published
python3 skill/scripts/query.py node beast-mev
python3 skill/scripts/query.py desiderata
```

If a table here disagrees with a note, the note wins, and it is a bug worth fixing.
