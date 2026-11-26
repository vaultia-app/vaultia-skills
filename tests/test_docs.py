"""Checks for repository docs: every locale is complete and local links resolve.

Docs live in docs/locales/<lang>/, one folder per language with the same file
names. English (docs/locales/en/) is the source of truth. The English README.md
stays at the repository root so GitHub shows it; every other locale also has
its own docs/locales/<lang>/README.md.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCALES = REPO_ROOT / "docs" / "locales"
SOURCE = LOCALES / "en"
ROOT_README = REPO_ROOT / "README.md"

# Markdown links [text](target) and HTML href/src/srcset attributes.
LINK = re.compile(r"\]\(([^)\s]+)\)|(?:href|src|srcset)=\"([^\"]+)\"")
LOCALE_NAME = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


def source_docs() -> list[Path]:
    return sorted(SOURCE.glob("*.md"))


def translations() -> list[Path]:
    """Locale folders other than the English source."""
    if not LOCALES.is_dir():
        return []
    return sorted(p for p in LOCALES.iterdir() if p.is_dir() and p != SOURCE)


def expected_names() -> list[str]:
    """File names every translation must have."""
    return ["README.md"] + [p.name for p in source_docs()]


def all_docs() -> list[Path]:
    root_docs = [REPO_ROOT / n for n in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "CHANGELOG.md")]
    localized = [doc for folder in [SOURCE, *translations()] for doc in sorted(folder.glob("*.md"))]
    return [p for p in root_docs if p.exists()] + localized


class LocalesTest(unittest.TestCase):
    def test_english_source_exists(self) -> None:
        self.assertTrue(source_docs(), "expected docs/locales/en/*.md")
        self.assertFalse((SOURCE / "README.md").exists(), "the English README.md belongs at the repository root")
        stray = sorted(p.name for p in (REPO_ROOT / "docs").glob("*.md"))
        self.assertEqual(stray, [], "put docs in docs/locales/<lang>/, not directly in docs/")

    def test_at_least_one_translation(self) -> None:
        self.assertTrue(translations(), "expected docs/locales/<lang>/ besides en")

    def test_locale_folder_names(self) -> None:
        for locale in [SOURCE, *translations()]:
            with self.subTest(locale=locale.name):
                self.assertRegex(locale.name, LOCALE_NAME, "use a language code such as vi or pt-BR")

    def test_every_translation_is_complete(self) -> None:
        for locale in translations():
            for name in expected_names():
                with self.subTest(locale=locale.name, doc=name):
                    self.assertTrue((locale / name).is_file(), f"missing docs/locales/{locale.name}/{name}")

    def test_no_orphan_translation(self) -> None:
        expected = set(expected_names())
        for locale in translations():
            for doc in sorted(locale.glob("*.md")):
                with self.subTest(locale=locale.name, doc=doc.name):
                    self.assertIn(doc.name, expected, "translation has no English source")

    def test_english_docs_link_to_every_translation(self) -> None:
        for locale in translations():
            with self.subTest(doc="README.md", locale=locale.name):
                self.assertIn(f"docs/locales/{locale.name}/README.md", ROOT_README.read_text(encoding="utf-8"),
                              "add the locale to the README language switch")
            for doc in source_docs():
                with self.subTest(doc=doc.name, locale=locale.name):
                    self.assertIn(f"../{locale.name}/{doc.name}", doc.read_text(encoding="utf-8"),
                                  "add the locale to the language switch")


class ReadmeBadgeTest(unittest.TestCase):
    def test_release_badge_matches_project_version(self) -> None:
        pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
        readmes = [ROOT_README] + [locale / "README.md" for locale in translations()]
        for readme in readmes:
            with self.subTest(readme=str(readme.relative_to(REPO_ROOT))):
                self.assertIn(f"/badge/release-v{version}-", readme.read_text(encoding="utf-8"),
                              "update the release badge to the version in pyproject.toml")


class LocalLinksTest(unittest.TestCase):
    def test_local_links_resolve(self) -> None:
        for doc in all_docs():
            text = doc.read_text(encoding="utf-8")
            text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore fenced code
            text = re.sub(r"`[^`\n]*`", "", text)  # ignore inline code
            for match in LINK.finditer(text):
                target = match.group(1) or match.group(2)
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                with self.subTest(doc=str(doc.relative_to(REPO_ROOT)), link=target):
                    self.assertTrue((doc.parent / path).exists(), f"broken link: {target}")


if __name__ == "__main__":
    unittest.main()
