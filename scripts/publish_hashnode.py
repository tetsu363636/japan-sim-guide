#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from typing import Any

from publish_utils import dump_json, load_markdown_asset, maybe_write_output, normalize_tags, request_json, slugify


HASHNODE_URL = "https://gql.hashnode.com/"


def build_tag_payloads(raw_tags: Any) -> list[dict[str, str]]:
    payloads = []
    for tag in normalize_tags(raw_tags):
        payloads.append({"name": tag, "slug": slugify(tag)})
    return payloads


def build_input(metadata: dict[str, Any], body: str, args: argparse.Namespace) -> dict[str, Any]:
    post_input: dict[str, Any] = {
        "title": args.title or metadata["title"],
        "publicationId": args.publication_id,
        "contentMarkdown": body,
    }

    if subtitle := args.subtitle or metadata.get("subtitle"):
        post_input["subtitle"] = subtitle
    if slug := args.slug or metadata.get("slug"):
        post_input["slug"] = slug
    if canonical := args.canonical_url or metadata.get("canonical_url"):
        post_input["originalArticleURL"] = canonical
    if publish_as := args.publish_as or metadata.get("publish_as"):
        post_input["publishAs"] = publish_as
    if series_id := args.series_id or metadata.get("series_id"):
        post_input["seriesId"] = series_id

    tags = build_tag_payloads(args.tags or metadata.get("tags"))
    if tags:
        post_input["tags"] = tags

    if image := args.cover_image or metadata.get("cover_image"):
        post_input["coverImageOptions"] = {"coverImageURL": image}

    return post_input


def build_operation(post_input: dict[str, Any], publish: bool) -> dict[str, Any]:
    if publish:
        query = """
        mutation PublishPost($input: PublishPostInput!) {
          publishPost(input: $input) {
            post {
              id
              slug
              url
              title
              canonicalUrl
            }
          }
        }
        """
    else:
        query = """
        mutation CreateDraft($input: CreateDraftInput!) {
          createDraft(input: $input) {
            draft {
              id
              slug
              title
              canonicalUrl
            }
          }
        }
        """
    return {"query": query, "variables": {"input": post_input}}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a draft or publish a post on Hashnode.")
    parser.add_argument("--file", required=True, help="Markdown file with simple front matter.")
    parser.add_argument("--publication-id", required=True, help="Target Hashnode publication ID.")
    parser.add_argument("--api-key", default=os.environ.get("HASHNODE_PAT"), help="Hashnode personal access token.")
    parser.add_argument("--publish", action="store_true", help="Publish immediately instead of creating a draft.")
    parser.add_argument("--title")
    parser.add_argument("--subtitle")
    parser.add_argument("--slug")
    parser.add_argument("--canonical-url")
    parser.add_argument("--cover-image")
    parser.add_argument("--tags", help="Comma-separated override.")
    parser.add_argument("--publish-as", help="Optional member ObjectId for team publications.")
    parser.add_argument("--series-id", help="Optional series ObjectId.")
    parser.add_argument("--dry-run", action="store_true", help="Print the GraphQL operation without hitting the API.")
    parser.add_argument("--output", help="Optional file path for payload or API response.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata, body = load_markdown_asset(args.file)
    post_input = build_input(metadata, body, args)
    operation = build_operation(post_input, publish=args.publish)

    if args.dry_run:
        rendered = dump_json(operation)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    if not args.api_key:
        raise SystemExit("Missing Hashnode PAT. Set HASHNODE_PAT or pass --api-key.")

    response = request_json(
        url=HASHNODE_URL,
        headers={
            "Authorization": args.api_key,
            "Content-Type": "application/json",
        },
        payload=operation,
    )
    rendered = dump_json(response)
    print(rendered)
    maybe_write_output(args.output, rendered)


if __name__ == "__main__":
    main()
