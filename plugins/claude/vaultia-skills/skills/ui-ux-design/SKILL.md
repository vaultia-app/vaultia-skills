---
name: ui-ux-design
description: Design and build user interfaces for portals, landing pages, and storefronts — screen maps, user flows, page layouts, component choices, every UI state, accessibility, and brand theming — and implement them as React screens with the Vaultia Base UI React kit (Base UI, Tailwind CSS v4, cva). Use when the user asks for UI/UX design, screen or page design, wireframes, an admin portal, dashboard, or back office, a landing page or marketing site, an online store, product page, cart, or checkout, turning a PRD or feature spec into screens, setting up a UI kit or design system, creating a brand theme or dark mode, or reviewing an existing UI for usability and accessibility problems. Not for defining product scope or requirements (use product-requirements) or for backend and system architecture (use architecture-requirements).
---

# UI/UX Design

Turn requirements into screens people can use: plan the experience first (screens, flows, states), then build it with a ready-made component kit instead of starting from scratch.

Every page belongs to one of three surfaces, grouped by design intent: **landing page** (impress: polished, animated), **storefront** (sell: clear, specific, little motion), and **portal** (work: business logic and interaction, just-enough visuals). The surface sets the defaults for polish, motion, content, and interaction (`references/surfaces.md`).

The default stack is the **Base UI React kit** from the public `vaultia-templates` repository: about 60 components (atoms, molecules, organisms) on Base UI, Tailwind CSS v4, and `cva`, with design tokens, generated themes, and English and Vietnamese locales. The kit's own `AGENTS.md` holds its coding rules.

## First reply

Screens built on unexamined guesses look finished but encode the wrong flows.

- Name the surface you identified. If it is unclear, ask it first, because it changes every later choice.
- If the input is a one-line idea with no requirements, propose a **screen map** (screens, who uses them, main flow) and ask the decisions that shape the UI; do not write page code yet.
- If the project has a PRD (`docs/PRD.md`) or feature specs (`docs/03-functional-specs/`), read them and propose the screen map and flows for the requested feature directly.
- If the user asks for a review, inspect the UI first and report findings before changing anything.
- Ask decisions as described in `references/asking-decisions.md`. Build immediately only when the user says so ("just build it") or the input already settles platform, users, main flow, and brand.

## When to use

- Designing screens, flows, or layouts for a portal or app, a landing page, or a storefront.
- Building those screens in React with the kit, including setting the kit up in a new project.
- Creating or changing a brand theme, dark mode, density, or typography.
- Reviewing an existing UI for UX, consistency, and accessibility problems.

Hand off when the work leaves the UI: unclear scope, users, or rules go to `product-requirements`; APIs, data storage, and system design go to `architecture-requirements`. Call the API through the app's existing data layer; never invent endpoints.

## Workflow

1. **Gather context.** Read the request and any PRD, feature spec, actors, workflows, and glossary. In a codebase, detect the framework, package manager, monorepo layout, and whether a UI kit or design system already exists (`packages/ui`, `components/ui`, a `tailwind` config, an `AGENTS.md` for UI).
2. **Classify each page** as landing page, storefront, or portal with `references/surfaces.md`. Its rules take precedence over the general defaults in the other references.
3. **Plan the UX** with `references/ux-planning.md`: screen map, the flow for each journey, and the states of each screen. Show it to the user with one diagram and ask only the decisions that block the design.
4. **Set up the kit** if the project has none, following `references/ui-kit-setup.md`. If the project already has a design system, use it and skip this step.
5. **Read the kit rules.** Read the project's `packages/ui/AGENTS.md` (or the kit's live copy, see `references/ui-kit-setup.md`) before writing UI code.
6. **Choose components and layout** with `references/component-map.md` and the typical pages in `references/surfaces.md`: map each part of each screen to an existing kit component, at the polish and interaction level of its surface. Add a kit component only when no composition works.
7. **Apply the visual design** with `references/visual-design.md`: hierarchy, spacing, color through semantic tokens, and a brand theme when the user has one.
8. **Build the screens** in the app (not in the kit): pages, sections, and feature components that compose kit components and receive data through props or the app's data layer.
9. **Check** every screen against `references/ux-checklist.md` and the surface rules: all states, forms, feedback, responsive layout, accessibility, and copy. Run the project's typecheck, lint, and build; fix what fails.
10. **Deliver.** List the screens and files created or changed, the decisions made, assumptions, and open questions. Offer the next feature or a review pass.

## Outputs

- A screen map and user flows for the feature (in the conversation; saved to `docs/04-ui/` when the project uses the standard `docs/` structure)
- Working React screens built from kit components, in the app's own folders
- The kit installed in `packages/ui` with its theme and locale wired into the app, when it was missing
- A brand theme generated from tokens, when requested
- For reviews: findings ranked Blocking → Important → Minor, each with the screen, the problem, and the fix

## Guardrails

- **Requirements are the source.** Every screen and field traces to a journey, requirement, or user request. Mark anything you add on your own as a proposal.
- **Reuse before you build.** Use kit components and page patterns; never re-create a button, input, dialog, or table in the app.
- **Business logic stays in the app.** Kit components stay pure UI; domain names, API calls, and permissions live in app code.
- **Semantic tokens only.** No hex values or raw palette classes in screens or kit components; color changes go through tokens and themes.
- **Every state is designed.** Loading, empty, error, partial, success, disabled, and no-permission states are part of the screen, not an afterthought.
- **Accessible by default.** Keyboard, focus, labels, contrast (WCAG 2.2 AA), and touch targets are checked, not assumed.
- **No hard-coded UI text inside the kit.** Kit defaults come from its locale; screen copy uses the user's language and the project's i18n setup when one exists.
- **Respect the existing stack.** In a project with another UI library or framework (Vue, Angular, Flutter, MUI…), apply the UX workflow and that stack's components; do not install the kit unless the user asks.
- **Never overwrite user work silently.** Ask before replacing an existing UI kit, theme, or layout.
- **Match the user's language** in replies and documents; code identifiers and file names stay in English.

## References

| File | Read when |
|---|---|
| `references/asking-decisions.md` | Any turn that asks the user to decide |
| `references/surfaces.md` | Classifying pages as landing page, storefront, or portal, and the defaults each one sets |
| `references/ux-planning.md` | Planning screens, flows, and states from requirements |
| `references/ui-kit-setup.md` | The project has no UI kit, or you need the kit's rules |
| `references/component-map.md` | Choosing kit components for each part of a screen |
| `references/visual-design.md` | Layout, hierarchy, spacing, color, typography, themes, dark mode |
| `references/ux-checklist.md` | Checking a screen before delivery, or reviewing an existing UI |
