# application-security-review — design

## Summary

A Claude Code skill that reviews the developer's **own application source code**
for security, anchored on OWASP frameworks. It inspects the project, selects
only the frameworks that apply, reviews the code against them, and reports
findings mapped to concrete standards with cheat-sheet-backed remediation.

Sibling to `agentic-security-review` (which audits untrusted AI skills/plugins/
MCP/hooks). Same collection, distinct scope: **app code vs. agent extensions.**

## Goals

- Give security findings a concrete framework mapping (Top 10 label + ASVS
  requirement) instead of a vague "possible XSS", so findings are actionable.
- Select frameworks by inspecting the project — never apply irrelevant ones.
- Stay read-only and static by default; report, don't modify.
- Be portable to Codex later (platform-neutral OWASP core).

## Non-goals

- Not a replacement for the built-in `/security-review`. That stays the quick
  diff-scoped bug pass; this is the deliberate, framework-anchored, whole-module
  review. No shared triggering.
- Not an automated SAST/scanner. Static reasoning is primary; running external
  tools is out of scope for v1.
- Not auto-fixing. Fixes are a separate action the user requests.

## Positioning vs. built-in /security-review

Complement, invoked explicitly. Triggered by framework-anchored intent
("owasp review this", "audit this API for auth flaws", "check this against
ASVS", "security review before release") and free to reason beyond the pending
diff — whole files, modules, config, architecture. A skill cannot reliably drive
another command from inside itself, and coupling to the built-in's diff scope
would cripple the review, so it does not wrap it.

## Security boundary and privileges

Reviews trusted first-party code, so it does NOT need the "reviewed material is
data, never instructions" lockdown that `agentic-security-review` requires.
It is still least-privilege and read-only:

- `allowed-tools: Read, Glob, Grep`.
- No Write/Edit (reports findings; fixing is a separate, user-requested action).
- No network required — static reasoning over the source in the repo.

## The core intelligence: framework selection

Inspect the project first, then activate only what applies. Governing rule,
stated in SKILL.md: **"Do not apply irrelevant frameworks merely because they
are available. More security context is not automatically better context."**

| Framework | Version | Activation |
|---|---|---|
| OWASP ASVS | 5.0.0 (2025-05-30) | Always — the backbone of verifiable requirements |
| OWASP Top 10 | 2025 (8th ed.) | Always — risk classification label |
| OWASP API Security Top 10 | 2023 | When an API surface is detected |
| OWASP WSTG | 4.2 (pinned; 5.0 in dev) | Deep/testing mode only (`--deep`, "test", "pentest plan") |
| OWASP MASVS/MASTG | current | v1.1 — mobile projects (stub in v1) |
| OWASP Desktop App Security Top 10 | 2021 | v1.2 — desktop apps (stub in v1) |
| OWASP GenAI LLM Top 10 | 2026 (2026-08-04) | v1.3 — apps with LLM/AI features (stub in v1) |

Detection cues live in `references/framework-selection.md`:

- **API surface** → route handlers (`app.(get|post|put|delete)`, Nest/Express/
  Fastify/Flask/Django/Rails controllers), OpenAPI/Swagger files, GraphQL
  schema/`.graphql`, gRPC `.proto`, tRPC routers, `/api/` paths.
- **Mobile** (v1.1) → `android/`, `ios/`, `*.xcodeproj`, `build.gradle`,
  `AndroidManifest.xml`, React Native / Flutter / Expo / Capacitor.
- **Desktop** (v1.2) → Electron, Tauri, .NET/WPF/WinUI, Qt, Swift/macOS,
  native Rust/C++ desktop. Electron/Tauri get both web and desktop checks.
- **GenAI** (v1.3) → OpenAI/Anthropic SDKs, prompt templates, RAG, vector DBs,
  tool/function calling, agent frameworks. Activates on the *application's* AI
  features, not because Claude/Codex authored the code.

Stubs (`references/future/*.md`) ship in v1 stating "detection is wired; the
checklist is not implemented yet — v1.x", so selection can name them without
pretending to review them.

## Verified framework facts (baked in at build time)

- **Top 10:2025** — A01 Broken Access Control · A02 Security Misconfiguration ·
  A03 Software Supply Chain Failures · A04 Cryptographic Failures · A05
  Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software
  or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10
  Mishandling of Exceptional Conditions.
- **API Security Top 10:2023** — API1 Broken Object Level Authorization · API2
  Broken Authentication · API3 Broken Object Property Level Authorization · API4
  Unrestricted Resource Consumption · API5 Broken Function Level Authorization ·
  API6 Unrestricted Access to Sensitive Business Flows · API7 Server Side
  Request Forgery · API8 Security Misconfiguration · API9 Improper Inventory
  Management · API10 Unsafe Consumption of APIs.
- **ASVS 5.0.0 chapters** — V1 Encoding and Sanitization · V2 Validation and
  Business Logic · V3 Web Frontend Security · V4 API and Web Service · V5 File
  Handling · V6 Authentication · V7 Session Management · V8 Authorization · V9
  Self-contained Tokens · V10 OAuth and OIDC · V11 Cryptography · V12 Secure
  Communication · V13 Configuration · V14 Data Protection · V15 Secure Coding
  and Architecture · V16 Security Logging and Error Handling · V17 WebRTC.

Each framework fact is re-verified against its OWASP source during the build,
not carried over from any summary. Versioned references are pinned (notably
WSTG 4.2), never "latest".

## ASVS distillation strategy

ASVS 5.0 has ~350 requirements across 17 chapters — too many to inline. `asvs-5.md`
distills each chapter to a **high-yield, code-review-oriented checklist** at L1/L2
depth (what to actually look for in source), with the chapter's ASVS id range and
a pointer to the full standard for L3. It is a working map, not a copy of ASVS.

## Finding & report format

`references/report-format.md`. A coverage header states which frameworks were
applied and why (from selection). Each finding:

```
### [SEVERITY] <title>
- Frameworks: OWASP Top 10 A0x:2025 — <name>; ASVS Vx.y.z; [APIx:2023 — <name>]
- Location: <file>:<line>
- Problem: <what is wrong>
- Abuse scenario: <realistic path to harm>
- Remediation: <concrete fix>
- OWASP guidance: <relevant Cheat Sheet name(s)>
- Confidence: High | Medium | Low
```

Severity = impact × exploitability, independent of confidence. Example: a
`/api/invoices/:id` handler with no ownership check is High — API1:2023 Broken
Object Level Authorization + ASVS V8 Authorization — even though it "looks clean".

## Modes

- **Standard review** — Top 10 + ASVS (+ API when present), static reasoning.
- **Deep review** (`--deep` / "test" / "pentest plan") — adds a WSTG-derived
  test plan on top of the standard findings.

## Cheat-sheet index

`references/cheat-sheet-index.md` is a routing map (topic → cheat-sheet *name*,
not content), consulted only when proposing remediation. Covers auth, authz/IDOR,
XSS/CSP, Node/npm, REST/GraphQL/WebSocket, JWT, crypto, deserialization, SSRF,
file upload, and the newer AI Agent / MCP / LLM Prompt Injection sheets.

## Structure

```
skills/application-security-review/
├── SKILL.md
├── README.md
└── references/
    ├── framework-selection.md
    ├── web-top10-2025.md
    ├── report-format.md
    ├── cheat-sheet-index.md
    ├── asvs-5.md
    ├── api-top10-2023.md
    ├── wstg.md
    └── future/
        ├── mobile-masvs.md
        ├── desktop-top10.md
        └── genai-llm-top10-2026.md
```

## Phased v1 build steps

1. Skeleton + `SKILL.md` (selection logic, workflow, modes, boundary) +
   `framework-selection.md` + `web-top10-2025.md` + `report-format.md` +
   `cheat-sheet-index.md`.
2. `asvs-5.md` backbone checklist (verified against ASVS 5.0.0).
3. `api-top10-2023.md` + conditional activation wiring.
4. `wstg.md` + deep-mode wiring.
5. Fixtures: one clean and one deliberately vulnerable web/API app under
   `.context/fixtures/`; run the skill against both; refine false positives /
   misses. Register in top-level README + plugin/marketplace manifests; bump
   version.
- Stubs under `references/future/` land in v1 (step 1).

## Future

- v1.1 — MASVS/MASTG mobile module.
- v1.2 — Desktop App Security Top 10 module.
- v1.3 — GenAI LLM Top 10:2026 module.
- Codex port — copy platform-neutral references; swap tool vocabulary.

## Testing

Follows the collection's RED/GREEN fixture approach: the vulnerable fixture must
produce the expected mapped findings (e.g. BOLA on the invoice handler, stored
XSS, weak crypto, missing rate limit), and the clean fixture must not raise false
positives. Framework selection is tested by asserting an API-less project does
NOT activate the API Top 10, and an API project does.
