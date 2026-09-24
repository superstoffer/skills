# Discovery and merge rules that fail silently

> Distilled for Nuxt 4.5.2 from docs fetched 2026-09-24, checked against the
> installed package. Load when the task touches layers, local modules,
> `server/utils`, `shared/`, `app.config`, or `useFetch` keys and watching.

Each rule below was answered wrong by Claude unaided. None produces an error
when broken: the file is skipped, the config is ignored, or the fetch does not
happen.

## Auto-imports

- **`server/utils/` is scanned recursively.** `server/utils/db/client.ts` is
  auto-imported in server code. Nitro globs `utils/**/*`.
  <!-- src: /docs/4.x/directory-structure/server -->
- **`shared/utils/` and `shared/types/` are scanned top-level only.** A nested
  file needs an explicit import: `import { upper } from '#shared/utils/formatters/upper'`.
  <!-- src: /docs/4.x/directory-structure/shared -->
- Neither applies under compat 5, which turns server auto-imports off. See
  `compat-v5.md`.

## Local modules

- **A typed `nuxt.config` key needs both `meta.name` and `meta.configKey`.**
  With only `configKey`, the key works at runtime but is untyped. Types appear
  after `nuxi prepare`. <!-- src: /docs/4.x/api/kit/modules -->

## Disabling a module

- Since 4.3, `<configKey>: false` in `nuxt.config` skips a module's setup —
  including one added by a layer. <!-- src: /docs/4.x/guide/concepts/modules -->
- **Exceptions:** `components`, `imports`, `pages`, `devtools` and `telemetry`
  ignore `false`. `devtools: false` leaves devtools running; use
  `devtools: { enabled: false }`.

## Layers

- **Every `layers/*` directory auto-registers, but only if it has a
  `nuxt.config.*`.** Without one it is skipped silently. An empty
  `export default defineNuxtConfig({})` is enough.
  <!-- src: /docs/4.x/directory-structure/layers -->
- **A layer with an `app/` directory scans from `app/`.** Its
  `app.config.ts`, `components/` and `pages/` belong at
  `layers/<name>/app/...`; root-level copies (Nuxt 3 layout) are ignored.
  <!-- src: /docs/4.x/guide/going-further/layers -->
- **`#layers/<name>` points at the layer root, not its `app/`.** Import
  `#layers/admin/app/composables/useAdmin`; the docs' shorter example fails.
  <!-- src: /docs/4.x/guide/going-further/layers -->

## Data fetching keys

- **`useFetch`'s generated key includes the call site.** Two components calling
  `useFetch('/api/x')` make two requests and hold separate state. Pass the same
  explicit `key` to share. <!-- src: /docs/4.x/api/composables/use-fetch -->
- **With `immediate: false`, changing the key, URL or query does not fetch**
  until `execute()` or `refresh()` has run once. Nuxt 3 fetched here.
  <!-- src: /docs/4.x/getting-started/upgrade -->
