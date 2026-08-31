#!/usr/bin/env python3
"""Validate corpus artifacts and the documentation index."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from _corpus import (
    decode_path,
    extract_signals,
    load_api_index,
    scan_binding_declarations,
    scan_script,
)
from myplayer_timer_consumers import (
    AnalysisError as TimerConsumerAnalysisError,
    analyze as analyze_timer_consumers,
    render_json as render_timer_consumers,
)
from quest_selector_consumers import (
    AnalysisError as QuestSelectorAnalysisError,
    analyze_script_consumers,
    validate_retained as validate_quest_selector_report,
)
from retail_lua_coverage import (
    TOOLS_COMMIT,
    TOOLS_SOURCES,
    sha256_file,
    sidecar_inventory,
    validate_report,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = REPO_ROOT / "schemas"
LUA_DIR = REPO_ROOT / "lua"
DOCS_DIR = REPO_ROOT / "docs"
MANIFESTS_DIR = REPO_ROOT / "manifests"
VENDOR_DIR = REPO_ROOT / "data" / "vendor" / "client-structs"
RETAIL_VENDOR_DIR = REPO_ROOT / "tools" / "vendor" / "unluac"
CORPUS_ABSENT = os.environ.get("XIVL_CORPUS_ABSENT") == "1"
PERMITTED_TOP_LEVEL_GROUPS = {
    "root",
    ".github",
    "data",
    "docs",
    "lua",
    "manifests",
    "schemas",
    "tools",
}
REQUIRED_AGENT_TOOLING_IGNORE_LINES = {
    "# Agent / AI tooling",
    ".claude/",
    ".agents/",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/ai_agents/local/",
}
EXPECTED_SCRIPT_COUNT = 2671
ABSOLUTE_MAINTAINER_PATH_RE = re.compile(
    rb"(?:[A-Za-z]:\\" + rb"Users\\|/" + rb"Users/|/" + rb"home/)",
    re.IGNORECASE,
)
PRIVATE_REFERENCE_TOKENS = (
    # Split the tokens so this validator does not match its own source text.
    b"must stay " + b"private",
    b"private " + b"repository",
    b"private " + b"repositories",
    b"repository is " + b"private",
)

try:
    import jsonschema  # noqa: PLC0415

    _HAVE_JSONSCHEMA = True
except ImportError:
    _HAVE_JSONSCHEMA = False

errors: list[str] = []


def _tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return sorted(path for path in result.stdout.decode("utf-8").split("\0") if path)


def validate_repository_boundary() -> list[str]:
    """Enforce the public tree and reject restricted or local content."""
    paths = _tracked_paths()
    for path in paths:
        group = path.split("/", 1)[0] if "/" in path else "root"
        if group not in PERMITTED_TOP_LEVEL_GROUPS:
            errors.append(f"unexpected top-level tracked group: {path}")

    for path in paths:
        lower = path.lower()
        if lower.startswith("lua/scripts/") and lower.endswith(".lua"):
            errors.append(f"forbidden tracked Lua corpus path: {path}")
        data = (REPO_ROOT / path).read_bytes()
        if data[:2] == b"MZ":
            errors.append(f"PE MZ magic in tracked file: {path}")
        if ABSOLUTE_MAINTAINER_PATH_RE.search(data):
            errors.append(f"absolute maintainer path in tracked file: {path}")
        if any(token in data.lower() for token in PRIVATE_REFERENCE_TOKENS):
            errors.append(f"private-reference token in tracked file: {path}")

    ignore_text = (
        (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        .replace("\r\n", "\n")
    )
    ignore_lines = set(ignore_text.split("\n"))
    for required in sorted(REQUIRED_AGENT_TOOLING_IGNORE_LINES):
        if required not in ignore_lines:
            errors.append(f".gitignore missing required line: {required}")
    return paths


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_all_json(paths: list[str]) -> int:
    """Parse every tracked JSON file."""
    json_paths = [REPO_ROOT / path for path in paths if path.endswith(".json")]
    failures: list[str] = []
    for path in json_paths:
        try:
            _load(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            label = path.relative_to(REPO_ROOT).as_posix()
            failures.append(f"{label}: cannot parse JSON: {exc}")
    if failures:
        errors.extend(failures)
        return len(json_paths)
    print(f"Validated {len(json_paths)} JSON files.")
    return len(json_paths)


def run_focused_tests() -> bool:
    """Run the focused tool tests as part of the single repository gate."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(REPO_ROOT / "tools" / "tests"),
            "-p",
            "test_*.py",
        ],
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode != 0:
        print(
            f"error: focused tool tests failed (exit {result.returncode})",
            file=sys.stderr,
        )
        return False
    retail = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "test_retail_script.py")],
        cwd=REPO_ROOT,
        check=False,
    )
    if retail.returncode != 0:
        print(
            f"error: retail script contract tests failed (exit {retail.returncode})",
            file=sys.stderr,
        )
        return False
    return True


