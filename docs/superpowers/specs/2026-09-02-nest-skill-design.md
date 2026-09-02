# Design: `nest` skill

**Date:** 2026-09-02
**Status:** Approved, revised after multi-agent review
**Repo:** `superstoffer/skills`

## Objective

Add a NestJS skill to this collection, so NestJS scaffolding help is available
in every project rather than only on the machine holding
`~/.claude/commands/nest.md`.

## Background

A NestJS assistant already exists as a personal slash command at
`~/.claude/commands/nest.md` — roughly 13 KB covering six modes, universal
rules, and a pitfalls list. Its limits: it must be typed to fire, it lives on
one machine unversioned, and it loads all 13 KB whatever the task.

Supporting research sits in
`~/.claude/projects/-Users-christoffer-Privat-cb-NestJS/memory/nestjs-skills.md`,
including v11 findings that never reached the command.

A related `nestjs-claude-plugin` MCP server in `~/.claude.json` points at
`/Users/christoffer/Privat/cb/NestJS/build/index.js`, a directory that no
longer exists. It fails to connect every session and is removed as cleanup.

**This revision follows a five-reviewer evaluation.** The findings that changed
the design are recorded inline, so the reasoning survives the decision.

## Goals

- NestJS help fires from a description of the task, without the user naming
  the skill.
- Generated code compiles **and its module graph resolves** against the
  project it was written into.
- Generated code matches the project's actual package majors — Nest, ORM,
  module system, test runner — rather than one assumed stack.
- The skill is installable from this repo like `triage` and `design-doc`.

## Non-goals

- Replacing the NestJS CLI. See "CLI relationship" below — this was previously
  stated as a non-goal and contradicted by the design; it is now settled.
- GraphQL. Excluded: it carries version-specific weight (the `@nestjs/graphql`
  release paired with Nest v12 removed `subscriptions-transport-ws` for
  `graphql-ws`, wire-incompatible) and has no stated user.
- Mongoose and Drizzle.
- Deciding *whether* to build something. That is `design-doc`'s job.

## The editorial rule

> **The rules are the product. The templates carry them.**

Four of five reviewers reached this independently. A competent model with the
project open already writes `findAll(): this.repo.find()`, `@IsEmail()` on an
email field, and the `JwtStrategy` shape. What it gets wrong is a short list of
non-obvious, mostly silent failures. Templates exist to carry a rule to the
place it applies; a template carrying no rule is filler and gets cut.

Corollary: **each rule is stated exactly once**, at the point it governs.
Restating a rule in two files guarantees they drift.

## Structure

```
skills/nest/
  SKILL.md                    <= 220 lines
  README.md                   <= 80 lines
  references/
    resource.md               <= 250   CRUD + Swagger annotation
    auth.md                   <= 200   Strategies, guards, RBAC
    testing.md                <= 200   Specs; Jest and Vitest
    pipeline.md               <= 200   Guards, interceptors, pipes, filters, decorators
    infrastructure.md         <= 250   main.ts, ConfigModule, migrations, queues
    orm.md                    <= 150   Cross-cutting: TypeORM 1.x vs Prisma 7
    version-matrix.md         <= 120   Cross-cutting: Nest v11 vs v12
```

Seven reference files exceeds this repo's precedent (`triage` has four). The
justification: `design-doc`'s references describe *document sections*, which
compress; these describe *code generation across two ORMs*, which does not.
Every file carries a size budget and a table of contents at the top, so a
partial read still shows scope.

`orm.md` and `version-matrix.md` are **cross-cutting modifiers, not modes**.
`SKILL.md` orders them directly during detection, never a mode reference
saying "also read X" — all reads stay one level deep.

### CLI relationship (settled)

The skill **writes files directly** and does not shell out to `nest g`. That
means it must itself do what `nest g` does for free: respect `nest-cli.json`
`sourceRoot` and monorepo `projects` layout, and update `app.module.ts`. Both
are specified below. The previous "the CLI still scaffolds" non-goal was
aspirational and is withdrawn.

