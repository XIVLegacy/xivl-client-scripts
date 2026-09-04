"""Internal builders and shared helpers for the Lua corpus."""

from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import stat
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterator


EXTRACTION_VERSION = "2012.09.19.0001"


class CorpusRootError(ValueError):
    """The selected Lua source root is missing or not a plain tree."""


def _is_link_or_reparse(path: Path, result: os.stat_result) -> bool:
    """Return whether a path is a link or Windows reparse point."""
    is_junction = getattr(os.path, "isjunction", None)
    return (
        path.is_symlink()
        or (is_junction is not None and is_junction(path))
        or bool(getattr(result, "st_file_attributes", 0) & 0x0400)
    )


def validate_scripts_root(scripts_root: Path) -> Path:
    """Validate a Lua source root before any enumeration or writes."""
    scripts_root = Path(scripts_root)
    try:
        root_result = os.lstat(scripts_root)
    except OSError as exc:
        raise CorpusRootError(
            f"Lua corpus not found or unreadable: {scripts_root}"
        ) from exc
    if _is_link_or_reparse(scripts_root, root_result):
        raise CorpusRootError(
            f"Lua scripts root must be a plain directory: {scripts_root}"
        )
    if not stat.S_ISDIR(root_result.st_mode):
        raise CorpusRootError(
            f"Lua scripts root must be a plain directory: {scripts_root}"
        )

    def onerror(exc: OSError) -> None:
        raise CorpusRootError(
            f"Lua scripts root cannot be inspected: {scripts_root}"
        ) from exc

    for current, directories, files in os.walk(
        scripts_root, topdown=True, followlinks=False, onerror=onerror
    ):
        for name in (*directories, *files):
            candidate = Path(current) / name
            try:
                result = os.lstat(candidate)
            except OSError as exc:
                raise CorpusRootError(
                    f"Lua scripts root cannot inspect descendant: {candidate}"
                ) from exc
            if _is_link_or_reparse(candidate, result):
                raise CorpusRootError(
                    f"Lua scripts root contains linked or reparse path: {candidate}"
                )
            if name in directories and not stat.S_ISDIR(result.st_mode):
                raise CorpusRootError(
                    f"Lua scripts root contains non-directory path: {candidate}"
                )
            if name in files and not stat.S_ISREG(result.st_mode):
                raise CorpusRootError(
                    f"Lua scripts root contains non-regular file: {candidate}"
                )
    return scripts_root


def resolve_scripts_root(default: Path, explicit: Path | None = None) -> Path:
    """Resolve an explicit or environment-configured Lua source root."""
    if explicit is None:
        configured = os.environ.get("XIVL_LUA_SCRIPTS_DIR")
        explicit = Path(configured) if configured else default
    # Keep the final component intact so validation can reject a symlink,
    # junction, or other reparse point instead of validating its target.
    return explicit.expanduser().absolute()


def write_json(path: Path, obj: object) -> None:
    """Write byte-stable UTF-8 JSON with LF endings on Windows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def iter_lua(root: Path) -> Iterator[tuple[Path, str]]:
    """Yield paths and POSIX stems in cross-platform stable order."""
    paths = sorted(
        root.rglob("*.lua"),
        key=lambda p: p.relative_to(root).with_suffix("").as_posix(),
    )
    for path in paths:
        yield path, path.relative_to(root).with_suffix("").as_posix()


def line_count(content: str) -> int:
    """Count lines with the annotator's splitlines semantics."""
    return len(content.splitlines())


def build_script_manifest(scripts_root: Path) -> dict:
    """Build the byte-for-byte reproduction contract for canonical scripts."""
    validate_scripts_root(scripts_root)
    scripts = []
    total_bytes = 0
    for lua_path, decoded in iter_lua(scripts_root):
        data = lua_path.read_bytes()
        total_bytes += len(data)
        scripts.append(
            {
                "relativePath": f"lua/scripts/{decoded}.lua",
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest().upper(),
                "lineCount": line_count(data.decode("utf-8")),
            }
        )
    return {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": EXTRACTION_VERSION,
        "pipeline": {
            "orchestrator": (
                "XIVLegacy/xivl-client-structs:tools/lpb_pipeline.py"
            ),
            "decoder": "XIVLegacy/xivl-client-structs:tools/decode_lpb.py",
            "decompiler": "user-supplied unluac.jar",
            "canonicalization": "replace CRLF byte pairs with LF",
        },
        "scriptCount": len(scripts),
        "totalBytes": total_bytes,
        "scripts": scripts,
    }


