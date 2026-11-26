# Existing Context (Handoffs, Specs, ADRs, Codebases)

Use this when the input already contains decisions: a handoff note, BRD/SRS, earlier PRD or architecture doc, ADRs, an ERD, or a codebase. The job is to **continue** that work, not to start a new one.

## 1. Build a context ledger first

Before proposing anything, read the material and write a short ledger (in chat, and as the first section of the draft when you create one):

| Ledger part | What to capture |
|---|---|
| **Decided** | ADRs, business rules, approved scope, chosen stack, naming — each with its source (`ADR-0008`, `CMS-BR-30`, `§6.3`) |
| **Existing system** | Current entities/tables, services, ID prefixes, document names, and what is implemented vs. only specified |
| **Constraints** | Out-of-scope items, NFR numbers, security rules, writing conventions (language, file layout) |
| **Open items** | Questions the source marks as open, plus its own "next actions" |

Ask the user to confirm the ledger only when something is contradictory or ambiguous; otherwise state it and continue.

## 2. Rules while working

- **Decided items are constraints.** Never re-ask them and never contradict them silently. To propose a change, name the item it supersedes (for example "supersedes ADR-0008"), show the impact, and ask *keep* or *change* through the choice tool — the same flow as an answer to an already-decided question.
- **Reuse names and IDs.** Use the existing entity/table names, ID prefixes, and numbering (continue `ADR-0009`, `MAST-01`, `CMS-BR-08` instead of starting `FR-1`). Extend existing entities with new fields or relations; **never create a parallel entity or table** for something that already exists. If a rename is really needed, propose it as a change.
- **The agenda comes from the source.** Build the decision agenda from the ledger's open items and the source's next actions, in their priority order. Add new items only with a reason.
- **Produce deltas, not a new document.** Output the new or changed pieces in the source's structure and language: a new ADR, new requirement IDs, an updated section, a migration note. Do not create a fresh "v0.1" product document unless the user asks for one.
- **Mark current vs. target.** Keep "implemented today" separate from "designed, not built" using the source's own convention.
- **Follow the source's conventions** for language, headings, file locations, and status markers.
- **A project with the standard `docs/` structure** is existing context too: its conventions, feature list, business rules, decisions log, and open questions are the ledger. Continue its numbering and add the new feature as the next `F<nn>` file. See `docs-structure.md`.
