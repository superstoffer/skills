# RED checklist — candidate rules

Scored against the four baseline runs in Task 2. A rule ships only if it has an
OBSERVED-FAIL, or if it guards a security or data-loss failure (R1–R5).

`F-PRISMA` = `fieldservice/apps/api` — Prisma 7.4.2, generator `output = "../src/generated/prisma"`,
`@nestjs/swagger` 11.2.6, `bcrypt` 6.0.0, `class-validator` 0.15.1, Jest, `uuid()` keys.
`F-TYPEORM` = `easy-grocery/apps/server` — TypeORM 0.3.26, `@nestjs/typeorm` 11.0.0, Jest,
existing `user.entity.ts`, `synchronize: false` already correct in two places.

| ID | Rule | Run | FAIL signature | PASS signature |
|---|---|---|---|---|
| R1 | `synchronize` env-gated | RED-2 | `synchronize: true`, or a new literal `true` added | left `false` / config-driven |
| R2 | bcrypt package matches what is installed | RED-3 | imports a package absent from `package.json` without adding it | imports the installed package, or adds the dep explicitly |
| R3 | password never returned or in JWT payload | RED-3 | `password` in a returned object or `sign()` payload | `@Exclude()`, `select`, `omit`, or explicit deletion |
| R4 | JWT secret from ConfigService | RED-3 | a string literal secret | `ConfigService` / `registerAsync` |
| R5 | required env vars validated at startup | RED-3 | `getOrThrow`/`get(...)!` with no `validationSchema` or `validate` | validation configured in `ConfigModule` |
| R6 | `APP_*` over `useGlobal*` when DI is needed | RED-2, RED-4 | `app.useGlobalGuards(new X(...))` where X injects | `APP_GUARD` provider |
| R7 | `PartialType` from `@nestjs/swagger` | RED-1 | imported from `@nestjs/mapped-types` while swagger is installed | imported from `@nestjs/swagger` |
| R8 | `getAllAndOverride` with `[handler, class]` | RED-4 | `getAllAndMerge`, or the array reversed | `getAllAndOverride(Key, [getHandler(), getClass()])` |
| R9 | `autoLoadEntities` not used in the CLI DataSource | RED-2 | `autoLoadEntities` added to `typeorm.datasource.ts` | explicit `entities` there |
| R10 | DTOs are classes, value-imported | RED-1 | `interface .*Dto`, or `import type {.*Dto}` | `export class .*Dto` + value import |
| R11 | every DTO property carries a validator | RED-1 | a property with no `class-validator` decorator | all decorated |
| R12 | `getRepositoryToken` as the spec provider token | RED-2 | `provide: Repository` or a bare string | `provide: getRepositoryToken(Order)` |
| R13 | literal routes declared before `:id` | RED-1, RED-2 | `@Get(':id')` above any literal route | literals first, or no literal routes added |
| R14 | `forwardRef` on a circular module pair | RED-3 | Auth↔Users cycle without it | `forwardRef(() => ...)` both sides, or no cycle created |
| R15 | e2e closes the app | RED-2 | `afterAll` without `app.close()` | `await app.close()`, or no e2e written |
| R16 | `ParseUUIDPipe` for uuid keys | RED-1 | `ParseIntPipe` on a uuid param | `ParseUUIDPipe` or no pipe |
| R17 | specs assert real behaviour | RED-2 | `should be defined` is the only test | per-method assertions incl. an error path |
| R18 | Prisma module provides **and exports** the service | RED-1 | `PrismaService` in `providers` with no `exports` | provided and exported, or existing module imported |
| R19 | `findFirst` for non-unique lookups | RED-1 | `findUnique({ where: { <non-unique> } })` | `findUnique` only on `@id`/`@unique`, else `findFirst` |
| R20 | Prisma 7 client import path | RED-1 | `import { PrismaClient } from '@prisma/client'` | imported from `src/generated/prisma` per the generator `output` |
| R21 | new module registered in `AppModule` | RED-1, RED-2 | module created but absent from `app.module.ts` imports | registered |
