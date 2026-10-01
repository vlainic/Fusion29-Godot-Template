#!/usr/bin/env python3
"""Generate code via Haiku from spec + reference; write to disk; print metadata only."""

from __future__ import annotations

import argparse
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from anthropic_shunt import complete

SYSTEM = """You are a code writer for a Godot/GDScript project.
Match the reference file's style, naming, patterns, and structure.
Output ONLY the full source for the target file — no markdown fences, no explanation.
If the spec asks for GDScript, use Godot 4.x conventions."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Write code via Haiku using a reference file")
    parser.add_argument("--spec", required=True, help="What to implement")
    parser.add_argument("--reference", required=True, help="Path to pattern reference file")
    parser.add_argument("--out", required=True, help="Output file path")
    args = parser.parse_args()

    if not os.path.isfile(args.reference):
        print(f"Error: reference not found: {args.reference}", file=sys.stderr)
        return 1

    with open(args.reference, encoding="utf-8", errors="replace") as fh:
        ref_content = fh.read()

    user = (
        f"Specification:\n{args.spec}\n\n"
        f'<reference path="{args.reference}">\n{ref_content}\n</reference>\n\n'
        f"Write the complete file that should be saved to: {args.out}"
    )

    try:
        code = complete(SYSTEM, user)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    # Strip accidental fences
    text = code.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
        if not text.endswith("\n"):
            fh.write("\n")

    line_count = text.count("\n") + (1 if text else 0)
    print(f"Wrote {args.out} ({line_count} lines). Do not Read back unless you must edit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
