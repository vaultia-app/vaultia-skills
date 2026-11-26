# UI Kit Setup

The Base UI React kit lives in the public `vaultia-templates` repository at `src/frontend/base-ui-react-kit`. It is copied into the project once; from then on the project owns the code and changes it freely.

## Decide whether to install

| Project | Do |
|---|---|
| Already has `packages/ui` from this kit (its `AGENTS.md` starts with "UI Kit (`@workspace/ui`)") | Use it. Do not reinstall or overwrite. |
| Has another design system or UI library | Use that. Install the kit only if the user asks, and never replace the existing one without approval. |
| React project (Next.js, Vite, Remix…) with no UI kit | Install the kit (below). Tell the user in one line. |
| Not React | Do not install. Apply the UX workflow with the project's own stack. |
| No file access (chat only) | Show the screen code inline and say it assumes the kit; link the kit's README. |

## Read the kit rules

Before writing UI code, read the kit's `AGENTS.md`:

- Installed kit: `packages/ui/AGENTS.md` (the project's copy is the source of truth).
- Not installed yet: `https://raw.githubusercontent.com/vaultia-app/vaultia-templates/main/src/frontend/base-ui-react-kit/AGENTS.md`. If it cannot be fetched, follow the rules in `component-map.md` and `visual-design.md`.

## Install

1. **Copy the kit** into `packages/ui` (monorepo) with one of:
   ```bash
   npx degit vaultia-app/vaultia-templates/src/frontend/base-ui-react-kit packages/ui
   ```
   ```bash
   git clone --depth 1 https://github.com/vaultia-app/vaultia-templates.git <tmp>
   cp -R <tmp>/src/frontend/base-ui-react-kit packages/ui
   ```
   If neither works (no network or no shell), stop and ask the user to copy it; do not rewrite the kit from memory.
2. **Package name.** Keep `@workspace/ui`, or rename it to the project scope (for example `@acme/ui`) by replacing `@workspace/ui` across `packages/ui` and the app.
3. **TypeScript config.** If the monorepo has a shared tsconfig, make `packages/ui/tsconfig.json` extend it and keep its `paths`.
4. **Dependencies.** Add `"@workspace/ui": "workspace:*"` to the app. Make sure the app has `tailwindcss` v4, `@tailwindcss/postcss` (or the Vite plugin), and `tw-animate-css`. Install with the project's package manager.
5. **Styles.** In the app's Tailwind entry CSS:
   ```css
   @import 'tailwindcss';
   @import 'tw-animate-css';
   @import '@workspace/ui/styles/theme.css';
   @source '<relative path to packages/ui/src>';
   ```
   Add base styles: `* { @apply border-border; }` and `body { @apply bg-background text-foreground; }`.
6. **Theme and locale.** On `<html>`, set `data-theme={DEFAULT_THEME}`; for dark mode, toggle the `dark` class (for example `next-themes` with `attribute='class'`). Wrap the app in `<UiLocaleProvider locale='vi'>` for Vietnamese defaults (`'en'` is the default).
7. **Single-app repository (no workspaces).** Still copy to `packages/ui`, add its dependencies to the app's `package.json`, and map the alias in the app's tsconfig: `"@workspace/ui": ["./packages/ui/src/index.ts"]`, `"@workspace/ui/*": ["./packages/ui/src/*"]`.
8. **Verify.** Run the app's typecheck and build, and `bun run theme:check` (or `node scripts/build-theme.mjs --check`) in `packages/ui`. Render one kit component on a page to confirm styles load.

## After install

- Screens and feature components go in the app (for example `apps/web/src/app/...` and `apps/web/src/components/<feature>/`), never in `packages/ui`.
- Generic, reusable UI that the kit lacks goes in `packages/ui` following its `AGENTS.md` (right atomic level, Base UI primitive, `cva`, `data-slot`, semantic tokens, locale strings).
