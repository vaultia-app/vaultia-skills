# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `product-requirements` covers non-functional requirements and service commitments: it proposes product-wide NFRs as 🟡 defaults (performance, availability, security and privacy, accessibility, localization, compliance, data recovery), asks whether a product sold to customers promises an SLA, never drops the NFR section, and checks both before v1.0. The `docs/` starter kit's NFR file gains these categories and an SLA table (uptime, support response, maintenance window, data recovery).
- `architecture-requirements` maps each SLA commitment from the PRD to an SLO, SLI, design response, and verification (*From SLA to design*).

### Fixed
- `product-requirements` no longer switches itself to fast mode when the agenda is done, and no longer exports a zip without being asked: only the user switches modes, and every mode ends with v1.0 in one file followed by the delivery choice.

## [0.4.0] - 2026-11-27

### Added
- `product-requirements` scope checklist before v1.0: the user ticks the functional requirements that ship in this release (recommended set pre-ticked), the skill checks the selection for broken dependencies, an incomplete primary journey, orphan rules, and actors left without a capability, and asks how to fix each conflict. Unticked items move to a later release with their reason.

### Changed
- `product-requirements` drafts and delivers the PRD as one Markdown file, `docs/PRD.md`, using the starter kit's sections and conventions (one subsection per feature). At v1.0 the file is returned in the chat, followed by a choice: keep the single file, export to the `docs/` template (a zip in chat hosts), hand off to `architecture-requirements`, or add the next feature. The export runs only when the user chooses it. Projects that already use the `docs/` structure keep working in it.
- `architecture-requirements` splits `references/collaborative-loop.md` into the loop itself, `references/asking-decisions.md`, and `references/diagrams.md`, matching `product-requirements`, and tightens the wording: a guided turn now loads about 3,700 words instead of 5,000.
- Faster replies in chat hosts: `product-requirements` describes screens with tables instead of UI mockups; diagrams stay Mermaid in the file and appear in ChatGPT as a text version, rendered as an image only on request and only when they change; `ui-ux-design` plans in text (tables, outlines, ASCII wireframes) and renders mockups only on request.
- `ui-ux-design` uses the shadcn/ui Neutral palette as the default theme of the Base UI React kit (monochrome primary, neutral grays) and applies a brand only when the user has one.
- `product-requirements` delivers the PRD in the host's document surface (ChatGPT canvas or writing block, a Claude artifact, or the saved file) instead of plain message text, and keeps its own comments out of the document.
- Documentation cleanup across skills: decision IDs use one format (`D-001`, `Q-001`) in every skill, and `architecture-requirements` continues the project's decision numbering when it has one; host tool names appear only in each skill's *Host choice tools* table; consistent *First reply* headings and agenda numbering; `ui-ux-design` reads and records decisions in `docs/PRD.md`; the README and the plugin distribution guide list `ui-ux-design`; domain-neutral Mermaid example.

## [0.3.2] - 2026-11-26

