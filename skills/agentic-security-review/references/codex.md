# Platform notes — Codex

The AST01–AST10 methodology and the lethal trifecta are platform-neutral and
apply unchanged. Only the capability *surfaces* and file names differ. This file
is what makes the core skill portable — copy `SKILL.md` and the `astNN-*.md`
files into a Codex skill and swap this reference for `claude-code.md`.

## Where skills live

- `~/.agents/skills/<name>/` (user), or project-local equivalents.
- Instruction file is typically `AGENTS.md` (project root) and/or a `SKILL.md`.

## Capability surfaces to inventory

- **Agent instructions:** `AGENTS.md` / `SKILL.md` — prose that steers the agent.
  Same prompt-injection surface as a Claude `SKILL.md`; apply Rule 0.
- **Tool / permission config:** Codex's approval mode and sandbox settings, and
  any allow/deny tool configuration. Note whether shell/network are enabled and
  whether the sandbox is workspace-write vs. broader.
- **MCP servers:** configured for Codex the same conceptual way — external
  processes with their own capabilities and egress.
- **Scripts, hooks, `postinstall`, manifests:** identical concerns to Claude Code
  (AST02/AST05/AST06).

## Cross-platform (AST10)

A skill shipping both `AGENTS.md` and `SKILL.md`, or install steps naming several
agents, must be reviewed under each host's trust model. A tool restriction one
host enforces may be ignored by another; do not assume one sandbox covers both.

## Porting checklist

1. Copy `SKILL.md` + `references/astNN-*.md` + `report-format.md` unchanged.
2. Keep the instruction to use only file read and search. Configure and verify
   the host's actual tool, filesystem, and network restrictions for an enforced
   read-only reviewer; translating `allowed-tools` names does not establish one.
3. Keep this `codex.md`; keep `claude-code.md` too if the reviewer audits both.
