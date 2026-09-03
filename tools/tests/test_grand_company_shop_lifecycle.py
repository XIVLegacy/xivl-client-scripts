from __future__ import annotations

import json
import os
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "lua" / "scripts"


def compact(relative: str) -> str:
    return " ".join((SCRIPTS / relative).read_text(encoding="utf-8").split())


class GrandCompanyShopLifecycleCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get("XIVL_CORPUS_ABSENT") == "1" or not SCRIPTS.is_dir():
            raise unittest.SkipTest("local retail Lua corpus is absent")

    def test_actor_open_ask_and_close_result_shape(self) -> None:
        actor = compact("chara/npc/populace/populacecompanyshop.lua")
        connector = compact("widget/desktopwidget_connector.lua")
        for event_flag in (8, 11, 0):
            self.assertIn(f"L1_2.eventFlag = {event_flag}", actor)
        self.assertIn('L3_2 = "Ask/GrandCompanyShopWidget" L4_2 = A0_2', actor)
        self.assertIn('L3_2 = "Ask/GrandCompanyShopWidget" L1_2, L2_2', actor)
        self.assertIn("if L1_2 == false then L2_2 = -1", actor)
        self.assertIn('L3_2 = "Ask/GrandCompanyShopWidget" L1_2(L2_2, L3_2)', actor)
        self.assertIn(
            "L6_2 = L4_2.getAskResult L6_2, L7_2 = L6_2(L7_2) "
            "return L5_2, L6_2, L7_2",
            connector,
        )

    def test_catalog_admission_and_sheet_row_identity(self) -> None:
        actor = compact("chara/npc/populace/populacecompanyshop.lua")
        widget = compact("widget/ask/grandcompanyshopwidget.lua")
        self.assertIn("L6_2 = L5_2 + A3_2 L6_2 = L6_2 - 1", actor)
        self.assertIn("if A1_2 == 3 then", actor)
        self.assertIn("L5_2 = L5_2.eventFlag if L5_2 == 0 then", actor)
        self.assertIn("if L12_2 <= L13_2 then L4_2 = true", actor)
        self.assertIn("if L18_2 == true then", widget)
        for prop in ("itemIndex", "essentialRank", "sheetIndex", "pricedata"):
            self.assertIn(f'"{prop}"', widget)

    def test_rank_and_point_checks_are_local_widget_gates(self) -> None:
        widget = compact("widget/ask/grandcompanyshopwidget.lua")
        self.assertIn('L9_2 = "mask"', widget)
        self.assertIn("if L5_2 == 1 then", widget)
        self.assertIn('L9_2 = "essentialRank"', widget)
        self.assertIn("if L5_2 > L6_2 then", widget)
        self.assertIn("L11_2 = 13", widget)
        self.assertIn("L13_2 = A0_2.getPointCount", widget)

    def test_child_numeric_value_is_stored_but_omitted_from_result(self) -> None:
        child = compact("widget/shopeditwidget.lua")
        widget = compact("widget/ask/grandcompanyshopwidget.lua")
        generic = compact("widget/ask/shopbuywidget.lua")
        self.assertIn("L8_2 = 1 L9_2 = A0_2.work L9_2 = L9_2.num1", child)
        self.assertIn("L3_2.buyCount = A2_2", widget)
        self.assertIn("L3_2 = 1 L1_2(L2_2, L3_2)", widget)
        self.assertIn("L1_2 = L2_2.selectedItemSheetIndex", widget)
        self.assertIn("return L1_2 end L0_1.getAskResult", widget)
        self.assertNotIn("buyCount return", widget)
        self.assertIn("L2_2 = L2_2.buycount return L1_2, L2_2", generic)

    def test_update_route_does_not_establish_widget_dispatch(self) -> None:
        connector = compact("widget/desktopwidget_connector.lua")
        widget = compact("widget/ask/grandcompanyshopwidget.lua")
        self.assertIn('L9_2 = "Ask/GrandCompanyShopWidget"', connector)
        self.assertIn(
            "L6_2 = A0_2 L5_2 = A0_2.updatePlayerItem L7_2 = L4_2 "
            "L8_2 = A2_2 L9_2 = A3_2",
            connector,
        )
        self.assertIn("L3_2.updateItemCount = A2_2", widget)
        self.assertIn("L3_2.isUpdateMoney = true", widget)
        self.assertIn("L3_2 = A0_2.updateShopItemList", widget)

    def test_relevant_sidecars_have_no_purchase_mutator_or_command(self) -> None:
        relatives = (
            "chara/npc/populace/populacecompanyshop.calls.json",
            "widget/ask/grandcompanyshopwidget.calls.json",
            "widget/shopeditwidget.calls.json",
        )
        forbidden = {
            "_addItem",
            "_removeItem",
            "_updateWork",
            "_doServerOnCommand",
            "purchaseItem",
        }
        names: set[str] = set()
        for relative in relatives:
            payload = json.loads((SCRIPTS / relative).read_text(encoding="utf-8"))
            names.update(payload["apis"].keys())
        self.assertIn("_getSpecialEventWork", names)
        self.assertIn("_getItemPackageCapacity", names)
        self.assertTrue(forbidden.isdisjoint(names))


if __name__ == "__main__":
    unittest.main()
