# AST08 — Poor Scanning

Relying on pattern-matching scanners that miss semantic and behavioral threats.
For the reviewer, this is a caution about *your own method*: grep finds strings,
not intent.

## Detection cues / method

- Behavior that is dangerous only in combination: a benign file read + a benign
  network call = exfiltration. Signatures miss the *composition*; the lethal
  trifecta step exists to catch it.
- Semantic obfuscation a regex passes: string concatenation building a URL,
  encoded payloads, indirection through variables, logic in a binary or minified
  blob (`NEEDS REVIEW`, do not execute to find out).
- Intent in prose: a SKILL.md instructing the agent to misbehave has no code
  signature at all — read for meaning, not keywords.

## Applying it

Use grep to *locate*, then reason about what the located code composes to. Never
downgrade a finding just because a scanner would miss it — that is exactly the
gap this category names. When static reasoning runs out, return `NEEDS REVIEW`
with the specific thing a human (or a sandboxed dynamic run) must verify.

## Severity

This category is usually about method rather than a single line; record residual
uncertainty as `NEEDS REVIEW` in the report rather than a false PASS.
