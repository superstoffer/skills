# Platform notes — Claude Code

Where a Claude Code skill/plugin gets its capability, so you can map the target
to an effective trust boundary.

## Where skills live

- User skills: `~/.claude/skills/<name>/SKILL.md`
- Project skills: `.claude/skills/<name>/SKILL.md`
- Plugins/marketplaces: `.claude-plugin/marketplace.json`, `plugin.json`; a
  plugin bundles many skills and may add hooks, MCP servers, and commands.

## Capability surfaces to inventory

- **`allowed-tools` in frontmatter.** Adds pre-approvals for listed tools; it
  does not remove access to unlisted tools. Session permissions apply whether
  this field is present or absent. `Bash` pre-approves broad shell use;
  `Bash(git log:*)` scopes that pre-approval, not all shell access.
  `Write`/`Edit` = mutation. `WebFetch`/`WebSearch` = egress. MCP tools appear as
  `mcp__<server>__<tool>`.
- **MCP servers.** `.mcp.json` / `mcp.json` / `settings.json` `mcpServers`. Each
  server is an external process with its own capabilities and its own egress —
  treat a server the skill pulls in as part of the target. A `command`/`args`
  that runs `npx`/`uvx` a remote package = supply-chain + remote-code surface.
- **Hooks.** `settings.json` hooks (`PreToolUse`, `PostToolUse`, `Stop`, etc.)
  run shell commands on events, often without per-call approval. A hook is
  ambient execution — scrutinize like a script. Also plain git hooks in the repo.
- **`postinstall`/build** in a bundled `package.json` — runs on install.
- **Settings & permissions.** `permissions.allow`/`deny`, `defaultMode`
  (e.g. `bypassPermissions`), `enableAllProjectMcpServers` — a skill that ships
  settings loosening these is escalating privilege.

## Mapping to the trifecta

- Private data: `Read` of repo/home, MCP tools returning secrets, env access.
- Untrusted content: `WebFetch`, MCP tools that read issues/email/pages, the
  reviewed inputs themselves.
- External comms: `WebFetch`/`WebSearch`, `Bash` with `curl`/`git push`, an MCP
  server that egresses.

## Notes

Assess effective capabilities using the host's existing permissions, permission
mode, enforced deny rules, sandbox, and connected MCP servers as well as the
skill's added pre-approvals. A skill listing only `Read`, `Glob`, `Grep` can still
use shell, write, or network tools permitted by its host. If host configuration
is unavailable, mark the affected assessment `NEEDS REVIEW` and state which
capabilities remain unknown.

For an enforced read-only reviewer, the host must deny or remove mutation,
execution, and network tools and constrain filesystem/network access as needed,
including MCP paths. A prose prohibition is an instruction, not isolation.
Never infer a hard boundary from `allowed-tools` alone.

Source: [Claude Code skill tool pre-approvals](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill).