def _validator_for(schema_path: Path):
    return jsonschema.Draft202012Validator(_load(schema_path))


def _check(instance, validator, label: str) -> None:
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{label}: schema violation at {loc}: {err.message}")


SIDECAR_SUFFIX = ".calls.json"


def load_sidecars() -> dict[str, dict]:
    """Load sidecars once for cross-file checks."""
    scripts_root = LUA_DIR / "scripts"
    if not scripts_root.is_dir():
        return {}
    return {
        p.relative_to(scripts_root).as_posix()[: -len(SIDECAR_SUFFIX)]: _load(p)
        for p in sorted(scripts_root.rglob("*" + SIDECAR_SUFFIX))
    }


def validate_schemas(sidecars: dict[str, dict]) -> None:
    pairs = [
        (
            MANIFESTS_DIR / "scripts.json",
            "lua_scripts_manifest.schema.json",
            "manifests/scripts.json",
        ),
        (LUA_DIR / "registry.json", "lua_registry.schema.json", "lua/registry.json"),
        (LUA_DIR / "napi_index.json", "lua_napi_index.schema.json", "lua/napi_index.json"),
        (
            MANIFESTS_DIR / "retail_lua_coverage.json",
            "retail_lua_coverage.schema.json",
            "manifests/retail_lua_coverage.json",
        ),
        (
            MANIFESTS_DIR / "myplayer_timer_consumers.json",
            "myplayer_timer_consumers.schema.json",
            "manifests/myplayer_timer_consumers.json",
        ),
        (
            MANIFESTS_DIR / "quest_selector_consumers.json",
            "quest_selector_consumers.schema.json",
            "manifests/quest_selector_consumers.json",
        ),
    ]
    for inst_path, schema_name, label in pairs:
        schema_path = SCHEMAS / schema_name
        if not inst_path.is_file():
            errors.append(f"{label}: file missing")
            continue
        if not schema_path.is_file():
            errors.append(f"{label}: schema {schema_name} missing")
            continue
        _check(_load(inst_path), _validator_for(schema_path), label)

    retail_pairs = [
        (
            MANIFESTS_DIR / "retail_inputs.json",
            "retail-inputs.schema.json",
            "manifests/retail_inputs.json",
        ),
        (
            MANIFESTS_DIR / "retail_battle_command_check.json",
            "retail-script-check.schema.json",
            "manifests/retail_battle_command_check.json",
        ),
    ]
    attestation_path = (
        MANIFESTS_DIR / "retail_evidence" / "battle-command-baseclass.json"
    )
    if attestation_path.is_file():
        retail_pairs.append((
            attestation_path,
            "retail-evidence-attestation.schema.json",
            "manifests/retail_evidence/battle-command-baseclass.json",
        ))
    for inst_path, schema_name, label in retail_pairs:
        schema_path = SCHEMAS / schema_name
        if not inst_path.is_file():
            errors.append(f"{label}: file missing")
        elif not schema_path.is_file():
            errors.append(f"{label}: schema {schema_name} missing")
        else:
            _check(_load(inst_path), _validator_for(schema_path), label)

    calls_schema = SCHEMAS / "lua_script_calls.schema.json"
    if not calls_schema.is_file():
        errors.append(
            "lua sidecars: schema lua_script_calls.schema.json missing"
        )
    elif sidecars:
        validator = _validator_for(calls_schema)
        for key, sidecar in sidecars.items():
            _check(sidecar, validator, f"lua/scripts/{key}{SIDECAR_SUFFIX}")


