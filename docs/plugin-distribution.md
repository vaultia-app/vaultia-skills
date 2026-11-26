# Plugin Distribution

**English** · [Tiếng Việt](locales/vi/plugin-distribution.md)

Canonical skills in `skills/` are packaged for each platform by `scripts/build_plugins.py`. Plugins and marketplaces are committed so platforms can install straight from GitHub. **Never edit generated files by hand**: change `skills/` and rebuild.

## What gets built

| Output | Committed | Platform | Purpose |
|---|---|---|---|
| `.claude-plugin/marketplace.json` | Yes | Claude Code | Marketplace listing every plugin |
| `plugins/claude/<plugin>/` | Yes | Claude Code | Installable plugin |
| `.agents/plugins/marketplace.json` | Yes | Codex CLI, ChatGPT | Marketplace listing every plugin |
| `plugins/openai/<plugin>/` | Yes | Codex CLI, ChatGPT | Installable plugin, with brand icons |
| `dist/skills/<skill>.zip` | No (release asset) | claude.ai | Single skill upload |
| `dist/plugins/<plugin>.zip` | No (release asset) | ChatGPT, Claude Desktop | Plugin upload |

| Plugin | Contains |
|---|---|
| `product-requirements` | `product-requirements` |
| `architecture-requirements` | `architecture-requirements` |
| `vaultia-skills` (display name "Vaultia", zip `vaultia.zip`) | every skill |

The skills' `tests/` folders are left out of plugins and zips.

```bash
python3 scripts/build_plugins.py          # regenerate plugins + marketplaces
python3 scripts/build_plugins.py --zip    # also build dist/skills/*.zip and dist/plugins/*.zip
python3 scripts/build_plugins.py --check  # CI: fail if generated files are stale
```

The plugin version comes from `version` in `pyproject.toml`. Bump it on every release: platforms cache plugins by version and may not pick up changes otherwise.

## Claude Code

```bash
claude plugin marketplace add vaultia-app/vaultia-skills
claude plugin install vaultia-skills@vaultia-skills          # all skills
claude plugin install product-requirements@vaultia-skills    # or one skill
```

Inside a session the same works with `/plugin marketplace add …` and `/plugin install …`. Skills are namespaced by plugin, for example `/vaultia-skills:product-requirements`.

Teams can preconfigure the marketplace in a project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "vaultia-skills": { "source": { "source": "github", "repo": "vaultia-app/vaultia-skills" } }
  },
  "enabledPlugins": { "vaultia-skills@vaultia-skills": true }
}
```

**Update** after a new release: `claude plugin marketplace update vaultia-skills`, then start a new session.

**Test a local checkout** before pushing: `claude plugin marketplace add ./` from the repository root.

Validate before publishing:

```bash
claude plugin validate .                              # marketplace
claude plugin validate plugins/claude/vaultia-skills  # a plugin
```

## Codex CLI

```bash
codex plugin marketplace add vaultia-app/vaultia-skills
codex plugin list
codex plugin add vaultia-skills@vaultia-skills
```

Start a new Codex session after installing. Update with `codex plugin marketplace upgrade vaultia-skills`.

## ChatGPT

ChatGPT reads the same plugin format as Codex:

1. **Desktop app:** add the marketplace with `codex plugin marketplace add …` and install from the **Plugins** directory, then start a new chat.
2. **Upload:** upload `dist/plugins/vaultia.zip`.
3. **Workspace (Business / Enterprise / Edu):** an admin can import this GitHub marketplace in the workspace plugin settings.
4. **Public listing:** submit through OpenAI's plugin submission portal (requires a license, a privacy policy, and review).

Skill availability differs by ChatGPT plan and surface; check OpenAI's current documentation.

## claude.ai (web, desktop, mobile)

Upload each `dist/skills/<skill>.zip` under **Settings → Capabilities → Skills → Upload skill**. Each zip contains a single `<skill-name>/` folder with `SKILL.md` at its top. To update, remove the old skill and upload the new zip.

## Release checklist

Releases are published by the [Release workflow](../.github/workflows/release.yml) when you push a version tag.

1. Bump `version` in `pyproject.toml` and the release badge in every README (a test checks they match).
2. In `CHANGELOG.md`, move the *Unreleased* entries under a new `## [X.Y.Z] - YYYY-MM-DD` heading. That section becomes the release notes.
3. Run the checks locally:
   ```bash
   python3 scripts/validate.py
   python3 scripts/build_plugins.py
   python3 -m unittest discover -s tests
   ```
4. Commit `skills/`, `plugins/`, both `marketplace.json` files, and the docs on a branch, open a pull request, and merge it once CI passes. `main` is protected: direct pushes are blocked (see `.github/rulesets/`).
5. Update your local `main`, then tag and push the tag (only repository admins can create `v*` tags):
   ```bash
   git switch main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

The workflow then checks that the tag matches `pyproject.toml` and that `CHANGELOG.md` has a section for it, runs validation and tests, builds the zips, and creates the GitHub release with `dist/skills/*.zip` and `dist/plugins/*.zip` attached. Pushing the same tag again (after deleting it) updates the existing release.

Preview the release notes locally with `python3 scripts/release_notes.py X.Y.Z`.
