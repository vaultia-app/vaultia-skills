# Product Requirements Quality Checklist

Run before delivering a PRD or feature spec, and use as the rubric when reviewing one. Report review findings as **Blocking**, **Important**, or **Minor**.

## Completeness

- [ ] Problem statement is in user terms and supported by evidence (or the evidence gap is flagged).
- [ ] Primary users are named; out-of-scope users are explicit when ambiguous.
- [ ] Goals describe outcomes, not features.
- [ ] Non-goals are listed.
- [ ] Every main user journey has functional requirements.
- [ ] Every functional requirement has acceptance criteria.
- [ ] Business objects this feature uses are in the domain model (`01-business/02-domain-model.md` in a `docs/` project) with relationships and lifecycles (conceptual only: no column types or storage).
- [ ] Every calculation or money rule (`BR-xxx`) has a worked example, rounding, and boundary behavior.
- [ ] Success metrics have a baseline (or "unknown"), a target, a timeframe, and a measurement method.
- [ ] Product-wide non-functional requirements are measurable as users notice them (performance, availability, security and privacy, accessibility, localization, compliance, data recovery), or marked `N/A` with a reason.
- [ ] The SLA is decided: commitments with targets, or "No SLA" with a reason. A product sold to customers does not leave it `TBD` at v1.0.
- [ ] Scope, rollout, and dependencies are stated.
- [ ] Risks have mitigations.
- [ ] Every success metric can be computed from named events or an existing data source.
- [ ] Risky launches state a kill switch or rollback path.

## Clarity

- [ ] Each requirement states a single behavior.
- [ ] No ambiguous terms left unqualified: *fast, easy, simple, intuitive, secure, scalable, flexible, robust, user-friendly, etc., as needed, appropriate*.
- [ ] Terms are used consistently; terms that could be misread are in the glossary.
- [ ] Requirements use "shall" (mandatory) consistently; optional behavior uses priority, not wording.

## Testability

- [ ] Every requirement can be verified by a test, demo, inspection, or measurement.
- [ ] Acceptance criteria cover unhappy paths, not only the happy path.
- [ ] Every listed edge case (`E-n`) maps to at least one acceptance criterion.
- [ ] Numbers and limits are concrete where they affect behavior.

## Traceability

- [ ] IDs follow `00-overview/03-conventions.md`: global `F`, `G`, `BR`, `NFR`, `W`, `D`, `Q`; local `J`, `E`, `FR`, `AC`, `NFR-L`, `M`, `A`. No ID was renumbered or reused.
- [ ] Each functional requirement links to a journey or goal.
- [ ] No orphan requirements (requirements that serve no goal).
- [ ] No goal without at least one requirement or metric.

## Placement (documentation structure)

- [ ] Single file: sections follow the order in `docs-structure.md`; each feature is an `F<nn>` subsection with a row in *Features and MVP scope*; local IDs are qualified (`F02/FR-1`) outside their own subsection.
- [ ] `docs/` project: the spec is `03-functional-specs/F<nn>-<slug>.md` and has a row in `02-requirements/01-feature-list.md` that links to it.
- [ ] Rules, objects, actors, and terms that other features could use live in the shared sections or files; features reference them by ID instead of repeating them.
- [ ] Every `BR-xxx`, `D-xxx`, and `Q-xxx` a feature mentions exists where it lives, and its *Used by* / *Affects* / *Raised in* column names this feature.
- [ ] Links and anchors resolve.

## Scope discipline

- [ ] Requirements describe WHAT and WHY, not HOW (no unnecessary technology or design choices).
- [ ] Priorities are assigned; not everything is "Must".
- [ ] The v1 scope is the smallest version that achieves the goal.
- [ ] The scope checklist lists every functional requirement once, ticked or not; each unticked line says why and where it goes.
- [ ] No ticked item depends on an unticked one; the primary journey can be completed with the ticked items; every actor in the release has a ticked capability.

## Honesty

- [ ] Confirmed decisions, assumptions, and open questions are clearly separated.
- [ ] No invented stakeholder approvals, data, or metric targets presented as fact.
- [ ] Open questions have an owner or a "needed by" signal when known.
- [ ] No decision depends on an open question: scope, priorities, and metrics are not marked confirmed while the primary user or problem is still TBD.

## Hygiene

- [ ] No empty placeholder sections (items that only say "TBD"): omit them or turn them into open questions with an owner.
- [ ] No template placeholders (`<…>`) left in the delivered files.
- [ ] No promotional content, signatures, contact links, or third-party URLs the user did not provide.

## Common defects

| Defect | Fix |
|---|---|
| Solution disguised as a requirement ("Use Redis for caching") | Restate the need ("Search results appear within 1 s at p95") and move the idea to architecture notes. |
| Compound requirement ("Users can create, edit, and share reports") | Split into separate FRs. |
| Untestable adjective ("intuitive UI") | Replace with a measurable criterion or a usability-test target. |
| Missing failure behavior | Add ACs for errors, limits, and permission denials. |
| Everything is "Must" | Force-rank; ask what ships if time is cut by half. |
| NFRs missing or written as adjectives ("fast", "always available") | Propose measurable 🟡 defaults per category and confirm the ones that matter. |
| Technical targets in the PRD ("p95 300 ms at 200 req/s") | Restate as users notice it; move the technical target to the architecture notes. |
| Metric without baseline | Record "baseline unknown" and add a question to measure it. |
| Scope confirmed while the target user is TBD | Downgrade scope to proposed; resolve the user decision first. |
| Edge case listed but never specified | Add an AC that states the system's behavior in that case. |
