---
name: nest
description: >-
  Write or change NestJS server-side code. Use when the request names NestJS
  or its vocabulary: module, controller, provider, service, DTO, entity,
  guard, interceptor, pipe, exception filter, custom decorator, APP_GUARD,
  main.ts, app.module.ts, nest g, any @nestjs/* package, TypeORM or Prisma
  inside Nest, Passport/JWT auth, Swagger annotation, BullMQ queues,
  ConfigModule, migrations, or Jest/Vitest specs for those. ALSO use when
  the project is NestJS — @nestjs/core in package.json, nest-cli.json, or
  src/app.module.ts — and the user asks to add an endpoint, a resource,
  CRUD, login, background jobs, or tests WITHOUT naming NestJS; check for
  that evidence before concluding this does not apply. NOT for TypeScript,
  Express, Fastify, or Node work outside a NestJS project.
---

# Nest

Supply what reading the project cannot tell you — which package majors it is
actually on — then verify that what you wrote compiles and resolves.

## What this skill does not do

It does not teach NestJS idiom. Given a project it can read, Claude already
gets the conventions right: DTOs as classes with validators on every property,
`PartialType` from `@nestjs/swagger`, `ParseUUIDPipe` for uuid keys,
`getRepositoryToken` in spec providers, new modules registered in `AppModule`,
`synchronize: false` preserved, passwords kept out of JWT payloads. Restating
any of that would cost context on every invocation and change nothing.

Two things reading the project cannot supply, and this skill does:

1. **Framework and ORM releases published after the training cutoff.** The
   failure is worst where confidence is highest — TypeORM 1.x removed APIs
   that a model will insist still exist.
2. **Verification.** A Nest module graph resolves at runtime, so a missing
   `imports` entry typechecks clean and throws on boot.

## Hard rules

1. **No `@nestjs/core` in the project: say so and stop.** Never scaffold Nest
   code into an Express or plain-TypeScript project. Never offer to install
   NestJS unless asked.
2. **Every required env var belongs in the `ConfigModule` validation schema.**
   `getOrThrow` throws at call time, not startup — a key read inside a request
   handler boots green and dies on first traffic. Validation is the startup
   gate; `getOrThrow` is only the accessor. `ConfigService<Config, true>` makes
   `get<T>()` return `T`, removing the need for `!`.

## Step 1 — Detect

**Read resolved versions, not declared ranges.** `package.json` holds
`^11.0.0`, which cannot distinguish 11.0.0 from 11.2.3 — and that distinction
decides real behaviour. Read `node_modules/<pkg>/package.json`, or the
lockfile. pnpm workspaces write `catalog:` and `workspace:*`, which carry no
version at all.

**Resolve layout before reading any source path.** In Nest monorepo mode
`src/main.ts` does not exist; sources live at `apps/<name>/src/` per
`sourceRoot` and the `projects` map in `nest-cli.json`. Every path you write
to depends on this.

| Read | Determines |
|---|---|
| `nest-cli.json` `projects` / `sourceRoot` | Monorepo layout; every write path |
| Resolved `@nestjs/core` | Whether `references/version-matrix.md` is needed |
| Resolved `@nestjs/config` | Its major moves independently of core and its peer range spans two core majors — gate config behaviour on this package, never on core |
| Resolved `typeorm` + `@nestjs/typeorm` | Which TypeORM major, and whether the pair is compatible |
| Resolved `@prisma/client`; the generator block; `prisma.config.ts` | Which Prisma major, and the generated client's import path |
| Installed `@prisma/adapter-*` | Required from Prisma 7 on — if none is installed, stop and ask rather than guessing one |
| `package.json` `type` **and** tsconfig `module`/`moduleResolution` | Emitted module format. `"type": "module"` alone does not determine it |
| `jest` / `vitest` in devDependencies | Spec idiom. If both are present, follow the test script |
| Lockfile name | Package manager, for the verify step |

**Both ORMs present** (a project mid-migration): ask which to use. Do not guess.

## Step 2 — Load what you cannot know

Before writing anything:

- `@nestjs/core` is v12 or later → read `references/version-matrix.md`.
- An ORM is present → read `references/orm.md`.

Neither file repeats general NestJS idiom. They carry only version deltas, so
reading them is cheap and skipping them produces confidently wrong code.

## Step 3 — Write and verify

Write files at the resolved layout path, never a hardcoded `src/`. Make the
`app.module.ts` registration edit yourself — leaving it to the user means the
typecheck passes, the report says success, and the module is unregistered at
runtime.

Then verify, in this order:

1. **Baseline first.** Run the typecheck *before* writing and record the error
   set. Real projects carry pre-existing errors; without a baseline you cannot
   tell yours from theirs, and will either report failure on good output or
   start editing files nobody mentioned.
2. **Re-run after writing.** Only errors absent from the baseline are yours.
3. **Compile the module graph.** `tsc` cannot see a missing `imports` entry, a
   provider missing from `exports`, or a cycle needing `forwardRef` — all of
   them typecheck clean and throw on boot. Run
   `Test.createTestingModule({ imports: [AppModule] }).compile()`. If it cannot
   run, say so rather than implying it passed.
4. **Repair at most twice.** Stop if the new-error count does not strictly
   decrease. Confine edits to files you wrote plus the `app.module.ts` edit you
   announced. Never revert the user's existing code to silence an error.
5. **Report a fixed shape:** files written; command run; error count before and
   after; what remains. Say "compiles" and "module graph resolves" — never
   "works". If you generated specs and did not run them, say so and do not
   claim they pass.

**Typecheck lookup order:** `package.json` scripts `typecheck` → `type-check`
→ `npx tsc --noEmit -p <resolved tsconfig>`.

**Exclude `build`.** `nest build` writes `dist/` and in many projects triggers
codegen, containers, or database access. The one legitimate pre-step is
`prisma generate`, without which every generated-client import is unresolved
for reasons unrelated to what you wrote.

**Never run `npm install`.** If `node_modules` is absent, report and stop.

## Reference files

- `references/version-matrix.md` — NestJS v11 → v12 deltas. Read during
  detection when the project is on v12 or later.
- `references/orm.md` — TypeORM and Prisma major-version deltas. Read during
  detection when an ORM is present.
