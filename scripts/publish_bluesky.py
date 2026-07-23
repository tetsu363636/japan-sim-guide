#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from publish_utils import dump_json, maybe_write_output, request_api_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNIPPETS = ROOT / "outreach" / "snippets" / "bluesky-posts.txt"
DEFAULT_SERVICE = os.environ.get("BLUESKY_SERVICE", "https://bsky.social").rstrip("/")
DEFAULT_MAX_LENGTH = 300
TRAILING_URL_PUNCTUATION = b".,!?:;)]}"
URL_PATTERN = re.compile(rb"(https?://[^\s<>\"]+)")


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

    raise SystemExit(f"Unknown Bluesky option {option!r}. Run --list-options to see valid values.")


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


def normalize_langs(raw_langs: str | None) -> list[str]:
    if not raw_langs:
        return []
    return [item.strip() for item in raw_langs.split(",") if item.strip()]


def count_text_length(text: str) -> int:
    return len(text)


def build_link_facets(text: str) -> list[dict[str, Any]]:
    facets: list[dict[str, Any]] = []
    text_bytes = text.encode("utf-8")

    for match in re.finditer(URL_PATTERN, text_bytes):
        start = match.start(1)
        end = match.end(1)
        url_bytes = match.group(1)

        while url_bytes and url_bytes[-1:] in TRAILING_URL_PUNCTUATION:
            url_bytes = url_bytes[:-1]
            end -= 1

        if not url_bytes:
            continue

        facets.append(
            {
                "index": {"byteStart": start, "byteEnd": end},
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": url_bytes.decode("utf-8"),
                    }
                ],
            }
        )

    return facets


def now_utc_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_external_embed(
    *,
    url: str | None,
    title: str | None,
    description: str | None,
) -> dict[str, Any] | None:
    if not url:
        if title or description:
            raise SystemExit("--external-title and --external-description require --external-url.")
        return None

    if not title or not description:
        raise SystemExit("--external-url requires both --external-title and --external-description.")

    return {
        "$type": "app.bsky.embed.external",
        "external": {
            "uri": url,
            "title": title,
            "description": description,
        },
    }


def build_post_record(
    text: str,
    *,
    langs: list[str] | None = None,
    add_link_facets: bool = True,
    external_url: str | None = None,
    external_title: str | None = None,
    external_description: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": created_at or now_utc_z(),
    }

    if langs:
        record["langs"] = langs

    if add_link_facets:
        facets = build_link_facets(text)
        if facets:
            record["facets"] = facets

    embed = build_external_embed(
        url=external_url,
        title=external_title,
        description=external_description,
    )
    if embed:
        record["embed"] = embed

    return record


def build_create_payload(repo: str, record: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo": repo,
        "collection": "app.bsky.feed.post",
        "record": record,
    }


def resolve_pds_host(
    session: dict[str, Any],
    *,
    service: str = DEFAULT_SERVICE,
    explicit_pds_host: str | None = None,
) -> str:
    if explicit_pds_host:
        return explicit_pds_host.rstrip("/")

    did_doc = session.get("didDoc")
    if isinstance(did_doc, dict):
        for service_entry in did_doc.get("service", []):
            if not isinstance(service_entry, dict):
                continue
            endpoint = service_entry.get("serviceEndpoint")
            if not endpoint:
                continue
            entry_id = str(service_entry.get("id", ""))
            entry_type = str(service_entry.get("type", ""))
            if entry_id.endswith("#atproto_pds") or "PersonalDataServer" in entry_type:
                return str(endpoint).rstrip("/")

    return service.rstrip("/")


def create_session(identifier: str, app_password: str, *, service: str = DEFAULT_SERVICE) -> dict[str, Any]:
    return request_api_json(
        url=f"{service.rstrip('/')}/xrpc/com.atproto.server.createSession",
        method="POST",
        headers={"Accept": "application/json"},
        payload={
            "identifier": identifier,
            "password": app_password,
        },
    )


def create_post(
    *,
    access_token: str,
    pds_host: str,
    repo: str,
    record: dict[str, Any],
) -> dict[str, Any]:
    return request_api_json(
        url=f"{pds_host.rstrip('/')}/xrpc/com.atproto.repo.createRecord",
        method="POST",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        payload=build_create_payload(repo, record),
    )


def public_post_url(profile_id: str | None, at_uri: str | None) -> str | None:
    if not profile_id or not at_uri:
        return None

    parts = at_uri.split("/")
    if len(parts) < 5:
        return None
    rkey = parts[-1]
    return f"https://bsky.app/profile/{profile_id}/post/{rkey}"


