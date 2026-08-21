#!/usr/bin/env python3
"""Mutation and fixture tests for the retail BattleCommandBaseClass lane."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import retail_script  # noqa: E402
import verify_retail_script as verifier  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
JAR = REPO / "tools" / "vendor" / "unluac" / "unluac_2025_12_23.jar"
LICENSE = REPO / "tools" / "vendor" / "unluac" / "LICENSE.txt"
INPUTS = REPO / "manifests" / "retail_inputs.json"
CHECK = REPO / "manifests" / "retail_battle_command_check.json"
WORKFLOW = REPO / ".github" / "workflows" / "retail-checks.yml"
PASS_KEYS = {
    "schemaVersion", "publicRepositoryCommit", "approvedInputSha256",
    "toolVersions", "check", "result",
}
PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def _load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO / "tools" / "verify_retail_script.py"), *args],
        cwd=REPO, capture_output=True, text=True, check=False,
    )


def _fixture_check(
    decoded_bytes: int,
    decoded_hash: str,
    script_bytes: int,
    script_hash: str,
    script_lines: int,
) -> dict:
    document = copy.deepcopy(_load(CHECK))
    assert isinstance(document, dict)
    document["decoded"] = {"bytes": decoded_bytes, "sha256": decoded_hash}
    document["script"] = {
        "bytes": script_bytes,
        "sha256": script_hash,
        "lineCount": script_lines,
    }
    return document


def main() -> int:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    check(
        "artifact upload requires cleanup and allowlist success",
        "steps.cleanup.outcome == 'success' && steps.allowlist.outcome == 'success'"
        in workflow,
    )
    check(
        "retained-file allowlist scans the full tree",
        "find _retail-staging -mindepth 1 -print" in workflow,
    )
    check(
        "preflight job and remote-main lookup are bounded",
        "timeout-minutes: 10" in workflow
        and "timeout 30s git ls-remote origin refs/heads/main" in workflow,
    )
    check(
        "hosted Python patch is pinned",
        workflow.count('python-version: "3.12.14"') == 2,
    )
    python_commands = [
        line for line in workflow.splitlines()
        if "python" in line
        and "python-version" not in line
        and "setup-python" not in line
    ]
    check(
        "every hosted Python command is bounded",
        bool(python_commands) and all("timeout " in line for line in python_commands),
    )
    check("vendor JAR size is pinned", JAR.is_file() and JAR.stat().st_size == 796256)
    check(
        "vendor JAR hash is pinned",
        JAR.is_file()
        and hashlib.sha256(JAR.read_bytes()).hexdigest()
        == "98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc",
    )
    license_bytes = LICENSE.read_bytes() if LICENSE.is_file() else b""
    check("vendor license is the embedded MIT notice", license_bytes.startswith(b"Copyright (c) 2011-2020 tehtmi\r\n"))
    check("vendor license names both authors", b"Thomas Klaeger" in license_bytes)

    clear = b"\x1bLuaQ\x00\x01\x04\x04\x04\x08\x00"
    check("rlu wrapper fixture decodes", retail_script.decode_lpb(b"rlu\x0b" + b"\x00" * 4 + clear) == clear)
    encoded = bytes(value ^ 0x73 for value in clear[:3])
    encoded_body = bytes(value ^ 0x73 for value in clear[3:])
    check(
        "rle wrapper fixture decodes",
        retail_script.decode_lpb(b"rle\x0c" + b"\x00" * 9 + encoded + encoded_body)
        == clear,
    )
    check("unknown wrapper fails closed", retail_script.decode_lpb(b"unknown") is None)
    check("filename cipher fixture", retail_script.encode_filename("ZoneMoveProgTest") == "kvw5xvo5usv3q5rq")
    check("filename cipher involution", retail_script.encode_filename(retail_script.encode_filename("Man0g0")) == "man0g0")

    canonical = b"a\r\nb\r\n"
    check("CRLF canonicalization is exact", retail_script.canonicalize_unluac(canonical) == b"a\nb\n")
    regression = b"A" * 2389 + b"\n" * 144
    raw_windows = regression.replace(b"\n", b"\r\n")
    check("Windows unluac regression sizes", len(raw_windows) == 2677 and len(regression) == 2533)
    check("Windows unluac regression canonicalizes", retail_script.canonicalize_unluac(raw_windows) == regression)

    with tempfile.TemporaryDirectory(prefix="retail-script-pipeline-test-") as raw:
        root = Path(raw)
        source = root / "fixture.le.lpb"
        source.write_bytes(b"rlu\x0b" + b"\x00" * 4 + clear)

        def fake_unluac(_jar: Path, _decoded: Path, output: Path, timeout: int = 120) -> None:
            del timeout
            output.write_bytes(b"fixture\r\n")

        with patch.object(retail_script, "run_unluac", fake_unluac):
            retail_script.reproduce(source, root / "tool.jar", root / "one.luac", root / "one.lua")
            retail_script.reproduce(source, root / "tool.jar", root / "two.luac", root / "two.lua")
        check("two synthetic pipeline runs are byte-identical", (root / "one.luac").read_bytes() == (root / "two.luac").read_bytes() and (root / "one.lua").read_bytes() == (root / "two.lua").read_bytes())

    decoded = b"\x1bLuaQ" + bytes(range(256)) * 5 + b"tail"
    decoded_hash = hashlib.sha256(decoded).hexdigest()
    with tempfile.TemporaryDirectory(prefix="retail-script-test-") as raw:
        root = Path(raw)
        decoded_path = root / "decoded.luac"
        decoded_path.write_bytes(decoded)
        script = b"fixture one\nfixture two\n"
        script_hash = hashlib.sha256(script).hexdigest()
        script_path = root / "canonical.lua"
        script_path.write_bytes(script)
        expected_path = root / "expected.json"
        expected_path.write_text(
            json.dumps(_fixture_check(len(decoded), decoded_hash, len(script), script_hash, 2)),
            encoding="utf-8",
        )
        with patch.object(verifier, "DECODED_BYTES", len(decoded)), \
             patch.object(verifier, "DECODED_SHA256", decoded_hash), \
             patch.object(verifier, "SCRIPT_BYTES", len(script)), \
             patch.object(verifier, "SCRIPT_SHA256", script_hash), \
             patch.object(verifier, "SCRIPT_LINES", 2), \
             patch.object(verifier, "_tracked_metadata_errors", return_value=[]):
            errors = verifier.verify(decoded_path, script_path, check_manifest_path=expected_path)
            check("canonical synthetic reproduction passes", not errors)

            mutated = bytearray(decoded)
            mutated[-1] ^= 1
            decoded_path.write_bytes(mutated)
            check("decoded byte mutation fails", bool(verifier.verify(decoded_path, script_path, check_manifest_path=expected_path)))
            decoded_path.write_bytes(decoded)

            mutated_script = root / "mutated.lua"
            script_bytes = script_path.read_bytes()
            mutated_script.write_bytes(script_bytes[:-1] + bytes([script_bytes[-1] ^ 1]))
            check("canonical script byte mutation fails", bool(verifier.verify(decoded_path, mutated_script, check_manifest_path=expected_path)))

            bad_check = _fixture_check(len(decoded), decoded_hash, len(script), script_hash, 2)
            bad_check["calls"]["_getData"] = [75, 81, 88]
            bad_path = root / "bad-check.json"
            bad_path.write_text(json.dumps(bad_check), encoding="utf-8")
            check("expected call metadata mutation fails", bool(verifier.verify(decoded_path, script_path, check_manifest_path=bad_path)))
            bad_hash = _fixture_check(len(decoded), decoded_hash, len(script), script_hash, 2)
            bad_hash["script"]["sha256"] = "0" * 64
            bad_hash_path = root / "bad-hash-check.json"
            bad_hash_path.write_text(json.dumps(bad_hash), encoding="utf-8")
            check("expected hash mutation fails", bool(verifier.verify(decoded_path, script_path, check_manifest_path=bad_hash_path)))

        first = _run_cli("--contract-only")
        second = _run_cli("--contract-only")
        check("contract-only invocation passes", first.returncode == second.returncode == 0)
        check("repeated contract attestations are byte-identical", first.stdout.encode() == second.stdout.encode())
        raw = subprocess.run(
            [
                sys.executable,
                str(REPO / "tools" / "verify_retail_script.py"),
                "--contract-only",
            ],
            cwd=REPO,
            capture_output=True,
            text=False,
            check=False,
        )
        check(
            "contract attestation has a literal LF terminator",
            raw.returncode == 0
            and raw.stdout.endswith(b"\n")
            and b"\r" not in raw.stdout,
        )
        try:
            attestation = json.loads(first.stdout)
        except json.JSONDecodeError:
            attestation = {}
        check("attestation has only approved fields", set(attestation) == PASS_KEYS)
        check("attestation records pass", attestation.get("result", {}).get("status") == "pass")
        check("passing attestation satisfies schema", not verifier.attestation_errors(attestation))
        zero_commit = copy.deepcopy(attestation)
        zero_commit["publicRepositoryCommit"] = "0" * 40
        check("all-zero public commit is rejected", bool(verifier.attestation_errors(zero_commit)))
        attestation["decoded"] = "not retained"
        check("attestation extra body field is rejected", bool(verifier.attestation_errors(attestation)))

        with patch.object(verifier.subprocess, "run", side_effect=OSError):
            try:
                verifier._git_commit()
            except verifier.VerificationError:
                git_failed_closed = True
            else:
                git_failed_closed = False
        check("git commit lookup fails closed", git_failed_closed)

        failed = _run_cli("--decoded", str(root / "missing.luac"), "--script", str(root / "missing.lua"))
        try:
            failed_output = json.loads(failed.stdout)
        except json.JSONDecodeError:
            failed_output = {}
        check("failure invocation exits nonzero", failed.returncode != 0)
        check("failure attestation stays sanitized", set(failed_output) == PASS_KEYS and failed_output.get("result", {}).get("status") == "fail")
        check("failure output contains no body marker", "LuaQ" not in failed.stdout and "observations" not in failed.stdout)

    if FAILED:
        print("FAIL: " + "; ".join(FAILED))
        return 1
    print(f"PASS: {len(PASSED)} retail script verification checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
