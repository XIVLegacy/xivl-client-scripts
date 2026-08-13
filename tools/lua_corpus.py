#!/usr/bin/env python3
"""Publish the Lua corpus or regenerate its N-API annotations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _corpus import annotate_corpus, build_script_manifest, publish_corpus, write_json


def _add_strictness(parser: argparse.ArgumentParser, noun: str) -> None:
    parser.add_argument(
        "--lenient",
        action="store_true",
        help=f"Warn and skip an unreadable {noun}; strict by default.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    publish = commands.add_parser(
        "publish",
        help="Build the registry and publish decoded scripts atomically.",
    )
    publish.add_argument(
        "--lua-root",
        type=Path,
        required=True,
        help="Explicit ciphered decompile output tree.",
    )
    publish.add_argument(
        "--output-root",
        type=Path,
        default=Path("lua"),
        help="Directory containing registry.json and scripts/ (default: lua).",
    )
    _add_strictness(publish, "source script")

    annotate = commands.add_parser(
        "annotate",
        help="Regenerate sidecars and the N-API inverted index.",
    )
    annotate.add_argument("--scripts-root", type=Path, default=Path("lua/scripts"))
    annotate.add_argument("--registry", type=Path, default=Path("lua/registry.json"))
    annotate.add_argument(
        "--api-index",
        type=Path,
        default=Path("data/vendor/client-structs/lua_api_index.json"),
    )
    annotate.add_argument("--index-out", type=Path, default=Path("lua/napi_index.json"))
    _add_strictness(annotate, "published script")

    manifest = commands.add_parser(
        "manifest",
        help="Build the canonical script reproduction manifest.",
    )
    manifest.add_argument("--scripts-root", type=Path, default=Path("lua/scripts"))
    manifest.add_argument(
        "--output",
        type=Path,
        default=Path("manifests/scripts.json"),
    )

    args = parser.parse_args()
    if args.command == "publish":
        return publish_corpus(
            args.lua_root,
            args.output_root,
            strict=not args.lenient,
        )
    if args.command == "annotate":
        return annotate_corpus(
            args.scripts_root,
            args.registry,
            args.api_index,
            args.index_out,
            strict=not args.lenient,
        )
    if not args.scripts_root.is_dir():
        print(f"error: {args.scripts_root} not found", file=sys.stderr)
        return 1
    try:
        contract = build_script_manifest(args.scripts_root)
        write_json(args.output, contract)
    except (OSError, UnicodeError) as exc:
        print(f"error: manifest generation failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {contract['scriptCount']} script hashes to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
