# Source PDFs: provenance and licence

Generated alongside `papers/WANTED.md`. One row per file in `papers/pdf/`.

**Licence.** Every eprint-hosted file here is the authors' own submission to the
IACR Cryptology ePrint Archive, retrieved from the URL in the table. ePrint
submissions are distributed under the terms the authors chose, commonly CC BY 4.0
or author-retained copyright with permission to distribute; they are **not**
publisher versions, and no Springer, ACM, IEEE or USENIX typeset PDF is included.
If you are an author and want a file removed, open an issue and it will be removed.

Rights in these PDFs belong to their authors and are unaffected by this
repository's own licence.

18 files.

| file | source | title | vault note |
|---|---|---|---|
| `2009-391.pdf` | [2009/391](https://eprint.iacr.org/2009/391) | Bendlin-Damgard threshold Regev | `bendlin-damgard` |
| `2021-630.pdf` | [2021/630](https://eprint.iacr.org/2021/630) | Non-interactive CCA2 threshold cryptosystems without pairings | `devevey-libert-nguyen-peters-yung` |
| `2023-016.pdf` | [2023/016](https://eprint.iacr.org/2023/016) | Boudgoust-Scholl threshold FHE at polynomial modulus | `boudgoust-scholl` |
| `2023-1728.pdf` | [2023/1728](https://eprint.iacr.org/2023/1728) | Micciancio-Suhl simulation-secure threshold PKE | `micciancio-suhl` |
| `2024-1417.pdf` | [2024/1417](https://eprint.iacr.org/2024/1417) | Distributed broadcast encryption from lattices | `champion-wu-dbe` |
| `2024-1533.pdf` | [2024/1533](https://eprint.iacr.org/2024/1533) | BEAT-MEV | `beat-mev` |
| `2024-263.pdf` | [2024/263](https://eprint.iacr.org/2024/263) | Threshold Encryption with Silent Setup | `gkpw-silent-setup` |
| `2025-1254.pdf` | [2025/1254](https://eprint.iacr.org/2025/1254) | BLT threshold batch IBE without epochs | `blt-batch-ibe`, `identity-tag-replication`, `index-collision-censorship` |
| `2025-1419.pdf` | [2025/1419](https://eprint.iacr.org/2025/1419) | BEAST-MEV | `beast-mev` |
| `2025-1665.pdf` | [2025/1665](https://eprint.iacr.org/2025/1665) | Threshold Public-Key Encryption: Definitions, Relations, and CPA-to-CCA Transforms | `brzuska-klooss-woo` |
| `2025-1691.pdf` | [2025/1691](https://eprint.iacr.org/2025/1691) | Pilvi | `pilvi` |
| `2025-279.pdf` | [2025/279](https://eprint.iacr.org/2025/279) | Context-dependent threshold decryption | `bbnrs-context-dependent` |
| `2026-1454.pdf` | [2026/1454](https://eprint.iacr.org/2026/1454) | Batched attribute-based encryption from bilinear pairings | `batched-abe-pairings` |
| `2026-1464.pdf` | [2026/1464](https://eprint.iacr.org/2026/1464) | Optimal distributed monotone-policy encryption for DNFs | `champion-wu-optimal-dnf` |
| `2026-1627.pdf` | [2026/1627](https://eprint.iacr.org/2026/1627) | Adaptively secure threshold decryption at polynomial modulus | `sjtu-adaptive-threshold-decryption` |
| `2026-318.pdf` | [2026/318](https://eprint.iacr.org/2026/318) | Distributed monotone-policy encryption for DNFs from lattices | `champion-wu-monotone-dnf` |
| `2026-754.pdf` | [2026/754](https://eprint.iacr.org/2026/754) | BTX | `btx` |
| `TACET.pdf` | not on eprint | TACET working draft | `tacet`, `tacet-silent` |

## Adding to this list

Drop the PDF into `papers/pdf/` named `YYYY-NNNN.pdf`, then run
`python3 scripts/check_pdfs.py --write`. See `papers/pdf/README.md`.
