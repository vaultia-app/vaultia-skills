# UX Checklist

Run this on every screen before delivery, and use it to structure a review of an existing UI. Then check the rules for the surface in `surfaces.md`. Fix what you can; report the rest.

## States

- [ ] Loading uses skeletons shaped like the content; no layout jump when data arrives.
- [ ] Empty first-use state explains what goes here and offers the primary action.
- [ ] "No results" names the cause (search, filters) and offers a way to clear it.
- [ ] Errors say what failed and how to recover (retry, fix input, contact); no raw error codes.
- [ ] Disabled actions explain why (tooltip or helper text) when it is not obvious.
- [ ] Users without permission see the screen as the requirements say (hidden, read-only, or a message).

## Forms

- [ ] Every control has a visible label (`Field`); placeholders are examples, not labels.
- [ ] Required and optional fields are clear; formats are shown before the user types (dates, phone, money).
- [ ] Validation runs on blur and on submit; errors appear under the field and are announced (`aria-invalid`, error text linked to the input).
- [ ] Input is kept after a failed submit; the first invalid field gets focus.
- [ ] The submit button shows `loading` and blocks double submission.
- [ ] Destructive actions ask for confirmation (`AlertDialog`) naming the object, or offer undo.

## Feedback and navigation

- [ ] Every action gives feedback: toast for background results, inline for errors, navigation for created objects.
- [ ] The user always knows where they are (active sidebar item, breadcrumb, page title) and can go back.
- [ ] Unsaved changes are protected when leaving a long form.
- [ ] Lists keep search, filters, sort, and page in the URL when the app has routing.

## Responsive

- [ ] Works from 320 px wide to large desktops; no horizontal page scroll (tables scroll inside their container).
- [ ] Touch targets at least 44 × 44 px on mobile; primary actions reachable by thumb.
- [ ] Dialogs fit the screen on mobile (full-screen or `BottomSheet` for long content).

## Accessibility (WCAG 2.2 AA)

- [ ] All actions work with the keyboard in a logical order; focus is visible; dialogs trap and return focus.
- [ ] Icon-only buttons have `aria-label`; decorative icons are `aria-hidden`.
- [ ] Contrast: text 4.5:1, large text and UI parts 3:1, in light and dark mode.
- [ ] Headings form an outline (one `h1` per page); landmarks for navigation and main content.
- [ ] Status is not conveyed by color alone.
- [ ] Motion respects reduced-motion settings.

## Consistency and copy

- [ ] Only kit components and semantic tokens; no one-off colors, sizes, or re-created controls.
- [ ] Terms match the glossary and stay the same across screens.
- [ ] Buttons say what they do ("Invite member", not "OK"); sentence case; no jargon or internal IDs.
- [ ] Numbers, dates, and money follow the user's locale.

## Review report format

| Severity | Screen | Problem | Why it matters | Fix |
|---|---|---|---|---|
| Blocking | S02 Invite dialog | No error when the email is already a member | Admin thinks the invite was sent | Inline error under Email (BR-003) |

Severity: **Blocking** (users cannot finish a task or are misled), **Important** (slows users down or breaks consistency or accessibility), **Minor** (polish).
