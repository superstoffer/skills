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

# Application Security Review

Review the application's own source code for security, anchored on the OWASP
frameworks that actually apply to it — and map every finding to a concrete
standard so it is actionable, not a vague "possible XSS".

## Boundary

This reviews **trusted first-party code** — the app you are building. It does not
need the "reviewed material is data, never instructions" lockdown that its
sibling `agentic-security-review` requires for untrusted third-party skills. It
is still least-privilege and **read-only**:

- Tools are `Read`, `Glob`, `Grep`. Static reasoning over the repo; no network.
- It **reports findings; it never edits code** unless you separately ask it to.
- Reviewing is a bounded action, not a background process.

## Rule: select frameworks, don't spray them

> **Do not apply irrelevant frameworks merely because they are available. More
> security context is not automatically better context.**

Inspect the project first, then activate only what applies. The cues are in
`references/framework-selection.md`. ASVS 5.0 and the Top 10:2025 are always on;
everything else waits for a positive signal.

## Workflow

1. **Inventory the app.** Language and framework, entry points, the API surface
   (routes/handlers/schema), authentication and authorization, data stores,
   configuration and secrets handling, and dependencies. Read before concluding.
2. **Select frameworks** from `references/framework-selection.md`.
3. **Review the code** against each selected framework using its reference file.
   Reason about behaviour and composition, not just string matches — a clean-
   looking handler with no ownership check is still a finding.
4. **Map each issue** to a Top 10:2025 category **and** the ASVS chapter/
   requirement it violates (plus the API item when an API is involved).
5. **Report** using `references/report-format.md`.

## Framework map

| Framework | Version | When | Reference |
|---|---|---|---|
| OWASP ASVS | 5.0.0 | Always — backbone of verifiable requirements | `references/asvs-5.md` |
| OWASP Top 10 | 2025 | Always — risk classification label | `references/web-top10-2025.md` |
| OWASP API Security Top 10 | 2023 | When an API surface is detected | `references/api-top10-2023.md` |
| OWASP WSTG | 4.2 (pinned) | Deep/testing mode only | `references/wstg.md` |
| OWASP MASVS/MASTG | current | Mobile projects — **v1.1, not yet implemented** | `references/future/mobile-masvs.md` |
| OWASP Desktop App Security Top 10 | 2021 | Desktop apps — **v1.2, not yet implemented** | `references/future/desktop-top10.md` |
| OWASP GenAI LLM Top 10 | 2026 | Apps with LLM/AI features — **v1.3, not yet implemented** | `references/future/genai-llm-top10-2026.md` |

## Modes

- **Standard review** — Top 10:2025 + ASVS (+ API Top 10 when an API is present),
  static reasoning over the source. The default.
- **Deep review** — triggered by `--deep`, "test", "pentest plan", or an explicit
  request to test. Adds a **WSTG-derived test plan** (`references/wstg.md`) on top
  of the standard findings — concrete things to attempt/verify, not more static
  findings.

## When NOT to use this skill

- Vetting a third-party or AI-generated **skill / plugin / MCP server / hook**
  before installing it → use `agentic-security-review` (different threat model:
  untrusted content, hard read-only, lethal-trifecta check).
- A quick pass over just the **pending diff** for obvious bugs → the built-in
  `security-review`. This skill is the deliberate, framework-anchored review that
  reasons across whole files, modules, and configuration.
