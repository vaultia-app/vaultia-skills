# Plugin Distribution

Canonical skills in `skills/` are packaged for each platform by `scripts/build_plugins.py`. Everything it generates is committed so platforms can install straight from the GitHub repository. **Never edit generated files by hand**; change `skills/` and rebuild.

Replace `OWNER` below with the GitHub account or organization that hosts this repository.

## What gets built

| Output | Platform | Purpose |
|---|---|---|
| `.claude-plugin/marketplace.json` | Claude Code | Marketplace listing every plugin |
| `plugins/claude/<plugin>/.claude-plugin/plugin.json` + `skills/` | Claude Code | Installable plugin |
| `.agents/plugins/marketplace.json` | Codex CLI, ChatGPT | Marketplace listing every plugin |
| `plugins/openai/<plugin>/plugin.json` + `skills/` | Codex CLI, ChatGPT | Installable plugin (portable root `plugin.json`) |
| `dist/skills/<skill>.zip` (`--zip`, not committed) | claude.ai, ChatGPT | Manual skill upload |

Plugins built:

| Plugin | Contains |
|---|---|
| `product-requirements` | `product-requirements` |
| `architecture-requirements` | `architecture-requirements` |
| `vaultia-skills` | every skill (bundle) |

The skills' `tests/` folders are left out of plugins and zips.

```bash
python3 scripts/build_plugins.py          # regenerate plugins + marketplaces
python3 scripts/build_plugins.py --zip    # also build dist/skills/*.zip
python3 scripts/build_plugins.py --check  # CI: fail if generated files are stale
```

The plugin version comes from `version` in `pyproject.toml`.

## Claude Code

```bash
claude plugin marketplace add OWNER/vaultia-skills
claude plugin install vaultia-skills@vaultia-skills          # all skills
claude plugin install product-requirements@vaultia-skills    # or one skill
```

Inside a session the same works with `/plugin marketplace add OWNER/vaultia-skills` and `/plugin install …`. Skills are namespaced by plugin, e.g. `/vaultia-skills:product-requirements`.

Teams can preconfigure the marketplace in a project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "vaultia-skills": { "source": { "source": "github", "repo": "OWNER/vaultia-skills" } }
  },
  "enabledPlugins": { "vaultia-skills@vaultia-skills": true }
}
```

Validate before publishing:

```bash
claude plugin validate .                              # marketplace
claude plugin validate plugins/claude/vaultia-skills  # a plugin
```

Update after a new release: `claude plugin marketplace update vaultia-skills`.

## Codex CLI

```bash
codex plugin marketplace add OWNER/vaultia-skills
codex plugin list
codex plugin add vaultia-skills@vaultia-skills
```

Start a new Codex session after installing. Update with `codex plugin marketplace upgrade vaultia-skills`.

## ChatGPT

ChatGPT reads the same plugin format as Codex. Options:

1. **Desktop app, local testing:** add the marketplace with `codex plugin marketplace add …` (above) and install from the **Plugins** directory in the ChatGPT desktop app, then start a new chat.
2. **Workspace (Business / Enterprise / Edu):** a workspace admin can import this GitHub marketplace in the workspace plugin management settings, or publish an installed local plugin from **Plugins → Personal → ⋯ → Publish**.
3. **Single skill upload:** build `dist/skills/<skill>.zip` and upload it under **Plugins → Skills → Upload from computer**.
4. **Public listing:** submit through OpenAI's plugin submission portal (requires a license, privacy policy and review).

Skill availability differs by ChatGPT plan and surface (web, desktop, mobile); check OpenAI's current documentation.

## claude.ai (web, desktop, mobile)

Build the zips and upload each under **Settings → Capabilities → Skills → Upload skill**:

```bash
python3 scripts/build_plugins.py --zip
# upload dist/skills/product-requirements.zip and dist/skills/architecture-requirements.zip
```

Each zip contains a single `<skill-name>/` folder with `SKILL.md` at its top. Organization owners can provision skills for everyone from the admin settings.

## Release checklist

1. Bump `version` in `pyproject.toml` and update `CHANGELOG.md`.
2. `python3 scripts/validate.py && python3 scripts/build_plugins.py --zip`
3. `python3 -m unittest discover -s tests`
4. `claude plugin validate .`
5. Commit, tag `vX.Y.Z`, push, and attach `dist/skills/*.zip` to the GitHub release.
