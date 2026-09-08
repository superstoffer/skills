# AST04 — Insecure Metadata

Manifest / frontmatter parsing that turns data into behavior: YAML/JSON quirks,
type coercion, or fields interpreted as executable instructions.

## Detection cues (static)

- YAML tags that instantiate objects (`!!python/object`, `!!ruby/…`) — only
  safe under `yaml.safe_load`. Grep for `yaml.load(` without `SafeLoader`.
- Frontmatter fields whose *values* are treated as commands (a `version: latest`
  that triggers a network resolve; a `hooks:`/`command:` field pointing at a
  script).
- Description/name fields carrying injected instructions to the agent (overlaps
  AST01) or control characters, zero-width chars, homoglyphs, RTL overrides.
  Grep for non-ASCII in metadata.
- Untrusted metadata used to build a shell command or path without sanitizing.

## Severity

`yaml.load` on attacker-controlled input = **High**. Metadata field that
executes = **High/Critical**. Hidden-character injection = **Medium/High**.

## Remediation

`yaml.safe_load` only. Treat every manifest value as inert data. Validate/allow-
list fields; strip or reject control and bidi characters.
