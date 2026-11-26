"""Checks for the product-requirements docs starter kit (assets/docs-starter/).

The bundled kit is synced from vaultia-templates (scripts/sync_templates.py).

The kit is copied as-is into a project's docs/ folder, so its files must exist,
follow the naming conventions, and link to each other correctly.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "product-requirements"
STARTER = SKILL / "assets" / "docs-starter"

REQUIRED = [
    "README.md",
    "00-overview/01-introduction.md",
    "00-overview/02-glossary.md",
    "00-overview/03-conventions.md",
    "01-business/01-actors-and-permissions.md",
    "01-business/02-domain-model.md",
    "01-business/03-business-rules.md",
    "01-business/04-workflows.md",
    "02-requirements/01-feature-list.md",
    "02-requirements/02-non-functional-requirements.md",
    "03-functional-specs/_template.md",
    "09-working/open-questions.md",
    "09-working/decisions-log.md",
]
LINK = re.compile(r"\]\(([^)\s]+)\)")
NUMBERED = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*(\.md)?$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")


class StarterKitTest(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        for rel in REQUIRED:
            with self.subTest(file=rel):
                self.assertTrue((STARTER / rel).is_file(), f"missing {rel}")

    def test_no_unexpected_files(self) -> None:
        actual = sorted(str(p.relative_to(STARTER)) for p in STARTER.rglob("*") if p.is_file())
        self.assertEqual(actual, sorted(REQUIRED), "update REQUIRED and docs-structure.md when adding files")

    def test_names_follow_conventions(self) -> None:
        for path in STARTER.rglob("*"):
            rel = path.relative_to(STARTER)
            name = rel.name
            if name in ("README.md", "_template.md"):
                continue
            with self.subTest(path=str(rel)):
                if rel.parts[0] == "09-working" and len(rel.parts) > 1:
                    self.assertRegex(name, KEBAB, "09-working files use kebab-case without a prefix")
                else:
                    self.assertRegex(name, NUMBERED, "use a two-digit prefix and kebab-case")

    def test_local_links_resolve(self) -> None:
        for doc in STARTER.rglob("*.md"):
            text = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
            for target in LINK.findall(text):
                if "://" in target or target.startswith("#") or "<" in target:
                    continue  # external, anchor, or a placeholder filled in by the skill
                with self.subTest(doc=str(doc.relative_to(STARTER)), link=target):
                    self.assertTrue((doc.parent / target.split("#")[0]).exists(), f"broken link: {target}")

    def test_conventions_list_every_shared_id_file(self) -> None:
        conventions = (STARTER / "00-overview" / "03-conventions.md").read_text(encoding="utf-8")
        for prefix, rel in [("BR", "01-business/03-business-rules.md"), ("D", "09-working/decisions-log.md"),
                            ("Q", "09-working/open-questions.md"), ("F", "02-requirements/01-feature-list.md")]:
            with self.subTest(prefix=prefix):
                self.assertIn(f"`{prefix}`", conventions)
                self.assertIn(Path(rel).name, conventions)

    def test_skill_references_the_kit(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        structure = (SKILL / "references" / "docs-structure.md").read_text(encoding="utf-8")
        self.assertIn("assets/docs-starter/", skill)
        self.assertIn("assets/docs-starter/03-functional-specs/_template.md", skill)
        live = "https://raw.githubusercontent.com/vaultia-app/vaultia-templates/main/"
        self.assertIn(live + "manifest.json", structure, "docs-structure.md should fetch the live kit")
        self.assertIn(live + "src/requirements/docs-starter/", structure)
        self.assertIn("`assets/docs-starter/`", structure, "docs-structure.md should name the bundled fallback")
        for rel in REQUIRED:
            if rel.startswith(("01-business/", "02-requirements/01", "09-working/")):
                with self.subTest(file=rel):
                    self.assertIn(rel, structure, "docs-structure.md should say when this shared file is updated")


if __name__ == "__main__":
    unittest.main()
