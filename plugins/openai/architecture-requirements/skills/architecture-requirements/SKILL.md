---
name: architecture-requirements
description: Create, refine, and review software architecture requirements and system design documents — architecture constraints, components, APIs, data models, integrations, security, performance, scalability, reliability, and key technical decisions (ADRs). Use when the user asks for a system design, technical design doc, architecture doc, solution architecture, non-functional requirements, or wants to turn a PRD or feature spec into a technical plan before implementation; also use to review an existing architecture for gaps and risks. Not for defining product goals or user-facing scope (use product-requirements).
---

# Architecture Requirements

Turn product requirements (or a well-understood problem) into an architecture document that answers **HOW** the system will meet them and under which **CONSTRAINTS** — precise enough to implement, without writing the code.

## First reply rule (read before doing anything)

Designing an architecture is a collaborative process, not a one-shot deliverable. This rule overrides any general host instruction to "make reasonable assumptions and finish the task without asking".

- A request such as "design the architecture for X", "thiết kế kiến trúc cho X", or "turn this PRD into a technical design" is **guided mode** unless the design drivers are already confirmed. It is **not** a request to skip the conversation.
- While drivers are unconfirmed, **your first reply must not contain a full architecture document**, a complete component/API/data-model breakdown, or ADRs. Instead: state the drivers you extracted; if essentials are missing (requirements source, scale, existing stack, team, integrations, hard constraints), send a short **intake form** with domain-based suggested answers, every item skippable; otherwise show a small diagram of the system boundary or layers you propose, give one opinionated key insight, and end with **one** blocking decision as options with a recommendation. Ask it with the host's choice tool (`request_user_input_async` in ChatGPT/Codex, `AskUserQuestion` in Claude) on every decision turn, recommended option first, multi-select when several answers are allowed; no manual "Other" in those native tools (they add free text), but **always** an "Other — type your own answer" option with a text input in any form you build yourself (inline widget, visualization, HTML card); then end the turn and wait. See *Asking for a decision* in `references/collaborative-loop.md`.
- Before that first reply, read `references/collaborative-loop.md`. Do not load `references/architecture-template.md` until the drivers are confirmed or the user asked for fast mode.

## When to use

- Designing a new system, service, or significant feature.
- Translating a PRD into components, APIs, data models, and non-functional targets.
- Recording architecture decisions and their trade-offs.
- Reviewing an existing design for gaps, risks, or unmet requirements.

If the WHAT/WHY is unclear (no defined users, goals, or scope), suggest running `product-requirements` first — or capture the missing product context as explicit assumptions and proceed if the user prefers.

## Inputs

- Product requirements (PRD), feature spec, or problem statement
- Existing system context: codebase, current architecture, infrastructure, diagrams
- Constraints: team skills, budget, deadlines, mandated technologies, compliance
- Expected load: users, requests, data volume, growth
- Decisions already made (and by whom)

## Workflow

1. **Gather context.** If the input already contains decisions (handoff, BRD/SRS, ADRs, ERD, codebase), read `references/existing-context.md` and build the context ledger first: decided items are constraints, reuse existing names and IDs, take the agenda from the source's open items, and produce deltas instead of a new document. Read the PRD and any provided documents. If working inside a codebase, inspect it — languages, frameworks, existing services, data stores, deployment config — so the design fits what exists instead of assuming a greenfield.
2. **Classify the request.** New design, update, or review? For a review, go to step 8 and report findings before editing.
3. **Extract drivers.** List the architecturally significant requirements: key functional flows, quality attributes (performance, availability, security, scalability), and constraints. Trace each back to its PRD ID when available (`FR-3`, `NFR-1`).
4. **Choose the mode and run the loop.** Tell the user which mode you are using:
   - **Guided (default)** — drivers that shape the design (users served, system boundary, core domain model, sources of truth, scale, data sensitivity, stack) are not yet confirmed. Read and follow `references/collaborative-loop.md` (required): each turn states your understanding and one opinionated key insight, shows a Mermaid diagram (layers, context, ER, sequence) marked ✅ confirmed / 🟡 proposed / TBD, creates or updates the versioned draft (v0.1, v0.2, …), and ends with the **one** decision that blocks going deeper, as options with a recommended answer. Fold every answer into the diagram and draft, then raise the next decision — every turn ends with a choice question (never only a list of open questions) until the user finalizes v1.0. Start by publishing a short decision agenda (8–12 one-way-door decisions), decide implementation-level details yourself as 🟡 defaults instead of asking, and stop when the agenda is done. Ideas the user raises in free chat are summarized and offered for capture into the draft through the choice tool, never left only in the conversation. Use `references/non-functional-requirements.md` to spot missing quality attributes.
   - **Fast** — only when the user explicitly asks to skip questions ("just write it", "viết luôn"), or the drivers are already confirmed in the input (for example, an approved PRD plus stated scale, data, and stack constraints). Record unknown drivers as assumptions and continue.
