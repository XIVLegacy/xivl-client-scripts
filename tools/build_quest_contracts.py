#!/usr/bin/env python3
"""Build or validate retained class, job, and company quest contracts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import sys
import zipfile
from collections import Counter, deque
from pathlib import Path

import jsonschema

from retail_script import decode_lpb

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data/quest_contracts.json"
FAMILIES = {
    "class": "acn alc arc bsm cnj cul exc fsh gla gld hrv lnc min pgl tan thm wdk wvr".split(),
    "job": "blm brd drg mnk pld war whm".split(),
    "grand-company": "com gcg gcl gcu".split(),
}
PINS = [
    "manifests/scripts.json",
    "manifests/retail_lua_coverage.json",
    "manifests/private_lua_corpus.json",
    "manifests/quest_selector_consumers.json",
]
REPLAY_SHA256 = "2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37"
OPCODES = (
    "MOVE LOADK LOADBOOL LOADNIL GETUPVAL GETGLOBAL GETTABLE SETGLOBAL SETUPVAL "
    "SETTABLE NEWTABLE SELF ADD SUB MUL DIV MOD POW UNM NOT LEN CONCAT JMP EQ LT LE "
    "TEST TESTSET CALL TAILCALL RETURN FORLOOP FORPREP TFORLOOP SETLIST CLOSE CLOSURE VARARG"
).split()
TEXT_METHODS = {
    "say",
    "ask",
    "askRestrictChoices",
    "askExtendWidget",
    "sayFreeDisplayName",
    "notify",
    "tell",
    "tellByNpcLinkshellChat",
}


class ContractError(ValueError):
    """An input or retained contract violates the evidence boundary."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_digest(value: object) -> str:
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class ChunkReader:
    """Read the fixed Lua 5.1 chunk representation used by the retained LPBs."""

    def __init__(self, data: bytes):
        if data[:12] != bytes.fromhex("1b4c75615100010404040800"):
            raise ContractError("unsupported Lua chunk header")
        self.data = data
        self.pos = 12

    def read(self, count: int) -> bytes:
        result = self.data[self.pos : self.pos + count]
        if len(result) != count:
            raise ContractError("truncated Lua chunk")
        self.pos += count
        return result

    def u32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def string(self) -> str | None:
        size = self.u32()
        if not size:
            return None
        value = self.read(size)
        if value[-1] != 0:
            raise ContractError("unterminated Lua string")
        return value[:-1].decode("utf-8")

    def prototype(self, path: str = "root") -> dict:
        self.string()
        first, last = self.u32(), self.u32()
        upvalues, parameters, vararg, stack = self.read(4)
        count = self.u32()
        offset = self.pos
        code = [self.u32() for _ in range(count)]
        constants = []
        for _ in range(self.u32()):
            tag = self.read(1)[0]
            if tag == 0:
                value = None
            elif tag == 1:
                value = bool(self.read(1)[0])
            elif tag == 3:
                value = struct.unpack("<d", self.read(8))[0]
                if value.is_integer():
                    value = int(value)
            elif tag == 4:
                value = self.string()
            else:
                raise ContractError("unsupported Lua constant")
            constants.append(value)
        children = [self.prototype(f"{path}/proto{i}") for i in range(self.u32())]
        lines = [self.u32() for _ in range(self.u32())]
        for _ in range(self.u32()):
            self.string()
            self.u32()
            self.u32()
        for _ in range(self.u32()):
            self.string()
        return dict(
            path=path,
            first=first,
            last=last,
            upvalues=upvalues,
            parameters=parameters,
            vararg=vararg,
            stack=stack,
            code=code,
            offset=offset,
            constants=constants,
            children=children,
            lines=lines,
        )


def walk(prototype: dict):
    yield prototype
    for child in prototype["children"]:
        yield from walk(child)


def instruction(word: int) -> tuple[str, int, int, int, int]:
    opcode = word & 63
    if opcode >= len(OPCODES):
        raise ContractError("unsupported Lua opcode")
    return (
        OPCODES[opcode],
        (word >> 6) & 255,
        (word >> 23) & 511,
        (word >> 14) & 511,
        word >> 14,
    )


