#!/usr/bin/env python3
"""Build and check the retail quest selector consumer report."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from _corpus import CorpusRootError, resolve_scripts_root, validate_scripts_root


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "lua" / "scripts"
OUTPUT_PATH = REPO_ROOT / "manifests" / "quest_selector_consumers.json"

SOURCE_HASHES = {
    "csv/quest.csv": "bdadece1907b7050aaeee7c94a2a2d395fe76b504e47cbb1616b57ba380209dc",
    "csv/xtx_quest.csv": "938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719",
    "csv/worldMaster.csv": "2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643",
}

JOB_BASE_CLASS_IDS = {
    "Warrior": 4,
    "Monk": 2,
    "White Mage": 23,
    "Black Mage": 22,
    "Paladin": 3,
    "Bard": 7,
    "Dragoon": 8,
}
JOB_SELECTOR_IDS = {
    "Monk": 15,
    "Paladin": 16,
    "Warrior": 17,
    "Bard": 18,
    "Dragoon": 19,
    "Black Mage": 26,
    "White Mage": 27,
}
JOB_SCRIPT_FAMILIES = {
    111200: "war",
    111220: "mnk",
    111240: "whm",
    111260: "blm",
    111280: "pld",
    111300: "brd",
    111320: "drg",
}
EXPECTED_NAMED_IDS = [
    base + offset
    for base in JOB_SCRIPT_FAMILIES
    for offset in range(1, 7)
]
EXPECTED_NAMED_ROWS_SHA256 = (
    "72c8867c28d8836525e92308a2a1404aabadbdeaf446200cf51747921f5ebe64"
)
CLASS_IDS = {
    "Pugilist": 2,
    "Gladiator": 3,
    "Marauder": 4,
    "Archer": 7,
    "Lancer": 8,
    "Thaumaturge": 22,
    "Conjurer": 23,
}
NAMED_RE = re.compile(
    r"^(?P<primary>[A-Za-z ]+), [Ll]evel (?P<level>\d+) & (?P<secondary>[A-Za-z]+)$"
)
MESSAGE_FIELDS = {
    51130: ("questId", "primarySelectorId", "primaryLevel", "secondarySelectorId", "secondaryLevel"),
    51131: ("questId", "primarySelectorId"),
    51132: ("questId", "primarySelectorId"),
}
MESSAGE_ROLES = {
    51130: "two-level requirement presentation",
    51131: "active primary class or job required to accept",
    51132: "active primary class or job required to advance",
}


class AnalysisError(ValueError):
    """The source inputs no longer match the bounded selector contract."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_csv(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _numeric_rows(path: Path) -> dict[int, tuple[int, list[str]]]:
    rows = {}
    for line, row in enumerate(_read_csv(path), 1):
        if row and row[0].strip().isdigit():
            rows[int(row[0])] = (line, row)
    return rows


