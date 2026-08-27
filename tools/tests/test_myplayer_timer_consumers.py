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

import myplayer_timer_consumers as analyzer  # noqa: E402


class MyPlayerTimerConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not analyzer.SCRIPTS_ROOT.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_report_rebuild_is_stable(self) -> None:
        expected = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(analyzer.analyze(), expected)

    def test_all_occupancy_arguments_map_to_the_native_vector(self) -> None:
        report = analyzer.analyze()
        rows = report["occupancyArgumentMap"]
        self.assertEqual([row["luaArgument"] for row in rows], list(range(1, 17)))
        self.assertEqual([row["nativeVectorIndex"] for row in rows], list(range(16)))

    def test_schema_rejects_inconsistent_callsite_shapes(self) -> None:
        schema = json.loads(
            (analyzer.REPO_ROOT / "schemas" / "myplayer_timer_consumers.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = jsonschema.Draft202012Validator(schema)
        report = json.loads(analyzer.OUTPUT_PATH.read_text(encoding="utf-8"))

        scalar_mutation = deepcopy(report)
        scalar_mutation["directCallsites"][0]["argument"] = 1
        self.assertTrue(list(validator.iter_errors(scalar_mutation)))

        occupancy_mutation = deepcopy(report)
        fixed = next(
            row
            for row in occupancy_mutation["directCallsites"]
            if row["callback"] == "_getOccupancyContentsTime"
            and isinstance(row["argument"], int)
        )
        del fixed["nativeVectorIndex"]
        self.assertTrue(list(validator.iter_errors(occupancy_mutation)))

    def test_mutation_to_out_of_range_argument_is_rejected(self) -> None:
        source_path = analyzer.SCRIPTS_ROOT / "widget" / "pcmatchingeditwidget.lua"
        source = source_path.read_text(encoding="utf-8")
        old = "  L8_2 = 16\n  L6_2 = L6_2(L7_2, L8_2)"
        self.assertEqual(source.count(old), 1)
        with tempfile.TemporaryDirectory() as temp:
            mutated = Path(temp) / source_path.name
            mutated.write_text(source.replace(old, old.replace("16", "17")), encoding="utf-8")
            spec = analyzer.CALLSITE_SPECS[("widget/pcmatchingeditwidget.lua", 842)]
            with self.assertRaisesRegex(analyzer.AnalysisError, "expected argument 16"):
                analyzer._verify_callsite_shape(mutated, 842, spec)

    def test_mutation_to_status_propagation_is_rejected(self) -> None:
        source_path = analyzer.SCRIPTS_ROOT / "widget" / "statuswidget.lua"
        source = source_path.read_text(encoding="utf-8")
        old = "  L6_2 = 16\n  L7_2 = A1_2\n  L3_2 = L3_2(L4_2, L5_2, L6_2, L7_2)"
        self.assertEqual(source.count(old), 1)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "widget" / "statuswidget.lua"
            target.parent.mkdir(parents=True)
            target.write_text(source.replace(old, old.replace("16", "17")), encoding="utf-8")
            with self.assertRaisesRegex(analyzer.AnalysisError, "argument 16"):
                analyzer._verify_status_propagation(root)

    def test_mutation_to_hamlet_remap_is_rejected(self) -> None:
        source_path = analyzer.SCRIPTS_ROOT / "widget" / "statuswidget.lua"
        source = source_path.read_text(encoding="utf-8")
        old = "  if L12_2 == 8 then\n    L11_2 = 2"
        self.assertEqual(source.count(old), 1)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "widget" / "statuswidget.lua"
            target.parent.mkdir(parents=True)
            target.write_text(source.replace(old, old[:-1] + "4"), encoding="utf-8")
            with self.assertRaisesRegex(analyzer.AnalysisError, "L11_2 = 2"):
                analyzer._verify_status_propagation(root)

    def test_mutation_to_warp_subtraction_is_rejected(self) -> None:
        relatives = (
            "chara/player/playerbaseclass.lua",
            "command/system/teleportcommand.lua",
            "widget/desktopwidget_connector.lua",
            "widget/mainmenuwidget.lua",
            "widget/statuswidget.lua",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in relatives:
                source = (analyzer.SCRIPTS_ROOT / relative).read_text(encoding="utf-8")
                if relative == "chara/player/playerbaseclass.lua":
                    source = source.replace("  L4_2 = L1_2 - L4_2", "  L4_2 = L1_2 + L4_2", 1)
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source, encoding="utf-8")
            with self.assertRaisesRegex(analyzer.AnalysisError, "scalar consumer chain"):
                analyzer._verify_scalar_chains(root)


if __name__ == "__main__":
    unittest.main()