def validate_retail_lua_coverage() -> None:
    """Verify retained census claims without requiring local retail bytes."""
    coverage_path = MANIFESTS_DIR / "retail_lua_coverage.json"
    manifest_path = MANIFESTS_DIR / "scripts.json"
    registry_path = LUA_DIR / "registry.json"
    if not all(path.is_file() for path in (coverage_path, manifest_path, registry_path)):
        return
    coverage = _load(coverage_path)
    manifest = _load(manifest_path)
    registry = _load(registry_path)
    for problem in validate_report(coverage, manifest, registry):
        errors.append(f"manifests/retail_lua_coverage.json: {problem}")

    corpus = coverage.get("corpus", {})
    expected_corpus = {
        "manifest": "manifests/scripts.json",
        "manifestSha256": sha256_file(manifest_path),
        "registry": "lua/registry.json",
        "registrySha256": sha256_file(registry_path),
        "scriptCount": len(manifest.get("scripts", [])),
    }
    sidecar_count, sidecar_digest = sidecar_inventory()
    expected_corpus.update(
        {
            "sidecarCount": sidecar_count,
            "sidecarInventorySha256": sidecar_digest,
        }
    )
    if corpus != expected_corpus:
        errors.append(
            "manifests/retail_lua_coverage.json: corpus pins disagree with tracked inputs"
        )

    expected_tool = {
        "repository": "XIVLegacy/xivl-tools",
        "commit": TOOLS_COMMIT,
        "sources": [
            {"path": path, "sha256": digest}
            for path, digest in TOOLS_SOURCES.items()
        ],
    }
    if coverage.get("tool") != expected_tool:
        errors.append(
            "manifests/retail_lua_coverage.json: xivl-tools pin disagrees with generator"
        )


def validate_myplayer_timer_consumers() -> None:
    """Verify the retained timer-consumer report and its corpus pins."""
    report_path = MANIFESTS_DIR / "myplayer_timer_consumers.json"
    if not report_path.is_file():
        return
    report = _load(report_path)
    corpus = report.get("corpus", {})
    expected_pins = {
        "manifest": "manifests/scripts.json",
        "manifestSha256": hashlib.sha256(
            (MANIFESTS_DIR / "scripts.json").read_bytes()
        ).hexdigest(),
        "registry": "lua/registry.json",
        "registrySha256": hashlib.sha256(
            (LUA_DIR / "registry.json").read_bytes()
        ).hexdigest(),
        "napiIndex": "lua/napi_index.json",
        "napiIndexSha256": hashlib.sha256(
            (LUA_DIR / "napi_index.json").read_bytes()
        ).hexdigest(),
        "scriptCount": EXPECTED_SCRIPT_COUNT,
    }
    if corpus != expected_pins:
        errors.append(
            "manifests/myplayer_timer_consumers.json: corpus pins disagree with tracked inputs"
        )
    if CORPUS_ABSENT:
        return
    try:
        rebuilt = analyze_timer_consumers()
    except (OSError, UnicodeError, json.JSONDecodeError, TimerConsumerAnalysisError) as exc:
        errors.append(f"manifests/myplayer_timer_consumers.json: analysis failed: {exc}")
        return
    if render_timer_consumers(rebuilt) != report_path.read_bytes():
        errors.append("manifests/myplayer_timer_consumers.json: generated report is stale")