def literal(value: object) -> tuple:
    return ("literal", type(value).__name__, value)


def member(base: tuple | None, key: tuple | None) -> tuple | None:
    if base is None or key is None or key[0] != "literal":
        return None
    if len(repr(base)) > 350:
        return None
    return ("member", base, key[2])


def value_json(value: tuple | None) -> object:
    if value is None:
        return {"unknown": "control-flow-or-computed-value"}
    if value[0] == "literal":
        return value[2]
    if value[0] == "parameter":
        return {"unknown": "caller-argument", "parameter": value[1]}
    if value[0] == "global":
        return {"unknown": "global-value", "name": value[1]}
    if value[0] == "result":
        return {"unknown": "call-result", "pc": value[1], "result": value[2]}
    if value[0] == "member":
        return {
            "unknown": "member-value",
            "base": value_json(value[1]),
            "key": value[2],
        }
    return {"unknown": "closure-or-vararg"}


def rk(prototype: dict, state: tuple, operand: int) -> tuple | None:
    return (
        literal(prototype["constants"][operand - 256])
        if operand >= 256
        else state[operand]
    )


def successors(prototype: dict, pc: int) -> list[int]:
    opcode, _, _, c, bx = instruction(prototype["code"][pc])
    if opcode in {"RETURN", "TAILCALL"}:
        return []
    if opcode in {"JMP", "FORPREP"}:
        targets = [pc + 1 + bx - 131071]
    elif opcode == "FORLOOP":
        targets = [pc + 1, pc + 1 + bx - 131071]
    elif opcode in {"EQ", "LT", "LE", "TEST", "TESTSET", "TFORLOOP"}:
        targets = [pc + 1, pc + 2]
    elif opcode == "LOADBOOL" and c:
        targets = [pc + 2]
    elif opcode == "SETLIST" and not c:
        targets = [pc + 2]
    elif opcode == "CLOSURE":
        targets = [pc + 1 + prototype["children"][bx]["upvalues"]]
    else:
        targets = [pc + 1]
    if any(target < 0 or target >= len(prototype["code"]) for target in targets):
        raise ContractError("Lua control-flow target outside prototype")
    return targets


def transfer(prototype: dict, pc: int, incoming: tuple) -> tuple:
    state = list(incoming)
    opcode, a, b, c, bx = instruction(prototype["code"][pc])
    if opcode == "MOVE":
        state[a] = state[b]
    elif opcode == "LOADK":
        state[a] = literal(prototype["constants"][bx])
    elif opcode == "LOADBOOL":
        state[a] = literal(bool(b))
    elif opcode == "LOADNIL":
        state[a : b + 1] = [literal(None)] * (b - a + 1)
    elif opcode == "GETGLOBAL":
        state[a] = ("global", prototype["constants"][bx])
    elif opcode == "GETTABLE":
        state[a] = member(state[b], rk(prototype, incoming, c))
    elif opcode == "SELF":
        state[a + 1] = state[b]
        state[a] = member(state[b], rk(prototype, incoming, c))
    elif opcode == "CLOSURE":
        state[a] = ("prototype", prototype["children"][bx]["path"])
    elif opcode in {"CALL", "TAILCALL"}:
        count = c - 1 if c else len(state) - a
        for index in range(count):
            state[a + index] = ("result", pc, index)
    elif opcode == "VARARG":
        for index in range(b - 1 if b else len(state) - a):
            state[a + index] = None
    elif opcode == "FORLOOP":
        state[a] = state[a + 3] = None
    elif opcode == "FORPREP":
        state[a] = None
    elif opcode == "TFORLOOP":
        for index in range(a + 2, a + 3 + c):
            state[index] = None
    elif opcode == "TESTSET":
        # TESTSET may copy B to A. Clear A because both successors share this state.
        state[a] = None
    elif opcode in {
        "GETUPVAL",
        "NEWTABLE",
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "MOD",
        "POW",
        "UNM",
        "NOT",
        "LEN",
        "CONCAT",
    }:
        state[a] = None
    return tuple(state)


