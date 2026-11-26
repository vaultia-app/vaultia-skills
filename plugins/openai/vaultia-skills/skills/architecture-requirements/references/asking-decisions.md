# Asking for Decisions and Handling Answers

Every decision in guided mode is asked through the host's **choice tool**, on every turn, not only the first. Plain-text options are only the fallback for hosts without one. After asking, **end the turn and wait**: do not draft content that depends on the answer.

## Host choice tools

This is the only place host-specific tool names appear. Elsewhere, say "the choice tool".

| Host | Tool | How to fill it |
|---|---|---|
| ChatGPT, Codex | `request_user_input_async` | `questions: [{"title": "<self-contained question>", "options": ["<recommended> (recommended)", "<option>"]}]`. Options are plain strings; omit `options` for free text. All intake items fit in one call |
| Codex Plan mode | `request_user_input` | 1–3 questions, each `{"id": "snake_case", "header": "≤12 chars", "options": [{"label": "1–5 words (Recommended)", "description": "one-sentence trade-off"}]}`, 2–3 options |
| Claude (Claude Code, Desktop, claude.ai) | `AskUserQuestion` or the host's equivalent | 1–4 questions per call, each with a short `header`, 2–4 options with `label` + `description`, and `multiSelect`; "(Recommended)" on the first label |
| Self-built forms (inline widgets, visualizations, HTML cards) | The form you render | Same rules, **plus** a last option "Other — type your own answer" with a text input |
| No choice tool | Plain text | See *Fallback* |

## Rules for every question

- **Stable ID first.** Start the title with the decision ID (`D-003 · Primary data store: …`). When the project already numbers decisions (the PRD's *Decisions* section or `docs/09-working/decisions-log.md`), continue that numbering. Use the same ID in the draft's decision log.
- **Recommended option first**, labeled "(recommended)" in the user's language. Several hosts preselect the first option.
- **Self-contained title.** The user may see only the form, so include the context needed to answer.
- **2–4 mutually exclusive options** with short labels; put what each implies for the design in the description (or after a dash when options are plain strings), so the user decides on trade-offs, not labels.
- **"Other":** native tools (`request_user_input_async`, `request_user_input`, `AskUserQuestion`) add free text themselves, so don't add it. Any form you build yourself must add "Other — type your own answer" with a text input. If unsure which you are using, add it.
- **No instructions inside options or titles** ("update the design and ask the next question"). The submitted selection should read as the user's answer only.
- **Don't ask the same topic twice** unless the user reopens it.

## Multi-select

Use multi-select when the user may pick several answers (integrations, platforms, environments):

- Claude `AskUserQuestion`, or any tool with a multi-select flag: set it (`multiSelect: true`).
- ChatGPT / Codex (single-select plus free text): say in the title that several can be chosen and how to type them ("Choose a set, or type your own combination such as \"A, C, D\""). Offer ready-made sets, recommended first: "Core set (recommended): A + B + D", "All of them", "Only A". Do not split one multi-select into many yes/no questions.
- Plain text: label items A, B, C… and end with "Reply with one or more letters (for example \"A, C\"), your own answer, or \"you decide\"".
- Record each selected item as its own decision in the draft, and the unselected ones as later / out of scope.

## Fallback: plain text

```text
### Decision needed before <next step>

D-<nnn> · <Question?>

A) <Option> — <what it implies for the design> ← recommended: <one-line reason>
B) <Option> — <what it implies for the design>
C) <Option> — <what it implies for the design>

Reply with a letter, your own answer, or "you decide".
```

## Handling answers

- **"You decide"** → take the recommendation and record it as 🟡 assumption (and a proposed ADR if significant), not ✅ confirmed.
- **A typed answer beats a selected option.** If you had to interpret it, record your interpretation as 🟡 and confirm it in the next choice call ("I understood <X>, correct?" with *Correct (recommended)* / *<most likely alternative>*), alongside the next decision. Do not ask for confirmation in prose. Mark it ✅ only after the user agrees.

### An answer to an already-decided question

Hosts keep old forms clickable, so the user may pick a different option for an earlier `D-xxx`. Never overwrite silently:

1. Name the change: "This changes D-002 · Primary data store from *PostgreSQL* to *MongoDB*."
2. List what depends on it: later decisions, components, data model, NFRs, and diagram nodes that would change.
3. Ask: *Keep <current value>* / *Change to <new value> and update the affected parts*. Recommend *Keep* unless the user clearly meant to change it.
4. On *Change*: bump the version, update every affected part, mark dependent decisions 🟡 for re-confirmation, and record old and new values in the change log; supersede the ADR rather than rewriting it. On *Keep*: change nothing.

If another question is still pending, handle its answer first, then raise the change.

### New ideas and side discussions

The user may raise something outside the pending question: a requirement they just remembered, a constraint, a change of mind. Never let it stay only in the chat:

1. Discuss it as long as the user wants; give your opinion and the trade-offs.
2. When the discussion concludes or the user moves on, summarize what was agreed (what, for whom, why) and ask how to capture it, with a new ID (`D-xxx`, or `FR-n` for a requirement):
   - *Add to the draft now (recommended when it serves a core flow)*
   - *Add as a later phase*
   - *Record as an open question*
   - *Don't add it*
3. On *Add*: update the draft, diagram, and tables, bump the version, and log it. If it conflicts with an earlier decision, handle it as above.
4. If a decision was pending before the side discussion, ask it again in the **same** choice call as the capture question.