def copy_lua_lf(source: Path, destination: Path) -> None:
    """Publish Lua bytes with only CRLF line endings normalized to LF."""
    destination.write_bytes(source.read_bytes().replace(b"\r\n", b"\n"))


def decode_filename_segment(s: str) -> str:
    """Inverse-cipher one path segment."""
    out = []
    for c in s.lower():
        if c.isalpha():
            pos = ord(c) - ord("a") + 1
            if 1 <= pos <= 10:
                out.append(str(10 - pos))
            else:
                out.append(chr(ord("a") + (37 - pos) - 1))
        elif c.isdigit():
            out.append(chr(ord("a") + (10 - int(c)) - 1))
        else:
            out.append(c)
    return "".join(out)


def decode_path(ciphered_path: str) -> str:
    """Decode each path segment via the cipher. Preserve the structure."""
    parts = ciphered_path.replace("\\", "/").split("/")
    return "/".join(decode_filename_segment(part) for part in parts)


_RESERVED_RHS = {"_G", "require", "_defineClass", "_defineBaseClass"}
CLASS_ASSIGN_RE = re.compile(
    r"^L\d+_\d+\s*=\s*(?![AL]\d+_\d+\s*$)([A-Z][A-Za-z0-9_]+)\s*$",
    re.MULTILINE,
)
METHOD_ASSIGN_RE = re.compile(
    r"^L\d+_\d+\.(_?[a-zA-Z][a-zA-Z0-9_]*)\s*=\s*L\d+_\d+\s*$",
    re.MULTILINE,
)
STRING_LITERAL_RE = re.compile(r'"([A-Z][A-Za-z0-9_]+)"')
REQUIRE_RE = re.compile(
    r"^(L\d+_\d+)[ \t]*=[ \t]*require[ \t]*\n"
    r'(L\d+_\d+)[ \t]*=[ \t]*"(/[A-Za-z0-9_/]+)"[ \t]*\n'
    r"\1\(\2\)[ \t]*$",
    re.MULTILINE,
)
IDENT_RE = re.compile(r"(?<!\w)(_[a-zA-Z][a-zA-Z0-9_]*)")


def extract_signals(
    content: str,
    decoded_basename: str,
) -> tuple[list[str], list[str], list[str]]:
    """Return class names, method names, and requires from script content."""
    classes: list[str] = []
    seen_classes = set()
    for match in CLASS_ASSIGN_RE.finditer(content):
        name = match.group(1)
        if name in _RESERVED_RHS or name in seen_classes:
            continue
        seen_classes.add(name)
        classes.append(name)

    if not classes:
        for match in STRING_LITERAL_RE.finditer(content):
            literal = match.group(1)
            if literal.lower() == decoded_basename and literal not in seen_classes:
                seen_classes.add(literal)
                classes.append(literal)
                break

    methods: list[str] = []
    seen_methods = set()
    for match in METHOD_ASSIGN_RE.finditer(content):
        name = match.group(1)
        if name not in seen_methods:
            seen_methods.add(name)
            methods.append(name)

    requires: list[str] = []
    seen_requires = set()
    for match in REQUIRE_RE.finditer(content):
        path = match.group(3)
        if path not in seen_requires:
            seen_requires.add(path)
            requires.append(path)
    return classes, methods, requires


def build_registry(lua_root: Path) -> dict:
    """Build registry data from an explicit ciphered decompile tree."""
    scripts: dict[str, dict] = {}
    for lua_path, ciphered_stem in iter_lua(lua_root):
        relative = lua_path.relative_to(lua_root).as_posix()
        decoded = decode_path(ciphered_stem)
        content = lua_path.read_text(encoding="utf-8")
        classes, methods, requires = extract_signals(
            content,
            decoded.rsplit("/", 1)[-1],
        )
        scripts[decoded] = {
            "ciphered": relative,
            "classes": classes,
            "methods": methods,
            "requires": requires,
            "lineCount": line_count(content),
        }
    scripts = dict(sorted(scripts.items()))
    return {
        "version": "1",
        "gameVersion": "1.23b",
        "extraction": EXTRACTION_VERSION,
        "source": (
            "ciphered LPB decompile output "
            "(XIVLegacy/xivl-client-structs tools/lpb_pipeline.py); "
            "regeneration is an explicit-path research run"
        ),
        "scriptCount": len(scripts),
        "scripts": scripts,
    }