def validate_quest_selector_consumers() -> None:
    """Verify retained selector evidence and local script callsites."""
    report_path = MANIFESTS_DIR / "quest_selector_consumers.json"
    if not report_path.is_file():
        return
    report = _load(report_path)
    for problem in validate_quest_selector_report(report):
        errors.append(f"manifests/quest_selector_consumers.json: {problem}")
    if CORPUS_ABSENT:
        return
    try:
        consumers = analyze_script_consumers()
    except (OSError, UnicodeError, QuestSelectorAnalysisError) as exc:
        errors.append(
            f"manifests/quest_selector_consumers.json: analysis failed: {exc}"
        )
        return
    if report.get("messageConsumers") != consumers:
        errors.append(
            "manifests/quest_selector_consumers.json: message consumers are stale"
        )


def validate_reproduction_contract(sidecars: dict[str, dict]) -> None:
    """Validate manifest metadata and, when supplied, every corpus byte."""
    manifest_path = MANIFESTS_DIR / "scripts.json"
    registry_path = LUA_DIR / "registry.json"
    if not manifest_path.is_file() or not registry_path.is_file():
        return
    manifest = _load(manifest_path)
    registry = _load(registry_path)
    rows = manifest.get("scripts", [])
    if not isinstance(rows, list):
        return
    if manifest.get("scriptCount") != len(rows):
        errors.append(
            f"manifests/scripts.json: scriptCount {manifest.get('scriptCount')} "
            f"!= {len(rows)} rows"
        )
    if len(rows) != EXPECTED_SCRIPT_COUNT:
        errors.append(
            f"manifests/scripts.json: expected {EXPECTED_SCRIPT_COUNT} rows, "
            f"got {len(rows)}"
        )
    expected_pipeline = {
        "orchestrator": "XIVLegacy/xivl-client-structs:tools/lpb_pipeline.py",
        "decoder": "XIVLegacy/xivl-client-structs:tools/decode_lpb.py",
        "decompiler": "user-supplied unluac.jar",
        "canonicalization": "replace CRLF byte pairs with LF",
    }
    if manifest.get("pipeline") != expected_pipeline:
        errors.append("manifests/scripts.json: pipeline identity changed")

    paths = [row.get("relativePath") for row in rows if isinstance(row, dict)]
    if paths != sorted(paths):
        errors.append("manifests/scripts.json: rows are not sorted by relativePath")
    if len(paths) != len(set(paths)):
        errors.append("manifests/scripts.json: duplicate relativePath rows")
    manifest_keys = {
        path[len("lua/scripts/") : -len(".lua")]
        for path in paths
        if isinstance(path, str)
        and path.startswith("lua/scripts/")
        and path.endswith(".lua")
    }
    registry_keys = set(registry.get("scripts", {}))
    sidecar_keys = set(sidecars)
    for label, keys in (
        ("registry", registry_keys),
        ("sidecars", sidecar_keys),
    ):
        missing = manifest_keys - keys
        extra = keys - manifest_keys
        if missing or extra:
            errors.append(
                f"manifests/scripts.json: {label} key mismatch "
                f"({len(missing)} manifest-only, {len(extra)} {label}-only)"
            )

    scripts_root = LUA_DIR / "scripts"
    local_files = sorted(scripts_root.rglob("*.lua")) if scripts_root.is_dir() else []
    if CORPUS_ABSENT:
        if local_files:
            errors.append(
                "corpus absence declaration: found local .lua files while "
                "XIVL_CORPUS_ABSENT=1"
            )
        return
    if not local_files:
        errors.append(
            "local Lua corpus missing; supply lua/scripts/*.lua or set "
            "XIVL_CORPUS_ABSENT=1 for a public-tree-only gate"
        )
        return

    by_path = {
        row["relativePath"]: row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("relativePath"), str)
    }
    on_disk = {
        path.relative_to(REPO_ROOT).as_posix(): path for path in local_files
    }
    for path in sorted(set(by_path) - set(on_disk)):
        errors.append(f"manifests/scripts.json: {path} listed but missing on disk")
    for path in sorted(set(on_disk) - set(by_path)):
        errors.append(f"{path}: local corpus file absent from manifests/scripts.json")

    total_bytes = 0
    for relative in sorted(set(by_path) & set(on_disk)):
        row = by_path[relative]
        data = on_disk[relative].read_bytes()
        total_bytes += len(data)
        if row.get("bytes") != len(data):
            errors.append(
                f"{relative}: bytes {len(data)} != manifest {row.get('bytes')}"
            )
        digest = hashlib.sha256(data).hexdigest()
        if digest.lower() != str(row.get("sha256", "")).lower():
            errors.append(f"{relative}: sha256 mismatch")
        try:
            actual_lines = len(data.decode("utf-8").splitlines())
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: not valid UTF-8 ({exc})")
            continue
        if row.get("lineCount") != actual_lines:
            errors.append(
                f"{relative}: lineCount {actual_lines} != manifest "
                f"{row.get('lineCount')}"
            )
    if manifest.get("totalBytes") != total_bytes:
        errors.append(
            f"manifests/scripts.json: totalBytes {manifest.get('totalBytes')} "
            f"!= {total_bytes} bytes on disk"
        )


