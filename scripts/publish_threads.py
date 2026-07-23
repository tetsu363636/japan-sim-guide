#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from publish_utils import build_url, dump_json, maybe_write_output, request_api_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNIPPETS = ROOT / "outreach" / "snippets" / "threads-posts.txt"
PUBLISH_BASE = os.environ.get("THREADS_PUBLISH_BASE", "https://graph.threads.net").rstrip("/")
DEFAULT_LOOKUP_FIELDS = "id,media_product_type,media_type,permalink,shortcode,text,timestamp,username"


def bearer_headers(access_token: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }


def parse_post_options(path: str | Path) -> dict[str, str]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    options: dict[str, str] = {}
    current_title: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_title, current_lines
        if current_title:
            body = "\n".join(current_lines).strip()
            if body:
                options[current_title] = body
        current_title = None
        current_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("post option"):
            flush()
            current_title = stripped
            continue
        if current_title is not None:
            current_lines.append(line.rstrip())

    flush()
    return options


def resolve_option(option: str, available: dict[str, str]) -> tuple[str, str]:
    if option in available:
        return option, available[option]

    numbered = f"Post option {option}"
    if numbered in available:
        return numbered, available[numbered]

    lowered = option.strip().lower()
    for title, body in available.items():
        if title.lower() == lowered:
            return title, body

    raise SystemExit(f"Unknown Threads option {option!r}. Run --list-options to see valid values.")


def describe_options(available: dict[str, str]) -> str:
    lines = []
    for title, body in available.items():
        preview = body.splitlines()[0].strip() if body.splitlines() else ""
        lines.append(f"{title}: {preview}")
    return "\n".join(lines)


def load_text(args: argparse.Namespace) -> tuple[str, dict[str, str]]:
    if args.text:
        return args.text.strip(), {"type": "inline"}

    if args.text_file:
        path = Path(args.text_file)
        return path.read_text(encoding="utf-8").strip(), {"type": "file", "path": str(path)}

    if args.option:
        available = parse_post_options(args.snippets_file)
        title, text = resolve_option(args.option, available)
        return text, {"type": "option", "name": title, "path": str(Path(args.snippets_file))}

    return "", {"type": "empty"}


def infer_media_type(args: argparse.Namespace) -> str:
    if args.image_url and args.video_url:
        raise SystemExit("Pass either --image-url or --video-url, not both.")
    if args.image_url:
        return "IMAGE"
    if args.video_url:
        return "VIDEO"
    return "TEXT"


def build_container_query(args: argparse.Namespace, text: str, media_type: str) -> dict[str, Any]:
    query: dict[str, Any] = {"media_type": media_type}

    if text:
        query["text"] = text
    if args.reply_control:
        query["reply_control"] = args.reply_control
    if args.reply_to_id:
        query["reply_to_id"] = args.reply_to_id
    if args.link_attachment:
        query["link_attachment"] = args.link_attachment
    if args.topic_tag:
        query["topic_tag"] = args.topic_tag
    if args.location_id:
        query["location_id"] = args.location_id
    if args.enable_reply_approvals:
        query["enable_reply_approvals"] = True
    if args.ghost_post:
        query["is_ghost_post"] = True

    if media_type == "TEXT":
        if args.alt_text:
            raise SystemExit("--alt-text is only valid for IMAGE or VIDEO posts.")
        if args.auto_publish_text:
            query["auto_publish_text"] = True
    elif media_type == "IMAGE":
        query["image_url"] = args.image_url
        if args.alt_text:
            query["alt_text"] = args.alt_text
    elif media_type == "VIDEO":
        query["video_url"] = args.video_url
        if args.alt_text:
            query["alt_text"] = args.alt_text

    return query


def validate_args(args: argparse.Namespace, text: str, media_type: str) -> None:
    if args.list_options:
        return

    if args.create_only and args.auto_publish_text:
        raise SystemExit("--create-only cannot be combined with --auto-publish-text.")

    if media_type != "TEXT" and args.link_attachment:
        raise SystemExit("--link-attachment is only supported for text posts.")

    if media_type == "TEXT" and not text and not args.link_attachment:
        raise SystemExit("Text posts need content. Pass --text, --text-file, --option, or --link-attachment.")

    if media_type in {"IMAGE", "VIDEO"} and not text and not args.captionless_media:
        raise SystemExit("Media posts need --text by default. Pass --captionless-media if you really want a media-only post.")


def create_container(access_token: str, query: dict[str, Any]) -> dict[str, Any]:
    return request_api_json(
        url=f"{PUBLISH_BASE}/me/threads",
        method="POST",
        headers=bearer_headers(access_token),
        query=query,
        raw_body=b"",
    )


def publish_container(access_token: str, creation_id: str) -> dict[str, Any]:
    return request_api_json(
        url=f"{PUBLISH_BASE}/me/threads_publish",
        method="POST",
        headers=bearer_headers(access_token),
        query={"creation_id": creation_id},
        raw_body=b"",
    )


