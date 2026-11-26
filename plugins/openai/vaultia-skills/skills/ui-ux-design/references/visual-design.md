# Visual Design

The kit already sets the look; good screens come from consistent use of it. Change the look through tokens and themes, never per screen.

The rules below are shared. `surfaces.md` sets what differs: type scale and whitespace (landing pages are larger and airier), density (portals can be compact), and how strongly the brand shows (landing page > storefront > portal).

## Hierarchy

- One primary action per view (`Button` default variant). Other actions are `outline`, `secondary`, or `ghost`.
- One page title (largest text); section titles one step smaller; body text at the default size; metadata `text-muted-foreground` and smaller.
- Put the most important information top-left (in left-to-right languages); group related things and separate groups with space before lines.

## Spacing and layout

- Use the Tailwind spacing scale only (`gap-2`, `p-4`, `space-y-6`), no arbitrary pixel values.
- A consistent rhythm: small gaps inside a group (`gap-2`/`gap-3`), larger between groups (`gap-6`), largest between page sections (`gap-8`+).
- Reading content has a max width (`max-w-3xl` for forms and text); data pages can use the full width.
- Grids collapse to one column on small screens; tables scroll horizontally or switch to cards.

## Color

- Use semantic tokens only: `bg-background`, `bg-card`, `text-foreground`, `text-muted-foreground`, `border-border`, `bg-primary`, `text-primary`.
- Status color carries meaning: `success`, `warning`, `info`, `error`/`destructive`, with `-accent` backgrounds for subtle badges and alerts. Never rely on color alone; pair it with text or an icon.
- `primary` is for the main action and current selection, not decoration.
- No hex values, `rgb()`, or palette classes (`bg-blue-500`) in screens.

## Typography

- Use the app font set on `body`; at most two weights for most text (normal, semibold), bold for page titles and key numbers.
- Numbers in tables and KPIs: `tabular-nums`. Truncate long text with a tooltip or a detail view, never by cutting meaning.

## Brand theme

When the user has brand colors:

1. In `packages/ui/src/tokens/tokens.json`, replace the `brand` scale (50–950) with a scale built from the brand color (the brand color is usually 500 or 600). Adjust `neutral` only if the brand calls for warm or cool grays.
2. Keep `primary` readable: check `primary-foreground` on `primary` meets 4.5:1 contrast in light and dark; switch the foreground (white or near-black) if not.
3. Run `bun run theme:build` (or `node scripts/build-theme.mjs`) in `packages/ui`, then `theme:check`.
4. For several brands in one product, add a theme file per brand as described in the kit's `AGENTS.md`, and switch with `data-theme`.

## Dark mode

- Comes from the theme's `.dark` values; screens need no `dark:` color classes when they use semantic tokens.
- Check every new screen in both modes: contrast, borders that disappear, images or charts with hard-coded backgrounds.

## Motion

The amount of motion comes from the surface (`surfaces.md`): rich on landing pages, hover and feedback only on storefronts, functional only in portals. In every case:

- Content is readable without the animation and never waits for it.
- Respect `prefers-reduced-motion` (`motion-safe:` / `motion-reduce:` variants).
- Animate `transform` and `opacity`, not layout properties, to avoid jank and layout shift.
- Use the kit's `tw-animate-css` utilities for enter and exit; add an animation library only for landing pages that need it.

## Density

- Default: comfortable (kit sizes as they are).
- Compact for data-heavy portal screens: `size='sm'` controls, tighter table rows, smaller gaps. Apply per screen type, consistently.