def _ignore_lua(_directory: str, names: list[str]) -> list[str]:
    """Preserve generated sidecars while replacing published Lua files."""
    return [name for name in names if name.endswith(".lua")]


def _remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def _install_publication(
    staged_registry: Path,
    staged_scripts: Path,
    output_root: Path,
) -> None:
    """Install both staged outputs, restoring both on any failure."""
    output_root.mkdir(parents=True, exist_ok=True)
    final_registry = output_root / "registry.json"
    final_scripts = output_root / "scripts"
    backup_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}-backup-", dir=output_root.parent)
    )
    backup_registry = backup_root / "registry.json"
    backup_scripts = backup_root / "scripts"
    registry_backed_up = scripts_backed_up = False
    registry_installed = scripts_installed = False
    rollback_complete = False
    try:
        if final_registry.exists():
            os.replace(final_registry, backup_registry)
            registry_backed_up = True
        if final_scripts.exists():
            os.replace(final_scripts, backup_scripts)
            scripts_backed_up = True
        os.replace(staged_registry, final_registry)
        registry_installed = True
        os.replace(staged_scripts, final_scripts)
        scripts_installed = True
        rollback_complete = True
    except OSError as install_error:
        rollback_errors: list[str] = []
        for installed, final_path in (
            (scripts_installed, final_scripts),
            (registry_installed, final_registry),
        ):
            if installed:
                try:
                    _remove_path(final_path)
                except OSError as exc:
                    rollback_errors.append(f"remove {final_path}: {exc}")
        for backed_up, backup_path, final_path in (
            (registry_backed_up, backup_registry, final_registry),
            (scripts_backed_up, backup_scripts, final_scripts),
        ):
            if backed_up:
                try:
                    os.replace(backup_path, final_path)
                except OSError as exc:
                    rollback_errors.append(f"restore {final_path}: {exc}")
        rollback_complete = not rollback_errors
        if rollback_errors:
            details = "; ".join(rollback_errors)
            raise RuntimeError(
                f"publication failed and rollback was incomplete: {details}; "
                f"recovery files remain in {backup_root}"
            ) from install_error
        raise
    finally:
        if rollback_complete:
            shutil.rmtree(backup_root)


