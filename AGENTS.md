# Agent Instructions

This repository contains reusable Agent Skills. Guidance for any AI agent working **on** this repository:

- Canonical skills live in `skills/<skill-name>/`. Edit only there. Anything under `plugins/` is generated — never hand-edit it.
- Skill names are full, descriptive, lowercase `kebab-case` and must equal the folder name.
- `SKILL.md` frontmatter uses only portable fields (`name`, `description`, and optionally `license`, `compatibility`, `metadata`, `allowed-tools`).
- Keep `SKILL.md` concise; put templates and detailed guidance in `references/` and link them from the workflow step that needs them.
- All skill content is written in English. Documentation is written in English first: the root `README.md` and `docs/locales/en-US/*.md`. Translations live in `docs/locales/<lang>/` (Vietnamese: `docs/locales/vi-VN/`) with the same file names, plus their own `README.md`. When you change an English doc, update every translation in the same change.
- Shared document templates (for example the `docs/` starter kit) live in the public `vaultia-templates` repository; skills read them live from `main`. The bundled fallback copies (listed in `BUNDLES` in `scripts/sync_templates.py`) are generated: refresh them with `python3 scripts/sync_templates.py` (or `--source ../vaultia-templates`), never hand-edit them.
- Generated (never hand-edit): `plugins/`, `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `dist/`. Regenerate with `python3 scripts/build_plugins.py`.
- After any change, run:
  ```bash
  python3 scripts/validate.py
  python3 scripts/build_plugins.py
  python3 -m unittest discover -s tests
  ```
- Scripts use the Python standard library only unless a dependency is explicitly agreed.
- Never commit secrets, credentials, or private product data.
- Follow `docs/locales/en-US/skill-authoring.md` when adding or changing a skill.
