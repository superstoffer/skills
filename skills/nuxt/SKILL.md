---
name: nuxt
description: >-
  Write or change code in a Nuxt application. Use when the request names Nuxt
  or its vocabulary: nuxt.config, app.config, useFetch, useAsyncData,
  useState, useRuntimeConfig, definePageMeta, route middleware, navigateTo,
  routeRules, layouts, server/api, server/utils, shared/, Nitro plugin,
  layers, defineNuxtModule, @nuxt/kit, nuxi, compatibilityVersion, error.vue,
  or useSeoMeta. ALSO use when the project is Nuxt — nuxt in package.json or
  a nuxt.config.ts at the root — and the user asks for a page, an API route,
  auth, SEO, a layout, a module, or an upgrade WITHOUT naming Nuxt; check for
  that evidence before concluding this does not apply. NOT for @nuxt/ui
  components or theming (the nuxt-ui skill covers those), and NOT for Vue or
  Vite work outside a Nuxt project.
---

# Nuxt

Supply what reading the project cannot tell you — which Nuxt release it runs,
what that release lacks that the docs already describe, and the few behaviours
that fail without an error — then verify what you wrote.

## What this skill does not do

It does not teach Nuxt idiom. Unaided, Claude already writes correct Nuxt 4:
`data` as a `shallowRef`, `undefined` defaults, `status` over `pending`,
`return navigateTo(...)` in middleware, `useRuntimeConfig(event)`, `#shared`
types, `swr` over `isr` on Node, `app/error.vue`, `clearError({ redirect })`.
Restating that would cost context and change nothing.

What it supplies:

1. **The release boundary.** The `docs/4.x` pages lead npm. They describe
   Nuxt 4.6 — `nuxt/server`, `addNitroPlugin`, `serialize`, session helpers —
   while npm's latest is 4.5.2, and many of those pages carry no version
   badge. Fetching current docs produces code for a release the project does
   not have.
2. **`compatibilityVersion: 5` behaviour** on a 4.x install, where server code
   builds clean and fails at runtime.
3. **Discovery rules that fail silently** — a skipped layer, an ignored
   `app.config`, a nested util that is or is not auto-imported.
4. **Verification** that catches what `nuxi build` does not.

## Hard rules

1. **No `nuxt` dependency: say so and stop.** Never scaffold Nuxt code into a
   plain Vue or Vite project, and never offer to install Nuxt unless asked.
2. **Installed code beats documentation.** Before using an API you know from a
   docs page — fetched or remembered — confirm the resolved package exports
   it: grep `node_modules/nuxt/dist`, `@nuxt/kit/dist/index.d.mts`, or
   `@nuxt/schema/dist`. Absent means unreleased for this project; use the
   equivalent in `references/releases.md`.
3. **Under `compatibilityVersion: 5`, every `server/` file imports what it
   uses** — from `h3`, `nitropack/runtime`, `#server/...`, `#shared/...`.
   Without imports, `nuxi build` exits 0 and the route returns 500
   `ReferenceError: defineEventHandler is not defined`.

## Step 1 — Detect

**Read the resolved version, not the declared range.** `package.json` says
`^4.0.0`; that cannot distinguish 4.0 from 4.5, and the boundary between them
decides real behaviour. Read `node_modules/nuxt/package.json`, or the lockfile.

| Read | Determines |
|---|---|
| Resolved `nuxt` | Which rows of `references/releases.md` exist for this project |
| `future.compatibilityVersion` in `nuxt.config.ts` and in every layer's config | Whether `references/compat-v5.md` applies |
| `srcDir`, and whether `app/` exists | Where `~` resolves; `server/`, `shared/`, `modules/`, `layers/` stay at the root |
| `layers/*`, `extends` | Layer rules in `references/conventions.md` |
| `modules/*` | Local modules that register themselves |
| Resolved `nitropack`, `h3`, `@unhead/vue` | Server and head API surface |
| Resolved `typescript`, `vue-tsc` | Whether typecheck can run (Step 3) |
| Lockfile name | Package manager for Step 3 |

## Step 2 — Load what you cannot know

- **Always:** `references/releases.md`. Check its version stamp against the
  resolved `nuxt`.
- **If the compat flag is `5`:** `references/compat-v5.md`.
- **If the task touches layers, local modules, `server/utils`, `shared/`,
  `app.config`, or `useFetch` keys and watching:**
  `references/conventions.md`.

**If the project resolves a newer `nuxt` than the references' stamp**, the
"not in 4.5.2" rows may now exist. Fetch the specific page as Markdown —
`https://nuxt.com/docs/4.x/<path>.md` — then apply hard rule 2 before using
anything it shows. Never fetch `llms-full.txt`; it is ~1.2M tokens and mixes
three major versions.

## Step 3 — Verify

1. **Baseline before writing.** Run `npx nuxi typecheck` and record existing
   errors, so they are not mistaken for yours.
   - `ERR_PACKAGE_PATH_NOT_EXPORTED ... './lib/tsc'`: `vue-tsc` 3 cannot load
     TypeScript 7. Install `typescript@^6` as a dev dependency and say so.
   - `vue-tsc` missing: install `vue-tsc` and `typescript@^6` as dev
     dependencies and say so. Do not skip the step.
2. **After writing,** re-run `npx nuxi typecheck`. New errors in files you
   wrote are yours.
3. **Run `npx nuxi build`.**
4. **If you added or changed server routes,** start
   `node .output/server/index.mjs` with `PORT` set to a random free port,
   request each route you touched, then stop that process by its PID. Never
   `pkill` by pattern — other sessions may be serving from the same path.
   A clean build does not prove a route loads.

Cap repairs at two attempts, confined to files you wrote. Report what was
checked: "typechecks", "builds", "routes respond" — never "works".