def census_rows(client_data_root: Path) -> tuple[list[dict], dict, list[dict]]:
    """Return all named rows, selector-shape counts, and fixed controls."""
    csv_root = client_data_root / "csv"
    for relative, expected in SOURCE_HASHES.items():
        path = client_data_root / relative
        if not path.is_file():
            raise AnalysisError(f"source missing: {path}")
        actual = sha256(path)
        if actual != expected:
            raise AnalysisError(f"{relative}: expected sha256 {expected}, got {actual}")

    quest_rows = _numeric_rows(csv_root / "quest.csv")
    text_rows = _numeric_rows(csv_root / "xtx_quest.csv")
    counts = {"namedBoth": 0, "disciplineSingle": 0, "allNoSelector": 0, "other": 0}
    named = []
    labels = {}
    for quest_id, (text_line, row) in sorted(text_rows.items()):
        label = row[42].strip() if len(row) > 42 else ""
        labels[quest_id] = label
        match = NAMED_RE.fullmatch(label)
        if match is not None:
            counts["namedBoth"] += 1
            primary = match.group("primary")
            secondary = match.group("secondary")
            primary_base_id = JOB_BASE_CLASS_IDS.get(primary, CLASS_IDS.get(primary))
            primary_selector_id = JOB_SELECTOR_IDS.get(primary, CLASS_IDS.get(primary))
            if primary_base_id is None or primary_selector_id is None or secondary not in CLASS_IDS:
                raise AnalysisError(f"xtx_quest row {quest_id}: unknown named selector")
            if quest_id not in quest_rows:
                raise AnalysisError(f"quest row {quest_id}: numeric row missing")
            quest_line, quest_row = quest_rows[quest_id]
            level = int(quest_row[52])
            label_level = int(match.group("level"))
            if level != label_level:
                raise AnalysisError(f"quest row {quest_id}: level disagrees with label")
            named.append({
                "questId": quest_id,
                "questCsvLine": quest_line,
                "xtxQuestCsvLine": text_line,
                "label": label,
                "primarySelector": primary,
                "primarySelectorId": primary_selector_id,
                "primaryBaseClassId": primary_base_id,
                "primaryLevel": level,
                "secondaryClass": secondary,
                "secondaryClassId": CLASS_IDS[secondary],
                "secondaryLevel": 15 if quest_id % 20 == 1 else None,
            })
        elif label.startswith("Disciples of "):
            counts["disciplineSingle"] += 1
        elif label == "All":
            counts["allNoSelector"] += 1
        else:
            counts["other"] += 1

    if counts != {"namedBoth": 42, "disciplineSingle": 126, "allNoSelector": 66, "other": 501}:
        raise AnalysisError(f"selector shape census drifted: {counts}")
    if [row["questId"] for row in named] != EXPECTED_NAMED_IDS:
        raise AnalysisError("named selector row set drifted")

    control_ids = (110627, 110813, 110814, 110001)
    controls = []
    for quest_id in control_ids:
        text_line, _ = text_rows[quest_id]
        controls.append({
            "questId": quest_id,
            "xtxQuestCsvLine": text_line,
            "label": labels[quest_id],
            "shape": "no selector" if labels[quest_id] == "All" else "discipline selector",
        })
    return named, counts, controls


def _message_at(path: Path, line_index: int, message_id: int) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    setup = lines[line_index - 4:line_index]
    receiver = re.fullmatch(r"\s*(L\d+_2) = worldMaster", setup[0]) if len(setup) == 4 else None
    if (
        receiver is None
        or re.fullmatch(rf"\s*L\d+_2 = {receiver.group(1)}", setup[1]) is None
        or re.fullmatch(
            rf"\s*{receiver.group(1)} = {receiver.group(1)}\.say", setup[2]
        ) is None
        or re.fullmatch(r"\s*L\d+_2 = worldMaster", setup[3]) is None
    ):
        raise AnalysisError(f"{path}:{line_index + 1}: message sink is not worldMaster.say")
    fields = MESSAGE_FIELDS[message_id]
    values = []
    for line in lines[line_index + 1:line_index + 1 + len(fields)]:
        match = re.fullmatch(r"\s*L\d+_2 = (\d+)", line)
        if match is None:
            raise AnalysisError(f"{path}:{line_index + 1}: message arguments drifted")
        values.append(int(match.group(1)))
    call_line = lines[line_index + 1 + len(fields)]
    if re.fullmatch(r"\s*L\d+_2\(L\d+_2(?:, L\d+_2)+\)", call_line) is None:
        raise AnalysisError(f"{path}:{line_index + 1}: message call drifted")
    row = dict(zip(fields, values, strict=True))
    row.update({"messageId": message_id, "role": MESSAGE_ROLES[message_id]})
    return row


