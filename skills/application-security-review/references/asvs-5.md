# OWASP ASVS 5.0 — backbone checklist

ASVS 5.0.0 (released 2025-05-30) is the review backbone: it states the security
*properties* the application should have. This is a **working review map at L1/L2
depth** — the highest-yield checks per chapter, not the full ~350 requirements.
For L3 or exact requirement wording, consult the ASVS 5.0.0 document and cite
requirements as `ASVS Vx.y.z`. **Do not invent requirement numbers** — cite the
chapter (`Vx`) when you do not know the exact sub-id.

The 17 chapters:

## V1 — Encoding and Sanitization
- Output is contextually encoded at the sink (HTML, attribute, JS, URL, SQL) —
  encoding matches the context, not a single global escape.
- User input reaching an interpreter (SQL, OS command, LDAP, XPath, template) is
  parameterized or safely constructed, never string-concatenated.
- Rich/HTML input is sanitized with a vetted allow-list library, not a regex.

## V2 — Validation and Business Logic
- Input validated server-side against a positive (allow-list) schema; client
  validation is not trusted.
- Business rules enforce sequence, quantity, and ownership limits (no negative
  amounts, no step-skipping, no replay of one-time actions).
- Sensitive flows are rate-limited / anti-automation protected.

## V3 — Web Frontend Security
- Security headers set: CSP, X-Content-Type-Options, Referrer-Policy, frame
  protection.
- Cookies are `HttpOnly`, `Secure`, and `SameSite`; no sensitive data in
  `localStorage`.
- No `dangerouslySetInnerHTML` / `v-html` / `innerHTML` on unsanitized input.

## V4 — API and Web Service
- Content-Type enforced and validated; no unintended methods enabled.
- CORS is an explicit allow-list, not `*` with credentials.
- Errors do not leak stack traces, framework versions, or internal paths.

## V5 — File Handling
- Uploads validated by type/size; stored outside the web root; filenames not
  attacker-controlled paths (no traversal).
- Downloads/reads resolve within an allowed base directory.

## V6 — Authentication
- Passwords stored with a memory-hard KDF (argon2/bcrypt/scrypt), never MD5/SHA1.
- Login has lockout / rate limiting; credential-stuffing resistance.
- MFA available for sensitive operations; secure password-reset flow.

## V7 — Session Management
- Session id rotated on privilege change (login); invalidated on logout.
- Idle and absolute timeouts; no session fixation.
- Tokens are unpredictable and never placed in URLs.

## V8 — Authorization
- Every object accessed by id is checked against the caller's ownership/role
  (guards BOLA); function-level authz enforced server-side (guards BFLA).
- Deny-by-default on new routes; authorization decisions centralized, not
  scattered per handler.

## V9 — Self-contained Tokens
- JWTs verify signature and algorithm (reject `alg:none`); `exp`/`aud`/`iss`
  validated; no sensitive data in the payload.
- Keys rotated; symmetric secrets not shared across trust boundaries.

## V10 — OAuth and OIDC
- Authorization Code + PKCE for public clients; `state` and `nonce` validated.
- Redirect URIs strictly allow-listed; tokens scoped least-privilege.

## V11 — Cryptography
- Vetted algorithms only (AES-GCM, not ECB); no hard-coded keys/secrets in
  source; secrets from a manager/env, not the repo.
- Secure random for tokens/IVs; correct IV/nonce handling.

## V12 — Secure Communication
- TLS enforced end to end; HSTS set; no mixed content; no downgrade to plaintext.
- Certificate validation not disabled in clients.

## V13 — Configuration
- No debug/verbose mode in production; secure defaults; least-privilege service
  accounts.
- Dependencies pinned with a committed lockfile; no install-time code execution.

## V14 — Data Protection
- Sensitive data classified; PII encrypted at rest where required; least data
  retained.
- Caching/headers prevent sensitive responses being stored; no secrets in logs.

## V15 — Secure Coding and Architecture
- Trust boundaries explicit; unsafe deserialization avoided; SSRF egress
  controls on server-side fetches.
- Third-party code and supply chain vetted; dangerous sinks reviewed.

## V16 — Security Logging and Error Handling
- Security events (authn, authz failures, input rejection) logged with enough
  context; secrets never logged.
- Errors fail closed; responses do not expose internal detail; alerting on
  repeated failures.

## V17 — WebRTC
- Signaling authenticated; media (DTLS-SRTP) encryption enforced; TURN
  credentials scoped and short-lived.
- (Skip unless the app uses WebRTC — see framework-selection.)
