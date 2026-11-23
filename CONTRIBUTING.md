# Contributing

Thanks for improving Vaultia Skills.

## Workflow

1. Create a branch from `main`.
2. Edit or add a skill under `skills/<skill-name>/` following [docs/skill-authoring.md](docs/skill-authoring.md).
3. Run the checks:
   ```bash
   python3 scripts/validate.py
   python3 scripts/build_plugins.py
   python3 -m unittest discover -s tests
   ```
4. Test the skill by hand in at least one agent (Claude Code, Codex, or Cursor) using the prompts in its `tests/trigger-cases.json`.
5. Update the skill table in `README.md` and add an entry to `CHANGELOG.md`.
6. Open a pull request describing what changed and how you tested it.

## Rules

- One canonical copy per skill; do not create per-platform copies by hand.
- Use full, descriptive `kebab-case` names; avoid unclear abbreviations.
- Write all skill content and docs in English.
- Do not commit secrets, credentials, or private product data.
- Review any executable script and its dependencies before adding it.
