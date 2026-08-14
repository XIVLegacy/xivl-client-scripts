from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import validate_corpus as validator  # noqa: E402
from _corpus import (  # noqa: E402
    copy_lua_lf,
    extract_signals,
    publish_corpus,
    read_text_or_warn,
)


class CorpusToolTests(unittest.TestCase):
    def tearDown(self) -> None:
        validator.errors.clear()

    def test_extract_signals_requires_top_level_declarations(self) -> None:
        content = """L0_1 = RealClass
function L1_1(A0_2)
  local L1_2, L2_2
  L1_2 = OTHER_CONSTANT
  L1_2.field = L2_2
  L1_2 = "/i"
end
L0_1.realMethod = L1_1
L2_1 = require
L3_1 = "/Base/Class"
L2_1(L3_1)
L4_1 = "//dev"
"""

        self.assertEqual(
            extract_signals(content, "realclass"),
            (["RealClass"], ["realMethod"], ["/Base/Class"]),
        )

    def test_text_helpers_preserve_corpus_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "bad.lua"
            path.write_bytes(b"ok\n\xff\n")

            with self.assertRaises(UnicodeDecodeError):
                read_text_or_warn(path, strict=True)
            with redirect_stderr(io.StringIO()):
                self.assertIsNone(read_text_or_warn(path, strict=False))

            source = root / "source.lua"
            published = root / "published.lua"
            source.write_bytes(b"trailing \r\nnext\r\nbare\rno-final-newline")
            copy_lua_lf(source, published)
            self.assertEqual(
                published.read_bytes(),
                b"trailing \nnext\nbare\rno-final-newline",
            )

    def test_publish_failure_leaves_outputs_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            output = root / "lua"
            source.mkdir()
            output.mkdir()
            (source / "a.lua").write_text("L0_1 = A\n", encoding="utf-8")
            (source / "b.lua").write_text("L0_1 = B\n", encoding="utf-8")
            registry = output / "registry.json"
            scripts = output / "scripts"
            scripts.mkdir()
            existing_script = scripts / "existing.lua"
            registry.write_bytes(b"existing registry\n")
            existing_script.write_bytes(b"existing script\n")
            calls = 0

            def fail_during_copy(source_path: Path, destination: Path) -> object:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("deliberate staged-copy failure")
                return shutil.copyfile(source_path, destination)

            with redirect_stderr(io.StringIO()):
                result = publish_corpus(
                    source,
                    output,
                    strict=True,
                    copy_file=fail_during_copy,
                )

            self.assertEqual(result, 1)
            self.assertEqual(registry.read_bytes(), b"existing registry\n")
            self.assertEqual(existing_script.read_bytes(), b"existing script\n")
            self.assertEqual(
                sorted(path.name for path in scripts.iterdir()),
                ["existing.lua"],
            )
            self.assertEqual(list(root.glob(".lua-publish-*")), [])

    def test_install_failure_rolls_back_both_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            output = root / "lua"
            source.mkdir()
            output.mkdir()
            (source / "a.lua").write_text("L0_1 = A\n", encoding="utf-8")
            registry = output / "registry.json"
            scripts = output / "scripts"
            scripts.mkdir()
            existing_script = scripts / "existing.lua"
            registry.write_bytes(b"existing registry\n")
            existing_script.write_bytes(b"existing script\n")
            real_replace = os.replace

            def fail_before_script_install(source_path: Path, destination: Path) -> None:
                staged = Path(source_path)
                if (
                    staged.name == "scripts"
                    and staged.parent.name.startswith(".lua-publish-")
                ):
                    raise OSError("deliberate install failure")
                real_replace(source_path, destination)

            with (
                patch("_corpus.os.replace", side_effect=fail_before_script_install),
                redirect_stderr(io.StringIO()),
            ):
                result = publish_corpus(source, output, strict=True)

            self.assertEqual(result, 1)
            self.assertEqual(registry.read_bytes(), b"existing registry\n")
            self.assertEqual(existing_script.read_bytes(), b"existing script\n")
            self.assertEqual(
                sorted(path.name for path in scripts.iterdir()),
                ["existing.lua"],
            )
            self.assertEqual(list(root.glob(".lua-publish-*")), [])
            self.assertEqual(list(root.glob(".lua-backup-*")), [])

    def test_missing_sidecar_schema_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            previous = validator.SCHEMAS
            validator.SCHEMAS = Path(temp)
            try:
                validator.errors.clear()
                validator.validate_schemas({})
            finally:
                validator.SCHEMAS = previous

        self.assertTrue(
            any("lua_script_calls.schema.json missing" in error
                for error in validator.errors)
        )

    def test_sidecar_callsites_are_checked_against_lua(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            lua_dir = Path(temp) / "lua"
            scripts = lua_dir / "scripts"
            scripts.mkdir(parents=True)
            (scripts / "x.lua").write_text("L0_1 = _api\n", encoding="utf-8")
            registry = {
                "scripts": {
                    "x": {
                        "ciphered": "m.lua",
                        "classes": [],
                        "methods": [],
                        "requires": [],
                        "lineCount": 1,
                    }
                }
            }
            (lua_dir / "registry.json").write_text(
                json.dumps(registry), encoding="utf-8"
            )
            sidecars = {
                "x": {
                    "decoded": "x",
                    "ciphered": "m.lua",
                    "classes": [],
                    "lineCount": 1,
                    "apiCount": 0,
                    "callsiteCount": 0,
                    "apis": {},
                }
            }

            previous = validator.LUA_DIR
            previous_absent = validator.CORPUS_ABSENT
            validator.LUA_DIR = lua_dir
            validator.CORPUS_ABSENT = False
            try:
                validator.errors.clear()
                validator.validate_lua_corpus(sidecars, {"_api": []})
            finally:
                validator.LUA_DIR = previous
                validator.CORPUS_ABSENT = previous_absent

        self.assertTrue(
            any("api callsites do not match" in error
                for error in validator.errors)
        )

    def test_napi_bindings_are_checked_against_vendor(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            lua_dir = Path(temp) / "lua"
            lua_dir.mkdir()
            napi = {
                "apis": {
                    "_api": {
                        "bcsIds": ["BCS-Y-999999"],
                        "callsites": [{"script": "x", "line": 1}],
                    }
                }
            }
            (lua_dir / "napi_index.json").write_text(
                json.dumps(napi), encoding="utf-8"
            )
            sidecars = {"x": {"apis": {"_api": [1]}}}

            previous = validator.LUA_DIR
            validator.LUA_DIR = lua_dir
            try:
                validator.errors.clear()
                validator.validate_napi_index(
                    sidecars, {"_api": ["BCS-Y-000001"]}
                )
            finally:
                validator.LUA_DIR = previous

        self.assertTrue(
            any("bcsIds disagree" in error for error in validator.errors)
        )

    def test_vendor_hash_is_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vendor_dir = Path(temp)
            (vendor_dir / "lua_api_index.json").write_text(
                json.dumps({"apis": {}}), encoding="utf-8"
            )
            (vendor_dir / "PROVENANCE.json").write_text(
                json.dumps({
                    "files": [{
                        "file": "lua_api_index.json",
                        "sourceLicense": "CC-BY-4.0",
                        "sourceLicenseUrl": "https://creativecommons.org/licenses/by/4.0/",
                        "sha256": "0" * 64,
                    }]
                }),
                encoding="utf-8",
            )

            previous = validator.VENDOR_DIR
            validator.VENDOR_DIR = vendor_dir
            try:
                validator.errors.clear()
                validator.validate_vendor()
            finally:
                validator.VENDOR_DIR = previous

        self.assertTrue(
            any("sha256" in error for error in validator.errors)
        )

    def test_vendor_license_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vendor_dir = Path(temp)
            api_path = vendor_dir / "lua_api_index.json"
            api_path.write_text(json.dumps({"apis": {}}), encoding="utf-8")
            (vendor_dir / "PROVENANCE.json").write_text(
                json.dumps({
                    "files": [{
                        "file": api_path.name,
                        "sha256": hashlib.sha256(api_path.read_bytes()).hexdigest(),
                    }]
                }),
                encoding="utf-8",
            )

            previous = validator.VENDOR_DIR
            validator.VENDOR_DIR = vendor_dir
            try:
                validator.errors.clear()
                validator.validate_vendor()
            finally:
                validator.VENDOR_DIR = previous

        self.assertTrue(
            any("sourceLicense missing" in error for error in validator.errors)
        )


if __name__ == "__main__":
    unittest.main()
