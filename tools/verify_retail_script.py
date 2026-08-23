#!/usr/bin/env python3
"""Verify the bounded BattleCommandBaseClass script observation contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
INPUT_MANIFEST = REPO / "manifests" / "retail_inputs.json"
CHECK_MANIFEST = REPO / "manifests" / "retail_battle_command_check.json"
REGISTRY = REPO / "lua" / "registry.json"
CALLS = REPO / "lua" / "scripts" / "command" / "game" / "battlecommandbaseclass.calls.json"

CHECK_ID = "battle-command-baseclass-v1"
INPUT_ID = "battle-command-baseclass-lpb-1.23b"
INPUT_SHA256 = "74761459950b4dbafab6c879ea9a4c1437d4bfe8084058be2023e32add32e569"
INPUT_FILENAME = "89qqy57vxx9w689r57y9rr.le.lpb"
INPUT_SIZE = 1507
PRIVATE_REPOSITORY = "XIVLegacy/xivl-private-assets"
PRIVATE_COMMIT = "aeb52f6dbde95a793ee6d52be28de9f28a885b15"
PRIVATE_PATH = "client-scripts/ffxiv-1.23b/client/script/7vxx9w6/39x5/89qqy57vxx9w689r57y9rr.le.lpb"
SOURCE_NAME = "command/game/battlecommandbaseclass"
CIPHERED_PATH = "7vxx9w6/39x5/89qqy57vxx9w689r57y9rr.lua"
DECODED_BYTES = 1494
DECODED_SHA256 = "95d29680ba473e0090a3a90573d38e7ce13a9ca63759c7f846bc8a9e5fa83eb0"
SCRIPT_BYTES = 2533
SCRIPT_SHA256 = "0eb0b8c77b05128461d94ca1a9bee9b65bccf397ab8efd60903c448915d1e757"
SCRIPT_LINES = 144
METHODS = [
    "isBattleCommand",
    "getCommandType",
    "canAimForRelation",
    "getCommandTargettingMode",
    "canFireForRelation",
    "canAimParts",
    "getCommandRangeCode",
    "getRangeAngle",
    "useWeaponRangeInformation",
    "isLongRangeCommand",
]
REGISTRY_FIELDS = {
    "classes": ["BattleCommandBaseClass"],
    "methods": METHODS,
    "requires": ["/Command/Game/GameCommandBaseClass"],
}
CALL_FIELDS = {"_defineBaseClass": [5], "_getData": [75, 81, 87]}
ROOT_ATTESTATION_KEYS = frozenset({
    "schemaVersion", "publicRepositoryCommit", "approvedInputSha256",
    "toolVersions", "check", "result",
})


class VerificationError(Exception):
    """Malformed verification input."""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("verification document malformed") from exc


def _expected_input_manifest() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "inputs": [{
            "id": INPUT_ID,
            "filename": INPUT_FILENAME,
            "size": INPUT_SIZE,
            "sha256": INPUT_SHA256,
            "source": {
                "repository": PRIVATE_REPOSITORY,
                "commit": PRIVATE_COMMIT,
                "path": PRIVATE_PATH,
            },
            "allowedChecks": [CHECK_ID],
        }],
    }


def _expected_check_manifest() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "checkId": CHECK_ID,
        "approvedInputId": INPUT_ID,
        "approvedInputSha256": INPUT_SHA256,
        "sourceName": SOURCE_NAME,
        "cipheredPath": CIPHERED_PATH,
        "decoded": {"bytes": DECODED_BYTES, "sha256": DECODED_SHA256},
        "script": {"bytes": SCRIPT_BYTES, "sha256": SCRIPT_SHA256, "lineCount": SCRIPT_LINES},
        "registry": REGISTRY_FIELDS,
        "calls": CALL_FIELDS,
    }


def _retail_contract_errors(
    input_manifest: Any, check_manifest: Any,
) -> list[str]:
    errors: list[str] = []
    if input_manifest != _expected_input_manifest():
        errors.append("retail input grant drifted")
    if check_manifest != _expected_check_manifest():
        errors.append("retail script check contract drifted")
    return errors


def _tracked_metadata_errors() -> list[str]:
    errors: list[str] = []
    try:
        registry = _read_json(REGISTRY)
        entry = registry["scripts"][SOURCE_NAME]
    except (KeyError, TypeError, VerificationError):
        return ["tracked registry entry unavailable"]
    for field, expected in REGISTRY_FIELDS.items():
        if entry.get(field) != expected:
            errors.append(f"tracked registry {field} drifted")
    if entry.get("ciphered") != CIPHERED_PATH:
        errors.append("tracked registry ciphered path drifted")
    if entry.get("lineCount") != SCRIPT_LINES:
        errors.append("tracked registry line count drifted")
    try:
        calls = _read_json(CALLS)
    except VerificationError:
        return errors + ["tracked call sidecar unavailable"]
    expected_calls = {
        "decoded": SOURCE_NAME,
        "ciphered": CIPHERED_PATH,
        "classes": REGISTRY_FIELDS["classes"],
        "lineCount": SCRIPT_LINES,
        "apiCount": 2,
        "callsiteCount": 4,
        "apis": CALL_FIELDS,
    }
    if calls != expected_calls:
        errors.append("tracked call sidecar drifted")
    return errors


def verify(
    decoded_path: Path | None = None,
    script_path: Path | None = None,
    *,
    check_manifest_path: Path = CHECK_MANIFEST,
    contract_only: bool = False,
) -> list[str]:
    """Return fixed-label errors; no input payload or diagnostics are emitted."""
    try:
        input_manifest = _read_json(INPUT_MANIFEST)
        check_manifest = _read_json(check_manifest_path)
    except VerificationError:
        return ["retail contract document malformed"]
    errors = _retail_contract_errors(input_manifest, check_manifest)
    errors.extend(_tracked_metadata_errors())
    if contract_only:
        return errors
    if decoded_path is None or script_path is None:
        return errors + ["reproduction outputs missing"]
    try:
        decoded = decoded_path.read_bytes()
        script = script_path.read_bytes()
    except OSError:
        return errors + ["reproduction outputs unreadable"]
    if len(decoded) != DECODED_BYTES:
        errors.append("decoded chunk size drifted")
    if hashlib.sha256(decoded).hexdigest() != DECODED_SHA256:
        errors.append("decoded chunk hash drifted")
    if not decoded.startswith(b"\x1bLuaQ"):
        errors.append("decoded chunk is not Lua 5.1")
    if len(script) != SCRIPT_BYTES:
        errors.append("canonical script size drifted")
    if hashlib.sha256(script).hexdigest() != SCRIPT_SHA256:
        errors.append("canonical script hash drifted")
    if b"\r\n" in script:
        errors.append("canonical script has CRLF bytes")
    try:
        if len(script.decode("utf-8").splitlines()) != SCRIPT_LINES:
            errors.append("canonical script line count drifted")
    except UnicodeDecodeError:
        errors.append("canonical script is not UTF-8")
    return errors


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, check=True,
            capture_output=True, text=True, timeout=10,
        )
        commit = result.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise VerificationError("public commit unavailable") from exc
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None or commit == "0" * 40:
        raise VerificationError("public commit unavailable")
    return commit


def build_attestation(status: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "publicRepositoryCommit": _git_commit(),
        "approvedInputSha256": INPUT_SHA256,
        "toolVersions": {
            "jdk": "21.0.12.1+1",
            "unluac": "2025_12_23",
            "verifier": "1.0",
        },
        "check": {"id": CHECK_ID, "version": 1},
        "result": {"status": status},
    }


def attestation_errors(document: Any) -> list[str]:
    """Apply the attestation schema's closed, sanitized field contract."""
    if not isinstance(document, dict) or set(document) != ROOT_ATTESTATION_KEYS:
        return ["attestation shape drifted"]
    if document.get("schemaVersion") != 1:
        return ["attestation schema version drifted"]
    commit = document.get("publicRepositoryCommit")
    if (
        not isinstance(commit, str)
        or re.fullmatch(r"[0-9a-f]{40}", commit) is None
        or commit == "0" * 40
    ):
        return ["attestation public commit malformed"]
    if document.get("approvedInputSha256") != INPUT_SHA256:
        return ["attestation input identity drifted"]
    if document.get("toolVersions") != {
        "jdk": "21.0.12.1+1",
        "unluac": "2025_12_23",
        "verifier": "1.0",
    }:
        return ["attestation tool versions drifted"]
    if document.get("check") != {"id": CHECK_ID, "version": 1}:
        return ["attestation check identity drifted"]
    if document.get("result") not in ({"status": "pass"}, {"status": "fail"}):
        return ["attestation result drifted"]
    return []


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decoded", type=Path, default=None)
    parser.add_argument("--script", type=Path, default=None)
    parser.add_argument("--check", type=Path, default=CHECK_MANIFEST)
    parser.add_argument("--contract-only", action="store_true")
    parser.add_argument("--validate-attestation", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.validate_attestation is not None:
        try:
            errors = attestation_errors(_read_json(args.validate_attestation))
        except VerificationError:
            errors = ["attestation document malformed"]
        if errors:
            print("retail attestation validation failed", file=sys.stderr)
            return 1
        print("retail attestation schema passed")
        return 0
    errors = verify(
        args.decoded,
        args.script,
        check_manifest_path=args.check,
        contract_only=args.contract_only,
    )
    status = "pass" if not errors else "fail"
    try:
        attestation = build_attestation(status)
    except VerificationError:
        print("retail public commit unavailable", file=sys.stderr)
        return 1
    payload = json.dumps(
        attestation, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii") + b"\n"
    sys.stdout.buffer.write(payload)
    if errors:
        print(f"retail script verification failed ({len(errors)} fixed checks)", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
