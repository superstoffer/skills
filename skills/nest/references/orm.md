# ORM version facts

Contents: TypeORM detection & 0.3→1.x breaking changes · Prisma detection & 6→7 changes · PrismaService shape · adapter selection.

Your training is unreliable here. Two beliefs you may hold with high confidence are **false**: TypeORM
shipped a **1.x major**, and the string-array `relations: ['profile']` form **was removed** in it.
Do not trust recall below. Detect, then generate.

## TypeORM

### Detect the installed major first

Read the **resolved** version, never the range in `package.json`:

```bash
node -p "['typeorm','@nestjs/typeorm'].map(m=>m+' '+require(m+'/package.json').version)"
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

## Prisma

### Detect both packages — they version independently

```bash
node -p "['prisma','@prisma/client'].map(m=>m+' '+require(m+'/package.json').version)"
npm view prisma dist-tags && npm view @prisma/client dist-tags
```

The two `latest` tags do **not** track each other. The `prisma` CLI's `latest` has pointed at an
`8.0.0-rc.*` while `@prisma/client`'s `latest` was 7.x, and no stable `@prisma/client` 8 is
published (only `8.1.0-dev.*` prereleases) — so `npm i prisma @prisma/client` can install a
prerelease CLI against a stable client.

- **Safe pairs: CLI and client on the same stable major**, ideally the same exact version. Pin both.
- **Prisma 8 is a release candidate**, not stable, and its scope may still change. Generate for it only
  if the project already pins an 8 prerelease on both packages, and flag that first. Nothing below is
  confirmed for 8.
- `@prisma/adapter-*` packages track the client's version. Match them to `@prisma/client`.

### Prisma 6 → 7 changes that land on generated code

1. **Generator.** `prisma-client-js` is superseded by `prisma-client` (Rust-free) and will be
   removed. `output` is **required** on the new generator. For NestJS also set `moduleFormat`:

   ```prisma
   generator client {
     provider     = "prisma-client"
     output       = "../src/generated/prisma"
     moduleFormat = "cjs"   // Prisma 7 ships ESM by default; NestJS builds CommonJS
   }
   ```

2. **Connection config moves to `prisma.config.ts`**, not the schema's `datasource` block:

   ```ts
   import 'dotenv/config';
   import { defineConfig, env } from 'prisma/config';
   export default defineConfig({
     schema: 'prisma/schema.prisma',
     migrations: { path: 'prisma/migrations', seed: 'tsx prisma/seed.ts' },
     datasource: { url: env('DATABASE_URL') },
   });
   ```

3. **A driver adapter is mandatory for every database.** `new PrismaClient()` with no adapter throws
   *at construction*. In Nest that is not a type error — it surfaces at bootstrap as the provider
   failing to instantiate, which reads like a DI resolution failure. If a Prisma 7 service fails to
   resolve, check the adapter before checking the module wiring.

### PrismaService

**Prisma 7** — adapter into `super()`, no lifecycle hook:

```ts
import { Injectable } from '@nestjs/common';
import { PrismaClient } from './generated/prisma/client.js'; // the generator's output path
import { PrismaPg } from '@prisma/adapter-pg';

@Injectable()
export class PrismaService extends PrismaClient {
  constructor() {
    super({ adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL }) });
  }
}
```

**Prisma 6** — the `onModuleInit` / `$connect()` form. Correct for 6, wrong for 7:

```ts
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() { await this.$connect(); }
}
```

### Choosing the adapter

| Package | Class |
|---|---|
| `@prisma/adapter-pg` | `PrismaPg` |
| `@prisma/adapter-better-sqlite3` | `PrismaBetterSqlite3` |
| `@prisma/adapter-mariadb` | `PrismaMariaDb` (MySQL, MariaDB) |
| `@prisma/adapter-neon` | `PrismaNeon`, `PrismaNeonHttp` |
| `@prisma/adapter-planetscale` | `PrismaPlanetScale` |

Detect which `@prisma/adapter-*` is in `package.json`. **If none is installed on Prisma 7, STOP and
ask which database** — do not guess an adapter, and do not fall back to `new PrismaClient()`.
