#!/usr/bin/env python3
"""Cursor hook: block full reads / shell dumps of files over SHUNT_MAX_LINES."""

from __future__ import annotations

import json
import os
import sys

from shunt_gate_lib import (
    bulk_read_hint,
    count_lines,
    max_lines,
    should_allow_read,
    should_allow_shell,
)


def _emit(payload: dict) -> None:
    print(json.dumps(payload), flush=True)


def _deny(user: str, agent: str) -> None:
    _emit(
        {
            "permission": "deny",
            "user_message": user,
            "agent_message": agent,
        }
    )


def _allow() -> None:
    _emit({"permission": "allow"})


def _handle_pre_tool_use(data: dict) -> None:
    if data.get("tool_name") != "Read":
        _allow()
        return

    tool_input = data.get("tool_input") or {}
    path = tool_input.get("path") or tool_input.get("file_path")
    if not path or not os.path.isfile(path):
        _allow()
        return

    offset = tool_input.get("offset")
    limit = tool_input.get("limit")
    if offset is not None:
        try:
            offset = int(offset)
        except (TypeError, ValueError):
            offset = None
    if limit is not None:
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = None

    try:
        total = count_lines(path)
    except OSError:
        _allow()
        return

    decision = should_allow_read(total, offset, limit)
    if decision.allow:
        _allow()
        return

    cap = max_lines()
    user = f"Blocked read of {path} ({total} lines; cap {cap}). Use bulk_read.py."
    agent = bulk_read_hint([path])
    _deny(user, agent)


def _handle_before_shell(data: dict) -> None:
    command = data.get("command") or ""
    cwd = data.get("cwd") or os.getcwd()
    decision = should_allow_shell(command, cwd)
    if decision.allow:
        _allow()
        return

    # Extract first file path from decision reason if present
    path = decision.reason.split(":", 1)[-1] if ":" in decision.reason else ""
    paths = [path] if path and os.path.isfile(path) else []
    user = f"Blocked shell dump of a large file (>{max_lines()} lines). Use bulk_read.py."
    agent = bulk_read_hint(paths) if paths else bulk_read_hint([], "Summarize the file you need.")
    _deny(user, agent)


def main() -> int:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        _allow()
        return 0

    event = data.get("hook_event_name") or ""
    if event == "preToolUse":
        _handle_pre_tool_use(data)
    elif event == "beforeShellExecution":
        _handle_before_shell(data)
    else:
        _allow()
    return 0


if __name__ == "__main__":
    sys.exit(main())
