# application-security-review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill that reviews the developer's own application source code against the OWASP frameworks that actually apply, mapping each finding to a concrete standard with cheat-sheet remediation.

**Architecture:** A `SKILL.md` entry point holds the framework-*selection* intelligence, the workflow, the two modes, and the read-only boundary. Reference files hold each framework's checklist and the routing indexes; the selection step decides which references to load. Platform-neutral OWASP content is kept free of Claude-specific vocabulary so it can port to Codex later.

**Tech Stack:** Markdown skill files (YAML frontmatter + Markdown body). Validation via shell `grep`, `find`, and a small Python `yaml.safe_load` check — no build system. Fixtures are throwaway app trees under `.context/fixtures/` (gitignored).

**Spec:** `docs/superpowers/specs/2026-09-08-application-security-review-design.md`. Every framework fact below is already verified against its OWASP source in the spec — reproduce it verbatim; do not paraphrase from memory.

---

## File structure

```
skills/application-security-review/
├── SKILL.md                    # selection rule, workflow, modes, boundary   (Task 1)
├── README.md                   # collection-convention overview               (Task 8)
└── references/
    ├── framework-selection.md  # detection cues → which frameworks activate   (Task 1)
    ├── report-format.md        # coverage header + finding block              (Task 1)
    ├── web-top10-2025.md        # A01–A10:2025 labels + code-review cues       (Task 2)
    ├── cheat-sheet-index.md     # topic → cheat-sheet name routing            (Task 2)
    ├── asvs-5.md                # V1–V17 backbone checklist                    (Task 3)
    ├── api-top10-2023.md        # API1–API10:2023, conditional                 (Task 4)
    ├── wstg.md                  # deep-mode WSTG 4.2 test areas                (Task 5)
    └── future/
        ├── mobile-masvs.md      # v1.1 stub                                    (Task 6)
        ├── desktop-top10.md     # v1.2 stub                                    (Task 6)
        └── genai-llm-top10-2026.md  # v1.3 stub                               (Task 6)
```

Fixtures (Task 7), not shipped: `.context/fixtures/appsec-clean/` and `.context/fixtures/appsec-vuln/`.

---

## Task 1: Skeleton — SKILL.md, framework-selection, report-format

**Files:**
- Create: `skills/application-security-review/SKILL.md`
- Create: `skills/application-security-review/references/framework-selection.md`
- Create: `skills/application-security-review/references/report-format.md`

- [ ] **Step 1: Write the SKILL.md frontmatter with read-tool pre-approvals.**

`allowed-tools` adds pre-approvals; it does not restrict other host-permitted
tools. The body instructs read-only behavior. Enforced isolation requires host
tool restrictions and filesystem/network controls, including MCP access.

Frontmatter (exact):

```yaml
---
name: application-security-review
description: >-
  Security-review the developer's own application source code against the OWASP
  frameworks that apply. Use when asked to review code for security, "owasp
  review this", audit an endpoint/API for auth or injection flaws, check code
  against ASVS or the OWASP Top 10, or do a security pass before a release.
  Inspects the project and applies only relevant frameworks — ASVS 5.0 and the
  Top 10:2025 always, the API Security Top 10 when an API is present, WSTG in a
  deep/testing pass. NOT for vetting a third-party or AI-generated skill/plugin/
  MCP/hook (use agentic-security-review); NOT the quick pending-diff pass of the
  built-in security-review. This is a deliberate, framework-anchored review of
  application code across whole files, modules, and configuration.
allowed-tools:
  - Read
  - Glob
  - Grep
---
```

- [ ] **Step 2: Write the SKILL.md body.**

Sections, in order:

1. **Title + one-line purpose.**
2. **Boundary** — reviews trusted first-party code, so no "data-not-instructions"
   lockdown (that is the sibling `agentic-security-review`), but read-only:
   reports findings; never edits code unless separately asked; static reasoning
   over the repo; no network needed.
3. **Rule: select frameworks, don't spray them.** Verbatim load-bearing line:
   *"Do not apply irrelevant frameworks merely because they are available. More
   security context is not automatically better context."* Inspect first, then
   activate. Points to `references/framework-selection.md`.
4. **Workflow** (numbered): (1) Inventory the app — language, framework, entry
   points, API surface, auth, data stores, config, dependencies. (2) Select
   frameworks from the cues. (3) Review the code against each selected framework
   using its reference file. (4) For each issue, map it to Top 10:2025 + the ASVS
   requirement (+ API item when relevant). (5) Report per `report-format.md`.
