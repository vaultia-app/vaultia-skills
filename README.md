<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/vaultia-brand-kit/logos/vaultia-horizontal-dark.svg">
    <img src="assets/vaultia-brand-kit/logos/vaultia-horizontal-light.svg" alt="Vaultia" width="260">
  </picture>
</p>

<p align="center">
  <strong>🇺🇸 English</strong> | <a href="docs/locales/vi-VN/README.md">🇻🇳 Tiếng Việt</a>
</p>

<p align="center">
  <a href="https://github.com/vaultia-app/vaultia-skills/releases/latest"><img src="https://img.shields.io/badge/release-v0.3.2-FFC533?style=for-the-badge&labelColor=3a3a3a" alt="Release v0.3.2"></a>
  <a href="skills"><img src="https://img.shields.io/badge/skills-3-2EA043?style=for-the-badge&labelColor=3a3a3a" alt="Skills: 3"></a>
  <a href="#installation"><img src="https://img.shields.io/badge/works_with-Claude_Code_%C2%B7_Codex_%C2%B7_ChatGPT_%C2%B7_Cursor-6E40C9?style=for-the-badge&labelColor=3a3a3a" alt="Works with Claude Code, Codex, ChatGPT, Cursor"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-D9A400?style=for-the-badge&labelColor=3a3a3a&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-TBD-8A8A8A?style=for-the-badge&labelColor=3a3a3a" alt="License: TBD">
</p>

<p align="center">
  <a href="https://github.com/vaultia-app/vaultia-skills/actions/workflows/validate.yml"><img src="https://github.com/vaultia-app/vaultia-skills/actions/workflows/validate.yml/badge.svg" alt="Validate"></a>
  <a href="https://github.com/vaultia-app/vaultia-skills/stargazers"><img src="https://img.shields.io/github/stars/vaultia-app/vaultia-skills?style=flat&logo=github&label=stars" alt="GitHub stars"></a>
  <a href="https://github.com/vaultia-app/vaultia-skills/commits/main"><img src="https://img.shields.io/github/last-commit/vaultia-app/vaultia-skills?style=flat" alt="Last commit"></a>
</p>

<p align="center">
  AI Agent Skills that turn a product idea into build-ready specs: a PRD first, then the screens and the system design.<br>They work <strong>with</strong> you, proposing options and asking one decision at a time instead of guessing.
</p>

## Skills

| Skill | What it does | Answers |
|---|---|---|
| [`product-requirements`](skills/product-requirements/SKILL.md) | Product requirements documents (PRDs): goals, users, journeys, functional requirements, acceptance criteria, success metrics, scope, rollout | **WHAT / WHY** |
| [`ui-ux-design`](skills/ui-ux-design/SKILL.md) | Screen maps, user flows, layouts, UI states, accessibility, and brand themes, built as React screens with the ready-made [Base UI React kit](https://github.com/vaultia-app/vaultia-templates/tree/main/src/frontend/base-ui-react-kit) | **LOOK / FEEL** |
| [`architecture-requirements`](skills/architecture-requirements/SKILL.md) | Architecture and system design: drivers, components, APIs, data models, NFRs, security, deployment, ADRs | **HOW / CONSTRAINTS** |

```text
Product idea
  → product-requirements       (WHAT / WHY)
  → ui-ux-design               (LOOK / FEEL)
  → architecture-requirements  (HOW / CONSTRAINTS)
  → implementation
```

Each skill also works on its own when enough input is available.

## Installation

### Claude Code

```bash
claude plugin marketplace add vaultia-app/vaultia-skills
claude plugin install vaultia-skills@vaultia-skills        # all skills
claude plugin install product-requirements@vaultia-skills  # or a single skill
```

### Codex CLI and ChatGPT

```bash
codex plugin marketplace add vaultia-app/vaultia-skills
codex plugin add vaultia-skills@vaultia-skills
```

The ChatGPT desktop app shows marketplaces added this way in its **Plugins** directory.

### claude.ai or ChatGPT (upload)

Download `vaultia-plugin.zip` from the [latest release](https://github.com/vaultia-app/vaultia-skills/releases/latest) and upload it as a plugin. The same file works on every platform below. To build it yourself, run `python3 scripts/build_plugins.py --zip` (output: `dist/plugins/vaultia.zip`).

| Platform | Upload | Where |
|---|---|---|
| claude.ai, Claude Desktop, ChatGPT | `vaultia-plugin.zip` | **Plugins → Upload** |

### Manual copy (any agent)

Copy or symlink a skill folder into your agent's skills directory:

| Platform | Project scope | User scope |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |

```bash
# Claude Code, available in every project
mkdir -p ~/.claude/skills
cp -R skills/product-requirements skills/ui-ux-design skills/architecture-requirements ~/.claude/skills/

# Local development: symlink so edits are picked up immediately
ln -s "$PWD/skills/product-requirements" ~/.claude/skills/product-requirements
```

More options, team setup, and updating: [plugin distribution guide](docs/locales/en-US/plugin-distribution.md).

## Usage

Ask your agent naturally:

- *"Write a PRD for a personal expense tracking app."*
- *"Turn these meeting notes into requirements with acceptance criteria."*
- *"Design the admin portal screens from this PRD."*
- *"Turn this PRD into a technical design."*
- *"Review this architecture for gaps and risks."*

In Claude Code you can also call a skill directly, for example `/product-requirements`. To skip the questions and get a draft right away, say *"just write it"*.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [skill authoring guide](docs/locales/en-US/skill-authoring.md).

## License

Not yet chosen. A license will be added before the first public release.
