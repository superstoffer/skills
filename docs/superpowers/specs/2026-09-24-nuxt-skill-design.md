# Design: `nuxt` skill

**Date:** 2026-09-24
**Status:** Approved in brainstorming
**Repo:** `superstoffer/skills`

---

## Objective

Add a Nuxt skill to this collection so that Nuxt code Claude writes matches
the Nuxt release a project actually runs — including releases and
compatibility flags published after the training cutoff — and so that the
output is verified to typecheck and build.

## Background

Nuxt publishes its documentation for language models in two forms:

| Source | Size | Approx. tokens |
|---|---|---|
| `nuxt.com/llms.txt` (index) | 58 KB | ~15k |
| `nuxt.com/llms-full.txt` (everything) | 4.8 MB | ~1.2M |

Neither can ship as a skill. The full file exceeds any context window; the
index costs ~15k tokens per invocation and carries links, not facts. The full
file also mixes three documentation versions — 1,012 `docs/3.x` links, 1,256
`docs/4.x`, 1,296 `docs/5.x` — so distilling it means choosing a version per
fact.

**The docs lead npm.** On 2026-09-24 `nuxt@latest` is **4.5.2**, while the
docs describe v4.6 features and Nuxt 5 behaviour reachable today through
`future.compatibilityVersion: 5`. A bundle has to be stamped with the version
it was taken from.

**Live Markdown exists.** Every docs page is served as Markdown by appending
`.md` (verified: HTTP 200, `text/markdown`), and an MCP server runs at
`nuxt.com/mcp`. This is the fallback when a project is newer than the bundle.

**Nuxt UI is already covered.** `~/.claude/skills/nuxt-ui` — the official
Nuxt UI skill, 334-line SKILL.md plus component, theming, and layout
references — is installed. A second skill covering `@nuxt/ui` would compete
with it for triggering.

## Decisions

| Question | Decision |
|---|---|
| Scope | **Nuxt core only.** `@nuxt/ui` components defer to `nuxt-ui`. |
| Versions | **Nuxt 4.x, including projects that opt into `compatibilityVersion: 5`.** Nuxt 3 migration is out of scope. |
| Motivation | Proactive — no observed failure. RED decides what ships. |
| Approach | **Curated knowledge bundle**, distilled from `llms-full.txt` into task-oriented topic references, version-stamped, with a live-`.md` fallback. |

Two approaches were considered and not chosen: a pure live-lookup router
(small and always current, but it relies on Claude noticing uncertainty, and
the `nest` baseline showed the dangerous failure is confident wrongness), and
a `nest`-style minimal delta skill. The chosen design keeps the latter's
discipline — RED decides content, verification is mandatory — inside the
bundle approach.

## Goals

- Nuxt help fires from a description of the task, without the user naming
  the skill, in any project with a `nuxt` dependency.
- Generated code matches the resolved `nuxt` version and the project's
  `compatibilityVersion`.
- Generated code typechecks and builds against the project it was written
  into.
- The bundle can be refreshed by re-checking only the source pages that
  changed.

## Non-goals

- `@nuxt/ui`, Nuxt Content, Nuxt Image, or any other module's API.
- Nuxt 2 or Nuxt 3 → 4 migration.
- Vue, Vite, Nitro, or h3 APIs beyond what Nuxt itself re-exports.
- Automatic regeneration of the bundle. Distillation needs judgment.

## Structure

```
skills/nuxt/
  SKILL.md                     ~120 lines  trigger, detect, load topic, verify, freshness
  README.md
  references/                  each <= ~200 lines, headed with source version + fetch date
    routing.md                 pages, layouts, route middleware, navigation, typed routes
    data-fetching.md           useFetch / useAsyncData / useState, v4 defaults, keys, caching
    server.md                  server/ + shared/, Nitro/h3 handlers, runtime config, server plugins
    config-and-modules.md      nuxt.config vs app.config, layers, @nuxt/kit modules, hooks
    rendering-and-seo.md       routeRules, hybrid rendering, useHead/useSeoMeta, errors
    compat-v5.md               compatibilityVersion: 5 deltas; loaded only when the flag is set
  scripts/
    check-freshness.sh         re-fetch llms-full.txt; report cited pages whose content changed
```

