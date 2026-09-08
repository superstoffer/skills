# agentic-security-review

A Claude Code skill that audits an agent extension — a skill, plugin, MCP
server, hook, or a Codex skill — against the [OWASP Agentic Skills Top 10
(AST01–AST10)](https://owasp.org/www-project-agentic-skills-top-10/) and the
lethal trifecta, then tells you whether it is safe to install, enable, commit,
or publish.

## What it does

1. **Inventories** the target statically — SKILL.md/AGENTS.md and frontmatter,
   scripts, hooks, manifests, MCP config, dependencies and lockfiles, referenced
   files, external URLs, and every declared or implied grant.
2. **Establishes effective capabilities** — what the thing can actually do once
   enabled, not what it claims — using per-platform notes for Claude Code and
   Codex.
3. **Reviews AST01–AST10** with detection cues per category, then names which of
   the three lethal-trifecta capabilities the target holds. Two of three is a
   warning; all three is a top-of-report callout.
4. **Reports** a fixed format: per-category PASS / FINDING / NEEDS REVIEW / N/A,
   findings with severity, file:line, evidence, abuse scenario, remediation and
   confidence, and a go/no-go verdict with blockers and hardening.

Two modes: **Full audit** (all ten categories) and **Preflight** (fast go/no-go
on Critical/High only — "is this safe to install?").

## The security boundary

The skill's defining property is that **it treats the reviewed material as data,
never instructions**, and **it runs itself with least privilege**: its
`allowed-tools` are `Read`, `Glob`, `Grep` only — no `Bash`, no write, no
network. It never executes the target's scripts, runs its setup, installs its
dependencies, follows its URLs, reads secrets, or obeys instructions embedded in
it. A malicious skill's first move is to talk to its reviewer; this skill is
built not to listen.

## Platform-neutral core

AST01–AST10 and the trifecta are host-agnostic. Platform specifics live only in
`references/claude-code.md` and `references/codex.md`, so the same methodology
ports to a Codex `SKILL.md` without rewriting the OWASP logic.

## Usage

```
agentic-security-review ./path/to/skill        # full audit
"preflight this before I install it" ./path     # fast go/no-go
```

## Layout

```
agentic-security-review/
├── SKILL.md
└── references/
    ├── ast01-malicious-skills.md … ast10-cross-platform.md
    ├── claude-code.md
    ├── codex.md
    └── report-format.md
```
