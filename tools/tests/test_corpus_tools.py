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
import quest_selector_consumers as quest_analyzer  # noqa: E402
from _corpus import (  # noqa: E402
    CorpusRootError,
    annotate_corpus,
    build_script_manifest,
    copy_lua_lf,
    extract_signals,
    publish_corpus,
    resolve_scripts_root,
    scan_binding_declarations,
    validate_scripts_root,
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

    def test_external_scripts_tree_rejects_linked_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            scripts = Path(temp) / "scripts"
            scripts.mkdir()
            linked = scripts / "linked.lua"
            linked.write_text("return nil\n", encoding="utf-8")
            previous_root = validator.EXTERNAL_SCRIPTS_ROOT
            previous_absent = validator.CORPUS_ABSENT
            validator.EXTERNAL_SCRIPTS_ROOT = scripts
            validator.CORPUS_ABSENT = False
            try:
                with patch.object(
                    validator,
                    "_is_link_or_reparse",
                    side_effect=lambda path, result: path == linked,
                ):
                    self.assertFalse(validator.validate_scripts_tree_boundary())
            finally:
                validator.EXTERNAL_SCRIPTS_ROOT = previous_root
                validator.CORPUS_ABSENT = previous_absent
        self.assertTrue(
            any("linked or invalid file" in error for error in validator.errors)
        )

    def test_external_scripts_tree_rejects_linked_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            scripts = Path(temp) / "scripts"
            scripts.mkdir()
            previous_root = validator.EXTERNAL_SCRIPTS_ROOT
            previous_absent = validator.CORPUS_ABSENT
            validator.EXTERNAL_SCRIPTS_ROOT = scripts
            validator.CORPUS_ABSENT = False
            try:
                with patch.object(
                    validator,
                    "_is_link_or_reparse",
                    side_effect=lambda path, result: path == scripts,
                ):
                    self.assertFalse(validator.validate_scripts_tree_boundary())
            finally:
                validator.EXTERNAL_SCRIPTS_ROOT = previous_root
                validator.CORPUS_ABSENT = previous_absent
        self.assertTrue(
            any("plain directory" in error for error in validator.errors)
        )

    def test_missing_external_scripts_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            previous_root = validator.EXTERNAL_SCRIPTS_ROOT
            previous_absent = validator.CORPUS_ABSENT
            validator.EXTERNAL_SCRIPTS_ROOT = missing
            validator.CORPUS_ABSENT = False
            try:
                self.assertFalse(validator.validate_scripts_tree_boundary())
            finally:
                validator.EXTERNAL_SCRIPTS_ROOT = previous_root
                validator.CORPUS_ABSENT = previous_absent
        self.assertTrue(
            any("missing or unreadable" in error for error in validator.errors)
        )

    def test_scripts_root_resolution_preserves_linked_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            linked = root / "linked"
            with patch.object(
                Path,
                "resolve",
                side_effect=AssertionError("root resolution followed a link"),
            ):
                self.assertEqual(
                    resolve_scripts_root(root / "default", linked), linked.absolute()
                )

    def test_shared_scripts_root_rejects_linked_root_and_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "scripts"
            root.mkdir()
            linked = root / "linked.lua"
            linked.write_text("return nil\n", encoding="utf-8")

            with patch.object(
                sys.modules["_corpus"],
                "_is_link_or_reparse",
                side_effect=lambda path, _result: path in (root, linked),
            ):
                with self.assertRaisesRegex(CorpusRootError, "plain directory"):
                    validate_scripts_root(root)

            with patch.object(
                sys.modules["_corpus"],
                "_is_link_or_reparse",
                side_effect=lambda path, _result: path == linked,
            ):
                with self.assertRaisesRegex(CorpusRootError, "linked or reparse"):
                    validate_scripts_root(root)

    def test_shared_scripts_root_rejects_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            with self.assertRaisesRegex(CorpusRootError, "corpus not found or unreadable"):
                validate_scripts_root(missing)

    def test_validate_approves_boundary_before_focused_tests(self) -> None:
        validator.errors.clear()

        def reject_boundary() -> bool:
            validator.errors.append("synthetic unsafe root")
            return False

        with (
            patch.object(validator, "validate_repository_boundary", return_value=[]),
            patch.object(validator, "validate_all_json", return_value=0),
            patch.object(validator, "validate_scripts_tree_boundary", side_effect=reject_boundary),
            patch.object(validator, "run_focused_tests", side_effect=AssertionError("focused tests ran too early")) as focused,
            redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(validator.main([]), 1)
        focused.assert_not_called()

    def test_quest_check_rejects_missing_explicit_scripts_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"
            with patch.object(
                sys,
                "argv",
                ["quest_selector_consumers.py", "--check", "--scripts-root", str(missing)],
            ), redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(quest_analyzer.main(), 1)
            self.assertIn("Lua corpus not found", stderr.getvalue())

    def test_binding_declarations_keep_receiver_class(self) -> None:
        content = '''L0_1 = WidgetBaseClass
function L1_1(A0_2)
  L2_2 = "self"
  L3_2 = "_getProperty_cpp"
  return L2_2, L3_2
end
L0_1 = GroupBaseClass
L1_1 = "_getProperty_cpp"
L2_1 = "_notNative_lua"
L0_1 = _G
L1_1 = "_defineClass_cpp"
'''

        self.assertEqual(
            scan_binding_declarations(content),
            {"_getProperty": ["GroupBaseClass", "WidgetBaseClass"]},
        )

    def test_annotate_emits_binding_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "widget_u.lua").write_text(
                'L0_1 = WidgetBaseClass\nL1_1 = "_getProperty_cpp"\n'
                "L2_1 = _getProperty\n",
                encoding="utf-8",
            )
            registry = root / "registry.json"
            registry.write_text(
                json.dumps({
                    "scripts": {
                        "widget_u": {
                            "ciphered": "x.lua",
                            "classes": ["WidgetBaseClass"],
                            "lineCount": 3,
                        }
                    }
                }),
                encoding="utf-8",
            )
            api_index = root / "api-index.json"
            api_index.write_text(
                json.dumps({
                    "apis": {"_getProperty": [{"bcsId": "BCS-Y-1"}]}
                }),
                encoding="utf-8",
            )
            output = root / "napi.json"

            self.assertEqual(
                annotate_corpus(scripts, registry, api_index, output),
                0,
            )
            entry = json.loads(output.read_text(encoding="utf-8"))["apis"][
                "_getProperty"
            ]
            self.assertEqual(
                entry["bindings"],
                [{"class": "WidgetBaseClass", "script": "widget_u"}],
            )

    def test_annotate_external_source_keeps_sidecars_in_repository_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            external = root / "hydrated"
            external.mkdir()
            tracked_scripts = root / "repo" / "lua" / "scripts"
            (external / "nested").mkdir()
            (external / "nested" / "widget.lua").write_text(
                'L0_1 = WidgetBaseClass\nL1_1 = "_getProperty_cpp"\n'
                "L2_1 = _getProperty\n",
                encoding="utf-8",
            )
            registry = root / "registry.json"
            registry.write_text(
                json.dumps({
                    "scripts": {
                        "nested/widget": {
                            "ciphered": "x.lua",
                            "classes": ["WidgetBaseClass"],
                            "lineCount": 3,
                        }
                    }
                }),
                encoding="utf-8",
            )
            api_index = root / "api-index.json"
            api_index.write_text(
                json.dumps({
                    "apis": {"_getProperty": [{"bcsId": "BCS-Y-1"}]}
                }),
                encoding="utf-8",
            )
            output = root / "napi.json"

            self.assertEqual(
                annotate_corpus(
                    external,
                    registry,
                    api_index,
                    output,
                    tracked_scripts,
                ),
                0,
            )
            self.assertFalse((external / "nested" / "widget.calls.json").exists())
            self.assertTrue(
                (tracked_scripts / "nested" / "widget.calls.json").is_file()
            )

    def test_manifest_reads_external_source_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "hydrated"
            source.mkdir()
            (source / "widget.lua").write_bytes(b"return 'external'\n")

            manifest = build_script_manifest(source)

            self.assertEqual(manifest["scriptCount"], 1)
            self.assertEqual(manifest["scripts"][0]["relativePath"], "lua/scripts/widget.lua")
            self.assertEqual(manifest["scripts"][0]["bytes"], 18)

    def test_text_reading_preserves_corpus_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source_root = root / "source"
            source_root.mkdir()
            (source_root / "bad.lua").write_bytes(b"ok\n\xff\n")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(publish_corpus(source_root, root / "published"), 1)

            scripts_root = root / "scripts"
            scripts_root.mkdir()
            (scripts_root / "bad.lua").write_bytes(b"ok\n\xff\n")
            registry = root / "registry.json"
            registry.write_text('{"scripts": {}}', encoding="utf-8")
            api_index = root / "api-index.json"
            api_index.write_text('{"apis": {}}', encoding="utf-8")
            with self.assertRaises(UnicodeDecodeError):
                annotate_corpus(scripts_root, registry, api_index, root / "calls.json")

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
                result = publish_corpus(source, output)

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