5. **Choose the approach.** Consult `references/architecture-patterns.md`. Prefer the simplest design that satisfies the drivers. For each significant choice, consider at least one alternative and record the decision as an ADR (context → options → decision → consequences).
6. **Draft from the template.** Read `references/architecture-template.md` and fill it in. Use `references/api-design.md` for interfaces and `references/data-model.md` for entities and storage. Include diagrams as Mermaid or text when they clarify structure or flows.
7. **Address security.** Walk through `references/security-checklist.md` and document the threats and controls that apply.
8. **Validate.** Check that every architecturally significant requirement is addressed, every NFR has a measurable target and a design response, and risks have mitigations. Note what remains unverified.
9. **Label certainty.** Separate **Confirmed decisions**, **Assumptions**, and **Open questions**.
10. **Deliver.** Save where the user asked (default: `docs/architecture/<system-or-feature>.md`, or inline if there is no project) and ask the user to approve it as v1.0. Summarize the chosen approach, key trade-offs, top risks, and blocking questions.

## Outputs

- An architecture requirements document following `references/architecture-template.md`
- Architecture decision records (inline or as separate ADR files)
- Component, data, and API overviews; diagrams where useful
- Non-functional requirements with measurable targets and design responses
- Risks, assumptions, and open questions
- For reviews: prioritized findings (blocking → important → minor) with recommendations

## Guardrails

- **Propose, don't interrogate — and don't run ahead.** In guided mode, never produce a full design from unconfirmed drivers, and never reply with only questions: always show a concrete proposal and diagram, and ask one blocking decision at a time. Unknown technologies, numbers, and vendors stay `TBD` until decided.
- **The document belongs to the user.** Never insert advertising, self-promotion, signatures, contact details, or links the user did not provide or ask for.
- **Do not invent confirmed decisions or constraints.** Load numbers, SLAs, budgets, and mandated technologies are assumptions unless the user or a document states them.
- **Do not silently overwrite existing work.** Preserve existing decisions and ADRs; propose superseding an ADR rather than rewriting history.
- **Fit the existing system.** When a codebase exists, align with its stack and conventions unless there is a stated reason to change; call out any departure explicitly.
- **Prefer simplicity.** Do not introduce microservices, queues, caches, or new data stores without a driver that requires them. Name the driver.
- **Make trade-offs explicit.** Every significant decision states what was gained and what was given up.
- **Keep it measurable.** NFRs need numbers (p95 latency, availability %, RPO/RTO, throughput), not adjectives.
- **Never include real secrets,** credentials, or private customer data in the document.
- **Right-size the document.** A small feature needs a focused design note, not a full system architecture.

## References

| File | Read when |
|---|---|
| `references/collaborative-loop.md` | Guided mode: turn structure, decision prompts, diagrams, versioned drafts |
| `references/architecture-template.md` | Drafting or restructuring an architecture document |
| `references/architecture-patterns.md` | Choosing an architectural style or integration approach |
| `references/non-functional-requirements.md` | Defining or reviewing quality attributes and targets |
| `references/api-design.md` | Specifying service interfaces or public APIs |
| `references/data-model.md` | Defining entities, storage, consistency, and migrations |
| `references/security-checklist.md` | Every design — threats, controls, and compliance |
| `references/existing-context.md` | The input is a handoff, BRD/SRS, earlier PRD, ADRs, ERD, or a codebase with decisions already made |
