# PQ Threshold Encryption Knowledge Base

Canonical knowledge base for post-quantum threshold encryption for encrypted
mempools. Work in progress; see the milestones in the task description.

Three consumption modes (documented in full once the vault is populated):

1. **Obsidian vault** - open `vault/` as a vault.
2. **Agent skill** - `skill/SKILL.md` plus `skill/scripts/query.py`.
3. **Static webapp** - `webapp/`, built by `scripts/build_webapp.py`.

## Local checks

```bash
pip install -r requirements.txt
python3 scripts/test_kb.py          # script self-tests
python3 scripts/build_graph.py      # vault -> graph/graph.json
python3 scripts/validate.py         # links, schema, quality bar, orphans
python3 scripts/build_webapp.py     # -> dist/
```