def states_for(prototype: dict) -> dict[int, tuple]:
    initial = tuple(
        ("parameter", i) if i < prototype["parameters"] else None
        for i in range(prototype["stack"])
    )
    states = {0: initial}
    pending = deque([0])
    while pending:
        pc = pending.popleft()
        after = transfer(prototype, pc, states[pc])
        for target in successors(prototype, pc):
            previous = states.get(target)
            joined = (
                after
                if previous is None
                else tuple(
                    x if x == y else None for x, y in zip(previous, after, strict=True)
                )
            )
            if previous != joined:
                states[target] = joined
                pending.append(target)
    return states


def location(prototype: dict, pc: int) -> dict:
    return {
        "prototype": prototype["path"],
        "pc": pc,
        "offset": prototype["offset"] + pc * 4,
    }


def method_name(value: tuple | None) -> str | None:
    if value and value[0] == "member" and isinstance(value[2], str):
        return value[2]
    if value and value[0] == "global":
        return value[1]
    return None


def has_member(value: tuple | None, name: str) -> bool:
    return bool(
        value
        and value[0] == "member"
        and (value[2] == name or has_member(value[1], name))
    )


def call_record(prototype: dict, pc: int, state: tuple) -> dict:
    _, a, b, c, _ = instruction(prototype["code"][pc])
    target = state[a]
    return {
        **location(prototype, pc),
        "target": method_name(target),
        "receiver": value_json(target[1]) if target and target[0] == "member" else None,
        "argumentCount": b - 1 if b else None,
        "arguments": [value_json(v) for v in state[a + 1 : a + b]] if b else [],
        "resultCount": c - 1 if c else None,
    }


