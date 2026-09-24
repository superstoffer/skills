# nest docs refresh — fixture results

**Date:** 2026-09-24
**Spec:** [2026-09-24-nest-docs-refresh-design.md](../specs/2026-09-24-nest-docs-refresh-design.md)
**Environment:** Node 26.8.1, npm 11.19.0. Both fixtures were generated with
`npx @nestjs/cli@latest new` (CLI 12.0.6) in `.context/nest-fixture/` (gitignored).
Each subagent read the skill from the worktree, not from the stale 1.5.0 plugin cache.

## Fixtures

| Fixture | Module / runner | Resolved |
|---|---|---|
| `app` | ESM (`"type": "module"`) + Vitest 4.1 | `@nestjs/core`/`common` 12.1.0, `@nestjs/config` 12.0.1, `@nestjs/swagger` 12.0.2, TypeScript 6.0.3, Prisma 7.10.0, zod 4 |
| `cjsapp` | CommonJS (no `type`, tsconfig `nodenext`) + Jest 30.5 | same Nest and Prisma versions |

The generator was non-interactive: piped stdin produces the ESM default. The
CommonJS variant can only be chosen at the interactive prompt, so it was
scaffolded by driving that prompt with `expect`. tmux is not installed.

## Facts found by running, not by reading

These are corrections the docs audit alone could not have made. Each has been
folded into the skill.

1. **`require('<pkg>/package.json')` fails on v12 packages.** Their `exports`
   map (`"./*": "./*.js"`) resolves it to `package.json.js`. The skill's
   detection commands now read `./node_modules/<pkg>/package.json` by path.
2. **The old Swagger plugin paths fail under ESM.** `@nestjs/swagger/dist/plugin`
   throws `ERR_PACKAGE_PATH_NOT_EXPORTED`, and the extension-less
   `plugin-metadata-generator` import throws `ERR_MODULE_NOT_FOUND`. The docs'
   paths resolve.
3. **A fresh `nest new` v12 project fails its own typecheck.** It reports
   `test/app.e2e-spec.ts: Cannot find module 'supertest/types'`. This is direct
   evidence for the baseline-first rule.
4. **`tsc --noEmit` is not side-effect free.** Generated tsconfigs set
   `incremental`, so tsc rewrites `tsbuildinfo`. The fallback uses
   `--incremental false` for non-composite projects; composite projects keep
   incremental compilation and redirect `tsBuildInfoFile` to a temporary directory.
5. **A global pipe registered in `main.ts` misses e2e apps.** e2e apps built from
   `AppModule` never run `app.useGlobalPipes()`, so schema validation is silently
   off there. The skill now registers `StandardSchemaValidationPipe` through
   `APP_PIPE`. `useSecurityHeaders()` and `enableCsrfProtection()` have no module
   form, so the skill points to a shared `configureApp(app)`.
6. **`compile()` proves wiring, not connectivity.** It runs no lifecycle hooks,
   so Prisma's `$connect()` never fires and a bad URL passes.
7. **CommonJS + Jest fails under bare `npx jest`, even on Node 26.** It fails with
   "Must use import to load ES Module". The generated `test` script runs Jest
   under `node --experimental-vm-modules`, and `npm test` passes. The docs do not
   mention this.
8. **Prisma adapters take different constructor options.** `PrismaBetterSqlite3`
   takes `{ url }` and `PrismaPg` takes `{ connectionString }`.
9. **The Prisma 8 warning is real.** `prisma migrate` printed
   "Update available 7.10.0 -> 8.0.0-rc.15 … npm i prisma@latest".
10. **CommonJS + `nodenext` + Jest also needs `importFileExtension = ""`.**
    Even with `moduleFormat = "cjs"`, Prisma 7.10 writes `.js` into the
    generated client's relative imports. Jest resolves the `.ts` sources and
    fails with `Cannot find module './internal/class.js'`. I reproduced it by
    removing the line (the spec failed), and restoring the line brought back
    4/4 passing. The docs do not mention it.
11. **From 7.10, `moduleFormat = "cjs"` is inferred.** With the line removed,
    `nodenext` without `"type": "module"` still produced a CommonJS client with
    no `import.meta`, and the tests passed. The line is kept because it is
    harmless and required before 7.10.

## GREEN runs

### Run 1 — ESM fixture

Task: users resource with a Zod body, a UUID `x-tenant-id` header, Prisma on
SQLite, security headers, and a theme cookie.

- Detection was correct: common 12.1.0 → built-ins apply, ESM, Vitest, Prisma 7.10.
- Fetched `/security/helmet.md`, `/http/cookies.md`, `/application/validation.md`,
  `/application/configuration.md` and `/data/prisma.md`, and read both references.
- **Pass:**
  - `StandardSchemaValidationPipe({ validateCustomDecorators: true })` for the
    header decorator.
  - PrismaService in the docs' shape: adapter plus both hooks.
  - No `moduleFormat`, `.js` imports, and `prisma7.config.ts`.
  - `useSecurityHeaders()` and `@Cookies()`, with no helmet or cookie-parser.
- Typecheck errors went 1 → 1, the baseline `supertest/types` error only. The
  module graph compiles. e2e 6/6 and unit 1/1 passed. I re-verified this
  independently: a real SQLite round trip returned 201 on create and 409 on the
  duplicate.
- Exposed findings 4 and 5 and the adapter-options gap. All were fixed.

### Run 2 — ESM fixture, reset to baseline, after the fixes

Task: orders with a Zod body, Prisma on SQLite, and CSRF protection.

- Fetched `llms.txt` (header), `/security/csrf.md`, `/data/prisma.md`,
  `/application/validation.md` and `/application/configuration.md`.
- **Pass:**
  - The fixes held: it chose `APP_PIPE`, used `--incremental false`, and deleted
    the throwaway spec.
  - `enableCsrfProtection()` with no extra package. A throwaway spec confirmed
    201 / 400 / 400 / 403 cross-site / 201 same-origin.
- Typecheck errors went 1 → 1.
- Exposed finding 6 and the `tsx` seed line in the Prisma config example. Both
  were fixed.

### Run 3 — CommonJS + Jest fixture

Task: products (`POST` Zod + `GET /:id`), Prisma on SQLite, and a unit test for
the service.

- Fetched `llms.txt`, `/data/prisma.md`, `/application/validation.md` and
  `/application/configuration.md`.
- **Pass:**
  - Detected CommonJS from the missing `"type"`, and used extension-less
    relative imports.
  - `moduleFormat = "cjs"`, `APP_PIPE`, and the PrismaService in the docs' shape.
  - Ran tests through `npm test`, not bare `npx jest`.
- Typecheck errors went 0 → 0; the CommonJS baseline has no `supertest/types`
  error. The throwaway spec booted `AppModule`, made real HTTP calls (400 / 201 /
  200 / 404 / 400), and was deleted. `npm test` passed 4/4, and I re-verified
  this independently.
- The graph-compile step, not the typecheck, exposed finding 10. The agent
  fixed it within the repair budget.
- The agent also found two wording problems, both now fixed. The repair budget
  was ambiguous across typecheck and test failures, and the confined-edit rule
  omitted `main.ts`.

## Not verified

- Monorepo write paths, because there is no Nest monorepo fixture.
- Prisma 8, which is prerelease only.
- Drizzle and MikroORM content. It was checked against their docs chapters but
  not exercised.
- The Jest `ERR_REQUIRE_ASYNC_MODULE` failure below Node 24.9, because this
  machine runs Node 26.
- The Swagger CLI plugin at runtime. Only its import paths were checked.
