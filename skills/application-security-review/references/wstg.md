# OWASP WSTG — deep-mode test plan

Pinned to **WSTG 4.2** (the current versioned release; 5.0 is in development — do
not follow a "latest" branch). Activated only in **deep mode** (`--deep`, "test",
"pentest plan", or an explicit request to test).

Deep mode does not add more static findings. It turns the review into a **test
plan** — concrete things to attempt or verify against a running system — while the
Top 10:2025 + ASVS findings from standard mode still stand.

## Testing areas (WSTG 4.2)

1. **Information Gathering** — fingerprint the app, enumerate entry points, map
   the surface, find leaked info (comments, headers, error pages).
2. **Configuration and Deployment Management** — TLS config, HTTP methods,
   admin interfaces, old/backup files, cloud/storage exposure.
3. **Identity Management** — registration, account provisioning, username
   enumeration, role definitions.
4. **Authentication** — credentials over an encrypted channel, default creds,
   lockout, weak reset/remember-me, bypass, browser cache of credentials.
5. **Authorization** — directory traversal, privilege escalation, IDOR/BOLA,
   OAuth flows.
6. **Session Management** — cookie attributes, fixation, exposed variables,
   CSRF, logout, timeout, session puzzling.
7. **Input Validation** — reflected/stored/DOM XSS, SQL/NoSQL/LDAP/XML/command
   injection, SSRF, host header injection.
8. **Error Handling** — improper error output, stack traces, fail-open.
9. **Cryptography** — weak TLS, padding oracle, sensitive data over unencrypted
   channels.
10. **Business Logic** — logic flaws, abuse of workflows, request forgery,
    upload of malicious/unexpected files.
11. **Client-Side** — DOM XSS, JS execution, CSS/clickjacking, CORS, WebSockets,
    web messaging, storage.

For each relevant area, output the specific tests to run, the inputs to try, and
the expected secure behaviour — a checklist the developer or a tester can execute.
