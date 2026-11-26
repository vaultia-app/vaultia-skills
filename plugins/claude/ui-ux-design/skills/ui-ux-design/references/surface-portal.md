# Surface: Portal

Admin portals, dashboards, back offices, SaaS apps, and customer account areas: signed-in users who come back often to get work done.

## What good looks like

- **Efficiency for repeat users:** fewer clicks for frequent tasks, keyboard support, remembered filters.
- **Accuracy:** clear status, validation before saving, confirmation for destructive or bulk actions.
- **Orientation:** the user always knows where they are and what they can do with their role.

Success is measured by task completion time, error rate, and support requests, not by visits or conversion.

## Screen set

Derive screens from the requirements; a portal usually has: app shell, dashboard, list and detail pages per main object, create and edit forms, settings, profile, and auth (sign in, reset password, invitation).

## Layout and navigation

- **App shell:** `Sidebar` grouped by information architecture, header with `Breadcrumb`, search or `Command` (⌘K), `NotificationsPopover`, and a user menu. Collapse the sidebar to icons or a sheet on small screens.
- Hide or disable navigation items the role cannot use, as the permissions file says.
- Data pages use the full width; forms and reading content use a max width.

## Page patterns

### List page
Header (title, count, primary action) → toolbar (search, filters as `Select`/`Combobox`/`DateRangePicker`, active filter chips) → `Table` with status `Badge`s and a row `DropdownMenu` → `Pagination`. Support bulk selection with a bulk action bar when the requirements need it. Keep search, filters, sort, and page in the URL.

### Detail page
`Breadcrumb` → header (title, status `Badge`, actions) → `Tabs` or sections of `Card` + `DescriptionList` → related lists or `Timeline` (history, audit). Edit in a `Sheet` for short edits, or on an edit page for long ones.

### Form
Group fields in sections; one column on mobile; `Field` for every control; primary action at the end, secondary next to it. Validate on blur and on submit; keep input after errors; `loading` on submit; warn about unsaved changes.

### Dashboard
KPI `Card`s (value, change, period) → charts (`ChartContainer`) with a period filter → recent activity (`Table` or `Timeline`). Every widget has its own loading, empty, and error state. Show only metrics that lead to a decision or action.

### Settings
Navigation or `Tabs` by topic → sections of `Card` with `Field`s → save per section, toast on success.

### Auth
Centered `Card`, logo, one primary action, clear errors, password visibility toggle (`InputGroup`), "forgot password" link.

## Visual defaults

- Theme: the product's brand, applied with restraint; `primary` for the main action and current selection only.
- Density: comfortable by default; offer compact (`size='sm'`, tighter rows) for data-heavy roles.
- Typography: default kit sizes; `tabular-nums` for numbers.

## Technical priorities

- Pages are behind sign-in: no SEO work; client-side rendering is fine.
- Fast perceived speed: skeletons, optimistic updates where safe, no full-page reloads.
- Respect roles in the UI, and never rely on the UI alone for permission checks (the API enforces them).

## Checklist additions

- [ ] Each role sees only the navigation and actions it may use.
- [ ] Bulk and destructive actions confirm the scope ("Delete 12 members?") and report the result.
- [ ] Tables: sortable where useful, sticky header for long lists, horizontal scroll on mobile.
- [ ] Frequent actions reachable by keyboard; `Command` palette for large portals.
- [ ] Filters and pagination survive reload and back navigation.
- [ ] Timestamps show time zone or relative time consistently.
