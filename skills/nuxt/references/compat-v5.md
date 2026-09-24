# `future.compatibilityVersion: 5` on Nuxt 4.x

> Distilled for Nuxt 4.5.2 from docs fetched 2026-09-24, checked against the
> installed package. Load only when the project, or a layer it extends, sets
> `future.compatibilityVersion: 5`.

The flag flips Nuxt 5 **defaults** on a 4.x install. It does not upgrade the
server: the project still runs nitropack 2 and h3 1. <!-- src: /docs/4.x/getting-started/upgrade -->

## Server code must import everything

`experimental.nitroAutoImports` becomes `false`, and Nitro gets
`imports: false`. Nothing under `server/` is auto-imported — not h3 helpers,
not `useRuntimeConfig`, not `server/utils`, not `shared/utils`.
<!-- src: /docs/4.x/getting-started/upgrade -->

This is the failure that matters: **`nuxi build` exits 0 and the route returns
500 `ReferenceError: defineEventHandler is not defined` at runtime.**
`nuxi typecheck` catches it as TS2304.

```ts
// server/api/notes.post.ts — compat 5
import { createError, defineEventHandler, readValidatedBody } from 'h3'
import { useRuntimeConfig } from 'nitropack/runtime'
import { notesStore } from '#server/utils/notes'
import { formatDate } from '#shared/utils/formatDate'
```

`defineNitroPlugin` also comes from `nitropack/runtime`. Do not import from
`nuxt/server`; it ships in 4.6. To keep the old behaviour instead, set
`experimental: { nitroAutoImports: true }`.
<!-- src: /docs/4.x/guide/going-further/server-imports -->

## Silent behaviour changes

Each of these typechecks clean and misbehaves at runtime.

| Change | Consequence | Keep old behaviour / fix |
|---|---|---|
| `useServerHead`, `useServerHeadSafe`, `useServerSeoMeta` lose their auto-import | TS2304 on bare use | `if (import.meta.server) { useSeoMeta({...}) }` <!-- src: /docs/4.x/api/composables/use-server-seo-meta --> |
| Vue Options API compiled out (`__VUE_OPTIONS_API__: false`) | `data()`, `methods`, `computed:` stop working | `vue: { optionsApi: true }`, or `<script setup>` <!-- src: /docs/4.x/getting-started/upgrade --> |
| `experimental.clientNodePlaceholder` | `.client.vue` components render an HTML comment in SSR; their `class`/`style` never reach the SSR HTML | `<ClientOnly>` with a `#fallback` to reserve space <!-- src: /docs/4.x/guide/going-further/experimental-features --> |
| `experimental.normalizePageNames` | page component names follow the route (`foo`, not `index`) | update `<KeepAlive include/exclude>` <!-- src: /docs/4.x/guide/going-further/experimental-features --> |
| `useState` `resetOnClear` | `clearNuxtState(key)` re-runs the init value instead of setting `undefined` | `clearNuxtState(key, { reset: false })` <!-- src: /docs/4.x/api/utils/clear-nuxt-state --> |
| `experimental.asyncCallHook: false` | `nuxtApp.callHook(...)` may return `void`; `.then()` throws | `await nuxtApp.callHook(...)` <!-- src: /docs/4.x/getting-started/upgrade --> |
| Unhead registers only `TemplateParamsPlugin` | `hid`, `vmid`, promise values and `tagPriority: 'before:…'` stop working; `unhead.legacy` is forced off (NUXT_B5013) | dedupe with `key`; resolve promises first <!-- src: /docs/4.x/getting-started/upgrade --> |
| `experimental.payloadExtraction: 'client'` | first load inlines the payload; `_payload.json` only on client navigation | expected; no action <!-- src: /docs/4.x/getting-started/prerendering --> |
| `experimental.viteEnvironmentApi` | Vite plugins run per environment | register with `addVitePlugin`; use `applyToEnvironment` for per-side plugins <!-- src: /docs/4.x/guide/going-further/experimental-features --> |

The generated tsconfig also adds `noUncheckedSideEffectImports: true`.

## Listed as v5 in the docs, not flipped on 4.5.2

`upgrade.md` lists these under the flag, but the installed 4.5.2 schema does
not change them. They arrive in 4.6. Do not rely on them, and do not "fix"
code for them:

- case-sensitive routing — `/About` still matches `pages/about.vue`
- `experimental.typedPages` on by default — still opt-in
- `navigateToEarlyReturn` — code after `await navigateTo()` still runs; keep
  `return navigateTo(...)`
- `extractSerializablePageMeta`, `routeTypedFetch`, `strictRouteTypes`
- PostCSS `autoprefixer`/`cssnano` defaults off; TS `baseUrl` removal
<!-- src: /docs/4.x/getting-started/upgrade -->

## Unchanged by the flag, still wrong

`process.client` / `process.server` are still replaced at runtime under either
compat version, but `.nuxt/tsconfig.app.json` sets `"types": []`, so they fail
`nuxi typecheck` with TS2591 in app code. Use `import.meta.client` /
`import.meta.server`. <!-- src: /docs/4.x/api/advanced/import-meta -->
