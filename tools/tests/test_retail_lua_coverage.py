from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import retail_lua_coverage as coverage  # noqa: E402


def raw_lpb(chunk: bytes = b"\x1bLuaQbody") -> bytes:
    return b"rlu\x0bABCD" + chunk


def xor_lpb(chunk: bytes = b"\x1bLuaQbody") -> bytes:
    return (
        b"rle\x0cABCD"
        + len(chunk).to_bytes(4, "little")
        + b"Z"
        + bytes(byte ^ coverage.XOR_KEY for byte in chunk)
    )


class RetailLuaCoverageTests(unittest.TestCase):
    def test_path_transform_is_ascii_casefolded_involution(self) -> None:
        self.assertEqual(coverage.transform_lua_path("4VV"), "foo")
        source = "judge/JudgeBaseClass_u"
        ciphered = coverage.transform_lua_path(source)
        self.assertEqual(coverage.transform_lua_path(ciphered), source.lower())

    def test_normalization_collapses_slashes_and_rejects_unsafe_paths(self) -> None:
        self.assertEqual(
            coverage.normalize_resource_path(r"A\.\B//C.LE.LPB"),
            "a/b/c.le.lpb",
        )
        with self.assertRaises(coverage.CoverageError):
            coverage.normalize_resource_path("a/../b.le.lpb")
        with self.assertRaises(coverage.CoverageError):
            coverage.normalize_resource_path("lu\N{LATIN SMALL LETTER A WITH ACUTE}.le.lpb")

    def test_extracts_both_pinned_wrappers(self) -> None:
        raw = coverage.extract_lpb(raw_lpb())
        self.assertEqual(raw["variant"], "raw")
        self.assertEqual(raw["headerBytes"], 8)
        xor = coverage.extract_lpb(xor_lpb())
        self.assertEqual(xor["variant"], "xor-73")
        self.assertEqual(xor["headerBytes"], 16)
        self.assertEqual(xor["advisorySize"], 9)
        self.assertEqual(raw["decodedPayloadSha256"], xor["decodedPayloadSha256"])

    def test_wrapper_failures_have_stable_classifications(self) -> None:
        cases = [
            (b"bad!payload", "unsupported-wrapper"),
            (b"rle\x0c", "unexpected-end"),
            (b"rlu\x0bABCDxxxxx", "invalid-lua-chunk"),
        ]
        for data, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaises(coverage.CoverageError) as raised:
                    coverage.extract_lpb(data)
                self.assertEqual(raised.exception.kind, expected)

    def test_pinned_source_hash_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            for relative in coverage.TOOLS_SOURCES:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"drift")
            completed = SimpleNamespace(stdout=coverage.TOOLS_COMMIT + "\n")
            with patch.object(coverage.subprocess, "run", return_value=completed):
                with self.assertRaisesRegex(ValueError, "source hash drift"):
                    coverage.pinned_tool_metadata(root)

    def test_fabricated_coverage_match_is_rejected_after_redigest(self) -> None:
        manifest = {"scripts": [{"relativePath": "lua/scripts/foo.lua"}]}
        registry = {"scripts": {"foo": {"ciphered": "4vv.lua"}}}
        tool = {
            "repository": "XIVLegacy/xivl-tools",
            "commit": coverage.TOOLS_COMMIT,
            "sources": [],
        }
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            (root / "4vv.le.lpb").write_bytes(raw_lpb())
            report = coverage.analyze_resource_tree(root, manifest, registry, tool)
        self.assertEqual(report["summary"]["matchedScriptCount"], 1)

        mutated = copy.deepcopy(report)
        row = mutated["resources"][0]
        row["resourcePath"] = "alias.le.lpb"
        row["normalizedResourcePath"] = "alias.le.lpb"
        mutated["source"]["inventorySha256"] = coverage.inventory_digest(
            mutated["resources"]
        )
        self.assertIn(
            "resources[0]: fabricated coverage match",
            coverage.validate_report(mutated, manifest, registry),
        )

    def test_inventory_digest_detects_hash_mutation(self) -> None:
        rows = [
            {
                "resourcePath": "a.le.lpb",
                "normalizedResourcePath": "a.le.lpb",
                "bytes": 1,
                "sha256": "A" * 64,
            }
        ]
        original = coverage.inventory_digest(rows)
        rows[0]["sha256"] = "B" * 64
        self.assertNotEqual(original, coverage.inventory_digest(rows))

    def test_duplicate_normalized_match_is_rejected(self) -> None:
        manifest = {"scripts": [{"relativePath": "lua/scripts/foo.lua"}]}
        registry = {"scripts": {"foo": {"ciphered": "4vv.lua"}}}
        wrapper = coverage.extract_lpb(raw_lpb())
        row = {
            "resourcePath": "4vv.le.lpb",
            "normalizedResourcePath": "4vv.le.lpb",
            "bytes": len(raw_lpb()),
            "sha256": coverage.sha256_bytes(raw_lpb()),
            "wrapper": wrapper,
            "decodedScriptPath": "lua/scripts/foo.lua",
            "classification": "matched-script",
        }
        report = {
            "source": {"fileCount": 2, "inventorySha256": ""},
            "summary": {
                "classifications": {"matched-script": 2},
                "wrapperVariants": {"raw": 2},
                "lpbCandidateCount": 2,
                "validLpbCount": 2,
                "matchedScriptCount": 1,
                "missingScriptCount": 0,
            },
            "resources": [copy.deepcopy(row), copy.deepcopy(row)],
            "missingScripts": [],
        }
        report["source"]["inventorySha256"] = coverage.inventory_digest(
            report["resources"]
        )
        problems = coverage.validate_report(report, manifest, registry)
        self.assertTrue(any("duplicate normalized resource" in item for item in problems))


if __name__ == "__main__":
    unittest.main()
