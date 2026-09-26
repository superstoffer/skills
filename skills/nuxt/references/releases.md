# The 4.x release boundary

> Distilled for Nuxt 4.5.2 from docs fetched 2026-09-24, checked against the
> installed package. On 2026-09-24 npm `nuxt@latest` is 4.5.2; there is no 4.6
> on npm, not even a prerelease. Where docs and installed code disagree, the
> installed code is recorded here.

## Installed stack on 4.5.2

- **Server: nitropack 2, h3 1** — on every compat version. h3 v1 APIs apply:
  `readValidatedBody(event, schema.parse)` takes a function, not a schema
  object; `H3Error` exposes `statusCode`, not `status`.
  <!-- src: /docs/4.x/getting-started/upgrade -->
- **Head: Unhead v3**, not v2 as the upgrade guide says. `hid`, `vmid`,
  `children` and `body` are gone; compat 4 shims them through legacy plugins,
  compat 5 does not. `templateParams` work without registering a plugin.
  <!-- src: /docs/4.x/getting-started/upgrade -->
- **Typecheck: `vue-tsc` 3 needs TypeScript 6.** `typescript@latest` is 7,
  which `vue-tsc` 3 cannot load (`ERR_PACKAGE_PATH_NOT_EXPORTED ... './lib/tsc'`).

## Released in 4.2–4.5

Newer than most training data. On an older 4.x minor, a row above the
project's version does not exist yet.

| Since | Feature |
|---|---|
| 4.2 | `future.compatibilityVersion: 5` opt-in <!-- src: /docs/4.x/getting-started/upgrade --> |
| 4.2 | `createUseFetch` / `createUseAsyncData` for custom wrappers — per-call options override object-form defaults; pass a function to enforce them <!-- src: /docs/4.x/api/composables/use-fetch --> |
| 4.3 | `routeRules: { '/admin/**': { appLayout: 'admin' } }`; `appLayout: false` disables. A page's `definePageMeta({ layout })` still wins <!-- src: /docs/4.x/directory-structure/app/layouts --> |
| 4.3–4.4 (docs disagree) | Layout props: `definePageMeta({ layout: { name: 'panel', props: { title: 'x' } } })` or `setPageLayout('panel', props)`. Props must be serializable <!-- src: /docs/4.x/api/utils/set-page-layout --> |
| 4.3 | Route groups expose `route.meta.groups` (`pages/(admin)/users.vue` → `['admin']`) <!-- src: /docs/4.x/directory-structure/app/pages --> |
| 4.3 | `<configKey>: false` disables a module, including a layer's (not `devtools`; see `conventions.md`) <!-- src: /docs/4.x/guide/concepts/modules --> |
| 4.3 | `#server` alias, inside `server/` only <!-- src: /docs/4.x/directory-structure/server --> |
| 4.4 | `clearNuxtState(key, { reset: true })` resets to the init value; default sets `undefined` <!-- src: /docs/4.x/api/utils/clear-nuxt-state --> |
| 4.4 | `useCookie` `refresh` option <!-- src: /docs/4.x/api/composables/use-cookie --> |
| 4.5 | `enabled` on `useFetch`/`useAsyncData`: `false` blocks fetch, `execute`, `refresh` and watchers; switching back to `true` does **not** refetch — call `refresh()` <!-- src: /docs/4.x/api/composables/use-async-data --> |
| 4.5 | `useLayout()` — resolved layout name, including one set by `appLayout`; `route.meta.layout` misses those <!-- src: /docs/4.x/api/composables/use-layout --> |
| 4.5 | Named views `pages/parent/child@sidebar.vue`; page meta is read from the default view file only <!-- src: /docs/4.x/directory-structure/app/pages --> |

## Documented, but not in 4.5.2

These appear in `docs/4.x`. Many carry **no version badge**. On 4.5.2 they
fail to typecheck, do nothing, or throw.

| Docs describe | On 4.5.2 |
|---|---|
| `import { … } from 'nuxt/server'` | not exported; use auto-imports, or `h3` / `nitropack/runtime` <!-- src: /docs/4.x/guide/going-further/server-imports --> |
| `addNitroPlugin(path)` | `addServerPlugin(path)` <!-- src: /docs/4.x/api/kit/nitro --> |
| `addServerHandler({ handler: { nuxt, nitro2 } })` | `handler` must be a string path; the object form throws a TypeError <!-- src: /docs/4.x/guide/modules/server-compatibility --> |
| kit `tryUseNitro`, `ensureDependencyInstalled`, `getAddDependencyCommand`, `useTerminal`, `diffNuxtConfig` | not exported <!-- src: /docs/4.x/api/kit/nitro --> |
| `server/types/` and `app/types/` auto-imports | use `shared/types/` or an explicit import <!-- src: /docs/4.x/directory-structure/server --> |
| `appSecret`, `NUXT_APP_SECRET`, `deriveSecret`, built-in session helpers | h3 `useSession(event, { password })`, 32+ characters <!-- src: /docs/4.x/guide/going-further/runtime-config --> |
| `SharedAppConfig` interface | absent <!-- src: /docs/4.x/directory-structure/app/app-config --> |
| `serialize` on `useFetch`/`useAsyncData`; `experimental.stripNeverHydratedData` | ignored; use `pick` or `server: false` <!-- src: /docs/4.x/api/composables/use-fetch --> |
| `experimental.navigateToEarlyReturn` | absent; code after `await navigateTo()` runs — `return navigateTo(...)` <!-- src: /docs/4.x/api/utils/navigate-to --> |
| `routeTypedFetch`, `strictRouteTypes`, `early404`, `extractSerializablePageMeta` | absent <!-- src: /docs/4.x/guide/going-further/experimental-features --> |
| `useCookie` `expires` as a function | throws; pass a `Date` <!-- src: /docs/4.x/api/composables/use-cookie --> |
| `experimental.prerenderErrorPages` | absent; `404.html` is the SPA shell <!-- src: /docs/4.x/guide/concepts/rendering --> |
| `error.cause` exposed to `error.vue` in dev | not serialized <!-- src: /docs/4.x/getting-started/error-handling --> |
| v5 list items: case-sensitive routes, `typedPages` by default, PostCSS defaults, TS `baseUrl` | not flipped by the flag; see `compat-v5.md` <!-- src: /docs/4.x/getting-started/upgrade --> |

If the project resolves a version newer than 4.5.2, a row here may now exist.
Confirm it in the installed package before using it.
