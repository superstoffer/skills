# Design: `nest` skill

**Date:** 2026-09-02
**Status:** Approved
**Repo:** `superstoffer/skills`

## Objective

Add a NestJS skill to this collection, so that NestJS scaffolding help is
available in every project rather than only on the machine holding
`~/.claude/commands/nest.md`.

## Background

A NestJS assistant already exists as a personal slash command at
`~/.claude/commands/nest.md` — roughly 13 KB covering six modes, a set of
universal rules, and a pitfalls list. It works, but it has three limits:

1. It is a slash command, so it never fires on its own. It must be typed.
2. It lives on one machine and is not versioned.
3. It is one flat file. Every invocation loads all 13 KB, whatever the task.

Supporting research sits in
`~/.claude/projects/-Users-christoffer-Privat-cb-NestJS/memory/nestjs-skills.md`,
including NestJS v11 findings that never reached the command.

A related `nestjs-claude-plugin` MCP server is configured in `~/.claude.json`
pointing at `/Users/christoffer/Privat/cb/NestJS/build/index.js`. That
directory no longer exists, so the server fails to connect. It is dead
configuration and gets removed as cleanup.

## Goals

- NestJS help fires automatically from a description of the task, without
  the user remembering a command name.
- Generated code compiles against the project it was written into.
- Generated code matches the project's actual NestJS major, ORM, module
  system, and test runner rather than a single assumed stack.
- The skill is installable from this repo like `triage` and `design-doc`.

## Non-goals

- Replacing the NestJS CLI. `nest g` still scaffolds; this skill fills in
  what the CLI leaves empty.
- GraphQL. Considered and excluded — it carries its own version-specific
  weight in v12 (`subscriptions-transport-ws` removed in favour of
  `graphql-ws`) and can be added later as its own mode.
- Mongoose and Drizzle. TypeORM and Prisma only.
- Deciding *whether* to build something. That is `design-doc`'s job.

## Design

### Structure

One skill folder, following the convention already set by `triage` and
`design-doc`: a `SKILL.md` that loads on every invocation, with bulk pushed
into `references/` that load only when a mode needs them.

```
skills/nest/
  SKILL.md                      ~180 lines
  README.md                     ~70 lines
  references/
    resource.md                 CRUD scaffold: TypeORM and Prisma
    auth.md                     JWT/local strategies, guards, RBAC
    testing.md                  Service/controller/e2e specs, Jest and Vitest
    swagger.md                  OpenAPI annotation of existing code
    pipeline.md                 Guards, interceptors, pipes, filters, decorators
    infrastructure.md           main.ts, ConfigModule, migrations
    queues.md                   BullMQ processors and registration
    version-matrix.md           v11 vs v12 deltas
```

The universal rules stay in `SKILL.md` rather than a reference file. They
apply to every mode and must not depend on a file read, mirroring how
`design-doc` keeps its hard rules on the front page.

### `SKILL.md` contents

**Frontmatter.** A `description` long enough to trigger reliably, listing
the vocabulary of each mode and carrying an explicit exclusion clause, as
both existing skills do. Excludes general TypeScript/Express work and
excludes build-or-not decisions, pointing those at `design-doc`.

**Step 1 — Detect project context.** Silently read, before generating
anything:

| Read | Determines |
|---|---|
| `@nestjs/core` version in `package.json` | v11 vs v12 code paths |
| `"type": "module"` in `package.json` | ESM vs CommonJS output |
| `jest` / `vitest` in devDependencies | Which mocking idiom specs use |
| `@prisma/client` + `prisma/schema.prisma` | Prisma path vs TypeORM path |
| `@nestjs/swagger`, `@nestjs/jwt`, `passport` | Whether to annotate, whether auth exists |
| `nest-cli.json` | Monorepo mode, Swagger CLI plugin |
| `src/main.ts` | Global prefix, ValidationPipe, CORS, platform |
| `src/app.module.ts` | Existing modules, TypeOrmModule, ConfigModule |

Detection replaces asking. The skill only asks about what it cannot read.

**Step 2 — Route by intent.** Nine modes, inferred from the request, never
selected by the user:

| User mentions | Mode |
|---|---|
| resource, entity, CRUD, generate, scaffold, module | Resource Scaffold |
| auth, login, JWT, passport, register, token, session | Auth Scaffold |
| test, spec, unit test, e2e, coverage | Test Generator |
| swagger, openapi, docs, api docs, `@Api` | Swagger Annotator |
| guard, interceptor, pipe, filter, middleware, decorator | Pipeline Building Block |
| setup, bootstrap, `main.ts`, global prefix, CORS, validation | Project Setup |
| config, env, ConfigModule, environment variable, secrets | Config & Env |
| migration, migrate, schema change, DataSource | Migrations |
| queue, job, worker, BullMQ, background, cron | Queues |