The split is by **task**, not by the docs' own sections, because a task is
what Claude holds when deciding what to load. Any reference that RED does not
justify is cut before release.

### SKILL.md

- **Trigger.** Nuxt vocabulary (`nuxt.config`, `useFetch`, `useAsyncData`,
  `server/api`, `defineNuxtRouteMiddleware`, `routeRules`, layers,
  `@nuxt/kit`, `nuxi`) **or** project evidence (`nuxt.config.ts`, `nuxt` in
  `package.json`) when the user never says "Nuxt". Excludes `@nuxt/ui`
  component work and plain Vue/Vite.
- **Hard rule.** No `nuxt` dependency: say so and stop.
- **Detect.** Resolved `nuxt` from `node_modules/nuxt/package.json` or the
  lockfile, never the declared range; `future.compatibilityVersion` in
  `nuxt.config.ts`; `srcDir` and `app/` layout; `extends` layers; package
  manager from the lockfile.
- **Load.** Only the topic references the task needs; `compat-v5.md` if and
  only if the flag is `5`.
- **Freshness.** If the resolved `nuxt` is newer than a reference's header,
  fetch `https://nuxt.com/docs/4.x/<path>.md` for the specific API before
  writing.
- **Verify.** Baseline `nuxi typecheck` before writing, re-run after, then
  `nuxi build`. At most two repair attempts, confined to files the skill
  wrote. Report "typechecks" and "builds" — never "works".

## Building the bundle

1. Fetch `llms-full.txt` and `sitemap.md`; record the fetch date and
   `nuxt@latest`.
2. Distill per topic. **Keep** signatures, defaults (especially those that
   changed in 4.x), version badges v4.2–v4.6, deprecations, and pitfalls that
   typecheck clean. **Cut** tutorial prose and examples Claude already writes
   correctly. 4.x docs win conflicts; 5.x content goes only to
   `compat-v5.md`.
3. Every fact carries its source: `<!-- src: /docs/4.x/... -->`.
4. **Trim** against a tools-disabled knowledge probe. Drop facts Claude
   answers correctly and confidently; keep what it gets wrong or refuses.

Refresh: `check-freshness.sh` reports which cited pages changed; a person or
agent re-distils only those facts and bumps the headers.

## Validation

**RED — before any skill file exists.** Fixture: a fresh `nuxi init` project
on 4.5.2 under `.context/fixtures/`, plus a copy with
`compatibilityVersion: 5`.

- Knowledge probe, tools disabled, answers labelled CERTAIN / UNSURE /
  DON'T KNOW.
- Seven coding runs, one fresh subagent each:
  1. A page using `useAsyncData` with a key and refresh (v4 defaults).
  2. A `server/api` route using runtime config and `shared/` types.
  3. On the v5 fixture: SEO meta and client-only logic.
  4. Auth route middleware with `navigateTo` / `abortNavigation`, typed routes.
  5. Extend a local layer; override its component and config.
  6. A local module via `defineNuxtModule` adding a component, an import, and
     a server handler.
  7. `routeRules` per route plus `createError` / `error.vue`.

**GREEN — with the skill.** The same seven tasks; trigger tests (a Nuxt
project task without the word "Nuxt" fires; a `UForm` task goes to `nuxt-ui`;
plain Vue + Vite fires neither); and the verify step's success path against a
real `nuxi typecheck` and `nuxi build` — a path the `nest` skill never
exercised.

Results are recorded in `docs/superpowers/plans/2026-09-24-nuxt-red-results.md`
and `...-green-results.md`, with a verified / not-verified table.

## Release

Add a row to the root `README.md`, write `skills/nuxt/README.md`, and bump
`.claude-plugin/plugin.json` and `marketplace.json` from 1.5.0 to 1.6.0.
