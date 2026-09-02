# RED baseline results

Run 2026-09-02 against git worktrees of two real projects, with the `nest`
skill absent from disk. Four coding runs plus one knowledge probe.

## Coding runs

| Run | Fixture | Prompt | Outcome |
|---|---|---|---|
| RED-1 | `fieldservice/apps/api` (Nest 11.1.14, Prisma 7.4.2, Swagger, uuid keys) | "Add a CRUD resource for orders. Fields: name (string) and total (number)." | 7 files written |
| RED-2 | `easy-grocery/apps/server` (Nest 11.0.1, TypeORM 0.3.26) | same, plus "add unit tests for the service" | 8 files written |
| RED-3 | `easy-grocery/apps/server` | "Add JWT login. Users authenticate with email and password." | 14 files written |
| RED-4 | `fieldservice/apps/api` | "Add a roles guard so that only admins can delete a customer." | **no files** — feature already existed; declined to add redundant code or invent an `ADMIN` role absent from the schema |

## Scoring

| ID | Rule | Result | Evidence |
|---|---|---|---|
| R1 | `synchronize` env-gated | PASS | left `synchronize: false` untouched in both places |
| R2 | bcrypt package matches installed | PASS | imported `bcrypt` **and** added `"bcrypt": "^6.0.0"` to package.json |
| R3 | password never returned or in JWT | PASS | `@Column({ name: 'password_hash', select: false })`, `.addSelect('user.passwordHash')` at login, payload `{ sub, email }` only |
| R4 | JWT secret from ConfigService | PASS | `JwtModule.registerAsync` + `ConfigService`, throws when absent |
| **R5** | **required env vars validated at startup** | **FAIL** | `ConfigModule.forRoot({ isGlobal: true })` — no `validationSchema`, no `validate`. A hand-rolled `if (!secret) throw` covers `JWT_SECRET` only; DB vars fall back to `??` defaults |
| R6 | `APP_*` over `useGlobal*` | NOT-EXERCISED | no global guard was created in any run |
| R7 | `PartialType` from `@nestjs/swagger` | PASS | imported `IntersectionType, OmitType, PartialType, PickType` from `@nestjs/swagger` |
| R8 | `getAllAndOverride([handler, class])` | NOT-EXERCISED | fixture already contained a correct `roles.guard.ts`; RED-4 wrote nothing |
| R9 | `autoLoadEntities` absent from CLI DataSource | PASS | added `entities: [User, Order]` explicitly to `typeorm.datasource.ts` |
| R10 | DTOs are classes, value-imported | PASS | `export class CreateOrderDto` with value imports |
| R11 | every DTO property validated | PASS | `@IsString()`, `@Type(() => Number) @IsNumber() @Min(0)` |
| R12 | `getRepositoryToken` as spec token | PASS | `provide: getRepositoryToken(Order)` |
| R13 | literal routes before `:id` | NOT-EXERCISED | no literal routes created |
| R14 | `forwardRef` on circular pair | PASS | created no cycle |
| R15 | e2e closes the app | NOT-EXERCISED | no new e2e written |
| R16 | `ParseUUIDPipe` for uuid keys | PASS | `@Param('id', ParseUUIDPipe)` on all three routes, both fixtures |
| R17 | specs assert real behaviour | PASS | 8 `it()` blocks, zero `should be defined`, 7 `NotFoundException` error paths |
| R18 | Prisma module provides and exports | PASS | reused the existing `PrismaModule`, which already exports `PrismaService` |
| R19 | `findFirst` for non-unique lookups | PASS | used `findFirst` for the tenant-scoped read |
| **R20** | **Prisma 7 client import path** | PASS | `import type { Prisma } from '../generated/prisma/client'` — read the generator `output` block rather than assuming `@prisma/client` |
| R21 | new module registered in `AppModule` | PASS | registered in both runs |

**14 PASS, 1 FAIL, 5 NOT-EXERCISED, 1 partial.**

## Knowledge probe

A fresh agent, all tools disabled, asked five NestJS/TypeORM version questions.

| Question | Answer | Verdict |
|---|---|---|
| Latest NestJS major? | "no reliable knowledge of a NestJS 12 release" | DO-NOT-KNOW |
| v12 Standard Schema with Zod? | "I won't invent a decorator name or a registration step" | DO-NOT-KNOW |
| v12 `@nestjs/config` `validationSchema` change? | "I won't guess at a migration step" | DO-NOT-KNOW |
| v12 default test runner / linter? | correct for v11, "cannot confirm" for v12 | DO-NOT-KNOW |
| TypeORM latest major; is string-array `relations` removed? | "TypeORM has never left `0.x`"; "the array form was not removed" — labelled **CERTAIN** | **CONFIDENTLY WRONG** |

Ground truth: `typeorm@latest` is 1.1.1 (2026-09-01); `0.3.31` is tagged
`legacy`; string-array `relations` and `select` are removed in 1.x.

## Conclusion

The pitfalls list does not change behaviour. Claude reads the project and
applies these correctly on its own — including the two findings the design
review considered most dangerous (the Prisma 7 generated-client path, and
`getRepositoryToken` in specs).

Where Claude fails is where it structurally cannot succeed: framework releases
after its training cutoff. The two failure shapes differ in severity —
NestJS 12 produces honest refusal, which a user notices; TypeORM 1.x produces
confident wrongness, which a user ships.

**The skill ships version knowledge and a verification procedure. It does not
ship a pitfalls list.**

## Rules that ship

- **R5** — required env vars belong in the `ConfigModule` validation schema;
  `getOrThrow` throws at call time, not startup.

All others cut. R6, R8, R13, R15 were never exercised and are not security or
data-loss rules; they are recorded here rather than shipped, and can be
revisited if a future RED run exercises them.
