# application-security-review

A Claude Code skill that reviews your **own application source code** for
security, anchored on the OWASP frameworks that actually apply to it. Sibling to
[agentic-security-review](../agentic-security-review/README.md) — same
collection, different scope: **your app's code vs. the agent extensions you
install.**

## What it does

1. **Inventories** the app — language, framework, entry points, API surface,
   auth, data stores, configuration, dependencies.
2. **Selects frameworks** by inspecting the project, applying only what fits:
   **ASVS 5.0** (the backbone of verifiable requirements) and the **OWASP Top
   10:2025** (risk labels) always; the **API Security Top 10:2023** when an API
   surface is detected; **WSTG 4.2** in a deep/testing pass. Mobile (MASVS),
   Desktop, and GenAI (LLM Top 10:2026) modules are stubbed for v1.1–v1.3.
3. **Reviews** the code and **maps every finding** to a concrete standard — a Top
   10 label *and* the ASVS requirement behind it (plus the API item when
   relevant) — so a finding is actionable, not "possible XSS".
4. **Reports** a fixed format with a coverage header, findings (severity,
   file:line, abuse scenario, remediation, the relevant OWASP Cheat Sheet, and
   confidence), and an overall verdict.

The governing rule: **don't apply irrelevant frameworks merely because they are
available.** More security context is not automatically better context.

## Complements, doesn't replace

The built-in `/security-review` is the quick pass over your pending diff. This
skill is the deliberate, framework-anchored review that reasons across whole
files, modules, and configuration — invoke it on purpose ("owasp review this",
"audit this API for auth flaws", "check this against ASVS"). Distinct triggering,
no collision.

## Boundary

It reviews trusted first-party code, so it drops the "reviewed material is data,
never instructions" lockdown its sibling needs for untrusted skills — but it
stays **read-only** (`Read`, `Glob`, `Grep`). It reports findings; fixing is a
separate action you ask for.

## Verified frameworks

Every framework fact is pinned from its OWASP source, not a summary: OWASP Top
10:2025 (A01–A10), API Security Top 10:2023 (API1–API10), and ASVS 5.0.0's 17
chapters (V1–V17). Versioned references are pinned (WSTG 4.2), never "latest".

## Platform-neutral core

The OWASP references carry no Claude-specific vocabulary, so the methodology
ports to a Codex skill without rewriting the framework logic.

## Usage

```
owasp review ./src                      # standard review
"audit this API for auth flaws" ./src   # standard, API Top 10 auto-activates
"security review --deep before release" # adds a WSTG test plan
```

## Layout

```
application-security-review/
├── SKILL.md
└── references/
    ├── framework-selection.md   # detection cues → which frameworks
    ├── web-top10-2025.md         # A01–A10:2025
    ├── api-top10-2023.md         # API1–API10:2023 (conditional)
    ├── asvs-5.md                 # V1–V17 backbone checklist
    ├── cheat-sheet-index.md      # topic → cheat-sheet routing
    ├── report-format.md          # coverage header + finding block
    ├── wstg.md                   # deep-mode test plan (WSTG 4.2)
    └── future/                   # v1.1–v1.3 stubs (MASVS, Desktop, GenAI)
```