def analyze_chunk(data: bytes, replay_rows: list[dict]) -> dict:
    reader = ChunkReader(data)
    root = reader.prototype()
    if reader.pos != len(data):
        raise ContractError("trailing Lua chunk bytes")
    declarations, calls, text, work, unknown, actors = [], [], [], [], [], []
    counts = Counter()
    comparisons, returns, prototype_census, class_definitions = [], [], [], []
    replay = {}
    for row in replay_rows:
        replay.setdefault(row["key"], []).append(row["rowId"])
    prototypes = {p["path"]: p for p in walk(root)}
    for prototype in prototypes.values():
        states = states_for(prototype)
        prototype_census.append(
            {
                "prototype": prototype["path"],
                "codeOffset": prototype["offset"],
                "instructionCount": len(prototype["code"]),
                "reachableInstructions": len(states),
                "unreachableCallPcs": [
                    pc
                    for pc, word in enumerate(prototype["code"])
                    if pc not in states and instruction(word)[0] in {"CALL", "TAILCALL"}
                ],
            }
        )
        for pc, word in enumerate(prototype["code"]):
            opcode, a, b, c, _ = instruction(word)
            state = states.get(pc)
            if state is None:
                continue
            if opcode in {"CALL", "TAILCALL"}:
                row = call_record(prototype, pc, state)
                name = row["target"]
                counts[name or "<unresolved>"] += 1
                if name == "_defineClass":
                    class_definitions.append(row)
                if name is None:
                    unknown.append(row)
                elif name in TEXT_METHODS:
                    text.append(
                        {
                            **location(prototype, pc),
                            "target": name,
                            "arguments": row["arguments"],
                        }
                    )
                elif (
                    name == "_loadTextDataPermanently"
                    or name == "callClientFunction"
                    or "CutScene" in name
                    or "Widget" in name
                    or "Quest" in name
                    or "Reward" in name
                    or "reward" in name
                ):
                    row["kind"] = (
                        "client-function"
                        if name == "callClientFunction"
                        else "scene"
                        if name
                        in {
                            "startNQCutScene",
                            "startHQCutScene",
                            "startSnpcNQCutScene",
                            "startSnpcHQCutScene",
                        }
                        else "presentation"
                    )
                    if row["kind"] == "scene":
                        key = (
                            row["arguments"][1]
                            if len(row["arguments"]) > 1
                            else {"unknown": "missing-scene-argument"}
                        )
                        row["sceneKey"] = key
                        row["replayRowIds"] = (
                            replay.get(key, []) if isinstance(key, str) else []
                        )
                        row["joinStatus"] = (
                            "exact-key-match"
                            if row["replayRowIds"]
                            else "unmatched-literal"
                            if isinstance(key, str)
                            else "dynamic-key"
                        )
                    calls.append(row)
                elif name.startswith("ask"):
                    calls.append({**row, "kind": "selector"})
                if name and "ActorClass" in name:
                    actors.append(row)
            elif opcode in {"EQ", "LT", "LE"}:
                left, right = rk(prototype, state, b), rk(prototype, state, c)
                if left and right:
                    result, value = (
                        (left, right) if left[0] == "result" else (right, left)
                    )
                    if result[0] == "result" and value[0] == "literal":
                        comparisons.append(
                            {
                                **location(prototype, pc),
                                "callPc": result[1],
                                "result": result[2],
                                "operator": opcode,
                                "literal": value[2],
                                "resultOperand": "B" if left[0] == "result" else "C",
                                "skipWhen": not bool(a),
                            }
                        )
            elif opcode == "SETTABLE":
                key, value = rk(prototype, state, b), rk(prototype, state, c)
                if key and key[0] == "literal" and value and value[0] == "prototype":
                    child = prototypes[value[1]]
                    declarations.append(
                        {
                            "name": key[2],
                            "prototype": child["path"],
                            "parameterCount": child["parameters"],
                            "variadic": bool(child["vararg"] & 2),
                            "callerArguments": "unknown",
                            "instructionCount": len(child["code"]),
                            "declaredAt": location(prototype, pc),
                        }
                    )
            if opcode in {"GETTABLE", "SELF", "SETTABLE"}:
                base = state[a] if opcode == "SETTABLE" else state[b]
                key = rk(prototype, state, b if opcode == "SETTABLE" else c)
                if has_member(base, "work"):
                    work.append(
                        {
                            **location(prototype, pc),
                            "access": "write" if opcode == "SETTABLE" else "read",
                            "base": value_json(base),
                            "key": value_json(key),
                        }
                    )
            if opcode == "RETURN":
                returns.append(
                    {
                        **location(prototype, pc),
                        "resultCount": b - 1 if b else None,
                        "values": [value_json(v) for v in state[a : a + b - 1]]
                        if b
                        else [],
                    }
                )
    selectors = []
    all_calls = {(r["prototype"], r["pc"]): r for r in calls + text + unknown}
    for row in comparisons:
        source = all_calls.get((row["prototype"], row["callPc"]))
        if source:
            selectors.append({**row, "callTarget": source["target"]})
    selector_sets = []
    for row in calls + text:
        if row["target"].startswith("ask") or row["target"] == "showQuestInfomation":
            observed = [
                c
                for c in selectors
                if (c["prototype"], c["callPc"]) == (row["prototype"], row["pc"])
            ]
            selector_sets.append(
                {
                    "prototype": row["prototype"],
                    "pc": row["pc"],
                    "target": row["target"],
                    "comparedLiterals": [
                        v
                        for _, v in sorted(
                            {
                                json.dumps(c["literal"]): c["literal"] for c in observed
                            }.items()
                        )
                    ],
                    "completeResultDomain": "unknown",
                }
            )
    return {
        "declarations": declarations,
        "calls": calls,
        "textCalls": text,
        "resultComparisons": selectors,
        "questWorkAccesses": work,
        "callCounts": dict(sorted(counts.items())),
        "unresolvedCalls": unknown,
        "actorClassCalls": actors,
        "prototypeCensus": prototype_census,
        "selectorResultSets": selector_sets,
        "returnSites": returns,
        "classDefinitions": class_definitions,
        "uncertainties": [
            "quest-id-not-joined",
            "caller-arguments-unknown",
            "actor-parameters-not-literal-actor-classes",
        ],
    }


def census(manifest: dict) -> list[dict]:
    result = []
    for source in manifest["scripts"]:
        path = source["relativePath"]
        if not path.startswith("lua/scripts/quest/scenario/"):
            continue
        parts = path.split("/")
        family = parts[4] if len(parts) == 6 else "<root>"
        group = next(
            (name for name, families in FAMILIES.items() if family in families), None
        )
        result.append(
            {
                "script": path,
                "family": family,
                "group": group,
                "classification": "included" if group else "outside-selected-families",
            }
        )
    return sorted(result, key=lambda row: row["script"])


