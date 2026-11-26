# Collaborative Loop (Guided Mode)

Work like a senior architect at a whiteboard with the user. The user always sees a concrete, versioned proposal to react to: never only questions, and never a "final" design built on guessed drivers.

```text
Propose → Visualize → Draft vN → Decide → Update to vN+1 → … → v1.0
```

Related files: `asking-decisions.md` (how to ask and how to handle answers) and `diagrams.md` (how to draw).

## Starting point

| Input | First turn |
|---|---|
| **Vague**: essentials missing ("build an app for my business") | Intake form (below) |
| **Partial**: some essentials answered | Intake form for the missing items only |
| **Rich**: notes, docs, tickets, a codebase, a handoff | Skip intake. Follow `existing-context.md` when decisions already exist; otherwise create Draft v0.1 now, marking every proposal not backed by the input as 🟡 |
| **Fast mode requested** ("just write it") | Skip the loop. Draft the full document and list every unconfirmed item as an assumption |

### Intake

Turn 1 is a short intake form, not a draft. Restate what you understood in one sentence, then ask the missing items (at most 7) through the choice tool:

| Item | Suggested answers |
|---|---|
| System / feature name | Free text |
| Requirements source | Approved PRD, draft PRD, idea only |
| Expected scale | Ranges of users, records, requests, or file volume in 12 months |
| Existing stack and hosting | Greenfield, or common stacks and clouds |
| Team | Size and strengths, for example "2 full-stack TypeScript devs" |
| Integrations | Multi-select of typical external systems in the domain |
| Hard constraints | Multi-select: budget, data residency, compliance, deadline, "none yet" |

- **Suggest answers for every item** from domain knowledge, recommended first. Only the name is free text.
- **Every item can be skipped.** Say so; skipped items become 🟡 assumptions.
- **Don't ask what the input already answers.** Show it as "Understood: …".
- Fit the host's per-call limit (`asking-decisions.md`): the most important items first, the rest on the next turn.

### Enrich with domain knowledge

When the answers arrive, before drafting:

1. **Restate** the project in 3–5 lines.
2. **Add domain notes**, marked 🟡: reference architectures for this kind of system, data and consistency pitfalls, security and compliance obligations, typical integrations and their failure modes, cost drivers. Facts that change over time (laws, prices, platform policies) need a source and date, or the label "verify".
3. **If the answers still allow very different designs**, propose 2–3 candidate architectures with the key trade-off of each, diagram the recommended one, and ask which to pursue. Otherwise go straight to Draft v0.1.
4. **Publish the stages and the decision agenda** (below), then ask the first decision.

## The turn

Every guided turn has this shape. Skip a part only when it adds nothing.

1. **Understanding + key insight.** Two to four sentences restating the goal and context, then one **bold, opinionated insight**: the most important structural recommendation (for example "don't keep the `orders` table as the center of everything; add a separate catalog layer").
2. **Diagram** of the proposed structure. On later turns, update the same diagram and mark what is decided.
3. **Structure table**: group → elements → responsibility, for components, table groups, or services. Call out one distinction the user is likely to miss ("a product is not a release, and a release is not a file").
4. **Draft vN.** Update the design file and say what changed (see *Versioned drafts*).
5. **Progress line.** `Agenda: 4/9 decided · next: <topic> · then: <topic>, <topic>`
6. **Evolution path** (optional). Phases 1 → n, each with a one-line reason for its position.
7. **The next decision**, through the choice tool, then end the turn and wait.

**Decisions per turn:** ask the one decision that blocks going deeper (for example "before writing the SQL schema"). Batch up to 3 in one call only when they are independent, such as confirming an interpreted answer plus the next decision.

When the user answers, even loosely across stack, scope, and new requirements, start the next turn with "Updated based on your decisions:", fold **every** stated decision into the diagram, tables, and draft (add a comparison table when an answer introduces a new distinction), then raise the next decision.

**Every turn ends with a decision until v1.0.** Never end with only a list of open questions, a "reply 'yes' if correct" sentence, or a summary.

### Clarification notes

