# AST03 — Over-Privileged Skills

The skill requests more capability than its function needs. Excess privilege is
latent blast radius: a bug or a compromise now reaches everything the grant
allowed.

## Detection cues (static)

- Broad `allowed-tools`: `Bash` (unrestricted), `Write`, `Edit`, `WebFetch`,
  `WebSearch` on a skill whose job is read-only analysis or text generation.
- No `allowed-tools` at all (inherits everything) on a non-trivial skill.
- Filesystem reach beyond the project (`~`, `/etc`, absolute paths outside cwd).
- An MCP server exposing write/exec/network tools for a read-only task.
- Capability the description never justifies ("generate a changelog" that also
  wants `git push` and the network).

## Judging it

Ask: what is the *minimum* set of tools this function needs? Everything beyond
that is a finding. A changelog generator needs `Read`/`Glob`/`Grep` and maybe
scoped `Bash(git log:*)` — not `Bash` + `Write` + network.

## Severity

Unrestricted `Bash` or `Write` with no functional need = **High**. Network tools
on a local-only task = **High** (it enables the trifecta). Slightly-too-broad
but bounded = **Medium/Low**.

## Remediation

Least privilege. Enumerate `allowed-tools` explicitly; scope `Bash(cmd:*)` to
the exact commands; drop write/network unless the core function needs them.
