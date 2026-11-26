"""Tests for scripts/release_notes.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import release_notes  # noqa: E402

CHANGELOG = """# Changelog

## [Unreleased]

## [0.2.4] - 2026-11-26

### Added
- New thing.

### Changed
- Other thing.

## [0.2.3] - 2026-11-20

### Fixed
- Old fix.

## [0.2.2] - 2026-11-10

[0.2.4]: https://example.com/compare/v0.2.3...v0.2.4
"""


class ChangelogSectionTest(unittest.TestCase):
    def test_returns_only_the_requested_section(self) -> None:
        notes = release_notes.changelog_section(CHANGELOG, "0.2.4")
        self.assertIn("- New thing.", notes)
        self.assertIn("### Changed", notes)
        self.assertNotIn("Old fix", notes)

    def test_accepts_tag_prefix(self) -> None:
        self.assertEqual(
            release_notes.changelog_section(CHANGELOG, "v0.2.3"),
            "### Fixed\n- Old fix.",
        )

    def test_missing_or_empty_section(self) -> None:
        self.assertIsNone(release_notes.changelog_section(CHANGELOG, "9.9.9"))
        self.assertIsNone(release_notes.changelog_section(CHANGELOG, "Unreleased"))
        self.assertIsNone(release_notes.changelog_section(CHANGELOG, "0.2.2"))

    def test_version_dots_are_literal(self) -> None:
        self.assertIsNone(release_notes.changelog_section(CHANGELOG, "0x2x4"))


class RepositoryReleaseTest(unittest.TestCase):
    def test_current_version_has_changelog_section(self) -> None:
        version = release_notes.project_version()
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIsNotNone(
            release_notes.changelog_section(changelog, version),
            f"add a '## [{version}]' section to CHANGELOG.md",
        )


if __name__ == "__main__":
    unittest.main()
