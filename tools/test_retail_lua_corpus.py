#!/usr/bin/env python3
"""Mutation tests for the restricted decoded-Lua corpus contract."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import private_lua_corpus as corpus  # noqa: E402
import verify_retail_lua_corpus as verifier  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "manifests" / "private_lua_corpus.json"
SCHEMA = REPO / "schemas" / "private_lua_corpus.schema.json"
ATTESTATION_SCHEMA = REPO / "schemas" / "retail_lua_corpus_attestation.schema.json"
VERIFY = REPO / "tools" / "verify_retail_lua_corpus.py"
WORKFLOW = REPO / ".github" / "workflows" / "retail-checks.yml"
CHECKS_WORKFLOW = REPO / ".github" / "workflows" / "checks.yml"
PASSED: list[str] = []
FAILED: list[str] = []


def check(label: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(label)


def write_json(path: Path, value: object, *, canonical: bool = False) -> None:
    if canonical:
        raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    else:
        raw = json.dumps(value, ensure_ascii=True, indent=2)
    path.write_text(raw + "\n", encoding="ascii", newline="")


def run_verifier(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFY), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def workflow_job(workflow: str, job_id: str) -> str:
    lines = workflow.splitlines()
    marker = f"  {job_id}:"
    try:
        start = lines.index(marker)
    except ValueError:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("  ") and not line.startswith("    ") and line.endswith(":"):
            end = index
            break
    return "\n".join(lines[start:end])


def contract_tests(root: Path) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    schema = json.loads(SCHEMA.read_text(encoding="ascii"))
    check(
        "Lua grant schema pins the check",
        schema.get("properties", {}).get("checkId", {}).get("const")
        == verifier.CHECK_ID,
    )
    check("Lua grant passes exact contract", not verifier.contract_errors())
    for field in (
        ("source", "commit"),
        ("archive", "bytes"),
        ("archive", "sha256"),
        ("expanded", "fileCount"),
        ("expanded", "totalBytes"),
        ("expanded", "treeSha256"),
    ):
        mutated = copy.deepcopy(manifest)
        value = mutated[field[0]][field[1]]
        mutated[field[0]][field[1]] = value + 1 if isinstance(value, int) else "0" * len(value)
        path = root / ("mutated-" + "-".join(field) + ".json")
        write_json(path, mutated)
        check("mutated " + "/".join(field) + " fails", bool(verifier.contract_errors(path)))


def archive_logic_tests(root: Path) -> None:
    expected = corpus.CorpusSummary(
        verifier.EXPANDED_FILE_COUNT,
        verifier.EXPANDED_TOTAL_BYTES,
        verifier.EXPANDED_TREE_SHA256,
    )
    check("canonical expanded shape passes", not verifier._shape_errors(expected))
    check(
        "mutated expanded count fails",
        bool(verifier._shape_errors(corpus.CorpusSummary(expected.file_count + 1, expected.total_bytes, expected.tree_sha256))),
    )
    check(
        "mutated expanded bytes fail",
        bool(verifier._shape_errors(corpus.CorpusSummary(expected.file_count, expected.total_bytes + 1, expected.tree_sha256))),
    )
    check(
        "mutated expanded tree fails",
        bool(verifier._shape_errors(corpus.CorpusSummary(expected.file_count, expected.total_bytes, "0" * 64))),
    )
    short = root / "short.zip"
    short.write_bytes(b"x")
    check("archive size mutation fails", bool(verifier.archive_errors(short)))
    original_size = verifier.ARCHIVE_SIZE
    try:
        verifier.ARCHIVE_SIZE = 1
        check("archive hash mutation fails", bool(verifier.archive_errors(short)))
    finally:
        verifier.ARCHIVE_SIZE = original_size


def output_tests(root: Path) -> None:
    schema = json.loads(ATTESTATION_SCHEMA.read_text(encoding="ascii"))
    attestation = verifier.build_attestation("pass", "1" * 40)
    check(
        "attestation schema pins the approved hash",
        schema.get("properties", {}).get("approvedInputSha256", {}).get("const")
        == verifier.ARCHIVE_SHA256,
    )
    check("pass attestation satisfies contract", not verifier.attestation_errors(attestation))
    extra = copy.deepcopy(attestation)
    extra["archive"] = "forbidden"
    check("attestation additional field fails", bool(verifier.attestation_errors(extra)))
    zero = copy.deepcopy(attestation)
    zero["publicRepositoryCommit"] = "0" * 40
    check("attestation zero commit fails", bool(verifier.attestation_errors(zero)))

    failed = run_verifier("--archive", str(root / "missing.zip"))
    try:
        document = json.loads(failed.stdout)
    except json.JSONDecodeError:
        document = {}
    check("missing archive exits nonzero", failed.returncode != 0)
    check(
        "failure output is sanitized",
        set(document)
        == {
            "schemaVersion",
            "publicRepositoryCommit",
            "approvedInputSha256",
            "toolVersions",
            "check",
            "result",
        }
        and document.get("result", {}).get("status") == "fail"
        and "missing.zip" not in failed.stdout
        and "missing.zip" not in failed.stderr,
    )
    first = run_verifier("--check-contract")
    second = run_verifier("--check-contract")
    check(
        "contract attestations are deterministic",
        first.returncode == second.returncode == 0 and first.stdout == second.stdout,
    )
    check("attestation uses LF", first.stdout.endswith("\n") and "\r" not in first.stdout)

    retained = root / "retained"
    retained.mkdir()
    write_json(retained / verifier.ATTESTATION_FILENAME, attestation, canonical=True)
    check("one retained attestation passes", not verifier.retained_output_errors(retained))
    (retained / "extra.log").write_text("forbidden\n", encoding="ascii")
    check("extra retained output fails", bool(verifier.retained_output_errors(retained)))


def workflow_tests() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    checks = CHECKS_WORKFLOW.read_text(encoding="utf-8")
    lua_job = workflow_job(workflow, "lua-corpus")
    check("Lua corpus retail job exists", bool(lua_job))
    check(
        "Lua fetch pins approved archive",
        f"commit: {verifier.SOURCE_COMMIT}" in lua_job
        and f"path: {verifier.SOURCE_PATH}" in lua_job
        and f"size: {verifier.ARCHIVE_SIZE}" in lua_job
        and f"sha256: {verifier.ARCHIVE_SHA256}" in lua_job,
    )
    check(
        "Lua job hydrates an external root",
        "XIVL_LUA_SCRIPTS_DIR=" in lua_job
        and "private_lua_corpus.py hydrate" in lua_job
        and "verify_retail_lua_corpus.py" in lua_job,
    )
    check(
        "normal checks stay asset-free",
        "XIVL_CORPUS_ABSENT" in checks
        and verifier.SOURCE_PATH not in checks
        and "test_private_lua_corpus.py" in checks
        and "test_retail_lua_corpus.py" in checks,
    )
    check(
        "retail artifacts retain attestations only",
        lua_job.count("path: _retail-staging/retail-evidence-attestation.json") == 1
        and "path: _retail-staging/" not in lua_job.replace(
            "path: _retail-staging/retail-evidence-attestation.json", ""
        ),
    )


def optional_archive_test() -> None:
    configured = os.environ.get("XIVL_PRIVATE_LUA_ARCHIVE")
    if not configured:
        check("restricted archive is optional in normal tests", True)
        return
    check(
        "explicit restricted archive passes",
        run_verifier("--archive", configured).returncode == 0,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="retail-lua-corpus-test-") as raw:
        root = Path(raw)
        contract_tests(root)
        archive_logic_tests(root)
        output_tests(root)
    workflow_tests()
    optional_archive_test()
    if FAILED:
        print("FAIL: " + "; ".join(FAILED))
        return 1
    print(f"PASS: {len(PASSED)} retail Lua corpus checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
