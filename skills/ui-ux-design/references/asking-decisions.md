# Asking for Decisions

Ask only decisions that change the design and that you cannot settle from the requirements or sensible defaults. Decide the rest yourself and list them as reviewable defaults.

## Host choice tools

This is the only place host-specific tool names appear. Elsewhere, say "the choice tool".

| Host | Tool | How to fill it |
|---|---|---|
| ChatGPT, Codex | `request_user_input_async` | `questions: [{"title": "<self-contained question>", "options": ["<recommended> (recommended)", "<option>"]}]` |
| Codex Plan mode | `request_user_input` | 1–3 questions, each with `id`, a short `header`, and 2–3 options with `label` and `description` |
| Claude (Claude Code, Desktop, claude.ai) | `AskUserQuestion` or the host's equivalent | 1–4 questions, each with a short `header` and 2–4 options with `label` + `description`; "(Recommended)" on the first label |
| No choice tool | Plain text | Numbered options, recommended first, and "or type your own answer" |

After asking, end the turn and wait. Do not build screens that depend on the answer.

## Rules

- **Propose first.** Show the screen map or layout you recommend, then ask.
- **Recommended option first**, with the trade-off of each option in its description.
- **Self-contained question.** The user may see only the form; include the context.
- **At most 4 questions per turn**, and only independent ones.
- **Use a preview** (ASCII layout or short code) when the user must compare layouts, if the tool supports it.
- **Record answers** as decisions; when the project has `docs/09-working/decisions-log.md`, add them there with the next `D-xxx`.

## Decisions worth asking

| Decision | Ask when | Typical options |
|---|---|---|
| Surface | Not clear from the request | Portal (signed-in work) · Landing page (marketing, one CTA) · Storefront (catalog, cart, checkout) · A mix (say which pages are which) |
| Platform and layout shell | Not stated | Responsive web app with sidebar · Mobile-first web (bottom navigation) · Desktop-only admin |
| Navigation model | More than about 5 top-level sections | Sidebar · Top bar · Tabs · Hub and spoke |
| Offer and primary CTA | Landing page without a stated goal | Sign up · Book a demo · Buy · Contact |
| Checkout and payments | Storefront without stated payment or delivery rules | Guest checkout + cards/wallets · Also bank transfer or QR · Also cash on delivery |
| Brand | Building a new app or site | Use the default theme now · Provide brand color(s) · Copy an existing theme |
| Density | Data-heavy screens | Comfortable · Compact |
| Language and locale | Users are not English speakers | English · Vietnamese · Both (i18n) |
| Pattern for a key screen | Two layouts are both reasonable | List + detail page · List + side sheet · Split view |

Do not ask about things the kit or requirements already decide (component library, form field style, icon set, a rule already in the feature spec).
