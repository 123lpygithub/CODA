from __future__ import annotations

import json
from typing import Any


def _strip_code_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _extract_balanced_span(
    text: str,
    *,
    opener: str,
    closer: str,
) -> str | None:
    start = text.find(opener)
    if start < 0:
        return None
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def extract_json_object(text: str) -> dict[str, Any] | None:
    """Extract the first JSON object from model output."""

    candidate = _extract_balanced_span(_strip_code_fences(text), opener="{", closer="}")
    if not candidate:
        return None
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def extract_json_array(text: str) -> list[Any] | None:
    """Extract the first JSON array from model output."""

    candidate = _extract_balanced_span(_strip_code_fences(text), opener="[", closer="]")
    if not candidate:
        return None
    try:
        value = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, list) else None


def require_fields(
    payload: dict[str, Any] | None,
    *,
    required_fields: list[str],
) -> dict[str, Any]:
    """Raise a clear error when required JSON fields are missing."""

    if payload is None:
        raise ValueError("Expected a JSON object, but none could be parsed.")
    missing = [field_name for field_name in required_fields if field_name not in payload]
    if missing:
        msg = f"Missing required fields: {', '.join(missing)}"
        raise ValueError(msg)
    return payload
