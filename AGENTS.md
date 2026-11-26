# Agent Instructions

This repository contains reusable Agent Skills. Guidance for any AI agent working **on** this repository:

- Canonical skills live in `skills/<skill-name>/`. Edit only there. Anything under `plugins/` is generated — never hand-edit it.
- Skill names are full, descriptive, lowercase `kebab-case` and must equal the folder name.
- `SKILL.md` frontmatter uses only portable fields (`name`, `description`, and optionally `license`, `compatibility`, `metadata`, `allowed-tools`).
- Keep `SKILL.md` concise; put templates and detailed guidance in `references/` and link them from the workflow step that needs them.
- All skill content is written in English. Documentation is written in English first (`README.md`, `docs/*.md`); translations live in `docs/locales/<lang>/` (Vietnamese: `docs/locales/vi/`) with the same file names, including `README.md`. When you change an English doc, update every translation in the same change.
- Generated (never hand-edit): `plugins/`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `dist/`. Regenerate with `python3 scripts/build_plugins.py`.
- After any change, run:
  ```bash
  python3 scripts/validate.py
  python3 scripts/build_plugins.py
  python3 -m unittest discover -s tests
  ```
- Scripts use the Python standard library only unless a dependency is explicitly agreed.
- Never commit secrets, credentials, or private product data.
- Follow `docs/skill-authoring.md` when adding or changing a skill.
