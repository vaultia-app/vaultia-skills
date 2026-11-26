# Documentation Structure

Every PRD lands in one standard `docs/` structure, so the output can be used as-is: shared knowledge (actors, domain, rules, decisions) lives once, and each feature is one file that references it.

The starter kit is `assets/docs-starter/`. Its `00-overview/03-conventions.md` is the single source for IDs, file names, statuses, and versions; follow it and do not restate it elsewhere.

## Where the documents go

Pick the first case that matches:

| Situation | Do |
|---|---|
| The project already has `docs/` in this structure (it has `00-overview/03-conventions.md`) | Read `docs/README.md`, the conventions, and the feature list first. Add to it. |
| The project has docs in a different structure | Follow the existing structure (`existing-context.md`). Offer the standard structure once as an option; never restructure without approval. |
| The project has no docs yet | Scaffold: copy `assets/docs-starter/` to `docs/` when you write the first draft (below). |
| No project or file access (chat only) | Reply inline with the feature spec, followed by the entries to add to each shared file. |
| The user asked for another location | Use it, keeping the same internal structure. |

## Scaffolding

1. Copy every file from `assets/docs-starter/` to `docs/`, keeping folder and file names.
2. Fill what the conversation already confirmed: product name, owner, date, `<language>` in the conventions, the introduction. Translate headings and placeholder text into the user's language; keep file names, folder names, and IDs in English.
3. Leave unknown fields as `TBD`. Do not invent content to fill a template.
4. Do not create the optional folders (`04-ui/`, `05-architecture/`, `06-testing/`, `07-roadmap/`) until they have content.
5. Tell the user, in one line, that the structure was created and where the feature file is.

## One feature, one file

- Path: `docs/03-functional-specs/F<nn>-<slug>.md`, created from `03-functional-specs/_template.md`. `<nn>` is the next free number in the feature list; `<slug>` is a short English `kebab-case` name.
- The spec is the draft of the collaborative loop: create it at v0.1 and update the same file every turn.
- Omit template sections that do not apply; keep the order and numbering of the rest.

## Shared files to update with each feature

Update the shared files in the same turn as the spec, and say which ones changed.

| When the feature… | Update |
|---|---|
| is created, or its priority, release, or status changes | `02-requirements/01-feature-list.md`: one row with a link to the spec |
| introduces or changes a business object | `01-business/02-domain-model.md`: object row, relationship, lifecycle |
| needs a rule that other features could also depend on | `01-business/03-business-rules.md`: a new `BR-xxx` with a worked example; the spec lists it by ID |
| adds an actor or a permission | `01-business/01-actors-and-permissions.md` |
| is a step in a process that spans several features | `01-business/04-workflows.md`: the `W-x` workflow, with this feature's ID on its step |
| uses a term that could be misread | `00-overview/02-glossary.md` |
| gets a decision confirmed | `09-working/decisions-log.md`: the next `D-xxx`; the spec lists it by ID |
| raises a question that cannot be decided now | `09-working/open-questions.md`: the next `Q-xxx` with an owner |
| adds a requirement for the whole product | `02-requirements/02-non-functional-requirements.md` |

Rule of thumb: if a second feature could need it, it goes in a shared file and the spec references it by ID. If only this feature needs it, it stays in the spec.

## Numbering

- Before assigning a global ID (`F`, `BR`, `NFR`, `D`, `Q`, `W`), read the file that holds it and take the next free number.
- Decision agenda items in the collaborative loop use the decision IDs they will have in the decisions log.
- Never renumber. To fix a duplicate, give one item a new ID and note "formerly …" in it.
