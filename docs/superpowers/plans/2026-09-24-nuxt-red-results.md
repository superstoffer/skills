# `nuxt` skill — RED results

**Date:** 2026-09-24
**Spec:** `docs/superpowers/specs/2026-09-24-nuxt-skill-design.md`
**Skill present during RED:** none. No `nuxt` skill existed in `~/.claude/skills`,
the plugin cache, or this repo. Coding agents were told not to invoke the Skill
tool. The installed `nuxt-ui` skill was therefore unused.

## Fixtures

| ID | Path (gitignored) | State |
|---|---|---|
| F-BASE | `.context/fixtures/nuxt-base` | `nuxi init -t minimal`, `nuxt` resolved **4.5.2**, nitropack 2.13.4, h3 1.15.11, vue-router 5.3.1, vite 8.3.1, `@unhead/vue` 3.4.1; `vue-tsc` 3.3.11 + `typescript` 6.0.3 |
| F-V5 | `.context/fixtures/nuxt-v5` | F-BASE plus `future: { compatibilityVersion: 5 }` |

Both typecheck and build clean before any run.

**Found while building the fixture.** `npm i -D vue-tsc typescript` installs
`typescript@7.0.2` (the current `latest`), and `nuxi typecheck` then crashes:
`ERR_PACKAGE_PATH_NOT_EXPORTED: Package subpath './lib/tsc' is not defined by
"exports"`. `vue-tsc` 3.x cannot load TypeScript 7. Pinning `typescript@^6`
fixes it. The fixture was pinned before the runs, so no coding agent met this —
but any fresh project will.

## Source of truth

npm `nuxt@latest` is **4.5.2** (2026-08-05). There is no 4.6 on npm, not even a
prerelease. The `docs/4.x` pages already describe 4.6: some with a `v4.6`
badge, many with **no badge at all**. Three ground-truth agents distilled 108
facts from the 286 local `docs/4.x` pages and checked each against the
installed 4.5.2 code, recording both sides where they disagree.

Documented but absent from 4.5.2 (selection, no badge unless noted):
`nuxt/server` import surface · `addNitroPlugin` (kit exports `addServerPlugin`)
· `addServerHandler({ handler: { nuxt, nitro2 } })` (TypeError at runtime) ·
`tryUseNitro` and four other kit utilities · `server/types/` and `app/types/`
auto-imports · `appSecret` / `NUXT_APP_SECRET` / `deriveSecret` ·
`SharedAppConfig` · `serialize` on `useFetch` (badged) · `stripNeverHydratedData`
· `navigateToEarlyReturn` · `routeTypedFetch` · function-valued `useCookie`
`expires` (throws) · `experimental.prerenderErrorPages` · dev `error.cause`
exposure · and, in the v5 list of `upgrade.md`, case-sensitive routing,
`typedPages` by default, `extractSerializablePageMeta`, PostCSS defaults, TS
`baseUrl`. The docs also still say Unhead v2; 4.5.2 installs v3.

**Consequence for the design:** the spec's live-`.md` fallback is unsafe as
written. A Claude that fetches current docs for a 4.5.2 project writes 4.6 code.
The installed package's types are the authority; docs are a lead.

## Coding runs

Eight fresh subagents, one task each, default model, tools enabled, no skill.
Graded by reading the diff against the ground truth and by the agent's own
verification transcript.

| # | Fixture | Task | Result |
|---|---|---|---|
| 1 | F-BASE | `useFetch` list + filter + refresh, optimistic rename, shared categories | **PASS.** Reassigned `data.value` (shallowRef-safe), explicit shared key, knew `dedupe: 'cancel'` default and chose `'defer'` |
| 2 | F-BASE | `server/api` route, private + public runtime config, `shared/` type, logger | **PASS.** `#shared/types`, `useRuntimeConfig(event)`, `NUXT_PUBLIC_*`, key kept out of client bundle |
| 3 | F-V5 | SEO meta server-only, client-only component, SSR-safe composable, `.client`/`.server` plugins | **PASS.** Avoided `useServerSeoMeta` (noticed it is not auto-imported), `import.meta.*` throughout |
| 4 | F-BASE | Cookie auth, named + global middleware, 403, typed routes | **PASS.** `return navigateTo`, `abortNavigation(createError({ fatal: true }))`, `experimental.typedPages`, verified a typo fails typecheck |
| 5 | F-BASE | Local layer, override component + one `app.config` key, disable layer module | **PASS, by experiment.** `devtools: false` did not disable the layer's devtools module; found `devtools: { enabled: false }` by running `loadNuxt` |
| 6 | F-BASE | Local module: component, import, server route, Nitro plugin, typed options | **PASS.** `addServerPlugin` (correct for 4.5.2). Reported that `modules/*/index.ts` plus a `nuxt.config` entry installs the module twice — **not reproduced**; see "Correction" below |
| 7 | F-BASE | `routeRules` (prerender, swr, ssr:false, cors, 301), 404, `error.vue`, `NuxtErrorBoundary` | **PASS.** Chose `swr` over `isr` for Node; `{ to, statusCode: 301 }` |
| 8 | F-V5 | Notes API with `server/utils`, `shared/utils`, server middleware | **FAIL, then recovered.** Wrote auto-imported server code; `nuxt build` succeeded; every route crashed at runtime (`defineEventHandler` undefined). Recovered only because it chose to curl the built server |

Every agent verified heavily without being asked: typecheck, build, curl
against the built server, and in three runs Playwright. Run 6 killed a sibling
run's server with `pkill -f`; later prompts forbid pattern kills.

