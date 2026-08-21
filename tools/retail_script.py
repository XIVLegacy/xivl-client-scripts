#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Decode one retail LPB and run the pinned unluac decompiler.

The decoder is adapted under MIT terms from
XIVLegacy/xivl-client-structs tools/decode_lpb.py at commit
708e6b76802e897e2bc91bc138799f454b747e73. It keeps the byte-producing stages
separate so a caller can place both intermediate files below one mode-0700
temporary root and remove them unconditionally.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


class RetailScriptError(Exception):
    """A fixed-stage failure safe to report without payload or path details."""


def decode_lpb(data: bytes) -> bytes | None:
    """Decode an FFXIV ``.le.lpb`` wrapper to Lua 5.1 bytecode."""
    if data[:4] == b"rlu\x0b":
        return data[8:] if len(data) >= 8 else None
    if data[:4] == b"rle\x0c":
        if len(data) < 16:
            return None
        prefix = bytes(value ^ 0x73 for value in data[13:16])
        body = bytes(value ^ 0x73 for value in data[16:])
        return prefix + body
    return None


def encode_filename(name: str) -> str:
    """Apply the shipped script filename substitution cipher."""
    result: list[str] = []
    for char in name.lower():
        if char.isalpha():
            position = ord(char) - ord("a") + 1
            if position <= 10:
                result.append(str(10 - position))
            else:
                result.append(chr(ord("a") + (37 - position) - 1))
        elif char.isdigit():
            result.append(chr(ord("a") + (10 - int(char)) - 1))
        else:
            result.append(char)
    return "".join(result)


def canonicalize_unluac(data: bytes) -> bytes:
    """Apply the repository's exact CRLF-pair-to-LF rule."""
    return data.replace(b"\r\n", b"\n")


def run_unluac(jar: Path, decoded: Path, script_out: Path, timeout: int = 120) -> None:
    """Run Java unluac without exposing its output or diagnostics."""
    try:
        result = subprocess.run(
            ["java", "-jar", str(jar), str(decoded)],
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RetailScriptError("unluac stage failed") from exc
    if result.returncode != 0:
        raise RetailScriptError("unluac stage failed")
    try:
        script_out.parent.mkdir(parents=True, exist_ok=True)
        script_out.write_bytes(canonicalize_unluac(result.stdout))
    except OSError as exc:
        raise RetailScriptError("script output stage failed") from exc


def reproduce(input_path: Path, jar: Path, decoded_out: Path, script_out: Path) -> None:
    """Run the bounded decode/decompile pipeline with no payload logging."""
    try:
        source = input_path.read_bytes()
    except OSError as exc:
        raise RetailScriptError("LPB input stage failed") from exc
    decoded = decode_lpb(source)
    if decoded is None or not decoded.startswith(b"\x1bLuaQ"):
        raise RetailScriptError("LPB decode stage failed")
    try:
        decoded_out.parent.mkdir(parents=True, exist_ok=True)
        decoded_out.write_bytes(decoded)
    except OSError as exc:
        raise RetailScriptError("decoded output stage failed") from exc
    run_unluac(jar, decoded_out, script_out)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--decoded-out", type=Path, required=True)
    parser.add_argument("--script-out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        reproduce(args.input, args.jar, args.decoded_out, args.script_out)
    except RetailScriptError:
        print("retail script reproduction failed", file=sys.stderr)
        return 1
    print("LPB decode and unluac stages passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
