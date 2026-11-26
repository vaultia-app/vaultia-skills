# Example PRD (small feature)

A finished v1.0 for a small feature, to calibrate depth and tone. Note what it leaves out: sections that do not apply are omitted, not filled with TBD. A larger product uses more of the template, at the same level of precision.

---

````markdown
# Workspace Member Invitations — Product Requirements

| Field | Value |
|---|---|
| Status | Approved |
| Version | v1.0 |
| Owner | Product lead, Collaboration |
| Last updated | 2026-03-02 |

## 1. Summary

Workspace admins can invite teammates by email so a team can start collaborating without asking support to add accounts. Today 38% of new workspaces never add a second member, and support handles about 120 "please add my colleague" tickets a month.

## 2. Problem

- **Problem statement:** Admins cannot add teammates themselves, so new workspaces stay single-user and churn.
- **Evidence:** 120 support tickets/month (Jan–Feb 2026); single-member workspaces retain 3× worse at day 30.
- **Why now:** Team plans launch in Q2 and are priced per seat.

## 3. Goals and non-goals

- G-1: Admins add teammates without contacting support.
- G-2: More new workspaces become multi-member.
- **Non-goals:** SSO / SCIM provisioning; inviting by shareable link; guest (external) roles.

## 4. Target users

| Persona | Description | Primary need |
|---|---|---|
| Workspace admin | Person who created or manages the workspace | Add and remove teammates quickly |
| Invitee | Colleague receiving the invitation, may have no account | Join with as few steps as possible |

## 5. User journeys

### J-1: Invite a teammate
1. Admin opens **Members** and enters one or more emails.
2. Invitee receives an email and opens the link.
3. Invitee signs in or creates an account and lands in the workspace.

**Edge cases**
- E-1: Email already belongs to a member → AC-1.2
- E-2: Invitation expired → AC-2.2
- E-3: Seat limit reached → AC-1.4

## 6. Domain model and business rules

| Object | Meaning | Lifecycle |
|---|---|---|
| Invitation | An offer for one email to join one workspace | pending → accepted / expired / revoked |

- BR-1: An invitation expires 14 days after it is sent. Example: sent 2026-03-01 10:00 → valid until 2026-03-15 10:00 in the workspace's time zone.
- BR-2: Pending invitations count toward the seat limit. Example: plan of 10 seats, 8 members + 2 pending → no further invitations.

## 7. Functional requirements

| ID | Requirement | Priority | Journey |
|---|---|---|---|
| FR-1 | The system shall let a workspace admin invite members by email. | Must | J-1 |
| FR-2 | The system shall let an invitee accept an invitation from the email link. | Must | J-1 |
| FR-3 | The system shall let an admin revoke a pending invitation. | Should | J-1 |

## 8. Acceptance criteria

### FR-1: Invite by email
- AC-1.1: Given an admin on Members, when they submit a valid email, then an invitation email is sent and the invitee appears as "Pending".
- AC-1.2: Given the email already belongs to a member, when the admin submits it, then "Already a member" is shown and no email is sent.
- AC-1.3: Given a non-admin member, when they open Members, then the invite control is not shown.
- AC-1.4: Given the seat limit is reached (BR-2), when the admin invites, then the invitation is blocked and the upgrade option is shown.

### FR-2: Accept invitation
- AC-2.1: Given a valid invitation, when the invitee opens the link and signs in, then they land in the workspace as a member.
- AC-2.2: Given an expired invitation (BR-1), when the invitee opens the link, then "Invitation expired" is shown with a "Request a new invitation" action.

### FR-3: Revoke invitation
- AC-3.1: Given a pending invitation, when the admin revokes it, then the link shows "Invitation no longer valid" and the seat is freed.

## 10. Success metrics

| ID | Metric | Baseline | Target | Measurement |
|---|---|---|---|---|
| M-1 | New workspaces with ≥ 2 members by day 7 | 62% | 75% within 60 days of launch | `member_joined` events |
| M-2 | "Add member" support tickets per month | 120 | ≤ 20 | Support tag report |
| M-3 (guardrail) | Invitation emails marked as spam | unknown | < 0.3% | Email provider report |

## 11. Scope and release plan

- **In scope (v1):** FR-1 to FR-3.
- **Later:** bulk CSV invite, invitation links.
- **Rollout:** feature flag, 10% of new workspaces for one week, then all.
- **Kill switch:** the flag disables the invite control; pending links keep working.

## 13. Decisions, assumptions, and open questions

### Confirmed decisions
- D-1: Only admins can invite — Product lead, 2026-02-20
- D-2: 14-day expiry — Product lead, 2026-02-20

### Assumptions
- A-1: Invitees mostly use the same email domain as the admin — validate with launch data.

### Open questions (non-blocking)
- Q-1: Should admins get a reminder when an invitation expires? — Design, before v1.1

## Change log

| Version | Decisions applied | Sections changed |
|---|---|---|
| v0.1 | Initial proposal | All |
| v0.2 | D-1, D-2 | 5, 6, 8 |
| v1.0 | Approved | Status |
````
