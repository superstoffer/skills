# OWASP Cheat Sheet routing index

A map from topic to the OWASP Cheat Sheet **name** — not its content. Consult it
**only when proposing remediation**, and cite the sheet by name in a finding's
"OWASP guidance" line. Do not dump cheat sheets into every review.

| Topic | Cheat Sheet(s) |
|---|---|
| Authentication | Authentication; Multifactor Authentication; Credential Stuffing Prevention; Forgot Password |
| Session management | Session Management |
| Authorization | Authorization; Insecure Direct Object Reference Prevention |
| XSS | Cross Site Scripting Prevention; DOM based XSS Prevention |
| Content Security Policy | Content Security Policy |
| SQL / query injection | SQL Injection Prevention; Query Parameterization |
| OS command injection | OS Command Injection Defense |
| Deserialization | Deserialization |
| SSRF | Server Side Request Forgery Prevention |
| File upload | File Upload |
| Path traversal | (see Input Validation; File Upload) |
| Input validation | Input Validation |
| Cryptography | Cryptographic Storage; Key Management; Password Storage |
| Secrets | Secrets Management |
| Transport | Transport Layer Security; HTTP Strict Transport Security |
| JWT / tokens | JSON Web Token for Java (concepts apply broadly); JWT best practices |
| OAuth / OIDC | OAuth 2.0 Protocol; (see ASVS V10) |
| REST / API | REST Security; Web Service Security; Microservices Security |
| GraphQL | GraphQL |
| WebSocket | (see REST Security; input validation for messages) |
| Node.js / npm | Nodejs Security; NPM Security |
| Next.js | Nextjs Security |
| CI/CD & supply chain | CI CD Security; Vulnerable Dependency Management; Third Party Javascript Management |
| Logging | Logging |
| Error handling | Error Handling |
| Headers | HTTP Headers |
| AI features | AI Agent Security; MCP Security; LLM Prompt Injection Prevention |

Cheat Sheet names track the OWASP Cheat Sheet Series; if a name has drifted, cite
the closest current sheet and note it. These give implementation guidance only —
the finding's framework mapping still comes from Top 10 + ASVS.
