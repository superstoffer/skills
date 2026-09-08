# Report format

Deterministic output so reviews are comparable. Open with a coverage header, then
findings most-severe first, then an overall verdict.

## Coverage header

State which frameworks were applied and why — so the reader can see what was and
was not in scope.

```
# Application Security Review — <target>
Frameworks applied: ASVS 5.0; OWASP Top 10:2025[; API Security Top 10:2023 — API surface detected]
Mode: Standard | Deep (WSTG test plan appended)
Scope: <files / modules / feature reviewed>
```

## Finding block (repeat, most severe first)

```
### [SEVERITY] <short title>
- Frameworks: OWASP Top 10 A0x:2025 — <name>; ASVS Vx[.y.z]; [API Security APIx:2023 — <name>]
- Location: <file>:<line>
- Problem: <what is wrong, concretely>
- Abuse scenario: <realistic path from this to harm>
- Remediation: <concrete fix>
- OWASP guidance: <relevant Cheat Sheet name(s) — from cheat-sheet-index.md>
- Confidence: High | Medium | Low
```

**Severity is impact × exploitability, and is independent of confidence.** A
plausible-but-unconfirmed Critical is still Critical, reported at lower
confidence. Cite the exact ASVS sub-id (`Vx.y.z`) only when you know it; otherwise
cite the chapter (`Vx`) — never invent a requirement number.

## Worked example — the finding that "looks clean"

```
### [High] Invoice endpoint has no ownership check
- Frameworks: OWASP Top 10 A01:2025 — Broken Access Control; ASVS V8;
  API Security API1:2023 — Broken Object Level Authorization
- Location: src/routes/invoices.ts:42
- Problem: GET /api/invoices/:id returns the record for any id; the handler
  never verifies the authenticated user owns that invoice.
- Abuse scenario: an authenticated user enumerates :id and reads every
  customer's invoices (BOLA).
- Remediation: scope the query to the caller — where: { id, ownerId: req.user.id }
  — and return 404 on a miss. Enforce authorization server-side, deny by default.
- OWASP guidance: Authorization Cheat Sheet; Insecure Direct Object Reference
  Prevention Cheat Sheet
- Confidence: High
```

## Verdict footer

```
## Overall risk: Critical | High | Medium | Low
## Blockers (fix before release): ...
## Recommended hardening: ...
```
