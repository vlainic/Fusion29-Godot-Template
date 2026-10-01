---
name: bulk-read
description: Use when a large file Read or cat was blocked by the shunt hook, or when you need structured bullets from files over SHUNT_MAX_LINES without loading them into context.
disable-model-invocation: false
---

# Bulk read (Haiku shunt)

When the hook denies a **Read** or shell dump of a large file:

1. Do **not** retry full `Read`, `cat`, or unbounded `sed` on that path.
2. Run from the project root:

```bash
python3 .cursor/scripts/bulk_read.py "path/to/file" --question "Your specific question"
```

3. Use multiple paths in one call if needed: `python3 .cursor/scripts/bulk_read.py file1 file2 --question "..."`
4. Work from the printed bullets only. Use bounded `Read` with `offset` + `limit` (window ≤ 350 lines) if you need exact lines.

Requires `ANTHROPIC_API_KEY` in the environment. Optional: `ANTHROPIC_SHUNT_MODEL`, `SHUNT_MAX_LINES`.
