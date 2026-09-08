# AST05 — Untrusted External Instructions

The skill fetches its behavior — rules, prompts, code — from an external URL at
runtime, unpinned and unrescanned. What you reviewed is not what will run.

## Detection cues (static)

- Remote code execution: `curl … | bash`, `curl … | sh`,
  `eval "$(curl …)"`, `source <(curl …)`, `exec eval …`. Grep `curl`, `wget`,
  `eval`, `source <(`, `| sh`, `| bash`.
- Remote *instructions* loaded into the prompt: "fetch the rule pack from URL and
  execute", `WebFetch` of a config the skill then follows.
- Runtime code load in any language: `requests.get(url).text` into `exec()`,
  `import()` of a remote module, `Function(await fetch(...))`.
- The tell: a file that says "rules are not stored here, they are fetched fresh
  every run" — the repo you audited no longer describes what executes.

## Severity

Any `curl|bash`/`eval(remote)` = **Critical** — it defeats the entire review and
enables silent post-audit changes (compounds AST07).

## Remediation

Vendor the instructions/code into the repo and pin them. If a remote fetch is
truly required, pin by content hash and re-review on change; never `eval` the
response.
