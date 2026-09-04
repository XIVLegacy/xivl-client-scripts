"""Package and verify the local, private Lua source corpus.

The tracked reproduction manifest is the only source of file identities.  The
archive format intentionally contains only the bytes under ``lua/scripts``;
sidecars and other repository metadata are not package members.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence


_MANIFEST_PREFIX = "lua/scripts/"
_LUA_SUFFIX = ".lua"
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)


class CorpusError(ValueError):
    """A package, manifest, source tree, or destination failed validation."""


@dataclass(frozen=True)
class FileIdentity:
    """The per-file identity needed by every corpus operation."""

    relative_path: str
    member_path: str
    size: int
    sha256: str


@dataclass(frozen=True)
class CorpusSummary:
    """Stable, non-sensitive summary returned by package operations."""

    file_count: int
    total_bytes: int
    tree_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "fileCount": self.file_count,
            "totalBytes": self.total_bytes,
            "treeSha256": self.tree_sha256,
        }


def _error(message: str) -> CorpusError:
    return CorpusError(message)


def _is_link_or_reparse(path: Path, st: os.stat_result | None = None) -> bool:
    """Return whether *path* is a symlink or Windows reparse point."""
    if st is None:
        st = os.lstat(path)
    return path.is_symlink() or bool(getattr(st, "st_file_attributes", 0) & _REPARSE_POINT)


def _lstat(path: Path, label: str) -> os.stat_result:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        raise _error(f"{label}: missing: {path}") from None
    except OSError as exc:
        raise _error(f"{label}: cannot inspect {path}: {exc}") from exc
    if _is_link_or_reparse(path, st):
        raise _error(f"{label}: link or reparse point is not allowed: {path}")
    return st


def _check_safe_member_path(name: object, *, where: str) -> str:
    if not isinstance(name, str):
        raise _error(f"{where}: member path is not a string")
    if not name:
        raise _error(f"{where}: empty member path")
    if not name.isascii():
        raise _error(f"{where}: non-ASCII member path: {name!r}")
    if "\\" in name:
        raise _error(f"{where}: backslash in member path: {name!r}")
    if ":" in name:
        raise _error(f"{where}: drive or colon in member path: {name!r}")
    if name.startswith("/"):
        raise _error(f"{where}: absolute member path: {name!r}")
    if any(ord(char) < 0x20 or ord(char) == 0x7F for char in name):
        raise _error(f"{where}: control character in member path: {name!r}")

    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise _error(f"{where}: traversal or empty component in member path: {name!r}")
    if PurePosixPath(name).is_absolute():
        raise _error(f"{where}: absolute member path: {name!r}")
    if not name.endswith(_LUA_SUFFIX):
        raise _error(f"{where}: non-Lua member: {name!r}")
    return name


def _manifest_identities(manifest: Mapping[str, object]) -> tuple[FileIdentity, ...]:
    rows = manifest.get("scripts")
    if not isinstance(rows, list):
        raise _error("manifest: scripts must be a list")

    identities: list[FileIdentity] = []
    exact: set[str] = set()
    folded: dict[str, str] = {}
    total_bytes = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise _error(f"manifest scripts[{index}]: row is not an object")
        relative = row.get("relativePath")
        if not isinstance(relative, str):
            raise _error(f"manifest scripts[{index}]: relativePath is not a string")
        if not relative.startswith(_MANIFEST_PREFIX):
            raise _error(
                f"manifest scripts[{index}]: path must start with {_MANIFEST_PREFIX!r}: {relative!r}"
            )
        member = _check_safe_member_path(
            relative[len(_MANIFEST_PREFIX) :],
            where=f"manifest scripts[{index}]",
        )
        if not relative.endswith(_LUA_SUFFIX):
            raise _error(f"manifest scripts[{index}]: path is not a Lua file: {relative!r}")
        if relative in exact:
            raise _error(f"manifest: duplicate path: {relative}")
        exact.add(relative)
        folded_key = member.casefold()
        previous = folded.get(folded_key)
        if previous is not None:
            raise _error(f"manifest: case-fold collision: {previous} and {member}")
        folded[folded_key] = member

        size = row.get("bytes")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise _error(f"manifest {relative}: bytes must be a non-negative integer")
        digest = row.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            raise _error(f"manifest {relative}: sha256 must be 64 hexadecimal characters")
        try:
            int(digest, 16)
        except ValueError:
            raise _error(f"manifest {relative}: sha256 is not hexadecimal") from None
        identities.append(FileIdentity(relative, member, size, digest.lower()))
        total_bytes += size

    script_count = manifest.get("scriptCount")
    if script_count is not None:
        if isinstance(script_count, bool) or not isinstance(script_count, int):
            raise _error("manifest: scriptCount must be an integer")
        if script_count != len(identities):
            raise _error(f"manifest: scriptCount {script_count!r} != {len(identities)} rows")
    manifest_bytes = manifest.get("totalBytes")
    if manifest_bytes is not None:
        if isinstance(manifest_bytes, bool) or not isinstance(manifest_bytes, int):
            raise _error("manifest: totalBytes must be an integer")
        if manifest_bytes != total_bytes:
            raise _error(f"manifest: totalBytes {manifest_bytes!r} != {total_bytes} row bytes")
    if [item.member_path for item in identities] != sorted(item.member_path for item in identities):
        raise _error("manifest: scripts are not sorted by relativePath")
    return tuple(identities)


def load_manifest(path: Path | str) -> tuple[FileIdentity, ...]:
    """Load and validate the manifest's per-file identities."""
    manifest_path = Path(path)
    _lstat(manifest_path, "manifest")
    try:
        with manifest_path.open("r", encoding="utf-8") as stream:
            document = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _error(f"manifest: cannot read {manifest_path}: {exc}") from exc
    if not isinstance(document, dict):
        raise _error("manifest: top-level value must be an object")
    return _manifest_identities(document)


