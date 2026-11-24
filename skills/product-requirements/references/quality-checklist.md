# Product Requirements Quality Checklist

Run before delivering a PRD, and use as the rubric when reviewing one. Report review findings as **Blocking**, **Important**, or **Minor**.

## Completeness

- [ ] Problem statement is in user terms and supported by evidence (or the evidence gap is flagged).
- [ ] Primary users are named; out-of-scope users are explicit when ambiguous.
- [ ] Goals describe outcomes, not features.
- [ ] Non-goals are listed.
- [ ] Every main user journey has functional requirements.
- [ ] Every functional requirement has acceptance criteria.
- [ ] Success metrics have a baseline (or "unknown"), a target, a timeframe, and a measurement method.
- [ ] Scope, rollout, and dependencies are stated.
- [ ] Risks have mitigations.
- [ ] Every success metric can be computed from named events or an existing data source.
- [ ] Risky launches state a kill switch or rollback path.

## Clarity

- [ ] Each requirement states a single behavior.
- [ ] No ambiguous terms left unqualified: *fast, easy, simple, intuitive, secure, scalable, flexible, robust, user-friendly, etc., as needed, appropriate*.
- [ ] Terms are used consistently; domain terms are defined in a glossary when needed.
- [ ] Requirements use "shall" (mandatory) consistently; optional behavior uses priority, not wording.

## Testability

- [ ] Every requirement can be verified by a test, demo, inspection, or measurement.
- [ ] Acceptance criteria cover unhappy paths, not only the happy path.
- [ ] Every listed edge case (`E-n`) maps to at least one acceptance criterion.
- [ ] Numbers and limits are concrete where they affect behavior.

## Traceability

- [ ] Stable IDs are used: `G-`, `J-`, `FR-`, `AC-`, `NFR-`, `M-`, `D-`, `A-`, `Q-`.
- [ ] Each functional requirement links to a journey or goal.
- [ ] No orphan requirements (requirements that serve no goal).
- [ ] No goal without at least one requirement or metric.

## Scope discipline

- [ ] Requirements describe WHAT and WHY, not HOW (no unnecessary technology or design choices).
- [ ] Priorities are assigned; not everything is "Must".
- [ ] The v1 scope is the smallest version that achieves the goal.

## Honesty

- [ ] Confirmed decisions, assumptions, and open questions are clearly separated.
- [ ] No invented stakeholder approvals, data, or metric targets presented as fact.
- [ ] Open questions have an owner or a "needed by" signal when known.
- [ ] No decision depends on an open question: scope, priorities, and metrics are not marked confirmed while the primary user or problem is still TBD.

## Hygiene

- [ ] No empty placeholder sections (appendix items that only say "TBD") — omit them or turn them into open questions with an owner.
- [ ] No promotional content, signatures, contact links, or third-party URLs the user did not provide.

## Common defects

| Defect | Fix |
|---|---|
| Solution disguised as a requirement ("Use Redis for caching") | Restate the need ("Search results appear within 1 s at p95") and move the idea to architecture notes. |
| Compound requirement ("Users can create, edit, and share reports") | Split into separate FRs. |
| Untestable adjective ("intuitive UI") | Replace with a measurable criterion or a usability-test target. |
| Missing failure behavior | Add ACs for errors, limits, and permission denials. |
| Everything is "Must" | Force-rank; ask what ships if time is cut by half. |
| Metric without baseline | Record "baseline unknown" and add a question to measure it. |
| Scope confirmed while the target user is TBD | Downgrade scope to proposed; resolve the user decision first. |
| Edge case listed but never specified | Add an AC that states the system's behavior in that case. |