def replay_input(csv_root: Path) -> list[dict]:
    path = csv_root / "cutReplay.csv"
    if digest(path.read_bytes()) != REPLAY_SHA256:
        raise ContractError("cutReplay.csv identity mismatch")
    result = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line, row in enumerate(csv.reader(handle), 1):
            if row and row[0].isdigit():
                result.append({"rowId": int(row[0]), "key": row[1], "line": line})
    return result


def build(retail_root: Path, replay_rows: list[dict]) -> dict:
    manifest = load(ROOT / PINS[0])
    coverage = load(ROOT / PINS[1])
    source_rows = {row["relativePath"]: row for row in manifest["scripts"]}
    resources = {row.get("decodedScriptPath"): row for row in coverage["resources"]}
    inventory = census(manifest)
    presentation = load(ROOT / "manifests/quest_selector_consumers.json")[
        "messageConsumers"
    ]
    scripts = []
    for item in inventory:
        if item["classification"] != "included":
            continue
        source = source_rows[item["script"]]
        resource = resources[item["script"]]
        original = (retail_root / resource["resourcePath"]).read_bytes()
        if (
            len(original) != resource["bytes"]
            or digest(original) != resource["sha256"].lower()
        ):
            raise ContractError("quest LPB identity mismatch")
        decoded = decode_lpb(original)
        if (
            decoded is None
            or digest(decoded) != resource["wrapper"]["decodedPayloadSha256"].lower()
            or len(decoded) != resource["wrapper"]["decodedPayloadBytes"]
        ):
            raise ContractError("quest decoded payload identity mismatch")
        analysis = analyze_chunk(decoded, replay_rows)
        references = [row for row in presentation if row["script"] == item["script"]]
        for reference in references:
            if not any(
                call["target"] == "say"
                and len(call["arguments"]) > 3
                and call["arguments"][2:4]
                == [reference["messageId"], reference["questId"]]
                for call in analysis["textCalls"]
            ):
                raise ContractError(
                    "retained selector reference does not match bytecode"
                )
        scripts.append(
            {
                **item,
                "source": source,
                "resource": resource,
                "decodeStatus": "matched-retained-corpus",
                "questId": None,
                "questPresentationReferences": references,
                **analysis,
            }
        )
    report = {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": "2012.09.19.0001",
        "evidenceClass": "retail-lua-bytecode-static-analysis",
        "inputs": [
            {"path": path, "sha256": digest((ROOT / path).read_bytes())}
            for path in PINS
        ],
        "replaySource": {
            "source": "xivl-client-data:csv/cutReplay.csv",
            "sha256": REPLAY_SHA256,
            "keyColumn": 0,
            "comparison": "case-sensitive-exact",
        },
        "replayRows": replay_rows,
        "census": inventory,
        "scripts": scripts,
    }
    report["summary"] = summarize(report)
    report["contentSha256"] = json_digest(report)
    return report


def summarize(report: dict) -> dict:
    rows = report["scripts"]
    families = []
    for group, names in FAMILIES.items():
        for name in names:
            selected = [r for r in rows if r["family"] == name]
            families.append(
                {
                    "family": name,
                    "group": group,
                    "scripts": len(selected),
                    "decoded": sum(
                        r["decodeStatus"] == "matched-retained-corpus" for r in selected
                    ),
                    "withHandlers": sum(
                        any(d["name"] != "initText" for d in r["declarations"])
                        for r in selected
                    ),
                    "unknownQuestIds": sum(r["questId"] is None for r in selected),
                }
            )
    return {
        "scenarioMembers": len(report["census"]),
        "includedScripts": len(rows),
        "excludedScripts": len(report["census"]) - len(rows),
        "families": families,
        "sceneCalls": sum(c["kind"] == "scene" for r in rows for c in r["calls"]),
        "clientFunctionCalls": sum(
            c["target"] == "callClientFunction" for r in rows for c in r["calls"]
        ),
        "unresolvedCalls": sum(len(r["unresolvedCalls"]) for r in rows),
        "questPresentationReferences": sum(
            len(r["questPresentationReferences"]) for r in rows
        ),
        "unknownQuestIds": sum(r["questId"] is None for r in rows),
    }


