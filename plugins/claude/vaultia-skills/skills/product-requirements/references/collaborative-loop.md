# Collaborative Loop (Guided Mode)

Work like a senior product manager pairing with the user. The user always sees a concrete, versioned proposal to react to: never a wall of questions, and never a "final" document built on guesses.

```text
Propose → Visualize → Draft vN → Decide → Update to vN+1 → … → v1.0
```

Related files: `asking-decisions.md` (how to ask and how to handle answers) and `diagrams.md` (how to draw).

## Starting point

Classify the input first:

| Input | First turn |
|---|---|
| **Vague**: essentials missing ("build an app for my business", one line with no users or purpose) | Intake form (below) |
| **Partial**: some essentials answered | Intake form for the missing items only |
| **Rich**: notes, docs, tickets, a codebase, a handoff | Skip intake. Follow `existing-context.md` when decisions already exist; otherwise create Draft v0.1 now, marking every proposal not backed by the input as 🟡 |
| **Fast mode requested** (by the user only) | Skip the loop. Draft the full document and list every unconfirmed item as an assumption. Include the scope checklist with the recommended set ticked, without asking. Still end with *Delivering v1.0*: return the file and ask the delivery choice |

### Intake

Turn 1 is a short intake form, not a draft. Restate what you understood in one sentence, then ask the missing items (at most 7) through the choice tool:

| Item | Suggested answers |
|---|---|
| Project name | Free text, or "suggest one" |
| Purpose / problem | 3–4 problems typical of the domain |
| Primary users | Typical roles in the domain |
| Platform | Web, mobile, both, internal tool |
| Must-have capabilities | Multi-select from the domain's core capabilities |
| Business model / context | Personal use, internal company tool, commercial product (SaaS, marketplace) |
| Constraints | Multi-select: deadline, budget, compliance, existing systems, "none yet" |

- **Suggest answers for every item** from domain knowledge, recommended first. Only the name is free text.
- **Every item can be skipped.** Say so; skipped items become 🟡 assumptions.
- **Don't ask what the input already answers.** Show it as "Understood: …".
- Fit the host's per-call limit (`asking-decisions.md`): the most important items first, the rest on the next turn.

### Enrich with domain knowledge

When the intake answers arrive, before drafting:

1. **Restate** the project in 3–5 lines.
2. **Add domain notes**, marked 🟡: standard workflows, regulations, calculations and edge cases that usually cause problems, features users expect, common pitfalls, typical success metrics. Facts that change over time (laws, tax and pricing rules, platform policies) need a source and date, or the label "verify".
3. **If the answers still allow very different products**, propose 2–3 directions (target user × core value × MVP shape), diagram the recommended one, and ask which to pursue. Otherwise go straight to Draft v0.1.
4. **Publish the stages and the decision agenda** (below), then ask the first decision.

## The turn

Every guided turn has this shape. Skip a part only when it adds nothing.

1. **Understanding + key insight.** Two to four sentences restating what you understood, then one **bold, opinionated insight**: the most important thing you would do differently or watch out for.
2. **Diagram.** One small diagram of the current shape of the idea. On later turns, update the same diagram and mark what is now decided.
3. **Structure table** (when useful). Capabilities, user types, or scope, one line per row. Call out one distinction the user is likely to miss.
4. **Draft vN.** Update the PRD file and say what changed (see *Versioned drafts*).
5. **Progress line.** `Agenda: 4/9 decided · next: <topic> · then: <topic>, <topic>`
6. **Roadmap** (optional). Phases, when the idea is larger than one release, each with a one-line reason for its position.
7. **The next decision**, through the choice tool, then end the turn and wait.

**Decisions per turn:** ask the one decision that most blocks progress. Batch up to 3 in one call only when they are independent, for example confirming an interpreted answer plus the next decision.

When the user answers, even loosely across several topics, start the next turn with "Updated based on your decisions:", fold **every** stated decision into the diagram and draft, then raise the next decision.

**Every turn ends with a decision until v1.0.** Never end with only a list of open questions, a "reply 'yes' if correct" sentence, or a summary.

### Clarification notes

When a term or boundary could be misread, add a short **Note:** after the table or diagram that pins down the meaning (for example which users count as "admin", or whether an external service is part of the product). These notes prevent most rework.

## Which decision next

Ask the decision whose answer changes the most downstream content. The usual order, adjusted to what is already known:

1. Problem and target user (who exactly, in which situation)
2. Product direction / value proposition vs. alternatives
3. MVP scope: Must vs. later (MoSCoW)
4. Primary user journey for the Must scope
5. Success metric and target
6. Constraints and rollout (deadline, platforms, compliance)

Challenge weak inputs along the way: a vague problem, an oversized MVP, or an unmeasurable goal deserves a sharper counter-proposal. If the idea does not survive scrutiny (no real problem or user), say so plainly and suggest what to validate first.

## Decision agenda and when to stop

The loop must have a visible end.

