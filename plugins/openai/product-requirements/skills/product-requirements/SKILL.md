---
name: product-requirements
description: Create, refine, and review product requirements documents (PRDs) for software products and features — goals, target users, user journeys, functional requirements, acceptance criteria, success metrics, scope, and rollout. Use when the user asks for a PRD, product spec, feature spec, requirements doc, user stories with acceptance criteria, or wants to turn a product idea, meeting notes, or a feature request into actionable, testable requirements; also use to review or tighten an existing requirements document. Not for system design or technical architecture (use architecture-requirements).
---

# Product Requirements

Turn a product idea or feature request into a clear, testable PRD that answers **WHAT** is being built and **WHY**, without prescribing **HOW**.

The PRD is **one Markdown file**, `docs/PRD.md`: shared sections for actors, domain, rules, and decisions, plus one subsection per feature. It uses the sections and conventions of the starter kit, read live from the `vaultia-templates` repository with `assets/docs-starter/` as the bundled fallback. At v1.0 the file is returned in the chat, and the user can choose to export it to the full `docs/` structure (zip). A project that already has that structure keeps working in it, one file per feature (`references/docs-structure.md`).

## First reply

A PRD is built with the user, not handed over in one shot. A long document built on unexamined guesses looks finished but is mostly invented.

- Default to **guided mode**. "Write a PRD for X" is a guided-mode request, not a request to skip the conversation.
- If the input is vague or partial, the first reply contains **no PRD, no section outline, and no requirements table**. Send the intake form instead (see *Starting point* in `references/collaborative-loop.md`).
- Read `references/collaborative-loop.md` and `references/asking-decisions.md` before that first reply.
- Do not create the PRD file until the intake is answered; then follow `references/docs-structure.md` for where it goes.
- Use **fast mode** only when the user explicitly asks to skip questions ("just write it", "draft now without asking"), or when the input already confirms all essentials: problem, users, goal, MVP scope, metric, and constraints.

## When to use

- Writing a new PRD or feature spec from an idea, notes, a ticket, or a conversation.
- Refining or extending an existing requirements document.
- Reviewing a PRD for gaps, ambiguity, or untestable requirements.
- Producing user stories and acceptance criteria for a defined scope.

The PRD includes a **conceptual** domain model: business objects, relationships, lifecycles, and business rules with worked examples. Database-level design (tables, columns, keys, storage), APIs, and system design belong to `architecture-requirements`; hand off once the WHAT/WHY is stable. If the user asks for an ERD here, give the conceptual one and offer the handoff for the physical one.

## Workflow

1. **Gather context.** Read every document, file, or note the user provided. If the project already has `docs/PRD.md` or the `docs/` structure, read it first (`references/docs-structure.md`). If the input already contains decisions (handoff, BRD/SRS, ADRs, ERD, codebase), follow `references/existing-context.md`. When editing an existing PRD, read all of it before changing anything.
2. **Classify the request:** new document, update, or review. For a review, go to step 8 and report findings before editing.
3. **Choose the mode** and tell the user which one you use (they can switch at any time): guided (default) → step 4; fast → list gaps with `references/discovery-questions.md`, record them as assumptions and open questions, then go to step 6.
4. **Run the collaborative loop** in `references/collaborative-loop.md`: propose → diagram → draft vN → ask one decision → update. The draft is the single PRD file, placed as described in `references/docs-structure.md`. Ask decisions as described in `references/asking-decisions.md`, and draw diagrams as described in `references/diagrams.md`.
5. **Close the loop** when problem, target user, MVP scope, primary journey, primary metric, and hard constraints are confirmed. Tell the user you are completing the remaining sections.
6. **Complete the document.** Each feature subsection follows the starter kit's `03-functional-specs/_template.md` (the bundled one is `assets/docs-starter/03-functional-specs/_template.md`); update the shared sections it depends on (feature list, domain model, business rules, decisions, open questions) as listed in `references/docs-structure.md`. Extend the existing draft and keep its version history. Omit sections that do not apply; keep the order. `references/example-feature-spec.md` shows the expected depth.
7. **Write acceptance criteria** for each functional requirement, following `references/acceptance-criteria.md`.
8. **Quality check** with `references/quality-checklist.md`. Fix what you can; list the rest as open questions.
9. **Scope checklist.** Let the user tick what ships in this release and check the dependencies of the selection, as in *Scope checklist* in `references/collaborative-loop.md` (fast mode: tick the recommended set and do not ask). Then ask the user to approve v1.0.
10. **Deliver v1.0** as in *Delivering v1.0* in `references/docs-structure.md`: return the single file in the chat, summarize key decisions, top assumptions, and blocking open questions, then offer: keep the single file, export to the `docs/` template (zip), hand off to `architecture-requirements`, or add the next feature. Export only when the user chooses it.

