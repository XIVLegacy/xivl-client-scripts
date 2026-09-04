"""Focused mutation tests for private Lua corpus packaging and hydration."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

try:
    from . import private_lua_corpus as corpus
except ImportError:  # Direct ``python tools/test_private_lua_corpus.py``.
    import private_lua_corpus as corpus


class PrivateLuaCorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "lua" / "scripts"
        self.source.mkdir(parents=True)
        self.manifest = self.root / "manifests" / "scripts.json"
        self.manifest.parent.mkdir()
        self.files = {
            "alpha.lua": b"return 'alpha'\n",
            "nested/beta.lua": b"return 'beta'\n",
        }
        for name, data in self.files.items():
            path = self.source / Path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self._write_manifest()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_manifest(self, rows: list[dict[str, object]] | None = None) -> None:
        if rows is None:
            rows = []
            for name in sorted(self.files):
                data = self.files[name]
                rows.append(
                    {
                        "relativePath": f"lua/scripts/{name}",
                        "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest().upper(),
                        "lineCount": len(data.decode("utf-8").splitlines()),
                    }
                )
        document = {
            "version": "1",
            "scriptCount": len(rows),
            "totalBytes": sum(int(row["bytes"]) for row in rows),
            "scripts": rows,
        }
        self.manifest.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    def _package(self, name: str = "corpus.zip") -> Path:
        output = self.root / name
        corpus.package_corpus(self.source, output, self.manifest)
        return output

    def _write_zip(self, output: Path, members: dict[str, bytes]) -> None:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, data in members.items():
                archive.writestr(name, data)

    def test_deterministic_bytes_and_summary(self) -> None:
        first = self._package("first.zip")
        second = self._package("second.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        summary = corpus.verify_package(first, self.manifest)
        self.assertEqual(summary.file_count, 2)
        self.assertEqual(summary.total_bytes, sum(map(len, self.files.values())))
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(archive.namelist(), sorted(self.files))
            self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist()))

    def test_source_overwrite_is_rejected(self) -> None:
        (self.source / "alpha.lua").write_bytes(b"return 'ALPHA'\n")
        with self.assertRaisesRegex(corpus.CorpusError, "mismatch"):
            self._package()

    def test_package_output_inside_source_is_rejected(self) -> None:
        with self.assertRaisesRegex(corpus.CorpusError, "outside"):
            corpus.package_corpus(
                self.source, self.source / "private.zip", self.manifest
            )

    def test_manifest_traversal_is_rejected(self) -> None:
        data = self.files["alpha.lua"]
        self._write_manifest(
            [
                {
                    "relativePath": "lua/scripts/../escape.lua",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            ]
        )
        with self.assertRaisesRegex(corpus.CorpusError, "traversal"):
            corpus.load_manifest(self.manifest)

    def test_manifest_case_fold_collision_is_rejected(self) -> None:
        rows = []
        for name in ("FOO.lua", "foo.lua"):
            rows.append(
                {
                    "relativePath": f"lua/scripts/{name}",
                    "bytes": 1,
                    "sha256": "0" * 64,
                }
            )
        self._write_manifest(rows)
        with self.assertRaisesRegex(corpus.CorpusError, "case-fold collision"):
            corpus.load_manifest(self.manifest)

    def test_archive_corrupt_missing_and_unexpected_members_are_rejected(self) -> None:
        corrupt = self.root / "corrupt.zip"
        self._write_zip(corrupt, {"alpha.lua": b"bad", "nested/beta.lua": self.files["nested/beta.lua"]})
        with self.assertRaisesRegex(corpus.CorpusError, "mismatch"):
            corpus.verify_package(corrupt, self.manifest)

        missing = self.root / "missing.zip"
        self._write_zip(missing, {"alpha.lua": self.files["alpha.lua"]})
        with self.assertRaisesRegex(corpus.CorpusError, "missing member"):
            corpus.verify_package(missing, self.manifest)

        unexpected = self.root / "unexpected.zip"
        self._write_zip(
            unexpected,
            {**self.files, "extra.lua": b"extra\n"},
        )
        with self.assertRaisesRegex(corpus.CorpusError, "unexpected member"):
            corpus.verify_package(unexpected, self.manifest)

    def test_archive_traversal_case_collision_and_directory_are_rejected(self) -> None:
        traversal = self.root / "traversal.zip"
        self._write_zip(traversal, {"../alpha.lua": self.files["alpha.lua"]})
        with self.assertRaisesRegex(corpus.CorpusError, "traversal"):
            corpus.verify_package(traversal, self.manifest)

        case_collision = self.root / "case-collision.zip"
        self._write_zip(
            case_collision,
            {
                "alpha.lua": self.files["alpha.lua"],
                "ALPHA.lua": self.files["alpha.lua"],
                "nested/beta.lua": self.files["nested/beta.lua"],
            },
        )
        with self.assertRaisesRegex(corpus.CorpusError, "case-fold collision"):
            corpus.verify_package(case_collision, self.manifest)

        directory = self.root / "directory.zip"
        with zipfile.ZipFile(directory, "w") as archive:
            archive.writestr("nested/", b"")
        with self.assertRaisesRegex(corpus.CorpusError, "traversal|non-file"):
            corpus.verify_package(directory, self.manifest)

    def test_nonempty_destination_is_rejected_without_writes(self) -> None:
        package = self._package()
        destination = self.root / "destination"
        destination.mkdir()
        sentinel = destination / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(corpus.CorpusError, "absent or empty"):
            corpus.hydrate_package(package, destination, self.manifest)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_empty_and_absent_destination_publish_complete_tree(self) -> None:
        package = self._package()
        for destination in (self.root / "empty", self.root / "absent"):
            if destination.name == "empty":
                destination.mkdir()
            summary = corpus.hydrate_package(package, destination, self.manifest)
            self.assertEqual(summary, corpus.verify_package(package, self.manifest))
            for name, data in self.files.items():
                self.assertEqual((destination / name).read_bytes(), data)

    def test_publish_failure_rolls_back_original_destination(self) -> None:
        package = self._package()
        destination = self.root / "destination"
        destination.mkdir()
        real_replace = os.replace
        calls = 0

        def fail_stage_publish(source: str | os.PathLike[str], target: str | os.PathLike[str]) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected publication failure")
            real_replace(source, target)

        with mock.patch.object(corpus.os, "replace", side_effect=fail_stage_publish):
            with self.assertRaisesRegex(OSError, "injected publication failure"):
                corpus.hydrate_package(package, destination, self.manifest)
        self.assertTrue(destination.is_dir())
        self.assertEqual(list(destination.iterdir()), [])
        self.assertEqual(
            [path.name for path in self.root.iterdir() if path.name.startswith(".private-lua-corpus-")],
            [],
        )


if __name__ == "__main__":
    unittest.main()