def validate_retained(report: dict) -> list[str]:
    problems = []
    unsigned = {key: value for key, value in report.items() if key != "contentSha256"}
    if report.get("contentSha256") != json_digest(unsigned):
        problems.append("contract content digest mismatch")
    expected_inputs = [
        {"path": path, "sha256": digest((ROOT / path).read_bytes())} for path in PINS
    ]
    if report.get("inputs") != expected_inputs:
        problems.append("contract input pins mismatch")
    manifest = load(ROOT / PINS[0])
    inventory = census(manifest)
    if report.get("census") != inventory:
        problems.append("scenario census mismatch")
    sources = {row["relativePath"]: row for row in manifest["scripts"]}
    resources = {
        row.get("decodedScriptPath"): row for row in load(ROOT / PINS[1])["resources"]
    }
    presentation = load(ROOT / "manifests/quest_selector_consumers.json")[
        "messageConsumers"
    ]
    expected = [r["script"] for r in inventory if r["classification"] == "included"]
    if [r["script"] for r in report["scripts"]] != expected:
        problems.append("included script set mismatch")
    replay = {}
    for row in report["replayRows"]:
        replay.setdefault(row["key"], []).append(row["rowId"])
    for row in report["scripts"]:
        path = row["script"]
        if row["source"] != sources.get(path) or row["resource"] != resources.get(path):
            problems.append(f"script identity mismatch: {path}")
        expected_item = next(
            (item for item in inventory if item["script"] == path), None
        )
        if expected_item is None or any(
            row[key] != expected_item[key] for key in expected_item
        ):
            problems.append(f"script census classification mismatch: {path}")
        prototypes = {p["prototype"]: p for p in row["prototypeCensus"]}
        if len(prototypes) != len(row["prototypeCensus"]):
            problems.append(f"duplicate bytecode prototype: {path}")
        for prototype in prototypes.values():
            count = prototype["instructionCount"]
            reachable = prototype["reachableInstructions"]
            unreachable_calls = prototype["unreachableCallPcs"]
            if (
                not 1 <= reachable <= count
                or len(set(unreachable_calls)) != len(unreachable_calls)
                or any(not 0 <= pc < count for pc in unreachable_calls)
                or len(unreachable_calls) > count - reachable
            ):
                problems.append(f"bytecode reachability bounds mismatch: {path}")
            if (
                prototype["codeOffset"] < 12
                or prototype["codeOffset"] + 4 * count
                > row["resource"]["wrapper"]["decodedPayloadBytes"]
            ):
                problems.append(f"bytecode instruction bounds mismatch: {path}")
        if sum(row["callCounts"].values()) > sum(
            prototype["reachableInstructions"] for prototype in prototypes.values()
        ):
            problems.append(f"bytecode call count bounds mismatch: {path}")
        for declaration in row["declarations"]:
            prototype = prototypes.get(declaration["prototype"])
            if (
                prototype is None
                or declaration["instructionCount"] != prototype["instructionCount"]
            ):
                problems.append(f"declaration instruction count mismatch: {path}")
        locations = (
            row["calls"]
            + row["textCalls"]
            + row["unresolvedCalls"]
            + row["returnSites"]
            + row["resultComparisons"]
            + row["questWorkAccesses"]
            + row["classDefinitions"]
        )
        locations += [d["declaredAt"] for d in row["declarations"]]
        for call in locations:
            prototype = prototypes.get(call["prototype"])
            if (
                prototype is None
                or not 0 <= call["pc"] < prototype["instructionCount"]
                or call["offset"] != prototype["codeOffset"] + 4 * call["pc"]
            ):
                problems.append(f"bytecode locator mismatch: {path}")
            if call.get("kind") == "scene":
                key = call["sceneKey"]
                matched = replay.get(key, []) if isinstance(key, str) else []
                if call["replayRowIds"] != matched:
                    problems.append(f"replay join mismatch: {path}")
                expected_status = (
                    "exact-key-match"
                    if matched
                    else "unmatched-literal"
                    if isinstance(key, str)
                    else "dynamic-key"
                )
                if call["joinStatus"] != expected_status:
                    problems.append(f"replay join status mismatch: {path}")
                expected_key = (
                    call["arguments"][1]
                    if len(call["arguments"]) > 1
                    else {"unknown": "missing-scene-argument"}
                )
                if call["sceneKey"] != expected_key:
                    problems.append(f"scene key argument mismatch: {path}")
        for call in (
            row["calls"]
            + row["unresolvedCalls"]
            + row["classDefinitions"]
            + row["actorClassCalls"]
        ):
            if call["argumentCount"] is not None and call["argumentCount"] != len(
                call["arguments"]
            ):
                problems.append(f"call argument arity mismatch: {path}")
        for returned in row["returnSites"]:
            if (
                returned["resultCount"] is not None
                and returned["resultCount"] != len(returned["values"])
            ) or (returned["resultCount"] is None and returned["values"]):
                problems.append(f"return result arity mismatch: {path}")
        if row["questId"] is not None:
            problems.append(f"unsupported quest identity: {path}")
        if row["questPresentationReferences"] != [
            r for r in presentation if r["script"] == path
        ]:
            problems.append(f"quest presentation reference mismatch: {path}")
    if report["replaySource"] != {
        "source": "xivl-client-data:csv/cutReplay.csv",
        "sha256": REPLAY_SHA256,
        "keyColumn": 0,
        "comparison": "case-sensitive-exact",
    }:
        problems.append("replay source identity mismatch")
    if report.get("summary") != summarize(report):
        problems.append("contract summary mismatch")
    return problems


