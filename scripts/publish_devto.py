#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import Any

from publish_utils import dump_json, load_markdown_asset, maybe_write_output, normalize_tags, request_json


DEVTO_URL = "https://dev.to/api/articles"


def build_payload(metadata: dict[str, Any], body: str, args: argparse.Namespace) -> dict[str, Any]:
    article: dict[str, Any] = {
        "title": args.title or metadata["title"],
        "body_markdown": body,
        "published": bool(args.publish or metadata.get("published", False)),
    }

    if description := args.description or metadata.get("description"):
        article["description"] = description
    if canonical := args.canonical_url or metadata.get("canonical_url"):
        article["canonical_url"] = canonical
    if image := args.main_image or metadata.get("cover_image"):
        article["main_image"] = image
    if series := args.series or metadata.get("series"):
        article["series"] = series
    if slug := args.slug or metadata.get("slug"):
        article["slug"] = slug
    if organization_id := args.organization_id or metadata.get("organization_id"):
        article["organization_id"] = int(organization_id)

    tags = normalize_tags(args.tags or metadata.get("tags"))
    if tags:
        article["tags"] = ",".join(tags)

    return {"article": article}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish or draft a post to dev.to/Forem.")
    parser.add_argument("--file", required=True, help="Markdown file with simple front matter.")
    parser.add_argument("--api-key", default=os.environ.get("DEVTO_API_KEY"), help="dev.to API key.")
    parser.add_argument("--publish", action="store_true", help="Publish immediately instead of creating a draft.")
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--canonical-url")
    parser.add_argument("--main-image")
    parser.add_argument("--series")
    parser.add_argument("--slug")
    parser.add_argument("--tags", help="Comma-separated override.")
    parser.add_argument("--organization-id")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without hitting the API.")
    parser.add_argument("--output", help="Optional file path for payload or API response.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata, body = load_markdown_asset(args.file)
    payload = build_payload(metadata, body, args)

    if args.dry_run:
        rendered = dump_json(payload)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if not args.api_key:
        raise SystemExit("Missing dev.to API key. Set DEVTO_API_KEY or pass --api-key.")

    response = request_json(
        url=DEVTO_URL,
        headers={
            "accept": "application/vnd.forem.api-v1+json",
            "content-type": "application/json",
            "api-key": args.api_key,
        },
        payload=payload,
    )
    rendered = dump_json(response)
    print(rendered)
    maybe_write_output(args.output, rendered)


if __name__ == "__main__":
    main()

