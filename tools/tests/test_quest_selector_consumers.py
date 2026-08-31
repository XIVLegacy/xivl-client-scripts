from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import jsonschema

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import quest_selector_consumers as analyzer  # noqa: E402


class QuestSelectorConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not analyzer.SCRIPTS_ROOT.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_complete_message_census(self) -> None:
        rows = analyzer.analyze_script_consumers()
        self.assertEqual(sum(row["messageId"] == 51130 for row in rows), 7)
        self.assertEqual(sum(row["messageId"] == 51131 for row in rows), 42)
        self.assertEqual(sum(row["messageId"] == 51132 for row in rows), 42)
        two_level = [row for row in rows if row["messageId"] == 51130]
        self.assertEqual({row["primaryLevel"] for row in two_level}, {30})
        self.assertEqual({row["secondaryLevel"] for row in two_level}, {15})

    def test_schema_rejects_secondary_fields_on_primary_only_message(self) -> None:
        schema = json.loads(
            (analyzer.REPO_ROOT / "schemas" / "quest_selector_consumers.schema.json").read_text(encoding="utf-8")
        )
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        mutation = deepcopy(report)
        row = next(item for item in mutation["messageConsumers"] if item["messageId"] == 51131)
        row["secondaryLevel"] = 15
        self.assertTrue(list(jsonschema.Draft202012Validator(schema).iter_errors(mutation)))

    def test_selector_and_level_mutations_are_rejected(self) -> None:
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        for field, value in (("secondaryLevel", 10), ("secondaryClassId", 8)):
            mutation = deepcopy(report)
            mutation["namedRows"][0][field] = value
            with self.subTest(field=field):
                self.assertTrue(any(
                    problem.startswith("selector alignment disagrees:")
                    for problem in analyzer.validate_retained(mutation)
                ))

        mutation = deepcopy(report)
        advance = next(
            row for row in mutation["messageConsumers"]
            if row["messageId"] == 51132 and row["questId"] == 111201
        )
        advance["primarySelectorId"] = 8
        self.assertTrue(any(
            problem.startswith("selector alignment disagrees:")
            for problem in analyzer.validate_retained(mutation)
        ))

    def test_duplicate_named_row_id_is_rejected(self) -> None:
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        report["namedRows"][1]["questId"] = 111203
        self.assertIn("named selector row set disagrees", analyzer.validate_retained(report))

    def test_later_row_metadata_mutation_is_rejected(self) -> None:
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        report["namedRows"][1]["secondaryClassId"] = 8
        self.assertIn(
            "named selector row content disagrees", analyzer.validate_retained(report)
        )

    def test_non_worldmaster_sink_is_rejected(self) -> None:
        source_path = analyzer.SCRIPTS_ROOT / "quest" / "scenario" / "war" / "war0j1.lua"
        lines = source_path.read_text(encoding="utf-8").splitlines()
        index = next(i for i, line in enumerate(lines) if line.strip() == "L6_2 = 51130")
        lines[index - 4] = "  L3_2 = fakeMaster"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "war0j1.lua"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(analyzer.AnalysisError, "not worldMaster.say"):
                analyzer._message_at(path, index, 51130)

    def test_retained_report_pins_and_counts(self) -> None:
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(analyzer.validate_retained(report), [])


if __name__ == "__main__":
    unittest.main()