**Reading.** As with `nest`, Claude writes idiomatic Nuxt 4 unaided. The one
real failure (run 8) is a compat-v5 behaviour that **builds clean and fails at
runtime**, and the two near-misses (runs 5, 6) were rescued by experiments a
less diligent session would not run.

## Knowledge probe

Two independent closed-book runs (no tools), 114 questions: the 108 ground-truth
probes plus 6 drawn from the coding runs. A fact is **kept** if either run
answered it wrong or DON'T KNOW; a fact both runs got right is dropped, whatever
the confidence label.

| Outcome | Count |
|---|---|
| Right in both runs | 88 |
| Wrong/DK in both runs | 17 |
| Wrong/DK in one run only | 8 |
| Withdrawn (X-05, see Correction) | 1 |
| Confidently wrong (CERTAIN) | 1 — SV-09 |

**Wrong or DON'T KNOW in both runs:**

| ID | Truth on 4.5.2 | Probe answer |
|---|---|---|
| SV-09 | nitropack scans `server/utils/**/*` (nested files auto-import) | "only top-level" — **CERTAIN** in run A |
| V5-05 / SV-13 | compat 5 turns Nitro auto-imports off entirely | "still works on 4.5.2" (both) |
| V5-04 | `process.client` still replaced at runtime, but fails typecheck (TS2591) | "no longer works" |
| V5-10 | `.client` components render a comment node in SSR under v5 | "placeholder keeps class" |
| LY-01 | a `layers/*` dir without `nuxt.config` is silently skipped | "auto-registered anyway" |
| X-04 | `devtools: false` does not disable devtools (ignored key) | "yes it does" |
| SEO-01 | Unhead **v3** | "v2" |
| RT-09 | `definePageMeta({ layout: { name, props } })` (4.3/4.4) | `<NuxtLayout>` workaround |
| RT-10 | `useLayout()` (4.5) | `route.meta.layout` |
| DF-13 | `enabled` option (4.5); re-enabling does not refetch | DK |
| RR-08 | `prerenderErrorPages` is 4.6-only | DK |
| MD-02 | variant-object `handler` is 4.6-only; TypeError on 4.5.2 | DK |
| X-01 | npm latest is 4.5.2; 4.6 unreleased | DK |
| X-02 | TypeScript 7 breaks `vue-tsc` 3; pin `^6` | DK / wrong guess |
| RR-05 | page `definePageMeta({ layout })` beats `appLayout` | DK in both (one guessed right) |
| SV-08 | event-less `useRuntimeConfig()` is deep-frozen; mutating throws | "leaks across requests" — right advice, wrong mechanism. **Not shipped**: the advice Claude gives ("don't mutate it") is already correct |

**Wrong or DON'T KNOW in one run only:** DF-04 (auto-key includes call site),
DF-11 (`immediate: false` + key change does not fetch), DF-14 (`serialize` is
4.6), LY-05 (layer with `app/` ignores root `app.config.ts`), V5-08 (Options
API compiled out under v5), V5-12 (`navigateToEarlyReturn` is 4.6), SEO-02
(`templateParams` need no plugin), MD-04 (typed config key needs `meta.name`
too).

**Right in both:** effectively all of data fetching (16 of 19), errors (9 of 9),
`routeRules` semantics, runtime config, `shared/`, route middleware.

## Decisions

1. **The six task-oriented references are cut.** `data-fetching.md`,
   `routing.md`, `server.md`, `config-and-modules.md` and `rendering-and-seo.md`
   would restate what both probes and all seven v4 coding runs got right. The
   spec's rule — cut any reference RED does not justify — applies.
2. **What survives groups by failure cause, not by task:**
   - `references/releases.md` — the version boundary: what 4.3–4.5 added, what
     the docs describe that 4.5.2 lacks, and the installed stack majors.
     Justified by X-01, SEO-01, RT-09, RT-10, DF-13, RR-08, MD-02 and the
     docs-lead finding.
   - `references/compat-v5.md` — loaded only with the flag. Justified by run 8
     (the only coding failure), V5-05, V5-04, V5-10, V5-08, V5-12.
   - `references/conventions.md` — discovery, scanning and merge rules that
     fail silently. Justified by SV-09 (confidently wrong), LY-01, LY-05, X-04,
     MD-04, DF-04, DF-11.
3. **Verification gains two steps.** Pin `typescript@^6` when `vue-tsc` crashes
   (X-02), and smoke-request every server route the task touched — `nuxt build`
   passed on run 8's broken code.
4. **The docs fallback is gated on installed types.** Fetched docs may describe
   4.6; any API taken from them is checked against `node_modules` before use.

## Correction — X-05 withdrawn

Run 6 reported that a module at `modules/analytics/index.ts`, also listed in
`nuxt.config`, was installed twice. That claim entered the first draft of
`conventions.md` without independent verification. A later unaided run of the
same task reported the opposite, which prompted a direct test on F-BASE: a
module at `modules/dup/index.ts` listed as `./modules/dup`,
`./modules/dup/index` and `./modules/dup/index.ts`, with and without
`meta.name`. `setup` ran **once** in every case; after `nuxi build`, a Nitro
plugin it registered initialised once and logged once per request. Both probes
had answered "deduplicated" — correctly. X-05 is withdrawn and the rule removed.

The lesson is procedural: an agent's explanation of its own observation is a
hypothesis, not ground truth. Every other fact in the references was confirmed
in installed code or by a typecheck/build/request run on a fixture.
