# Source PDFs

Drop PDFs into this folder. **Name each file by its eprint id with the slash
replaced by a hyphen**, for example `2025-1254.pdf`. That naming is what lets the
build link a vault note to its local PDF automatically.

Every link below goes to the eprint PDF. Commit the **eprint** version, not the
Springer or USENIX one: eprint submissions are CC BY or author-retained and fine
to redistribute in a public repo, publisher PDFs are not.

Why this is needed at all: eprint and USENIX serve PDFs behind a Cloudflare bot
challenge, so this session can read abstract pages but no full text. Everything
below is already recorded in the vault from its verified abstract; the PDFs are
what upgrade `source_depth: abstract` to `full-text` and let the parameter
tables, lemma statements and per-desideratum reasoning be checked against the
source.

## Tier 1: the vault makes claims about internals that cannot be verified without these

| eprint | save as | paper | what is blocked |
|---|---|---|---|
| [`2025/1254`](https://eprint.iacr.org/2025/1254.pdf) | `2025-1254.pdf` | Threshold Batch IBE without Epochs (Boneh, Laufer, Tas) | succinctness barrier + PQ BEAT-MEV appendix, both named in the brief |
| [`2026/1627`](https://eprint.iacr.org/2026/1627.pdf) | `2026-1627.pdf` | Adaptively Secure Threshold Decryption from LWE with Poly Modulus (Zhang, Zhou, Han, Liu, Huang) | Lemma 6, ZeroShare, TD0/TD1/TD2, and which open problem it resolves |
| [`2023/1728`](https://eprint.iacr.org/2023/1728.pdf) | `2023-1728.pdf` | Simulation-Secure Threshold PKE from LWE with Poly Modulus (Micciancio, Suhl) | the FrodoKEM-comparable parameter table |
| [`2023/016`](https://eprint.iacr.org/2023/016.pdf) | `2023-016.pdf` | Simple Threshold (FHE) from LWE with Poly Modulus (Boudgoust, Scholl) | the Renyi argument and why it is game-based only |
| [`2025/279`](https://eprint.iacr.org/2025/279.pdf) | `2025-279.pdf` | Context-Dependent Threshold Decryption (Boneh, Bunz, Nayak, Rotem, Shoup) | the two constructions and the generic add-context transform |
| [`2025/1665`](https://eprint.iacr.org/2025/1665.pdf) | `2025-1665.pdf` | Threshold PKE: Definitions, Relations, CPA-to-CCA (Brzuska, Klooss, Woo) | the definitional implications and separations are the whole node |
| [`2021/630`](https://eprint.iacr.org/2021/630.pdf) | `2021-630.pdf` | Non-Interactive CCA2 Threshold Cryptosystems (Devevey, Libert, Nguyen, Peters, Yung) | to source the open problem 2026/1627 claims to resolve |

## Tier 2: headline numbers came from the abstract, full text would sharpen

| eprint | save as | paper | what is blocked |
|---|---|---|---|
| [`2025/1419`](https://eprint.iacr.org/2025/1419.pdf) | `2025-1419.pdf` | BEAST-MEV (Bormet, Choudhuri, Faust, Garg, Othman, Policharla, Qu, Wang) | abstract has no evaluation numbers at all |
| [`2024/1533`](https://eprint.iacr.org/2024/1533.pdf) | `2024-1533.pdf` | BEAT-MEV (Bormet, Faust, Othman, Qu) | key sizes and the index-collision failure rate |
| [`2025/1691`](https://eprint.iacr.org/2025/1691.pdf) | `2025-1691.pdf` | Pilvi (Cini, Lai, Woo) | the low-norm sharing and the threshold-LWE definition |
| [`2024/1417`](https://eprint.iacr.org/2024/1417.pdf) | `2024-1417.pdf` | Distributed Broadcast Encryption from Lattices (Champion, Wu) | how l-succinct LWE is used |
| [`2026/318`](https://eprint.iacr.org/2026/318.pdf) | `2026-318.pdf` | Distributed Monotone-Policy Encryption for DNFs (Champion, Wu) | to settle whether 2026/1464 supersedes it |
| [`2026/1464`](https://eprint.iacr.org/2026/1464.pdf) | `2026-1464.pdf` | Optimal Distributed Monotone-Policy Encryption for DNFs (Champion, Wu) | same question, other side |
| [`2009/391`](https://eprint.iacr.org/2009/391.pdf) | `2009-391.pdf` | Threshold Decryption and ZK Proofs for Lattice-Based Cryptosystems (Bendlin, Damgard) | root of the linear route; parameters |

## Tier 3: completeness, so the repo holds every paper the KB cites

| eprint | save as | paper | note |
|---|---|---|---|
| [`2024/263`](https://eprint.iacr.org/2024/263.pdf) | `2024-263.pdf` | Threshold Encryption with Silent Setup (Garg, Kolonelos, Policharla, Wang) |  |
| [`2024/669`](https://eprint.iacr.org/2024/669.pdf) | `2024-669.pdf` | Mempool Privacy via Batched Threshold Encryption: Attacks and Defenses (Choudhuri, Garg, Piet, Policharla) |  |
| [`2024/1516`](https://eprint.iacr.org/2024/1516.pdf) | `2024-1516.pdf` | Practical Mempool Privacy via One-time Setup BTE (Choudhuri, Garg, Policharla, Wang) |  |
| [`2025/1384`](https://eprint.iacr.org/2025/1384.pdf) | `2025-1384.pdf` | Silent Threshold Encryption with One-Shot Adaptive Security (Hall-Andersen, Simkin, Wagner) |  |
| [`2025/1547`](https://eprint.iacr.org/2025/1547.pdf) | `2025-1547.pdf` | Silent Threshold Cryptography from Pairings (Waters, Wu) |  |
| [`2025/2115`](https://eprint.iacr.org/2025/2115.pdf) | `2025-2115.pdf` | Weighted Batched Threshold Encryption (Agarwal, Babel, Das, Gilkalaye, Mondal, Pinkas, Rindal, Yadav) |  |
| [`2017/956`](https://eprint.iacr.org/2017/956.pdf) | `2017-956.pdf` | Threshold Cryptosystems From Threshold FHE (Boneh, Gennaro, Goldfeder, Jain, Kim, Rasmussen, Sahai) |  |
| [`2024/1575`](https://eprint.iacr.org/2024/1575.pdf) | `2024-1575.pdf` | APTOS batched threshold IBE (Agarwal, Fernando, Pinkas) | from Wagner's note; I have no abstract yet |
| [`2025/2103`](https://eprint.iacr.org/2025/2103.pdf) | `2025-2103.pdf` | Batched threshold IBE, silent setup (GongWWW) | from Wagner's note |
| [`2026/372`](https://eprint.iacr.org/2026/372.pdf) | `2026-372.pdf` | Distributed monotone-policy encryption, l-decomposed LWE | from Wagner's note |
| [`2025/2048`](https://eprint.iacr.org/2025/2048.pdf) | `2025-2048.pdf` | Agarwal et al. (2) | from Wagner's note |
| [`2026/021`](https://eprint.iacr.org/2026/021.pdf) | `2026-021.pdf` | SOTA for lattice threshold encryption (per Wagner's note, Mar 2026) | from Wagner's note |
| [`2026/754`](https://eprint.iacr.org/2026/754.pdf) | `2026-754.pdf` | BTX | from Wagner's note; identical to 2026/760 |
| [`2026/760`](https://eprint.iacr.org/2026/760.pdf) | `2026-760.pdf` | BTX (Guru version) | from Wagner's note; identical to 2026/754 |
| [`2026/1195`](https://eprint.iacr.org/2026/1195.pdf) | `2026-1195.pdf` | Encrypted Mempools without Committees and via PoW | from Wagner's note |
| [`2026/1454`](https://eprint.iacr.org/2026/1454.pdf) | `2026-1454.pdf` | Uncategorized in Wagner's note | from Wagner's TODO list |
| [`2026/1585`](https://eprint.iacr.org/2026/1585.pdf) | `2026-1585.pdf` | Proving Threshold Regev PKE from Adaptive Hint-MLWE | from Wagner's TODO list |
| [`2026/1609`](https://eprint.iacr.org/2026/1609.pdf) | `2026-1609.pdf` | Uncategorized in Wagner's note | from Wagner's TODO list |
| [`2022/284`](https://eprint.iacr.org/2022/284.pdf) | `2022-284.pdf` | Lattice-Based ZK Proofs and Applications (Lyubashevsky, Nguyen, Plancon) | technique note only |
| [`2022/1341`](https://eprint.iacr.org/2022/1341.pdf) | `2022-1341.pdf` | LaBRADOR (Beullens, Seiler) | technique note only |
| [`2021/927`](https://eprint.iacr.org/2021/927.pdf) | `2021-927.pdf` | Bootstrap Lattice ZK Proofs to QROM NIZKs (Katsumata) | technique note only |

## Not on eprint

| source | save as | paper |
|---|---|---|
| [escholarship](https://www.escholarship.org/content/qt3b84884k/qt3b84884k_noSplash_70a7ed3adfc3e82bcceeecc5157da509.pdf) | `mevade-icbc-2023.pdf` | MEVade: An MEV-Resistant Blockchain Design (Piet, Nair, Subramanian), IEEE ICBC 2023 |
| [notes.ethereum.org](https://notes.ethereum.org/@b-wagn/SkZxlQEYbg) | `wagner-desiderata.md` | Wagner's encrypted mempool / threshold encryption literature note. Already captured in the vault as `vault/papers/wagner-desiderata.md`; a snapshot here guards against the note changing. |
| private repo | `tacet.pdf` | TACET. Already available to this session at `pepae/pq-threshold:paper/TACET.pdf`, so only add it here if the KB should ship it publicly. |

## After you drop them in

```bash
git add papers/pdf && git commit -m "Add source PDFs" && git push
```

Then tell the agent to backfill. It will extract text, replace every
`source_depth: abstract` with `full-text`, fill in the `assumptions_pending`
queue that `scripts/validate.py` prints, and correct anything the abstracts got
wrong. `papers/SOURCES.md` records URL, version and licence per paper.