When a term or boundary could be misread, add a short **Architecture note:** that pins it down, for example "Google Drive is on the internet but counts as internal storage here, because we control where files live" or "`localhost` means the worker machine, not the visitor's". These notes prevent most rework.

## Which decision next

Ask the decision that changes the most of the design. The usual order, adjusted to what is already known:

1. Who and what the system serves (internal tool, public product, both; tenants)
2. System boundary and integrations
3. Core domain model: the central entities and their relationships
4. Data ownership: sources of truth, where files and data live, consistency needs
5. Quality drivers with numbers: scale, latency, availability, data sensitivity, and the SLA from the PRD
6. Stack and deployment constraints: existing stack, hosting, team skills

Challenge risky choices along the way: an unnecessary new data store, a missing source of truth, or an unmeasurable NFR deserves a sharper counter-proposal that names the driver.

## Decision agenda and when to stop

The loop must have a visible end.

- **Stages with approval gates.** Drivers & context → Architecture style & components → Data model (logical → physical) → Interfaces, security & NFRs → Deployment, migration & milestones. Show them as a checklist (✅ approved · 🔄 in progress · ⏳ not started). A stage closes when the user approves it through the choice tool (*Approve <stage> (recommended)* / *Needs changes*), bundled with the first decision of the next stage. Approved stages reopen only when the user asks or a later answer changes them.
- **Documentation sets.** If the user asks for a whole set of documents ("build the docs for my app"), first show a document map (each document, what it covers, which skill produces it, the order: product requirements first, then architecture) and confirm it. Do not draft documents another skill owns.
- **Publish the agenda first.** On the first guided turn, list the **8–12** decisions needed before v1.0 with their IDs (`D-001 …`, see `asking-decisions.md`), one line each, with your recommended answer in brackets when you have one. Show it again with ✅ / 🟡 / ⏳ whenever it changes.
- **Only one-way doors go on the agenda**: answers that are hard to reverse or that change the document's structure, such as system boundary and tenancy, architecture style (monolith / services / serverless), core domain model and sources of truth, primary data store, hosting and runtime, authentication and authorization model, sync vs. async for core flows, and integration contracts.
- **Decide two-way doors yourself.** Storage keys and file naming, image sizes and formats, libraries inside a chosen stack, retries and timeouts, log fields, folder structure, naming conventions, and tunable limits are not asked one by one. Record each as 🟡 in a *Defaults (review anytime)* table in the draft (item, default, one-line reason), and mention new defaults in one line per turn. The user can override any default; that does not reopen the loop.
- **New agenda items need a reason.** Add one only when an answer creates a new one-way door: `Agenda: 6/9 decided · +1 added: <topic> because <reason>`.
- **Open questions are the queue.** Each blocking `Q-xxx` in the draft is asked in a later turn, highest impact first. Questions that change nothing move to *Open questions (non-blocking)* without being asked.
- **Stop** when every agenda item is ✅ or explicitly deferred and these are confirmed: boundary, core domain model, sources of truth, key quality drivers with numbers, and stack constraints. Then ask: *Finalize v1.0 (recommended)* / *Review section by section first*. Never stop at a v0.x draft without offering this.
- **Budget.** If about **12** decisions have been asked and items remain, offer: *Finalize v1.0 with the remaining items as 🟡 defaults (recommended)* / *Continue with the remaining <n> decisions* / *Review the defaults table first*.

## Versioned drafts

- **The draft file is the memory, not the chat.** Save it from the first draft: `docs/05-architecture/<system-or-feature>.md` in the standard `docs/` structure, otherwise `docs/architecture/<system-or-feature>.md`; inline when there is no project. Update the same file every turn.
- Bump the version on every substantive update: v0.1, v0.2, … v1.0 is reserved for the version the user approves.
- Keep a **Change log** at the end: version → decisions applied → sections changed. Significant decisions also become ADRs.
- In chat, show only what changed, the progress line, and the diagram when it changed. If the conversation gets long, suggest continuing in a new chat from the latest draft file.

## Finishing

When the core is ✅ (boundary, core domain model, sources of truth, quality drivers with numbers, stack constraints), move to the full template, the security pass, and validation. Complete the remaining sections, ask the user to approve v1.0, and summarize trade-offs, risks, and open questions.
