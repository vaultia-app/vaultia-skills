# Non-Functional Requirements

Each NFR needs: a **measurable target**, the **conditions** under which it applies, a **design response**, and a **verification method**. Adjectives ("fast", "scalable", "highly available") are not requirements.

## NFR statement format

```text
NFR-<n> [<category>]: <metric> shall be <target> under <conditions>, verified by <method>.
```

Example: `NFR-2 [Performance]: Search API p95 latency shall be ≤ 300 ms at 200 requests/s with a 1M-document index, verified by load test in staging.`

## Categories and questions

| Category | Questions to answer | Typical metrics |
|---|---|---|
| **Performance** | What latency do users tolerate for key operations? Interactive vs. background? | p50/p95/p99 latency, throughput (req/s), time to first byte |
| **Scalability** | Expected users, data volume, and traffic today and in 12–24 months? Peak vs. average? | Concurrent users, req/s at peak, data growth per month |
| **Availability** | What does downtime cost? Maintenance windows allowed? | Uptime % (99.9% ≈ 43 min/month; 99.99% ≈ 4.3 min/month) |
| **Reliability / resilience** | Which failures must the system survive (node, zone, region, dependency)? | Error rate, MTBF, MTTR |
| **Disaster recovery** | How much data loss and downtime are acceptable after a disaster? | RPO (data loss window), RTO (recovery time) |
| **Security** | What data is sensitive? Who are the threat actors? | See security checklist |
| **Privacy** | Personal data collected? Consent, retention, deletion, residency? | Retention periods, deletion SLA, data regions |
| **Compliance** | Applicable regulations or certifications (GDPR, HIPAA, PCI DSS, SOC 2, ISO 27001)? | Controls mapped to requirements |
| **Observability** | How will we detect, diagnose, and alert on problems? | Log/metric/trace coverage, alert latency, SLO dashboards |
| **Maintainability** | Who will maintain this? How often will it change? | Deployment frequency, lead time, test coverage on critical paths |
| **Operability** | Deployment model, configuration, on-call expectations? | Deploy time, rollback time |
| **Usability / accessibility** | Accessibility standard? Supported devices and browsers? | WCAG 2.2 AA, supported browser matrix |
| **Localization** | Languages, time zones, currencies, formats? | Supported locales |
| **Cost** | Budget for infrastructure and third-party services? | Monthly cost ceiling, cost per user/transaction |
| **Portability / lock-in** | Must it run on multiple clouds or on-premises? | Supported environments |

## Defaults to propose (as assumptions) when the user has no numbers

Mark these clearly as **assumptions** and ask for confirmation when they drive design.

| Attribute | Reasonable default for a typical B2B/B2C web app |
|---|---|
| Interactive API latency | p95 ≤ 500 ms |
| Page load (largest contentful paint) | ≤ 2.5 s at p75 |
| Availability | 99.9% monthly |
| RPO / RTO | ≤ 15 min / ≤ 4 h |
| Accessibility | WCAG 2.2 AA |
| Encryption | TLS 1.2+ in transit, AES-256 at rest |
| Log retention | 30 days hot, 1 year archived (subject to privacy rules) |

## From SLA to design

The PRD states what the business promises customers (SLA) and what users notice (NFRs). Turn each into an internal target (SLO), the measurement behind it (SLI), a design response, and a check:

| PRD commitment | SLO (internal target) | SLI (what is measured) | Design response | Verification |
|---|---|---|---|---|
| Uptime 99.5% per month | 99.9% per month | Share of successful requests at the load balancer | Two app instances behind health checks; managed database with automatic failover | Synthetic checks every minute; monthly SLO report |
| Data restored to ≤ 24 h old within 8 h | RPO ≤ 1 h, RTO ≤ 4 h | Age of the latest restorable backup; restore drill time | Point-in-time recovery; backups in a second region | Quarterly restore drill |

- Set the SLO stricter than the SLA, so the team is alerted before the promise is broken. The gap is the error budget.
- Trace each row to its PRD ID (`NFR-002`, the SLA table). A commitment with no design response is a blocking finding.
- When the PRD has no SLA, record "No SLA" and still set SLOs for the key flows.

## Trade-offs to make explicit

- Consistency vs. availability during partitions.
- Latency vs. cost (caching, replicas, regions).
- Availability targets vs. operational complexity (each extra "9" costs roughly an order of magnitude more effort).
- Security controls vs. user friction.
- Time to market vs. scalability headroom.

## Verification methods

Load and stress tests, chaos/failure injection, DR drills, security scans and penetration tests, accessibility audits, SLO monitoring in production, cost dashboards.
