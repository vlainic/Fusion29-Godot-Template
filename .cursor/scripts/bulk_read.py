#!/usr/bin/env python3
"""Summarize large files via Haiku; print bullets only (no raw file to stdout)."""

from __future__ import annotations

import argparse
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from anthropic_shunt import complete

SYSTEM = """You are a bulk reader for a coding agent.
Read the attached file contents and answer ONLY with concise markdown bullets.
Each bullet must cite symbol or section names and approximate line numbers when possible.
No preamble, no code fences unless a tiny snippet is essential (max 3 lines).
Do not reproduce the whole file."""


def _read_file_block(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    return f'<file path="{path}">\n{content}\n</file>'


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-read files via Haiku")
    parser.add_argument("paths", nargs="+", help="File paths to summarize")
    parser.add_argument(
        "--question",
        default="Summarize what matters for the current task.",
        help="What the main agent needs from these files",
    )
    args = parser.parse_args()

    blocks: list[str] = []
    for p in args.paths:
        if not os.path.isfile(p):
            print(f"Error: not a file: {p}", file=sys.stderr)
            return 1
        blocks.append(_read_file_block(p))

    user = (
        f"Question: {args.question}\n\n"
        + "\n\n".join(blocks)
    )
    try:
        summary = complete(SYSTEM, user)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
