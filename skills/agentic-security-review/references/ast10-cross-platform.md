# AST10 — Cross-Platform Reuse

The same malicious skill ported across agent platforms (Claude Code ↔ Codex ↔
others). Formats differ, so a check that catches it on one platform may not on
another, and capability grants mean different things per platform.

## Detection cues (static)

- The same skill shipped for multiple hosts: both a `SKILL.md` and an
  `AGENTS.md`, or `allowed-tools` (Claude) alongside a Codex/other manifest.
- A capability that is bounded on one platform but not another (e.g. a tool
  restriction one host enforces and another ignores).
- Install instructions targeting several agents ("works in Claude Code and
  Codex") — widen the review to each host's trust model.
- Platform-specific escape hatches: a hook type or config field that only one
  host honors, used to smuggle behavior.

## Applying it

When a target is multi-platform, evaluate capabilities under *each* host's rules
using `references/claude-code.md` and `references/codex.md`. A grant that is safe
under Claude Code's `allowed-tools` may be unrestricted under another runtime.

## Severity

Depends on the underlying behavior; the cross-platform aspect *raises* severity
because the blast radius and the detection gap both grow. Flag prominently when a
malicious behavior is packaged for more than one host.

## Remediation

Review per platform. Do not assume one host's sandbox applies to another. Prefer
skills that declare a single, explicit target.
