#!/usr/bin/env python3
# scripts/agents/composer.py
# Stub composer: reads top-k from data/index/meta.json and writes a draft
from pathlib import Path, json
DRAFTS = Path('drafts')
DRAFTS.mkdir(parents=True, exist_ok=True)
d = DRAFTS/'sample_section.md'
d.write_text('# Sample Section\n\nThis is an auto-generated draft (stub).')
print('Wrote', d)
