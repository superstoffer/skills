# ORM version facts

Contents: TypeORM detection & 0.3→1.x breaking changes · Prisma detection & 6→7 changes · PrismaService shape · adapter selection · Drizzle (`@nestjs/drizzle`) · MikroORM v7.

Your training is unreliable here. Two beliefs you may hold with high confidence are **false**: TypeORM
shipped a **1.x major**, and the string-array `relations: ['profile']` form **was removed** in it.
Do not trust recall below. Detect, then generate. Each `→ /path.md` names the
docs.nestjs.com chapter to fetch for anything beyond the trap stated here.

## TypeORM

### Detect the installed major first

Read the **resolved** version, never the range in `package.json`:

```bash
node -p "['typeorm','@nestjs/typeorm'].map(m=>m+' '+require('./node_modules/'+m+'/package.json').version)"
```

Both majors are live: `typeorm@latest` resolves to the 1.x line, `typeorm@legacy` pins 0.3 (0.3.31).

**The mismatch trap.** `@nestjs/typeorm`'s peer range is `^0.3.0 || ^1.0.0-dev` — it spans both
majors, so npm resolves a mismatched pair silently, with no peer warning. Check both packages.

- **TypeORM 1.x requires `@nestjs/typeorm` >= 11.0.1.** 11.0.0 and every 10.x declare `^0.3.0` only.
  If the project pairs TypeORM 1.x with `@nestjs/typeorm` <= 11.0.0, say so before writing code.
- TypeORM 1.x declares `engines.node` as `^20.19.0 || ^22.13.0 || >=24.11.0` — narrower
  than "Node 20+". The 21.x and 23.x lines, and early 24.x, are excluded.

### 0.3 → 1.x changes that land on generated CRUD

| 0.3 | 1.x |
|---|---|
| `relations: ['profile', 'posts']` | `relations: { profile: true, posts: true }` |
| `select: ['id', 'name']` | `select: { id: true, name: true }` |
| `join: { ... }` | `relations` object, or QueryBuilder |
| `findOneById(id)` | `findOneBy({ id })` |
| `findByIds([1, 2])` | `findBy({ id: In([1, 2]) })` |
| `repo.exist(...)` | `repo.exists(...)` |
| `@Column({ readonly: true })` | `@Column({ update: false })` |
| `getRepository(User)` (global import) | `dataSource.getRepository(User)` |
| `getConnection()` / `getManager()` / `createConnection()` / `createQueryBuilder()` | `DataSource` instance methods |
| `@EntityRepository` + `AbstractRepository` + `getCustomRepository()` | `dataSource.getRepository(User).extend({ findByName(n) { ... } })` |
| `qb.onConflict(...)` | `qb.orIgnore()` / `qb.orUpdate()` |

**`null` / `undefined` in `where` now throws.** In 0.3 these keys were silently dropped, so a
generated service that spread an optional filter into `where` still worked. In 1.x it throws — build
the `where` object conditionally instead.

```ts
await repo.find({ where: { text: null } });      // 1.x: throws
await repo.find({ where: { text: IsNull() } });  // 1.x: correct null match (import IsNull)
// legacy opt-out, a DataSource option:
new DataSource({ invalidWhereValuesBehavior: { null: 'ignore', undefined: 'ignore' } });
```

**`nullable: false` relations now emit INNER JOIN**, not LEFT JOIN. So `@ManyToOne(() => User,
{ nullable: false })` loaded via `relations` silently drops rows with no match, where 0.3 returned
them with a null relation — a behavior change with no compile error. Keep a relation nullable unless
the FK genuinely cannot be null. Migrating a 0.3 codebase: `npx @typeorm/codemod v1 src/` covers most
of the table above. 1.x driver config: MySQL is `mysql2`-only (`connectorPackage` removed); SQLite
requires `better-sqlite3` and renames `busyTimeout` to `timeout`; MongoDB needs v7+; env-var
DataSource config is gone, use a file.

**`autoLoadEntities: true` only loads entities registered through `forFeature()`.** An entity reached
solely through another entity's relation is not included — register it in some module's
`forFeature()` or list it explicitly. → `/data/typeorm.md`

## Prisma

### Detect both packages — they version independently

```bash
node -p "['prisma','@prisma/client'].map(m=>m+' '+require('./node_modules/'+m+'/package.json').version)"
npm view prisma dist-tags && npm view @prisma/client dist-tags
```

The two `latest` tags do **not** track each other: the `prisma` CLI's `latest` points at a Prisma 8
prerelease, a different CLI that lacks `prisma migrate` and `prisma generate`. So
`npm i prisma @prisma/client` installs a CLI that cannot run the workflow.

- **Pin both to the same stable major** (`prisma@7`, `@prisma/client@7`), and match
  `@prisma/adapter-*` to the client. Generate for Prisma 8 only if the project already pins an 8
  prerelease on both, and flag it first — nothing below is confirmed for 8.
- **MongoDB stays on Prisma 6** — Prisma 7 supports the SQL databases only. A Mongo project on 6 uses
  the Prisma 6 shape below and needs no adapter.

### Prisma 6 → 7 changes that land on generated code

