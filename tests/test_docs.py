"""Checks for repository docs: every locale is complete and local links resolve.

English is the source of truth: README.md at the repository root and docs/*.md.
Each translation lives in docs/locales/<lang>/ with the same file names,
including README.md (for example docs/locales/vi/README.md).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
LOCALES = DOCS / "locales"

# Markdown links [text](target) and HTML href/src/srcset attributes.
LINK = re.compile(r"\]\(([^)\s]+)\)|(?:href|src|srcset)=\"([^\"]+)\"")
LOCALE_NAME = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


def source_names() -> list[str]:
    """File names every locale must translate."""
    return ["README.md"] + sorted(p.name for p in DOCS.glob("*.md"))


def locales() -> list[Path]:
    if not LOCALES.is_dir():
        return []
    return sorted(p for p in LOCALES.iterdir() if p.is_dir())


def all_docs() -> list[Path]:
    root_docs = [REPO_ROOT / n for n in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "CHANGELOG.md")]
    translated = [doc for locale in locales() for doc in sorted(locale.glob("*.md"))]
    return [p for p in root_docs if p.exists()] + sorted(DOCS.glob("*.md")) + translated


class LocalesTest(unittest.TestCase):
    def test_at_least_one_locale(self) -> None:
        self.assertTrue(locales(), "expected docs/locales/<lang>/")

    def test_locale_folder_names(self) -> None:
        for locale in locales():
            with self.subTest(locale=locale.name):
                self.assertRegex(locale.name, LOCALE_NAME, "use a language code such as vi or pt-BR")

    def test_every_locale_translates_every_source_doc(self) -> None:
        for locale in locales():
            for name in source_names():
                with self.subTest(locale=locale.name, doc=name):
                    self.assertTrue((locale / name).is_file(), f"missing docs/locales/{locale.name}/{name}")

    def test_no_orphan_translation(self) -> None:
        expected = set(source_names())
        for locale in locales():
            for doc in sorted(locale.glob("*.md")):
                with self.subTest(locale=locale.name, doc=doc.name):
                    self.assertIn(doc.name, expected, "translation has no English source")

    def test_english_docs_link_to_every_locale(self) -> None:
        sources = [REPO_ROOT / "README.md"] + sorted(DOCS.glob("*.md"))
        for doc in sources:
            text = doc.read_text(encoding="utf-8")
            for locale in locales():
                with self.subTest(doc=doc.name, locale=locale.name):
                    self.assertIn(f"locales/{locale.name}/{doc.name}", text, "add the locale to the language switch")


class ReadmeBadgeTest(unittest.TestCase):
    def test_release_badge_matches_project_version(self) -> None:
        pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
        readmes = [REPO_ROOT / "README.md"] + [locale / "README.md" for locale in locales()]
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