## Outputs

- One PRD file, `docs/PRD.md` (returned in the chat at v1.0), with acceptance criteria for each functional requirement, product-wide non-functional requirements and the SLA decision, and a scope checklist of what ships in this release
- On request only: the export to the `docs/` template, as a zip in chat hosts
- In a project that already has the `docs/` structure: the feature spec `docs/03-functional-specs/F<nn>-<slug>.md` and the shared files it changed
- Confirmed decisions separated from assumptions and open questions
- For reviews: findings ranked Blocking → Important → Minor, each with a suggested fix

## Guardrails

- **Propose, don't interrogate, and don't run ahead.** Every guided turn shows a concrete proposal; never answer with only questions, and never jump from a one-line idea to a full PRD.
- **Never invent.** Unknowns are `TBD`. Inferences and "you decide" answers are assumptions until the user confirms them. Never present a guess as a decision, a metric target as agreed, or a stakeholder as having approved something.
- **Challenge, then respect the decision.** Push back on weak problems, oversized scope, or unmeasurable goals with a sharper option; once the user decides, record it and move on.
- **Preserve existing work.** Describe what changed. Ask before deleting or restructuring large sections.
- **Stay at WHAT/WHY.** Name technology only when it is a genuine business constraint; note other technical points for the architecture phase.
- **No UI mockups.** Describe screens, forms, and fields with tables (field, type, rule), not rendered previews: mockups are slow to generate and belong to `ui-ux-design`. Offer that handoff when the user wants to see screens.
- **Keep requirements testable.** Replace vague words ("fast", "easy", "intuitive", "secure") with measurable statements, or flag them.
- **Use stable IDs** as defined in the conventions file (`F01`, `BR-001`, `D-001`, `Q-001`, and local `FR-1`, `AC-1.1`). Never renumber or reuse an ID.
- **Right-size.** A small feature gets a short spec. Shared knowledge is written once in the shared sections, not repeated in every feature.
- **The document belongs to the user.** No advertising, signatures, contact details, or links the user did not provide.
- **Match the user's language** for document content, keeping IDs and section structure unchanged.

## References

| File | Read when |
|---|---|
| `references/collaborative-loop.md` | Guided mode: intake, turn shape, decision agenda, stop rules, versioned drafts, scope checklist before v1.0 |
| `references/asking-decisions.md` | Every turn that asks the user to decide, and every answer that comes back |
| `references/diagrams.md` | Drawing or updating a diagram |
| `references/discovery-questions.md` | Finding missing information or preparing questions |
| `references/docs-structure.md` | Creating the first draft: getting the starter kit, where the file goes, the single-file layout, delivering v1.0, exporting to the `docs/` template |
| `assets/docs-starter/` | Bundled fallback copy of the starter kit; read the live one first, as in `references/docs-structure.md` |
| `references/example-feature-spec.md` | Calibrating the depth and tone of a finished feature spec |
| `references/acceptance-criteria.md` | Writing or reviewing acceptance criteria |
| `references/quality-checklist.md` | Final check before delivery, or reviewing a PRD |
| `references/existing-context.md` | The input is a handoff, BRD/SRS, earlier PRD, ADRs, ERD, or codebase with decisions already made |