### Added
- `ui-ux-design` skill: classifies pages into three surfaces by design intent (landing page: polished and animated; storefront: clear and specific; portal: business logic and interaction with just-enough visuals) that set the defaults for polish, motion, content, and interaction, plans screens, user flows, and every UI state from requirements, then builds them as React screens with the Base UI React kit from [vaultia-templates](https://github.com/vaultia-app/vaultia-templates) (`frontend/base-ui-react-kit`: about 60 Base UI + Tailwind CSS v4 + cva components, DTCG tokens, generated themes, English and Vietnamese locales). Sets the kit up in projects that have none, creates brand themes through tokens, and reviews existing UIs for usability and accessibility.

## [0.3.1] - 2026-11-26

### Changed
- `product-requirements` reads the `docs/` starter kit live from the public [vaultia-templates](https://github.com/vaultia-app/vaultia-templates) repository (`requirements/docs-starter`), so every installed version uses the latest templates. `assets/docs-starter/` stays as a bundled fallback, used only when the live copy cannot be fetched.

### Added
- `scripts/sync_templates.py` refreshes the bundled template copies from `vaultia-templates@main`; `--check` fails when they are out of date. The release workflow runs the check.

## [0.3.0] - 2026-11-26

### Added
- `product-requirements` writes into one standard `docs/` structure that can be used as-is. The first feature scaffolds it from the new starter kit (`assets/docs-starter/`: README, introduction, glossary, conventions, actors and permissions, domain model, business rules, workflows, feature list, non-functional requirements, feature spec template, open questions, decisions log).
- Each feature is one file, `docs/03-functional-specs/F<nn>-<slug>.md`; shared actors, objects, rules, terms, decisions, and questions are written once in the shared files and referenced by ID.
- `references/docs-structure.md`: when to scaffold, where each kind of content goes, which shared files to update, and how to number IDs.
- `tests/test_docs_starter.py` and behavior cases for scaffolding, adding a second feature, and keeping an existing docs layout.

### Changed
- `references/requirements-template.md` is replaced by the feature spec template in the starter kit; `references/example-prd.md` is now `references/example-feature-spec.md` and shows the rows a feature adds to the shared files.
- Decisions and open questions go to `09-working/decisions-log.md` (`D-001`) and `09-working/open-questions.md` (`Q-001`); feature specs list their IDs. IDs inside a spec (`FR-1`, `AC-1.1`) are local and referenced from outside as `F04/AC-1.1`.
- `architecture-requirements` saves to `docs/05-architecture/` and reads the domain model and business rules from `docs/01-business/` when the project uses the standard structure.

## [0.2.6] - 2026-11-26

### Changed
- Releases attach a single asset, `vaultia-plugin.zip`: the bundle plugin with every skill, which installs in claude.ai, Claude Desktop, and ChatGPT / Codex. Per-skill and per-plugin zips are still built locally with `build_plugins.py --zip`.

## [0.2.5] - 2026-11-26

### Added
- Rulesets in `.github/rulesets/` to protect `main` (pull request and passing CI required, no force push) and release tags (admins only).

### Changed
- README shows only what users need: the roadmap, hero image, and development section are removed; a short Contributing section links to `CONTRIBUTING.md`.
- `CONTRIBUTING.md` describes the fork-based workflow for outside contributors and leaves versioning to maintainers.
- CI uses `actions/checkout@v5` and `actions/setup-python@v6` (Node 24).
- Every language has its own docs folder named with a BCP 47 tag: English docs moved to `docs/locales/en-US/`, Vietnamese from `docs/locales/vi/` to `docs/locales/vi-VN/`. The English `README.md` stays at the repository root.

### Fixed
- Release workflow: create the release as a draft, upload the zips with retries, then publish. Uploading right after creating a release could fail with HTTP 404 and leave a draft without assets.
- Release assets get distinct names (`<skill>-skill.zip`, `<plugin>-plugin.zip`); skill and plugin zips with the same file name used to overwrite each other.

## [0.2.4] - 2026-11-26

### Added
- Release workflow (`.github/workflows/release.yml`): pushing a `vX.Y.Z` tag checks the tag against `pyproject.toml` and `CHANGELOG.md`, runs validation and tests, builds the zips, and publishes a GitHub release with them attached.
- `scripts/release_notes.py`: prints a version's CHANGELOG section as release notes, and checks a tag before release.
- Translated documentation under `docs/locales/<lang>/`, starting with Vietnamese (`docs/locales/vi/`: README, skill authoring, plugin distribution), with a language switch at the top of each file. English stays the source of truth.
- README header: language switch with flags, release / skills / platforms / Python / license badges, CI / stars / last-commit badges, and a hero image. A test keeps the release badge in sync with `pyproject.toml`.
- `docs/plugin-distribution.md` restored and updated (GitHub owner, plugin zips, release steps).
- `tests/test_docs.py`: every locale translates every English doc, and local links in docs resolve.
- `product-requirements/references/example-prd.md`: a complete small-feature PRD for calibrating depth.
- `tests/behavior-cases.json` for `product-requirements`, checked by `scripts/validate.py`.
- More trigger cases, including near-miss negatives (ADR, release notes, technical design).

### Changed
- `product-requirements` SKILL.md slimmed to a router: short First reply rules, one-line workflow steps that point to references, no duplicated loop content.
- `collaborative-loop.md` split: choice tools, multi-select, fallback and answer handling move to `references/asking-decisions.md`; Mermaid rules move to `references/diagrams.md`. Host tool names now appear in one table only.
- Conflicting rules unified: one blocking decision per turn, batch up to 3 only when independent; fast mode defined once.
- `docs/skill-authoring.md` restored and extended (router principle, one rule per place, split references by moment, examples, behavior cases).

## [0.2.3] and earlier

### Added
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
