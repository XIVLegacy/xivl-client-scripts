#!/usr/bin/env python3
"""Build and check the MonsterAttackWeaponSkill getter-rule profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from _corpus import CorpusRootError, resolve_scripts_root, validate_scripts_root


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "lua" / "scripts"
OUTPUT_PATH = REPO_ROOT / "manifests" / "monster_attack_weapon_skill_profiles.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "monster_attack_weapon_skill_profiles.schema.json"
SCRIPTS_MANIFEST_PATH = REPO_ROOT / "manifests" / "scripts.json"

SOURCE_RELATIVE = Path(
    "command/game/weaponskill/monsterattackweaponskill.lua"
)
SOURCE_PATH = "lua/scripts/command/game/weaponskill/monsterattackweaponskill.lua"
SOURCE_SHA256 = "d5b8e884aad2ca2cfe5cfa96cf5e029d975a32bb0bc1742873ded2f3a78b668e"
SOURCE_BYTES = 59652
SOURCE_LINE_COUNT = 3469
GETTER_RULES_SHA256 = "446bb12571d90c6a5095feb49ed9f5056c2ccee84f902204e70ec985833e25f2"
EXTRACTION = "2012.09.19.0001"
GAME_VERSION = "1.23b"
CLASS_PATH = "/Command/Game/WeaponSkill/MonsterAttackWeaponSkill"
PARENT_PATH = "/Command/Game/WeaponSkill/WeaponSkillBaseClass"
SUMMARY = {
    "getterCount": 6,
    "overrideGroupCount": 12,
    "overrideCommandCount": 57,
}
UNRESOLVED = [
    "getCommandInformation returns nil when its selector is not 8.",
    "getPartsDamageAdjust's pair consumer and combination rule are unresolved.",
]

GETTER_NAMES = (
    "getCommandInformation",
    "getFrequency",
    "getRangeWidth",
    "getRangeRotate",
    "getCommandRangeHeight",
    "getPartsDamageAdjust",
)


class AnalysisError(ValueError):
    """The selected source no longer matches the bounded getter model."""


def _source_path(scripts_root: Path) -> Path:
    return scripts_root / SOURCE_RELATIVE


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_sha256(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256(encoded)


def _source_manifest_row() -> dict[str, Any]:
    """Return the uniquely matching retained source-manifest row."""
    try:
        manifest = json.loads(SCRIPTS_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AnalysisError(f"cannot read {SCRIPTS_MANIFEST_PATH.name}: {exc}") from exc
    rows = manifest.get("scripts") if isinstance(manifest, dict) else None
    if not isinstance(rows, list):
        raise AnalysisError(f"{SCRIPTS_MANIFEST_PATH.name}: scripts list is missing")
    matches = [
        row
        for row in rows
        if isinstance(row, dict) and row.get("relativePath") == SOURCE_PATH
    ]
    if len(matches) != 1:
        raise AnalysisError(
            f"{SCRIPTS_MANIFEST_PATH.name}: expected one row for {SOURCE_PATH}, "
            f"found {len(matches)}"
        )
    row = matches[0]
    expected = {
        "relativePath": SOURCE_PATH,
        "bytes": SOURCE_BYTES,
        "sha256": SOURCE_SHA256.upper(),
        "lineCount": SOURCE_LINE_COUNT,
    }
    if row != expected:
        raise AnalysisError(
            f"{SCRIPTS_MANIFEST_PATH.name}: retained source row disagrees"
        )
    return row


def _function_block(lines: list[str], getter: str) -> tuple[int, int, list[str]]:
    """Return zero-based function start/end and its source lines."""
    marker = f"L0_1.{getter} = L1_1"
    markers = [index for index, line in enumerate(lines) if line == marker]
    if len(markers) != 1:
        raise AnalysisError(f"{getter}: expected one method assignment")
    end = markers[0]
    starts = [
        index
        for index in range(end - 1, -1, -1)
        if lines[index].startswith("function L1_1")
    ]
    if not starts:
        raise AnalysisError(f"{getter}: function definition is missing")
    start = starts[0]
    return start, end, lines[start:end]


def _assignment_before(
    block: list[str], variable: str, before_index: int | None = None
) -> int | list[int] | None:
    limit = len(block) if before_index is None else before_index
    pattern = re.compile(rf"^\s*{re.escape(variable)} = (-?\d+)\s*$")
    values: list[int] = []
    for line in block[:limit]:
        match = pattern.match(line)
        if match:
            values.append(int(match.group(1)))
    return values


def _condition_branches(
    block: list[str], condition_variable: str, line_offset: int = 0
) -> list[tuple[list[int], list[str], int]]:
    """Find top-level generated Lua condition branches for one variable."""
    condition = re.compile(
        rf"^\s*(?:if|elseif) {re.escape(condition_variable)} == (?P<expr>.+?) then\s*$"
    )
    matches = [
        (index, match)
        for index, line in enumerate(block)
        if (match := condition.match(line)) is not None
    ]
    branches: list[tuple[list[int], list[str], int]] = []
    for position, (start, match) in enumerate(matches):
        end = matches[position + 1][0] if position + 1 < len(matches) else len(block)
        # A final if/elseif branch is followed by its standalone end. Stop
        # before the fallback code that follows that end. The generated
        # sources use standalone end lines for these small branch blocks.
        for index in range(start + 1, end):
            if block[index].strip() == "else" or block[index].strip() == "end":
                end = index
                break
        ids = [
            int(value)
            for value in re.findall(r"(?<![A-Za-z0-9_])(\d+)(?![A-Za-z0-9_])", match.group("expr"))
            if int(value) >= 10000
        ]
        if not ids:
            raise AnalysisError(f"line {start + 1}: command id condition is missing")
        branches.append((ids, block[start:end], line_offset + start + 1))
    if not branches:
        raise AnalysisError(f"{condition_variable}: command-id branches are missing")
    return branches


def _last_assignment(lines: list[str], variable: str) -> int | None:
    # Generated if/elseif branches put a fallback assignment after an else.
    # The selected branch result is the assignment before that fallback.
    branch = lines
    for index, line in enumerate(lines):
        if re.match(r"^\s*else\s*$", line):
            branch = lines[:index]
            break
    values = _assignment_before(branch, variable)
    if not isinstance(values, list) or not values:
        return None
    return values[-1]


def _assignments(
    block: list[str], variable: str, start: int = 0, end: int | None = None
) -> list[int]:
    """Return literal assignments in one bounded block range."""
    limit = len(block) if end is None else end
    pattern = re.compile(rf"^\s*{re.escape(variable)} = (-?\d+)\s*$")
    return [
        int(match.group(1))
        for line in block[start:limit]
        if (match := pattern.match(line)) is not None
    ]


def _scalar_default(
    block: list[str], condition_variable: str, result_variable: str
) -> int:
    """Derive a scalar fallback from the generated function control flow."""
    condition = re.compile(
        rf"^\s*(?:if|elseif) {re.escape(condition_variable)} == .+? then\s*$"
    )
    condition_indices = [
        index for index, line in enumerate(block) if condition.match(line)
    ]
    if not condition_indices:
        raise AnalysisError(f"{condition_variable}: command-id branches are missing")
    first = condition_indices[0]
    last = condition_indices[-1]

    # Generated sources either put the fallback in the final else block or
    # after the final end. If neither has an assignment, use the initializer
    # that remains live for an unmatched command id.
    else_index = next(
        (
            index
            for index in range(last + 1, len(block))
            if block[index].strip() == "else"
        ),
        None,
    )
    if else_index is not None:
        end_index = next(
            (
                index
                for index in range(else_index + 1, len(block))
                if block[index].strip() == "end"
            ),
            None,
        )
        if end_index is None:
            raise AnalysisError(f"{condition_variable}: fallback end is missing")
        values = _assignments(block, result_variable, else_index + 1, end_index)
        if values:
            return values[-1]
        tail = _assignments(block, result_variable, end_index + 1)
        if tail:
            return tail[-1]
    else:
        end_index = next(
            (
                index
                for index in range(last + 1, len(block))
                if block[index].strip() == "end"
            ),
            None,
        )
        if end_index is None:
            raise AnalysisError(f"{condition_variable}: fallback end is missing")
        tail = _assignments(block, result_variable, end_index + 1)
        if tail:
            return tail[-1]

    values = _assignments(block, result_variable, 0, first)
    if values:
        return values[-1]
    raise AnalysisError(f"{condition_variable}: scalar fallback is missing")


def _group_overrides(
    values: dict[int, Any], source_lines: dict[int, int], default: Any
) -> list[dict[str, Any]]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for command_id, value in sorted(values.items()):
        if value != default:
            grouped[json.dumps(value, sort_keys=True, separators=(",", ":"))].append(
                command_id
            )
    overrides: list[dict[str, Any]] = []
    for encoded, command_ids in sorted(grouped.items(), key=lambda item: item[1][0]):
        result = json.loads(encoded)
        overrides.append(
            {
                "commandIds": command_ids,
                "result": result,
                "sourceLines": sorted({source_lines[command_id] for command_id in command_ids}),
            }
        )
    return overrides


def _scalar_rule(
    getter: str,
    block: list[str],
    condition_variable: str,
    result_variable: str,
    line_offset: int,
) -> dict[str, Any]:
    default = _scalar_default(block, condition_variable, result_variable)
    branches = _condition_branches(block, condition_variable, line_offset)
    values: dict[int, int] = {}
    source_lines: dict[int, int] = {}
    for command_ids, branch, line in branches:
        value = _last_assignment(branch, result_variable)
        if value is None:
            continue
        for command_id in command_ids:
            if command_id in values:
                raise AnalysisError(f"{getter}: duplicate command id {command_id}")
            values[command_id] = value
            source_lines[command_id] = line
    if not values:
        raise AnalysisError(f"{getter}: no constant branch results found")
    return {
        "default": default,
        "overrides": _group_overrides(values, source_lines, default),
    }


def _command_information_rule(block: list[str], line_offset: int) -> dict[str, Any]:
    default = _scalar_default(block, "L2_2", "L12_2")
    branches = _condition_branches(block, "L2_2", line_offset)
    values: dict[int, int] = {}
    source_lines: dict[int, int] = {}
    for command_ids, branch, line in branches:
        value = _last_assignment(branch, "L12_2")
        if value is None:
            value = _last_assignment(branch, "L21_2")
        if value is None:
            raise AnalysisError(f"getCommandInformation: branch at line {line} has no result")
        for command_id in command_ids:
            if command_id in values:
                raise AnalysisError(f"getCommandInformation: duplicate command id {command_id}")
            values[command_id] = value
            source_lines[command_id] = line
    selector_matches = [
        re.match(r"^\s*if A1_2 == (\d+) then\s*$", line)
        for line in block
    ]
    selectors = [int(match.group(1)) for match in selector_matches if match]
    if selectors != [8]:
        raise AnalysisError("getCommandInformation: selector boundary drifted")
    return {
        "default": default,
        "selector": 8,
        "otherSelectors": "nil",
        "overrides": _group_overrides(values, source_lines, default),
    }


def _parts_rule(block: list[str], line_offset: int) -> dict[str, Any]:
    branches = _condition_branches(block, "L1_2", line_offset)
    values: dict[int, list[int]] = {}
    source_lines: dict[int, int] = {}
    for command_ids, branch, line in branches:
        match = re.search(
            r"(?ms)^\s*L2_2 = (-?\d+)\s*$.*?^\s*L3_2 = (-?\d+)\s*$.*?^\s*return L2_2, L3_2\s*$",
            "\n".join(branch),
        )
        if match is None:
            raise AnalysisError(f"getPartsDamageAdjust: branch at line {line} has no pair")
        result = [int(match.group(1)), int(match.group(2))]
        for command_id in command_ids:
            if command_id in values:
                raise AnalysisError(f"getPartsDamageAdjust: duplicate command id {command_id}")
            values[command_id] = result
            source_lines[command_id] = line
    default_match = re.search(
        r"(?ms)^\s*else\s*$.*?^\s*L2_2 = (-?\d+)\s*$.*?^\s*L3_2 = (-?\d+)\s*$.*?^\s*return L2_2, L3_2\s*$",
        "\n".join(block),
    )
    if default_match is None:
        raise AnalysisError("getPartsDamageAdjust: default pair is missing")
    default = [int(default_match.group(1)), int(default_match.group(2))]
    return {
        "default": default,
        "returnArity": 2,
        "overrides": _group_overrides(values, source_lines, default),
    }


def _class_declaration(lines: list[str]) -> tuple[str, str]:
    prefix = "\n".join(lines[:10])
    parent_match = re.search(r'L1_1 = "(?P<parent>/Command/[^"]+)"', prefix)
    class_match = re.search(
        r'L1_1 = "(?P<class>MonsterAttackWeaponSkill)"\s*\nL2_1 = "(?P<base>WeaponSkillBaseClass)"',
        prefix,
    )
    if parent_match is None or class_match is None:
        raise AnalysisError("class declaration drifted")
    parent = parent_match.group("parent")
    class_name = class_match.group("class")
    base_name = class_match.group("base")
    expected_base = PARENT_PATH.rsplit("/", 1)[-1]
    if parent != PARENT_PATH or base_name != expected_base or class_name != "MonsterAttackWeaponSkill":
        raise AnalysisError("class declaration does not match MonsterAttackWeaponSkill")
    return class_name, parent


def analyze(scripts_root: Path | None = None) -> dict[str, Any]:
    """Build the bounded profile from the exact decoded Lua source file."""
    scripts_root = resolve_scripts_root(SCRIPTS_ROOT, scripts_root)
    validate_scripts_root(scripts_root)
    source_manifest_row = _source_manifest_row()
    source_path = _source_path(scripts_root)
    try:
        data = source_path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise AnalysisError(f"cannot read {SOURCE_RELATIVE.as_posix()}: {exc}") from exc
    digest = _sha256(data)
    if digest != source_manifest_row["sha256"].lower():
        raise AnalysisError(
            f"{SOURCE_RELATIVE.as_posix()}: sha256 {digest} does not match retained source"
        )
    lines = text.splitlines()
    if (
        len(data) != source_manifest_row["bytes"]
        or len(lines) != source_manifest_row["lineCount"]
    ):
        raise AnalysisError(f"{SOURCE_RELATIVE.as_posix()}: source size or line count drifted")
    class_name, parent = _class_declaration(lines)

    starts: dict[str, int] = {}
    rules: dict[str, dict[str, Any]] = {}
    for getter in GETTER_NAMES:
        start, _end, block = _function_block(lines, getter)
        starts[getter] = start + 1
        if getter == "getCommandInformation":
            rule = _command_information_rule(block, start)
        elif getter == "getFrequency":
            rule = _scalar_rule(getter, block, "L3_2", "L1_2", start)
        elif getter == "getRangeWidth":
            rule = _scalar_rule(getter, block, "L4_2", "L5_2", start)
        elif getter == "getRangeRotate":
            rule = _scalar_rule(getter, block, "L6_2", "L5_2", start)
        elif getter == "getCommandRangeHeight":
            rule = _scalar_rule(getter, block, "L4_2", "L5_2", start)
        else:
            rule = _parts_rule(block, start)
        rule["definitionLine"] = start + 1
        rules[getter] = rule

    override_count = sum(len(rule["overrides"]) for rule in rules.values())
    override_command_count = sum(
        sum(len(override["commandIds"]) for override in rule["overrides"])
        for rule in rules.values()
    )
    rules_sha256 = _canonical_sha256(rules)
    if rules_sha256 != GETTER_RULES_SHA256:
        raise AnalysisError("getter rule digest drifted")
    summary = {
        "getterCount": len(rules),
        "overrideGroupCount": override_count,
        "overrideCommandCount": override_command_count,
    }
    if summary != SUMMARY:
        raise AnalysisError("getter rule summary drifted")
    return {
        "version": "1",
        "gameVersion": GAME_VERSION,
        "extraction": EXTRACTION,
        "classPath": CLASS_PATH,
        "parentPath": parent,
        "getterRulesSha256": rules_sha256,
        "source": {
            "script": SOURCE_PATH,
            "sha256": digest,
            "bytes": len(data),
            "lineCount": len(lines),
            "manifest": "manifests/scripts.json",
        },
        "summary": summary,
        "getterRules": rules,
        "unresolved": UNRESOLVED,
    }


def render_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def validate_retained(report: dict[str, Any]) -> list[str]:
    """Validate the pinned manifest without requiring decoded Lua bytes."""
    problems: list[str] = []
    if not isinstance(report, dict):
        return ["schema validation failed: report must be an object"]
    try:
        source_manifest_row = _source_manifest_row()
    except AnalysisError as exc:
        problems.append(str(exc))
        source_manifest_row = None
    source = report.get("source")
    if not isinstance(source, dict):
        return ["source record is missing"]
    expected_source = None
    if source_manifest_row is not None:
        expected_source = {
            "script": source_manifest_row["relativePath"],
            "sha256": source_manifest_row["sha256"].lower(),
            "bytes": source_manifest_row["bytes"],
            "lineCount": source_manifest_row["lineCount"],
            "manifest": "manifests/scripts.json",
        }
    if expected_source is not None and source != expected_source:
        problems.append("source pin disagrees")
    if report.get("version") != "1":
        problems.append("version disagrees")
    if report.get("gameVersion") != GAME_VERSION:
        problems.append("game version disagrees")
    if report.get("extraction") != EXTRACTION:
        problems.append("extraction disagrees")
    if report.get("classPath") != CLASS_PATH:
        problems.append("class path disagrees")
    if report.get("parentPath") != PARENT_PATH:
        problems.append("parent path disagrees")
    if report.get("getterRulesSha256") != GETTER_RULES_SHA256:
        problems.append("getter rule digest disagrees")
    elif _canonical_sha256(report.get("getterRules")) != GETTER_RULES_SHA256:
        problems.append("getter rules disagree")
    if report.get("summary") != SUMMARY:
        problems.append("summary disagrees")
    if report.get("unresolved") != UNRESOLVED:
        problems.append("unresolved boundaries disagree")
    try:
        import jsonschema
    except ImportError:
        problems.append("schema validation unavailable: install jsonschema")
    else:
        try:
            schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
            validator = jsonschema.Draft202012Validator(schema)
            for error in sorted(
                validator.iter_errors(report), key=lambda item: list(item.path)
            ):
                location = ".".join(str(part) for part in error.path)
                suffix = f" at {location}" if location else ""
                problems.append(f"schema validation failed{suffix}: {error.message}")
        except jsonschema.exceptions.SchemaError as exc:
            problems.append(f"schema validation failed: invalid schema: {exc.message}")
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            problems.append(f"schema validation failed: {exc}")
    return problems


def _selected_root(args: argparse.Namespace) -> tuple[Path, bool]:
    explicit = args.scripts_root is not None or bool(os.environ.get("XIVL_LUA_SCRIPTS_DIR"))
    return resolve_scripts_root(SCRIPTS_ROOT, args.scripts_root), explicit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--scripts-root",
        type=Path,
        help=(
            "directory containing decoded .lua files (default: lua/scripts, "
            "or XIVL_LUA_SCRIPTS_DIR)"
        ),
    )
    args = parser.parse_args()
    try:
        root, explicit = _selected_root(args)
        source = _source_path(root)
        if not args.check or explicit or source.is_file():
            report = analyze(root)
        else:
            report = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
            problems = validate_retained(report)
            if problems:
                raise AnalysisError("; ".join(problems))
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        AnalysisError,
        CorpusRootError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    rendered = render_json(report)
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != rendered:
            print(f"error: {OUTPUT_PATH.relative_to(REPO_ROOT)} is stale", file=sys.stderr)
            return 1
        print("PASS: MonsterAttackWeaponSkill getter profile is current")
        return 0
    OUTPUT_PATH.write_bytes(rendered)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
