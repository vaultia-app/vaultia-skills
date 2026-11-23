# Skill Authoring Guide

How to write a skill for this repository so it works across Codex, Claude Code, Cursor, and other Agent Skills–compatible agents.

## Anatomy

```text
skills/<skill-name>/
├── SKILL.md            # required
├── references/         # templates, checklists, background (loaded when needed)
├── scripts/            # deterministic helpers (validation, generation)
├── assets/             # files used in outputs (templates, images)
└── tests/
    └── trigger-cases.json
```

Only `SKILL.md` is required. Add the other folders when they have content.

## Frontmatter

Use only portable fields:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
---
```

| Field | Rules |
|---|---|
| `name` | Required. Lowercase `kebab-case`, ≤ 64 characters, identical to the folder name. Full words — no unclear abbreviations (`product-requirements`, not `prd`). |
| `description` | Required. ≤ 1024 characters, no angle brackets. |
| `license`, `compatibility`, `metadata`, `allowed-tools` | Optional, per the Agent Skills specification. |

Keep platform-specific settings (model choice, invocation flags) out of the canonical skill; they belong in generated plugin packages.

## Writing the description

The description is the only text an agent sees when deciding whether to load the skill, so it carries the triggering.

- Start with what the skill produces.
- List the phrases and situations that should trigger it ("Use when the user asks for a PRD, product spec, feature spec…").
- Name the nearest neighbor it should **not** handle and point to the right skill ("Not for system design (use architecture-requirements)").
- Be specific and slightly generous — agents tend to under-trigger skills.

## Writing the body

Recommended sections:

1. **Purpose** — one or two sentences.
2. **When to use** — situations, and handoffs to other skills.
3. **Inputs** — what helps; mark what is essential.
4. **Workflow** — numbered, imperative steps. Point to reference files at the step where they are needed.
5. **Outputs** — concrete artifacts and their default location.
6. **Guardrails** — what the agent must not do, with the reason when not obvious.
7. **References** — a table of reference files and when to read each.

Guidelines:

- Keep `SKILL.md` under ~500 lines; move templates and detailed guidance into `references/`.
- Explain *why* behind rules; agents generalize better from reasons than from bare commands.
- Prefer one focused question at a time over long questionnaires; capture the rest as assumptions.
- Always separate confirmed decisions, assumptions, and open questions.
- Never instruct an agent to overwrite user work silently.
- Write in English. Skills may tell the agent to answer in the user's language.

## Trigger cases

`tests/trigger-cases.json` documents positive and negative prompts:

```json
{
  "skill": "skill-name",
  "should_trigger": ["realistic prompt that should load the skill"],
  "should_not_trigger": ["near-miss prompt that belongs to another skill"]
}
```

Negative cases are most valuable when they are *near misses* — prompts that share vocabulary but belong to another skill. Use these prompts when manually testing skill selection on each platform.

## Checklist before opening a pull request

- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 -m unittest discover -s tests` passes.
- [ ] Every file referenced from `SKILL.md` exists.
- [ ] Trigger cases include near-miss negatives.
- [ ] Tested by hand in at least one agent with a realistic prompt.
- [ ] `README.md` skill table and `CHANGELOG.md` updated.
