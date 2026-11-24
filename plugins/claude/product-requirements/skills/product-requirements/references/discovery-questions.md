# Discovery Questions

Use this list to find gaps and pick probing questions, not as a questionnaire. In guided mode, turn them into one blocking decision per turn with options and a recommendation, as described in `collaborative-loop.md`. In fast mode, do not ask — record gaps as assumptions or open questions.

## Essentials (ask if missing)

1. **Problem** — What problem are we solving, and for whom?
2. **Users** — Who is the primary user? Is there a secondary user or buyer?
3. **Goal** — What outcome would make this a success in 3–6 months?
4. **Scope** — What is the smallest version worth shipping? What is explicitly out?
5. **Constraints** — Any fixed deadline, budget, platform, regulation, or dependency?

## Problem and evidence

- How do users solve this today? What is painful about it?
- What evidence do we have (data, research, support tickets, sales feedback)?
- What happens if we do nothing?
- Is this a new capability, an improvement, or a fix?

## Users and context

- Which personas or segments are in scope? Which are not?
- In what context do they use the product (device, frequency, environment, expertise)?
- Are there accessibility, localization, or regional needs?
- Who else is affected (admins, support, partners)?

## Goals and metrics

- Which business goal does this support (acquisition, activation, retention, revenue, cost, compliance)?
- What metric moves if this works? What is the current baseline?
- What target and timeframe would we consider success? Failure?
- Are there guardrail metrics that must not get worse?

## Behavior and scope

- Walk through the main journey step by step. Where does it start and end?
- What are the edge cases: empty state, errors, permissions, limits, concurrency?
- What happens with existing data or existing users at launch?
- What needs configuration or admin control?
- Which notifications, emails, or audit logs are required?

## Constraints and dependencies

- Which teams, systems, or vendors must be involved?
- Are there legal, privacy, security, or compliance requirements (GDPR, HIPAA, SOC 2, PCI)?
- Are there platform constraints (web, iOS, Android, desktop, API-only)?
- Any decisions already made that we must respect?

## Rollout

- Big-bang, phased, beta, or feature-flagged?
- Do we need migration, training, documentation, or support preparation?
- How will we roll back if something goes wrong?

## Asking well

- Prefer: "Who is the primary user? A) small-business admins ← recommended, the notes mention billing setup; B) individual freelancers; C) enterprise IT."
- Avoid: dumping ten questions at once, or asking without first showing a proposal and a recommendation.
- Avoid: drafting a full PRD from a one-line idea without confirming problem, users, and scope first.
- Stop asking when remaining unknowns would not change scope or requirements; list them as open questions.
