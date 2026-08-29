from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

import general_parameter_18_consumers as analyzer  # noqa: E402


class GeneralParameter18ConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not analyzer.SCRIPTS_ROOT.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_complete_corpus_chain(self) -> None:
        report = analyzer.analyze()
        self.assertEqual(report["nativeIndex"], 18)
        self.assertEqual(report["luaIndex"], 19)
        self.assertEqual(report["accessor"], "CharaBaseClass.getNormalDefence")
        self.assertEqual(report["directConsumers"], (
            "StatusWidget.updateBattleParameter",
            "EquipWidget.updateBattleParameter",
        ))
        self.assertEqual(
            report["propertyCallbackBoundary"],
            "empty DesktopWidget battleParameter branch",
        )

    def _mutated_file(self, relative: str, old: str, new: str) -> Path:
        source = (analyzer.SCRIPTS_ROOT / relative).read_text(encoding="utf-8")
        self.assertEqual(source.count(old), 1)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        target = Path(temp.name) / Path(relative).name
        target.write_text(source.replace(old, new), encoding="utf-8")
        return target

    def test_mutation_to_lua_index_is_rejected(self) -> None:
        path = self._mutated_file(
            "chara/charabaseclass_ffxivbattle.lua",
            "  L1_2 = L1_2[19]\n  return L1_2\nend\n\nL0_1.getNormalDefence",
            "  L1_2 = L1_2[18]\n  return L1_2\nend\n\nL0_1.getNormalDefence",
        )
        with self.assertRaisesRegex(analyzer.AnalysisError, "consumer chain"):
            analyzer._verify_ffxivbattle(path)

    def test_mutation_to_parameter_name_row_is_rejected(self) -> None:
        path = self._mutated_file(
            "widget/statuswidget.lua",
            "  L4_2 = 214\n  L5_2 = 15019",
            "  L4_2 = 214\n  L5_2 = 15018",
        )
        with self.assertRaisesRegex(analyzer.AnalysisError, "consumer chain"):
            patterns = (
                'L5_2 = "Label_PhysicsDefense" L6_2 = "TextBlock_Title" '
                "L3_2 = L3_2(L4_2, L5_2, L6_2) L4_2 = 214 L5_2 = 15019",
            )
            analyzer._require_patterns("widget/statuswidget.lua", analyzer._compact(path), patterns)

    def test_mutation_to_generic_argument_is_rejected(self) -> None:
        path = self._mutated_file(
            "widget/equipwidget.lua",
            "  L15_2 = 12\n  L13_2 = L13_2(L14_2, L15_2)",
            "  L15_2 = 16\n  L13_2 = L13_2(L14_2, L15_2)",
        )
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for relative in analyzer.EXPECTED_PHYSICAL_ARGUMENTS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if relative == "widget/equipwidget.lua":
                target.write_bytes(path.read_bytes())
            else:
                target.write_bytes((analyzer.SCRIPTS_ROOT / relative).read_bytes())
        with self.assertRaisesRegex(analyzer.AnalysisError, "argument domain"):
            analyzer._verify_physical_arguments(root)

    def test_mutation_to_update_group_is_rejected(self) -> None:
        path = self._mutated_file(
            "widget/desktopwidget_connector.lua",
            '      elseif L7_2 == "battleParameter" then',
            '      elseif L7_2 == "otherParameter" then',
        )
        with self.assertRaisesRegex(analyzer.AnalysisError, "consumer chain"):
            analyzer._verify_connector(path)


if __name__ == "__main__":
    unittest.main()