def validate_vendor() -> dict[str, list[str]] | None:
    """Verify the promoted N-API catalog and return its bindings."""
    api_path = VENDOR_DIR / "lua_api_index.json"
    provenance_path = VENDOR_DIR / "PROVENANCE.json"
    missing = False
    for path in (api_path, provenance_path):
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: file missing")
            missing = True
    if missing:
        return None

    try:
        provenance = _load(provenance_path)
        records = provenance.get("files", [])
        record = next(
            (item for item in records if item.get("file") == api_path.name),
            None,
        )
        for field in ("sourceLicense", "sourceLicenseUrl"):
            if (
                not isinstance(record, dict)
                or not isinstance(record.get(field), str)
                or not record[field]
            ):
                errors.append(
                    "data/vendor/client-structs/PROVENANCE.json: "
                    f"lua_api_index.json {field} missing"
                )
        expected_hash = record.get("sha256") if record else None
        if not expected_hash:
            errors.append(
                "data/vendor/client-structs/PROVENANCE.json: "
                "lua_api_index.json sha256 missing"
            )
        else:
            actual_hash = hashlib.sha256(api_path.read_bytes()).hexdigest()
            if actual_hash.lower() != expected_hash.lower():
                errors.append(
                    "data/vendor/client-structs/lua_api_index.json: "
                    f"sha256 {actual_hash} != provenance {expected_hash}"
                )
        return load_api_index(api_path)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"vendored N-API catalog: cannot load: {exc}")
        return None