def _tree_sha256(records: Iterable[tuple[str, int, str]]) -> str:
    """Hash sorted path/size/content-digest records with explicit framing."""
    digest = hashlib.sha256()
    for path, size, content_digest in sorted(records, key=lambda item: item[0]):
        path_bytes = path.encode("ascii")
        digest.update(len(path_bytes).to_bytes(4, "big"))
        digest.update(path_bytes)
        digest.update(size.to_bytes(8, "big"))
        digest.update(bytes.fromhex(content_digest))
    return digest.hexdigest()


def tree_sha256(records: Iterable[tuple[str, int, str]]) -> str:
    """Return the stable tree digest for ``(member, size, sha256)`` records."""
    return _tree_sha256(records)


def _summary(records: Sequence[tuple[str, int, str]]) -> CorpusSummary:
    return CorpusSummary(
        file_count=len(records),
        total_bytes=sum(item[1] for item in records),
        tree_sha256=_tree_sha256(records),
    )


def _walk_source_lua(source_root: Path) -> dict[str, Path]:
    root_st = _lstat(source_root, "source root")
    if not stat.S_ISDIR(root_st.st_mode):
        raise _error(f"source root is not a directory: {source_root}")
    found: dict[str, Path] = {}
    folded: dict[str, str] = {}
    for current, directories, files in os.walk(source_root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(directories):
            path = current_path / name
            st = _lstat(path, "source tree")
            if not stat.S_ISDIR(st.st_mode):
                raise _error(f"source tree: non-directory path: {path}")
            kept_dirs.append(name)
        directories[:] = kept_dirs
        for name in sorted(files):
            path = current_path / name
            st = _lstat(path, "source tree")
            if not stat.S_ISREG(st.st_mode):
                raise _error(f"source tree: non-file path: {path}")
            if not name.endswith(_LUA_SUFFIX):
                continue
            relative = path.relative_to(source_root).as_posix()
            member = _check_safe_member_path(relative, where="source tree")
            if member in found:
                raise _error(f"source tree: duplicate path: {member}")
            folded_key = member.casefold()
            previous = folded.get(folded_key)
            if previous is not None:
                raise _error(f"source tree: case-fold collision: {previous} and {member}")
            folded[folded_key] = member
            found[member] = path
    return found


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _ensure_output_safe(source_root: Path, output_path: Path) -> None:
    source = _resolved(source_root)
    output = _resolved(output_path)
    if output == source or source in output.parents:
        raise _error("package output must be outside (and above) the source root")
    if output_path.exists() or output_path.is_symlink():
        output_st = _lstat(output_path, "package output")
        if output_path.is_dir():
            raise _error(f"package output is a directory: {output_path}")
        if not stat.S_ISREG(output_st.st_mode):
            raise _error(f"package output is not a regular file: {output_path}")
    parent = output_path.parent
    parent_st = _lstat(parent, "package output parent")
    if not stat.S_ISDIR(parent_st.st_mode):
        raise _error(f"package output parent is not a directory: {parent}")


def _read_source(
    source_root: Path, identities: Sequence[FileIdentity]
) -> tuple[list[tuple[str, bytes]], CorpusSummary]:
    found = _walk_source_lua(source_root)
    expected = {item.member_path: item for item in identities}
    unexpected = sorted(set(found) - set(expected))
    missing = sorted(set(expected) - set(found))
    if missing:
        raise _error(f"source tree: missing member(s): {', '.join(missing)}")
    if unexpected:
        raise _error(f"source tree: unexpected member(s): {', '.join(unexpected)}")

    payloads: list[tuple[str, bytes]] = []
    records: list[tuple[str, int, str]] = []
    for item in identities:
        path = found[item.member_path]
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise _error(f"source tree: cannot read {item.member_path}: {exc}") from exc
        actual_digest = hashlib.sha256(data).hexdigest()
        if len(data) != item.size:
            raise _error(
                f"source tree: size mismatch for {item.member_path}: {len(data)} != {item.size}"
            )
        if actual_digest != item.sha256:
            raise _error(f"source tree: sha256 mismatch for {item.member_path}")
        payloads.append((item.member_path, data))
        records.append((item.member_path, len(data), actual_digest))
    return payloads, _summary(records)


def _zip_info_is_nonfile(info: zipfile.ZipInfo) -> bool:
    if info.is_dir() or info.filename.endswith("/"):
        return True
    mode = (info.external_attr >> 16) & 0xFFFF
    file_type = stat.S_IFMT(mode)
    if file_type in {stat.S_IFLNK, stat.S_IFDIR}:
        return True
    if file_type and file_type != stat.S_IFREG:
        return True
    # For DOS-created archives, bit 4 is the directory attribute.
    if info.create_system == 0 and (info.external_attr & 0x10):
        return True
    return False


def _read_verified_zip(package_path: Path, identities: Sequence[FileIdentity]) -> tuple[list[tuple[str, bytes]], CorpusSummary]:
    _lstat(package_path, "package")
    package_st = os.stat(package_path)
    if not stat.S_ISREG(package_st.st_mode):
        raise _error(f"package is not a file: {package_path}")
    expected = {item.member_path: item for item in identities}
    try:
        archive = zipfile.ZipFile(package_path, "r")
    except (OSError, zipfile.BadZipFile) as exc:
        raise _error(f"package: cannot open ZIP {package_path}: {exc}") from exc
    with archive:
        infos = archive.infolist()
        seen: set[str] = set()
        folded: dict[str, str] = {}
        payloads: list[tuple[str, bytes]] = []
        records: list[tuple[str, int, str]] = []
        member_order: list[str] = []
        for info in infos:
            member = _check_safe_member_path(info.filename, where="package")
            member_order.append(member)
            if _zip_info_is_nonfile(info):
                raise _error(f"package: non-file member: {member}")
            if member in seen:
                raise _error(f"package: duplicate member: {member}")
            seen.add(member)
            folded_key = member.casefold()
            previous = folded.get(folded_key)
            if previous is not None:
                raise _error(f"package: case-fold collision: {previous} and {member}")
            folded[folded_key] = member
            if member not in expected:
                raise _error(f"package: unexpected member: {member}")
            item = expected[member]
            if info.file_size != item.size:
                raise _error(
                    f"package: size mismatch for {member}: "
                    f"{info.file_size} != {item.size}"
                )
            try:
                data = archive.read(info)
            except (OSError, RuntimeError, ValueError, zipfile.BadZipFile) as exc:
                raise _error(f"package: cannot read member {member}: {exc}") from exc
            actual_digest = hashlib.sha256(data).hexdigest()
            if len(data) != item.size:
                raise _error(
                    f"package: size mismatch for {member}: {len(data)} != {item.size}"
                )
            if actual_digest != item.sha256:
                raise _error(f"package: sha256 mismatch for {member}")
            payloads.append((member, data))
            records.append((member, len(data), actual_digest))
        missing = sorted(set(expected) - seen)
        if missing:
            raise _error(f"package: missing member(s): {', '.join(missing)}")
        if len(payloads) != len(identities):
            raise _error(f"package: file count mismatch: {len(payloads)} != {len(identities)}")
        if member_order != sorted(member_order):
            raise _error("package: members are not sorted by POSIX path")
    return payloads, _summary(records)


def package_corpus(
    source_root: Path | str,
    output_path: Path | str,
    manifest_path: Path | str,
) -> CorpusSummary:
    """Verify and write a deterministic ZIP package outside ``source_root``."""
    source = Path(source_root)
    output = Path(output_path)
    _ensure_output_safe(source, output)
    identities = load_manifest(manifest_path)
    payloads, summary = _read_source(source, identities)
    temp_path: Path | None = None
    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
        )
        os.close(fd)
        temp_path = Path(temp_name)
        with zipfile.ZipFile(
            temp_path,
            mode="w",
            compression=zipfile.ZIP_STORED,
            allowZip64=True,
        ) as archive:
            archive.comment = b""
            for member, data in payloads:
                source_path = source.joinpath(*member.split("/"))
                source_st = _lstat(source_path, "source tree")
                if not stat.S_ISREG(source_st.st_mode):
                    raise _error(f"source tree: non-file path: {source_path}")
                if source_path.read_bytes() != data:
                    raise _error(f"source tree: changed during packaging: {member}")
                info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = 0
                info.create_version = 20
                info.extract_version = 20
                info.flag_bits = 0
                info.external_attr = 0
                info.internal_attr = 0
                info.extra = b""
                info.comment = b""
                archive.writestr(info, data)
        try:
            final_payloads, final_summary = _read_source(source, identities)
        except CorpusError as exc:
            raise _error("source tree: changed during packaging") from exc
        if final_payloads != payloads or final_summary != summary:
            raise _error("source tree: changed during packaging")
        os.replace(temp_path, output)
        temp_path = None
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass
    return summary


