#!/usr/bin/env python3
"""Verify the fixed restricted decoded-Lua corpus contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import private_lua_corpus as corpus  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO / "manifests" / "private_lua_corpus.json"
SOURCE_MANIFEST = REPO / "manifests" / "scripts.json"
ATTESTATION_FILENAME = "retail-evidence-attestation.json"

CHECK_ID = "decoded-lua-corpus-v1"
INPUT_ID = "decoded-lua-corpus-1.23b"
SOURCE_REPOSITORY = "XIVLegacy/xivl-private-assets"
SOURCE_COMMIT = "40006d5d716583d78690a6f3ef50ca1bc41dddee"
SOURCE_PATH = "extracted/ffxiv-1.23b/client-scripts/lua.zip"
ARCHIVE_PATH = "lua.zip"
ARCHIVE_SIZE = 14385427
ARCHIVE_SHA256 = "0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31"
EXPANDED_FILE_COUNT = 2671
EXPANDED_TOTAL_BYTES = 13971401
EXPANDED_TREE_SHA256 = "05edcf81aec7ad28007c059991b6858665680f860bd1ed2aa5100e7fc120da0d"
TARGET = "lua/scripts"
SCHEMA_VERSION = 1
TOOL_VERSIONS = {"python": "3.12", "verifier": "1.0"}


class VerificationError(Exception):
    """An input or output failed closed without exposing its contents."""


EXPECTED_MANIFEST = {
    "schemaVersion": SCHEMA_VERSION,
    "inputId": INPUT_ID,
    "checkId": CHECK_ID,
    "target": TARGET,
    "source": {
        "repository": SOURCE_REPOSITORY,
        "commit": SOURCE_COMMIT,
        "path": SOURCE_PATH,
    },
    "archive": {
        "path": ARCHIVE_PATH,
        "bytes": ARCHIVE_SIZE,
        "sha256": ARCHIVE_SHA256,
    },
    "expanded": {
        "fileCount": EXPANDED_FILE_COUNT,
        "totalBytes": EXPANDED_TOTAL_BYTES,
        "treeSha256": EXPANDED_TREE_SHA256,
    },
}


def _read_json(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError("JSON duplicate field")
            result[key] = value
        return result

    try:
        return json.loads(
            path.read_text(encoding="ascii"), object_pairs_hook=reject_duplicates
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise VerificationError("JSON input unreadable") from exc


def contract_errors(manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    try:
        manifest = _read_json(manifest_path)
    except VerificationError:
        return ["restricted Lua grant is unreadable"]
    return [] if manifest == EXPECTED_MANIFEST else ["restricted Lua grant drifted"]


def _is_link_or_reparse(path: Path) -> bool:
    try:
        is_junction = getattr(os.path, "isjunction", lambda value: False)
        return path.is_symlink() or is_junction(path)
    except OSError:
        return True


def _archive_identity_errors(archive_path: Path) -> list[str]:
    try:
        result = archive_path.lstat()
    except OSError:
        return ["restricted archive identity check failed"]
    if _is_link_or_reparse(archive_path) or not stat.S_ISREG(result.st_mode):
        return ["restricted archive identity check failed"]
    if result.st_size != ARCHIVE_SIZE:
        return ["restricted archive identity check failed"]
    digest = hashlib.sha256()
    try:
        with archive_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
    except OSError:
        return ["restricted archive identity check failed"]
    return (
        []
        if digest.hexdigest() == ARCHIVE_SHA256
        else ["restricted archive identity check failed"]
    )


def _shape_errors(summary: corpus.CorpusSummary) -> list[str]:
    if (
        summary.file_count != EXPANDED_FILE_COUNT
        or summary.total_bytes != EXPANDED_TOTAL_BYTES
        or summary.tree_sha256 != EXPANDED_TREE_SHA256
    ):
        return ["restricted archive shape differs"]
    return []


def archive_errors(archive_path: Path) -> list[str]:
    errors = _archive_identity_errors(archive_path)
    if errors:
        return errors
    try:
        summary = corpus.verify_package(archive_path, SOURCE_MANIFEST)
    except (corpus.CorpusError, OSError, RuntimeError, ValueError):
        return ["restricted archive validation failed"]
    return _shape_errors(summary)


def verify(archive_path: Path | None, manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    errors = contract_errors(manifest_path)
    if archive_path is not None:
        errors.extend(archive_errors(archive_path))
    return errors


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise VerificationError("public commit unavailable") from exc
    commit = result.stdout.strip()
    if (
        len(commit) != 40
        or any(char not in "0123456789abcdef" for char in commit)
        or commit == "0" * 40
    ):
        raise VerificationError("public commit unavailable")
    return commit


def build_attestation(status: str, public_commit: str | None = None) -> dict[str, Any]:
    if status not in {"pass", "fail"}:
        raise ValueError("attestation status invalid")
    commit = public_commit if public_commit is not None else _git_commit()
    if (
        len(commit) != 40
        or any(char not in "0123456789abcdef" for char in commit)
        or commit == "0" * 40
    ):
        raise ValueError("public commit invalid")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "publicRepositoryCommit": commit,
        "approvedInputSha256": ARCHIVE_SHA256,
        "toolVersions": dict(TOOL_VERSIONS),
        "check": {"id": CHECK_ID, "version": 1},
        "result": {"status": status},
    }


def attestation_errors(document: Any) -> list[str]:
    """Apply the closed sanitized attestation contract without dependencies."""
    if not isinstance(document, dict):
        return ["attestation is not an object"]
    expected_keys = {
        "schemaVersion",
        "publicRepositoryCommit",
        "approvedInputSha256",
        "toolVersions",
        "check",
        "result",
    }
    if set(document) != expected_keys:
        return ["attestation fields drifted"]
    commit = document.get("publicRepositoryCommit")
    if (
        document.get("schemaVersion") != SCHEMA_VERSION
        or not isinstance(commit, str)
        or len(commit) != 40
        or commit == "0" * 40
        or any(char not in "0123456789abcdef" for char in commit)
        or document.get("approvedInputSha256") != ARCHIVE_SHA256
        or document.get("toolVersions") != TOOL_VERSIONS
        or document.get("check") != {"id": CHECK_ID, "version": 1}
        or document.get("result") not in ({"status": "pass"}, {"status": "fail"})
    ):
        return ["attestation values drifted"]
    return []


def retained_output_errors(directory: Path) -> list[str]:
    try:
        if _is_link_or_reparse(directory) or not directory.is_dir():
            return ["retained output root invalid"]
        entries = list(directory.iterdir())
        if len(entries) != 1 or entries[0].name != ATTESTATION_FILENAME:
            return ["retained output allowlist differs"]
        path = entries[0]
        if _is_link_or_reparse(path) or not path.is_file() or path.stat().st_size > 4096:
            return ["retained attestation file invalid"]
        raw = path.read_bytes()
        if b"\r" in raw:
            return ["retained attestation line ending invalid"]
        document = json.loads(raw.decode("ascii"))
        canonical = (
            json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("ascii")
        if raw != canonical:
            return ["retained attestation serialization invalid"]
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return ["retained attestation unreadable"]
    return attestation_errors(document)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check-contract", action="store_true")
    parser.add_argument("--validate-retained-output", type=Path)
    return parser.parse_args(argv)


def _emit_attestation(status: str) -> None:
    document = build_attestation(status)
    if attestation_errors(document):
        raise VerificationError("attestation schema rejected output")
    payload = (
        json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    sys.stdout.buffer.write(payload)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.validate_retained_output is not None:
        errors = retained_output_errors(args.validate_retained_output)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1 if errors else 0

    errors = verify(args.archive, args.manifest)
    if args.archive is None and not args.check_contract:
        errors.append("restricted archive is required")
    try:
        _emit_attestation("pass" if not errors else "fail")
    except (VerificationError, ValueError):
        print("ERROR: attestation could not be built", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
