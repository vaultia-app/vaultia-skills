# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed (product-requirements restructure)
- `product-requirements` SKILL.md slimmed to a router: short First reply rules, one-line workflow steps that point to references, no duplicated loop content.
- `collaborative-loop.md` split: choice tools, multi-select, fallback and answer handling move to `references/asking-decisions.md`; Mermaid rules move to `references/diagrams.md`. Host tool names now appear in one table only.
- Conflicting rules unified: one blocking decision per turn, batch up to 3 only when independent; fast mode defined once.
- `docs/skill-authoring.md` restored and extended (router principle, one rule per place, split references by moment, examples, behavior cases).

### Added
- Translated documentation under `docs/locales/<lang>/`, starting with Vietnamese (`docs/locales/vi/`: README, skill authoring, plugin distribution), with a language switch at the top of each file. English stays the source of truth.
- README header: language switch with flags, release / skills / platforms / Python / license badges, CI / stars / last-commit badges, and a hero image (`assets/vaultia-brand-kit/readme/hero.svg`). A test keeps the release badge in sync with `pyproject.toml`.
- `docs/plugin-distribution.md` restored and updated (GitHub owner, plugin zips, release steps).
- `tests/test_docs.py`: every locale translates every English doc, and local links in docs resolve.
- `product-requirements/references/example-prd.md`: a complete small-feature PRD for calibrating depth.
- `tests/behavior-cases.json` for `product-requirements`, checked by `scripts/validate.py`.
- More trigger cases, including near-miss negatives (ADR, release notes, technical design).
- `product-requirements` skill with requirements template, discovery questions, acceptance-criteria guide, and quality checklist.
- `architecture-requirements` skill with architecture template, patterns, non-functional requirements, API design, data model, and security checklist references.
- Trigger cases for both skills.
- `scripts/validate.py` skill validator and its unit tests.
- `scripts/build_plugins.py`: generates Claude Code plugins (`plugins/claude/`) with `.claude-plugin/marketplace.json`, Codex / ChatGPT plugins (`plugins/openai/`) with `.agents/plugins/marketplace.json`, and skill zips for claude.ai / ChatGPT upload. One plugin per skill plus the `vaultia-skills` bundle.
- `docs/plugin-distribution.md` with install instructions per platform.
- GitHub Actions workflow running validation and tests.
- README, agent instructions, contributing and skill-authoring guides.
- OpenAI plugin branding (logo, composer icons, brand colors) and store listing fields; the bundle is listed as "Vaultia".
- `build_plugins.py --zip` also builds `dist/plugins/<plugin>.zip`, one upload for both ChatGPT (`.codex-plugin/plugin.json`) and Claude (`.claude-plugin/plugin.json`).

### Changed
- Both skills start in guided mode for short requests and ask one decision at a time before drafting.
- Guided mode uses the host's choice form for every decision turn, not only the first.
- Guided mode keeps asking until v1.0: progress line, typed answers confirmed through the choice form, open questions asked in order, and a final "Finalize v1.0" choice.
- Claude Code plugins and marketplace entries carry `displayName` ("Vaultia" for the bundle) and an `icon` for Anthropic's plugin directory.
- Choice forms submit only the answer (`<topic>: <option>`), without extra instructions.
- Decisions follow each host's choice tool contract (`request_user_input_async` / `request_user_input` in ChatGPT and Codex, `AskUserQuestion` in Claude): recommended option first, no manual "Other" option, then wait for the answer.
- Multiple-choice decisions: `multiSelect` in Claude, ready-made sets plus typed combinations in ChatGPT / Codex, letters in plain text.
- Decisions carry stable IDs (`D-n`); an answer to an already-decided question is treated as a proposed change (impact shown, keep or change asked, old value kept in the change log) instead of overwriting the draft.
- New ideas raised in free chat are summarized and offered for capture into the draft (Must / Later / open question / discard) through the choice tool, together with any pending question.
- Guided mode publishes a decision agenda up front (PRD 6–10, architecture 8–12 one-way-door decisions), records implementation details as reviewable 🟡 defaults instead of asking, and offers to finalize when the agenda or budget is reached.
- Both skills: `references/existing-context.md` for handoffs, specs, ADRs and codebases — context ledger, decided items as constraints, reuse of existing names and IDs, agenda from the source's open items, deltas instead of new documents.
- Guided mode builds the document in stages with approval gates, and shows a document map before producing a whole documentation set.
- `product-requirements`: new *Domain model and business rules* section (conceptual ER diagram, lifecycles, `BR-n` rules with worked examples); ERD requests are split into conceptual (PRD) and logical/physical (`architecture-requirements`).
- `architecture-requirements`: the data model starts from the PRD domain model and extends existing tables instead of creating parallel ones.
- Vague or partial input starts with a short intake form (name, purpose, users, platform, must-haves, business model, constraints for PRDs; requirements source, scale, stack, team, integrations, constraints for architecture) with domain-based suggested answers; answers are then enriched with domain notes (workflows, regulations, pitfalls) marked 🟡 before the agenda starts.
- Self-built forms (inline widgets, visualizations, HTML cards) always include an "Other — type your own answer" option with a text input; only native question tools omit it.
- Diagrams: Mermaid stays the source in documents; where the surface shows Mermaid as text (ChatGPT chat, canvas, documents) the diagram is also rendered visually, or shown as a relationship table / text tree instead of raw code.