- **Stages with approval gates.** Context & goals → Users & journeys → Domain model & business rules → Functional requirements & acceptance criteria → Metrics, scope & release. Show them as a checklist (✅ approved · 🔄 in progress · ⏳ not started). A stage closes when the user approves it through the choice tool (*Approve <stage> (recommended)* / *Needs changes*), bundled with the first decision of the next stage. Approved stages reopen only when the user asks or a later answer changes them.
- **Documentation sets.** If the user asks for a whole set of documents ("build the docs for my app"), first show a document map (each document, what it covers, which skill produces it, the order: product requirements first, then architecture) and confirm it. Do not draft documents another skill owns.
- **Publish the agenda first.** On the first guided turn after intake, list the **6–10** decisions needed before v1.0 with the next free decision IDs from the *Decisions* section (`D-004 … D-012`), one line each, with your recommended answer in brackets when you have one. Show it again with ✅ / 🟡 / ⏳ whenever it changes.
- **Only one-way doors go on the agenda**: answers that are hard to reverse or that change the document's structure (target user, product direction, MVP scope, primary journey, primary metric, a hard constraint such as platform or compliance, an SLA for a product sold to customers).
- **Decide two-way doors yourself.** Default categories, sort order, copy and labels, notification wording, minor validation rules, and secondary metrics are not asked one by one. Record each in a *Defaults (review anytime)* table in the draft (item, default, one-line reason), and mention new defaults in one line per turn. Overriding a default does not reopen the loop.
- **Non-functional requirements and SLA.** In the *Metrics, scope & release* stage, propose the product-wide NFRs as 🟡 defaults in the NFR section (performance as users notice it, availability, security and privacy, accessibility, localization, compliance, data recovery) instead of asking each one. When the product is sold to customers, put one decision on the agenda: *Do we promise an SLA?* (uptime, support response, maintenance window, data recovery). Technical targets such as p95 latency or RPO/RTO belong to `architecture-requirements`.
- **New agenda items need a reason.** Add one only when an answer creates a new one-way door: `Agenda: 6/9 decided · +1 added: <topic> because <reason>`.
- **Open questions are the queue.** Each blocking `Q-xxx` in the draft is asked in a later turn, highest impact first. Questions that change nothing move to *Open questions (non-blocking)* without being asked.
- **Stop** when every agenda item is ✅ or explicitly deferred and the essentials are confirmed: problem, target user, MVP scope, primary journey, primary metric, hard constraints. Stay in guided mode: complete the document, run the *Scope checklist* (below), ask for v1.0 approval, then deliver. Never stop at a v0.x draft without reaching it.
- **Budget.** If about **10** decisions have been asked and items remain, offer: *Move to the scope checklist with the remaining items as 🟡 defaults (recommended)* / *Continue with the remaining <n> decisions* / *Review the defaults table first*.

## Versioned drafts

- **The draft file is the memory, not the chat.** The draft is the single PRD file (`docs/PRD.md` by default, or the feature file in a project that already has the `docs/` structure; see `docs-structure.md`), created at v0.1 right after the intake. Update the same file every turn.
- Bump the version on every substantive update: v0.1, v0.2, … v1.0 is reserved for the version the user approves.
- Keep the document's **Change log** current: version → date → decisions applied and sections changed.
- Mark content inline: 🟡 for unconfirmed proposals, `TBD` for unknowns.
- **Decisions and questions have their own sections.** A confirmed decision is added to the *Decisions* section; a question that waits is added to *Open questions* (`09-working/decisions-log.md` and `09-working/open-questions.md` in a `docs/` project). Features list their IDs. Agenda items use the `D-xxx` numbers they will have there.
- Keep v0.x drafts compact: labeled bullets (**Pain:** / **Who:** / **Why now:** / **Assumptions:**), and omit sections with nothing decided yet rather than filling them with TBD. Expand to full prose and tables on the way to v1.0.
- In chat, show only what changed, the progress line, and the diagram when it changed. If the conversation gets long, suggest continuing in a new chat from the latest PRD file.

## Scope checklist (before v1.0)

When the essentials are ✅ and the remaining sections are complete, the user picks what ships in this release. It is the last step before v1.0, because cutting scope later means reopening v1.0.

1. **Write the checklist** in the *Features and MVP scope* section: one line per functional requirement, grouped by feature (one line per feature when there are more than about 30). Tick the recommended set. An unticked line says why and where it goes (Should, later phase). A line that needs another item names it.

   ```markdown
   ### F03 — Invoices
   - [x] F03/FR-1 Create an invoice for one customer
   - [x] F03/FR-2 Create invoices in bulk for a billing period — needs F01/FR-3
   - [ ] F03/FR-4 Export an invoice as PDF — later: viewing it online covers the MVP
   ```

2. **Ask** through the choice tool: *Accept the recommended set (<n> of <m>) (recommended)* / *Choose per feature* / *I'll edit the checklist in the file*.
   - *Choose per feature*: one multi-select question per feature with its requirements as options, recommended ones first (see *Multi-select* in `asking-decisions.md`). Split a feature that has more items than the tool allows.
   - *Edit in the file*: wait until the user says it is done, then re-read the checklist.
3. **Check the dependencies** of the selection:

   | Check | When it fails |
   |---|---|
   | A ticked item needs an unticked one | Bulk invoices are ticked, but the customer billing details they read are not |
   | The primary journey can be completed | A step of the journey has no ticked requirement |
   | Rules, metrics, and criteria still have a purpose | A `BR`, metric, or AC serves only unticked items: it moves with them |
   | Every actor still has something to do | An actor has no ticked capability: update the permissions, or confirm the actor leaves this release |
   | The selection matches the decisions | A ticked item contradicts a ✅ decision, or an unticked one was decided as Must |

   For each conflict, propose a fix (keep the needed item, or a smaller alternative) and ask it through the choice tool, up to 3 independent conflicts per call, until none is left.
4. **Apply.** Unticked items move to a later release in the feature table with their reason: never deleted, IDs kept. Each change from the recommended set is a decision (`D-xxx`). Bump the version and update the scope table and diagrams.
5. Ask: *Finalize v1.0 (recommended)* / *Review section by section first*.

## Finishing

When the essentials are ✅: complete the remaining sections from the template, write acceptance criteria, run the quality checklist and the scope checklist, and ask the user to approve v1.0. Then deliver it as in *Delivering v1.0* in `docs-structure.md`.