def verify_archive(path: Path) -> None:
    private_manifest = load(ROOT / "manifests/private_lua_corpus.json")
    expected = private_manifest["archive"]["sha256"]
    if digest(path.read_bytes()) != expected.lower():
        raise ContractError("Lua archive identity mismatch")
    manifest = load(ROOT / "manifests/scripts.json")
    with zipfile.ZipFile(path) as archive:
        for row in manifest["scripts"]:
            if row["relativePath"].startswith("lua/scripts/quest/scenario/"):
                data = archive.read(row["relativePath"][len("lua/scripts/") :])
                if len(data) != row["bytes"] or digest(data) != row["sha256"].lower():
                    raise ContractError("archived scenario identity mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--retail-root", type=Path, help="explicit client/script directory"
    )
    parser.add_argument(
        "--csv-root", type=Path, help="explicit directory containing cutReplay.csv"
    )
    parser.add_argument(
        "--lua-archive",
        type=Path,
        help="optionally authenticate the retained Lua archive",
    )
    args = parser.parse_args()
    try:
        if args.lua_archive:
            verify_archive(args.lua_archive)
        if args.check:
            report = load(OUTPUT)
            problems = validate_retained(report)
            if args.csv_root and replay_input(args.csv_root) != report["replayRows"]:
                problems.append("retained replay rows differ from authenticated CSV")
            if (
                args.retail_root
                and build(args.retail_root, report["replayRows"]) != report
            ):
                problems.append("retained contracts differ from retail bytecode")
            if problems:
                raise ContractError("; ".join(problems))
        else:
            if not args.retail_root or not args.csv_root:
                parser.error("generation requires --retail-root and --csv-root")
            report = build(args.retail_root, replay_input(args.csv_root))
            problems = validate_retained(report)
            if problems:
                raise ContractError("; ".join(problems))
            OUTPUT.write_text(
                json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="ascii"
            )
        jsonschema.Draft202012Validator(
            load(ROOT / "schemas/quest_contracts.schema.json")
        ).validate(report)
        print(
            f"Quest contracts passed: {report['summary']['includedScripts']} scripts, {report['summary']['sceneCalls']} scene calls"
        )
        return 0
    except (
        ContractError,
        OSError,
        ValueError,
        KeyError,
        struct.error,
        jsonschema.ValidationError,
    ) as exc:
        print(f"Quest contracts failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
