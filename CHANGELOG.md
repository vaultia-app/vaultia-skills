# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `product-requirements` skill with requirements template, discovery questions, acceptance-criteria guide, and quality checklist.
- `architecture-requirements` skill with architecture template, patterns, non-functional requirements, API design, data model, and security checklist references.
- Trigger cases for both skills.
- `scripts/validate.py` skill validator and its unit tests.
- `scripts/build_plugins.py`: generates Claude Code plugins (`plugins/claude/`) with `.claude-plugin/marketplace.json`, Codex / ChatGPT plugins (`plugins/openai/`) with `.agents/plugins/marketplace.json`, and skill zips for claude.ai / ChatGPT upload. One plugin per skill plus the `vaultia-skills` bundle.
- `docs/plugin-distribution.md` with install instructions per platform.
- GitHub Actions workflow running validation and tests.
- README, agent instructions, contributing and skill-authoring guides.
