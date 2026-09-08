# AST03 — Over-Privileged Skills

The skill requests more capability than its function needs. Excess privilege is
latent blast radius: a bug or a compromise now reaches everything the grant
allowed.

## Detection cues (static)

- Broad `allowed-tools`: `Bash` (unrestricted), `Write`, `Edit`, `WebFetch`,
  `WebSearch` on a skill whose job is read-only analysis or text generation.
- Host permissions that allow unnecessary shell, writes, or network, even when
  the skill lists only read tools. Missing `allowed-tools` alone is not a finding;
  it adds no pre-approvals, and host permissions still apply.
- Filesystem reach beyond the project (`~`, `/etc`, absolute paths outside cwd).
- An MCP server exposing write/exec/network tools for a read-only task.
- Capability the description never justifies ("generate a changelog" that also
  wants `git push` and the network).

## Judging it

Ask: what is the *minimum* set of tools this function needs? Everything beyond
that is a finding. A changelog generator needs `Read`/`Glob`/`Grep` and maybe
scoped `Bash(git log:*)` — not `Bash` + `Write` + network.
Separate permissions added by the target from ambient host capabilities. If
host configuration is unavailable, use `NEEDS REVIEW` for that uncertainty;
do not infer either unrestricted access or an enforced restriction from a
missing or narrow frontmatter list.

## Severity

Unrestricted `Bash` or `Write` with no functional need = **High**. Network tools
on a local-only task = **High** (it enables the trifecta). Slightly-too-broad
but bounded = **Medium/Low**.

## Remediation

Minimize added pre-approvals in `allowed-tools`, scoping shell commands where
needed. Removing an entry does not revoke an existing host permission. Enforce
unneeded tool denials and filesystem/network isolation in the host, including
MCP access; verify those controls before calling the boundary read-only.