**Step 3 — Write and verify.** The skill writes files to disk, then runs the
project's own typecheck command and repairs what it broke before reporting.
If no working toolchain exists, it says so rather than implying success.

**Universal rules.** The existing set from the command, plus the items from
the research memory that never reached it:

- Global guards/interceptors/pipes/filters that need DI use `APP_*`
  providers, never `app.useGlobal*()`.
- Never `synchronize: true`; warn explicitly when detected.
- `bcrypt.compare()` for passwords, never `===`.
- Never return a `password` field or place it in a JWT payload.
- `PartialType` from `@nestjs/swagger` when Swagger is present, otherwise
  `@nestjs/mapped-types`.
- `config.getOrThrow<T>('KEY')` over `config.get<T>('KEY')!` — a missing env
  var should fail loudly at startup.
- `autoLoadEntities: true` rather than listing entities manually.
- `Reflector.getAllAndOverride` vs `getAllAndMerge` — the wrong choice
  silently breaks role arrays.
- Route params are strings; use `ParseIntPipe` where a number is expected.
- Middleware must call `next()` or send a response.
- `canActivate` returning `false` yields 403; throw `UnauthorizedException`
  for 401.
- `@UseFilters(FilterClass)`, not `@UseFilters(new FilterClass())`.

### Version handling

The skill targets no single NestJS major. It detects one.

v11 remains actively maintained (11.2.3 shipped 2026-08-25) and v12.0.0 is
six days old at time of writing (2026-08-27, with 12.0.1 as `latest`).
Almost every existing codebase is on v11.

Default output uses v11 idioms, which run unchanged on v12 thanks to
`require(esm)`. `references/version-matrix.md` loads only when v12 is
detected, and covers:

| Area | v12 change |
|---|---|
| Validation | Standard Schema via a `schema` option on `@Body()`/`@Query()`/`@Param()`, offered alongside class-validator, not replacing it |
| `@nestjs/config` | `validationSchema` goes through Standard Schema; Joi needs v18+ with settings under `validationOptions.libraryOptions` |
| Custom pipes | `ArgumentMetadata` is now generic |
| Lifecycle hooks | Invoked by component hierarchy level |
| Exceptions | `HttpExceptionOptions` accepts `errorCode` |
| Logging | Structured params on by default; `structuredParams: false` restores prior behaviour |
| New ESM projects | Default to Vitest and oxlint rather than Jest and eslint |
| Node | Requires v20.19+ or v22.12+ |

The Test Generator is the mode most exposed to this: it must emit Vitest
mocks on a v12 ESM project and Jest mocks otherwise. Detection reads
devDependencies rather than inferring from the major.

### Prisma as a first-class path

The current command prompts for Prisma but has no templates behind it.
`references/resource.md` documents both ORMs side by side. Prisma differs
from TypeORM in five places downstream of the ORM choice:

| Concern | TypeORM | Prisma |
|---|---|---|
| Entity definition | `*.entity.ts` with decorators | `prisma/schema.prisma` is the source of truth; no entity file |
| Injection | `@InjectRepository(Entity) repo: Repository<Entity>` | `private prisma: PrismaService` |
| Read one | `repo.findOneBy({ id })` | `prisma.user.findUnique({ where: { id } })` |
| Module wiring | `TypeOrmModule.forFeature([Entity])` | Module provides `PrismaService` |
| Spec mock | Mocked `Repository<T>` | Mocked nested delegate object |

A `PrismaService` with `onModuleInit` calling `$connect()` is generated when
the project has `@prisma/client` but no such service yet.

### Repo wiring

- `.claude-plugin/marketplace.json` — add `nest` to the plugin description
  and `keywords`; bump `version` 1.1.0 → 1.2.0.
- `.claude-plugin/plugin.json` — same description and keywords; same bump.
- `README.md` — add a `nest` row to the skills table.

### Cleanup

Once the skill is in place and installable:

- Delete `~/.claude/commands/nest.md`, superseded by the skill.
- Remove the `nestjs-claude-plugin` entry from `~/.claude.json`; it points
  at a deleted directory and fails to connect every session.

Both are outside the repo and are done last, after the skill is verified.

## Testing

The skill produces code rather than being code, so verification is
behavioural:

1. Each reference file's templates must be internally consistent with the
   universal rules in `SKILL.md` — no template may contradict a rule.
2. Cross-check every claim about v12 against the release notes rather than
   from memory.
3. Exercise the skill against a real NestJS project for at least the
   Resource Scaffold mode on both ORM paths, confirming the generated code
   typechecks.

## Open issues

None. GraphQL, Mongoose, and Drizzle are deliberate exclusions, not
unresolved questions.
