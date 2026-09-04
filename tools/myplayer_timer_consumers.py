#!/usr/bin/env python3
"""Build or check the bounded MyPlayer timer-consumer corpus report."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "lua" / "scripts"
OUTPUT_PATH = REPO_ROOT / "manifests" / "myplayer_timer_consumers.json"
CALLBACKS = (
    "_getOccupancyContentsTime",
    "_getNormalBehestTime",
    "_getCompanyBehestTime",
    "_getWarpRecastTime",
    "_getNMRushUpdateTime",
)


class AnalysisError(ValueError):
    """The local corpus no longer matches the bounded semantic patterns."""


CALLSITE_SPECS = {
    ("chara/player/playerbaseclass.lua", 2819): {
        "callback": "_getWarpRecastTime",
        "caller": "PlayerBaseClass.getWarpRecastTime",
        "luaArityIncludingSelf": 1,
        "argument": None,
        "use": "subtract server time and clamp the result to a minimum of zero",
    },
    ("widget/desktopwidget_connector.lua", 24952): {
        "callback": "_getNMRushUpdateTime",
        "caller": "DesktopWidget.isNMRushEnable",
        "luaArityIncludingSelf": 1,
        "argument": None,
        "use": "return whether the value is greater than zero",
    },
    ("widget/statuswidget.lua", 3400): {
        "callback": "_getNormalBehestTime",
        "caller": "StatusWidget.setContentsListItem",
        "luaArityIncludingSelf": 1,
        "argument": None,
        "use": "treat as an endpoint for the contents-list countdown",
    },
    ("widget/statuswidget.lua", 3408): {
        "callback": "_getCompanyBehestTime",
        "caller": "StatusWidget.setContentsListItem",
        "luaArityIncludingSelf": 1,
        "argument": None,
        "use": "treat as an endpoint for the contents-list countdown",
    },
    ("widget/statuswidget.lua", 3416): {
        "callback": "_getNMRushUpdateTime",
        "caller": "StatusWidget.setContentsListItem",
        "luaArityIncludingSelf": 1,
        "argument": None,
        "use": "treat as an endpoint for the contents-list countdown",
    },
    ("widget/statuswidget.lua", 3424): {
        "callback": "_getOccupancyContentsTime",
        "caller": "StatusWidget.setContentsListItem",
        "luaArityIncludingSelf": 2,
        "argument": "parameter",
        "use": "treat as an endpoint for the contents-list countdown",
        "deterministicArguments": list(range(1, 17)),
    },
}

for line, argument in zip(
    (579, 599, 619, 639, 659),
    (1, 2, 6, 7, 13),
):
    CALLSITE_SPECS[("widget/pcmatchingeditwidget.lua", line)] = {
        "callback": "_getOccupancyContentsTime",
        "caller": "PcMatchingEditWidget.makeGuildleveList",
        "luaArityIncludingSelf": 2,
        "argument": argument,
        "use": "include the matching selection row only when the value is greater than zero",
    }

for line, argument in zip(
    (701, 726, 746, 761, 781, 801, 819, 842),
    (4, 3, 14, 5, 12, 11, 15, 16),
):
    CALLSITE_SPECS[("widget/pcmatchingeditwidget.lua", line)] = {
        "callback": "_getOccupancyContentsTime",
        "caller": "PcMatchingEditWidget.makeRaidList",
        "luaArityIncludingSelf": 2,
        "argument": argument,
        "use": "include the matching selection row only when the value is greater than zero",
    }

for line, argument in zip((918, 932, 946), (8, 9, 10)):
    CALLSITE_SPECS[("widget/pcmatchingeditwidget.lua", line)] = {
        "callback": "_getOccupancyContentsTime",
        "caller": "PcMatchingEditWidget.makeBanzokuList",
        "luaArityIncludingSelf": 2,
        "argument": argument,
        "use": "include the matching selection row only when the value is greater than zero",
    }


OCCUPANCY_VOCABULARY = (
    "the Thousand Maws of Toto-Rak",
    "Dzemael Darkhold",
    "the Bowl of Embers (Hard)",
    "the Bowl of Embers",
    "Thornmarch",
    "Aurum Vale",
    "Cutter's Cry",
    "the Battle for Aleport",
    "the Battle for Hyrstmill",
    "the Battle for the Golden Bazaar",
    "the Howling Eye (Hard)",
    "the Howling Eye",
    "Castrum Novum Transmission Tower",
    "the Bowl of Embers (Extreme)",
    "Rivenroad",
    "Rivenroad (Hard)",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _exact_reference_lines(scripts_root: Path) -> dict[str, list[tuple[str, int]]]:
    found: dict[str, list[tuple[str, int]]] = defaultdict(list)
    patterns = {
        name: re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
        for name in CALLBACKS
    }
    for path in sorted(scripts_root.rglob("*.lua")):
        relative = path.relative_to(scripts_root).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for name, pattern in patterns.items():
                if pattern.search(line):
                    found[name].append((relative, number))
    return found


def _verify_callsite_shape(path: Path, line_number: int, spec: dict) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    index = line_number - 1
    if index >= len(lines) or spec["callback"] not in lines[index]:
        raise AnalysisError(f"{path}:{line_number}: callback line drifted")
    callback_match = re.fullmatch(
        rf"\s*(L\d+_2) = [AL]\d+_2\.{re.escape(spec['callback'])}",
        lines[index],
    )
    if callback_match is None:
        raise AnalysisError(f"{path}:{line_number}: callback expression drifted")
    function_var = callback_match.group(1)
    if spec["luaArityIncludingSelf"] == 1:
        if index + 1 >= len(lines) or re.fullmatch(
            rf"\s*{function_var} = {function_var}\(L\d+_2\)",
            lines[index + 1],
        ) is None:
            raise AnalysisError(f"{path}:{line_number}: scalar call arity drifted")
    else:
        if index + 2 >= len(lines):
            raise AnalysisError(f"{path}:{line_number}: occupancy call is truncated")
        argument = spec["argument"]
        expected_value = str(argument) if isinstance(argument, int) else r"A\d+_2"
        argument_match = re.fullmatch(
            rf"\s*(L\d+_2) = {expected_value}",
            lines[index + 1],
        )
        if argument_match is None:
            raise AnalysisError(f"{path}:{line_number}: expected argument {argument}")
        argument_var = argument_match.group(1)
        if re.fullmatch(
            rf"\s*{function_var} = {function_var}\(L\d+_2, {argument_var}\)",
            lines[index + 2],
        ) is None:
            raise AnalysisError(f"{path}:{line_number}: occupancy call arity drifted")


def _verify_sidecars(
    sidecars_root: Path, found: dict[str, list[tuple[str, int]]]
) -> None:
    indexed: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for path in sorted(sidecars_root.rglob("*.calls.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        relative = (
            path.relative_to(sidecars_root).as_posix()[: -len(".calls.json")]
            + ".lua"
        )
        for callback in CALLBACKS:
            for line in data.get("apis", {}).get(callback, []):
                indexed[callback].append((relative, line))
    for callback in CALLBACKS:
        if sorted(indexed[callback]) != sorted(found[callback]):
            raise AnalysisError(f"{callback}: sidecar callsites disagree with Lua")

    napi = json.loads((REPO_ROOT / "lua" / "napi_index.json").read_text(encoding="utf-8"))
    for callback in CALLBACKS:
        rows = []
        for callsite in napi["apis"][callback]["callsites"]:
            rows.append((callsite["script"] + ".lua", callsite["line"]))
        if sorted(rows) != sorted(found[callback]):
            raise AnalysisError(f"{callback}: N-API index callsites disagree with Lua")


def _verify_declarations_and_registry(scripts_root: Path) -> list[dict]:
    declarations = []
    for callback in CALLBACKS:
        needle = callback + "_cpp"
        matches = []
        for path in sorted(scripts_root.rglob("*.lua")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if needle in line:
                    matches.append((path, number))
        if len(matches) != 1:
            raise AnalysisError(f"{callback}: expected one receiver declaration, got {len(matches)}")
        path, number = matches[0]
        declarations.append({
            "callback": callback,
            "receiverClass": "PlayerBaseClass",
            "script": "lua/scripts/" + path.relative_to(scripts_root).as_posix(),
            "line": number,
            "cppName": needle,
        })

    registry = json.loads((REPO_ROOT / "lua" / "registry.json").read_text(encoding="utf-8"))
    methods = registry["scripts"]["chara/player/playerbaseclass_u"]["methods"]
    for callback in CALLBACKS:
        inline = callback + "_inl"
        if methods.count(inline) != 1:
            raise AnalysisError(f"{callback}: registry inline metadata disagrees")
    return declarations


def _verify_status_propagation(scripts_root: Path) -> None:
    source = (scripts_root / "widget" / "statuswidget.lua").read_text(encoding="utf-8")
    compact = " ".join(source.split())
    constants = (-1, -2, -3, 1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 12, 11, 13, 14, 15, 16, -4)
    cursor = 0
    for value in constants:
        pattern = f"A0_2.setContentsListItem L5_2 = L2_2 L6_2 = {value}"
        position = compact.find(pattern, cursor)
        if position < 0:
            raise AnalysisError(f"StatusWidget.updateContents: missing ordered argument {value}")
        cursor = position + len(pattern)
    required = (
        "if 0 < L7_2 then",
        "L12_2 = L12_2._getServerTime",
        "L13_2 = L7_2 - L12_2",
        "L20_2 = L13_2 / 86400",
        "L20_2 = L13_2 / 3600",
        "L20_2 = L13_2 / 60",
        'L16_2 = "TextBlock_ContentsStatus"',
    )
    for pattern in required:
        if pattern not in compact:
            raise AnalysisError(f"StatusWidget.setContentsListItem: missing {pattern}")

    hamlet_start = compact.find("L11_2 = nil L12_2 = A2_2")
    hamlet_end = compact.find("if 0 < L7_2 then", hamlet_start)
    if hamlet_start < 0 or hamlet_end < 0:
        raise AnalysisError("StatusWidget.setContentsListItem: Hamlet block is missing")
    hamlet_block = compact[hamlet_start:hamlet_end]
    hamlet_patterns = (
        "if L12_2 == 8 then L11_2 = 2",
        "if L12_2 == 9 then L11_2 = 1",
        "if L12_2 == 10 then L11_2 = 3",
        "A0_2.isHamletDefenceBegin",
        "if L12_2 == false and 0 < L7_2 then",
        "A0_2.getHamletDefenceBeginTime",
        "L7_2 = L12_2 L8_2 = 10058",
    )
    cursor = 0
    for pattern in hamlet_patterns:
        position = hamlet_block.find(pattern, cursor)
        if position < 0:
            raise AnalysisError(f"StatusWidget.setContentsListItem: missing {pattern}")
        cursor = position + len(pattern)


def _verify_scalar_chains(scripts_root: Path) -> None:
    sources = {
        relative: " ".join((scripts_root / relative).read_text(encoding="utf-8").split())
        for relative in (
            "chara/player/playerbaseclass.lua",
            "command/system/teleportcommand.lua",
            "widget/desktopwidget_connector.lua",
            "widget/mainmenuwidget.lua",
            "widget/statuswidget.lua",
        )
    }
    required = {
        "chara/player/playerbaseclass.lua": (
            "A0_2._getWarpRecastTime",
            "L4_2 = L1_2 - L4_2 return L2_2(L3_2, L4_2)",
        ),
        "command/system/teleportcommand.lua": (
            "A1_2.getWarpRecastTime",
            "if 0 < L11_2 then L11_2 = false return L11_2",
        ),
        "widget/desktopwidget_connector.lua": (
            "L1_1 = \"isNMRushEnable\"",
            "L1_2._getNMRushUpdateTime",
            "if 0 < L2_2 then L2_2 = true return L2_2",
        ),
        "widget/mainmenuwidget.lua": (
            'L4_2 = 15 L5_2 = "DataTemplate_ListBoxItem_Return"',
            'L4_2 = 15 L5_2 = "MainName" L6_2 = 2112',
            "L10_2.getWarpRecastTime",
            "L1_2.getWarpRecastTime",
            'L7_2 = "FValue0" L8_2 = L2_2',
            'L7_2 = "TimerVisibility" L8_2 = "Visible"',
            'L7_2 = "TimerVisibility" L8_2 = "Collapsed"',
            "L0_1.setDezionTimer = L1_1",
        ),
        "widget/statuswidget.lua": (
            "A2_2 == -2",
            "L6_2 = 10049",
            "L10_2._getNormalBehestTime",
            "A2_2 == -3",
            "L6_2 = 10050",
            "L10_2._getCompanyBehestTime",
            "A2_2 == -4",
            "L6_2 = 10059",
            "L10_2._getNMRushUpdateTime",
            "L8_2 = 10055 L9_2 = 10056",
            "L8_2 = 10047 L9_2 = 10048",
        ),
    }
    for relative, patterns in required.items():
        for pattern in patterns:
            if pattern not in sources[relative]:
                raise AnalysisError(f"{relative}: scalar consumer chain missing {pattern}")


def analyze(
    scripts_root: Path = SCRIPTS_ROOT,
    sidecars_root: Path | None = None,
) -> dict:
    """Return the stable non-reconstructive report for one complete corpus."""
    if not scripts_root.is_dir():
        raise AnalysisError(f"Lua corpus not found: {scripts_root}")
    script_count = sum(1 for _ in scripts_root.rglob("*.lua"))
    if script_count != 2671:
        raise AnalysisError(f"expected 2671 scripts, got {script_count}")
    found = _exact_reference_lines(scripts_root)
    actual = sorted((path, line) for rows in found.values() for path, line in rows)
    expected = sorted(CALLSITE_SPECS)
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise AnalysisError(f"direct callsite set drifted ({len(missing)} missing, {len(extra)} extra)")
    _verify_sidecars(sidecars_root or scripts_root, found)
    declarations = _verify_declarations_and_registry(scripts_root)
    _verify_status_propagation(scripts_root)
    _verify_scalar_chains(scripts_root)

    callsites = []
    for (relative, line), base_spec in sorted(CALLSITE_SPECS.items()):
        spec = dict(base_spec)
        _verify_callsite_shape(scripts_root / relative, line, spec)
        row = {"script": f"lua/scripts/{relative}", "line": line, **spec}
        if spec["callback"] == "_getOccupancyContentsTime" and isinstance(spec["argument"], int):
            row["nativeVectorIndex"] = spec["argument"] - 1
        callsites.append(row)

    contexts: dict[int, list[str]] = defaultdict(list)
    for row in callsites:
        if row["callback"] != "_getOccupancyContentsTime":
            continue
        if isinstance(row["argument"], int):
            contexts[row["argument"]].append(row["caller"])
        else:
            for argument in row["deterministicArguments"]:
                contexts[argument].append(row["caller"])
    argument_map = []
    for argument, vocabulary in enumerate(OCCUPANCY_VOCABULARY, 1):
        row = {
            "luaArgument": argument,
            "nativeVectorIndex": argument - 1,
            "callerContexts": sorted(contexts[argument]),
            "statusTitleEnglish": vocabulary,
        }
        hamlet_slot = {8: 2, 9: 1, 10: 3}.get(argument)
        if hamlet_slot is not None:
            row["statusTransformation"] = (
                f"Hamlet slot {hamlet_slot}; before that defense window begins, "
                "replace a positive endpoint with getHamletDefenceBeginTime and "
                "use Hamlet defense available in"
            )
        argument_map.append(row)

    by_callback = defaultdict(int)
    for row in callsites:
        by_callback[row["callback"]] += 1
    return {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": "2012.09.19.0001",
        "corpus": {
            "manifest": "manifests/scripts.json",
            "manifestSha256": sha256(REPO_ROOT / "manifests" / "scripts.json"),
            "registry": "lua/registry.json",
            "registrySha256": sha256(REPO_ROOT / "lua" / "registry.json"),
            "napiIndex": "lua/napi_index.json",
            "napiIndexSha256": sha256(REPO_ROOT / "lua" / "napi_index.json"),
            "scriptCount": 2671,
        },
        "nativeMapping": {
            "source": "xivl-decomp:config/s2c_0193_native_state.json",
            "occupancySubopcodes": "0x00..0x0f",
            "occupancyInputTransform": "subtract one before indexing",
            "normalBehestSubopcode": "0x10",
            "companyBehestSubopcode": "0x11",
            "warpRecastSubopcode": "0x12",
            "nmRushSubopcode": "0x16",
        },
        "summary": {
            "directCallsiteCount": len(callsites),
            "directCallsitesByCallback": dict(sorted(by_callback.items())),
            "receiverDeclarationCount": 5,
            "occupancyProvenArgumentCount": len(argument_map),
        },
        "directCallsites": callsites,
        "receiverDeclarations": declarations,
        "occupancyArgumentMap": argument_map,
        "vocabularySources": [
            "xivl-client-data:csv/xtx_raidDungeon.csv",
            "xivl-client-data:csv/xtx__text_ui.csv",
        ],
        "scalarConsumerChains": [
            {
                "callback": "_getNormalBehestTime",
                "consumers": ["StatusWidget.setContentsListItem"],
                "presentation": "Behests; Available in; Available",
            },
            {
                "callback": "_getCompanyBehestTime",
                "consumers": ["StatusWidget.setContentsListItem"],
                "presentation": "Company Behests; Available in; Available",
            },
            {
                "callback": "_getWarpRecastTime",
                "consumers": [
                    "PlayerBaseClass.getWarpRecastTime",
                    "MainMenuWidget.getButtonMask",
                    "MainMenuWidget.setDezionTimer",
                    "TeleportCommand.canFire",
                ],
                "presentation": "Return; MainMenu item 15 timer properties",
            },
            {
                "callback": "_getNMRushUpdateTime",
                "consumers": [
                    "DesktopWidget.isNMRushEnable",
                    "StatusWidget.setContentsListItem",
                ],
                "presentation": "Skirmish; Available in; Available",
            },
        ],
        "exactReferenceAccounting": {
            "directCalls": 22,
            "receiverDeclarations": 5,
            "registryInlineMetadata": 5,
            "otherExactStringOrResourceReferences": 0,
        },
        "unresolved": [
            "The occupancy call is syntactically dynamic in StatusWidget.setContentsListItem, but all 20 corpus callers pass fixed values: -1 through -4 select other callbacks and 1 through 16 select occupancy entries.",
            "No corpus call passes occupancy argument zero, a negative value, or a value above 16; behavior for such an invocation is not established.",
        ],
        "rejectedInterpretations": [
            "The report does not infer timer units from the native storage.",
            "The report does not treat UI titles as packet or server field names.",
            "The report does not establish authoritative eligibility, setup or teardown behavior, or server policy.",
        ],
    }


def render_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        report = analyze()
    except (OSError, UnicodeError, json.JSONDecodeError, AnalysisError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    rendered = render_json(report)
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != rendered:
            print(f"error: {OUTPUT_PATH.relative_to(REPO_ROOT)} is stale", file=sys.stderr)
            return 1
        print("PASS: 22 MyPlayer timer callsites match the semantic report")
        return 0
    OUTPUT_PATH.write_bytes(rendered)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
