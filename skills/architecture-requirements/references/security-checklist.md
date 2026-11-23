# Security Checklist

Apply to every design. Document which items apply, the chosen control, and any accepted risk. Skip items consciously, not by omission.

## 1. Threat modeling (lightweight)

1. List assets: sensitive data, credentials, money movements, admin capabilities.
2. List actors: anonymous users, authenticated users, tenants, admins, internal services, third parties, attackers.
3. Draw trust boundaries: browser ↔ API, API ↔ database, service ↔ third party.
4. For each boundary, walk through **STRIDE**:

| Threat | Question | Typical controls |
|---|---|---|
| **S**poofing | Can someone pretend to be another user/service? | Strong authentication, MFA, mTLS, signed tokens |
| **T**ampering | Can data be modified in transit or at rest? | TLS, integrity checks, signed webhooks, least-privilege writes |
| **R**epudiation | Can someone deny an action? | Audit logs with actor, time, and target |
| **I**nformation disclosure | Can data leak? | Authorization checks, encryption, minimal responses, log redaction |
| **D**enial of service | Can the system be overwhelmed? | Rate limits, quotas, timeouts, autoscaling, payload limits |
| **E**levation of privilege | Can someone gain more rights? | RBAC/ABAC, object-level authorization, input validation, sandboxing |

## 2. Identity and access

- [ ] Authentication method defined (OIDC/OAuth 2.0, SSO, passwords with strong hashing such as Argon2id/bcrypt, passkeys).
- [ ] MFA for admin and sensitive actions.
- [ ] Session/token lifetime, refresh, and revocation defined.
- [ ] Authorization model defined (roles, permissions, tenant isolation).
- [ ] Object-level authorization checked on every request (prevents IDOR/BOLA).
- [ ] Least privilege for service accounts, database users, and cloud IAM roles.

## 3. Data protection

- [ ] Data classified (Public / Internal / Confidential / Restricted).
- [ ] TLS 1.2+ for all traffic, including internal where feasible.
- [ ] Encryption at rest for databases, backups, and object storage.
- [ ] Key management via a managed KMS; keys rotated.
- [ ] Secrets in a secrets manager — never in code, config files in Git, or logs.
- [ ] Sensitive data redacted from logs, traces, and error messages.
- [ ] Retention and deletion defined for sensitive data, including backups.

## 4. Input and output handling

- [ ] All input validated server-side against a schema (type, length, format, range).
- [ ] Parameterized queries / ORM — no string-built SQL.
- [ ] Output encoding to prevent XSS; Content Security Policy for web apps.
- [ ] CSRF protection for cookie-based sessions.
- [ ] File uploads: type and size limits, malware scanning, stored outside web root, served with safe headers.
- [ ] SSRF protection for any feature that fetches user-supplied URLs.
- [ ] Safe deserialization; no execution of user-supplied code without sandboxing.

## 5. Application and infrastructure

- [ ] Dependencies pinned and scanned (SCA); update process defined.
- [ ] Container/base images minimal and scanned.
- [ ] Network segmentation: databases not publicly reachable; private subnets.
- [ ] Security headers (HSTS, X-Content-Type-Options, frame protection).
- [ ] Rate limiting and abuse protection on authentication and expensive endpoints.
- [ ] Admin interfaces protected (SSO, MFA, IP restrictions where appropriate).

## 6. Logging, monitoring, and response

- [ ] Security-relevant events logged: logins, failures, permission changes, data exports, admin actions.
- [ ] Audit logs tamper-resistant and retained per policy.
- [ ] Alerts for anomalies (brute force, privilege changes, unusual data access).
- [ ] Incident response owner and runbook identified.

## 7. Third parties and AI components

- [ ] Each third party's data access documented; DPA in place where personal data is shared.
- [ ] Webhooks and callbacks verified (signatures, timestamps, replay protection).
- [ ] For LLM/AI features: prompt-injection risks considered, model output treated as untrusted input, tool permissions scoped, sensitive data not sent to providers without approval.

## 8. Compliance mapping

| Regulation / standard | Applies? | Key obligations | Design response |
|---|---|---|---|
| GDPR / privacy laws | | Lawful basis, consent, data subject rights, residency | |
| PCI DSS | | Card data scope reduction (prefer a tokenizing provider) | |
| HIPAA | | PHI safeguards, BAAs, audit | |
| SOC 2 / ISO 27001 | | Access control, change management, monitoring | |

Reference: OWASP Top 10 and OWASP API Security Top 10 for common vulnerability classes.
