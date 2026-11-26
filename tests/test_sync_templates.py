"""Tests for scripts/sync_templates.py using a fake vaultia-templates checkout."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import sync_templates  # noqa: E402

BUNDLES = {"requirements/kit": "skills/demo/assets/kit"}


def make_source(root: Path, files: dict[str, str], schema: int = 1) -> Path:
    source = root / "templates"
    for rel, text in files.items():
        path = source / "src" / "requirements" / "kit" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    manifest = {"schema": schema, "templates": {"requirements/kit": {"description": "d", "used_by": ["demo"], "files": list(files)}}}
    (source / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return source


class SyncTemplatesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.dest = self.root / "repo"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_adds_updates_and_removes(self) -> None:
        source = make_source(self.root, {"README.md": "new", "a/b.md": "b"})
        kit = self.dest / "skills/demo/assets/kit"
        (kit / "old").mkdir(parents=True)
        (kit / "README.md").write_text("old", encoding="utf-8")
        (kit / "old" / "gone.md").write_text("x", encoding="utf-8")

        changes = sync_templates.plan(source, self.dest, BUNDLES)
        self.assertEqual(sorted(a for a, _, _ in changes), ["add", "remove", "update"])

        sync_templates.apply(changes)
        self.assertEqual((kit / "README.md").read_text(encoding="utf-8"), "new")
        self.assertTrue((kit / "a/b.md").is_file())
        self.assertFalse((kit / "old").exists(), "empty folders are removed")
        self.assertEqual(sync_templates.plan(source, self.dest, BUNDLES), [])

    def test_rejects_unknown_schema(self) -> None:
        source = make_source(self.root, {"README.md": "x"}, schema=99)
        with self.assertRaises(ValueError):
            sync_templates.plan(source, self.dest, BUNDLES)

    def test_rejects_missing_template(self) -> None:
        source = make_source(self.root, {"README.md": "x"})
        with self.assertRaises(ValueError):
            sync_templates.plan(source, self.dest, {"requirements/other": "x"})

    def test_bundles_point_at_existing_skill_assets(self) -> None:
        for template_id, rel in sync_templates.BUNDLES.items():
            with self.subTest(template=template_id):
                self.assertTrue((REPO_ROOT / rel).is_dir(), f"{rel} does not exist")


if __name__ == "__main__":
    unittest.main()
