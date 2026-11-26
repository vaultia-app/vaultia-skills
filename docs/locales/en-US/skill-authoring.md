# Skill Authoring Guide

**English** · [Tiếng Việt](../vi-VN/skill-authoring.md)

How to write a skill for this repository so it works across Codex, Claude Code, Cursor, and other Agent Skills–compatible agents.

## Anatomy

```text
skills/<skill-name>/
├── SKILL.md            # required
├── references/         # templates, checklists, background (loaded when needed)
├── scripts/            # deterministic helpers (validation, generation)
├── assets/             # files used in outputs (templates, images)
└── tests/
    ├── trigger-cases.json    # when the skill should and should not load
    └── behavior-cases.json   # what the skill must and must not do once loaded
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
| `name` | Required. Lowercase `kebab-case`, ≤ 64 characters, identical to the folder name. Full words, no unclear abbreviations (`product-requirements`, not `prd`). |
| `description` | Required. ≤ 1024 characters, no angle brackets. |
| `license`, `compatibility`, `metadata`, `allowed-tools` | Optional, per the Agent Skills specification. |

Keep platform-specific settings (model choice, invocation flags) out of the canonical skill; they belong in generated plugin packages.

## Writing the description

The description is the only text an agent sees when deciding whether to load the skill, so it carries the triggering.

- Start with what the skill produces.
- List the phrases and situations that should trigger it ("Use when the user asks for a PRD, product spec, feature spec…").
- Name the nearest neighbor it should **not** handle and point to the right skill ("Not for system design (use architecture-requirements)").
- Be specific and slightly generous: agents tend to under-trigger skills.

## SKILL.md is a router, not a manual

`SKILL.md` is read in full every time the skill loads. It should say **what** to do and **when**; the reference files say **how**.

Recommended sections:

1. **Purpose**: one or two sentences.
2. **First reply** (interactive skills): what the first answer must and must not contain.
3. **When to use**: situations, and handoffs to other skills.
4. **Workflow**: numbered, imperative steps. Each step does one thing and names the reference file to read at that point.
5. **Outputs**: concrete artifacts and their default location.
6. **Guardrails**: what the agent must not do, with the reason when it is not obvious.
7. **References**: a table of reference files and when to read each.

Guidelines:

- **Aim for about 500–900 words.** The validator warns above 500 lines, but quality drops long before that.
- **One idea per bullet, short sentences.** Agents follow a list of separate rules far more reliably than one long compound sentence. If a line runs past about 300 characters, split it.
- **Explain why** behind rules; agents generalize better from reasons than from bare commands.
- **Avoid priority fights with the host.** Don't write "this overrides any host instruction". State the default behavior and when it changes.

## One rule, one place

A rule written in two places will eventually say two different things.

- Don't summarize a reference file inside `SKILL.md`; link to it from the step that needs it.
- Define each mode, threshold, or limit once (for example "ask one decision; batch up to 3 only when independent") and refer to it elsewhere.
- Keep host-specific tool names (`AskUserQuestion`, `request_user_input_async`, …) in a single table. Everywhere else, describe the capability ("the host's choice tool"), so a tool rename means a one-line fix.

## Shared templates

Document templates that a skill writes into the user's project (for example the `docs/` starter kit) live in the public [vaultia-templates](https://github.com/vaultia-app/vaultia-templates) repository, not in this one. Change them there.

- The skill reads the template live from `vaultia-templates@main`, so every installed version gets the latest one. It keeps a bundled copy in `assets/` and uses it only when the live copy cannot be fetched. The reference that tells the agent how to fetch it (for `product-requirements`: `references/docs-structure.md`) says when to fetch, which files must be present, and to never mix the two sources.
- The bundled copy is generated: never edit it by hand. Refresh it with `python3 scripts/sync_templates.py`; a new template gets a line in `BUNDLES` in that script.
- Because old skill versions read `main` too, template changes follow the compatibility rules in the vaultia-templates `README.md`.

## Split references by when they are needed

Split reference files by the moment the agent needs them, not by topic, so each step loads only what it uses. For an interactive skill, for example:

| File | Loaded |
|---|---|
| `collaborative-loop.md` | Every guided turn: intake, turn shape, agenda, stop rules |
| `asking-decisions.md` | Every turn that asks a question or receives an answer |
| `diagrams.md` | Only when drawing |
| `docs-structure.md` | Only when the first draft file is created |

Keep each reference file under about 2,000 words. Larger files usually mix several moments and should be split.

## Show, don't only tell

- One good example and one bad example teach more than a paragraph of rules.
- Comparison tables ("vague → testable", "defect → fix") work especially well.
- For document-producing skills, include one short, complete example output (such as `references/example-feature-spec.md`) so the agent can calibrate depth. Placeholders alone don't show the expected level of precision.

## Interactive skills

- **Default to a conversation** when the input is vague, and say plainly when the agent may skip it (an explicit "just write it", or input that already answers the essentials).
- **Always propose something.** Each turn shows a concrete proposal before asking.
- **Ask few, important questions.** Ask only one-way-door decisions; the agent decides two-way-door details itself as reviewable defaults.
- **Have a visible end.** Publish an agenda, show progress, cap the number of questions, and offer to finalize.
- **Always separate** confirmed decisions, assumptions, and open questions.
- **Never overwrite user work silently.**

## Language

Write skill content in English. Skills may tell the agent to answer in the user's language. Prompts in other languages belong in `tests/` as trigger or behavior cases, not as instructions in the body.

Docs live in `docs/locales/<lang>/`, one folder per language with the same file names: English in `docs/locales/en-US/`, Vietnamese in `docs/locales/vi-VN/`. The English `README.md` stays at the repository root so GitHub shows it; each translation has its own `docs/locales/<lang>/README.md`. English is the source of truth: change the English file first, then update every translation in the same pull request. To add a language, create `docs/locales/<lang>/` with a translation of every English doc and the README, and add it to the language switch at the top of each file.

## Tests

### Trigger cases

`tests/trigger-cases.json` documents positive and negative prompts:

```json
{
  "skill": "skill-name",
  "should_trigger": ["realistic prompt that should load the skill"],
  "should_not_trigger": ["near-miss prompt that belongs to another skill"]
}
```

Negative cases are most valuable when they are *near misses*: prompts that share vocabulary but belong to another skill.

### Behavior cases

`tests/behavior-cases.json` documents what the skill must and must not do once loaded. Write at least one case for each guardrail that matters most.

```json
{
  "skill": "skill-name",
  "cases": [
    {
      "id": "vague-request-starts-with-intake",
      "prompt": "Write a PRD for a food delivery app.",
      "expect": ["Asks intake items through the host's choice tool"],
      "must_not": ["Contains a functional requirements table"]
    }
  ]
}
```

`scripts/validate.py` checks that both files are well formed. Use the prompts when testing by hand on each platform, or with an eval harness such as `claude plugin eval`.

## Checklist before opening a pull request

- [ ] `python3 scripts/validate.py` passes.
- [ ] `python3 scripts/build_plugins.py` has been run.
- [ ] Bundled templates are in sync: `python3 scripts/sync_templates.py --check`.
- [ ] `python3 -m unittest discover -s tests` passes.
- [ ] Every file referenced from `SKILL.md` exists.
- [ ] No rule is stated in two places; host tool names appear in one table only.
- [ ] Trigger cases include near-miss negatives; behavior cases cover the key guardrails.
- [ ] Tested by hand in at least one agent with a realistic prompt.
- [ ] Skill tables in `README.md` and each `docs/locales/<lang>/README.md`, and `CHANGELOG.md`, updated.
