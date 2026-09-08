# Platform notes — Claude Code

Where a Claude Code skill/plugin gets its capability, so you can map the target
to an effective trust boundary.

## Where skills live

- User skills: `~/.claude/skills/<name>/SKILL.md`
- Project skills: `.claude/skills/<name>/SKILL.md`
- Plugins/marketplaces: `.claude-plugin/marketplace.json`, `plugin.json`; a
  plugin bundles many skills and may add hooks, MCP servers, and commands.

## Capability surfaces to inventory

- **`allowed-tools` in frontmatter.** The primary grant. Absent = inherits the
  session's tools. `Bash` unrestricted is broad; `Bash(git log:*)` is scoped.
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

`allowed-tools` is a *declaration*; unrestricted `Bash` makes it advisory. A
skill can bypass its own narrow declaration by shelling out. Weigh the real
commands the scripts run over the frontmatter's promise.