5. **Framework map table** — the seven rows from the spec's selection table
   (ASVS 5.0 always; Top 10:2025 always; API Top 10:2023 conditional; WSTG deep;
   MASVS v1.1; Desktop v1.2; GenAI v1.3), each linking its reference file.
6. **Modes** — Standard (Top 10 + ASVS + API, static) and Deep (`--deep`/"test"/
   "pentest plan" → adds a WSTG-derived test plan).
7. **When NOT to use** — third-party/AI skill vetting → `agentic-security-review`;
   quick diff pass → built-in `security-review`.

- [ ] **Step 3: Write framework-selection.md.**

Detection cues exactly as the spec's "core intelligence" section:
- API surface → `app.(get|post|put|delete|patch)`, Nest/Express/Fastify/Flask/
  Django/Rails controllers, OpenAPI/Swagger files, GraphQL schema/`.graphql`,
  gRPC `.proto`, tRPC routers, `/api/` paths.
- Mobile (v1.1) → `android/`, `ios/`, `*.xcodeproj`, `build.gradle`,
  `AndroidManifest.xml`, React Native / Flutter / Expo / Capacitor.
- Desktop (v1.2) → Electron, Tauri, .NET/WPF/WinUI, Qt, Swift/macOS, native
  Rust/C++ desktop. Electron/Tauri → both web and desktop checks.
- GenAI (v1.3) → OpenAI/Anthropic SDKs, prompt templates, RAG, vector DBs, tool/
  function calling, agent frameworks — on the app's AI features, not because an
  AI wrote the code.
Include grep commands for each cue. End with: "ASVS 5.0 and Top 10:2025 are
always on; the rest activate only on a positive cue. When unsure whether a
surface exists, say so and ask — do not assume."

- [ ] **Step 4: Write report-format.md.**

Coverage header + finding block exactly as the spec's "Finding & report format":
frameworks line (`A0x:2025` + `ASVS Vx.y.z` [+ `APIx:2023`]), location file:line,
problem, abuse scenario, remediation, OWASP guidance (cheat-sheet name),
confidence. State: severity = impact × exploitability, independent of confidence.
Include the worked `/api/invoices/:id` BOLA example from the spec.

- [ ] **Step 5: Validate (YAML + pre-approval list + selection cues).**

Run:
```bash
python3 - <<'PY'
import yaml
d=yaml.safe_load(open("skills/application-security-review/SKILL.md").read().split("---\n")[1])
assert d["name"]=="application-security-review"
assert d["allowed-tools"]==["Read","Glob","Grep"], d["allowed-tools"]
print("frontmatter OK, read-tool pre-approvals OK (host isolation not validated)")
PY
grep -q "Do not apply irrelevant frameworks" skills/application-security-review/SKILL.md && echo "selection rule present"
grep -qi "graphql" skills/application-security-review/references/framework-selection.md && echo "api cues present"
```
Expected: all three lines print; no assertion error.

- [ ] **Step 6: Commit.**

```bash
git add skills/application-security-review/SKILL.md skills/application-security-review/references/framework-selection.md skills/application-security-review/references/report-format.md
git commit -m "Add application-security-review skeleton: SKILL.md, selection, report format"
```

---

## Task 2: Web Top 10:2025 reference + cheat-sheet index

**Files:**
- Create: `skills/application-security-review/references/web-top10-2025.md`
- Create: `skills/application-security-review/references/cheat-sheet-index.md`

- [ ] **Step 1: Write web-top10-2025.md with the verified category list.**

The ten categories, verbatim (OWASP Top 10:2025, 8th edition):
A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply
Chain Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure
Design · A07 Authentication Failures · A08 Software or Data Integrity Failures ·
A09 Security Logging and Alerting Failures · A10 Mishandling of Exceptional
Conditions.
For each: 1–2 code-review detection cues (what the flaw looks like in source) and
the ASVS chapter it maps to (e.g. A01 → V8 Authorization; A05 → V1 Encoding and
Sanitization / V2 Validation; A04 → V11 Cryptography; A07 → V6 Authentication;
A03 → V15 Secure Coding and Architecture / dependency manifests). Note A01 now
explicitly covers BOLA/BFLA API authz and absorbed SSRF; A03 and A10 are new in
2025.

- [ ] **Step 2: Write cheat-sheet-index.md as a routing map (names, not content).**

Topic → OWASP Cheat Sheet name, covering at least: Authentication; MFA;
Authorization; IDOR/BOLA; XSS (DOM XSS Prevention, XSS Prevention); Content
Security Policy; SQL Injection / Query Parameterization; Deserialization; SSRF;
File Upload; Node.js Security; NPM Security; REST Security; GraphQL; Web Service
Security; WebSocket; JWT; Cryptographic Storage; Secrets Management; Logging;
Error Handling; plus the AI sheets (AI Agent Security, MCP Security, LLM Prompt
Injection Prevention). State: "consulted only when proposing remediation; do not
dump into every review."

