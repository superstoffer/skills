# Report format

Deterministic output so audits are comparable and diffable. Full audit uses the
whole template; Preflight uses only the header, Lethal Trifecta line, Blockers,
and Verdict.

## Header

```
# Agentic Security Review — <target name>
Mode: Full audit | Preflight
Target: <path>   Commit/version: <if known>
Reviewer note: static read-only inspection; nothing in the target was executed.
Host capability basis: <observed permissions/isolation, or unknown; state assumptions>
```

## Lethal trifecta (always, near the top)

```
Lethal trifecta: [private data: yes/no/unknown] [untrusted content: yes/no/unknown] [external comms: yes/no/unknown]
=> 0-1 of 3: low concern | 2 of 3: WARNING | 3 of 3: CRITICAL EXPOSURE
```

The count applies to established capabilities. An `unknown` is not a `no`:
record the affected assessment as `NEEDS REVIEW`, identify the missing host
configuration, and make the install verdict conditional on verifying it.

## Category table (full audit)

```
| AST | Title | Verdict | Top finding |
|-----|-------|---------|-------------|
| AST01 | Malicious Skills | FINDING | Credential exfil in scripts/bootstrap.sh:19 |
| ...   | ... | PASS / FINDING / NEEDS REVIEW / N/A | ... |
```

## Finding block (repeat per finding, most severe first)

```
### [SEVERITY] <short title>
- Category: AST0N — <title>
- Severity: Critical | High | Medium | Low | Informational
- Location: <file>:<line>
- Evidence:
      <quoted snippet — quote it, never re-run it>
- Why it matters: <impact in one or two sentences>
- Abuse scenario: <realistic attacker path from this to harm>
- Remediation: <concrete fix>
- Confidence: High | Medium | Low
```

Severity is impact × exploitability. Credential-read-plus-egress, remote code
execution, prompt injection against the agent, and persistence are Critical.
Confidence is separate from severity: a plausible-but-unconfirmed Critical is
still Critical, at lower confidence, and often `NEEDS REVIEW`.

## Footer

```
## Overall risk: Critical | High | Medium | Low
## Safe to install/enable? No | No, until blockers fixed | Yes, with cautions | Yes
## Blockers (fix before install):
  1. ...
## Recommended hardening:
  1. ...
```
