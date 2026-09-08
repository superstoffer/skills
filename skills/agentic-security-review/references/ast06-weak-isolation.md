# AST06 — Weak Isolation

The skill assumes or requires weaker sandboxing than it should, reaching host
resources directly instead of staying within a bounded runtime.

## Detection cues (static)

- Direct host access: absolute paths outside the workspace, `~`, `/etc`,
  `/var`, system config, the Docker socket, `/proc`.
- Escape/persistence: writing to `~/Library/LaunchAgents`, `~/.config/autostart`,
  crontab, shell rc files (`.bashrc`, `.zshrc`, `.profile`), git hooks dir.
- Assumes ambient credentials/network with no scoping.
- Spawns long-lived or background processes (`launchctl`, `nohup`, `&`,
  `systemctl`, a daemon) — a skill should be a bounded action, not a resident.
- "Runs continuously in the background" language in the description.

## Severity

Launch agent / cron / rc-file persistence = **Critical** (survives the session).
Direct out-of-workspace host access = **High**.

## Remediation

Confine to the workspace. No background daemons, no autostart, no host-config
writes. If persistence is a real feature, it must be explicit, visible, and
user-approved — never a setup side effect.
