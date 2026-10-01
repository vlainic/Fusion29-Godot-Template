"""Pure decision logic for large-file read shunt (unit-testable)."""

from __future__ import annotations

import os
import re
import shlex
from dataclasses import dataclass
from typing import Optional

DEFAULT_MAX_LINES = 350


def max_lines() -> int:
    raw = os.environ.get("SHUNT_MAX_LINES", "").strip()
    if not raw:
        return DEFAULT_MAX_LINES
    try:
        value = int(raw)
        return value if value > 0 else DEFAULT_MAX_LINES
    except ValueError:
        return DEFAULT_MAX_LINES


def count_lines(path: str) -> int:
    with open(path, "rb") as fh:
        return sum(1 for _ in fh)


def read_window_size(total_lines: int, offset: Optional[int], limit: Optional[int]) -> int:
    if total_lines <= 0:
        return 0
    start = offset if offset is not None and offset > 0 else 1
    if start > total_lines:
        return 0
    remaining = total_lines - start + 1
    if limit is None or limit <= 0:
        return remaining
    return min(limit, remaining)


@dataclass(frozen=True)
class GateDecision:
    allow: bool
    reason: str = ""


def should_allow_read(
    total_lines: int,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    cap: Optional[int] = None,
) -> GateDecision:
    cap = cap if cap is not None else max_lines()
    if total_lines <= cap:
        return GateDecision(True, "file_within_cap")
    window = read_window_size(total_lines, offset, limit)
    if window <= cap:
        return GateDecision(True, "bounded_window")
    return GateDecision(False, "full_or_large_window")


def bulk_read_hint(paths: list[str], question: str = "") -> str:
    paths_str = " ".join(f'"{p}"' for p in paths)
    q = question.strip() or "Summarize what matters for the current task."
    return (
        f"Large file read blocked (>{max_lines()} lines). "
        f'Run: python3 .cursor/scripts/bulk_read.py {paths_str} --question "{q}" '
        "Do not retry full Read or cat on this file."
    )


# Shell dumpers we inspect (grep/rg intentionally excluded).
_DUMP_CMD_RE = re.compile(r"^(cat|head|tail|less|more|bat)\b", re.IGNORECASE)
_SED_PRINT_RE = re.compile(r"^sed\b.*\s(-n|--quiet|-E|-r)\b", re.IGNORECASE)


def _resolve_path(arg: str, cwd: str) -> Optional[str]:
    if not arg or arg.startswith("-"):
        return None
    path = arg if os.path.isabs(arg) else os.path.normpath(os.path.join(cwd, arg))
    if os.path.isfile(path):
        return path
    return None


def _head_tail_line_cap(argv: list[str], cmd: str) -> Optional[int]:
    """Return max lines the command may print, or None if unbounded."""
    if cmd.lower() == "head":
        for i, a in enumerate(argv[1:], start=1):
            if a in ("-n", "--lines") and i + 1 < len(argv):
                try:
                    return int(argv[i + 1])
                except ValueError:
                    return None
            if a.startswith("-n") and len(a) > 2:
                try:
                    return int(a[2:])
                except ValueError:
                    return None
        return 10
    if cmd.lower() == "tail":
        for i, a in enumerate(argv[1:], start=1):
            if a in ("-n", "--lines") and i + 1 < len(argv):
                try:
                    return int(argv[i + 1])
                except ValueError:
                    return None
            if a.startswith("-n") and len(a) > 2:
                try:
                    return int(a[2:])
                except ValueError:
                    return None
        return 10
    return None


def should_allow_shell(command: str, cwd: str, cap: Optional[int] = None) -> GateDecision:
    cap = cap if cap is not None else max_lines()
    command = command.strip()
    if not command:
        return GateDecision(True, "empty")

    try:
        argv = shlex.split(command)
    except ValueError:
        return GateDecision(True, "unparsed")

    if not argv:
        return GateDecision(True, "empty_argv")

    base = os.path.basename(argv[0])
    if base.lower() not in ("cat", "head", "tail", "less", "more", "bat", "sed"):
        return GateDecision(True, "not_a_dumper")

    if base.lower() == "sed":
        if not _SED_PRINT_RE.match(command):
            return GateDecision(True, "sed_not_print")
        # sed -n with arbitrary range: treat as unbounded dump
        line_cap = None
    elif not _DUMP_CMD_RE.match(base):
        return GateDecision(True, "not_a_dumper")
    else:
        line_cap = _head_tail_line_cap(argv, base)

    if base.lower() in ("less", "more", "bat"):
        line_cap = None

    if base.lower() == "cat":
        line_cap = None

    targets: list[str] = []
    for arg in argv[1:]:
        if arg.startswith("-"):
            continue
        resolved = _resolve_path(arg, cwd)
        if resolved:
            targets.append(resolved)

    if not targets:
        return GateDecision(True, "no_file_target")

    for path in targets:
        try:
            total = count_lines(path)
        except OSError:
            continue
        if total <= cap:
            continue
        if line_cap is not None and line_cap <= cap:
            continue
        return GateDecision(False, f"shell_dump:{path}")

    return GateDecision(True, "shell_ok")
