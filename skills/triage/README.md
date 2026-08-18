# triage

A Claude Code skill that turns messy, unstructured input into clean, well-formed issues for your project tracker.

Paste meeting notes, Slack messages, bug reports, customer feedback, or stakeholder asks — triage classifies them, checks for duplicates, drafts issues, and creates them after your approval.

## What it does

1. **Ingests** raw text in any format
2. **Splits** multi-concern inputs (meeting notes with 10 items become 10 separate concerns)
3. **Classifies** each concern: Bug, Feature, Chore, Tech Debt, Spike, Question, Noise, or Strategic
4. **Checks for existing work** — searches your tracker for duplicates and related projects before drafting
5. **Drafts** concise, well-structured issues with the right template per type
6. **Confirms** with you before creating anything
7. **Creates** the issue in your project tracker

The skill never writes code. If you paste a stack trace, it treats it as evidence for a bug report — not a debugging request.

## Currently supported

- **Linear** via the [official Linear MCP server](https://linear.app/docs/mcp)

## Install

See the [repository README](../../README.md) for the plugin install.

If you'd rather not use the plugin, copy this folder directly:

```bash
# personal, all projects
mkdir -p ~/.claude/skills && cp -r skills/triage ~/.claude/skills/

# project-local, shared via git
mkdir -p .claude/skills && cp -r skills/triage .claude/skills/
```

Both are safe to re-run to update an existing copy.

## Prerequisites

1. The [Linear MCP server](https://linear.app/docs/mcp) configured in Claude Code:
   ```bash
   claude mcp add --transport http linear https://mcp.linear.app/mcp
   ```
2. Run `/mcp` in Claude Code to complete the OAuth flow.

## Usage

Invoke explicitly with `/triage` or let it trigger automatically when you paste text and say things like "file this," "make a ticket," "triage this," or "log this."

## Customize for your workspace

Edit `references/linear-conventions.md` with your team names, label vocabulary, and active projects. The skill uses this to set the right defaults when creating issues.
