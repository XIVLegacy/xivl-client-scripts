from __future__ import annotations

import os
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(
    os.environ.get("XIVL_LUA_SCRIPTS_DIR", str(REPO / "lua" / "scripts"))
).expanduser().absolute()


def compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class GuildleveLifecycleCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not SCRIPTS.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_publisher_confirmation_only_updates_presentation_work(self) -> None:
        source = compact(
            SCRIPTS / "chara" / "npc" / "populace" / "populaceguildlevepublisher.lua"
        )
        self.assertIn(
            "L10_2 = L10_2.askJournalDetailWidget L12_2 = 9 L13_2 = A1_2 "
            "L14_2 = A2_2 L15_2 = A3_2 L16_2 = A4_2 L17_2 = A5_2 "
            "L18_2 = A6_2 L19_2 = A7_2 L20_2 = A8_2",
            source,
        )
        self.assertIn("L11_2.nowCompleteFlag = A8_2", source)
        self.assertIn("return L10_2", source)

    def test_aetheryte_start_and_reward_argument_routes_are_stable(self) -> None:
        source = compact(
            SCRIPTS / "chara" / "npc" / "object" / "aetheryte" / "aetherytebaseclass.lua"
        )
        self.assertIn(
            'L10_2 = L10_2.askEventModeWidgetYield L12_2 = "Ask/GuildleveStartWidget" '
            "L13_2 = 1 L14_2 = A1_2 L15_2 = A2_2 L16_2 = A3_2 "
            "L17_2 = A4_2 L18_2 = A5_2 L19_2 = A6_2 L20_2 = A7_2 "
            "L21_2 = A8_2 L22_2 = 0 L23_2 = A9_2",
            source,
        )
        self.assertIn("L13_2.guildleveId = L25_2", source)
        self.assertIn("L24_2.difficulty = A12_2", source)
        for position in range(1, 12):
            self.assertIn(
                f"L{24 + position}_2 = A{position}_2",
                source,
            )
        self.assertIn(
            'L13_2 = L13_2.askEventModeWidgetYield '
            'L15_2 = "Ask/ContentRewardWidget"',
            source,
        )

    def test_player_completion_request_round_trip_is_stable(self) -> None:
        source = compact(SCRIPTS / "chara" / "player" / "playerbaseclass.lua")
        self.assertIn(
            'L3_2 = "questCompleteG" L4_2 = 1 + A1_2 A1_2 = L4_2 - 120001',
            source,
        )
        self.assertIn(
            'L4_2 = A0_2._updateWork L6_2 = "playerWork" L7_2 = L3_2 '
            "L8_2 = A1_2 L9_2 = A2_2",
            source,
        )
        self.assertIn(
            'elseif A1_2 == "questCompleteG" then L4_2 = desktopWidget',
            source,
        )
        self.assertIn(
            'if A1_2 == "requestedData" then L3_2, L4_2 = ... L5_2 = desktopWidget',
            source,
        )

    def test_server_helper_names_are_absent_from_retail_corpus(self) -> None:
        self.assertFalse(
            (SCRIPTS / "director" / "guildleve" / "guildlevecommon.lua").exists()
        )
        needles = ("GuildleveCommon", "GetGuildleveGamedata")
        found = {needle: [] for needle in needles}
        for path in SCRIPTS.rglob("*.lua"):
            source = path.read_text(encoding="utf-8")
            for needle in needles:
                if needle in source:
                    found[needle].append(path.relative_to(SCRIPTS).as_posix())
        self.assertEqual(found, {needle: [] for needle in needles})


if __name__ == "__main__":
    unittest.main()
