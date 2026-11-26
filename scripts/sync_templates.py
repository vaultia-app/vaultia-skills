#!/usr/bin/env python3
"""Sync the bundled template copies from the vaultia-templates repository.

Skills read their templates live from vaultia-templates@main and fall back to a
copy bundled in the skill. This script refreshes those bundled copies so the
fallback matches main.

  BUNDLES maps a template ID (its path under src/ in vaultia-templates) to the
  folder in this repository that holds its bundled copy.

Usage:
  python3 scripts/sync_templates.py                        # shallow-clone main and sync
  python3 scripts/sync_templates.py --source ../vaultia-templates
  python3 scripts/sync_templates.py --check                # fail if a bundled copy is out of date

Standard library only (uses the git command line to clone).
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_REPO = "https://github.com/vaultia-app/vaultia-templates.git"
SUPPORTED_SCHEMAS = {1}
BUNDLES = {
    "requirements/docs-starter": "skills/product-requirements/assets/docs-starter",
}


def load_manifest(source: Path) -> dict:
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") not in SUPPORTED_SCHEMAS:
        raise ValueError(f"unsupported manifest schema {manifest.get('schema')!r}")
    return manifest


def plan(source: Path, dest_root: Path, bundles: dict[str, str]) -> list[tuple[str, Path, Path | None]]:
    """Return the changes needed: (action, destination, source file or None)."""
    manifest = load_manifest(source)
    changes: list[tuple[str, Path, Path | None]] = []
    for template_id, rel_dest in bundles.items():
        entry = manifest.get("templates", {}).get(template_id)
        if entry is None:
            raise ValueError(f"template {template_id!r} is not in manifest.json")
        src_dir = source / "src" / template_id
        dest_dir = dest_root / rel_dest
        files = entry["files"]
        for rel in files:
            src_file = src_dir / rel
            if not src_file.is_file():
                raise ValueError(f"{template_id}: listed file {rel} is missing in the source")
            dest_file = dest_dir / rel
            if not dest_file.is_file():
                changes.append(("add", dest_file, src_file))
            elif not filecmp.cmp(src_file, dest_file, shallow=False):
                changes.append(("update", dest_file, src_file))
        if dest_dir.is_dir():
            for path in sorted(dest_dir.rglob("*")):
                if path.is_file() and str(path.relative_to(dest_dir)) not in files:
                    changes.append(("remove", path, None))
    return changes


def apply(changes: list[tuple[str, Path, Path | None]]) -> None:
    for action, dest, src in changes:
        if action == "remove":
            dest.unlink()
            parent = dest.parent
            while parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)


def clone_main(target: Path) -> Path:
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", "--branch", "main", TEMPLATES_REPO, str(target)],
        check=True,
    )
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--source", type=Path, help="local vaultia-templates checkout (default: clone main)")
    parser.add_argument("--check", action="store_true", help="only report differences; exit 1 if any")
    args = parser.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        source = args.source.resolve() if args.source else clone_main(Path(tmp) / "vaultia-templates")
        try:
            changes = plan(source, REPO_ROOT, BUNDLES)
        except (OSError, ValueError, KeyError) as exc:
            print(f"ERROR {exc}")
            return 1
        for action, dest, _ in changes:
            print(f"{action:7} {dest.relative_to(REPO_ROOT)}")
        if args.check:
            if changes:
                print("Bundled templates are out of date. Run: python3 scripts/sync_templates.py")
                return 1
            print("Bundled templates match vaultia-templates")
            return 0
        apply(changes)
        print(f"Synced {len(BUNDLES)} template(s), {len(changes)} file change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
