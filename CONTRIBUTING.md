# Contributing

Frontmatter is the single source of truth for the graph; prose is for humans.
`graph/schema.json` defines every legal node type, field, and edge type.

Full guide lands with milestone 5. For now:

```bash
pip install -r requirements.txt
python3 scripts/build_graph.py && python3 scripts/validate.py
```
