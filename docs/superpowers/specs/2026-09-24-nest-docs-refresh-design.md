# Design: `nest` skill refresh against docs.nestjs.com (v12.1)

**Date:** 2026-09-24
**Status:** Approved
**Supersedes:** nothing — amends [2026-09-02-nest-skill-design.md](2026-09-02-nest-skill-design.md)

## Why

The skill's v12 and Prisma content was written from release notes and type
declarations, and its README flagged that content as the part most likely to be
wrong. docs.nestjs.com now documents v12.1 (`@nestjs/common` 12.1.0) and
publishes `llms.txt` plus every chapter as raw markdown at `<path>.md`. An audit
against both found the content wrong in places, incomplete, and already stale:
v12.1 shipped features after the skill was written.

## Decisions

1. **Delete `~/.claude/skills/nest`.** It was an older copy of `skills/nest/`
   and loaded alongside the plugin's `superstoffer:nest`, competing on the same
   description.
2. **Delta scope only.** The 2026-09-02 rescope still holds: no general NestJS
   idiom. Only facts the model cannot have, plus verification.
3. **Hybrid live docs.** The static references keep two kinds of content:
   traps the model would never think to look up (silent failures,
   confidently-wrong recall), and a `→ /chapter.md` pointer for each. Anything
   else from the v12 era is fetched from the chapter at runtime, with `llms.txt`
   as the index. `llms-full.txt` (1.6 MB) is never fetched. Without network
   access the skill falls back to its static references and says so.
4. **Drizzle and MikroORM are detected and routed.** The earlier non-goal on
   Drizzle is lifted because `@nestjs/drizzle` is now official. Each ORM gets
   only a few trap lines plus its chapter pointer.
5. **Gate v12.1 features on `@nestjs/common` minor**, the package that exports
   them. This extends the existing rule of gating config behaviour on
   `@nestjs/config`.
6. **Verify on a real v12 fixture.** This closes the "not verified against a
   real project" gap.

## Audit findings

The sources were three per-page subagent audits, backed by the raw
`nestjs/docs.nestjs.com` markdown, and a grep over `llms-full.txt`.

### Wrong — generated incorrect code

| Claim | Docs say | Chapter |
|---|---|---|
| Prisma 7 PrismaService: adapter only, "no lifecycle hook" | Keep `onModuleInit` → `$connect()` (fail at boot) and `onModuleDestroy` → `$disconnect()` (ends adapter pool) | /data/prisma |
| `moduleFormat = "cjs"` always | Only for CommonJS projects; ESM (new default) needs nothing; pre-7.10 + `nodenext` must set it explicitly | /data/prisma |
| `prisma.config.ts` | `prisma7.config.ts` on 7.10+; old name still recognised | /data/prisma |
| `ReadonlyVisitor` from `@nestjs/swagger/dist/plugin` | `@nestjs/swagger/plugin`; generator path carries `.js` | /recipes/swc |
| "adding `type: module` is the whole switch" | Only for projects from `@nestjs/schematics` ≥ 11.0.6 | /migration-guide |

### Imprecise

- "`nest upgrade` bumps Joi to 18" does not appear in the docs. What the docs do list: TS 6, Jest 30,
  `engines.node`, tsconfig checks, and the local dev-dependency CLI update.
- The `@nestjs/config` peer range is on `@nestjs/common`, not core.
- `esmCompatible` is auto-detected per file, not required.
- "Prefer `createDecorator`" is not stated in the docs. Their only claim is that the schematic emits it.
- Early 22.x is also excluded from the CLI floor.
- The lifecycle order has a documented rule: modules run by distance from the root, and shutdown
  runs in reverse.
- The supertest default import applies only if the Vitest setup expects one.

### Missing — changes generated code

- **Validation and serialisation:**
  - `validateCustomDecorators` (a second silent no-validation trap)
  - `@Headers()` takes no schema
  - there is no `whitelist`
  - serializer: item schema for arrays, 500 on mismatch, `Reflector` for global registration
  - `errorFormat: 'grouped'`
  - `errorCode` is dropped with object bodies
- **DI and runtime:**
  - `@Optional()` is not inherited
  - Terminus `HealthIndicator` was removed
  - `RouteConflictException`
  - Jest needs Node ≥ 24.9 for v12
  - AWS Lambda needs `NODE_OPTIONS`
- **v12.1:** `useSecurityHeaders()`, `enableCsrfProtection()`, `@Cookies()` / `setCookie()`, and
  Fastify uploads.
- **Ecosystem:**
  - BullMQ `repeat` → `upsertJobScheduler()`
  - `@nestjs/drizzle` (Drizzle v1 `rc`)
  - MikroORM v7 imports
  - Prisma: MongoDB stays on 6, Accelerate, `PrismaMssql`, the Prisma 8 CLI lacks
    `migrate`/`generate`
  - `autoLoadEntities` skips relation-only entities
- **Verify step:** `compile()` creates no HTTP adapter.

### Deliberately excluded

These don't change generated code, or the live docs cover them: `nest deploy`,
`includeLibraryAssets`, the new build flags, Express graceful drain,
gRPC/Kafka/WebSocket additions, and GraphQL v14 (still a non-goal).

## Budget

SKILL.md ≈ 160 lines (fixture-proven verify-step facts pushed it past the ~150 target); version-matrix.md ≤ ~170; orm.md ≈ 210 (four ORMs, loaded only when one is present); no new files.

## Verification

This is a real `nest new` fixture on Node 26.8.1, ESM + Vitest by default. A
subagent reads the skill from the worktree and builds a users resource with:
- Zod validation
- a header-derived tenant id
- a Prisma 7 service
- security headers
- a preference cookie

**Pass criteria:**
- the correct pipes are registered
- the PrismaService matches the docs' shape
- the built-ins are used instead of helmet and cookie-parser
- at least one chapter was fetched
- the typecheck shows no new errors
- the module graph compiles

Results go in `docs/superpowers/plans/2026-09-24-nest-docs-refresh-results.md`.
