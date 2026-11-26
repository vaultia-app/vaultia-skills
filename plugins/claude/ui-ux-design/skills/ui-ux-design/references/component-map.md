# Component Map

Map each part of a screen to a kit component before writing code. Import from `@workspace/ui/atoms/<name>`, `@workspace/ui/molecules/<name>`, or `@workspace/ui/organisms/<name>` (everything is also exported from `@workspace/ui`). Check the actual exports in the project's `packages/ui/src/components` when unsure.

## Need → component

| Need | Use |
|---|---|
| Action | `Button` (variants: default, outline, secondary, ghost, destructive, link; `loading` prop), `ButtonGroup`, `LoadingButton` |
| Icon-only action | `Button size='icon'` with `aria-label`, plus `Tooltip` |
| Text, number, money input | `Input`, `Textarea`, `NumberInput`, `CurrencyInput`, `PinInput`, `InputGroup` (prefix/suffix) |
| Labeled field with hint and error | `Field` (label, description, error) wrapping the control |
| Choice | `Checkbox`, `RadioGroup`, `Switch`, `ToggleGroup`, `Select`, `Combobox`, `Autocomplete`, `Slider`, `Rating` |
| Date and time | `DatePicker`, `DateRangePicker`, `DateTimePicker`, `MonthPicker`, `TimePicker`, `Calendar` |
| Files | `FileUpload` |
| Status or category | `Badge` (success, warning, info, destructive, solid-*) |
| Person | `Avatar` |
| Grouped content | `Card` (header, title, description, content, footer) |
| Key–value details | `DescriptionList` |
| Tabular data | `Table` + `Pagination` |
| Sections in a page | `Tabs`, `Accordion`, `Collapsible`, `Separator` |
| Steps of a process | `Stepper`; history of events: `Timeline` |
| Navigation | `Sidebar` (app shell), `Breadcrumb`, `Tabs` (in-page), `Command` (search / command palette) |
| Short task over the page | `Dialog`; confirmation of destructive action: `AlertDialog` |
| Side panel (detail, filters, edit) | `Sheet`; on mobile: `BottomSheet` |
| Small contextual content | `Popover`, `DropdownMenu` (row and overflow actions), `Tooltip` |
| Feedback | Toasts: `Toaster` once in the layout, `toast()` from `sonner` for action results, `Alert` (persistent message in the page), `Progress` |
| Loading | `Skeleton` shaped like the content |
| Nothing to show | `Empty` (icon, title, description, primary action) |
| Notifications inbox | `NotificationsPopover` |
| Charts | `ChartContainer` + `ChartTooltip` (Recharts, theme colors `chart-1`…`chart-5`) |
| Copy to clipboard | `CopyButton` |
| Keyboard shortcut hint | `Kbd` |

## Page patterns

Typical pages for each surface are listed in `surfaces.md`. Build them from the components above.

## Composition rules

- Feature components live in the app and compose kit components: `MemberTable`, `InviteMemberDialog`, `HeroSection`, `ProductCard`.
- Surface-specific blocks (marketing sections, product cards, cart, checkout steps) are app code, never kit components.
- Pass data and callbacks through props; keep fetching and mutations in the app's data layer.
- Use the kit's variants and sizes before adding `className`; use `className` for layout (spacing, grid, width), not to restyle colors.
- Use Base UI's `render` prop for links styled as buttons: `<Button render={<Link href='/members/new' />}>Invite</Button>`.
