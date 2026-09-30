from __future__ import annotations

import hashlib
import json
import os
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retail_script import decode_lpb  # noqa: E402


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = (
    Path(os.environ.get("XIVL_LUA_SCRIPTS_DIR", str(REPO / "lua" / "scripts")))
    .expanduser()
    .absolute()
)


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
            'L3_2 = 200002 L4_2 = "work" L5_2 = "_globalTemp" L6_2 = "variableCommand"',
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

    def test_canonical_decompile_loses_the_open_result_tail(self) -> None:
        # Retail forwards six values; see docs/player-trade-lifecycle.md.
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


class PlayerTradeRetailArityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        configured = os.environ.get("XIVL_TRADE_LPB_ROOT")
        if configured is None:
            raise unittest.SkipTest("explicit retail client/script root is absent")
        if not configured:
            raise ValueError("explicit retail client/script root is empty")
        cls.root = Path(configured).expanduser().absolute()
        cls.coverage = json.loads(
            (REPO / "manifests" / "retail_lua_coverage.json").read_text(
                encoding="utf-8"
            )
        )

    def payload(self, relative: str) -> bytes:
        matches = [
            row
            for row in self.coverage["resources"]
            if row.get("decodedScriptPath") == f"lua/scripts/{relative}"
        ]
        self.assertEqual(len(matches), 1)
        row = matches[0]
        original = (self.root / row["resourcePath"]).read_bytes()
        self.assertEqual(len(original), row["bytes"])
        self.assertEqual(hashlib.sha256(original).hexdigest().upper(), row["sha256"])
        decoded = decode_lpb(original)
        self.assertIsNotNone(decoded)
        assert decoded is not None
        self.assertEqual(len(decoded), row["wrapper"]["decodedPayloadBytes"])
        self.assertEqual(
            hashlib.sha256(decoded).hexdigest().upper(),
            row["wrapper"]["decodedPayloadSha256"],
        )
        self.assertEqual(decoded[:12], bytes.fromhex("1b4c75615100010404040800"))
        return decoded

    def assert_instruction(
        self, payload: bytes, offset: int, expected: tuple[int, int, int, int]
    ) -> None:
        word = struct.unpack_from("<I", payload, offset)[0]
        operands = (
            word & 63,
            (word >> 6) & 255,
            (word >> 23) & 511,
            (word >> 14) & 511,
        )
        self.assertEqual(operands, expected, f"instruction at {offset:#x}")

    def test_widget_returns_five_values_for_item_and_gil(self) -> None:
        payload = self.payload("widget/tradewidget.lua")
        # Child 31 PCs 49/67: RETURN R2..R6. Locators are in the trade contract.
        for offset in (0x4C81, 0x4CC9):
            self.assert_instruction(payload, offset, (30, 2, 6, 0))

    def test_connector_forwards_ready_and_all_widget_results(self) -> None:
        payload = self.payload("widget/desktopwidget_connector.lua")
        # Child 216 PCs 15-18: true, SELF getAskResult, open CALL, open RETURN.
        self.assert_instruction(payload, 0x1ABDF, (2, 3, 1, 0))
        self.assert_instruction(payload, 0x1ABE3, (11, 4, 2, 262))
        self.assert_instruction(payload, 0x1ABE7, (28, 4, 2, 0))
        self.assert_instruction(payload, 0x1ABEB, (30, 3, 0, 0))

    def test_command_receives_six_results_and_preserves_stack(self) -> None:
        payload = self.payload("command/system/tradeexecutecommand.lua")
        # Child 4 PC5 receives R3..R8; PCs 100-103 return stack/package/item.
        self.assert_instruction(payload, 0x57D, (28, 3, 3, 7))
        self.assert_instruction(payload, 0x6F9, (0, 14, 8, 0))
        self.assert_instruction(payload, 0x6FD, (0, 15, 6, 0))
        self.assert_instruction(payload, 0x701, (0, 16, 7, 0))
        self.assert_instruction(payload, 0x705, (30, 10, 8, 0))


if __name__ == "__main__":
    unittest.main()
