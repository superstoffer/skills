# `nuxt` skill — GREEN results

**Date:** 2026-09-24
**RED:** `docs/superpowers/plans/2026-09-24-nuxt-red-results.md`
**Skill under test:** `skills/nuxt/` — SKILL.md plus `releases.md`,
`compat-v5.md`, `conventions.md`.

## Method

A running Claude Code session does not discover skills added after it
started, so in-session subagents could not load `nuxt`. GREEN coding and
trigger runs therefore used **fresh headless sessions** (`claude -p`), one per
fixture, each fixture carrying the skill at `.claude/skills/nuxt`. Prompts were
the RED prompts plus one line stating the run is non-interactive; none named
the skill. The in-session subagents launched before this was understood ran
without the skill and are recorded below as extra unaided samples.

## Knowledge probe

24 of the facts RED kept, answered by a fresh agent that first read the four
skill files. One of them, X-05, was withdrawn afterwards (see the RED
correction); the GREEN agent answered it from the draft that still contained
the wrong rule. The table scores the remaining 23.

| | RED run A | RED run B | GREEN |
|---|---|---|---|
| Correct of the 23 | 4 | 3 | **23** |
| Labelled CERTAIN and correct | 0 | 0 | **23** |

Not in the probe: DF-14 (`serialize` is 4.6) is covered by `releases.md`;
SV-08 was not shipped.

## Coding runs

| Run | Fixture | Skill fired | Result |
|---|---|---|---|
| gt-8 | v5 notes API (RED run 8, the only RED failure) | yes; read `compat-v5.md` | **FIXED.** Every `server/` file imported from `h3`, `#server/utils` and `#shared` on its **first write**. Independently re-verified: typecheck 0 errors, build exit 0, `GET` 200, `POST` 201, bad body 400, no `ReferenceError`. The session hit the account usage limit before its own route checks; the `X-Powered-By` header is overwritten to `Nuxt` on SSR pages — an unfinished task detail, unrelated to the skill |
| gt-9 | "Follow the current docs" module (new) | yes; read `releases.md`, `conventions.md` | **Single 4.5.2 path**: `addServerPlugin`, `h3`, `nitropack/runtime`. Stated plainly that the docs' `nuxt/server` style ships in 4.6 and could not be met on this project |
| gt-trig | `/status` page + endpoint, prompt never says "Nuxt" | **yes** | Typechecks, builds, routes respond — verified by the session and reported in exactly those words |

**Unaided comparison for gt-9.** Two runs without the skill (red-9, green-9)
also noticed the 4.6 gap — `nuxi typecheck` failed on `nuxt/server` — and both
shipped **two code paths** gated on the Nuxt version, one with a
`// @ts-ignore` on the unreleased import and one excluding files from the
typecheck. Correct, but carrying dead code the project cannot run. With the
skill the gap was named before writing and no dead path was produced.

**Unaided repeat of run 8.** A second unaided run of the v5 task (green-8)
reproduced the RED failure: first version relied on auto-imports, built clean,
and was caught only because the agent chose to test the running server. The
failure is 2 of 2 unaided, 0 of 1 with the skill.

## Triggering

| Prompt | Project | Expected | Observed |
|---|---|---|---|
| `/status` page + endpoint, no framework named | Nuxt 4.5.2 | `nuxt` | `nuxt` ✓ |
| `UForm`/`UInput` contact form with brand colours | Nuxt 4.5.2, no `@nuxt/ui` | `nuxt-ui`, not `nuxt` | `nuxt-ui` **and** `nuxt` — partial |
| Router + `/about` + fetch | plain Vue + Vite, skill installed in the project | none | none ✓ — cited the missing `nuxt` dependency against the description's evidence gate |

The UI case fired both skills. The session's reasoning: the project lacked
`@nuxt/ui` entirely, so the task included module installation and
`nuxt.config`/`app.vue` changes, which it judged to be Nuxt work. That is
defensible, and the two skills cooperated rather than conflicted — but the
boundary is not exclusive, and the description has not been changed to force
it.

## What is verified, and what is not

| Path | Status |
|---|---|
| compat-v5 server imports | **Verified** — failure 2/2 unaided, fixed 1/1 with skill; output re-run by hand |
| Unreleased-4.6 guard (hard rule 2) | **Verified** — gt-9 produced a single 4.5.2 path |
| Knowledge in the references | **Verified** — 23/23 on the facts RED kept |
| Triggering without the word "Nuxt" | **Verified** — gt-trig |
| Not firing outside Nuxt | **Verified** — gt-vue |
| Deferring `@nuxt/ui` work to `nuxt-ui` | **Partial** — `nuxt-ui` fired, `nuxt` fired alongside |
| Verify step, success path | **Verified** — gt-trig and gt-8 (typecheck, build, route requests) |
| Verify step, TypeScript 7 branch | **NOT verified** — every fixture was pinned to TypeScript 6 before testing; the crash and fix were observed by hand in RED only |
| Freshness fallback on a project newer than 4.5.2 | **NOT verified** — no newer release exists |
| `check-freshness.sh` detecting a real change | **NOT verified** — only the no-change and missing-lock paths ran |
| Sample size | One GREEN run per scenario. The usage limit ended the session before repeats |
