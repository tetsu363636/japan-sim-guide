#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re

from publish_utils import build_url, dump_json, maybe_write_output, request_api_json


GRAPH_BASE = os.environ.get("THREADS_GRAPH_BASE", "https://graph.threads.net").rstrip("/")
AUTH_BASE = os.environ.get("THREADS_AUTH_BASE", "https://threads.net/oauth/authorize")
DEFAULT_SCOPES = "threads_basic,threads_content_publish"
DEFAULT_PROFILE_FIELDS = "id,username,name,threads_profile_picture_url,threads_biography"


def parse_scopes(raw: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"[\s,]+", raw) if part.strip()]
    if not parts:
        raise SystemExit("At least one scope is required.")
    return parts


def bearer_headers(access_token: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }


def build_auth_url(client_id: str, redirect_uri: str, scopes: list[str], state: str | None) -> str:
    query = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": ",".join(scopes),
    }
    if state:
        query["state"] = state
    return build_url(AUTH_BASE, query)


def exchange_code_for_token(
    *,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    code: str,
) -> dict[str, object]:
    return request_api_json(
        url=f"{GRAPH_BASE}/oauth/access_token",
        method="POST",
        headers={"Accept": "application/json"},
        query={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
        raw_body=b"",
    )


def exchange_long_lived_token(*, client_secret: str, access_token: str) -> dict[str, object]:
    return request_api_json(
        url=f"{GRAPH_BASE}/access_token",
        headers=bearer_headers(access_token),
        query={
            "grant_type": "th_exchange_token",
            "client_secret": client_secret,
        },
    )


def refresh_long_lived_token(access_token: str) -> dict[str, object]:
    response = request_api_json(
        url=f"{GRAPH_BASE}/refresh_access_token",
        headers=bearer_headers(access_token),
        query={"grant_type": "th_refresh_token"},
    )
    if response:
        return response
    return {
        "access_token": access_token,
        "refreshed": True,
        "note": "The refresh endpoint returned an empty body, so keep using the same token unless Meta explicitly returns a replacement.",
    }


def get_profile(access_token: str, fields: str) -> dict[str, object]:
    return request_api_json(
        url=f"{GRAPH_BASE}/me",
        headers=bearer_headers(access_token),
        query={"fields": fields},
    )


def write_result(result: str, output: str | None) -> None:
    print(result)
    maybe_write_output(output, result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Meta Threads auth helpers for token bootstrap and refresh.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_url = subparsers.add_parser("auth-url", help="Build the manual OAuth URL to open in a browser.")
    auth_url.add_argument("--client-id", default=os.environ.get("THREADS_APP_ID"), help="Meta app ID.")
    auth_url.add_argument("--redirect-uri", default=os.environ.get("THREADS_REDIRECT_URI"), help="Redirect URI configured in the Meta app.")
    auth_url.add_argument("--scopes", default=os.environ.get("THREADS_SCOPES", DEFAULT_SCOPES), help="Comma- or space-separated scopes.")
    auth_url.add_argument("--state", help="Optional CSRF state value.")
    auth_url.add_argument("--output", help="Optional file path for the rendered URL.")

    exchange_code = subparsers.add_parser("exchange-code", help="Exchange an authorization code for a short-lived token.")
    exchange_code.add_argument("--client-id", default=os.environ.get("THREADS_APP_ID"), help="Meta app ID.")
    exchange_code.add_argument("--client-secret", default=os.environ.get("THREADS_APP_SECRET"), help="Meta app secret.")
    exchange_code.add_argument("--redirect-uri", default=os.environ.get("THREADS_REDIRECT_URI"), help="Redirect URI configured in the Meta app.")
    exchange_code.add_argument("--code", required=True, help="Authorization code returned to the redirect URI.")
    exchange_code.add_argument("--long-lived", action="store_true", help="Immediately exchange the short-lived token for a long-lived one.")
    exchange_code.add_argument("--output", help="Optional file path for the JSON response.")

    exchange_long = subparsers.add_parser("exchange-long-lived", help="Exchange a short-lived token for a long-lived token.")
    exchange_long.add_argument("--client-secret", default=os.environ.get("THREADS_APP_SECRET"), help="Meta app secret.")
    exchange_long.add_argument("--access-token", default=os.environ.get("THREADS_ACCESS_TOKEN"), help="Short-lived Threads user access token.")
    exchange_long.add_argument("--output", help="Optional file path for the JSON response.")

    refresh = subparsers.add_parser("refresh-token", help="Refresh a long-lived Threads user access token.")
    refresh.add_argument("--access-token", default=os.environ.get("THREADS_ACCESS_TOKEN"), help="Long-lived Threads user access token.")
    refresh.add_argument("--output", help="Optional file path for the JSON response.")

    profile = subparsers.add_parser("profile", help="Fetch the current Threads profile tied to the token.")
    profile.add_argument("--access-token", default=os.environ.get("THREADS_ACCESS_TOKEN"), help="Threads user access token.")
    profile.add_argument("--fields", default=DEFAULT_PROFILE_FIELDS, help="Comma-separated profile fields.")
    profile.add_argument("--output", help="Optional file path for the JSON response.")

    return parser.parse_args()


def require_arg(value: str | None, message: str) -> str:
    if value:
        return value
    raise SystemExit(message)


def main() -> None:
    args = parse_args()

    if args.command == "auth-url":
        url = build_auth_url(
            client_id=require_arg(args.client_id, "Missing Threads app ID. Set THREADS_APP_ID or pass --client-id."),
            redirect_uri=require_arg(args.redirect_uri, "Missing redirect URI. Set THREADS_REDIRECT_URI or pass --redirect-uri."),
            scopes=parse_scopes(args.scopes),
            state=args.state,
        )
        write_result(url, args.output)
        return

    if args.command == "exchange-code":
        short_lived = exchange_code_for_token(
            client_id=require_arg(args.client_id, "Missing Threads app ID. Set THREADS_APP_ID or pass --client-id."),
            client_secret=require_arg(args.client_secret, "Missing Threads app secret. Set THREADS_APP_SECRET or pass --client-secret."),
            redirect_uri=require_arg(args.redirect_uri, "Missing redirect URI. Set THREADS_REDIRECT_URI or pass --redirect-uri."),
            code=args.code,
        )
        response: dict[str, object] = {"short_lived": short_lived}
        if args.long_lived:
            short_token = short_lived.get("access_token")
            if not short_token:
                raise SystemExit("Meta did not return a short-lived access token.")
            response["long_lived"] = exchange_long_lived_token(
                client_secret=require_arg(args.client_secret, "Missing Threads app secret. Set THREADS_APP_SECRET or pass --client-secret."),
                access_token=str(short_token),
            )
        write_result(dump_json(response), args.output)
        return

    if args.command == "exchange-long-lived":
        response = exchange_long_lived_token(
            client_secret=require_arg(args.client_secret, "Missing Threads app secret. Set THREADS_APP_SECRET or pass --client-secret."),
            access_token=require_arg(args.access_token, "Missing Threads access token. Set THREADS_ACCESS_TOKEN or pass --access-token."),
        )
        write_result(dump_json(response), args.output)
        return

    if args.command == "refresh-token":
        response = refresh_long_lived_token(
            require_arg(args.access_token, "Missing Threads access token. Set THREADS_ACCESS_TOKEN or pass --access-token.")
        )
        write_result(dump_json(response), args.output)
        return

    if args.command == "profile":
        response = get_profile(
            access_token=require_arg(args.access_token, "Missing Threads access token. Set THREADS_ACCESS_TOKEN or pass --access-token."),
            fields=args.fields,
        )
        write_result(dump_json(response), args.output)
        return

    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
