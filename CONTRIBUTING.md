# Contributing

Thanks for improving Vaultia Skills. Bug reports and ideas are welcome in [Issues](https://github.com/vaultia-app/vaultia-skills/issues). For larger changes, such as a new skill, open an issue first so we can agree on the scope.

## Set up

1. **Fork** the repository on GitHub, then clone your fork:
   ```bash
   git clone https://github.com/<your-username>/vaultia-skills.git
   cd vaultia-skills
   git remote add upstream https://github.com/vaultia-app/vaultia-skills.git
   ```
2. Create a branch from the latest `main`:
   ```bash
   git fetch upstream
   git switch -c my-change upstream/main
   ```

Maintainers with write access can skip the fork and branch from `main` directly. Nobody pushes to `main`: every change goes through a pull request with passing CI.

Requires Python 3.10+, no third-party dependencies.

## Make the change

1. Edit or add a skill under `skills/<skill-name>/`, following [the skill authoring guide](docs/locales/en-US/skill-authoring.md). Never edit `plugins/` by hand.
2. Run the checks:
   ```bash
   python3 scripts/validate.py
   python3 scripts/build_plugins.py      # regenerates plugins/, commit the result
   python3 -m unittest discover -s tests
   ```
3. Test the skill by hand in at least one agent (Claude Code, Codex, or Cursor) with the prompts in its `tests/trigger-cases.json` and `tests/behavior-cases.json`.
4. If you added or renamed a skill, update the skill table in `README.md` and each `docs/locales/<lang>/README.md`.
5. Add a line under `## [Unreleased]` in `CHANGELOG.md`.

## Open the pull request

1. Push the branch to your fork: `git push -u origin my-change`.
2. Open a pull request against `vaultia-app/vaultia-skills:main`, describing what changed and how you tested it.
3. CI must pass before merge. If `main` has moved on, update your branch:
   ```bash
   git fetch upstream
   git rebase upstream/main
   git push --force-with-lease
   ```

Version numbers and releases are handled by maintainers; don't change `version` in `pyproject.toml`.

## Rules

- One canonical copy per skill; do not create per-platform copies by hand.
- Use full, descriptive `kebab-case` names; avoid unclear abbreviations.
- Write all skill content in English. Docs live in `docs/locales/<lang>/` (English in `docs/locales/en-US/`, the source of truth); translations are updated in the same pull request.
- Do not commit secrets, credentials, or private product data.
- Review any executable script and its dependencies before adding it.