- [ ] **Step 3: Validate all ten categories and routing present.**

Run:
```bash
for c in "Broken Access Control" "Security Misconfiguration" "Software Supply Chain Failures" "Cryptographic Failures" "Injection" "Insecure Design" "Authentication Failures" "Software or Data Integrity Failures" "Security Logging and Alerting Failures" "Mishandling of Exceptional Conditions"; do
  grep -q "$c" skills/application-security-review/references/web-top10-2025.md || echo "MISSING: $c"
done; echo "top10 check done"
grep -qi "MCP Security" skills/application-security-review/references/cheat-sheet-index.md && echo "cheat-sheet AI routing present"
```
Expected: "top10 check done" with no MISSING lines; AI routing present.

- [ ] **Step 4: Commit.**

```bash
git add skills/application-security-review/references/web-top10-2025.md skills/application-security-review/references/cheat-sheet-index.md
git commit -m "Add Top 10:2025 reference and cheat-sheet routing index"
```

---

## Task 3: ASVS 5.0 backbone checklist

**Files:**
- Create: `skills/application-security-review/references/asvs-5.md`

- [ ] **Step 1: Write asvs-5.md — one section per chapter, V1–V17.**

Verified ASVS 5.0.0 chapters (verbatim titles): V1 Encoding and Sanitization · V2
Validation and Business Logic · V3 Web Frontend Security · V4 API and Web Service
· V5 File Handling · V6 Authentication · V7 Session Management · V8 Authorization
· V9 Self-contained Tokens · V10 OAuth and OIDC · V11 Cryptography · V12 Secure
Communication · V13 Configuration · V14 Data Protection · V15 Secure Coding and
Architecture · V16 Security Logging and Error Handling · V17 WebRTC.

For each chapter give a **high-yield, code-review-oriented checklist** (3–7 bullet
checks of what to look for in source at L1/L2 depth) — NOT the full ~350
requirements. Example for V8 Authorization: "every object fetched by id is
checked against the caller's ownership/role before use (guards against BOLA);
function-level authz enforced server-side, not just hidden in UI; deny-by-default
on new routes." Head the file: "This is a working review map at L1/L2. For L3 or
exact requirement text, consult the ASVS 5.0.0 document; cite requirements as
`ASVS Vx.y.z`." Do NOT invent requirement numbers — cite chapter (`Vx`) when the
exact sub-id is not known.

- [ ] **Step 2: Validate all 17 chapters present in order.**

Run:
```bash
for t in "Encoding and Sanitization" "Validation and Business Logic" "Web Frontend Security" "API and Web Service" "File Handling" "Authentication" "Session Management" "Authorization" "Self-contained Tokens" "OAuth and OIDC" "Cryptography" "Secure Communication" "Configuration" "Data Protection" "Secure Coding and Architecture" "Security Logging and Error Handling" "WebRTC"; do
  grep -q "$t" skills/application-security-review/references/asvs-5.md || echo "MISSING: $t"
done; echo "asvs check done"
```
Expected: "asvs check done" with no MISSING lines.

- [ ] **Step 3: Commit.**

```bash
git add skills/application-security-review/references/asvs-5.md
git commit -m "Add ASVS 5.0 backbone checklist (V1-V17)"
```

---

## Task 4: API Security Top 10:2023 (conditional)

**Files:**
- Create: `skills/application-security-review/references/api-top10-2023.md`
- Modify: `skills/application-security-review/references/framework-selection.md` (add the "when API detected, load api-top10-2023.md" pointer if not already explicit)

- [ ] **Step 1: Write api-top10-2023.md with the verified list.**

Verbatim (OWASP API Security Top 10 2023): API1 Broken Object Level Authorization
· API2 Broken Authentication · API3 Broken Object Property Level Authorization ·
API4 Unrestricted Resource Consumption · API5 Broken Function Level Authorization
· API6 Unrestricted Access to Sensitive Business Flows · API7 Server Side Request
Forgery · API8 Security Misconfiguration · API9 Improper Inventory Management ·
API10 Unsafe Consumption of APIs. For each: a code-review cue and the ASVS
chapter mapping (API1/API3/API5 → V8 Authorization; API2 → V6; API4 → V2/V13;
API7 → V2 input validation + egress). State that API Top 10 supplements, not
replaces, the web Top 10 for API-backed apps.

