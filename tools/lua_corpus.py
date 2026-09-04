#!/usr/bin/env python3
"""Publish the Lua corpus or regenerate its N-API annotations."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _corpus import (
    CorpusRootError,
    annotate_corpus,
    build_script_manifest,
    publish_corpus,
    resolve_scripts_root,
    validate_scripts_root,
    write_json,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "lua" / "scripts"
REGISTRY_PATH = REPO_ROOT / "lua" / "registry.json"
API_INDEX_PATH = REPO_ROOT / "data" / "vendor" / "client-structs" / "lua_api_index.json"
NAPI_INDEX_PATH = REPO_ROOT / "lua" / "napi_index.json"
MANIFEST_PATH = REPO_ROOT / "manifests" / "scripts.json"


def _add_scripts_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--scripts-root",
        type=Path,
        help=(
            "directory containing decoded .lua files (default: lua/scripts, "
            "or XIVL_LUA_SCRIPTS_DIR)"
        ),
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

    annotate = commands.add_parser(
        "annotate",
        help="Regenerate sidecars and the N-API inverted index.",
    )
    _add_scripts_root(annotate)

    manifest = commands.add_parser(
        "manifest",
        help="Build the canonical script reproduction manifest.",
    )
    _add_scripts_root(manifest)

    args = parser.parse_args()
    if args.command == "publish":
        return publish_corpus(
            args.lua_root,
            args.output_root,
        )
    scripts_root = resolve_scripts_root(SCRIPTS_ROOT, args.scripts_root)
    try:
        validate_scripts_root(scripts_root)
    except CorpusRootError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.command == "annotate":
        return annotate_corpus(
            scripts_root,
            REGISTRY_PATH,
            API_INDEX_PATH,
            NAPI_INDEX_PATH,
            SCRIPTS_ROOT,
        )
    try:
        contract = build_script_manifest(scripts_root)
        write_json(MANIFEST_PATH, contract)
    except (OSError, UnicodeError, CorpusRootError) as exc:
        print(f"error: manifest generation failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {contract['scriptCount']} script hashes to {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
