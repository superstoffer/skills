# application-security-review — fixture validation results

Run 2026-09-08 against three throwaway fixtures under `.context/fixtures/`
(gitignored): `appsec-vuln` (Express billing API with planted defects),
`appsec-clean` (same app, fixed), `appsec-nolib` (a pure string library, no API).

## Framework selection (discrimination test)

| Fixture | API surface signals | Frameworks activated | Expected? |
|---|---|---|---|
| appsec-vuln | 3 (Express routes, `/api/`) | ASVS 5.0 + Top 10:2025 + API Top 10:2023 | ✅ |
| appsec-clean | 3 | ASVS 5.0 + Top 10:2025 + API Top 10:2023 | ✅ |
| appsec-nolib | 0 | ASVS 5.0 + Top 10:2025 only (no API Top 10) | ✅ |

Selection correctly withholds the API Top 10 from the no-API library — the
"don't apply irrelevant frameworks" rule holds.

## RED — planted defects in `appsec-vuln` (all detected, correctly mapped)

| # | Planted defect | File:line | Frameworks | Detected |
|---|---|---|---|---|
| 1 | Invoice fetched by id with no ownership scope (BOLA) | `src/routes/invoices.js:7` | A01:2025; ASVS V8; API1:2023 | ✅ |
| 2 | MD5 for password hashing | `src/routes/auth.js:9` | A04:2025; ASVS V6/V11 | ✅ |
| 3 | Hard-coded signing key in source | `src/routes/auth.js:6` | A04:2025; ASVS V11; V13 | ✅ |
| 4 | No rate limiting / lockout on `/api/login` | `src/routes/auth.js` | A07:2025; API4:2023; ASVS V6 | ✅ |
| 5 | `exec()` built from `req.query.name` (command injection) | `src/routes/reports.js:8` | A05:2025; ASVS V2 | ✅ |
| 6 | Unescaped user input in HTML response (XSS) | `src/routes/reports.js:10` | A05:2025; ASVS V1; V3 | ✅ |

## GREEN — `appsec-clean` (no false positives)

Each fixed line no longer matches its defect cue: invoice query scoped to
`ownerId: req.user.id` (404 on miss); argon2 + `process.env.JWT_SECRET`;
`express-rate-limit` on login; `execFile` with an argv array + input allow-list;
`escape-html` on both interpolations. No Critical/High findings remain.

## Conclusion

The skill's methodology detects every planted defect with the correct three-way
framework mapping, produces no false positives on the remediated code, and
selects frameworks by actual project surface. v1 validated.

Example finding output (format from `report-format.md`), defect #1:

```
### [High] Invoice endpoint has no ownership check
- Frameworks: OWASP Top 10 A01:2025 — Broken Access Control; ASVS V8;
  API Security API1:2023 — Broken Object Level Authorization
- Location: src/routes/invoices.js:7
- Problem: GET /api/invoices/:id returns the record for any id; the handler
  never verifies the authenticated user owns that invoice.
- Abuse scenario: an authenticated user enumerates :id and reads every
  customer's invoices.
- Remediation: scope the query to req.user.id (where: { id, ownerId }); 404 on
  a miss; enforce authorization server-side, deny by default.
- OWASP guidance: Authorization Cheat Sheet; Insecure Direct Object Reference
  Prevention Cheat Sheet
- Confidence: High
```
