# Writing Acceptance Criteria

Acceptance criteria define when a requirement is **done**. They must be observable and verifiable by someone who did not write them.

## Format

Prefer **Given / When / Then**:

```text
AC-<FR#>.<n>: Given <precondition/context>,
             when <actor performs action or event occurs>,
             then <observable, verifiable outcome>.
```

Use a short **rule-based checklist** when Given/When/Then is awkward (validation rules, display rules):

```text
AC-3.1: Password must be 12–128 characters.
AC-3.2: Password must not match any of the user's last 5 passwords.
```

## Rules

1. **One behavior per criterion.** Split "and" statements that test different things.
2. **Observable outcomes.** Describe what the user or system visibly does, not internal implementation.
3. **Concrete values.** Use numbers, limits, and specific messages where they matter.
4. **Cover the unhappy paths.** Include errors, empty states, permission denials, limits, and timeouts — not just the happy path.
5. **Traceable.** Every criterion belongs to exactly one functional requirement (`AC-1.2` → `FR-1`). Both IDs are local to the feature spec; from other documents, write `F04/AC-1.2`.
6. **Implementation-neutral.** No database tables, endpoints, or frameworks unless they are a business constraint.

## Coverage checklist per requirement

- [ ] Happy path
- [ ] Invalid input / validation
- [ ] Permissions / unauthorized access
- [ ] Empty state / first use
- [ ] Limits and boundaries (max size, rate, count)
- [ ] Failure of a dependency (network, third-party)
- [ ] Concurrency or duplicates, when relevant

Not every item applies; skip consciously, not by omission.

## Vague → testable

| Vague | Testable |
|---|---|
| The page loads fast. | Given a typical account (≤ 500 items), when the dashboard opens, then content is visible within 2 seconds at p95. |
| The user is notified. | Given an export finishes, when the user is offline, then they receive an email within 5 minutes containing a download link valid for 7 days. |
| Errors are handled gracefully. | Given the payment provider times out, when the user submits payment, then they see "Payment could not be processed, you have not been charged" and the order remains in Draft. |
| Easy to use. | Given a first-time user, when they follow the onboarding, then they can create their first project in ≤ 3 steps without leaving the page. |

## Example

**FR-2:** The system shall let a workspace admin invite members by email.

- AC-2.1: Given an admin on the Members page, when they submit a valid email, then an invitation email is sent and the invitee appears as "Pending".
- AC-2.2: Given the email already belongs to a member, when the admin submits it, then the system shows "Already a member" and sends no email.
- AC-2.3: Given a non-admin member, when they open the Members page, then the invite control is not shown.
- AC-2.4: Given a pending invitation older than 14 days, when the invitee opens the link, then they see "Invitation expired" and can request a new one.
- AC-2.5: Given the workspace has reached its seat limit, when the admin invites a member, then the system blocks the invitation and shows the upgrade option.
