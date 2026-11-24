"""Tests for scripts/build_plugins.py. Run with: python3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_plugins  # noqa: E402
import validate  # noqa: E402

SKILLS = [p.name for p in validate.discover_skills()]
PLUGINS = SKILLS + [build_plugins.BUNDLE_NAME]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BuildPluginsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name)
        build_plugins.build(cls.out, version="9.9.9")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_claude_plugins(self) -> None:
        for name in PLUGINS:
            with self.subTest(plugin=name):
                root = self.out / "plugins" / "claude" / name
                manifest = load(root / ".claude-plugin" / "plugin.json")
                self.assertEqual(manifest["name"], name)
                self.assertEqual(manifest["version"], "9.9.9")
                self.assertTrue(manifest["description"])
                self.assertTrue(manifest["displayName"].strip())
                self.assertTrue((root / manifest["icon"]).is_file())
                self.assertTrue((root / "skills").is_dir())

    def test_openai_plugins(self) -> None:
        for name in PLUGINS:
            with self.subTest(plugin=name):
                root = self.out / "plugins" / "openai" / name
                manifest = load(root / "plugin.json")
                self.assertEqual(manifest["name"], name)
                self.assertEqual(manifest["version"], "9.9.9")
                self.assertIn("com.openai", manifest["extensions"])
                self.assertFalse((root / ".codex-plugin").exists())

    def test_openai_plugins_are_branded(self) -> None:
        for name in PLUGINS:
            with self.subTest(plugin=name):
                root = self.out / "plugins" / "openai" / name
                interface = load(root / "plugin.json")["extensions"]["com.openai"]["interface"]
                for key in ("logo", "composerIcon", "composerIconDark"):
                    self.assertTrue(interface[key].startswith("./assets/brand/"))
                    self.assertTrue((root / interface[key]).is_file(), interface[key])
                self.assertRegex(interface["brandColor"], r"^#[0-9A-Fa-f]{6}$")

    def test_skill_copies_match_canonical_and_exclude_tests(self) -> None:
        for platform in ("claude", "openai"):
            for skill in SKILLS:
                with self.subTest(platform=platform, skill=skill):
                    copy = self.out / "plugins" / platform / skill / "skills" / skill
                    self.assertEqual(
                        (copy / "SKILL.md").read_text(),
                        (validate.SKILLS_DIR / skill / "SKILL.md").read_text(),
                    )
                    self.assertFalse((copy / "tests").exists())
                    self.assertEqual(validate.validate_skill(copy).errors, [])

    def test_bundle_contains_every_skill(self) -> None:
        for platform in ("claude", "openai"):
            skills_dir = self.out / "plugins" / platform / build_plugins.BUNDLE_NAME / "skills"
            self.assertEqual(sorted(p.name for p in skills_dir.iterdir()), sorted(SKILLS))

    def test_claude_marketplace(self) -> None:
        market = load(self.out / ".claude-plugin" / "marketplace.json")
        self.assertEqual(market["name"], build_plugins.MARKETPLACE_NAME)
        self.assertTrue(market["owner"]["name"])
        self.assertEqual([p["name"] for p in market["plugins"]], PLUGINS)
        for entry in market["plugins"]:
            self.assertTrue(entry["source"].startswith("./"))
            self.assertTrue((self.out / entry["source"] / ".claude-plugin" / "plugin.json").is_file())

    def test_openai_marketplace(self) -> None:
        market = load(self.out / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(market["name"], build_plugins.MARKETPLACE_NAME)
        self.assertEqual([p["name"] for p in market["plugins"]], PLUGINS)
        for entry in market["plugins"]:
            self.assertEqual(entry["source"]["source"], "local")
            self.assertTrue((self.out / entry["source"]["path"] / "plugin.json").is_file())
            self.assertIn("installation", entry["policy"])
            self.assertTrue(entry["category"])

    def test_rebuild_removes_stale_plugins(self) -> None:
        stale = self.out / "plugins" / "claude" / "removed-skill"
        stale.mkdir(parents=True)
        build_plugins.build(self.out, version="9.9.9")
        self.assertFalse(stale.exists())


class ZipTest(unittest.TestCase):
    def test_zip_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archives = build_plugins.build_zips(Path(tmp))
            self.assertEqual(sorted(a.stem for a in archives), sorted(SKILLS))
            for archive in archives:
                with zipfile.ZipFile(archive) as zf:
                    names = zf.namelist()
                self.assertIn(f"{archive.stem}/SKILL.md", names)
                self.assertTrue(all(n.startswith(f"{archive.stem}/") for n in names))
                self.assertFalse(any("/tests/" in n for n in names))


class PluginZipTest(unittest.TestCase):
    def test_plugin_zip_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build_plugins.build(out, version="9.9.9")
            archives = build_plugins.build_plugin_zips(out)
            expected = {"vaultia" if n == build_plugins.BUNDLE_NAME else n for n in PLUGINS}
            self.assertEqual({a.stem for a in archives}, expected)
            for archive in archives:
                with zipfile.ZipFile(archive) as zf:
                    names = zf.namelist()
                    manifest = json.loads(zf.read(".codex-plugin/plugin.json"))
                    claude = json.loads(zf.read(".claude-plugin/plugin.json"))
                self.assertIn(manifest["name"], PLUGINS)
                self.assertEqual(manifest["skills"], "./skills/")
                interface = manifest["interface"]
                for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
                    self.assertTrue(interface[key].strip(), key)
                self.assertTrue(interface["defaultPrompt"])
                self.assertNotIn("plugin.json", names)
                self.assertTrue(any(n.startswith("skills/") and n.endswith("/SKILL.md") for n in names))
                logo = manifest["interface"]["logo"].removeprefix("./")
                self.assertIn(logo, names)
                self.assertEqual(claude["name"], manifest["name"])
                self.assertEqual(claude["displayName"], interface["displayName"])
                self.assertIn(claude["icon"].removeprefix("./"), names)


class HelpersTest(unittest.TestCase):
    def test_short_description(self) -> None:
        self.assertEqual(build_plugins.short_description("Do X — and more. Use when Y."), "Do X.")
        self.assertEqual(build_plugins.short_description("Do X. Use when Y."), "Do X.")

    def test_repository_generated_files_are_current(self) -> None:
        self.assertEqual(build_plugins.check(), [], "run: python3 scripts/build_plugins.py")


if __name__ == "__main__":
    unittest.main()