def validate_retail_vendor() -> None:
    """Verify the exact redistributable unluac bytes and embedded license copy."""
    jar = RETAIL_VENDOR_DIR / "unluac_2025_12_23.jar"
    license_path = RETAIL_VENDOR_DIR / "LICENSE.txt"
    provenance_path = RETAIL_VENDOR_DIR / "PROVENANCE.json"
    for path in (jar, license_path, provenance_path):
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: file missing")
    if not all(path.is_file() for path in (jar, license_path, provenance_path)):
        return
    expected_jar = "98be0fa84ac73ca66dce2842a2e4512226f4c611b6500dc96415571fc5538fcc"
    expected_license = "37c47e72083e88b1c9b85c784298e93eee862c741a5f6f1210365bbe007975cf"
    actual_jar = hashlib.sha256(jar.read_bytes()).hexdigest()
    actual_license = hashlib.sha256(license_path.read_bytes()).hexdigest()
    if jar.stat().st_size != 796256 or actual_jar != expected_jar:
        errors.append("unluac vendor: size or sha256 mismatch")
    if actual_license != expected_license:
        errors.append("unluac vendor: license bytes mismatch")
    try:
        provenance = _load(provenance_path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append("unluac vendor: provenance malformed")
        return
    expected = {
        "file": "unluac_2025_12_23.jar",
        "source": "https://sourceforge.net/projects/unluac/files/unluac_2025_12_23.jar/download",
        "retrieved": "2026-08-21",
        "size": 796256,
        "sha256": expected_jar,
        "license": "MIT",
        "licenseFile": "LICENSE.txt",
        "upstreamProject": "unluac",
        "embeddedLicenseSha256": expected_license,
    }
    if provenance != expected:
        errors.append("unluac vendor: provenance record drifted")


def validate_lua_corpus(
    sidecars: dict[str, dict],
    api_bcs: dict[str, list[str]] | None,
) -> None:
    """Require registry, scripts, and sidecars to share one key set."""
    registry_path = LUA_DIR / "registry.json"
    scripts_root = LUA_DIR / "scripts"
    if not registry_path.is_file():
        errors.append("lua/registry.json: file missing")
        return
    if CORPUS_ABSENT:
        return
    if not scripts_root.is_dir():
        errors.append("lua/scripts: directory missing")
        return
    registry_scripts = _load(registry_path)["scripts"]
    registry_keys = set(registry_scripts)
    lua_keys = {
        p.relative_to(scripts_root).with_suffix("").as_posix()
        for p in scripts_root.rglob("*.lua")
    }
    sidecar_keys = set(sidecars)
    for label, keys in (("published .lua", lua_keys), (".calls.json sidecar", sidecar_keys)):
        for missing in sorted(registry_keys - keys):
            errors.append(f"lua corpus: {missing!r} in registry but no {label}")
        for extra in sorted(keys - registry_keys):
            errors.append(f"lua corpus: orphan {label} {extra!r} not in registry")

    whitelist = set(api_bcs) if api_bcs is not None else None
    # Re-derive registry and sidecar fields from the published .lua.
    for key in sorted(registry_keys & lua_keys):
        script_path = scripts_root / f"{key}.lua"
        try:
            raw = script_path.read_bytes()
            script = raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"lua/scripts/{key}.lua: cannot read: {exc}")
            continue
        # read_text would hide this: it folds CRLF to LF on the way in.
        if b"\r\n" in raw:
            errors.append(
                f"lua/scripts/{key}.lua: CRLF line endings; the corpus "
                "contract declares LF, normalised at publish time"
            )
        actual = len(script.splitlines())
        registry_entry = registry_scripts[key]
        classes, methods, requires = extract_signals(
            script, key.rsplit("/", 1)[-1]
        )
        expected_registry = {
            "classes": classes,
            "methods": methods,
            "requires": requires,
            "lineCount": actual,
        }
        for field, expected in expected_registry.items():
            claimed = registry_entry.get(field)
            if claimed != expected:
                errors.append(
                    f"lua/registry.json: {key}: {field} does not match the "
                    "published .lua"
                )

        ciphered = registry_entry.get("ciphered")
        if not isinstance(ciphered, str) or not ciphered.endswith(".lua"):
            errors.append(f"lua/registry.json: {key}: invalid ciphered path")
        elif decode_path(ciphered[:-4]) != key:
            errors.append(
                f"lua/registry.json: {key}: ciphered path decodes to "
                f"{decode_path(ciphered[:-4])!r}"
            )

        sidecar = sidecars.get(key)
        if sidecar is None:
            continue
        expected_sidecar = {
            "decoded": key,
            "ciphered": ciphered,
            "classes": classes,
            "lineCount": actual,
        }
        for field, expected in expected_sidecar.items():
            if sidecar.get(field) != expected:
                errors.append(
                    f"lua/scripts/{key}{SIDECAR_SUFFIX}: {field} does not "
                    "match the registry or published .lua"
                )
        if whitelist is not None:
            observed = scan_script(script, whitelist)
            if sidecar.get("apis") != observed:
                errors.append(
                    f"lua/scripts/{key}{SIDECAR_SUFFIX}: api callsites do not "
                    "match the published .lua"
                )


