"""Tests for scripts/validate.py. Run with: python3 -m unittest discover -s tests"""

from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate  # noqa: E402


def make_skill(root: Path, dirname: str, skill_md: str, files: dict[str, str] | None = None) -> Path:
    skill_dir = root / dirname
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(textwrap.dedent(skill_md).lstrip(), encoding="utf-8")
    for rel, content in (files or {}).items():
        path = skill_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return skill_dir


VALID = """
---
name: sample-skill
description: Does a sample thing. Use when testing.
---

# Sample

Read `references/guide.md`.
"""


class RepositorySkillsTest(unittest.TestCase):
    def test_all_repository_skills_are_valid(self) -> None:
        skills = validate.discover_skills()
        self.assertTrue(skills, "expected at least one skill in skills/")
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                result = validate.validate_skill(skill_dir)
                self.assertEqual(result.errors, [])

    def test_core_skills_exist(self) -> None:
        names = {p.name for p in validate.discover_skills()}
        self.assertTrue({"product-requirements", "architecture-requirements"} <= names)


class ValidateSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def errors(self, dirname: str, skill_md: str, files: dict[str, str] | None = None) -> list[str]:
        return validate.validate_skill(make_skill(self.root, dirname, skill_md, files)).errors

    def test_valid_skill(self) -> None:
        self.assertEqual(self.errors("sample-skill", VALID, {"references/guide.md": "x"}), [])

    def test_missing_skill_file(self) -> None:
        (self.root / "empty").mkdir()
        self.assertIn("missing SKILL.md", validate.validate_skill(self.root / "empty").errors)

    def test_missing_frontmatter(self) -> None:
        errors = self.errors("sample-skill", "# No frontmatter\n")
        self.assertTrue(any("frontmatter" in e for e in errors))

    def test_name_must_match_directory(self) -> None:
        errors = self.errors("other-name", VALID, {"references/guide.md": "x"})
        self.assertTrue(any("must match directory" in e for e in errors))

    def test_name_must_be_kebab_case(self) -> None:
        md = VALID.replace("name: sample-skill", "name: Sample_Skill")
        errors = self.errors("Sample_Skill", md, {"references/guide.md": "x"})
        self.assertTrue(any("kebab-case" in e for e in errors))

    def test_missing_description(self) -> None:
        md = VALID.replace("description: Does a sample thing. Use when testing.\n", "")
        errors = self.errors("sample-skill", md, {"references/guide.md": "x"})
        self.assertTrue(any("'description'" in e for e in errors))

    def test_description_too_long(self) -> None:
        md = VALID.replace("Does a sample thing. Use when testing.", "x" * 1100)
        errors = self.errors("sample-skill", md, {"references/guide.md": "x"})
        self.assertTrue(any("max 1024" in e for e in errors))

    def test_non_portable_key(self) -> None:
        md = VALID.replace("---\n\n#", "model: opus\n---\n\n#")
        errors = self.errors("sample-skill", md, {"references/guide.md": "x"})
        self.assertTrue(any("non-portable" in e for e in errors))

    def test_missing_reference(self) -> None:
        errors = self.errors("sample-skill", VALID)
        self.assertIn("referenced file not found: references/guide.md", errors)

    def test_broken_markdown_link(self) -> None:
        md = VALID + "\nSee [details](references/missing.md) and [site](https://example.com).\n"
        errors = self.errors("sample-skill", md, {"references/guide.md": "x"})
        self.assertEqual(errors, ["referenced file not found: references/missing.md"])

    def test_empty_body(self) -> None:
        md = "---\nname: sample-skill\ndescription: Something.\n---\n"
        self.assertIn("SKILL.md body is empty", self.errors("sample-skill", md))

    def test_quoted_and_nested_frontmatter(self) -> None:
        md = VALID.replace(
            "name: sample-skill",
            'name: "sample-skill"\nmetadata:\n  version: "1.0"',
        )
        self.assertEqual(self.errors("sample-skill", md, {"references/guide.md": "x"}), [])

    def test_invalid_trigger_cases(self) -> None:
        cases = json.dumps({"skill": "sample-skill", "should_trigger": [], "should_not_trigger": ["x"]})
        errors = self.errors(
            "sample-skill", VALID, {"references/guide.md": "x", "tests/trigger-cases.json": cases}
        )
        self.assertTrue(any("should_trigger" in e for e in errors))

    def test_main_exit_codes(self) -> None:
        good = make_skill(self.root, "sample-skill", VALID, {"references/guide.md": "x"})
        bad = make_skill(self.root, "broken", "# nothing\n")
        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validate.main([str(good)]), 0)
            self.assertEqual(validate.main([str(good), str(bad)]), 1)


if __name__ == "__main__":
    unittest.main()