- [ ] **Step 2: Wire conditional activation.**

Ensure `framework-selection.md` says: on a positive API cue, load
`api-top10-2023.md` in addition to ASVS + Top 10; otherwise skip it entirely.

- [ ] **Step 3: Validate all ten API items present.**

Run:
```bash
for c in "Broken Object Level Authorization" "Broken Authentication" "Broken Object Property Level Authorization" "Unrestricted Resource Consumption" "Broken Function Level Authorization" "Unrestricted Access to Sensitive Business Flows" "Server Side Request Forgery" "Security Misconfiguration" "Improper Inventory Management" "Unsafe Consumption of APIs"; do
  grep -q "$c" skills/application-security-review/references/api-top10-2023.md || echo "MISSING: $c"
done; echo "api top10 check done"
```
Expected: "api top10 check done" with no MISSING lines.

- [ ] **Step 4: Commit.**

```bash
git add skills/application-security-review/references/api-top10-2023.md skills/application-security-review/references/framework-selection.md
git commit -m "Add API Security Top 10:2023 reference with conditional activation"
```

---

## Task 5: WSTG deep mode

**Files:**
- Create: `skills/application-security-review/references/wstg.md`
- Modify: `skills/application-security-review/SKILL.md` (confirm deep-mode section points here)

- [ ] **Step 1: Write wstg.md.**

Head it: "OWASP WSTG 4.2 (pinned; 5.0 is in development — do not follow a
'latest' branch)." List the WSTG testing areas used in deep mode: information
gathering, configuration/deployment management, identity management,
authentication, authorization, session management, input validation, error
handling, cryptography, business logic, client-side. State that deep mode turns
these into a **test plan** (concrete things to attempt/verify), not more static
findings — the standard-mode findings still come from Top 10 + ASVS.

- [ ] **Step 2: Confirm SKILL.md deep-mode wiring references wstg.md.**

- [ ] **Step 3: Validate.**

Run:
```bash
grep -q "4.2" skills/application-security-review/references/wstg.md && echo "WSTG pinned"
grep -qi "wstg" skills/application-security-review/SKILL.md && echo "deep mode wired"
```
Expected: both lines print.

- [ ] **Step 4: Commit.**

```bash
git add skills/application-security-review/references/wstg.md skills/application-security-review/SKILL.md
git commit -m "Add WSTG 4.2 deep-mode test-plan reference"
```

---

## Task 6: Future-module stubs

**Files:**
- Create: `skills/application-security-review/references/future/mobile-masvs.md`
- Create: `skills/application-security-review/references/future/desktop-top10.md`
- Create: `skills/application-security-review/references/future/genai-llm-top10-2026.md`

- [ ] **Step 1: Write the three stubs.**

Each states: the framework and version (MASVS/MASTG current; Desktop App Security
Top 10 2021; GenAI LLM Top 10 2026, published 2026-08-04), the detection cues
that will activate it, and a clear line: "Detection is wired in
framework-selection.md; the review checklist is NOT implemented yet (planned:
v1.1 / v1.2 / v1.3). If a project triggers this, say the module is not yet
available rather than improvising a review." Note GenAI is distinct from the
`agentic-security-review` skill's Agentic Skills Top 10, and that an OWASP Top 10
for Agentic Applications (2026) also exists.

- [ ] **Step 2: Validate the stubs disclaim implementation.**

Run:
```bash
for f in mobile-masvs desktop-top10 genai-llm-top10-2026; do
  grep -qi "not.*implemented\|not yet" skills/application-security-review/references/future/$f.md || echo "STUB MISSING DISCLAIMER: $f"
done; echo "stub check done"
```
Expected: "stub check done" with no missing-disclaimer lines.

- [ ] **Step 3: Commit.**

```bash
git add skills/application-security-review/references/future
git commit -m "Add v1.1-v1.3 module stubs (MASVS, Desktop, GenAI)"
```

---

## Task 7: Fixtures + RED/GREEN validation

**Files (gitignored, not committed):**
- Create: `.context/fixtures/appsec-vuln/` — a small Express/Node API app with
  planted, mapped defects.
- Create: `.context/fixtures/appsec-clean/` — the same app, defects fixed.
- Create: `docs/superpowers/plans/2026-09-08-application-security-review-results.md`
  — record the validation outcome (this IS committed).

- [ ] **Step 1: Build the vulnerable fixture with at least these planted, mapped defects.**

- `GET /api/invoices/:id` returns the invoice with no ownership check →
  API1:2023 BOLA / A01:2025 / ASVS V8.
- A comment/render path inserting user HTML into the DOM/response unescaped →
  A05:2025 Injection / ASVS V1.
