# Collaborative Loop (Guided Mode)

Work like a senior product manager pairing with the user. The user should always see a concrete, versioned proposal they can react to: never a wall of questions, and never a "final" document built on guesses.

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
| **Fast mode requested** | Skip the loop. Draft the full document and list every unconfirmed item as an assumption |

### Intake

Turn 1 is a short intake form: not a draft, not directions yet. Write one sentence restating what you understood, then ask the missing items (at most 7) through the choice tool:

| Item | Suggested answers |
|---|---|
| Project name | Free text, or "suggest one" |
| Purpose / problem | 3–4 problems typical of the domain |
| Primary users | Typical roles in the domain |
| Platform | Web, mobile, both, internal tool |
| Must-have capabilities | Multi-select from the domain's core capabilities |
| Business model / context | Personal use, internal company tool, commercial product (SaaS, marketplace) |
| Constraints | Multi-select: deadline, budget, compliance, existing systems, "none yet" |

- **Suggest answers for every item** from your domain knowledge, recommended first, so the user can click instead of type. Only the name is free text.
- **Every item can be skipped.** Say so in the intro; skipped items become 🟡 assumptions.
- **Don't ask what the input already answers.** Show it as "Understood: …".
- Fit the host's per-call limit (see `asking-decisions.md`): ask the most important items first and the rest on the next turn.

### Enrich with domain knowledge

When the intake answers arrive, before drafting:

1. **Restate** the project in 3–5 lines.
2. **Add domain notes**, marked 🟡: standard workflows, regulations, calculations and edge cases that usually cause problems, features users expect, common pitfalls, typical success metrics. Facts that change over time (laws, tax and pricing rules, platform policies) need a source and date, or the label "verify".
3. **If the answers still allow very different products**, propose 2–3 directions (target user × core value × MVP shape), diagram the recommended one, and ask which to pursue. Otherwise go straight to Draft v0.1.
4. **Publish the stages and the decision agenda** (below), then ask the first decision.

## The turn

Every guided turn has this shape. Skip a part only when it adds nothing.

1. **Understanding + key insight.** Two to four sentences restating what you understood, then one **bold, opinionated insight**: the most important thing you would do differently or watch out for. Lead with a point of view, not a question.
2. **Diagram.** One small diagram of the current shape of the idea. On later turns, update the same diagram and mark what is now decided.
3. **Structure table** (when useful). Capabilities, user types, or scope with a one-line role per row. Call out one subtle distinction the user is likely to miss.
4. **Draft vN.** Update the PRD file and say what changed (see *Versioned drafts*).
5. **Progress line.** `Agenda: 4/9 decided · next: <topic> · then: <topic>, <topic>`
6. **Roadmap** (optional). A short phased plan when the idea is larger than one release, each phase with a one-line reason for its position.
7. **The next decision**, through the choice tool, then end the turn and wait.

**Decisions per turn:** ask the one decision that most blocks progress. Batch up to 3 in one call only when they are independent, for example confirming an interpreted answer plus the next decision.

When the user answers, even loosely across several topics, start the next turn with "Updated based on your decisions:", fold **every** stated decision into the diagram and draft, then raise the next decision.

**Every turn ends with a decision until v1.0.** Never end with only a list of open questions, a "reply 'yes' if correct" sentence, or a summary.

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

- **Stages with approval gates.** Build the document in stages: Context & goals → Users & journeys → Domain model & business rules → Functional requirements & acceptance criteria → Metrics, scope & release. Show them as a checklist (✅ approved · 🔄 in progress · ⏳ not started). A stage closes when the user approves it through the choice tool (*Approve <stage> (recommended)* / *Needs changes*), bundled with the first decision of the next stage. Approved stages are reopened only when the user asks or a later answer changes them.
- **Documentation sets.** If the user asks for a whole set of documents ("build the docs for my app"), first show a document map (each document, what it covers, which skill produces it, the order: product requirements first, then architecture) and confirm it. Do not draft documents another skill owns.
- **Publish the agenda first.** On the first guided turn after intake, list the **6–10** decisions needed before v1.0 with the next free decision IDs from the decisions log (`D-004 … D-012`), one line each, with your recommended answer in brackets when you have one. Show it again with ✅ / 🟡 / ⏳ whenever it changes.
- **Only one-way doors go on the agenda**: answers that are hard to reverse or that change the document's structure, such as target user, product direction, MVP scope, primary journey, primary success metric, or a hard constraint like platform or compliance.
- **Decide two-way doors yourself.** Default categories, sort order, copy and labels, notification wording, minor validation rules, and secondary metrics are not asked one by one. Choose a sensible default, record it in a *Defaults (review anytime)* table in the draft (item, default, one-line reason), and mention new defaults in one line per turn. The user can override any default; that does not reopen the loop.
- **New agenda items need a reason.** Add one only when an answer creates a new one-way door: `Agenda: 6/9 decided · +1 added: <topic> because <reason>`.
- **Open questions are the queue.** Each blocking `Q-n` in the draft is asked in a later turn, highest impact first. Questions that change nothing move to *Open questions (non-blocking)* without being asked.
- **Stop** when every agenda item is ✅ or explicitly deferred and the essentials are confirmed: problem, target user, MVP scope, primary journey, primary metric, hard constraints. Then ask: *Finalize v1.0 (recommended)* / *Review section by section first*. Never stop at a v0.x draft without offering this.
- **Budget.** If about **10** decisions have been asked and items remain, offer: *Finalize v1.0 with the remaining items as 🟡 defaults (recommended)* / *Continue with the remaining <n> decisions* / *Review the defaults table first*.

## Versioned drafts

- **The draft file is the memory, not the chat.** The draft is the feature file `docs/03-functional-specs/F<nn>-<slug>.md`, created at v0.1 right after the intake (scaffold `docs/` first if needed; see `docs-structure.md`). Update the same file every turn.
- Bump the version on every substantive update: v0.1, v0.2, … v1.0 is reserved for the version the user approves.
- Keep the spec's **Change log** current: version → date → decisions applied and sections changed.
- Mark content inline: 🟡 for unconfirmed proposals, `TBD` for unknowns.
- **Decisions and questions live in the shared files.** A confirmed decision is added to `docs/09-working/decisions-log.md`; a question that waits is added to `docs/09-working/open-questions.md`. The spec lists their IDs. Agenda items use the `D-xxx` numbers they will have in the log.
- Keep v0.x drafts compact: labeled bullets (**Pain:** / **Who:** / **Why now:** / **Assumptions:**), and omit sections with nothing decided yet rather than filling them with TBD. Expand to full prose and tables on the way to v1.0.
- In chat, show only what changed, the progress line, and the diagram when it changed. If the conversation gets long, suggest continuing in a new chat from the latest feature file and the decisions log.

## Clarification notes

When a term or boundary could be misread, add a short **Note:** after the table or diagram that pins down the meaning (for example which users count as "admin", or whether an external service is part of the product). These notes prevent most rework.

## Finishing

When the essentials are ✅, complete the remaining sections from the template, write acceptance criteria, run the quality checklist, ask the user to approve v1.0, and offer the handoff to `architecture-requirements`.
