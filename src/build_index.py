#!/usr/bin/env python3
# src/build_index.py
# Stub: builds a fake FAISS index placeholder for testing workflows
from pathlib import Path, json
OUT = Path('data/index')
OUT.mkdir(parents=True, exist_ok=True)
meta = {'created': 'stub', 'num_vectors': 0}
(OUT/'meta.json').write_text(json.dumps(meta, indent=2))
print('Wrote data/index/meta.json (stub)')
