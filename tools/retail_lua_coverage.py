#!/usr/bin/env python3
"""Build or check the bounded retail Lua resource coverage census."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "manifests" / "retail_lua_coverage.json"
MANIFEST_PATH = REPO_ROOT / "manifests" / "scripts.json"
REGISTRY_PATH = REPO_ROOT / "lua" / "registry.json"
SIDECARS_ROOT = REPO_ROOT / "lua" / "scripts"
TOOLS_COMMIT = "d371b9bfeb93787f7dfeb8b64600976df68ca8cb"
TOOLS_SOURCES = {
    "src/formats/src/lua_path.rs": "1C655BFE6C89B5A39366342A5B846F94564567F9A72749C81B6C6102C3AC362C",
    "src/formats/src/lpb.rs": "96639A41C4226DD41E8DD4F19E757947685BED9CDB07D6AF63B3D240CD08278A",
}
RAW_MAGIC = b"rlu\x0b"
XOR_MAGIC = b"rle\x0c"
LUA_51_SIGNATURE = b"\x1bLuaQ"
XOR_KEY = 0x73
SHA256_RE = re.compile(r"^[0-9A-F]{64}$")


class CoverageError(ValueError):
    """Stable local classification failure."""

    def __init__(self, kind: str, offset: int, message: str):
        super().__init__(message)
        self.kind = kind
        self.offset = offset


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalize_resource_path(value: str) -> str:
    """Return one lowercase ASCII POSIX resource path."""
    if not value.isascii():
        raise CoverageError("unsupported-path", 0, "resource path is not ASCII")
    parts = []
    for part in value.replace("\\", "/").split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            raise CoverageError("unsupported-path", 0, "resource path traverses upward")
        parts.append(part.lower())
    if not parts:
        raise CoverageError("unsupported-path", 0, "resource path is empty")
    return "/".join(parts)


def transform_lua_path(value: str) -> str:
    """Apply the pinned xivl-tools ASCII Lua-path involution."""
    if not value.isascii():
        raise CoverageError("unsupported-path", 0, "Lua resource path is not ASCII")
    output = []
    for byte in value.encode("ascii"):
        lower = byte + 32 if ord("A") <= byte <= ord("Z") else byte
        if ord("a") <= lower <= ord("j"):
            transformed = ord("9") - (lower - ord("a"))
        elif ord("k") <= lower <= ord("z"):
            transformed = ord("z") - (lower - ord("k"))
        elif ord("0") <= lower <= ord("9"):
            transformed = ord("j") - (lower - ord("0"))
        else:
            transformed = lower
        output.append(chr(transformed))
    return "".join(output)


def extract_lpb(data: bytes) -> dict:
    """Return non-reconstructive metadata for the two pinned LPB wrappers."""
    if len(data) < 4:
        raise CoverageError("unexpected-end", len(data), "LPB magic is truncated")
    if data[:4] == RAW_MAGIC:
        if len(data) < 8:
            raise CoverageError("unexpected-end", len(data), "raw LPB header is truncated")
        variant = "raw"
        header_bytes = 8
        advisory_size = None
        decoded = data[8:]
    elif data[:4] == XOR_MAGIC:
        if len(data) < 16:
            raise CoverageError("unexpected-end", len(data), "XOR LPB header is truncated")
        variant = "xor-73"
        header_bytes = 16
        advisory_size = int.from_bytes(data[8:12], "little")
        decoded = bytes(byte ^ XOR_KEY for byte in data[13:])
    else:
        raise CoverageError("unsupported-wrapper", 0, "LPB wrapper magic is unsupported")
    if len(decoded) < len(LUA_51_SIGNATURE):
        raise CoverageError(
            "unexpected-end", len(data), "decoded Lua 5.1 signature is truncated"
        )
    if not decoded.startswith(LUA_51_SIGNATURE):
        raise CoverageError(
            "invalid-lua-chunk", header_bytes, "decoded payload is not Lua 5.1"
        )
    result = {
        "variant": variant,
        "headerBytes": header_bytes,
        "decodedPayloadBytes": len(decoded),
        "decodedPayloadSha256": sha256_bytes(decoded),
    }
    if advisory_size is not None:
        result["advisorySize"] = advisory_size
    return result


def expected_resource_map(registry: dict) -> dict[str, str]:
    """Map normalized retail resources to canonical tracked script paths."""
    result: dict[str, str] = {}
    for decoded, entry in registry["scripts"].items():
        ciphered = entry["ciphered"]
        if not ciphered.endswith(".lua"):
            raise ValueError(f"registry ciphered path is not .lua: {ciphered}")
        resource = normalize_resource_path(ciphered[:-4] + ".le.lpb")
        script = f"lua/scripts/{decoded}.lua"
        if resource in result:
            raise ValueError(f"duplicate expected retail resource: {resource}")
        result[resource] = script
    return result


def pinned_tool_metadata(tools_root: Path) -> dict:
    """Verify and describe the explicit read-only xivl-tools checkout."""
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tools_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != TOOLS_COMMIT:
        raise ValueError(f"xivl-tools revision is {revision}, expected {TOOLS_COMMIT}")
    sources = []
    for relative, expected_hash in TOOLS_SOURCES.items():
        actual_hash = sha256_file(tools_root / relative)
        if actual_hash != expected_hash:
            raise ValueError(f"xivl-tools source hash drift: {relative}")
        sources.append({"path": relative, "sha256": actual_hash})
    return {
        "repository": "XIVLegacy/xivl-tools",
        "commit": revision,
        "sources": sources,
    }


def inventory_digest(resources: list[dict]) -> str:
    lines = [
        f"{row['resourcePath']}\t{row['normalizedResourcePath']}\t"
        f"{row['bytes']}\t{row['sha256']}\n"
        for row in resources
    ]
    return sha256_bytes("".join(lines).encode("utf-8"))


def sidecar_inventory() -> tuple[int, str]:
    rows = []
    for path in sorted(SIDECARS_ROOT.rglob("*.calls.json")):
        relative = path.relative_to(REPO_ROOT).as_posix()
        rows.append(f"{relative}\t{path.stat().st_size}\t{sha256_file(path)}\n")
    return len(rows), sha256_bytes("".join(rows).encode("ascii"))


def analyze_resource_tree(
    resource_root: Path,
    manifest: dict,
    registry: dict,
    tool_metadata: dict,
) -> dict:
    """Analyze every file below an explicit retail client/script root."""
    manifest_scripts = {row["relativePath"] for row in manifest["scripts"]}
    expected = expected_resource_map(registry)
    rows = []
    normalized_groups: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(
        resource_root.rglob("*"),
        key=lambda item: (item.as_posix().lower(), item.as_posix()),
    ):
        if not path.is_file():
            continue
        relative = path.relative_to(resource_root).as_posix()
        data = path.read_bytes()
        base = {
            "resourcePath": relative,
            "normalizedResourcePath": "",
            "bytes": len(data),
            "sha256": sha256_bytes(data),
        }
        try:
            normalized = normalize_resource_path(relative)
            base["normalizedResourcePath"] = normalized
        except CoverageError as exc:
            base["classification"] = "unsupported-path"
            base["error"] = {"kind": exc.kind, "offset": exc.offset}
            rows.append(base)
            continue

        is_lpb_name = normalized.endswith(".lpb")
        is_lpb_magic = data[:4] in {RAW_MAGIC, XOR_MAGIC}
        if not is_lpb_name and not is_lpb_magic:
            base["classification"] = "non-script-resource"
            rows.append(base)
            normalized_groups[normalized].append(base)
            continue
        try:
            base["wrapper"] = extract_lpb(data)
        except CoverageError as exc:
            base["classification"] = (
                "unsupported-wrapper" if exc.kind == "unsupported-wrapper" else "extraction-failure"
            )
            base["error"] = {"kind": exc.kind, "offset": exc.offset}
            rows.append(base)
            normalized_groups[normalized].append(base)
            continue
        if not normalized.endswith(".le.lpb"):
            base["classification"] = "non-script-wrapper"
            rows.append(base)
            normalized_groups[normalized].append(base)
            continue
        ciphered_stem = normalized[: -len(".le.lpb")]
        base["decodedScriptPath"] = f"lua/scripts/{transform_lua_path(ciphered_stem)}.lua"
        rows.append(base)
        normalized_groups[normalized].append(base)

    for group in normalized_groups.values():
        if len(group) > 1:
            for row in group:
                row["classification"] = "duplicate-alias"

    valid_named = [row for row in rows if "decodedScriptPath" in row]
    by_decoded: dict[str, list[dict]] = defaultdict(list)
    for row in valid_named:
        by_decoded[row["decodedScriptPath"]].append(row)
    for script_path, group in by_decoded.items():
        expected_resources = [
            resource for resource, script in expected.items() if script == script_path
        ]
        expected_resource = expected_resources[0] if expected_resources else None
        primary = next(
            (
                row
                for row in group
                if row["normalizedResourcePath"] == expected_resource
                and script_path in manifest_scripts
                and row.get("classification") != "duplicate-alias"
            ),
            None,
        )
        if primary is not None:
            primary["classification"] = "matched-script"
        for row in group:
            if row is primary or row.get("classification") == "duplicate-alias":
                continue
            if script_path not in manifest_scripts:
                row["classification"] = "missing-script"
            else:
                row["classification"] = "ciphered-path-mismatch"
        if primary is not None:
            for row in group:
                if row is not primary:
                    row["classification"] = "duplicate-alias"

    rows.sort(key=lambda row: (row["normalizedResourcePath"], row["resourcePath"]))
    covered = {
        row["decodedScriptPath"]
        for row in rows
        if row["classification"] == "matched-script"
    }
    missing = [
        {"scriptPath": path, "classification": "missing-retail-resource"}
        for path in sorted(manifest_scripts - covered)
    ]
    classifications = dict(sorted(Counter(row["classification"] for row in rows).items()))
    wrapper_variants = dict(
        sorted(Counter(row["wrapper"]["variant"] for row in rows if "wrapper" in row).items())
    )
    sidecar_count, sidecar_digest = sidecar_inventory()
    return {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": "2012.09.19.0001",
        "source": {
            "resourceRoot": "client/script",
            "fileCount": len(rows),
            "inventorySha256": inventory_digest(rows),
        },
        "tool": tool_metadata,
        "corpus": {
            "manifest": "manifests/scripts.json",
            "manifestSha256": sha256_file(MANIFEST_PATH),
            "registry": "lua/registry.json",
            "registrySha256": sha256_file(REGISTRY_PATH),
            "scriptCount": len(manifest_scripts),
            "sidecarCount": sidecar_count,
            "sidecarInventorySha256": sidecar_digest,
        },
        "summary": {
            "classifications": classifications,
            "wrapperVariants": wrapper_variants,
            "lpbCandidateCount": sum(
                row["normalizedResourcePath"].endswith(".lpb") or "wrapper" in row
                for row in rows
            ),
            "validLpbCount": sum("wrapper" in row for row in rows),
            "matchedScriptCount": len(covered),
            "missingScriptCount": len(missing),
        },
        "resources": rows,
        "missingScripts": missing,
    }


def validate_report(report: dict, manifest: dict, registry: dict) -> list[str]:
    """Check claims that do not require retail bytes."""
    errors = []
    resources = report.get("resources", [])
    manifest_scripts = {row["relativePath"] for row in manifest["scripts"]}
    expected = expected_resource_map(registry)
    normalized_groups: dict[str, list[dict]] = defaultdict(list)
    matched_by_script: Counter[str] = Counter()
    for index, row in enumerate(resources):
        label = f"resources[{index}]"
        try:
            normalized = normalize_resource_path(row["resourcePath"])
        except CoverageError:
            normalized = ""
            if row.get("classification") != "unsupported-path":
                errors.append(f"{label}: unsupported path claims another classification")
        if normalized != row.get("normalizedResourcePath"):
            errors.append(f"{label}: normalized resource path disagrees")
        if normalized:
            normalized_groups[normalized].append(row)
        if not SHA256_RE.fullmatch(row.get("sha256", "")):
            errors.append(f"{label}: invalid input sha256")
        wrapper = row.get("wrapper")
        if wrapper and not SHA256_RE.fullmatch(wrapper.get("decodedPayloadSha256", "")):
            errors.append(f"{label}: invalid decoded payload sha256")
        if wrapper:
            variant = wrapper.get("variant")
            if variant == "raw" and (
                wrapper.get("headerBytes") != 8 or "advisorySize" in wrapper
            ):
                errors.append(f"{label}: raw wrapper metadata disagrees")
            if variant == "xor-73" and (
                wrapper.get("headerBytes") != 16 or "advisorySize" not in wrapper
            ):
                errors.append(f"{label}: XOR wrapper metadata disagrees")
        script = row.get("decodedScriptPath")
        resource = row.get("normalizedResourcePath", "")
        if script and wrapper and resource.endswith(".le.lpb"):
            decoded = f"lua/scripts/{transform_lua_path(resource[:-7])}.lua"
            if decoded != script:
                errors.append(f"{label}: decoded script path disagrees")
        if row.get("classification") == "matched-script":
            matched_by_script[script] += 1
            if not wrapper:
                errors.append(f"{label}: matched script has no valid wrapper")
            if script not in manifest_scripts:
                errors.append(f"{label}: matched script is absent from the corpus")
            if expected.get(row.get("normalizedResourcePath")) != script:
                errors.append(f"{label}: fabricated coverage match")

    for normalized, group in normalized_groups.items():
        if len(group) > 1 and any(
            row.get("classification") != "duplicate-alias" for row in group
        ):
            errors.append(f"duplicate normalized resource is not classified: {normalized}")
    for script, count in matched_by_script.items():
        if count > 1:
            errors.append(f"script has multiple matched resources: {script}")

    counts = dict(sorted(Counter(row.get("classification") for row in resources).items()))
    if report.get("summary", {}).get("classifications") != counts:
        errors.append("summary classifications disagree with resources")
    if report.get("source", {}).get("fileCount") != len(resources):
        errors.append("source file count disagrees with resources")
    if report.get("source", {}).get("inventorySha256") != inventory_digest(resources):
        errors.append("source inventory digest disagrees with resources")
    covered = {
        row.get("decodedScriptPath")
        for row in resources
        if row.get("classification") == "matched-script"
    }
    expected_missing = [
        {"scriptPath": path, "classification": "missing-retail-resource"}
        for path in sorted(manifest_scripts - covered)
    ]
    if report.get("missingScripts") != expected_missing:
        errors.append("missing script classification disagrees with matches")
    summary = report.get("summary", {})
    if summary.get("matchedScriptCount") != len(covered):
        errors.append("matched script count disagrees")
    if summary.get("missingScriptCount") != len(expected_missing):
        errors.append("missing script count disagrees")
    wrapper_variants = dict(
        sorted(
            Counter(
                row["wrapper"]["variant"]
                for row in resources
                if isinstance(row.get("wrapper"), dict)
            ).items()
        )
    )
    if summary.get("wrapperVariants") != wrapper_variants:
        errors.append("wrapper variant counts disagree with resources")
    valid_lpb_count = sum(isinstance(row.get("wrapper"), dict) for row in resources)
    if summary.get("validLpbCount") != valid_lpb_count:
        errors.append("valid LPB count disagrees with resources")
    candidate_count = sum(
        str(row.get("normalizedResourcePath", "")).endswith(".lpb")
        or isinstance(row.get("wrapper"), dict)
        for row in resources
    )
    if summary.get("lpbCandidateCount") != candidate_count:
        errors.append("LPB candidate count disagrees with resources")
    return errors


def render_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-root", required=True, type=Path)
    parser.add_argument("--tools-root", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    resource_root = args.client_root / "client" / "script"
    if not resource_root.is_dir():
        print(f"error: client/script not found below {args.client_root}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    try:
        tool_metadata = pinned_tool_metadata(args.tools_root)
        report = analyze_resource_tree(resource_root, manifest, registry, tool_metadata)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors = validate_report(report, manifest, registry)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    rendered = render_json(report)
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != rendered:
            print(f"error: {OUTPUT_PATH.relative_to(REPO_ROOT)} is stale", file=sys.stderr)
            return 1
        print(f"PASS: {len(report['resources'])} retail resources match the coverage census")
        return 0
    OUTPUT_PATH.write_bytes(rendered)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} with {len(report['resources'])} resources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
