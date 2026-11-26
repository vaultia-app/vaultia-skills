---
name: product-requirements
description: Create, refine, and review product requirements documents (PRDs) for software products and features — goals, target users, user journeys, functional requirements, acceptance criteria, success metrics, scope, and rollout. Use when the user asks for a PRD, product spec, feature spec, requirements doc, user stories with acceptance criteria, or wants to turn a product idea, meeting notes, or a feature request into actionable, testable requirements; also use to review or tighten an existing requirements document. Not for system design or technical architecture (use architecture-requirements).
---

# Product Requirements

Turn a product idea or feature request into a clear, testable PRD that answers **WHAT** is being built and **WHY**, without prescribing **HOW**.

## First reply

A PRD is built with the user, not handed over in one shot. A long document built on unexamined guesses looks finished but is mostly invented.

- Default to **guided mode**. "Write a PRD for X" is a guided-mode request, not a request to skip the conversation.
- If the input is vague or partial, the first reply contains **no PRD, no section outline, and no requirements table**. Send the intake form instead (see *Starting point* in `references/collaborative-loop.md`).
- Read `references/collaborative-loop.md` and `references/asking-decisions.md` before that first reply.
- Do not read `references/requirements-template.md` until the essentials are confirmed (step 6) or fast mode applies.
- Use **fast mode** only when the user explicitly asks to skip questions ("just write it", "draft now without asking"), or when the input already confirms all essentials: problem, users, goal, MVP scope, metric, and constraints.

## When to use

- Writing a new PRD or feature spec from an idea, notes, a ticket, or a conversation.
- Refining or extending an existing requirements document.
- Reviewing a PRD for gaps, ambiguity, or untestable requirements.
- Producing user stories and acceptance criteria for a defined scope.

The PRD includes a **conceptual** domain model: business objects, relationships, lifecycles, and business rules with worked examples. Database-level design (tables, columns, keys, storage), APIs, and system design belong to `architecture-requirements`; hand off once the WHAT/WHY is stable. If the user asks for an ERD here, give the conceptual one and offer the handoff for the physical one.

## Workflow

1. **Gather context.** Read every document, file, or note the user provided. If the input already contains decisions (handoff, BRD/SRS, ADRs, ERD, codebase), follow `references/existing-context.md`. When editing an existing PRD, read all of it before changing anything.
2. **Classify the request:** new document, update, or review. For a review, go to step 8 and report findings before editing.
3. **Choose the mode** and tell the user which one you use (they can switch at any time): guided (default) → step 4; fast → list gaps with `references/discovery-questions.md`, record them as assumptions and open questions, then go to step 6.
4. **Run the collaborative loop** in `references/collaborative-loop.md`: propose → diagram → draft vN → ask one decision → update. Ask decisions as described in `references/asking-decisions.md`, and draw diagrams as described in `references/diagrams.md`.
5. **Close the loop** when problem, target user, MVP scope, primary journey, primary metric, and hard constraints are confirmed. Tell the user you are completing the remaining sections.
6. **Complete from the template** in `references/requirements-template.md`. Extend the existing draft and keep its version history. Omit sections that do not apply; keep the section order. `references/example-prd.md` shows the expected depth.
7. **Write acceptance criteria** for each functional requirement, following `references/acceptance-criteria.md`.
8. **Quality check** with `references/quality-checklist.md`. Fix what you can; list the rest as open questions.
9. **Deliver.** Save to the location the user asked for (default `docs/requirements/<feature-name>.md`, or inline when there is no project). Summarize key decisions, top assumptions, and blocking open questions. Ask the user to approve v1.0, then offer the handoff to `architecture-requirements`.

## Outputs

- A PRD following `references/requirements-template.md`, with acceptance criteria for each functional requirement
- Risks, assumptions, and open questions, separated from confirmed decisions
- For reviews: findings ranked Blocking → Important → Minor, each with a suggested fix

## Guardrails

- **Propose, don't interrogate, and don't run ahead.** Every guided turn shows a concrete proposal; never answer with only questions, and never jump from a one-line idea to a full PRD.
- **Never invent.** Unknowns are `TBD`. Inferences and "you decide" answers are assumptions until the user confirms them. Never present a guess as a decision, a metric target as agreed, or a stakeholder as having approved something.
- **Challenge, then respect the decision.** Push back on weak problems, oversized scope, or unmeasurable goals with a sharper option; once the user decides, record it and move on.
- **Preserve existing work.** Describe what changed. Ask before deleting or restructuring large sections.
- **Stay at WHAT/WHY.** Name technology only when it is a genuine business constraint; note other technical points for the architecture phase.
- **Keep requirements testable.** Replace vague words ("fast", "easy", "intuitive", "secure") with measurable statements, or flag them.
- **Use stable IDs** (`FR-1`, `NFR-1`, `AC-1.1`, `M-1`, `D-1`) so designs, tickets, and tests can reference them.
- **Right-size.** A small feature gets a short PRD.
- **The document belongs to the user.** No advertising, signatures, contact details, or links the user did not provide.
- **Match the user's language** for document content, keeping IDs and section structure unchanged.

## References

| File | Read when |
|---|---|
| `references/collaborative-loop.md` | Guided mode: intake, turn shape, decision agenda, stop rules, versioned drafts |
| `references/asking-decisions.md` | Every turn that asks the user to decide, and every answer that comes back |
| `references/diagrams.md` | Drawing or updating a diagram |
| `references/discovery-questions.md` | Finding missing information or preparing questions |
| `references/requirements-template.md` | Drafting or restructuring a PRD |
| `references/example-prd.md` | Calibrating the depth and tone of a finished PRD |
| `references/acceptance-criteria.md` | Writing or reviewing acceptance criteria |
| `references/quality-checklist.md` | Final check before delivery, or reviewing a PRD |
| `references/existing-context.md` | The input is a handoff, BRD/SRS, earlier PRD, ADRs, ERD, or codebase with decisions already made |
