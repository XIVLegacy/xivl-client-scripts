#!/usr/bin/env python3
"""Check the bounded generalParameter[18] retail Lua consumer census."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "lua" / "scripts"


class AnalysisError(ValueError):
    """The local corpus no longer matches the bounded semantic patterns."""


EXPECTED_GENERAL_PARAMETER_REFS = {
    "chara/charabaseclass_battle.lua": tuple(
        [1456] + list(range(1547, 1737, 7))
    ),
    "chara/charabaseclass_ffxivbattle.lua": (
        32, 451, 463, 475, 487, 499, 511, 523, 535,
        547, 559, 571, 583, 595, 607, 619, 631,
    ),
}

EXPECTED_NORMAL_DEFENCE_REFS = {
    "chara/charabaseclass_ffxivbattle.lua": (480,),
    "widget/equipwidget.lua": (2056,),
    "widget/statuswidget.lua": (1220,),
}

EXPECTED_PHYSICAL_PARAMETER_REFS = {
    "chara/charabaseclass_ffxivbattle.lua": (38,),
    "widget/ask/bonuspointassignwidget.lua": tuple(
        list(range(503, 534, 6)) + list(range(616, 647, 6))
    ),
    "widget/equipwidget.lua": tuple(range(1935, 1980, 4)),
    "widget/statuswidget.lua": tuple(range(1099, 1144, 4)),
}

EXPECTED_PHYSICAL_ARGUMENTS = {
    "widget/ask/bonuspointassignwidget.lua": tuple(range(1, 7)) * 2,
    "widget/equipwidget.lua": tuple(range(1, 13)),
    "widget/statuswidget.lua": tuple(range(1, 13)),
}


def _compact(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _exact_refs(token: str, scripts_root: Path) -> dict[str, tuple[int, ...]]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])")
    found: dict[str, tuple[int, ...]] = {}
    for path in sorted(scripts_root.rglob("*.lua")):
        lines = tuple(
            number
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            )
            if pattern.search(line)
        )
        if lines:
            found[path.relative_to(scripts_root).as_posix()] = lines
    return found


def _require_patterns(relative: str, compact: str, patterns: tuple[str, ...]) -> None:
    cursor = 0
    for pattern in patterns:
        position = compact.find(pattern, cursor)
        if position < 0:
            raise AnalysisError(f"{relative}: consumer chain missing {pattern}")
        cursor = position + len(pattern)


def _verify_ffxivbattle(path: Path) -> None:
    _require_patterns(
        "chara/charabaseclass_ffxivbattle.lua",
        _compact(path),
        (
            "L1_2 = A0_2.charaWork L1_2 = L1_2.battleTemp "
            "L1_2 = L1_2.generalParameter L1_2 = L1_2[19] return L1_2 end "
            "L0_1.getNormalDefence = L1_1",
        ),
    )


def _physical_arguments(scripts_root: Path) -> dict[str, tuple[int, ...]]:
    arguments: dict[str, tuple[int, ...]] = {}
    for relative, refs in EXPECTED_PHYSICAL_PARAMETER_REFS.items():
        if relative == "chara/charabaseclass_ffxivbattle.lua":
            continue
        lines = (scripts_root / relative).read_text(encoding="utf-8").splitlines()
        values = []
        for line_number in refs:
            for line in lines[line_number:line_number + 3]:
                match = re.search(r"= (\d+)$", line)
                if match is not None:
                    values.append(int(match.group(1)))
                    break
            else:
                raise AnalysisError(f"{relative}:{line_number}: fixed argument is missing")
        arguments[relative] = tuple(values)
    return arguments


def _verify_physical_arguments(scripts_root: Path) -> None:
    if _physical_arguments(scripts_root) != EXPECTED_PHYSICAL_ARGUMENTS:
        raise AnalysisError("getPhysicalParameter fixed argument domain drifted")


def _verify_connector(path: Path) -> None:
    _require_patterns(
        "widget/desktopwidget_connector.lua",
        _compact(path),
        (
            'L7_2 = A3_2 if L7_2 == "command"',
            'elseif L7_2 == "battleParameter" then else end '
            'if L7_2 == "gameParameter"',
            "L0_1.processCharacterParameterUpdated = L1_1",
        ),
    )


def analyze(scripts_root: Path = SCRIPTS_ROOT) -> dict[str, object]:
    """Return the stable, non-reconstructive census summary."""
    if not scripts_root.is_dir():
        raise AnalysisError(f"Lua corpus not found: {scripts_root}")
    script_count = sum(1 for _ in scripts_root.rglob("*.lua"))
    if script_count != 2671:
        raise AnalysisError(f"expected 2671 scripts, got {script_count}")

    general_refs = _exact_refs("generalParameter", scripts_root)
    if general_refs != EXPECTED_GENERAL_PARAMETER_REFS:
        raise AnalysisError("generalParameter reference census drifted")
    defence_refs = _exact_refs("getNormalDefence", scripts_root)
    if defence_refs != EXPECTED_NORMAL_DEFENCE_REFS:
        raise AnalysisError("getNormalDefence reference census drifted")
    physical_refs = _exact_refs("getPhysicalParameter", scripts_root)
    if physical_refs != EXPECTED_PHYSICAL_PARAMETER_REFS:
        raise AnalysisError("getPhysicalParameter reference census drifted")
    _verify_physical_arguments(scripts_root)

    battle = _compact(scripts_root / "chara" / "charabaseclass_battle.lua")
    _require_patterns(
        "chara/charabaseclass_battle.lua",
        battle,
        (
            'L8_2 = "generalParameter" L9_2 = "array" L10_2 = 35 L11_2 = "integer16"',
            'L28_2 = "battleTemp" L29_2 = "generalParameter" L30_2 = 18',
            "L9_2[18] = L27_2",
        ),
    )

    _verify_ffxivbattle(scripts_root / "chara" / "charabaseclass_ffxivbattle.lua")

    widget_specs = {
        "widget/statuswidget.lua": (
            'L5_2 = "Label_PhysicsDefense" L6_2 = "TextBlock_Title" '
            "L3_2 = L3_2(L4_2, L5_2, L6_2) L4_2 = 214 L5_2 = 15019",
            "L2_2 = A0_2.setDefence L5_2 = L1_2 "
            "L4_2 = L1_2.getNormalDefence L4_2, L5_2, L6_2 = L4_2(L5_2) "
            "L2_2(L3_2, L4_2, L5_2, L6_2)",
            'L6_2 = "Label_PhysicsDefense" L7_2 = "TextBlock_BaseParameter" '
            "L4_2 = L4_2(L5_2, L6_2, L7_2) L5_2 = tostring L6_2 = A1_2",
        ),
        "widget/equipwidget.lua": (
            "L2_2 = A0_2.setDefence L5_2 = L1_2 "
            "L4_2 = L1_2.getNormalDefence L4_2, L5_2, L6_2 = L4_2(L5_2) "
            "L2_2(L3_2, L4_2, L5_2, L6_2)",
            'L5_2 = "Label_PhysicsDefense" L6_2 = "TextBlock_Title" '
            "L3_2 = L3_2(L4_2, L5_2, L6_2) L4_2 = 3188 L5_2 = 15019",
            'L6_2 = "Label_PhysicsDefense" L7_2 = "TextBlock_BaseParameter" '
            "L4_2 = L4_2(L5_2, L6_2, L7_2) L5_2 = tostring L6_2 = A1_2",
        ),
    }
    for relative, patterns in widget_specs.items():
        _require_patterns(relative, _compact(scripts_root / relative), patterns)

    chara = _compact(scripts_root / "chara" / "charabaseclass.lua")
    _require_patterns(
        "chara/charabaseclass.lua",
        chara,
        (
            "L5_2 = desktopWidget L6_2 = L5_2 "
            "L5_2 = L5_2.processCharacterParameterUpdated",
            "L0_1._onUpdateWork = L1_1",
        ),
    )
    _verify_connector(scripts_root / "widget" / "desktopwidget_connector.lua")

    return {
        "scriptCount": script_count,
        "nativeIndex": 18,
        "luaIndex": 19,
        "accessor": "CharaBaseClass.getNormalDefence",
        "directConsumers": (
            "StatusWidget.updateBattleParameter",
            "EquipWidget.updateBattleParameter",
        ),
        "displayControl": "Label_PhysicsDefense",
        "parameterNameRow": 15019,
        "helpRow": 70019,
        "propertyCallbackBoundary": "empty DesktopWidget battleParameter branch",
        "generalParameterReferenceCount": sum(map(len, general_refs.values())),
        "normalDefenceReferenceCount": sum(map(len, defence_refs.values())),
        "genericPhysicalParameterCallCount": sum(map(len, physical_refs.values())) - 1,
        "genericPhysicalParameterArgumentRange": (1, 12),
    }


def main() -> int:
    try:
        report = analyze()
    except (OSError, UnicodeError, AnalysisError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS: generalParameter[18] maps to Lua slot 19 and "
        f"{report['accessor']} across {report['scriptCount']} scripts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
