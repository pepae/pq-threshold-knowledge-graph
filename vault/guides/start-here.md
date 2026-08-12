---
id: start-here
type: guide
title: "Start here: encrypted mempools in plain language"
aliases: ["Start here", "Home", "Overview"]
angle: orientation
order: 1
audience: anyone, no cryptography assumed
reading_time: 10 minutes
covers: [D8, D14, beat-mev, blt-batch-ibe, beatmev-pq-implementation, wagner-desiderata, the-goals, the-problems, the-history, choosing-a-scheme, glossary]
---

This knowledge base is about one narrow engineering problem and roughly twenty
years of cryptography aimed at it. This page explains the problem in ordinary
language, tells you honestly where things stand, and points you at the right next
page. Nothing here assumes you know any cryptography.

## The problem, in one scene

You want to trade on a decentralised exchange. You sign a transaction and send it
to the network. Before it is finalised, it sits in a public waiting area called the
**mempool**, where anyone can read it.

Someone is watching. They see your order, and they see that it will move the price.
So they place their own order just before yours, let yours push the price, and sell
straight after. You get a worse price. They pocket the difference. Your transaction
paid for their profit.

This is a **sandwich attack**. It is not a bug, and nobody is breaking any rules.
It is a direct consequence of the mempool being public. Wagner's literature note
puts the frequency plainly:

> About every 30 seconds an Ethereum user gets sandwiched on average.

The general term for value extractable by whoever controls transaction visibility
and ordering is **MEV**. Sandwiching is the part of MEV that comes specifically
from being able to *read* transactions early.

## The idea of a fix

If nobody can read your transaction until it is too late to react, they cannot
front-run it. So: **encrypt the transaction, let it be included in a block while
still encrypted, and only decrypt it once its position is locked in.**

That immediately raises the question that the whole field is about. Who holds the
decryption key?

Not you: you might go offline and stall the chain. Not one server: that server
becomes a single party who can read everything, which is the problem you started
with. So you split the key.

## Threshold encryption

**Threshold encryption** splits a decryption key across n parties, such that any t
of them together can decrypt, and any fewer than t learn nothing at all. Not a
little bit less. Nothing.

The n parties are a **committee**, often called keypers. On a blockchain they might
be validators. Users encrypt to the committee's joint public key. Once a block is
fixed, each committee member publishes one short **decryption share**, and anyone
can combine t of them to recover the key and read the transactions.

That is the whole architecture. Everything else in this knowledge base is about the
gap between that paragraph and something you could actually ship.

## Why it is hard: five things that go wrong

**One key per block, not one per transaction.** A block has hundreds of
transactions. If the committee has to do work per transaction, and every committee
member has to broadcast something per transaction, the bandwidth cost is
hundreds times the committee size. So you want *one* short value that opens a whole
block. That is **batching**, and it turns out to be genuinely difficult. See
[[D14]].

**Only the transactions that got in.** The committee must decrypt exactly the
transactions included in the block, and nothing else. Otherwise an attacker submits
a transaction, gets the committee to decrypt the whole pool, and reads everything
that did not make it in.

**Setting up the committee is expensive.** The classic way to split a key is an
interactive protocol among all n parties, a **distributed key generation** or DKG.
With a large committee that is slow and fragile, and it must be redone whenever the
committee changes. The alternative, where everyone just posts their own key and the
joint key is computed from those, is called **silent setup**, and getting it was a
significant research result.

**Forks.** Blockchains temporarily disagree about which block is next. If a
committee member publishes shares on two competing versions of history, an attacker
can collect a few shares from each and combine them into a decryption that no
majority ever authorised. Preventing that is **context binding**.

**Quantum computers.** Almost every efficient scheme here relies on mathematics
(elliptic curve pairings) that a quantum computer would break. Committee keys are
long-lived, so this is not a distant concern for them. Schemes built on **lattice**
mathematics are believed to survive quantum attack, and they are dramatically more
expensive today. That gap is the reason this knowledge base exists.

## Where things actually stand

Honest summary, as of the papers collected here.

**Classically, this is close to solved.** [[beat-mev]] and its successors give you
batched, epoch-free threshold encryption over pairings at practical cost:
transactions encrypt in about 2 ms, an entire block of 512 decrypts in under half a
second, ciphertexts are a few hundred bytes, and a committee member broadcasts
tens of bytes per block. If quantum computers did not exist, the cryptography would
essentially be ready.

**Post-quantum, it is not close.** The one implementation that measures a
post-quantum batched scheme end to end,
[[beatmev-pq-implementation]], reports at batch size 512:

| | classical | post-quantum | factor |
|---|---|---|---|
| ciphertext | 722 bytes | 1.9 MB | ~2700x |
| combine a block | 3.8 to 7.7 s | 327 s | ~40-90x |
| public key | a few KB | 259 MB | ~10^5x |

A 1.9 MB ciphertext per transaction is not deployable on a chain. 327 seconds to
open a block is longer than the block. So the post-quantum answer is not "slower",
it is "not a mempool".

**There is a theoretically better post-quantum answer that nobody can run.**
[[blt-batch-ibe]] achieves a genuinely tiny block-opening key from lattices, about
five orders of magnitude smaller than the batch. But at secure parameters it needs
matrices with roughly a billion columns, so its own reference implementation runs
only at toy sizes that provide no security at all.

That is the state of the art: a solved classical problem, a measured
post-quantum disaster, and a promising post-quantum construction stuck between
them.

## Where to go next

Four different routes into the same material. Pick the one matching why you came.

- **[[the-goals]]** starts from what a good scheme would look like: the fifteen
  requirements D1 to D15, in plain terms, and which of them pull against each
  other. Read this if you want the evaluation framework.
- **[[the-problems]]** starts from what goes wrong: the attacks, the two
  impossibility results, and the seven open problems with what would count as
  solving each. Read this if you want to know what to work on.
- **[[the-history]]** tells the story in order, from 2005 to 2026, so each result
  arrives as an answer to the previous one's limitation. Read this if you want to
  understand *why* the schemes look the way they do.
- **[[choosing-a-scheme]]** is for someone deciding what to build on today, with
  comparison tables and a recommendation per deployment shape.

And **[[glossary]]** defines every term in one line, if a word here was unfamiliar.

## How this knowledge base is put together

Every note is markdown with structured frontmatter, and the frontmatter generates a
typed graph: 27 schemes, 15 requirements, 7 open problems, 5 attacks, and the
assumptions and techniques they rest on, wired together with edges like
`satisfies`, `assumes`, `builds_on` and `attacks`.

That means claims are queryable rather than buried in prose:

```bash
python3 skill/scripts/query.py filter --type scheme --pq true --satisfies D14
```

Every note also carries its own provenance. `source_depth: full-text` means it was
checked against the paper; `abstract` means only the abstract was available.
`peer_reviewed: false` means treat it as a preprint. `self_assessed: true` means the
evaluation was done by the authors of the thing being evaluated. `disputes` records
where sources contradict each other instead of quietly picking a winner.

One node needs a warning: **TACET** is an unpublished, unreviewed draft by this
repository's owner. It is included for its measurements and for two useful findings
that came out of building it, not as a peer-reviewed result, and it is labelled as
such throughout.

The requirements D1 to D15 come from [[wagner-desiderata]], an Ethereum Foundation
literature note. That note is not numbered; the numbering here is a documented
flattening of it, explained in `vault/desiderata/_wagner-mapping.md`.