def validate_napi_index(
    sidecars: dict[str, dict],
    api_bcs: dict[str, list[str]] | None,
) -> None:
    """Require the inverted index to match sidecar callsites."""
    napi_path = LUA_DIR / "napi_index.json"
    if not napi_path.is_file():
        return
    from_sidecars: dict[str, set[tuple[str, int]]] = {}
    for key, sidecar in sidecars.items():
        for api, lines in sidecar.get("apis", {}).items():
            from_sidecars.setdefault(api, set()).update((key, line) for line in lines)
    expected_bindings: dict[str, set[tuple[str, str]]] = {}
    if not CORPUS_ABSENT:
        scripts_root = LUA_DIR / "scripts"
        for lua_path in scripts_root.rglob("*.lua"):
            decoded = lua_path.relative_to(scripts_root).with_suffix("").as_posix()
            content = lua_path.read_text(encoding="utf-8")
            for name, classes in scan_binding_declarations(content).items():
                expected_bindings.setdefault(name, set()).update(
                    (receiver_class, decoded) for receiver_class in classes
                )
    for api, entry in _load(napi_path).get("apis", {}).items():
        if api_bcs is not None:
            expected_bcs = api_bcs.get(api)
            if expected_bcs is None:
                errors.append(
                    f"lua/napi_index.json: {api}: absent from the vendored "
                    "N-API catalog"
                )
            elif entry.get("bcsIds") != expected_bcs:
                errors.append(
                    f"lua/napi_index.json: {api}: bcsIds disagree with the "
                    "vendored N-API catalog"
                )
        if not CORPUS_ABSENT:
            expected = [
                {"class": receiver_class, "script": script}
                for receiver_class, script in sorted(expected_bindings.get(api, set()))
            ]
            if entry.get("bindings") != expected:
                errors.append(
                    f"lua/napi_index.json: {api}: bindings disagree with the "
                    "published .lua"
                )
        callsites = [(c["script"], c["line"]) for c in entry.get("callsites", [])]
        indexed = set(callsites)
        # Reject duplicates before comparing callsite sets.
        if len(callsites) != len(indexed):
            errors.append(
                f"lua/napi_index.json: {api}: {len(callsites) - len(indexed)} "
                f"duplicate callsite(s) in the index"
            )
        observed = from_sidecars.pop(api, set())
        if indexed != observed:
            errors.append(
                f"lua/napi_index.json: {api}: callsites disagree with the "
                f"sidecars ({len(indexed - observed)} indexed-only, "
                f"{len(observed - indexed)} sidecar-only)"
            )
    for api in sorted(from_sidecars):
        errors.append(
            f"lua/napi_index.json: api {api!r} appears in the sidecars but has "
            f"no index entry"
        )