def lookup_post(access_token: str, post_id: str, fields: str) -> dict[str, Any]:
    return request_api_json(
        url=f"{PUBLISH_BASE}/{post_id}",
        headers=bearer_headers(access_token),
        query={"fields": fields},
    )


def render_dry_run(
    *,
    text: str,
    text_source: dict[str, str],
    media_type: str,
    create_query: dict[str, Any],
    create_only: bool,
    auto_publish_text: bool,
) -> str:
    payload: dict[str, Any] = {
        "text_source": text_source,
        "media_type": media_type,
        "text_length": len(text),
        "create_request": {
            "method": "POST",
            "url": build_url(f"{PUBLISH_BASE}/me/threads", create_query),
            "query": create_query,
        },
    }
    if not create_only and not auto_publish_text:
        payload["publish_request"] = {
            "method": "POST",
            "url": build_url(f"{PUBLISH_BASE}/me/threads_publish", {"creation_id": "<creation_id>"}),
            "query": {"creation_id": "<creation_id>"},
        }
    return dump_json(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a Threads post from inline text, a file, or a saved snippet.")
    parser.add_argument("--access-token", default=os.environ.get("THREADS_ACCESS_TOKEN"), help="Threads user access token.")
    parser.add_argument("--text", help="Inline post text.")
    parser.add_argument("--text-file", help="Path to a plain text file to post.")
    parser.add_argument("--option", help="Named option from the snippets file, such as 'Post option 2' or just '2'.")
    parser.add_argument("--snippets-file", default=str(DEFAULT_SNIPPETS), help="Snippet file used with --option.")
    parser.add_argument("--list-options", action="store_true", help="List the available snippet titles and exit.")
    parser.add_argument("--image-url", help="Public image URL for an IMAGE post.")
    parser.add_argument("--video-url", help="Public video URL for a VIDEO post.")
    parser.add_argument("--alt-text", help="Optional alt text for IMAGE or VIDEO posts.")
    parser.add_argument("--link-attachment", help="Optional link attachment for a text post.")
    parser.add_argument("--reply-control", help="Optional reply control value accepted by the Threads API.")
    parser.add_argument("--reply-to-id", help="Optional parent Threads post ID for replies.")
    parser.add_argument("--topic-tag", help="Optional topic tag to attach to the post.")
    parser.add_argument("--location-id", help="Optional Threads location ID.")
    parser.add_argument("--enable-reply-approvals", action="store_true", help="Require reply approvals when the API permits it.")
    parser.add_argument("--ghost-post", action="store_true", help="Create the post as a ghost post when supported.")
    parser.add_argument("--captionless-media", action="store_true", help="Allow IMAGE or VIDEO posts with no text.")
    parser.add_argument("--create-only", action="store_true", help="Stop after creating the media container.")
    parser.add_argument("--auto-publish-text", action="store_true", help="Let Meta auto-publish a TEXT post without a second publish call.")
    parser.add_argument("--lookup-fields", default=DEFAULT_LOOKUP_FIELDS, help="Fields to fetch after publish. Ignored with --no-lookup.")
    parser.add_argument("--no-lookup", action="store_true", help="Skip the follow-up post details request.")
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved request(s) without calling the API.")
    parser.add_argument("--output", help="Optional file path for the JSON output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_options:
        rendered = describe_options(parse_post_options(args.snippets_file))
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    text, text_source = load_text(args)
    media_type = infer_media_type(args)
    validate_args(args, text, media_type)
    create_query = build_container_query(args, text, media_type)

    if args.dry_run:
        rendered = render_dry_run(
            text=text,
            text_source=text_source,
            media_type=media_type,
            create_query=create_query,
            create_only=args.create_only,
            auto_publish_text=args.auto_publish_text and media_type == "TEXT",
        )
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if not args.access_token:
        raise SystemExit("Missing Threads access token. Set THREADS_ACCESS_TOKEN or pass --access-token.")

    container = create_container(args.access_token, create_query)
    result: dict[str, Any] = {
        "text_source": text_source,
        "media_type": media_type,
        "container": container,
    }

    if args.create_only:
        rendered = dump_json(result)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if args.auto_publish_text and media_type == "TEXT":
        result["published"] = {
            "mode": "auto_publish_text",
            "note": "Meta was asked to publish automatically when the text container was created.",
        }
        rendered = dump_json(result)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    creation_id = container.get("id")
    if not creation_id:
        raise SystemExit("Meta did not return a creation container ID.")

    published = publish_container(args.access_token, str(creation_id))
    result["published"] = published

    post_id = published.get("id")
    if post_id and not args.no_lookup:
        result["details"] = lookup_post(args.access_token, str(post_id), args.lookup_fields)

    rendered = dump_json(result)
    print(rendered)
    maybe_write_output(args.output, rendered)


if __name__ == "__main__":
    main()