1. **Generator.** `prisma-client-js` is superseded by `prisma-client` (Rust-free). Set `output` inside
   `src/` so the client compiles with the app (`prisma init` defaults to `../generated/prisma`,
   outside it):

   ```prisma
   generator client {
     provider = "prisma-client"
     output   = "../src/generated/prisma"
   }
   ```

   **Module format follows the project.** Prisma infers it from `tsconfig.json`: an ESM Nest project
   (the v12 default) gets an ES module client and needs nothing. A **CommonJS** project adds
   `moduleFormat = "cjs"` — and must, before Prisma 7.10, whenever tsconfig says `nodenext`, which
   otherwise yields an ESM client inside a CJS app. Never add `cjs` to an ESM project.

2. **Connection config lives in a config file**, not the schema's `datasource` block (which keeps only
   `provider`). From 7.10 the file is `prisma7.config.ts`; earlier releases name it
   `prisma.config.ts`, which is still recognized — edit whichever exists, create the one matching the
   resolved version:

   ```ts
   import 'dotenv/config';
   import { defineConfig, env } from 'prisma/config';
   export default defineConfig({
     schema: 'prisma/schema.prisma',
     migrations: { path: 'prisma/migrations', seed: 'tsx prisma/seed.ts' },
     datasource: { url: env('DATABASE_URL') },
   });
   ```

3. **A driver adapter (or a Prisma Accelerate URL) is required** to construct a client. In Nest a
   missing one is not a type error — it surfaces at bootstrap as the provider failing to instantiate,
   which reads like a DI resolution failure. If a Prisma 7 service fails to resolve, check the adapter
   before checking the module wiring.

### PrismaService

**Prisma 7** — adapter into `super()`, and keep both hooks. The client connects lazily, so
`$connect()` in `onModuleInit` makes a bad connection fail at boot rather than on first query;
`$disconnect()` also ends the pool the adapter created:

```ts
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '../generated/prisma/client.js'; // generator output; drop `.js` in CommonJS

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor(configService: ConfigService) {
    super({ adapter: new PrismaPg({ connectionString: configService.getOrThrow<string>('DATABASE_URL') }) });
  }
  async onModuleInit() { await this.$connect(); }
  async onModuleDestroy() { await this.$disconnect(); }
}
```

This needs `ConfigModule.forRoot({ isGlobal: true })` with `DATABASE_URL` in its validation schema
(SKILL.md hard rule 2); without `@nestjs/config`, read `process.env` under `node --env-file=.env`.
`onModuleDestroy` runs on signals only if `main.ts` calls `app.enableShutdownHooks()`.

**Prisma 6** — the same service without the adapter: no constructor, `import { PrismaClient } from
'@prisma/client'` (or the generator's `output`).

### Choosing the adapter

| Package | Class |
|---|---|
| `@prisma/adapter-pg` | `PrismaPg` |
| `@prisma/adapter-better-sqlite3` | `PrismaBetterSqlite3` |
| `@prisma/adapter-mariadb` | `PrismaMariaDb` (MySQL, MariaDB) |
| `@prisma/adapter-mssql` | `PrismaMssql` (SQL Server, Azure SQL) |
| `@prisma/adapter-neon` | `PrismaNeon`, `PrismaNeonHttp` |
| `@prisma/adapter-planetscale` | `PrismaPlanetScale` |

Detect which `@prisma/adapter-*` is in `package.json`. **If none is installed on Prisma 7 and no
Accelerate URL is configured, STOP and ask which database** — do not guess an adapter, and do not fall
back to `new PrismaClient()`. → `/data/prisma.md`

## Drizzle

`@nestjs/drizzle` is the official integration; your training predates it. Detect `drizzle-orm`'s
resolved version: the docs target **Drizzle v1, published under the `rc` tag**
(`npm i @nestjs/drizzle drizzle-orm@rc` + `drizzle-kit@rc`); v0.35+ is also supported, and on v0.x only
relations and relational queries differ.

- `DrizzleModule.forRoot({ drizzle, connection })` takes the driver's `drizzle()` **function** (e.g.
  from `drizzle-orm/node-postgres`), not an instance. There is **no `forFeature()`**: tables are plain
  imports, and the database is injected anywhere with `@InjectDrizzle()`.
- v1 relations: `defineRelations(schema, r => …)`, passed as `forRoot({ …, relations })`; type the
  database once as `NodePgDatabase<typeof relations>` so `db.query` is typed.
- `forRoot()` options are evaluated at import, so read the URL via `forRootAsync()` + `ConfigService`.
  A `db` instance built at import time and passed as `forRoot({ db })` is shared by every app and closed
  by the first to shut down — per-test e2e apps break; build it in the `forRootAsync()` factory, or set
  `autoCloseConnection: false`. → `/data/drizzle.md`

## MikroORM

`@mikro-orm/nestjs` is third-party (not the Nest team's). The docs target **MikroORM v7**, which moved
imports your training will get wrong:

- Decorators (`@Entity()`, `@Property()`, …) are no longer exported from `@mikro-orm/core`. Nest uses
  legacy decorators, so import them from **`@mikro-orm/decorators/legacy`** (install
  `@mikro-orm/decorators`).
- `EntityManager`, `EntityRepository`, `MikroORM`, and `defineConfig` come from the **driver package**
  (e.g. `@mikro-orm/postgresql`).
- `ReflectMetadataProvider` is no longer the default — set `metadataProvider: ReflectMetadataProvider`
  (from `@mikro-orm/decorators/legacy`) explicitly.
- `MikroOrmModule.forRoot()` no longer accepts an empty argument list; pass the config.
  → `/data/mikroorm.md`
