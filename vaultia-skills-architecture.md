# Vaultia Skills — Repository Architecture

> **Status:** Architecture proposal (not yet implemented)  
> **Repository:** `vaultia-skills`  
> **Purpose:** Reusable Agent Skills and plugin distribution for OpenAI Codex, Claude Code, Cursor, and other compatible AI agents.

## 1. Decisions

- **Repository name:** `vaultia-skills`.
- **Naming:** Full, descriptive, lowercase `kebab-case` names; avoid unclear abbreviations such as `prd` and `ard`.
- **Core skills:** `product-requirements` and `architecture-requirements`.
- **Distribution model:** Hybrid — install skills at user/global scope or per-project; package platform-specific plugins where supported.
- **Source of truth:** One canonical implementation of each skill in `skills/<skill-name>/`.
- **Goal:** Avoid maintaining separate manual copies of the same skill for Codex, Claude Code and Cursor.

## 2. Architecture

```text
User request
    ↓
Agent / platform skill discovery
    ↓
skills/<skill-name>/SKILL.md
    ├── references/  (templates, checklists, guidelines)
    ├── scripts/     (optional automated operations)
    ├── assets/      (optional output resources)
    └── tests/       (optional skill test cases)
    ↓
Product Requirements / Architecture Requirements / other outputs
```

`SKILL.md` defines when the skill is useful, its inputs, workflow, outputs, and guardrails. Reference documents are loaded when needed rather than embedding everything in the main instructions.

**Separation of concerns:**
- **Agent instructions (`AGENTS.md`, `CLAUDE.md`, etc.):** repo-wide behavior or platform-specific guidance.
- **Skills:** task-specific operational instructions.
- **References:** templates and background material.
- **Scripts:** deterministic tasks such as validation and packaging.
- **Plugins:** platform-specific installable packages, generated from canonical skills.
- **Tools:** platform runtime capabilities (web, filesystem, code execution, etc.), not the same as skills.

## 3. Proposed repository tree

```text
vaultia-skills/
├── skills/                           # Canonical skills (edit here)
│   ├── product-requirements/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── requirements-template.md
│   │   │   ├── discovery-questions.md
│   │   │   ├── acceptance-criteria.md
│   │   │   └── quality-checklist.md
│   │   ├── assets/
│   │   └── tests/
│   ├── architecture-requirements/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── architecture-template.md
│   │   │   ├── architecture-patterns.md
│   │   │   ├── non-functional-requirements.md
│   │   │   ├── api-design.md
│   │   │   ├── data-model.md
│   │   │   └── security-checklist.md
│   │   ├── assets/
│   │   └── tests/
│   ├── product-discovery/
│   │   └── SKILL.md
│   ├── market-research/
│   │   └── SKILL.md
│   ├── user-experience-design/
│   │   └── SKILL.md
│   ├── api-design/
│   │   └── SKILL.md
│   ├── database-design/
│   │   └── SKILL.md
│   ├── code-review/
│   │   └── SKILL.md
│   ├── software-testing/
│   │   └── SKILL.md
│   └── software-deployment/
│       └── SKILL.md
├── plugins/                          # Generated packages, not hand-edited
│   ├── claude/
│   └── cursor/
├── .claude-plugin/
│   └── marketplace.json              # If publishing a Claude plugin marketplace
├── scripts/
│   ├── install.py                     # global / project / hybrid
│   ├── uninstall.py
│   ├── validate.py
│   ├── sync.py
│   └── build_plugins.py
├── tests/
│   ├── test_installer.py
│   ├── test_validator.py
│   └── test_plugins.py
├── docs/
│   ├── getting-started.md
│   ├── architecture.md
│   ├── installation.md
│   ├── plugin-distribution.md
│   └── skill-authoring.md
├── .github/
│   └── workflows/
│       ├── validate.yml
│       ├── test.yml
│       └── release.yml
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── pyproject.toml
```

This is a **target structure**, not a claim that these files already exist. Create only the files needed for the first release.

## 4. Skill catalog

| Skill | Responsibility | Priority |
|---|---|---|
| `product-requirements` | Product goals, users, user journeys, functional requirements, acceptance criteria, success metrics, scope and rollout | P0 |
| `architecture-requirements` | System design, architecture constraints, APIs, data models, security, performance and scalability | P0 |
| `product-discovery` | User problems, interviews, Jobs-to-be-Done and assumptions | P1 |
| `market-research` | Market landscape, competitors and benchmarks | P1 |
| `user-experience-design` | User flows, UX requirements and wireframes | P1 |
| `api-design` | API contracts and interface design | P1 |
| `database-design` | Data schemas, relationships and migrations | P1 |
| `code-review` | Code quality, correctness, maintainability and risk review | P2 |
| `software-testing` | Test plans, cases and strategies | P2 |
| `software-deployment` | Release, deployment, rollback and operations | P2 |

