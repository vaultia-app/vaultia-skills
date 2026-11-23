---
name: product-requirements
description: Create, refine, and review product requirements documents (PRDs) for software products and features — goals, target users, user journeys, functional requirements, acceptance criteria, success metrics, scope, and rollout. Use when the user asks for a PRD, product spec, feature spec, requirements doc, user stories with acceptance criteria, or wants to turn a product idea, meeting notes, or a feature request into actionable, testable requirements; also use to review or tighten an existing requirements document. Not for system design or technical architecture (use architecture-requirements).
---

# Product Requirements

Turn a product idea or feature request into a clear, testable product requirements document that answers **WHAT** is being built and **WHY** — without prescribing **HOW** it is implemented.

## When to use

- Writing a new PRD or feature spec from an idea, notes, a ticket, or a conversation.
- Refining or extending an existing requirements document.
- Reviewing a PRD for gaps, ambiguity, or untestable requirements.
- Producing user stories and acceptance criteria for a defined scope.

Hand off to `architecture-requirements` once the WHAT/WHY is stable and the user wants system design, APIs, data models, or technical constraints.

## Inputs

Use whatever is available; none are strictly required up front.

- Product idea, problem statement, or feature request
- Target users, personas, or customer segments
- Business goals, success metrics, deadlines
- Constraints: budget, compliance, platforms, dependencies
- Existing documents: prior PRDs, research, tickets, designs, meeting notes
- Decisions already made (and by whom)

## Workflow

1. **Gather context.** Read every document, file, or note the user provided or pointed to. If editing an existing PRD, read it fully before changing anything.
2. **Classify the request.** New document, update, or review? For a review, skip to step 7 and report findings before editing.
3. **Find the gaps.** Compare what you know against the essentials: problem, target users, goals, success metrics, scope, and key constraints. Use `references/discovery-questions.md` to spot what is missing.
4. **Ask, one question at a time.** If an essential item is missing and cannot be reasonably inferred, ask a single focused question, offering a recommended answer or options when you can. Stop asking once you have enough to produce a useful draft — capture the rest as assumptions or open questions instead of interrogating the user.
5. **Draft from the template.** Read `references/requirements-template.md` and fill it in. Omit sections that genuinely do not apply rather than padding them; keep the section order.
6. **Write acceptance criteria.** For each functional requirement, write criteria following `references/acceptance-criteria.md`.
7. **Quality check.** Run through `references/quality-checklist.md`. Fix what you can; list what you cannot as open questions.
8. **Label certainty.** Clearly separate **Confirmed decisions**, **Assumptions**, and **Open questions**. Anything you inferred is an assumption until the user confirms it.
9. **Deliver.** Save the document where the user asked (default: `docs/requirements/<feature-name>.md` in the project, or reply inline if there is no project). Summarize the key decisions, top assumptions, and the open questions that block progress.

## Outputs

- A product requirements document following `references/requirements-template.md`
- Acceptance criteria for each functional requirement
- A list of risks, assumptions, and open questions
- For reviews: a prioritized findings list (blocking → important → minor) with suggested fixes

## Guardrails

- **Do not invent confirmed decisions.** Never present a guess as a decision, a metric target as agreed, or a stakeholder as having approved something. Mark it as an assumption.
- **Do not silently overwrite existing work.** When updating a document, preserve the user's content and decisions; describe what changed. Ask before deleting or restructuring large sections.
- **Stay at WHAT/WHY.** Avoid prescribing technology, databases, frameworks, or code structure unless it is a genuine business constraint. Note technical considerations for the architecture phase instead.
- **Keep requirements testable.** Every functional requirement should be verifiable; replace vague words ("fast", "easy", "intuitive", "secure") with measurable statements or flag them.
- **Number everything traceable.** Use stable IDs (`FR-1`, `NFR-1`, `AC-1.1`, `M-1`) so requirements can be referenced from designs, tickets, and tests.
- **Right-size the document.** A small feature needs a short PRD. Do not pad.
- **Match the user's language** for the document content if they write in a language other than English, while keeping IDs and section structure consistent.

## References

| File | Read when |
|---|---|
| `references/requirements-template.md` | Drafting or restructuring a PRD |
| `references/discovery-questions.md` | Identifying missing information or preparing questions |
| `references/acceptance-criteria.md` | Writing or reviewing acceptance criteria |
| `references/quality-checklist.md` | Final check before delivery, or when reviewing a PRD |