def publish_corpus(
    lua_root: Path,
    output_root: Path,
    copy_file: Callable[[Path, Path], object] = copy_lua_lf,
) -> int:
    """Stage and publish a registry plus decoded script tree together."""
    if not lua_root.is_dir():
        print(
            f"error: {lua_root} not found - provide --lua-root pointing at "
            "a decompile output tree",
            file=sys.stderr,
        )
        return 1

    output_root = output_root.resolve()
    output_root.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}-publish-", dir=output_root.parent)
    )
    staged_registry = stage_root / "registry.json"
    staged_scripts = stage_root / "scripts"
    try:
        registry = build_registry(lua_root)
        final_scripts = output_root / "scripts"
        if final_scripts.is_dir():
            shutil.copytree(final_scripts, staged_scripts, ignore=_ignore_lua)
        else:
            staged_scripts.mkdir(parents=True)

        for decoded, metadata in registry["scripts"].items():
            source = lua_root / metadata["ciphered"]
            destination = staged_scripts / f"{decoded}.lua"
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy_file(source, destination)

        write_json(staged_registry, registry)
        _install_publication(staged_registry, staged_scripts, output_root)
    except (OSError, UnicodeError, RuntimeError) as exc:
        print(f"error: publication failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root)

    print(
        f"published {registry['scriptCount']} scripts and registry to {output_root}"
    )
    return 0


def load_api_index(path: Path) -> dict[str, list[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    api_bcs: dict[str, list[str]] = {}
    for api, refs in raw["apis"].items():
        ids = []
        seen = set()
        for ref in refs:
            bcs_id = ref.get("bcsId")
            if bcs_id and bcs_id not in seen:
                seen.add(bcs_id)
                ids.append(bcs_id)
        api_bcs[api] = ids
    return api_bcs


def scan_script(content: str, api_whitelist: set[str]) -> dict[str, list[int]]:
    """Return API names and line numbers for every whitelisted reference."""
    hits: dict[str, list[int]] = defaultdict(list)
    for line_number, line in enumerate(content.splitlines(), 1):
        seen_in_line: set[str] = set()
        for match in IDENT_RE.finditer(line):
            name = match.group(1)
            if name in api_whitelist and name not in seen_in_line:
                seen_in_line.add(name)
                hits[name].append(line_number)
    return dict(hits)


def scan_binding_declarations(content: str) -> dict[str, list[str]]:
    """Return _cpp binding names and their declared receiver classes."""
    bindings: dict[str, set[str]] = defaultdict(set)
    receiver_class: str | None = None
    for line in content.splitlines():
        if line.startswith("L0_1 = "):
            candidate = line[len("L0_1 = ") :]
            if (
                candidate.isascii()
                and candidate[:1].isalpha()
                and candidate.isidentifier()
            ):
                receiver_class = candidate
            else:
                receiver_class = None
        if receiver_class is None or '_cpp"' not in line:
            continue
        for binding in re.findall(r'"(_[A-Za-z0-9]+)_cpp"', line):
            bindings[binding].add(receiver_class)
    return {name: sorted(classes) for name, classes in bindings.items()}


def annotate_corpus(
    scripts_root: Path,
    registry_path: Path,
    api_index_path: Path,
    index_out: Path,
    sidecars_root: Path | None = None,
) -> int:
    """Regenerate N-API sidecars and the inverted index.

    ``scripts_root`` is read-only input when ``sidecars_root`` is supplied;
    this keeps generated sidecars in the tracked repository tree while a
    hydrated corpus can live elsewhere.
    """
    try:
        validate_scripts_root(scripts_root)
    except CorpusRootError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not registry_path.is_file():
        print(
            f"error: {registry_path} not found - run lua_corpus.py publish first",
            file=sys.stderr,
        )
        return 1
    if not api_index_path.is_file():
        print(f"error: {api_index_path} not found", file=sys.stderr)
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    api_bcs = load_api_index(api_index_path)
    whitelist = set(api_bcs)
    inverted: dict[str, list[dict]] = defaultdict(list)
    binding_declarations: dict[str, set[tuple[str, str]]] = defaultdict(set)
    script_count = scripts_with_calls = 0
    sidecars_root = scripts_root if sidecars_root is None else sidecars_root
    for lua_path, decoded in iter_lua(scripts_root):
        registry_entry = registry["scripts"].get(decoded, {})
        content = lua_path.read_text(encoding="utf-8")
        hits = scan_script(content, whitelist)
        for api, classes in scan_binding_declarations(content).items():
            if api in whitelist:
                for receiver_class in classes:
                    binding_declarations[api].add((receiver_class, decoded))
        script_count += 1
        sidecar = {
            "decoded": decoded,
            "ciphered": registry_entry.get("ciphered", ""),
            "classes": registry_entry.get("classes", []),
            "lineCount": registry_entry.get("lineCount", line_count(content)),
            "apiCount": len(hits),
            "callsiteCount": sum(len(lines) for lines in hits.values()),
            "apis": {key: hits[key] for key in sorted(hits)},
        }
        sidecar_path = (
            sidecars_root / lua_path.relative_to(scripts_root)
        ).with_suffix(".calls.json")
        write_json(sidecar_path, sidecar)
        if hits:
            scripts_with_calls += 1
            for api, lines in hits.items():
                for line_number in lines:
                    inverted[api].append({"script": decoded, "line": line_number})

    napi_index = {
        "version": "2",
        "gameVersion": "1.23b",
        "extraction": EXTRACTION_VERSION,
        "source": (
            "lua/scripts/ cross-referenced against "
            "data/vendor/client-structs/lua_api_index.json "
            "(see data/vendor/client-structs/PROVENANCE.json "
            "for source identity)"
        ),
        "apiCount": len(inverted),
        "totalCallsites": sum(len(lines) for lines in inverted.values()),
        "apis": {},
    }
    for api in sorted(inverted):
        sites = sorted(inverted[api], key=lambda site: (site["script"], site["line"]))
        napi_index["apis"][api] = {
            "bcsIds": api_bcs.get(api, []),
            "bindings": [
                {"class": receiver_class, "script": script}
                for receiver_class, script in sorted(binding_declarations.get(api, set()))
            ],
            "callsiteCount": len(sites),
            "callsites": sites,
        }
    write_json(index_out, napi_index)

    print(
        f"annotated {script_count} scripts ({scripts_with_calls} with N-API "
        f"references); wrote {napi_index['apiCount']} unique APIs across "
        f"{napi_index['totalCallsites']} callsites to {index_out}"
    )
    return 0
