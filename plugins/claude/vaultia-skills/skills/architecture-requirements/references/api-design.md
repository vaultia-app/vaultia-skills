# API Design Guidelines

Specify interfaces precisely enough that two teams could implement client and server independently. In an existing codebase, follow its established conventions first; use these guidelines for gaps.

## Choose the style

| Style | Best for | Trade-off |
|---|---|---|
| **REST over HTTP/JSON** | Public and CRUD-oriented APIs, broad client compatibility, caching | Over/under-fetching for complex UIs |
| **GraphQL** | Client-driven queries over a rich graph, many UI variants | Caching, authorization per field, query cost control |
| **gRPC** | Internal service-to-service, low latency, streaming, strong contracts | Browser support needs a proxy; less human-readable |
| **Async events / messages** | Decoupled notifications, background processing | Eventual consistency, schema evolution |
| **Webhooks** | Pushing events to external consumers | Delivery guarantees, security, consumer downtime |

## What to specify for every operation

- **Purpose** and the requirement it serves (`FR-n`).
- **Method and path / RPC name / event name.**
- **Request:** parameters, body schema, required vs. optional, validation rules.
- **Response:** success schema and status codes.
- **Errors:** status codes and error body; every error the client must handle.
- **Auth:** authentication scheme and required permissions/scopes.
- **Idempotency:** safe to retry? Idempotency key required?
- **Limits:** rate limits, payload size, pagination limits.
- **Consistency:** synchronous result or eventual (and how the client learns completion).

Use a machine-readable contract when practical: OpenAPI for REST, protobuf for gRPC, SDL for GraphQL, AsyncAPI or JSON Schema for events.

## REST conventions

- Resource-oriented, plural nouns: `/v1/projects/{projectId}/tasks`.
- Methods: `GET` (read, safe), `POST` (create / non-idempotent action), `PUT` (full replace, idempotent), `PATCH` (partial update), `DELETE` (idempotent).
- Status codes: `200` OK, `201` Created (+ `Location`), `202` Accepted (async), `204` No Content, `400` validation, `401` unauthenticated, `403` forbidden, `404` not found, `409` conflict, `412` precondition failed, `422` semantic validation, `429` rate limited, `5xx` server errors.
- Consistent error body, e.g. RFC 9457 Problem Details:

```json
{
  "type": "https://example.com/errors/seat-limit-reached",
  "title": "Seat limit reached",
  "status": 409,
  "detail": "The workspace has used 10 of 10 seats.",
  "instance": "/v1/workspaces/42/invitations"
}
```

- **Pagination:** prefer cursor-based (`?limit=50&cursor=...`, response includes `nextCursor`) for large or changing collections; offset only for small, stable sets.
- **Filtering and sorting:** explicit, documented query parameters (`?status=open&sort=-createdAt`).
- **Idempotency:** `Idempotency-Key` header for `POST` operations that create or charge.
- **Concurrency:** `ETag` + `If-Match` for optimistic locking on updates.
- **Timestamps:** ISO 8601 in UTC; **IDs:** opaque strings.
- **Long-running operations:** return `202` with an operation resource to poll, or notify via webhook/event.

## Versioning and evolution

- Version public APIs from day one (`/v1/` or a header); internal APIs may rely on compatible evolution.
- Additive changes (new optional fields, new endpoints) are non-breaking.
- Breaking changes: removing/renaming fields, changing types or semantics, making optional fields required, changing error codes.
- Define a deprecation policy: announcement, `Deprecation`/`Sunset` headers, migration window.
- Clients must ignore unknown fields.

## Events

- Name events in past tense for facts: `invoice.paid`, `member.invited`.
- Include `id`, `type`, `occurredAt`, `version`, and a minimal payload (or a reference to fetch details).
- Assume at-least-once delivery: consumers must be idempotent.
- Document ordering guarantees (usually per aggregate/key only).

## Security for APIs

- Authenticate every request (OAuth 2.0 / OIDC tokens, signed API keys, mTLS internally).
- Authorize at the object level — check the caller can access *this* resource (prevents IDOR / BOLA).
- Validate all input against the schema; reject unknown fields where appropriate.
- Never expose internal errors, stack traces, or sensitive fields.
- Rate-limit and set payload size limits.
- Sign webhooks (HMAC with timestamp) and require HTTPS.