## `SKILL.md`

### Frontmatter

`description` must fire on two distinct signals, because a technology skill is
matched **before any file is read**. Vocabulary alone cannot catch "add an
endpoint for orders" — the disambiguating fact is on disk. So the description
carries an imperative second clause telling the model to go look.

Budget: description <= 900 characters, whole frontmatter <= 1000 (cap is 1024).
Calibration: `triage` 789/876, `design-doc` 885/946.

Drafted:

```yaml
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
```

Bare `docs` is deliberately excluded as a Swagger keyword — it cross-fires
with `design-doc` in the same namespace. `api docs`, `openapi`, `swagger`,
`@Api` are kept.

`allowed-tools` is deliberately omitted: the skill needs Read/Write/Edit/Bash,
matching `design-doc`. (`triage` restricts to `mcp__linear*` precisely because
it must never write code.)

### Step 1 — Detect

Read before generating anything. **Resolved versions, not declared ranges** —
`package.json` holds `^11.0.0`, which cannot distinguish 11.0.0 from 11.2.3.
Read `node_modules/<pkg>/package.json` or the lockfile. pnpm workspaces write
`catalog:` and `workspace:*`, which carry no version at all.

**Resolve layout first, then everything else.** In Nest monorepo mode
`src/main.ts` does not exist — sources live at `apps/<name>/src/` per
`sourceRoot` and the `projects` map. Reading fixed `src/` paths before
resolving layout is the ordering bug this step exists to avoid.

| Read | Determines |
|---|---|
| `nest-cli.json` `projects` / `sourceRoot` | Monorepo layout; **all write paths for every mode** |
| Resolved `@nestjs/core` | v11 vs v12 |
| Resolved `@nestjs/config` | Standard Schema validation — **peers `^11 \|\| ^12`, so gate on this package, not core** |
| Resolved `typeorm` + `@nestjs/typeorm` | TypeORM 0.3 vs 1.x. `@nestjs/typeorm` must be >= 11.0.1 for TypeORM 1.x; its peer range spans both majors, so npm installs a broken pair silently |
| Resolved `@prisma/client`; generator `output`; `prisma.config.ts` | Prisma 6 vs 7; the import path for the generated client |
| Installed `@prisma/adapter-*` | Prisma 7 driver adapter — **refuse to guess if absent** |
| `tsconfig.json` | `experimentalDecorators`, `emitDecoratorMetadata`, `strictPropertyInitialization`, `verbatimModuleSyntax`, `paths` |
| `package.json` `type` **and** tsconfig `module`/`moduleResolution` | Emitted module format — `"type": "module"` alone does not determine it |
| `jest` / `vitest` in devDependencies | Spec idiom. **Both present: prefer the test script's runner** |
| `class-validator` / `class-transformer` | Whether DTO decorators will even compile — these are not Nest dependencies |
| `bcrypt` vs `bcryptjs` | Which to import; wrong choice is a hard failure |
| `@nestjs/swagger`, `@nestjs/jwt`, `passport` | Whether to annotate; whether auth exists |
| Lockfile name | Package manager for the verify step |

**Both ORMs present** (mid-migration): ask. Do not guess.
**No `@nestjs/core`**: say so and stop. Never scaffold Nest into an Express
project; never offer to install NestJS unless asked.

Then, before routing: if `@nestjs/core` is v12+, read `version-matrix.md`. If
an ORM is detected, read `orm.md`.

### Step 2 — Route

**The routing table is a lookup, not a switch.** Modes compose: "add a
JWT-protected orders resource with Swagger and tests" is four of them. Select
*every* mode the request touches.

