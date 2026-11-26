#!/usr/bin/env python3
"""Build platform plugins and marketplaces from the canonical skills/.

Generated output (never edit by hand):

  plugins/claude/<plugin>/.claude-plugin/plugin.json   Claude Code plugin
  plugins/claude/<plugin>/skills/<skill>/...
  plugins/openai/<plugin>/plugin.json                  Codex / ChatGPT plugin
  plugins/openai/<plugin>/skills/<skill>/...
  plugins/openai/<plugin>/assets/brand/...             icons from the brand kit
  .claude-plugin/marketplace.json                      Claude Code marketplace
  .agents/plugins/marketplace.json                     Codex / ChatGPT marketplace
  dist/skills/<skill>.zip                              (--zip) skill upload (claude.ai)
  dist/plugins/<display-name>.zip                      (--zip) plugin upload for both ChatGPT / Codex
                                                       and Claude Desktop / claude.ai

One plugin is built per skill, plus a bundle plugin containing every skill.

Usage:
  python3 scripts/build_plugins.py           # regenerate plugins and marketplaces
  python3 scripts/build_plugins.py --zip     # also build dist/skills/*.zip and dist/plugins/*.zip
  python3 scripts/build_plugins.py --check   # fail if generated files are stale

Standard library only.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate  # noqa: E402

MARKETPLACE_NAME = "vaultia-skills"
BUNDLE_NAME = "vaultia-skills"
BUNDLE_DISPLAY_NAME = "Vaultia"
BUNDLE_DESCRIPTION = "All Vaultia skills: product requirements, UI/UX design, and architecture requirements for software teams."
AUTHOR = {"name": "Vaultia"}
OPENAI_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
OPENAI_CATEGORY = "Productivity"
OPENAI_CAPABILITIES = ["Interactive", "Write"]

# Store listing text for OpenAI plugins (ChatGPT requires longDescription).
# shortDescription stays short (~30 characters), like official plugins.
OPENAI_LISTING = {
    "product-requirements": {
        "shortDescription": "Write and review PRDs",
        "longDescription": (
            "Turn a product idea, notes, or a feature request into a clear, testable product "
            "requirements document: goals, target users, user journeys, functional requirements, "
            "acceptance criteria, success metrics, scope, and rollout. Works step by step with you: "
            "proposes options, shows a diagram, and asks one decision at a time before drafting."
        ),
        "defaultPrompt": [
            "Write a PRD for a personal expense tracking app",
            "Turn these meeting notes into requirements with acceptance criteria",
            "Review this PRD and list what is missing",
        ],
    },
    "architecture-requirements": {
        "shortDescription": "Design system architecture",
        "longDescription": (
            "Turn product requirements into an architecture document: drivers, components, APIs, "
            "data models, integrations, security, performance, scalability, reliability, and "
            "architecture decision records (ADRs). Works step by step with you: proposes a design, "
            "shows a diagram, and asks one blocking decision at a time."
        ),
        "defaultPrompt": [
            "Turn this PRD into a technical design",
            "Propose an architecture for a personal expense tracking app",
            "Review this architecture for gaps and risks",
        ],
    },
    "ui-ux-design": {
        "shortDescription": "Design and build UI screens",
        "longDescription": (
            "Turn requirements into screens people can use. Pages are grouped by design intent: "
            "polished, animated landing pages; clear, specific storefronts; and portals focused on "
            "business logic and interaction. Plans screen maps, user flows, every UI state, "
            "accessibility, and brand themes, then builds the screens "
            "in React with a ready-made "
            "Base UI and Tailwind CSS kit of about 60 components, so projects start from a complete "
            "design system instead of from scratch. Also reviews existing UIs for usability problems."
        ),
        "defaultPrompt": [
            "Design the screens for this feature spec",
            "Build a landing page for our app launch",
            "Review this page for usability and accessibility",
        ],
    },
}
OPENAI_LISTING[BUNDLE_NAME] = {
    "shortDescription": "Product, UI, and architecture",
    "longDescription": (
        "Skills for software teams. product-requirements turns an idea into a testable PRD (WHAT and "
        "WHY); ui-ux-design turns it into screens built with a ready-made Base UI React kit; "
        "architecture-requirements turns it into a system design with APIs, data models, "
        "non-functional requirements, and ADRs (HOW and CONSTRAINTS). They work step by step with "
        "you: they propose options, show diagrams, and ask only the decisions that matter."
    ),
    "defaultPrompt": [
        "Write a PRD for a personal expense tracking app",
        "Design the screens for this feature spec",
        "Turn this PRD into a technical design",
    ],
}
KEYWORDS = ["requirements", "product-management", "ui-ux", "design-system", "architecture", "software-design"]

# OpenAI plugin branding: `interface-snippet.json` lists the interface fields
# (logo, composer icons, brand colors); each "./assets/brand/<file>" it names is
# copied from this folder into every OpenAI plugin.
OPENAI_BRAND_DIR = Path("assets") / "vaultia-brand-kit" / "openai"
OPENAI_BRAND_SNIPPET = "interface-snippet.json"
PLUGIN_BRAND_PREFIX = "./assets/brand/"

# Skill content that is not shipped inside plugins or zips.
EXCLUDED_FROM_DISTRIBUTION = ("tests", "__pycache__", ".DS_Store")

GENERATED_PATHS = (
    Path("plugins"),
    Path(".claude-plugin") / "marketplace.json",
    Path(".agents") / "plugins" / "marketplace.json",
)


# ---------------------------------------------------------------- metadata

def project_version(root: Path = REPO_ROOT) -> str:
    match = re.search(r'^version\s*=\s*"([^"]+)"', (root / "pyproject.toml").read_text(), re.M)
    if not match:
        raise SystemExit("version not found in pyproject.toml")
    return match.group(1)


def read_skill(skill_dir: Path) -> dict[str, str]:
    block, _ = validate.split_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    return validate.parse_frontmatter(block or "")


def short_description(description: str) -> str:
    """First clause of a skill description, suitable for a plugin listing."""
    text = re.split(r" — |(?<=\.)\s", description, maxsplit=1)[0].strip().rstrip(".")
    return text + "."


def title_case(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))


# ---------------------------------------------------------------- writers

def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_skill(skill_dir: Path, destination: Path) -> None:
    shutil.copytree(skill_dir, destination, ignore=shutil.ignore_patterns(*EXCLUDED_FROM_DISTRIBUTION))


def claude_manifest(name: str, display_name: str, description: str, version: str,
                    icon: str | None = None) -> dict:
    manifest = {
        "name": name,
        "displayName": display_name,
        "version": version,
        "description": description,
        "author": AUTHOR,
        "keywords": KEYWORDS,
    }
    if icon:
        # Read by Anthropic's plugin directory only; Claude Code ignores it.
        manifest["icon"] = icon
    return manifest


def openai_branding(root: Path = REPO_ROOT) -> tuple[dict, list[Path]]:
    """Return the interface fields and source image files for OpenAI plugins."""
    brand_dir = root / OPENAI_BRAND_DIR
    snippet = brand_dir / OPENAI_BRAND_SNIPPET
    if not snippet.is_file():
        return {}, []
    interface = json.loads(snippet.read_text(encoding="utf-8"))["interface"]
    files = []
    for key, value in interface.items():
        if isinstance(value, str) and value.startswith(PLUGIN_BRAND_PREFIX):
            source = brand_dir / value[len(PLUGIN_BRAND_PREFIX):]
            if not source.is_file():
                raise SystemExit(f"brand file for interface.{key} not found: {source}")
            files.append(source)
    return interface, files


def openai_manifest(name: str, display_name: str, description: str, version: str,
                    branding: dict | None = None) -> dict:
    listing = OPENAI_LISTING.get(name, {})
    return {
        "$schema": OPENAI_PLUGIN_SCHEMA,
        "name": name,
        "version": version,
        "description": description,
        "author": AUTHOR,
        "keywords": KEYWORDS,
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": display_name,
                    "shortDescription": listing.get("shortDescription", description),
                    "longDescription": listing.get("longDescription", description),
                    "developerName": AUTHOR["name"],
                    "category": OPENAI_CATEGORY,
                    "capabilities": OPENAI_CAPABILITIES,
                    "defaultPrompt": listing.get("defaultPrompt", []),
                    "screenshots": [],
                    **(branding or {}),
                }
            }
        },
    }


def plan_plugins(skill_dirs: list[Path]) -> list[dict]:
    """Return plugin specs: one per skill plus the bundle."""
    plugins = []
    for skill_dir in skill_dirs:
        meta = read_skill(skill_dir)
        plugins.append({
            "name": meta["name"],
            "display_name": title_case(meta["name"]),
            "description": short_description(meta["description"]),
            "skills": [skill_dir],
        })
    plugins.append({
        "name": BUNDLE_NAME,
        "display_name": BUNDLE_DISPLAY_NAME,
        "description": BUNDLE_DESCRIPTION,
        "skills": skill_dirs,
    })
    return plugins


def build(out: Path, skills_root: Path = validate.SKILLS_DIR, version: str | None = None,
          brand_root: Path = REPO_ROOT) -> list[dict]:
    """Generate plugins and marketplaces into `out`. Returns the plugin specs."""
    version = version or project_version()
    branding, brand_files = openai_branding(brand_root)
    skill_dirs = validate.discover_skills(skills_root)
    if not skill_dirs:
        raise SystemExit("no skills found")

    failures = [r for r in map(validate.validate_skill, skill_dirs) if not r.ok]
    if failures:
        names = ", ".join(r.skill for r in failures)
        raise SystemExit(f"invalid skills, run scripts/validate.py: {names}")

    plugins_root = out / "plugins"
    for platform in ("claude", "openai"):
        shutil.rmtree(plugins_root / platform, ignore_errors=True)

    plugins = plan_plugins(skill_dirs)
    for spec in plugins:
        name, description = spec["name"], spec["description"]

        claude_dir = plugins_root / "claude" / name
        claude_icon = branding.get("logo")
        write_json(claude_dir / ".claude-plugin" / "plugin.json",
                   claude_manifest(name, spec["display_name"], description, version, claude_icon))
        if claude_icon:
            source = next(f for f in brand_files if f.name == Path(claude_icon).name)
            target = claude_dir / claude_icon
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        openai_dir = plugins_root / "openai" / name
        write_json(openai_dir / "plugin.json",
                   openai_manifest(name, spec["display_name"], description, version, branding))
        for source in brand_files:
            target = openai_dir / "assets" / "brand" / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        for skill_dir in spec["skills"]:
            copy_skill(skill_dir, claude_dir / "skills" / skill_dir.name)
            copy_skill(skill_dir, openai_dir / "skills" / skill_dir.name)

    write_json(out / ".claude-plugin" / "marketplace.json", {
        "name": MARKETPLACE_NAME,
        "description": "Reusable AI Agent Skills for product and architecture requirements.",
        "owner": AUTHOR,
        "metadata": {"version": version},
        "plugins": [
            {
                "name": spec["name"],
                "displayName": spec["display_name"],
                "source": f"./plugins/claude/{spec['name']}",
                "description": spec["description"],
                "version": version,
                "category": "productivity",
                "keywords": KEYWORDS,
            }
            for spec in plugins
        ],
    })

    write_json(out / ".agents" / "plugins" / "marketplace.json", {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": BUNDLE_DISPLAY_NAME},
        "plugins": [
            {
                "name": spec["name"],
                "source": {"source": "local", "path": f"./plugins/openai/{spec['name']}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": OPENAI_CATEGORY,
            }
            for spec in plugins
        ],
    })
    return plugins


def codex_manifest(portable: dict) -> dict:
    """Convert a portable OpenAI manifest to the native `.codex-plugin/plugin.json` shape."""
    manifest = {k: v for k, v in portable.items() if k not in ("$schema", "extensions")}
    manifest["skills"] = "./skills/"
    manifest["interface"] = portable["extensions"]["com.openai"]["interface"]
    return manifest


def plugin_zip_name(portable: dict) -> str:
    """Upload file name from the display name: "Vaultia" -> vaultia, "Product Requirements" -> product-requirements."""
    display = portable["extensions"]["com.openai"]["interface"]["displayName"]
    return re.sub(r"[^a-z0-9]+", "-", display.lower()).strip("-")


def build_plugin_zips(out: Path) -> list[Path]:
    """Zip each plugin once for upload in ChatGPT / Codex and Claude.

    Archive root = plugin root: `.codex-plugin/plugin.json` (ChatGPT / Codex),
    `.claude-plugin/plugin.json` (Claude), and the shared `skills/` and `assets/`.
    Each platform reads only its own manifest folder. Run after build().
    """
    dist = out / "dist" / "plugins"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir(parents=True)
    archives = []
    for plugin_dir in sorted(p for p in (out / "plugins" / "openai").iterdir() if p.is_dir()):
        portable = json.loads((plugin_dir / "plugin.json").read_text(encoding="utf-8"))
        archive = dist / f"{plugin_zip_name(portable)}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(".codex-plugin/plugin.json",
                        json.dumps(codex_manifest(portable), indent=2, ensure_ascii=False) + "\n")
            zf.write(out / "plugins" / "claude" / plugin_dir.name / ".claude-plugin" / "plugin.json",
                     ".claude-plugin/plugin.json")
            for path in sorted(plugin_dir.rglob("*")):
                rel = path.relative_to(plugin_dir)
                if path.is_dir() or rel == Path("plugin.json") or any(
                        part in EXCLUDED_FROM_DISTRIBUTION for part in rel.parts):
                    continue
                zf.write(path, rel)
        archives.append(archive)
    return archives


def build_zips(out: Path, skills_root: Path = validate.SKILLS_DIR) -> list[Path]:
    """Zip each skill as <skill>/SKILL.md ... for upload to claude.ai or ChatGPT."""
    dist = out / "dist" / "skills"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir(parents=True)
    archives = []
    for skill_dir in validate.discover_skills(skills_root):
        archive = dist / f"{skill_dir.name}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(skill_dir.rglob("*")):
                rel = path.relative_to(skill_dir)
                if path.is_dir() or any(part in EXCLUDED_FROM_DISTRIBUTION for part in rel.parts):
                    continue
                zf.write(path, Path(skill_dir.name) / rel)
        archives.append(archive)
    return archives


# ---------------------------------------------------------------- check

def diff_trees(expected: Path, actual: Path) -> list[str]:
    """List relative paths that differ between two files or directory trees."""
    if expected.is_file() or actual.is_file():
        if not (expected.is_file() and actual.is_file()):
            return [str(actual)]
        return [] if filecmp.cmp(expected, actual, shallow=False) else [str(actual)]
    if not actual.is_dir():
        return [str(actual)]
    comparison = filecmp.dircmp(expected, actual, ignore=["__pycache__", ".DS_Store"])
    problems = [str(actual / n) for n in comparison.left_only + comparison.right_only + comparison.funny_files]
    for name in comparison.common_files:
        if not filecmp.cmp(expected / name, actual / name, shallow=False):
            problems.append(str(actual / name))
    for name in comparison.common_dirs:
        problems.extend(diff_trees(expected / name, actual / name))
    return problems


def check(root: Path = REPO_ROOT) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        expected = Path(tmp)
        build(expected, root / "skills", project_version(root), brand_root=root)
        problems: list[str] = []
        for rel in GENERATED_PATHS:
            for platform_dir in ([rel / "claude", rel / "openai"] if rel == Path("plugins") else [rel]):
                problems.extend(
                    str(Path(p).relative_to(expected) if p.startswith(str(expected)) else Path(p).relative_to(root))
                    for p in diff_trees(expected / platform_dir, root / platform_dir)
                )
        return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build plugins and marketplaces from skills/.")
    parser.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    parser.add_argument("--zip", action="store_true", help="also build skill zips and plugin zips under dist/")
    args = parser.parse_args(argv)

    if args.check:
        problems = check()
        if problems:
            print("Generated plugins are out of date. Run: python3 scripts/build_plugins.py")
            for path in problems:
                print(f"  stale: {path}")
            return 1
        print("Generated plugins are up to date.")
        return 0

    plugins = build(REPO_ROOT)
    for spec in plugins:
        skills = ", ".join(p.name for p in spec["skills"])
        print(f"built {spec['name']}  [{skills}]")
    print("wrote .claude-plugin/marketplace.json and .agents/plugins/marketplace.json")
    if args.zip:
        for archive in build_zips(REPO_ROOT) + build_plugin_zips(REPO_ROOT):
            print(f"zipped {archive.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