def render_dry_run(
    *,
    text: str,
    text_source: dict[str, str],
    record: dict[str, Any],
    identifier: str | None,
    service: str,
    pds_host: str | None,
    max_length: int,
) -> str:
    payload = {
        "text_source": text_source,
        "text_length": count_text_length(text),
        "max_length": max_length,
        "auth_request": {
            "method": "POST",
            "url": f"{service.rstrip('/')}/xrpc/com.atproto.server.createSession",
            "payload": {
                "identifier": identifier or "<handle_or_did>",
                "password": "<app_password>",
            },
        },
        "create_request": {
            "method": "POST",
            "url": f"{(pds_host or '<resolved_pds_after_login>').rstrip('/')}/xrpc/com.atproto.repo.createRecord",
            "payload": build_create_payload(identifier or "<session.did>", record),
        },
    }
    return dump_json(payload)


def validate_args(args: argparse.Namespace, text: str) -> None:
    if args.list_options:
        return

    if not text:
        raise SystemExit("Pass --text, --text-file, or --option.")

    if count_text_length(text) > args.max_length:
        raise SystemExit(
            f"Bluesky text is {count_text_length(text)} characters, which exceeds the configured limit of {args.max_length}."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a Bluesky post with optional link facets and external card embed.")
    parser.add_argument("--identifier", default=os.environ.get("BLUESKY_HANDLE"), help="Bluesky handle or DID.")
    parser.add_argument(
        "--app-password",
        default=os.environ.get("BLUESKY_APP_PASSWORD"),
        help="Bluesky App Password. Use an app password, not your main account password.",
    )
    parser.add_argument(
        "--service",
        default=DEFAULT_SERVICE,
        help="Bluesky login host or entryway. Defaults to https://bsky.social.",
    )
    parser.add_argument(
        "--pds-host",
        default=os.environ.get("BLUESKY_PDS_HOST"),
        help="Optional direct PDS host. If omitted, the script uses the resolved PDS from the session when available.",
    )
    parser.add_argument("--text", help="Inline post text.")
    parser.add_argument("--text-file", help="Path to a plain text file to post.")
    parser.add_argument("--option", help="Named option from the snippets file, such as 'Post option 2' or just '2'.")
    parser.add_argument("--snippets-file", default=str(DEFAULT_SNIPPETS), help="Snippet file used with --option.")
    parser.add_argument("--list-options", action="store_true", help="List the available snippet titles and exit.")
    parser.add_argument("--langs", default="en", help="Comma-separated language tags for the post record.")
    parser.add_argument("--no-link-facets", action="store_true", help="Do not add Bluesky link facets for URLs found in the text.")
    parser.add_argument("--external-url", help="Optional URL for a Bluesky external card embed.")
    parser.add_argument("--external-title", help="Title used in the external card embed.")
    parser.add_argument("--external-description", help="Description used in the external card embed.")
    parser.add_argument(
        "--max-length",
        type=int,
        default=DEFAULT_MAX_LENGTH,
        help="Preflight length limit for the text field. Bluesky currently documents a 300-character limit.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved API requests without calling Bluesky.")
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
    validate_args(args, text)
    langs = normalize_langs(args.langs)
    record = build_post_record(
        text,
        langs=langs,
        add_link_facets=not args.no_link_facets,
        external_url=args.external_url,
        external_title=args.external_title,
        external_description=args.external_description,
    )

    if args.dry_run:
        rendered = render_dry_run(
            text=text,
            text_source=text_source,
            record=record,
            identifier=args.identifier,
            service=args.service,
            pds_host=args.pds_host,
            max_length=args.max_length,
        )
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if not args.identifier:
        raise SystemExit("Missing Bluesky identifier. Set BLUESKY_HANDLE or pass --identifier.")
    if not args.app_password:
        raise SystemExit("Missing Bluesky App Password. Set BLUESKY_APP_PASSWORD or pass --app-password.")

    session = create_session(args.identifier, args.app_password, service=args.service)
    pds_host = resolve_pds_host(session, service=args.service, explicit_pds_host=args.pds_host)
    repo = str(session.get("did") or args.identifier)
    created = create_post(
        access_token=str(session["accessJwt"]),
        pds_host=pds_host,
        repo=repo,
        record=record,
    )

    payload: dict[str, Any] = {
        "platform": "bluesky",
        "text_source": text_source,
        "text": text,
        "text_length": count_text_length(text),
        "record": record,
        "session": {
            "handle": session.get("handle"),
            "did": session.get("did"),
            "pds_host": pds_host,
        },
        "created": created,
    }
    post_url = public_post_url(str(session.get("handle") or session.get("did") or ""), str(created.get("uri") or ""))
    if post_url:
        payload["public_url"] = post_url

    rendered = dump_json(payload)
    print(rendered)
    maybe_write_output(args.output, rendered)


if __name__ == "__main__":
    main()