def verify_package(
    package_path: Path | str,
    manifest_path: Path | str,
) -> CorpusSummary:
    """Read and verify every ZIP member against the tracked manifest."""
    identities = load_manifest(manifest_path)
    _, summary = _read_verified_zip(Path(package_path), identities)
    return summary


def _ensure_destination(destination: Path) -> tuple[bool, Path]:
    """Validate an explicit absent/empty destination and return its parent."""
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        st = _lstat(destination, "hydration destination")
        if not stat.S_ISDIR(st.st_mode):
            raise _error(f"hydration destination is not a directory: {destination}")
        try:
            nonempty = next(destination.iterdir(), None) is not None
        except OSError as exc:
            raise _error(f"hydration destination cannot be read: {exc}") from exc
        if nonempty:
            raise _error(f"hydration destination must be absent or empty: {destination}")
        exists = True
    else:
        exists = False
    parent = destination.parent
    parent_st = _lstat(parent, "hydration destination parent")
    if not stat.S_ISDIR(parent_st.st_mode):
        raise _error(f"hydration destination parent is not a directory: {parent}")
    return exists, parent


def _verify_hydrated_tree(root: Path, identities: Sequence[FileIdentity]) -> CorpusSummary:
    found: dict[str, Path] = {}
    root_st = _lstat(root, "hydration staging")
    if not stat.S_ISDIR(root_st.st_mode):
        raise _error(f"hydration staging is not a directory: {root}")
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories):
            path = current_path / name
            st = _lstat(path, "hydration staging")
            if not stat.S_ISDIR(st.st_mode):
                raise _error(f"hydration staging: non-directory path: {path}")
        for name in sorted(files):
            path = current_path / name
            st = _lstat(path, "hydration staging")
            if not stat.S_ISREG(st.st_mode):
                raise _error(f"hydration staging: non-file path: {path}")
            member = _check_safe_member_path(
                path.relative_to(root).as_posix(), where="hydration staging"
            )
            if member in found:
                raise _error(f"hydration staging: duplicate path: {member}")
            found[member] = path
    expected = {item.member_path: item for item in identities}
    missing = sorted(set(expected) - set(found))
    unexpected = sorted(set(found) - set(expected))
    if missing:
        raise _error(f"hydration staging: missing member(s): {', '.join(missing)}")
    if unexpected:
        raise _error(f"hydration staging: unexpected member(s): {', '.join(unexpected)}")
    records: list[tuple[str, int, str]] = []
    for item in identities:
        data = found[item.member_path].read_bytes()
        actual_digest = hashlib.sha256(data).hexdigest()
        if len(data) != item.size or actual_digest != item.sha256:
            raise _error(f"hydration staging: identity mismatch for {item.member_path}")
        records.append((item.member_path, len(data), actual_digest))
    return _summary(records)


