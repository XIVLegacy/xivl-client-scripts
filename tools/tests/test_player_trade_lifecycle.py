from __future__ import annotations

import os
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "lua" / "scripts"


def compact(relative: str) -> str:
    return " ".join((SCRIPTS / relative).read_text(encoding="utf-8").split())


class PlayerTradeLifecycleCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not SCRIPTS.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_invitation_uses_trade_relation_group_and_variation(self) -> None:
        player = compact("chara/player/playerbaseclass_cliprog.lua")
        relation = compact("group/relationgroup/traderelationgroup.lua")
        confirm = compact("command/system/confirmtradecommand.lua")
        for relative in (
            "command/system/tradeoffercommand.lua",
            "command/system/tradeoffercancelcommand.lua",
        ):
            can_fire = compact(relative)
            for pattern in (
                "A1_2.isPlayer",
                "A1_2.isMyPlayer",
                "A6_2 == nil",
                "A6_2._isAlive",
                "A1_2.isLiving",
                "A6_2.isLiving",
                "A1_2.isActiveMode",
            ):
                self.assertIn(pattern, can_fire)
        self.assertIn("L3_2 = 50002 L1_2 = L1_2(L2_2, L3_2)", player)
        self.assertIn(
            'L3_2 = 200001 L4_2 = "work" L5_2 = "_globalTemp" L6_2 = "host"',
            relation,
        )
        self.assertIn(
            'L3_2 = 200002 L4_2 = "work" L5_2 = "_globalTemp" '
            'L6_2 = "variableCommand"',
            relation,
        )
        self.assertIn("A1_2.getConfirmTradeCommandVariation", confirm)
        self.assertIn("L12_2 = A2_2 == L11_2 return L12_2", confirm)
        self.assertNotIn("if A2_2 == nil", confirm)
        self.assertIn("30000 <= L1_2 and L1_2 <= 39999", confirm)
        self.assertIn("L0_1.fire = L1_1", confirm)

    def test_native_tray_callbacks_keep_the_widget_boundary(self) -> None:
        command = compact("command/system/tradeexecutecommand.lua")
        connector = compact("widget/desktopwidget_connector.lua")
        for callback in (
            "dictateOpenTradeWidget",
            "dictateCloseTradeWidget",
            "checkReplyTradeWidget",
            "dictateNoticeTradeWidget",
        ):
            self.assertIn(callback, command)
            self.assertIn(callback, connector)
        self.assertIn('L5_2 = 4 L6_2 = "TradeWidget"', connector)
        self.assertIn("A1_2._getTradingItem L7_2 = A2_2", connector)

    def test_widget_operation_result_map_is_stable(self) -> None:
        source = compact("widget/tradewidget.lua")
        expected = (
            "L2_2 = 1 L3_2 = L1_2",
            "L1_2 = 2 L2_2 = 0",
            "L2_2 = 3 L3_2 = L1_2",
            "L2_2 = 4 L3_2 = L1_2 L4_2 = 100",
            "L5_2.chosenOperation = 11",
            "L5_2.chosenOperation = 12",
            "L5_2.chosenOperation = 13",
        )
        for pattern in expected:
            self.assertIn(pattern, source)
        self.assertIn("L4_2.reservedSlot = L5_2", source)
        self.assertIn("L3_2.chosenOperation = 4", source)
        self.assertIn(
            "L2_2 = L1_2 L3_2 = nil L4_2 = nil L5_2 = nil L6_2 = nil "
            "return L2_2, L3_2, L4_2, L5_2, L6_2",
            source,
        )
        self.assertIn(
            "L2_2 = 3 L3_2 = L1_2 L4_2 = A0_2.work L4_2 = L4_2.chosenPackage "
            "L5_2 = A0_2.work L5_2 = L5_2.chosenItem L6_2 = A0_2.work "
            "L6_2 = L6_2.chosenStack return L2_2, L3_2, L4_2, L5_2, L6_2",
            source,
        )
        self.assertIn(
            "L2_2 = 4 L3_2 = L1_2 L4_2 = 100 L5_2 = A0_2.work "
            "L5_2 = L5_2.chosenItem L6_2 = A0_2.work L6_2 = L6_2.chosenStack "
            "return L2_2, L3_2, L4_2, L5_2, L6_2",
            source,
        )

    def test_published_connector_truncates_item_and_gil_results(self) -> None:
        command = compact("command/system/tradeexecutecommand.lua")
        connector = compact("widget/desktopwidget_connector.lua")
        self.assertIn(
            "L3_2, L4_2, L5_2, L6_2, L7_2, L8_2 = L3_2(L4_2, L5_2)",
            command,
        )
        self.assertIn(
            "L4_2, L5_2 = L4_2(L5_2) return L3_2, L4_2, L5_2",
            connector,
        )

    def test_reply_codes_and_fixed_state_transitions_are_stable(self) -> None:
        command = compact("command/system/tradeexecutecommand.lua")
        widget = compact("widget/tradewidget.lua")
        reply_codes = {
            "set": 103,
            "back": 101,
            "fix": 112,
            "targetfix": 90,
            "reedit": 91,
            "doedit": 113,
            "noabort": 211,
            "noreedit": 213,
            "cantset": 203,
            "cantback": 201,
        }
        for reply, code in reply_codes.items():
            self.assertIn(f'A2_2 == "{reply}"', command)
            self.assertIn(f"L9_2 = {code}", command)
        self.assertIn("L5_2 = A0_2.tradeFix L7_2 = true", widget)
        self.assertIn("L5_2 = A0_2.tradeFix L7_2 = false", widget)
        self.assertIn("L5_2 = A0_2.tradeDestFix L7_2 = true", widget)
        self.assertIn("L5_2 = A0_2.tradeDestFix L7_2 = false", widget)
        self.assertIn(
            "L1_2 = L1_2.sourceFix if L1_2 == true then L1_2 = A0_2.work "
            "L1_2 = L1_2.destinationFix if L1_2 == true then L1_2 = true return L1_2",
            widget,
        )
        self.assertIn(
            "L5_2 = L5_2.sourceFix if L5_2 == true then L5_2 = A0_2.work "
            "L5_2.chosenOperation = 13",
            widget,
        )

    def test_close_and_relation_finalize_do_not_claim_server_teardown(self) -> None:
        command = compact("command/system/tradeexecutecommand.lua")
        relation = compact("group/relationgroup/traderelationgroup.lua")
        self.assertIn("L2_2.dictateCloseTradeWidget", command)
        self.assertIn("L0_1._onFinalize = L1_1", relation)
        self.assertIn(
            "L1_2 = desktopWidget L2_2 = L1_2 "
            "L1_2 = L1_2.processUpdateConfirmTradeCommandVariation "
            "L1_2(L2_2) end L0_1._onFinalize = L1_1",
            relation,
        )


if __name__ == "__main__":
    unittest.main()
