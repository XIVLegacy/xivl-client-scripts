#!/usr/bin/env python3
"""Publish the Lua corpus or regenerate its N-API annotations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _corpus import annotate_corpus, build_script_manifest, publish_corpus, write_json

SCRIPTS_ROOT = Path("lua/scripts")
REGISTRY_PATH = Path("lua/registry.json")
API_INDEX_PATH = Path("data/vendor/client-structs/lua_api_index.json")
NAPI_INDEX_PATH = Path("lua/napi_index.json")
MANIFEST_PATH = Path("manifests/scripts.json")


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

    annotate = commands.add_parser(
        "annotate",
        help="Regenerate sidecars and the N-API inverted index.",
    )

    manifest = commands.add_parser(
        "manifest",
        help="Build the canonical script reproduction manifest.",
    )

    args = parser.parse_args()
    if args.command == "publish":
        return publish_corpus(
            args.lua_root,
            args.output_root,
        )
    if args.command == "annotate":
        return annotate_corpus(
            SCRIPTS_ROOT,
            REGISTRY_PATH,
            API_INDEX_PATH,
            NAPI_INDEX_PATH,
        )
    if not SCRIPTS_ROOT.is_dir():
        print(f"error: {SCRIPTS_ROOT} not found", file=sys.stderr)
        return 1
    try:
        contract = build_script_manifest(SCRIPTS_ROOT)
        write_json(MANIFEST_PATH, contract)
    except (OSError, UnicodeError) as exc:
        print(f"error: manifest generation failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {contract['scriptCount']} script hashes to {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
