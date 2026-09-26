# nuxt

A Claude Code skill for Nuxt work. It supplies what reading your project cannot: which Nuxt release you actually run, what that release lacks that the docs already describe, how `compatibilityVersion: 5` changes a 4.x install, and a verification step that catches what `nuxi build` misses.

## What it does

Three steps, on every invocation:

1. **Detects** the resolved `nuxt` version (not the `^` range), the compat flag in your config and every layer's, your directory layout, and the installed Nitro, h3 and Unhead majors.
2. **Loads the version boundary** — `releases.md` always; `compat-v5.md` only when the flag is `5`; `conventions.md` only when the task touches layers, modules, `server/utils`, `shared/`, `app.config` or fetch keys.
3. **Verifies** — baselines `nuxi typecheck`, re-runs it, builds, and requests every server route it touched.

## What it deliberately does not do

It does not teach Nuxt idiom, because Claude already knows it.

Before a line of it was written, eight coding runs on a real Nuxt 4.5.2 project recorded what Claude produces unaided. Seven were correct: `shallowRef`-safe updates to `data`, `undefined` defaults, `return navigateTo(...)` in middleware, `useRuntimeConfig(event)`, `#shared` types, `swr` over `isr` on Node, `NuxtErrorBoundary`, typed routes. Two closed-book quiz runs over 113 verified facts got 88 right both times — almost all of data fetching, errors and route rules.

So the skill is three short references, not a documentation dump. `llms-full.txt` is 4.8 MB; the whole skill is about 300 lines.

## Where Claude actually fails

**The docs describe a release you cannot install.** `nuxt.com/docs/4.x` documents Nuxt 4.6 — `nuxt/server`, `addNitroPlugin`, `serialize`, session helpers — while npm's latest is 4.5.2. Many of those pages carry no version badge. A Claude that fetches the current docs writes code for a release the project does not have.

**`compatibilityVersion: 5` breaks server code silently.** It turns off every Nitro auto-import. Code written the usual way builds clean and then returns 500 `defineEventHandler is not defined` on the first request. This was the only coding failure, and it reproduced in 2 of 2 unaided runs.

**Confident wrongness about discovery rules.** Asked whether nested `server/utils` files are auto-imported, Claude answered "only top-level" — labelled CERTAIN. Nitro scans `utils/**/*`.

## Verification

`nuxi build` exits 0 on the compat-5 failure above, so a build alone proves little. The skill baselines `nuxi typecheck` before writing, re-runs it after, builds, then runs the built output using the Nitro preset's local runner and requests each route it touched. Node-server output uses a free port; serverless and worker output needs a platform runner, and missing tooling is reported as blocked route verification. It also knows that `typescript@latest` is now 7, which `vue-tsc` 3 cannot load, and pins `typescript@^6` when typecheck crashes. It reports "typechecks", "builds", "routes respond" — never "works".

## Staying current

Every fact cites the docs page it came from. `scripts/check-freshness.sh` re-fetches the cited pages, compares them with `references/sources.lock`, and compares npm's latest `nuxt` with the version the references were distilled for. It reports; it never rewrites a reference.

```bash
bash skills/nuxt/scripts/check-freshness.sh           # exit 0 unchanged, 1 changed, 2 fetch failed
bash skills/nuxt/scripts/check-freshness.sh --update  # after re-distilling
```

## Install

See the [repository README](../../README.md) for the plugin install.

To copy this skill directly instead:

```bash
# personal, all projects
mkdir -p ~/.claude/skills && cp -r skills/nuxt ~/.claude/skills/

# project-local, shared via git
mkdir -p .claude/skills && cp -r skills/nuxt .claude/skills/
```

Both are safe to re-run to update an existing copy.

## Usage

Describe the change you want. The skill fires on Nuxt vocabulary, and on plain requests like "add a status page and endpoint" once it sees `nuxt` in your project. Both paths were exercised in fresh sessions.

## Scope

Nuxt core on 4.x, including projects that opt into `compatibilityVersion: 5`. Not `@nuxt/ui` components or theming — the [`nuxt-ui`](https://ui.nuxt.com) skill covers those — and not Vue or Vite work outside a Nuxt project.

## What is verified

The compat-5 import fix, the unreleased-4.6 guard, triggering with and without the word "Nuxt", not firing on plain Vue, and the verify step's success path were exercised in fresh sessions against real fixtures. Every fact in the references was confirmed in the installed 4.5.2 package or by a typecheck, build or request.

Not verified: the TypeScript 7 branch of the verify step inside a skill run (observed by hand only), the fallback for projects newer than 4.5.2 (no newer release exists), and `check-freshness.sh` detecting a real change. On a `@nuxt/ui` task in a project without `@nuxt/ui` installed, this skill fired alongside `nuxt-ui` rather than deferring entirely. Each scenario ran once. Full records: [RED](../../docs/superpowers/plans/2026-09-24-nuxt-red-results.md), [GREEN](../../docs/superpowers/plans/2026-09-24-nuxt-green-results.md).
