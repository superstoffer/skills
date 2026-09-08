# AST09 — No Governance

No inventory, ownership, provenance, or approval trail — skills proliferate
uncontrolled and nobody can say what is installed or who vouches for it.

## Detection cues (static)

- No identifiable author/maintainer, repository, or license.
- No version, no changelog, no provenance for where the skill came from.
- No stated scope of what it may touch; no review/approval marker.
- For a collection/marketplace: no manifest listing members, no owner field.

## Applying it

This is often an organizational finding rather than a code one, but it belongs
in the report: an unsourced, unowned, unversioned skill is one you cannot govern
or revoke. Note it as **Informational/Low** on its own, but it *raises* the risk
of every other finding because there is no accountable owner to fix them.

## Remediation

Require author, license, pinned version, source repo, and an approval record
before a skill enters a shared environment. Keep an inventory of installed
skills and their granted capabilities.