### Core workflow

```text
Product idea
    → product-requirements  (WHAT / WHY)
    → architecture-requirements  (HOW / CONSTRAINTS)
    → implementation
```

Both core skills should also work independently when sufficient input is available.

## 5. Portable SKILL.md format

Example: `skills/product-requirements/SKILL.md`

```markdown
---
name: product-requirements
description: Create, refine and review product requirements documents for software products and features. Use when a user needs a PRD or actionable product requirements.
---

# Product Requirements

## Inputs
- Product idea and context
- Target users and user problems
- Goals, constraints, and existing decisions

## Workflow
1. Read available context and existing requirements.
2. Identify missing essential information.
3. Ask one focused question at a time when needed.
4. Read `references/requirements-template.md`.
5. Create or update the requirements document.
6. Check measurability, traceability and testability.
7. Separate confirmed decisions, assumptions and open questions.

## Outputs
- Product requirements document
- Acceptance criteria
- Risks and open questions

## Guardrails
- Do not invent confirmed product decisions.
- Do not silently overwrite existing work.
- Keep requirements clear and testable.
```

Use the portable `name` and `description` frontmatter fields and ordinary Markdown; keep optional platform-specific settings outside the shared skill when practical.

## 6. Multi-platform installation

| Platform | Project scope | User/global scope |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |

**Hybrid model:**
- **Global:** General skills reused across unrelated projects.
- **Project:** Skills pinned/selected for a specific codebase or team.
- **Plugin:** Distribute installable bundles via each supported platform's native mechanism.

Suggested installer interface (**planned, not implemented**):

```bash
python scripts/install.py --scope global --platform all --skill product-requirements
python scripts/install.py --scope project --platform all --skill architecture-requirements
python scripts/install.py --scope project --platform cursor --all
python scripts/validate.py
python scripts/build_plugins.py --all
```

Installer design requirements: choose project/global destination, copy by default, optional symlink for local development, `--dry-run`, conflict detection, safe overwrite/backups, uninstall support, and validation. Confirm individual platform/plugin version compatibility during implementation.

## 7. Plugin packaging strategy

Canonical skill:

```text
skills/product-requirements/
```

Generated distributables (example):

```text
plugins/
├── claude/
│   └── product-requirements/
│       ├── .claude-plugin/plugin.json
│       └── skills/product-requirements/
└── cursor/
    └── product-requirements/
        ├── .cursor-plugin/plugin.json
        └── skills/product-requirements/
```

- Generate platform packages with `scripts/build_plugins.py`; do **not** manually modify generated copies.
- Claude Code can use a plugin marketplace manifest to list plugins.
- Cursor packaging follows its own manifest/distribution requirements.
- Codex can install standalone skills from a repository; plugin installation is a separate platform-specific concern.
- A skill/plugin for Claude, Cursor or Codex is **not automatically a ChatGPT Plugin**.

## 8. Quality and security

- Validate every `SKILL.md` frontmatter, names and required files.
- Check internal links, references and scripts.
- Test skill selection (positive/negative cases) and useful output quality, not just YAML syntax.
- Test installer in clean temporary home/project directories.
- Test plugin builds and detect divergence from canonical sources.
- Run checks in GitHub Actions on pull requests.
- Version changes with Git tags/releases.
- Never commit secrets, user credentials or private product data.
- Review any executable scripts and their dependencies before distribution.

## 9. Implementation roadmap

1. **Phase 1 (MVP):** `product-requirements`, `architecture-requirements`, shared format, README, validator and basic tests.
2. **Phase 2:** Hybrid installer, uninstall, CI, platform smoke tests.
3. **Phase 3:** Plugin builder, Claude/Cursor manifests, distribution docs and versioned releases.
4. **Phase 4:** Add P1/P2 skills as usage warrants.

## 10. Repository metadata

- **GitHub repository:** `vaultia-skills`
- **Description:** `Reusable AI Agent Skills and plugins for Codex, Claude Code, Cursor, and more.`
- **License:** Choose explicitly before public distribution.
- **Visibility:** Public if community distribution is desired.

## 11. References

- Agent Skills Specification: https://agentskills.io/specification
- OpenAI skills examples: https://github.com/openai/skills
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Cursor documentation: https://cursor.com/docs/skills

---

**Note:** This document summarizes the architecture and naming decisions discussed. It does not include a fully implemented or tested repository yet.
