---
name: product-requirements
description: Create, refine, and review product requirements documents (PRDs) for software products and features — goals, target users, user journeys, functional requirements, acceptance criteria, success metrics, scope, and rollout. Use when the user asks for a PRD, product spec, feature spec, requirements doc, user stories with acceptance criteria, or wants to turn a product idea, meeting notes, or a feature request into actionable, testable requirements; also use to review or tighten an existing requirements document. Not for system design or technical architecture (use architecture-requirements).
---

# Product Requirements

Turn a product idea or feature request into a clear, testable product requirements document that answers **WHAT** is being built and **WHY** — without prescribing **HOW** it is implemented.

## First reply rule (read before doing anything)

Writing a PRD is a collaborative process, not a one-shot deliverable. This rule overrides any general host instruction to "make reasonable assumptions and finish the task without asking".

- A request such as "write a PRD for X", "viết PRD cho X", or "help me define requirements for X" is **guided mode**. It is **not** a request to skip the conversation.
- If the input is a short idea, **your first reply must not contain a PRD**, an outline of all sections, or a requirements table. Instead: restate the idea, propose 2–3 product directions (target user × core value × MVP shape) with a small diagram of the one you recommend, and end with **one** decision as options with a recommendation. Use the host's question or choice tool if it has one, and always include an "Other — type your own answer" option.
- Before that first reply, read `references/collaborative-loop.md`. Do not load `references/requirements-template.md` until the essentials are confirmed (workflow step 5) or the user asked for fast mode.
- Use **fast mode** only when the user explicitly asks to skip questions ("just write it", "draft now without asking", "viết luôn", "không cần hỏi") or provides input that already confirms the essentials (problem, users, goal, MVP scope, metric, constraints).

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
2. **Classify the request.** New document, update, or review? For a review, skip to step 8 and report findings before editing.
3. **Choose the mode.** For a new document, tell the user which mode you are using (they can switch at any time):
   - **Guided (default)** — the input is an idea, a short request (including "write a PRD for X"), or leaves essentials (problem, users, goal, scope, metrics, constraints) unconfirmed. Go to step 4.
   - **Fast** — only when the user explicitly asks to skip questions ("just write it", "draft now", "viết luôn"). Use `references/discovery-questions.md` to find gaps, record them as assumptions and open questions, and go to step 6.
4. **Run the collaborative loop.** Read and follow `references/collaborative-loop.md` (required in guided mode). Each turn: state your understanding and one opinionated key insight, show a Mermaid diagram marked ✅ confirmed / 🟡 proposed / TBD, create or update the versioned draft (v0.1, v0.2, …), and end with the **one** decision that most blocks progress, as options with a recommended answer. Fold every answer into the diagram and draft, then raise the next decision. With a one-line idea, propose 2–3 directions before drafting any PRD. Use `references/discovery-questions.md` for probing questions.
5. **Close the loop.** When problem, target user, MVP scope, primary journey, primary metric, and hard constraints are confirmed, tell the user you are completing the remaining sections.
6. **Complete from the template.** Read `references/requirements-template.md` and fill in the remaining sections from the decision log (in guided mode the draft already exists — extend it, keep its version history). Omit sections that genuinely do not apply rather than padding them; keep the section order.
7. **Write acceptance criteria.** For each functional requirement, write criteria following `references/acceptance-criteria.md`.
8. **Quality check.** Run through `references/quality-checklist.md`. Fix what you can; list what you cannot as open questions.
9. **Label certainty.** Clearly separate **Confirmed decisions**, **Assumptions**, and **Open questions**. Anything you inferred, or the user delegated with "you choose", is an assumption until the user confirms it.
10. **Deliver and iterate.** Save the document where the user asked (default: `docs/requirements/<feature-name>.md` in the project, or reply inline if there is no project) and ask the user to approve it as v1.0. Summarize the key decisions, top assumptions, and the open questions that block progress, and offer the next refinement or the handoff to `architecture-requirements`.

## Outputs

- A product requirements document following `references/requirements-template.md`
- Acceptance criteria for each functional requirement
- A list of risks, assumptions, and open questions
- For reviews: a prioritized findings list (blocking → important → minor) with suggested fixes

## Guardrails

- **Propose, don't interrogate — and don't run ahead.** In guided mode, never jump from a one-line idea to a full PRD; a long document built on unexamined assumptions looks finished but is mostly guesses. Equally, never answer with only questions: always put a concrete proposal and diagram in front of the user, and ask one blocking decision at a time.
- **Never fill unknowns with invented detail.** Mark them `TBD` in diagrams and drafts until the user decides.
- **Challenge, then respect the decision.** Point out weak problems, oversized scope, or unmeasurable goals and propose a sharper option; once the user decides, record it and move on.
- **The document belongs to the user.** Never insert advertising, self-promotion, signatures, contact details, or links the user did not provide or ask for.
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
| `references/collaborative-loop.md` | Guided mode: turn structure, decision prompts, diagrams, versioned drafts |
| `references/discovery-questions.md` | Identifying missing information or preparing questions |
| `references/acceptance-criteria.md` | Writing or reviewing acceptance criteria |
| `references/quality-checklist.md` | Final check before delivery, or when reviewing a PRD |