- Password hashing with MD5 or a hard-coded secret → A04:2025 Cryptographic
  Failures / ASVS V11.
- A login route with no rate limiting / lockout → A07:2025 Authentication
  Failures + API4:2023 / ASVS V6.
- A `child_process.exec` built from request input → A05:2025 Injection / ASVS V2.
- The app must present a clear API surface (Express routes) so selection
  activates the API Top 10.

- [ ] **Step 2: RED — run the skill's methodology against the vulnerable fixture.**

Following SKILL.md: inventory → select (must activate ASVS + Top 10:2025 + API
Top 10 because routes exist) → review → report. Confirm every planted defect
above appears as a finding with the correct framework mapping and file:line.

- [ ] **Step 3: GREEN — run against the clean fixture.**

Confirm no Critical/High findings and that the previously-flagged lines are now
clean (no false positives on the fixed code).

- [ ] **Step 4: Selection assertion.**

Create a trivial no-API fixture (a pure library/CLI file, no routes) and confirm
selection does NOT activate the API Top 10 (proves selection discriminates).

- [ ] **Step 5: Record results and refine.**

Write the outcome table (defect → detected? → mapping correct?) to the results
doc. If a planted defect was missed or a clean line false-positived, refine the
relevant reference file and re-run. Commit the results doc.

```bash
git add docs/superpowers/plans/2026-09-08-application-security-review-results.md
git commit -m "Record application-security-review fixture validation results"
```

---

## Task 8: Register in README and plugin manifests

**Files:**
- Modify: `README.md` (skills table)
- Modify: `.claude-plugin/plugin.json` (description, keywords, version → 1.5.0)
- Modify: `.claude-plugin/marketplace.json` (same)

- [ ] **Step 1: Add the README table row** linking `skills/application-security-review/README.md` with a one-line description (OWASP-anchored app-code review; complements the built-in; sibling to agentic-security-review).

- [ ] **Step 2: Update both manifests** — append a sentence to `description` naming
the skill, add keywords (`asvs`, `owasp-top-10`, `api-security`, `appsec`,
`application-security-review`), bump `version` to `1.5.0` in both. Preserve
literal em-dashes (write JSON with `ensure_ascii=False` if using Python).

- [ ] **Step 3: Validate JSON + version.**

Run:
```bash
python3 -c "import json;[json.load(open(p)) for p in ['.claude-plugin/plugin.json','.claude-plugin/marketplace.json']];print('json ok')"
grep -c '\\\\u2014' .claude-plugin/*.json    # expect 0 0 (no escaped em-dashes)
grep -q '1.5.0' .claude-plugin/plugin.json && echo "version bumped"
```
Expected: `json ok`; both counts 0; version bumped.

- [ ] **Step 4: Commit.**

```bash
git add README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "Register application-security-review in README and manifests (v1.5.0)"
```

---

## Task 9: Skill README

**Files:**
- Create: `skills/application-security-review/README.md`

- [ ] **Step 1: Write the README** in the collection's voice (see
`skills/agentic-security-review/README.md` and `skills/nest/README.md`): what it
does (inspect → select → review → report), the complement-not-replace
positioning vs. built-in `security-review`, the read-only boundary, the
verified-frameworks note, and the platform-neutral/Codex-portable point. Include
usage lines and the layout block.

- [ ] **Step 2: Validate it links real files.**

Run:
```bash
grep -q "agentic-security-review" skills/application-security-review/README.md && echo "sibling cross-ref present"
test -f skills/application-security-review/SKILL.md && echo "skill present"
```
Expected: both lines print.

- [ ] **Step 3: Commit.**

```bash
git add skills/application-security-review/README.md
git commit -m "Add application-security-review README"
```

---

## Self-review notes

- **Spec coverage:** positioning (Task 1 boundary + When-NOT), selection
  intelligence (Task 1 + 4), verified facts (Tasks 2/3/4 with grep assertions),
  ASVS distillation (Task 3), finding format (Task 1 report-format), cheat-sheet
  index (Task 2), WSTG deep mode (Task 5), stubs (Task 6), fixtures/validation
  (Task 7), registration (Task 8), README (Task 9). All spec sections map to a task.
- **No placeholders:** every framework list is reproduced verbatim from the
  verified spec; validation commands are concrete with expected output.
- **Naming consistency:** file/skill names match the structure block throughout
  (`application-security-review`, `asvs-5.md`, `api-top10-2023.md`,
  `web-top10-2025.md`, `framework-selection.md`, `report-format.md`,
  `cheat-sheet-index.md`, `wstg.md`).
