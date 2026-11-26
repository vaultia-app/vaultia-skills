# Example Feature Spec

A finished v1.0 spec for a small feature, plus the rows it added to the shared files. Use it to calibrate depth and tone. Note what it leaves out: sections that do not apply are omitted, and shared rules and decisions are referenced by ID instead of repeated.

## The spec: `docs/03-functional-specs/F04-members.md`

````markdown
# F04 — Workspace Member Invitations

| Field | Value |
|---|---|
| Status | Approved |
| Version | v1.0 |
| Priority | Must |
| Release | MVP |
| Owner | Product lead, Collaboration |
| Last updated | 2026-03-02 |
| Related | D-007, D-008, Q-004 |

## 1. Summary

Workspace admins can invite teammates by email so a team can start collaborating without asking support to add accounts. Today 38% of new workspaces never add a second member, and support handles about 120 "please add my colleague" tickets a month.

## 2. Problem and goals

- **Problem:** Admins cannot add teammates themselves, so new workspaces stay single-user and churn.
- **Evidence:** 120 support tickets/month (Jan–Feb 2026); single-member workspaces retain 3× worse at day 30.
- **Contributes to:** G-2 (more teams active in their first month)
- **Feature goals:** admins add teammates without support; more new workspaces become multi-member.
- **Non-goals:** SSO / SCIM provisioning; invitation links; guest roles.

## 3. Users

| Actor | Need in this feature |
|---|---|
| Workspace admin | Add and remove teammates quickly |
| Invitee | Join with as few steps as possible, even without an account |

## 4. User journeys

### J-1: Invite a teammate

1. Admin opens **Members** and enters one or more emails.
2. Invitee receives an email and opens the link.
3. Invitee signs in or creates an account and lands in the workspace.

**Edge cases**
- E-1: Email already belongs to a member → AC-1.2
- E-2: Invitation expired → AC-2.2
- E-3: Seat limit reached → AC-1.4

## 5. Business objects and rules

- **Objects:** Invitation (new), Member, Workspace
- **Rules:** BR-012 invitations expire after 14 days; BR-013 pending invitations count toward the seat limit.

## 6. Functional requirements

| ID | Requirement | Priority | Journey |
|---|---|---|---|
| FR-1 | The system shall let a workspace admin invite members by email. | Must | J-1 |
| FR-2 | The system shall let an invitee accept an invitation from the email link. | Must | J-1 |
| FR-3 | The system shall let an admin revoke a pending invitation. | Should | J-1 |

## 7. Acceptance criteria

### FR-1: Invite by email
- AC-1.1: Given an admin on Members, when they submit a valid email, then an invitation email is sent and the invitee appears as "Pending".
- AC-1.2: Given the email already belongs to a member, when the admin submits it, then "Already a member" is shown and no email is sent.
- AC-1.3: Given a non-admin member, when they open Members, then the invite control is not shown.
- AC-1.4: Given the seat limit is reached (BR-013), when the admin invites, then the invitation is blocked and the upgrade option is shown.

### FR-2: Accept invitation
- AC-2.1: Given a valid invitation, when the invitee opens the link and signs in, then they land in the workspace as a member.
- AC-2.2: Given an expired invitation (BR-012), when the invitee opens the link, then "Invitation expired" is shown with a "Request a new invitation" action.

### FR-3: Revoke invitation
- AC-3.1: Given a pending invitation, when the admin revokes it, then the link shows "Invitation no longer valid" and the seat is freed.

## 9. Success metrics

| ID | Metric | Baseline | Target | Measurement |
|---|---|---|---|---|
| M-1 | New workspaces with ≥ 2 members by day 7 | 62% | 75% within 60 days of launch | `member_joined` events |
| M-2 | "Add member" support tickets per month | 120 | ≤ 20 | Support tag report |
| M-3 (guardrail) | Invitation emails marked as spam | unknown | < 0.3% | Email provider report |

## 10. Release

- **Rollout:** feature flag, 10% of new workspaces for one week, then all.
- **Kill switch:** the flag hides the invite control; pending links keep working.

## 12. Assumptions, defaults, and open items

### Assumptions
- A-1: Invitees mostly use the same email domain as the admin — validate with launch data.

### Decisions and open questions
- Decided: D-007 only admins can invite; D-008 14-day expiry (BR-012).
- Open: Q-004 should admins get a reminder when an invitation expires? (non-blocking, before v1.1)

## Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-02-18 | Initial proposal |
| v0.2 | 2026-02-20 | D-007, D-008 applied: sections 4, 5, 7 |
| v1.0 | 2026-03-02 | Approved |
````

## Rows it added to the shared files

`02-requirements/01-feature-list.md`

```markdown
| F04 | Workspace member invitations | [F04-members](../03-functional-specs/F04-members.md) | Must | MVP | Planned | |
```

`01-business/02-domain-model.md`

```markdown
| Invitation | An offer for one email to join one workspace | email, expiry date | pending → accepted / expired / revoked | F04 |
```

`01-business/03-business-rules.md`

```markdown
| BR-012 | An invitation expires 14 days after it is sent. | Sent 2026-03-01 10:00 → valid until 2026-03-15 10:00, workspace time zone | D-008 | F04 | ✅ Confirmed |
| BR-013 | Pending invitations count toward the seat limit. | 10 seats, 8 members + 2 pending → no further invitations | D-007 | F04 | ✅ Confirmed |
```

`09-working/decisions-log.md`

```markdown
| D-007 | Only workspace admins can invite members. | Members could invite too; rejected to keep seat costs under admin control. | Product lead | 2026-02-20 | F04, BR-013 | ✅ Confirmed |
| D-008 | Invitations expire after 14 days. | 7 days felt short for part-time teams; 30 days leaves stale seats. | Product lead | 2026-02-20 | F04, BR-012 | ✅ Confirmed |
```

`09-working/open-questions.md`

```markdown
| Q-004 | Should admins get a reminder when an invitation expires? | F04 | Design | Before v1.1 | Open | |
```
