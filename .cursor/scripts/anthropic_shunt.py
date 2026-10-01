"""Minimal Anthropic Messages API client (stdlib only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_MODEL = "claude-haiku-4-5"
DEFAULT_TIMEOUT = 30
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


def model_id() -> str:
    return os.environ.get("ANTHROPIC_SHUNT_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def complete(system: str, user: str, temperature: float = 0.2) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    body = {
        "model": model_id(),
        "max_tokens": 4096,
        "temperature": temperature,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic API error {exc.code}: {detail}") from exc

    blocks = payload.get("content") or []
    parts: list[str] = []
    for block in blocks:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text") or "")
    text = "".join(parts).strip()
    if not text:
        raise RuntimeError("Anthropic API returned empty text")
    return text
