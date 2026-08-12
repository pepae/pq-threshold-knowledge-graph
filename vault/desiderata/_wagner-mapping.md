# D1-D15 and Wagner's note: the exact mapping

**Wagner's note contains no numbered desiderata.** The
["Criteria / Properties that we care about"](https://notes.ethereum.org/@b-wagn/SkZxlQEYbg)
section is an unnumbered nested bullet list: thirteen top-level bullets, three of
which have sub-bullets. Any "D1-D15" numbering is therefore a flattening imposed
on top of it, and different flattenings give different counts.

This KB uses the flattening from `bench/ef_requirements.py` in
[pepae/pq-threshold](https://github.com/pepae/pq-threshold), so that the KB and
that project's scorecard mean the same thing by each identifier. The mapping:

| id | short name | Wagner's bullet (verbatim) | nesting |
|---|---|---|---|
| D1 | No trusted setup | trusted setup (want to avoid) | top level |
| D2 | Silent setup | silent setup vs. DKG (if number of parties large, avoid DKG) | top level |
| D3 | Non-interactive decryption | non-interactive decryption protocol | top level |
| D4 | CCA2 and associated data | CPA vs. CCA1 vs. CCA2 security (want CCA2) | under "security model" |
| D5 | Ciphertext-adaptive | selective vs. adaptive wrt ciphertext (want adaptive) | under "security model" |
| D6 | Corruption-adaptive | static vs. adaptive wrt corruptions (both seems fine, adaptive preferred) | under "security model" |
| D7 | Rogue-ciphertext security | for batched: security against rogue ciphertext attacks | under "security model" |
| D8 | Post-quantum | plausible PQ or not (want PQ) | top level |
| D9 | Context-dependent shares | context-dependent decryption shares | top level |
| D10 | Small public key | public key size (individual for silent setup) | top level |
| D11 | Small ciphertext | ciphertext size / overhead | top level |
| D12 | Short decryption keys | short decryption keys | top level |
| D13 | Small decryption shares | decryption share size | top level |
| D14 | Epoch-free batching | batch decryption | top level |
| D15 | Fast decryption | computationally efficient decryption (this is on critical path) | top level |

## Sub-bullets folded into their parent

Four of Wagner's sub-bullets do not get their own identifier and are folded into
the D-note they qualify:

- *can use hybrid encryption, but need to be careful* and *need thrKEM with
  associated data, as otherwise CCA2 not preserved* sit under "short decryption
  keys". The associated-data requirement is tracked in **D4**, because that is
  where it bites, and hybrid encryption is discussed in **D12**.
- *threshold IBE solutions ideal for that setting* sits under "short decryption
  keys" and is discussed in **D12**.
- *release one short decryption key for a large number of ciphertexts* and *with
  or without slot number, or "epoch-based" vs. "epoch-free" (ideally: without)*
  sit under "batch decryption" and are both part of **D14**. This is why D14's
  short name is "epoch-free batching" rather than just "batching": the epoch-free
  half is a sub-bullet, not a separate criterion.

## The one bullet with no identifier

> hardness assumptions and idealizations (want to use established ones)

This top-level bullet receives **no D number** in this flattening. That is a real
gap, and the KB compensates in two ways rather than pretending otherwise:

1. [[D8]] records the omission explicitly in its own note.
2. Assumption quality is represented structurally instead, on the `assumes` edges
   and the `falsifiable` field of each [assumption](../concepts/) node. A scheme
   resting on [[module-lwe]] and one resting on a q-type pairing assumption proved
   in the [[ggm]] are not equally well founded, and the graph shows that directly:

```
python3 skill/scripts/query.py neighbors beast-mev --edge-type assumes
python3 skill/scripts/query.py node ggm
```

So "does this scheme use established assumptions" is answerable by query, just not
by a desideratum edge.

## If you want a different numbering

Change it here and in `bench/ef_requirements.py` together, or the two artifacts
will silently disagree about what D14 means. The ids are load-bearing: they appear
in `satisfies`, `partially_satisfies` and `fails` edges across 27 scheme notes, and
`scripts/validate.py` enforces the `^D([1-9]|1[0-5])$` form.
