#!/usr/bin/env python3
"""Validate canonical skills in skills/<skill-name>/.

Checks, per skill directory:
  * SKILL.md exists and starts with YAML frontmatter delimited by '---'.
  * Frontmatter has a valid `name` (lowercase kebab-case, <= 64 chars,
    equal to the directory name) and a non-empty `description` (<= 1024 chars).
  * Only portable frontmatter keys are used.
  * The Markdown body is not empty (warns when longer than 500 lines).
  * Every referenced local file (`references/...`, `scripts/...`, `assets/...`
    in backticks, and relative Markdown links) exists.
  * Optional tests/trigger-cases.json is well formed.
  * Optional tests/behavior-cases.json is well formed (id, prompt, expect / must_not).

Usage:
  python3 scripts/validate.py              # validate every skill in skills/
  python3 scripts/validate.py skills/foo   # validate specific skill directories

Exit code is 1 when any error is found, 0 otherwise. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_BODY_LINES = 500
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REQUIRED_KEYS = ("name", "description")

# `references/foo.md`, `scripts/bar.py`, `assets/x.png` inside backticks.
BACKTICK_PATH = re.compile(r"`((?:references|scripts|assets)/[^`\s]+)`")
# [text](relative/path.md) — ignores URLs and anchors.
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


@dataclass
class Result:
    skill: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter, body). frontmatter is None when absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return None, text


def parse_frontmatter(block: str) -> dict[str, str]:
    """Parse top-level `key: value` pairs.

    Nested or multi-line values (indented lines, block scalars) are attached to
    the preceding key as raw text; this is enough for the checks performed here
    without requiring PyYAML.
    """
    data: dict[str, str] = {}
    current: str | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t" and current is not None:
            data[current] = (data[current] + " " + raw.strip()).strip()
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw!r}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"|", ">", "|-", ">-"}:
            value = ""
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        if key in data:
            raise ValueError(f"duplicate frontmatter key: {key!r}")
        data[key] = value
        current = key
    return data


def check_links(skill_dir: Path, body: str, result: Result) -> None:
    targets = set(BACKTICK_PATH.findall(body))
    for link in MARKDOWN_LINK.findall(body):
        if "://" in link or link.startswith(("#", "mailto:")):
            continue
        targets.add(link.split("#", 1)[0])
    for target in sorted(t for t in targets if t):
        if not (skill_dir / target).exists():
            result.errors.append(f"referenced file not found: {target}")


def check_trigger_cases(skill_dir: Path, name: str, result: Result) -> None:
    path = skill_dir / "tests" / "trigger-cases.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"tests/trigger-cases.json is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        result.errors.append("tests/trigger-cases.json must be a JSON object")
        return
    if data.get("skill") != name:
        result.errors.append("tests/trigger-cases.json 'skill' must match the skill name")
    for key in ("should_trigger", "should_not_trigger"):
        cases = data.get(key)
        if not isinstance(cases, list) or not cases:
            result.errors.append(f"tests/trigger-cases.json '{key}' must be a non-empty list")
        elif not all(isinstance(c, str) and c.strip() for c in cases):
            result.errors.append(f"tests/trigger-cases.json '{key}' must contain non-empty strings")


def check_behavior_cases(skill_dir: Path, name: str, result: Result) -> None:
    path = skill_dir / "tests" / "behavior-cases.json"
    if not path.exists():
        return
    prefix = "tests/behavior-cases.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"{prefix} is not valid JSON: {exc}")
        return
    if not isinstance(data, dict):
        result.errors.append(f"{prefix} must be a JSON object")
        return
    if data.get("skill") != name:
        result.errors.append(f"{prefix} 'skill' must match the skill name")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        result.errors.append(f"{prefix} 'cases' must be a non-empty list")
        return
    seen: set[str] = set()
    for index, case in enumerate(cases):
        where = f"{prefix} case {index}"
        if not isinstance(case, dict):
            result.errors.append(f"{where} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            result.errors.append(f"{where} needs a non-empty 'id'")
        elif case_id in seen:
            result.errors.append(f"{where} duplicates id {case_id!r}")
        else:
            seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            result.errors.append(f"{where} needs a non-empty 'prompt'")
        for key in ("expect", "must_not"):
            value = case.get(key, [])
            if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
                result.errors.append(f"{where} '{key}' must be a list of non-empty strings")
        if not case.get("expect") and not case.get("must_not"):
            result.errors.append(f"{where} needs at least one 'expect' or 'must_not' entry")


def validate_skill(skill_dir: Path) -> Result:
    skill_dir = skill_dir.resolve()
    result = Result(skill=skill_dir.name)

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        result.errors.append("missing SKILL.md")
        return result

    text = skill_file.read_text(encoding="utf-8")
    block, body = split_frontmatter(text)
    if block is None:
        result.errors.append("SKILL.md must start with frontmatter delimited by '---'")
        return result

    try:
        meta = parse_frontmatter(block)
    except ValueError as exc:
        result.errors.append(str(exc))
        return result

    for key in REQUIRED_KEYS:
        if not meta.get(key):
            result.errors.append(f"frontmatter is missing required field '{key}'")

    unknown = sorted(set(meta) - ALLOWED_KEYS)
    if unknown:
        result.errors.append(
            "non-portable frontmatter keys: " + ", ".join(unknown)
            + f" (allowed: {', '.join(sorted(ALLOWED_KEYS))})"
        )

    name = meta.get("name", "")
    if name:
        if not NAME_PATTERN.match(name):
            result.errors.append(f"name {name!r} must be lowercase kebab-case")
        if len(name) > MAX_NAME_LENGTH:
            result.errors.append(f"name exceeds {MAX_NAME_LENGTH} characters")
        if name != skill_dir.name:
            result.errors.append(f"name {name!r} must match directory name {skill_dir.name!r}")

    description = meta.get("description", "")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        result.errors.append(
            f"description is {len(description)} characters (max {MAX_DESCRIPTION_LENGTH})"
        )
    if "<" in description or ">" in description:
        result.errors.append("description must not contain angle brackets")

    if not body.strip():
        result.errors.append("SKILL.md body is empty")
    elif len(body.splitlines()) > MAX_BODY_LINES:
        result.warnings.append(
            f"SKILL.md body exceeds {MAX_BODY_LINES} lines; move detail into references/"
        )

    check_links(skill_dir, body, result)
    check_trigger_cases(skill_dir, name or skill_dir.name, result)
    check_behavior_cases(skill_dir, name or skill_dir.name, result)
    return result


def discover_skills(root: Path = SKILLS_DIR) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills.")
    parser.add_argument("paths", nargs="*", type=Path, help="skill directories (default: all in skills/)")
    args = parser.parse_args(argv)

    skill_dirs = args.paths or discover_skills()
    if not skill_dirs:
        print("No skills found.", file=sys.stderr)
        return 1

    failed = 0
    for skill_dir in skill_dirs:
        result = validate_skill(skill_dir)
        status = "OK  " if result.ok else "FAIL"
        print(f"[{status}] {result.skill}")
        for message in result.errors:
            print(f"       error:   {message}")
        for message in result.warnings:
            print(f"       warning: {message}")
        failed += not result.ok

    print(f"\n{len(skill_dirs) - failed}/{len(skill_dirs)} skills valid.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
