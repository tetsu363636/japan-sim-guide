#!/usr/bin/env python3
from __future__ import annotations

import argparse

from publish_utils import dump_json, maybe_write_output, request_json


HASHNODE_URL = "https://gql.hashnode.com/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Look up a Hashnode publication ID from its host.")
    parser.add_argument("--host", required=True, help="Publication host, e.g. blog.example.com or yourblog.hashnode.dev.")
    parser.add_argument("--dry-run", action="store_true", help="Print the GraphQL operation instead of calling Hashnode.")
    parser.add_argument("--output", help="Optional file path for the operation or response.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    operation = {
        "query": """
        query PublicationByHost($host: String!) {
          publication(host: $host) {
            id
            title
            url
          }
        }
        """,
        "variables": {"host": args.host},
    }

    if args.dry_run:
        rendered = dump_json(operation)
        print(rendered)
        maybe_write_output(args.output, rendered)
        return

    response = request_json(
        url=HASHNODE_URL,
        headers={"Content-Type": "application/json"},
        payload=operation,
    )
    rendered = dump_json(response)
    print(rendered)
    maybe_write_output(args.output, rendered)


if __name__ == "__main__":
    main()

