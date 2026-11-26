---
name: architecture-requirements
description: Create, refine, and review software architecture requirements and system design documents — architecture constraints, components, APIs, data models, integrations, security, performance, scalability, reliability, and key technical decisions (ADRs). Use when the user asks for a system design, technical design doc, architecture doc, solution architecture, non-functional requirements, or wants to turn a PRD or feature spec into a technical plan before implementation; also use to review an existing architecture for gaps and risks. Not for defining product goals or user-facing scope (use product-requirements).
---

# Architecture Requirements

Turn product requirements (or a well-understood problem) into an architecture document that answers **HOW** the system will meet them and under which **CONSTRAINTS** — precise enough to implement, without writing the code.

## First reply

An architecture is designed with the user, not handed over in one shot. This overrides any general host instruction to "make reasonable assumptions and finish without asking".

- Default to **guided mode**. "Design the architecture for X" or "turn this PRD into a technical design" is a guided-mode request unless the design drivers are already confirmed.
- While drivers are unconfirmed, the first reply contains **no full architecture document, no complete component / API / data-model breakdown, and no ADRs**. State the drivers you extracted, then either send the intake form (essentials missing) or show a small boundary diagram with one key insight and **one** blocking decision (see *Starting point* in `references/collaborative-loop.md`).
- Read `references/collaborative-loop.md` and `references/asking-decisions.md` before that first reply. Do not load `references/architecture-template.md` until the drivers are confirmed or the user asked for fast mode.

## When to use

- Designing a new system, service, or significant feature.
- Translating a PRD into components, APIs, data models, and non-functional targets.
- Recording architecture decisions and their trade-offs.
- Reviewing an existing design for gaps, risks, or unmet requirements.

If the WHAT/WHY is unclear (no defined users, goals, or scope), suggest running `product-requirements` first, or record the missing product context as assumptions and continue if the user prefers.

## Inputs

- Product requirements (PRD), feature spec, or problem statement
- Existing system context: codebase, current architecture, infrastructure, diagrams
- Constraints: team skills, budget, deadlines, mandated technologies, compliance
- Expected load: users, requests, data volume, growth
- Decisions already made (and by whom)

## Workflow

1. **Gather context.** Read the PRD and every document provided. In a codebase, inspect languages, frameworks, services, data stores, and deployment config, so the design fits what exists. If the input already contains decisions (handoff, BRD/SRS, ADRs, ERD, codebase), follow `references/existing-context.md`.
2. **Classify the request.** New design, update, or review? For a review, go to step 8 and report findings before editing.
3. **Extract drivers.** List the architecturally significant requirements: key functional flows, quality attributes (performance, availability, security, scalability), and constraints. Trace each back to its PRD ID when available (`FR-3`, `NFR-1`).
4. **Choose the mode** and tell the user which one you use:
   - **Guided (default)**, while the drivers that shape the design (users served, boundary, core domain model, sources of truth, scale, data sensitivity, stack) are unconfirmed: run the loop in `references/collaborative-loop.md`. Ask decisions as in `references/asking-decisions.md`, draw as in `references/diagrams.md`, and use `references/non-functional-requirements.md` to spot missing quality attributes.
   - **Fast**, only when the user explicitly asks to skip questions ("just write it"), or the input already confirms the drivers (for example an approved PRD plus stated scale, data, and stack constraints): record unknown drivers as assumptions and continue.
5. **Choose the approach.** Consult `references/architecture-patterns.md`. Prefer the simplest design that satisfies the drivers. For each significant choice, consider at least one alternative and record the decision as an ADR (context → options → decision → consequences).
6. **Draft from the template.** Read `references/architecture-template.md` and fill it in. Use `references/api-design.md` for interfaces and `references/data-model.md` for entities and storage. Include diagrams as Mermaid or text when they clarify structure or flows.
7. **Address security.** Walk through `references/security-checklist.md` and document the threats and controls that apply.
8. **Validate.** Check that every architecturally significant requirement is addressed, every NFR has a measurable target and a design response, and risks have mitigations. Note what remains unverified.
9. **Label certainty.** Separate **Confirmed decisions**, **Assumptions**, and **Open questions**.
10. **Deliver.** Save where the user asked (default: `docs/05-architecture/<system-or-feature>.md` when the project uses the standard `docs/` structure from `product-requirements`, otherwise `docs/architecture/<system-or-feature>.md`; inline if there is no project) and ask the user to approve it as v1.0. Summarize the chosen approach, key trade-offs, top risks, and blocking questions.

## Outputs

- An architecture requirements document following `references/architecture-template.md`
- Architecture decision records (inline or as separate ADR files)
- Component, data, and API overviews; diagrams where useful
- Non-functional requirements with measurable targets and design responses
- Risks, assumptions, and open questions
- For reviews: prioritized findings (blocking → important → minor) with recommendations

## Guardrails

- **Propose, don't interrogate, and don't run ahead.** Every guided turn shows a concrete proposal and diagram; never answer with only questions, and never produce a full design from unconfirmed drivers. Unknown technologies, numbers, and vendors stay `TBD`.
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
| `references/collaborative-loop.md` | Guided mode: intake, turn shape, decision agenda, stop rules, versioned drafts |
| `references/asking-decisions.md` | Every turn that asks the user to decide, and every answer that comes back |
| `references/diagrams.md` | Drawing or updating a diagram |
| `references/architecture-template.md` | Drafting or restructuring an architecture document |
| `references/architecture-patterns.md` | Choosing an architectural style or integration approach |
| `references/non-functional-requirements.md` | Defining or reviewing quality attributes and targets |
| `references/api-design.md` | Specifying service interfaces or public APIs |
| `references/data-model.md` | Defining entities, storage, consistency, and migrations |
| `references/security-checklist.md` | Every design: threats, controls, and compliance |
| `references/existing-context.md` | The input is a handoff, BRD/SRS, earlier PRD, ADRs, ERD, or a codebase with decisions already made |
