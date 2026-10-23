from __future__ import annotations

import struct
import sys
import unittest
from copy import deepcopy
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_quest_contracts as contracts  # noqa: E402


def abc(name: str, a: int = 0, b: int = 0, c: int = 0) -> int:
    return contracts.OPCODES.index(name) | a << 6 | c << 14 | b << 23


def abx(name: str, a: int, bx: int) -> int:
    return contracts.OPCODES.index(name) | a << 6 | bx << 14


def chunk(code: list[int], constants: list, parameters: int = 1) -> bytes:
    def u32(value: int) -> bytes:
        return struct.pack("<I", value)

    body = b"".join(u32(value) for value in code)
    values = b""
    for value in constants:
        if isinstance(value, str):
            encoded = value.encode() + b"\0"
            values += b"\4" + u32(len(encoded)) + encoded
        else:
            values += b"\3" + struct.pack("<d", value)
    return (
        bytes.fromhex("1b4c75615100010404040800")
        + u32(0) * 3
        + bytes([0, parameters, 0, 8])
        + u32(len(code))
        + body
        + u32(len(constants))
        + values
        + u32(0) * 4
    )


class QuestBytecodeTests(unittest.TestCase):
    def scene_branch(self, other_key: str) -> dict:
        data = chunk(
            [
                abc("SELF", 1, 0, 256),
                abc("TEST", 0),
                abx("JMP", 0, 131071 + 2),
                abx("LOADK", 3, 1),
                abx("JMP", 0, 131071 + 1),
                abx("LOADK", 3, 2),
                abx("LOADK", 4, 3),
                abc("CALL", 1, 4, 1),
                abc("RETURN", 0, 1),
            ],
            ["startNQCutScene", "firstKey", other_key, 1],
        )
        return contracts.analyze_chunk(data, [{"key": "firstKey", "rowId": 7}])

    def test_conflicting_branch_constants_remain_unknown(self) -> None:
        call = self.scene_branch("otherKey")["calls"][0]
        self.assertEqual(call["joinStatus"], "dynamic-key")
        self.assertIn("unknown", call["sceneKey"])
        self.assertEqual(call["replayRowIds"], [])

    def test_equal_branch_constants_and_exact_case_replay(self) -> None:
        call = self.scene_branch("firstKey")["calls"][0]
        self.assertEqual(call["sceneKey"], "firstKey")
        self.assertEqual(call["replayRowIds"], [7])
        data = chunk(
            [
                abc("SELF", 1, 0, 256),
                abx("LOADK", 3, 1),
                abx("LOADK", 4, 2),
                abc("CALL", 1, 4, 1),
                abc("RETURN", 0, 1),
            ],
            ["startNQCutScene", "FirstKey", 1],
        )
        call = contracts.analyze_chunk(data, [{"key": "firstKey", "rowId": 7}])[
            "calls"
        ][0]
        self.assertEqual(call["joinStatus"], "unmatched-literal")

    def test_caller_argument_is_not_a_literal(self) -> None:
        data = chunk(
            [
                abc("SELF", 2, 0, 256),
                abc("MOVE", 4, 1),
                abx("LOADK", 5, 1),
                abc("CALL", 2, 4, 1),
                abc("RETURN", 0, 1),
            ],
            ["startNQCutScene", 1],
            parameters=2,
        )
        call = contracts.analyze_chunk(data, [])["calls"][0]
        self.assertEqual(
            call["sceneKey"], {"unknown": "caller-argument", "parameter": 1}
        )

    def test_comparison_is_not_a_complete_selector_domain(self) -> None:
        data = chunk(
            [
                abc("SELF", 1, 0, 256),
                abc("MOVE", 3, 0),
                abx("LOADK", 4, 1),
                abx("LOADK", 5, 2),
                abc("CALL", 1, 5, 2),
                abc("EQ", 0, 1, 259),
                abx("JMP", 0, 131071),
                abc("RETURN", 1, 2),
            ],
            ["ask", 69, 2, 1],
        )
        analysis = contracts.analyze_chunk(data, [])
        self.assertEqual(analysis["selectorResultSets"][0]["comparedLiterals"], [1])
        self.assertEqual(
            analysis["selectorResultSets"][0]["completeResultDomain"], "unknown"
        )
        self.assertTrue(analysis["resultComparisons"][0]["skipWhen"])
        self.assertEqual(
            analysis["returnSites"][0]["values"][0]["unknown"], "call-result"
        )

    def test_malformed_chunks_fail(self) -> None:
        for data in (
            b"",
            b"\x1bLuaQ" + b"\0" * 50,
            chunk([abc("RETURN", 0, 1)], [])[:-1],
        ):
            with (
                self.subTest(size=len(data)),
                self.assertRaises(contracts.ContractError),
            ):
                contracts.analyze_chunk(data, [])


class RetainedQuestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = contracts.load(contracts.OUTPUT)
        cls.schema = contracts.load(
            contracts.ROOT / "schemas/quest_contracts.schema.json"
        )
        cls.validator = jsonschema.Draft202012Validator(cls.schema)
        # Keep references rooted in the complete schema for subtree checks.
        cls.call_validator = cls.validator.evolve(schema={"$ref": "#/$defs/call"})
        cls.script_validator = cls.validator.evolve(schema={"$ref": "#/$defs/script"})

    def resign(self, report: dict) -> dict:
        report["contentSha256"] = contracts.json_digest(
            {k: v for k, v in report.items() if k != "contentSha256"}
        )
        return report

    def test_retained_report_and_schema(self) -> None:
        self.assertEqual(contracts.validate_retained(self.report), [])
        self.validator.validate(self.report)
        self.assertEqual(self.report["summary"]["includedScripts"], 274)
        self.assertEqual(self.report["summary"]["scenarioMembers"], 620)

    def test_omitted_member_and_false_quest_owner_are_rejected(self) -> None:
        report = deepcopy(self.report)
        report["scripts"].pop()
        self.assertIn(
            "included script set mismatch",
            contracts.validate_retained(self.resign(report)),
        )
        report = deepcopy(self.report)
        report["scripts"][0]["questId"] = 111201
        self.assertTrue(
            any(
                "unsupported quest identity" in p
                for p in contracts.validate_retained(self.resign(report))
            )
        )

    def test_changed_join_and_locator_are_rejected_after_resigning(self) -> None:
        report = deepcopy(self.report)
        script = next(
            r
            for r in report["scripts"]
            if any(c["kind"] == "scene" for c in r["calls"])
        )
        call = next(c for c in script["calls"] if c["kind"] == "scene")
        call["replayRowIds"] = [999]
        call["offset"] += 1
        problems = contracts.validate_retained(self.resign(report))
        self.assertTrue(any("replay join mismatch" in p for p in problems))
        self.assertTrue(any("bytecode locator mismatch" in p for p in problems))

    def test_unknown_values_require_provenance(self) -> None:
        validator = self.call_validator
        report = deepcopy(self.report)
        call = next(c for r in report["scripts"] for c in r["calls"])
        call["arguments"][0] = {"unknown": "caller-argument"}
        self.assertTrue(list(validator.iter_errors(call)))

    def test_relabelled_replay_join_is_rejected_after_resigning(self) -> None:
        report = deepcopy(self.report)
        call = next(
            c
            for r in report["scripts"]
            for c in r["calls"]
            if c.get("joinStatus") == "exact-key-match"
        )
        call["joinStatus"] = "dynamic-key"
        self.resign(report)
        self.call_validator.validate(call)
        problems = contracts.validate_retained(report)
        self.assertNotIn("contract content digest mismatch", problems)
        self.assertTrue(any("replay join status mismatch" in p for p in problems))

    def test_fixed_return_arity_is_rejected_after_resigning(self) -> None:
        report = deepcopy(self.report)
        returned = report["scripts"][0]["returnSites"][0]
        self.assertEqual(returned["values"], [])
        returned["resultCount"] = 99
        self.resign(report)
        self.script_validator.validate(report["scripts"][0])
        problems = contracts.validate_retained(report)
        self.assertNotIn("contract content digest mismatch", problems)
        self.assertTrue(any("return result arity mismatch" in p for p in problems))

    def test_impossible_reachability_is_rejected_after_resigning(self) -> None:
        report = deepcopy(self.report)
        prototype = report["scripts"][0]["prototypeCensus"][0]
        prototype["reachableInstructions"] = 999999
        self.resign(report)
        self.script_validator.validate(report["scripts"][0])
        problems = contracts.validate_retained(report)
        self.assertNotIn("contract content digest mismatch", problems)
        self.assertTrue(
            any("bytecode reachability bounds mismatch" in p for p in problems)
        )

    def test_retail_dragoon_message_anomaly_is_preserved(self) -> None:
        script = next(
            r for r in self.report["scripts"] if r["script"].endswith("drg/drg0j4.lua")
        )
        reference = next(
            r for r in script["questPresentationReferences"] if r["messageId"] == 51132
        )
        self.assertEqual(reference["questId"], 111304)
        self.assertIsNone(script["questId"])


if __name__ == "__main__":
    unittest.main()
