<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/vaultia-brand-kit/logos/vaultia-horizontal-dark.svg">
    <img src="assets/vaultia-brand-kit/logos/vaultia-horizontal-light.svg" alt="Vaultia" width="260">
  </picture>
</p>

# Vaultia Skills

Reusable AI Agent Skills for Codex, Claude Code, Cursor, and other agents that support the [Agent Skills](https://agentskills.io/specification) format.

Each skill is a folder with a `SKILL.md` (when to use it, workflow, outputs, guardrails) and supporting reference files that the agent loads only when needed. One canonical copy lives in `skills/`; it works on every supported platform.

## Skills

| Skill | What it does | Status |
|---|---|---|
| [`product-requirements`](skills/product-requirements/SKILL.md) | Product requirements documents (PRDs): goals, users, journeys, functional requirements, acceptance criteria, success metrics, scope, rollout. Answers **WHAT / WHY**. | Available |
| [`architecture-requirements`](skills/architecture-requirements/SKILL.md) | Architecture and system design: drivers, components, APIs, data models, NFRs, security, deployment, ADRs. Answers **HOW / CONSTRAINTS**. | Available |

Planned: `product-discovery`, `market-research`, `user-experience-design`, `api-design`, `database-design`, `code-review`, `software-testing`, `software-deployment`.

### Core workflow

```text
Product idea
  → product-requirements       (WHAT / WHY)
  → architecture-requirements  (HOW / CONSTRAINTS)
  → implementation
```

Each skill also works on its own when enough input is available.

## Installation

Replace `OWNER` with the GitHub account hosting this repository. Full details: [docs/plugin-distribution.md](docs/plugin-distribution.md).

### Claude Code (plugin)

```bash
claude plugin marketplace add OWNER/vaultia-skills
claude plugin install vaultia-skills@vaultia-skills        # all skills
claude plugin install product-requirements@vaultia-skills  # or a single skill
```

### Codex CLI and ChatGPT (plugin)

```bash
codex plugin marketplace add OWNER/vaultia-skills
codex plugin add vaultia-skills@vaultia-skills
```

The ChatGPT desktop app shows marketplaces added this way in its **Plugins** directory. Workspace admins can import the GitHub marketplace for everyone.

### claude.ai or ChatGPT (upload a skill)

```bash
python3 scripts/build_plugins.py --zip
```

Upload `dist/skills/<skill>.zip` in claude.ai under **Settings → Capabilities → Skills**, or in ChatGPT under **Plugins → Skills → Upload from computer**.

### Manual copy (any agent)

Copy (or symlink) a skill folder into your agent's skills directory.

| Platform | Project scope | User / global scope |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |

Examples:

```bash
# Claude Code, available in every project
mkdir -p ~/.claude/skills
cp -R skills/product-requirements skills/architecture-requirements ~/.claude/skills/

# Cursor, only for one project
mkdir -p /path/to/project/.cursor/skills
cp -R skills/product-requirements /path/to/project/.cursor/skills/

# Local development: symlink so edits are picked up immediately
ln -s "$PWD/skills/product-requirements" ~/.agents/skills/product-requirements
```

Then ask your agent naturally, for example: *"Write a PRD for team calendars"* or *"Turn this PRD into a technical design."* Claude Code also lets you invoke a skill directly with `/product-requirements`.

An automated installer for manual copies (`scripts/install.py` with global / project / hybrid scopes) is planned — see [the roadmap](#roadmap).

## Repository layout

```text
skills/<skill-name>/
├── SKILL.md            # Instructions + portable frontmatter (name, description)
├── references/         # Templates, checklists, guidelines (loaded on demand)
├── scripts/            # Optional deterministic helpers
├── assets/             # Optional output resources
└── tests/              # Trigger cases (should / should not activate)
plugins/claude/         # Generated Claude Code plugins (do not edit)
plugins/openai/         # Generated Codex / ChatGPT plugins (do not edit)
.claude-plugin/         # Generated Claude Code marketplace
.agents/plugins/        # Generated Codex / ChatGPT marketplace
scripts/validate.py     # Skill validator
scripts/build_plugins.py# Plugin, marketplace and zip builder
tests/                  # Repository tests
docs/                   # Authoring and architecture docs
assets/vaultia-brand-kit/ # README logo and OpenAI plugin icons (only assets in use)
```

## Development

Requires Python 3.10+. No third-party dependencies.

```bash
python3 scripts/validate.py              # validate all skills
python3 scripts/build_plugins.py         # regenerate plugins after changing skills/
python3 -m unittest discover -s tests    # run tests (pytest also works)
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/skill-authoring.md](docs/skill-authoring.md) before adding or changing a skill.

## Roadmap

1. **Phase 1 — MVP (done):** `product-requirements`, `architecture-requirements`, shared format, validator, tests, CI.
2. **Plugins (done):** plugin builder, Claude Code and Codex / ChatGPT plugins and marketplaces, upload zips.
3. **Next:** installer (global / project / hybrid, dry-run, uninstall), Cursor plugin, versioned releases.
4. **Phase 4:** Additional skills as usage warrants.

## License

Not yet chosen. A license must be selected before public distribution.