def validate_derived_counts(sidecars: dict[str, dict]) -> None:
    """Recompute generator counts from their payloads."""
    registry_path = LUA_DIR / "registry.json"
    if registry_path.is_file():
        registry = _load(registry_path)
        actual = len(registry.get("scripts", {}))
        if registry.get("scriptCount") != actual:
            errors.append(
                f"lua/registry.json: scriptCount {registry.get('scriptCount')} "
                f"!= {actual} script entries"
            )

    napi_path = LUA_DIR / "napi_index.json"
    if napi_path.is_file():
        napi = _load(napi_path)
        apis = napi.get("apis", {})
        if napi.get("apiCount") != len(apis):
            errors.append(
                f"lua/napi_index.json: apiCount {napi.get('apiCount')} != "
                f"{len(apis)} api entries"
            )
        total = 0
        for name, entry in apis.items():
            callsites = entry.get("callsites", [])
            total += len(callsites)
            if entry.get("callsiteCount") != len(callsites):
                errors.append(
                    f"lua/napi_index.json: {name}: callsiteCount "
                    f"{entry.get('callsiteCount')} != {len(callsites)} callsites"
                )
        if napi.get("totalCallsites") != total:
            errors.append(
                f"lua/napi_index.json: totalCallsites "
                f"{napi.get('totalCallsites')} != {total} callsites across apis"
            )

    for key, sidecar in sidecars.items():
        label = f"lua/scripts/{key}{SIDECAR_SUFFIX}"
        apis = sidecar.get("apis", {})
        if sidecar.get("decoded") != key:
            errors.append(
                f"{label}: decoded {sidecar.get('decoded')!r} does not match "
                f"its path {key!r}"
            )
        if sidecar.get("apiCount") != len(apis):
            errors.append(
                f"{label}: apiCount {sidecar.get('apiCount')} != {len(apis)} apis"
            )
        callsites = sum(len(lines) for lines in apis.values())
        if sidecar.get("callsiteCount") != callsites:
            errors.append(
                f"{label}: callsiteCount {sidecar.get('callsiteCount')} != "
                f"{callsites} callsite lines"
            )


def validate_docs_index() -> None:
    """Require docs/README.md to index the tracked docs tree both ways."""
    readme = DOCS_DIR / "README.md"
    if not readme.is_file():
        errors.append("docs/README.md: file missing")
        return
    docs_root = DOCS_DIR.resolve()
    linked: set[str] = set()
    for target in re.findall(r"\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
        target = target.split("#", 1)[0]
        if not target.endswith(".md"):
            continue
        candidate = (DOCS_DIR / target).resolve()
        try:
            relative = candidate.relative_to(docs_root)
        except ValueError:
            continue
        if relative.as_posix() == "README.md":
            continue
        if relative.parts[:2] == ("ai_agents", "local"):
            continue
        linked.add(relative.as_posix())
    on_disk = {
        p.relative_to(DOCS_DIR).as_posix()
        for p in DOCS_DIR.rglob("*.md")
        if p.relative_to(DOCS_DIR).as_posix() != "README.md"
        and p.relative_to(DOCS_DIR).parts[:2] != ("ai_agents", "local")
    }
    for missing in sorted(linked - on_disk):
        errors.append(f"docs/README.md: indexes {missing} but no such file under docs/")
    for orphan in sorted(on_disk - linked):
        errors.append(f"docs/{orphan}: present under docs/ but unindexed in docs/README.md")


def main() -> int:
    tracked_paths = validate_repository_boundary()
    json_count = validate_all_json(tracked_paths)
    if errors:
        print(f"corpus validation FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    if not run_focused_tests():
        return 1
    if not _HAVE_JSONSCHEMA:
        print(
            "error: jsonschema not installed; schema validation is a required "
            "part of this gate and cannot be skipped. pip install jsonschema",
            file=sys.stderr,
        )
        return 1
    sidecars = load_sidecars()
    api_bcs = validate_vendor()
    validate_retail_vendor()
    validate_schemas(sidecars)
    validate_retail_lua_coverage()
    validate_myplayer_timer_consumers()
    validate_quest_selector_consumers()
    validate_reproduction_contract(sidecars)
    validate_lua_corpus(sidecars, api_bcs)
    validate_napi_index(sidecars, api_bcs)
    validate_derived_counts(sidecars)
    validate_docs_index()
    if errors:
        print(f"corpus validation FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    corpus_check = "manifest metadata" if CORPUS_ABSENT else "2,671 script hashes"
    print(
        f"repository boundary + Lua corpus validation OK ({len(tracked_paths)} tracked "
        f"files, {json_count} tracked JSON files, schemas, {corpus_check}, "
        "registry/sidecar/index agreement, vendor pin, derived counts + "
        "docs-index sync)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
