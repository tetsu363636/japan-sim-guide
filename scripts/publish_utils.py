#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib import error, request


class FrontMatterError(ValueError):
    """Raised when a markdown file has malformed front matter."""


def coerce_value(raw_value: str) -> Any:
    value = raw_value.strip()
    if not value:
        return ""

    if value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [coerce_value(item) for item in inner.split(",")]
    return value


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    normalized = text.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, normalized

    metadata: dict[str, Any] = {}
    body_start = None
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.strip() == "---":
            body_start = idx + 1
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise FrontMatterError(f"Invalid front matter line: {line!r}")
        key, raw_value = line.split(":", 1)
        metadata[key.strip()] = coerce_value(raw_value)

    if body_start is None:
        raise FrontMatterError("Front matter opened with '---' but never closed.")

    body = "\n".join(lines[body_start:]).lstrip("\n")
    return metadata, body


def load_markdown_asset(path: str | Path) -> tuple[dict[str, Any], str]:
    text = Path(path).read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    if "title" not in metadata:
        raise FrontMatterError("Expected a 'title' field in front matter.")
    return metadata, body


def normalize_tags(raw_tags: Any) -> list[str]:
    if raw_tags is None:
        return []
    if isinstance(raw_tags, list):
        items = raw_tags
    else:
        items = str(raw_tags).split(",")
    tags = []
    for item in items:
        tag = str(item).strip()
        if tag:
            tags.append(tag)
    return tags


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-")


def dump_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def maybe_write_output(path: str | None, content: str) -> None:
    if not path:
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content + "\n", encoding="utf-8")


def request_json(
    *,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> dict[str, Any]:
    req = request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {details}") from exc

