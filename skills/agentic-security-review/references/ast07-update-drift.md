# AST07 — Update Drift

Unpinned versions let the thing you approved become something else later — a
silent update ships a payload you never reviewed.

## Detection cues (static)

- Version pins that float: `latest`, `*`, `>=x`, `^`, `~`, `main`/`HEAD` refs,
  `version: latest` in frontmatter. Grep manifests for `latest`, `"*"`, `>=`,
  `^`, `~`.
- No lockfile committed, or a lockfile ignored by ranged specs.
- Auto-update logic inside the skill ("always pull the current version rather
  than pinning").
- Remote instruction/code load (AST05) is the extreme case — drift on every run.

## Severity

Auto-pull of executable content = **Critical** (via AST05). Ranged deps with no
lockfile = **Medium/High**. Cosmetic float on a pure-data dep = **Low**.

## Remediation

Pin exact versions; commit a lockfile with hashes. Adopt updates deliberately
through review, not automatically at runtime.