| User mentions | Mode | Read |
|---|---|---|
| resource, entity, CRUD, controller, endpoint | Resource | `resource.md` |
| auth, login, JWT, passport, register, token | Auth | `auth.md` |
| test, spec, unit test, e2e | Testing | `testing.md` |
| swagger, openapi, api docs, `@Api` | Swagger | `resource.md` |
| guard, interceptor, custom decorator, filter, middleware | Pipeline | `pipeline.md` |
| setup, bootstrap, main.ts, config, env, migration, DataSource | Infrastructure | `infrastructure.md` |
| queue, job, worker, BullMQ, background | Queues | `infrastructure.md` |

Execute in dependency order: **Infrastructure -> Resource -> Auth -> Pipeline
-> Queues -> Swagger -> Testing.** Swagger annotates code that must already
exist; tests test code that must already exist.

Generic verbs (`generate`, `scaffold`, `add`) select the *skill*, never a mode
— they are excluded from the table.

**No match:** answer directly from the rules and the detected versions. Do not
force a scaffold. This covers "why is my guard returning 403", "fix this DI
error", "review this controller", "upgrade us to v12" — all of which the
description will fire on. For the last, recommend `nest upgrade --dry-run`,
which mechanically applies most of the v11->v12 migration.

`SKILL.md` carries 4-5 worked request -> mode-set examples covering the
collisions above.

### Step 3 — Write and verify

**Writing.** Files land at the resolved layout path, never a hardcoded `src/`.
The skill makes the `app.module.ts` registration edit **itself** — with a
verify step in play, telling the user to add the import is a trap: typecheck
passes, report says success, module unregistered at runtime.

**Verifying.** Two reviewers with opposing briefs specified this
independently; it is the design's load-bearing procedure.

1. **Baseline.** Run the typecheck *before* writing. Record the error set.
   Real repos have pre-existing errors; without a baseline the skill either
   reports failure on good output or "repairs" files the user never mentioned.
2. **Write**, then re-run. **Only errors absent from the baseline are in
   scope.**
3. **Compile the module graph.** `tsc` cannot catch the most common scaffold
   failure: Nest resolves DI at runtime, so a module missing from `imports`, a
   provider missing from `exports`, or a circular dependency needing
   `forwardRef` all typecheck clean and throw on boot. Run
   `Test.createTestingModule({ imports: [AppModule] }).compile()`. If it
   cannot run, say so.
4. **Repair, bounded.** Maximum two attempts. Stop if the new-error count does
   not strictly decrease. Edits are confined to files this invocation wrote
   plus the announced `app.module.ts` edit. Never revert the user's existing
   code to silence an error.
5. **Report, fixed shape.** Files written; command run; error count before and
   after; what remains. Say "compiles" and "module graph resolves" — never
   "works". If specs were generated but not run, say they were not run and do
   not claim they pass.

Typecheck lookup order: `package.json` scripts `typecheck` -> `type-check` ->
`npx tsc --noEmit -p <resolved tsconfig>`. **`build` is excluded** — `nest
build` writes `dist/` and in many repos triggers codegen, containers, or DB
access. The one legitimate pre-step is `prisma generate`, without which every
generated-client import is unresolved for reasons unrelated to this skill.

Never run `npm install`. If `node_modules` is absent, report and stop.

### Hard rules

Split by consequence. (Existing skills use the heading `## Hard rules`; this
design previously invented "Universal rules" and the earlier justification —
"they apply to every mode" — was false. Almost none do. The real reason to
keep any in the body is **cost asymmetry**: a one-line fact costs ~10 tokens;
missing `synchronize: true` costs a production table.)

**In `SKILL.md`, as prohibitions — security and data loss:**

