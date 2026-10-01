---
name: code-write
description: Generate a new file that should match an existing reference (tests, GDScript siblings) without pasting the reference or output into the main agent context.
disable-model-invocation: false
---

# Code write (Haiku shunt)

Use when adding a file that should mirror patterns in an existing one (e.g. another test or menu script):

```bash
python3 .cursor/scripts/code_write.py \
  --spec "Describe behavior, exports, signals, and edge cases." \
  --reference "path/to/similar_existing.gd" \
  --out "path/to/new_file.gd"
```

- Do **not** `Read` the reference into the main chat if it is large; the script sends it to Haiku.
- After success, trust the one-line confirmation unless you must edit—then use bounded reads or bulk-read.
- Requires `ANTHROPIC_API_KEY`. Optional: `ANTHROPIC_SHUNT_MODEL`.