def analyze_script_consumers(scripts_root: Path | None = None) -> list[dict]:
    """Enumerate every job-quest use of messages 51130 through 51132."""
    scripts_root = resolve_scripts_root(SCRIPTS_ROOT, scripts_root)
    validate_scripts_root(scripts_root)
    if not scripts_root.is_dir():
        raise AnalysisError(f"Lua corpus not found: {scripts_root}")
    rows = []
    scenario_root = scripts_root / "quest" / "scenario"
    pattern = re.compile(r"\s*L\d+_2 = (5113[0-2])$")
    for path in sorted(scenario_root.rglob("*.lua")):
        relative = path.relative_to(scripts_root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            match = pattern.fullmatch(line)
            if match is None:
                continue
            message_id = int(match.group(1))
            row = {
                "script": f"lua/scripts/{relative}",
                "line": index + 1,
                **_message_at(path, index, message_id),
            }
            rows.append(row)
    counts = {message_id: sum(row["messageId"] == message_id for row in rows) for message_id in MESSAGE_FIELDS}
    if counts != {51130: 7, 51131: 42, 51132: 42}:
        raise AnalysisError(f"message consumer census drifted: {counts}")
    for row in rows:
        if row["messageId"] == 51130 and (row["primaryLevel"], row["secondaryLevel"]) != (30, 15):
            raise AnalysisError(f"{row['script']}:{row['line']}: two-level requirement drifted")
    return rows


def _corpus_pins() -> dict:
    return {
        "manifest": "manifests/scripts.json",
        "manifestSha256": sha256(REPO_ROOT / "manifests" / "scripts.json"),
        "registry": "lua/registry.json",
        "registrySha256": sha256(REPO_ROOT / "lua" / "registry.json"),
        "napiIndex": "lua/napi_index.json",
        "napiIndexSha256": sha256(REPO_ROOT / "lua" / "napi_index.json"),
        "scriptCount": 2671,
    }


def validate_selector_alignment(named: list[dict], consumers: list[dict]) -> None:
    """Require retained CSV selectors to agree with their script presentations."""
    by_script_message = {
        (row.get("script"), row.get("messageId")): row
        for row in consumers
    }
    for row in named:
        quest_id = row["questId"]
        base = quest_id - (quest_id % 20)
        offset = quest_id - base
        family = JOB_SCRIPT_FAMILIES.get(base)
        script = f"lua/scripts/quest/scenario/{family}/{family}0j{offset}.lua"
        for message_id in (51131, 51132):
            consumer = by_script_message.get((script, message_id))
            if consumer is None or consumer.get("primarySelectorId") != row["primarySelectorId"]:
                raise AnalysisError(
                    f"quest {quest_id}: {message_id} active-primary selector disagrees"
                )
            expected_quest_id = 111304 if quest_id == 111324 and message_id == 51132 else quest_id
            if consumer.get("questId") != expected_quest_id:
                raise AnalysisError(f"quest {quest_id}: {message_id} quest ID disagrees")
        two_level = by_script_message.get((script, 51130))
        if row["secondaryLevel"] is None:
            if two_level is not None:
                raise AnalysisError(f"quest {quest_id}: unexpected two-level consumer")
            continue
        expected = (
            row["primarySelectorId"], row["primaryLevel"],
            row["secondaryClassId"], row["secondaryLevel"],
        )
        actual = (
            two_level.get("primarySelectorId"), two_level.get("primaryLevel"),
            two_level.get("secondarySelectorId"), two_level.get("secondaryLevel"),
        ) if two_level is not None else None
        if actual != expected:
            raise AnalysisError(f"quest {quest_id}: CSV and script selectors disagree")


def build_report(client_data_root: Path, scripts_root: Path | None = None) -> dict:
    named, counts, controls = census_rows(client_data_root)
    consumers = analyze_script_consumers(scripts_root)
    validate_selector_alignment(named, consumers)
    return {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": "2012.09.19.0001",
        "corpus": _corpus_pins(),
        "clientDataSources": [
            {"source": f"xivl-client-data:{path}", "sha256": digest}
            for path, digest in SOURCE_HASHES.items()
        ],
        "summary": {
            **counts,
            "twoLevelMessageConsumers": 7,
            "activePrimaryAcceptConsumers": 42,
            "activePrimaryAdvanceConsumers": 42,
        },
        "namedRows": named,
        "controls": controls,
        "messageConsumers": consumers,
        "presentationContract": {
            "twoLevelMessage": "51130 formats primary level 30 and secondary level 15",
            "activeAcceptMessage": "51131 formats only the required active primary class or job",
            "activeAdvanceMessage": "51132 formats only the required active primary class or job",
            "sink": "worldMaster.say -> DesktopWidget.showMessage -> DesktopWidget._appendMessagePool",
            "sinkBcsId": "BCS-Y-0492",
        },
        "requestContract": {
            "questInfoAsk": "approval returns 1 and refusal returns 2",
            "selectorArguments": 0,
        },
        "unresolved": [
            "The recovered client scripts do not choose which named job-quest error event the server dispatches.",
            "No retained retail acceptance capture establishes whether the authoritative server checks the primary selector, the secondary selector, both selectors, or only prior job unlock state.",
            "Rows 2 through 6 in each job family retain the secondary class in localized eligibility text but have no recovered 51130 two-level message consumer.",
            "The Dragoon row 111324 advance consumer passes quest ID 111304 while retaining Dragoon selector 19; the report preserves the shipped arguments.",
        ],
    }


def render_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def validate_retained(report: dict) -> list[str]:
    problems = []
    expected_sources = [
        {"source": f"xivl-client-data:{path}", "sha256": digest}
        for path, digest in SOURCE_HASHES.items()
    ]
    if report.get("clientDataSources") != expected_sources:
        problems.append("client-data source pins disagree")
    if report.get("corpus") != _corpus_pins():
        problems.append("corpus pins disagree")
    named = report.get("namedRows", [])
    if len(named) != 42 or sum(row.get("secondaryLevel") == 15 for row in named) != 7:
        problems.append("named row census disagrees")
    if [row.get("questId") for row in named] != EXPECTED_NAMED_IDS:
        problems.append("named selector row set disagrees")
    if _json_sha256(named) != EXPECTED_NAMED_ROWS_SHA256:
        problems.append("named selector row content disagrees")
    consumers = report.get("messageConsumers", [])
    counts = {message_id: sum(row.get("messageId") == message_id for row in consumers) for message_id in MESSAGE_FIELDS}
    if counts != {51130: 7, 51131: 42, 51132: 42}:
        problems.append("message consumer counts disagree")
    try:
        validate_selector_alignment(named, consumers)
    except (KeyError, TypeError, AnalysisError) as exc:
        problems.append(f"selector alignment disagrees: {exc}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-data-root", type=Path)
    parser.add_argument(
        "--scripts-root",
        type=Path,
        help=(
            "directory containing decoded .lua files (default: lua/scripts, "
            "or XIVL_LUA_SCRIPTS_DIR)"
        ),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    scripts_root = resolve_scripts_root(SCRIPTS_ROOT, args.scripts_root)
    explicit_scripts_root = (
        args.scripts_root is not None
        or bool(os.environ.get("XIVL_LUA_SCRIPTS_DIR"))
    )
    try:
        if explicit_scripts_root:
            validate_scripts_root(scripts_root)
        if args.client_data_root is not None:
            report = build_report(args.client_data_root.resolve(), scripts_root)
            problems = validate_retained(report)
            if problems:
                raise AnalysisError("; ".join(problems))
        else:
            if not args.check:
                parser.error("--client-data-root is required when generating")
            report = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
            problems = validate_retained(report)
            if problems:
                raise AnalysisError("; ".join(problems))
            if scripts_root.is_dir() and report["messageConsumers"] != analyze_script_consumers(scripts_root):
                raise AnalysisError("message consumer report is stale")
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
        if OUTPUT_PATH.read_bytes() != rendered:
            print(f"error: {OUTPUT_PATH.relative_to(REPO_ROOT)} is stale", file=sys.stderr)
            return 1
        print("PASS: 42 named quest rows and 91 message consumers match")
        return 0
    OUTPUT_PATH.write_bytes(rendered)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