1. `synchronize` is never `true` outside development. Drive it from config,
   never a literal; always `false` in the migration DataSource. Warn only when
   hardcoded `true` or not environment-gated. (Previously "never `synchronize:
   true`", which nags on correctly-configured dev projects.)
2. Passwords compare with `bcrypt.compare()`, never `===`. Import the package
   the project actually has — `bcrypt` and `bcryptjs` are not interchangeable.
3. Never return `password`, and never place it in a JWT payload. **State the
   mechanism**, not the goal: `@Exclude()` plus a global
   `ClassSerializerInterceptor`, TypeORM `@Column({ select: false })` with
   `addSelect` at login, or an explicit Prisma `select`/`omit`. Note
   `ClassSerializerInterceptor` does nothing when the handler returns a plain
   object rather than a class instance — a silent leak.
4. JWT secrets come from `ConfigService`, never a literal.
5. Every required env var appears in the `ConfigModule` validation schema.
   **`getOrThrow` throws at call time, not startup** — a key read inside a
   handler boots green and dies on first traffic. Validation is the startup
   gate; `getOrThrow` is only the accessor. Better still,
   `ConfigService<Config, true>` makes `get<T>()` return `T`, removing the `!`.

**In the reference file, adjacent to the template each governs:**

- `APP_*` providers over `app.useGlobal*()` for anything needing DI — and the
  two stronger reasons than DI: `useGlobal*()` bindings do **not** apply to
  `Test.createTestingModule`, so e2e tests silently run without the global
  `ValidationPipe`; and `useGlobalFilters()` does not cover gateways or hybrid
  apps. But `app.useGlobalPipes(new ValidationPipe())`, `setGlobalPrefix`,
  `enableCors`, `enableVersioning` are legitimate and must not be rewritten.
  Registering both ways runs the pipe **twice**.
- `PartialType` from `@nestjs/swagger` when Swagger is present — **because**
  the `@nestjs/mapped-types` version does not re-apply `ApiProperty`, so the
  update DTO renders as an empty Swagger schema, silently. Same for `PickType`,
  `OmitType`, `IntersectionType`.
- `Reflector.getAllAndOverride([handler, class])`, in that order — **the
  failure is privilege escalation**, not "broken role arrays": with
  `getAllAndMerge`, a class marked `@Roles('admin')` and a method marked
  `@Roles('user')` yields both, so a method meant to narrow access widens it.
  Reversing the array lets class metadata override the method. On v12 the CLI
  emits `Reflector.createDecorator()`; mixing that with `SetMetadata` string
  keys returns `undefined`.
- `autoLoadEntities: true` **only inside Nest**. It misses entities reachable
  only through relations, and it does not exist for the TypeORM CLI — the
  migration DataSource must list entities explicitly. The glob form breaks
  under ESM (`__dirname` unavailable).
- DTOs are classes, imported as values. `import type` erases the class and
  `ValidationPipe` then validates nothing, silently — most likely on
  v12/ESM projects with `verbatimModuleSyntax`.
- `ValidationPipe({ whitelist: true })` **silently strips** any property
  lacking a validation decorator. `transform: true` is what makes
  `@Param('id') id: number` actually a number.
- Repository mocks use `getRepositoryToken(Entity)` as the provider token, not
  the `Repository` class — the most common reason a generated spec fails to
  compile its testing module.
- `@Get(':id')` shadows `@Get('search')` when declared first. On v12,
  `routeConflictPolicy` and `routeResolutionStrategy: 'specificity'` exist for
  exactly this.
- `forwardRef()` on both sides of a circular module dependency — the shape
  `AuthModule` <-> `UsersModule` takes by default.
- e2e specs `await app.close()` in `afterAll`, or the runner hangs.
- `ParseUUIDPipe` for UUID keys; `ParseIntPipe` for integer keys. Route params
  are strings either way.
- Prefer `@UseFilters(FilterClass)` over an instance, for DI and reuse —
  a preference, not a prohibition; instances are legitimate when the filter
  takes constructor arguments.
- Guards: throw `UnauthorizedException` for 401 rather than `return false`,
  which yields 403.
- Middleware calls `next()` or sends a response.
- Never emit `should be defined` as a spec's only test.

### ESM

Not a stylistic axis — generated ESM code that ignores these does not run:
relative imports carry a `.js` extension even from `.ts`; `__dirname` and
`__filename` do not exist (`import.meta.dirname`); `require()` is unavailable
(`createRequire(import.meta.url)`).

### ORM handling (`orm.md`)

Targets current stable: **TypeORM 1.x** (`latest` 1.1.1) and **Prisma 7.x**
(`@prisma/client` `latest` 7.10.0). Both majors are detected, so older
projects still generate correctly and Prisma 8 drops in when it stabilises —
its CLI is at `8.0.0-rc.12` with no matching stable client.

The ORM choice is not one table in one file. It forks Resource, Testing,
Auth (user lookup), and Infrastructure (bootstrap and migrations), which is
why it is single-sourced here.

| Concern | TypeORM 1.x | Prisma 7.x |
|---|---|---|
| Definition | `*.entity.ts` decorators | `schema.prisma`; no entity file, but generated **types** are imported |
| Client | — | Not from `@prisma/client`; from the generator's `output` path, which must be somewhere `tsc` compiles |
| Service | `@InjectRepository(E) repo: Repository<E>` | `PrismaService extends PrismaClient` with a **mandatory driver adapter in the constructor** — `new PrismaClient()` with no adapter throws during DI resolution. `onModuleInit`/`$connect()` is the Prisma 6 form and no longer the official recipe |
| Read one | `repo.findOneBy({ id })` | `findUnique` accepts **only `@id`/`@unique`** fields — `findFirst` is the general analogue. `findUniqueOrThrow` throws `PrismaClientKnownRequestError` (P2025), not `NotFoundException` |
| Module | `TypeOrmModule.forFeature([E])`, **re-exported** if another module injects it | `PrismaModule` provides **and exports** `PrismaService`; feature modules import it. Providing without exporting is the most common DI failure |
| DTOs | Entity decorators | Prisma model types are **not classes** — they cannot be `@Body()` DTOs. Hand-written class DTOs are still required |
| Spec mock | `getRepositoryToken(E)` | Nested delegate object under `PrismaService` |
| Migrations | `migration:generate` + standalone DataSource | `prisma migrate dev` |

TypeORM 1.x specifics that break inherited templates: `relations: ['profile']`
and string-array `select` are removed (`{ profile: true }`); `undefined` in
`where` now throws; `findByIds`, `findOneById`, `@EntityRepository`,
`getCustomRepository` are gone; `@Column({ readonly })` is `{ update: false }`;
`nullable: false` relations emit INNER JOIN.

### Version handling (`version-matrix.md`)

**No major is named as the default in prose** — `SKILL.md` says only "output
matches the detected version". v12 is days old and v11 is still shipping; in a
year the roles invert and prose stating a default would need rewriting.

The previous claim that "v11 idioms run unchanged on v12 thanks to
`require(esm)`" was **wrong and load-bearing**. `require(esm)` covers package
consumption: a CommonJS app can upgrade and stay CommonJS. v11 output is
source-compatible on v12 for **controllers, services and DTOs specifically**;
Config, custom pipes, logging assertions, and CLI config diverge regardless.

| Area | v12 |
|---|---|
| Validation | Standard Schema via `schema` on `@Body()`/`@Query()`/`@Param()`/`@RawBody()`, alongside class-validator. **Requires `StandardSchemaValidationPipe` registered — without it the decorator attaches metadata and validates nothing.** Response side: `StandardSchemaSerializerInterceptor` + `@SerializeOptions({ schema })` |
| `@nestjs/config` | Standard Schema; Joi >= 18 with settings under `validationOptions.libraryOptions`. Gate on the **config** major (it jumped 4.0.4 -> 12.0.0 and peers `^11 \|\| ^12`) |
| Pipes | `ArgumentMetadata` is generic |
| Lifecycle | Hooks invoked by component hierarchy level |
| Exceptions | `HttpExceptionOptions.errorCode` |
| Logging | Structured params default-on; `structuredParams: false` restores |
| Routing | `routeConflictPolicy`, `routeResolutionStrategy: 'specificity'` |
| Decorators | `Reflector.createDecorator()` preferred over `SetMetadata` |
| Generated projects | **oxlint for all** generated projects, not just ESM. Vitest only for ESM; CommonJS keeps Jest |
| Swagger | CLI plugin is a `tsc` transformer — **does not run under Vitest/SWC**, the v12 ESM default. Requires `PluginMetadataGenerator` + `SwaggerModule.loadPluginMetadata()`, or DTOs document as empty schemas |
| Monorepo | Rspack is the default bundler; `webpack` options in `nest-cli.json` are deprecated |
| Node | v20.19+/v22.12+ to run; **v22.22.3+/v24.15+/v26+ for the CLI**. `engines` says `>= 20` and understates both |
| Ecosystem | Every `@nestjs/*` moves major together; `@nestjs/graphql` went to 14 |

Absolute dates and version numbers stay in this spec. They must not reach
`SKILL.md`, where they rot.

## Testing

**RED phase first — non-negotiable.** Run 5-6 representative prompts against a
real NestJS project with **no skill loaded** and record verbatim what plain
Claude gets wrong. Prune the rules to what actually failed. A rule that plain
Claude already follows is dead weight in every invocation.

Triggering and behaviour are separate tests:

1. **Trigger.** Must fire on no-vocabulary prompts ("add an endpoint for
   orders", "users need to log in") inside a Nest project. Must not fire on
   "add a guard to this Express route" or "write a DTO" in a plain TS project.
2. **Behaviour.** Resource, Auth, and Testing modes against a real project on
   each detected ORM, confirming typecheck *and* module-graph compile.
3. **Consistency.** Each rule appears exactly once. Single-sourcing makes this
   near-automatic rather than a manual audit.

## Repo wiring

`marketplace.json` and `plugin.json` are edited in lockstep — git history
(`d273b14`) shows character-identical description and version edits when
`design-doc` was added. Version 1.1.0 -> 1.2.0 matches one minor bump per skill.

Note a pre-existing asymmetry: `plugin.json` carries a `productivity` keyword
`marketplace.json` lacks. **Preserve it** rather than silently normalising.

New keywords for both: `nest`, `nestjs`, `typeorm`, `prisma`.
Description clause, appended to the existing sentence in both files:
`"; nest scaffolds NestJS resources, auth, and tests against your project's own stack."`

`README.md` gains a `nest` row. `skills/nest/README.md` reproduces the house
install block verbatim and adds the CLAUDE.md snippet below.

### CLAUDE.md trigger snippet

A technology skill's description is matched before any file is read, so
description-based triggering is best-effort. `README.md` offers a line users
can paste into their NestJS project's `CLAUDE.md` as a reliable trigger.

## Cleanup

- Remove the dead `nestjs-claude-plugin` entry from `~/.claude.json`.
  Independent of this work; safe now.
- **Keep `~/.claude/commands/nest.md` until the skill passes its trigger
  tests.** Deleting a working artifact in the same change that ships its
  replacement leaves no fallback.

## Open issues

1. **Prisma 8 timing.** Its CLI is at `8.0.0-rc.12` with `@prisma/client`
   stable at 7.10.0. If 8 ships before the Prisma templates are written, they
   should target 8 instead. Next step: re-check dist-tags at implementation.
2. **Which rules survive RED.** The list above is the candidate set, not the
   final one. It cannot be settled before the baseline runs.
3. **Monorepo write paths are specified but untested.** Detection resolves
   `sourceRoot` and `projects`; no monorepo fixture exists to verify against.
   Next step: test against one Nest monorepo before release, or state the
   limitation in `README.md`.
4. **e2e/Vitest `supertest` imports.** The migration guide notes default-import
   changes under Vitest. Unverified. Next step: confirm when writing
   `testing.md`.
