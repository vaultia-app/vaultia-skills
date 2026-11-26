#!/usr/bin/env python3
"""Print the CHANGELOG.md section for one version, for use as GitHub release notes.

Usage:
  python3 scripts/release_notes.py 0.2.4          # prints the "## [0.2.4]" section
  python3 scripts/release_notes.py v0.2.4         # a leading "v" is accepted
  python3 scripts/release_notes.py --check-tag v0.2.4
      # exit 1 unless the tag equals the version in pyproject.toml
      # and CHANGELOG.md has a non-empty section for it

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def project_version(root: Path = REPO_ROOT) -> str:
    match = re.search(r'^version\s*=\s*"([^"]+)"', (root / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit("version not found in pyproject.toml")
    return match.group(1)


def changelog_section(changelog: str, version: str) -> str | None:
    """Return the body under '## [version]' up to the next '## ' heading, or None."""
    version = version.removeprefix("v")
    heading = re.compile(rf"^## \[{re.escape(version)}\][^\n]*\n", re.M)
    match = heading.search(changelog)
    if not match:
        return None
    rest = changelog[match.end():]
    end = re.search(r"^## ", rest, re.M)
    body = rest[: end.start()] if end else rest
    # Drop link reference definitions ("[0.2.4]: https://…") that belong to the footer.
    body = re.sub(r"^\[[^\]]+\]:\s*\S+\s*$", "", body, flags=re.M)
    return body.strip() or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print release notes from CHANGELOG.md.")
    parser.add_argument("version", nargs="?", help="version or tag, e.g. 0.2.4 or v0.2.4")
    parser.add_argument("--check-tag", metavar="TAG", help="verify a tag against pyproject.toml and CHANGELOG.md")
    args = parser.parse_args(argv)

    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    if args.check_tag:
        tag_version = args.check_tag.removeprefix("v")
        version = project_version()
        errors = []
        if tag_version != version:
            errors.append(f"tag {args.check_tag} does not match pyproject.toml version {version}")
        if changelog_section(changelog, tag_version) is None:
            errors.append(f"CHANGELOG.md has no non-empty '## [{tag_version}]' section")
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        if not errors:
            print(f"ok: {args.check_tag} matches pyproject.toml and CHANGELOG.md")
        return 1 if errors else 0

    if not args.version:
        parser.error("give a version, or use --check-tag")
    notes = changelog_section(changelog, args.version)
    if notes is None:
        print(f"error: no '## [{args.version.removeprefix('v')}]' section in CHANGELOG.md", file=sys.stderr)
        return 1
    print(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