def _unused_path(parent: Path, prefix: str) -> Path:
    fd, name = tempfile.mkstemp(prefix=prefix, dir=parent)
    os.close(fd)
    path = Path(name)
    path.unlink()
    return path


def hydrate_package(
    package_path: Path | str,
    destination: Path | str,
    manifest_path: Path | str,
) -> CorpusSummary:
    """Verify a package, then atomically publish it into an explicit directory."""
    identities = load_manifest(manifest_path)
    payloads, summary = _read_verified_zip(Path(package_path), identities)
    destination_path = Path(destination)
    existed, parent = _ensure_destination(destination_path)
    stage = Path(tempfile.mkdtemp(prefix=".private-lua-corpus-", dir=parent))
    backup: Path | None = None
    published = False
    try:
        for member, data in payloads:
            target = stage.joinpath(*member.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
        staged_summary = _verify_hydrated_tree(stage, identities)
        if staged_summary != summary:
            raise _error("hydration staging: summary changed before publication")

        current_exists, _ = _ensure_destination(destination_path)
        if current_exists != existed:
            raise _error("hydration destination changed before publication")

        if existed:
            backup = _unused_path(parent, ".private-lua-corpus-backup-")
            os.replace(destination_path, backup)
            if next(backup.iterdir(), None) is not None:
                os.replace(backup, destination_path)
                backup = None
                raise _error("hydration destination changed before publication")
            try:
                os.replace(stage, destination_path)
                published = True
            except BaseException:
                try:
                    os.replace(backup, destination_path)
                    backup = None
                except BaseException as rollback_exc:
                    raise _error(f"hydration publish failed and rollback failed: {rollback_exc}") from rollback_exc
                raise
        else:
            os.replace(stage, destination_path)
            published = True
    finally:
        if not published:
            if stage.exists():
                shutil.rmtree(stage)
        if backup is not None and backup.exists():
            shutil.rmtree(backup)
    return summary


def _default_manifest() -> Path:
    return Path(__file__).resolve().parents[1] / "manifests" / "scripts.json"


def _default_source() -> Path:
    return Path(__file__).resolve().parents[1] / "lua" / "scripts"


def _add_manifest_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--manifest",
        type=Path,
        default=_default_manifest(),
        help="tracked manifests/scripts.json (default: repository manifest)",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    package_parser = commands.add_parser("package")
    package_parser.add_argument("--source-root", type=Path, default=_default_source())
    package_parser.add_argument("--output", type=Path, required=True)
    _add_manifest_option(package_parser)

    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("--package", type=Path, required=True)
    _add_manifest_option(verify_parser)

    hydrate_parser = commands.add_parser("hydrate")
    hydrate_parser.add_argument("--package", type=Path, required=True)
    hydrate_parser.add_argument("--destination", type=Path, required=True)
    _add_manifest_option(hydrate_parser)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "package":
            summary = package_corpus(args.source_root, args.output, args.manifest)
        elif args.command == "verify":
            summary = verify_package(args.package, args.manifest)
        else:
            summary = hydrate_package(args.package, args.destination, args.manifest)
    except (CorpusError, OSError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary.as_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
