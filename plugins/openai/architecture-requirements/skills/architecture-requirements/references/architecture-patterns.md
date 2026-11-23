# Architecture Patterns

Choose the simplest pattern that satisfies the drivers. Every added moving part must be justified by a named requirement.

## Architectural styles

| Style | Choose when | Avoid when | Main trade-off |
|---|---|---|---|
| **Modular monolith** | Small to mid-size team, one product, evolving domain, need for fast iteration | Parts need radically different scaling, release cadence, or tech stacks | Simple ops and transactions vs. one deployable unit |
| **Microservices** | Multiple teams need independent deployment; clear bounded contexts; uneven scaling needs | Small team, unclear domain boundaries, no mature DevOps/observability | Team autonomy vs. distributed-system complexity |
| **Serverless / functions** | Spiky or low traffic, event-driven tasks, minimal ops capacity | Long-running, latency-critical, or high steady load workloads; heavy vendor lock-in concerns | Low ops and cost at small scale vs. cold starts, limits, lock-in |
| **Event-driven** | Many consumers react to the same facts; decoupling producers from consumers; audit trails | Strong immediate consistency required across steps; team new to async debugging | Decoupling and extensibility vs. eventual consistency and harder tracing |
| **Layered / hexagonal (ports & adapters)** | Business logic must stay independent of frameworks, databases, and transports | Trivial CRUD with no meaningful domain logic | Testability and replaceability vs. extra abstractions |
| **CQRS** | Read and write models differ greatly in shape or scale | Simple CRUD; small data volumes | Optimized reads vs. sync complexity |
| **Event sourcing** | Full history is a business requirement (ledger, audit), temporal queries | Most CRUD apps; team unfamiliar with the pattern | Complete history vs. schema evolution and replay complexity |

**Default recommendation:** start with a well-structured modular monolith with clear module boundaries; extract services only when a driver requires it.

## Integration patterns

| Pattern | Use for | Watch out for |
|---|---|---|
| Synchronous request/response (REST, gRPC, GraphQL) | User-facing reads, commands needing an immediate answer | Cascading failures, latency chains — set timeouts, retries with backoff, circuit breakers |
| Asynchronous messaging (queue) | Background work, load leveling, retryable tasks | Idempotency, poison messages, dead-letter queues, ordering |
| Publish/subscribe (event bus) | Broadcasting domain events to multiple consumers | Schema evolution, duplicate delivery, eventual consistency |
| Webhooks | Notifying external systems | Signing, retries, replay protection, consumer downtime |
| Batch / ETL | Large periodic data movement, reporting | Freshness, partial failure recovery |
| Outbox pattern | Reliably publishing events with a database write | Requires a relay process; ordering per aggregate |
| Saga (orchestrated or choreographed) | Multi-service workflows without distributed transactions | Compensating actions must be designed explicitly |

## Data and scaling patterns

| Pattern | Use for |
|---|---|
| Read replicas | Read-heavy workloads tolerant of slight lag |
| Caching (in-process, distributed, CDN) | Hot reads; define TTL, invalidation, and stampede protection |
| Partitioning / sharding | Data or write volume beyond a single node; choose the key carefully |
| Multi-tenancy: shared schema / schema-per-tenant / database-per-tenant | Trade isolation and compliance against cost and operational overhead |
| Rate limiting and quotas | Protect shared resources and enforce plans |
| Bulkheads | Isolate failures between workloads |

## Resilience checklist

- Timeouts on every remote call.
- Retries only for idempotent operations, with exponential backoff and jitter.
- Circuit breakers for unstable dependencies.
- Graceful degradation: what does the user see when a dependency is down?
- Idempotency keys for operations that create or charge.
- Health checks and readiness probes.

## Decision heuristics

1. Start from the drivers, not from technology preferences.
2. Prefer boring, well-understood technology the team already operates.
3. Reversible decisions can be made quickly; irreversible ones (data store, public API, tenancy model) deserve an ADR and an alternative analysis.
4. Optimize for the expected scale of the next 12–24 months, not hypothetical extremes — but keep the path to the next order of magnitude clear.
5. Every new infrastructure component has an operational cost: monitoring, upgrades, on-call, expertise.
