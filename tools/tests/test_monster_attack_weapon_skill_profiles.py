from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

import jsonschema

TOOLS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

import monster_attack_weapon_skill_profiles as profile  # noqa: E402


class MonsterAttackWeaponSkillProfileTests(unittest.TestCase):
    def test_retained_report_is_pinned_and_compact(self) -> None:
        report = json.loads(profile.OUTPUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(profile.validate_retained(report), [])
        self.assertEqual(report["summary"], {
            "getterCount": 6,
            "overrideGroupCount": 12,
            "overrideCommandCount": 57,
        })
        self.assertEqual(
            report["getterRules"]["getCommandInformation"]["overrides"][0]["result"],
            -1,
        )
        self.assertEqual(
            report["getterRules"]["getRangeWidth"]["overrides"][0]["commandIds"],
            [23297, 23479],
        )
        self.assertEqual(
            report["getterRules"]["getPartsDamageAdjust"]["overrides"][0]["result"],
            [1, 0],
        )

    def test_report_matches_schema(self) -> None:
        schema = json.loads(profile.SCHEMA_PATH.read_text(encoding="utf-8"))
        report = json.loads(profile.OUTPUT_PATH.read_text(encoding="utf-8"))
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(report))
        self.assertEqual(errors, [])

    def test_retained_getter_mutation_is_rejected(self) -> None:
        report = json.loads(profile.OUTPUT_PATH.read_text(encoding="utf-8"))
        mutation = deepcopy(report)
        mutation["getterRules"]["getFrequency"]["overrides"][0]["result"] = 9
        self.assertIn("getter rules disagree", profile.validate_retained(mutation))

    def test_retained_source_row_mutation_is_rejected(self) -> None:
        report = json.loads(profile.OUTPUT_PATH.read_text(encoding="utf-8"))
        manifest = json.loads(profile.SCRIPTS_MANIFEST_PATH.read_text(encoding="utf-8"))
        row = next(
            row
            for row in manifest["scripts"]
            if row["relativePath"] == profile.SOURCE_PATH
        )
        row["lineCount"] += 1
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "scripts.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(profile, "SCRIPTS_MANIFEST_PATH", manifest_path):
                problems = profile.validate_retained(report)
        self.assertTrue(
            any("retained source row disagrees" in problem for problem in problems)
        )

    def test_unknown_top_level_field_is_rejected(self) -> None:
        report = json.loads(profile.OUTPUT_PATH.read_text(encoding="utf-8"))
        mutation = deepcopy(report)
        mutation["unexpected"] = True
        problems = profile.validate_retained(mutation)
        self.assertTrue(
            any("additional properties" in problem.lower() for problem in problems)
        )

    def test_mutated_exact_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / profile.SOURCE_RELATIVE
            source.parent.mkdir(parents=True)
            source.write_bytes(b"-- changed source\n")
            with self.assertRaisesRegex(profile.AnalysisError, "sha256"):
                profile.analyze(root)

    def test_external_source_rebuild_is_byte_stable(self) -> None:
        configured = os.environ.get("XIVL_LUA_SCRIPTS_DIR")
        if configured:
            root = Path(configured)
        else:
            root = profile.SCRIPTS_ROOT
        source = root / profile.SOURCE_RELATIVE
        if not source.is_file():
            self.skipTest("exact decoded Lua source is absent")
        report = profile.analyze(root)
        self.assertEqual(profile.render_json(report), profile.OUTPUT_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main()
