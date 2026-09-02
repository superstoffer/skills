# `nest` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a `nest` skill in `superstoffer/skills` that scaffolds NestJS code matching the target project's actual package majors, and that verifies its output compiles and resolves.

**Architecture:** One skill folder. `SKILL.md` holds detection, routing, the verify procedure, and the security prohibitions. Seven `references/` files hold mode procedures and two cross-cutting modifiers (ORM, Nest version) that `SKILL.md` orders directly during detection. The rules are the product; templates exist to carry them.

**Tech Stack:** Markdown with YAML frontmatter. No runtime code. Verification is behavioural — real prompts against real NestJS projects on this machine.

**Spec:** `docs/superpowers/specs/2026-09-02-nest-skill-design.md`

---

## Why the test phase comes first

This artifact is a prompt document, so there is no unit test for "does this SKILL.md make Claude emit `getRepositoryToken`". The equivalent of a failing test is **watching plain Claude fail without the skill**, then writing the rule, then re-running the same prompt.

**The baseline window closes the moment the skill is installed.** Phase 1 must complete before any line of `SKILL.md` is written. A rule that survives no RED failure is dead weight loaded into every invocation.

## Fixtures

Verified present on this machine on 2026-09-02:

| ID | Path | Nest (resolved) | Stack |
|---|---|---|---|
| F-PRISMA | `/Users/christoffer/Privat/cb/epicly-aos/backend` | 11.1.13 (installed) | Prisma 7.4.0, class-validator, Jest |
| F-TYPEORM | `/Users/christoffer/Privat/cb/easy-grocery/apps/server` | 11 (declared) | TypeORM 0.3.26, Jest |
| F-SWAGGER | `/Users/christoffer/Privat/cb/fieldservice/apps/api` | 11.1.14 (declared) | Prisma 7.4.2, `@nestjs/swagger` 11.2.6, Jest |
| F-VITEST | `/Users/christoffer/Privat/cb/doculogic/backend` | 11 (declared) | Vitest 3.1, no ORM |
| F-V10 | `/Users/christoffer/Privat/cb/shopper/apps/api` | 10.4 (declared) | Jest, real `typecheck` script |

**Known gaps, carried as limitations:** no Nest v12 project and no TypeORM 1.x project exists locally. Those paths are written from primary sources and cannot be RED-baselined. Recorded in Task 26.

**Fixture safety protocol — apply to every fixture run:**

```bash
cd <FIXTURE>
git status --porcelain            # MUST be empty; if not, skip this fixture
git checkout -b red-baseline-throwaway
# ... run the prompt ...
git checkout . && git clean -fd
git checkout - && git branch -D red-baseline-throwaway
```

Never leave a fixture modified. Never commit in a fixture.

---

## File Structure

**Created:**

| Path | Responsibility | Budget |
|---|---|---|
| `skills/nest/SKILL.md` | Frontmatter, detection, routing, verify, security prohibitions, reference index | <= 220 lines |
| `skills/nest/README.md` | Human-facing: what it does, install, CLAUDE.md trigger snippet | <= 80 lines |
| `skills/nest/references/orm.md` | Cross-cutting: TypeORM 0.3/1.x vs Prisma 6/7 | <= 150 lines |
| `skills/nest/references/version-matrix.md` | Cross-cutting: Nest v11 vs v12 | <= 120 lines |
| `skills/nest/references/resource.md` | Resource + Swagger modes | <= 250 lines |
| `skills/nest/references/auth.md` | Auth mode | <= 200 lines |
| `skills/nest/references/testing.md` | Testing mode; Jest and Vitest | <= 200 lines |
| `skills/nest/references/pipeline.md` | Pipeline mode | <= 200 lines |
| `skills/nest/references/infrastructure.md` | Infrastructure + Queues modes | <= 250 lines |

**Modified:** `README.md`, `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`

**Working files (scratchpad, not committed):** `red/` transcripts and results under the session scratchpad.

---

## Phase 1 — RED baseline

### Task 1: Write the rule-candidate assertion checklist

**Files:**
- Create: `docs/superpowers/plans/red-checklist.md`

- [ ] **Step 1: Write the checklist**

Each row is a candidate rule from the spec, with a grep-able signature that
distinguishes pass from fail. A rule with no observed failure gets cut.

```markdown
# RED checklist — candidate rules

| ID | Rule | Fixture | FAIL signature (grep the transcript) | PASS signature |
|---|---|---|---|---|
| R1 | synchronize gated by env | F-TYPEORM | `synchronize: true` present and not env-gated | `synchronize:` reads from config, or `false` |
| R2 | bcrypt package match | F-PRISMA | imports `bcrypt` when only `bcryptjs` in package.json | imports the installed package |
| R3 | password never returned | F-PRISMA | `password` appears in a returned object or JWT payload | `@Exclude()`, `select`, or `omit` present |
| R4 | JWT secret from ConfigService | F-PRISMA | a string literal secret | `ConfigService` / `registerAsync` |
| R5 | env vars in validation schema | F-PRISMA | `getOrThrow` or `get(...)!` with no `validationSchema`/`validate` | validation configured |
| R6 | APP_* over useGlobal for DI | F-TYPEORM | `app.useGlobalGuards(new` with an injected dep | `APP_GUARD` provider |
| R7 | PartialType from swagger | F-SWAGGER | `PartialType` from `@nestjs/mapped-types` while `@nestjs/swagger` installed | from `@nestjs/swagger` |
| R8 | getAllAndOverride + order | F-TYPEORM | `getAllAndMerge`, or `[getClass(), getHandler()]` | `getAllAndOverride(..., [getHandler(), getClass()])` |
| R9 | autoLoadEntities not in CLI DataSource | F-TYPEORM | `autoLoadEntities` in a standalone DataSource file | explicit `entities` array there |
| R10 | DTOs are classes, value-imported | F-PRISMA | `interface .*Dto`, or `import type {.*Dto` | `export class .*Dto` + value import |
| R11 | whitelist strips undecorated | F-PRISMA | a DTO property with no validator while `whitelist: true` | every property decorated |
| R12 | getRepositoryToken in specs | F-TYPEORM | `provide: Repository` | `provide: getRepositoryToken(` |
| R13 | route order :id vs literal | F-TYPEORM | `@Get(':id')` declared before a literal route | literal routes first |
| R14 | forwardRef on circular modules | F-PRISMA | Auth<->Users import cycle with no `forwardRef` | `forwardRef(() =>` both sides |
| R15 | e2e closes the app | F-TYPEORM | `afterAll` without `app.close()` | `await app.close()` |
| R16 | ParseUUIDPipe for uuid keys | F-PRISMA | `ParseIntPipe` on a uuid-typed param | `ParseUUIDPipe` |
| R17 | no empty spec | F-TYPEORM | `should be defined` is the only test | real assertions per method |
| R18 | Prisma module exports service | F-PRISMA | `PrismaService` in `providers` with no `exports` | provided **and** exported |
| R19 | findFirst for non-unique | F-PRISMA | `findUnique({ where: { <non-unique> } })` | `findFirst` |
| R20 | Prisma 7 adapter in constructor | F-PRISMA | `extends PrismaClient` with only `onModuleInit`/`$connect` | adapter passed to `super({ adapter })` |
| R21 | app.module.ts registered | F-TYPEORM | new module never added to `AppModule` imports | edit made or shown |
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/plans/red-checklist.md
git commit -m "Add RED checklist for nest skill rule candidates

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 2: RED run — CRUD resource on the Prisma fixture

**Files:**
- Create: `<scratchpad>/red/R-prisma-resource.md`

- [ ] **Step 1: Confirm the fixture is clean**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && git status --porcelain
```
Expected: no output. If any output, stop and report — do not modify a dirty fixture.

- [ ] **Step 2: Branch**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && git checkout -b red-baseline-throwaway
```
Expected: `Switched to a new branch 'red-baseline-throwaway'`

- [ ] **Step 3: Run the baseline prompt**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && \
claude -p "Add a CRUD resource for orders with fields name (string) and total (number)." \
  > "$SCRATCH/red/R-prisma-resource.md" 2>&1
```

The `nest` skill does not exist yet, so this run **is** the baseline. Do not
install or reference the skill before Phase 1 completes.

- [ ] **Step 4: Score against the checklist**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend
git diff --stat
grep -nE "interface .*Dto|import type \{[^}]*Dto" -r src/ || echo "R10 pass"
grep -rn "PrismaService" src/*/*.module.ts | grep -c exports || echo "R18 FAIL: not exported"
grep -rnE "findUnique\(\{ *where" src/ || echo "R19 n/a"
grep -rn "ParseIntPipe" src/ && grep -rn "@id .*Uuid\|uuid()" prisma/schema.prisma && echo "R16 FAIL"
grep -rn "OrdersModule" src/app.module.ts || echo "R21 FAIL: not registered"
```

Record each of R3, R10, R11, R14, R16, R18, R19, R20, R21 as PASS or FAIL with
the verbatim offending line. **Do not fix anything.**

- [ ] **Step 5: Revert the fixture**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && \
git checkout . && git clean -fd && git checkout - && git branch -D red-baseline-throwaway && git status --porcelain
```
Expected: no output from `git status`.

- [ ] **Step 6: Commit the finding**

```bash
git -C /Users/christoffer/Privat/cb/skills add docs/superpowers/plans/red-results.md
git -C /Users/christoffer/Privat/cb/skills commit -m "RED: Prisma resource baseline

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 3: RED run — CRUD resource on the TypeORM fixture

**Files:**
- Append: `docs/superpowers/plans/red-results.md`

- [ ] **Step 1: Clean check and branch**

```bash
cd /Users/christoffer/Privat/cb/easy-grocery/apps/server && git status --porcelain && git checkout -b red-baseline-throwaway
```
Expected: no status output, then `Switched to a new branch`.

- [ ] **Step 2: Run**

```bash
cd /Users/christoffer/Privat/cb/easy-grocery/apps/server && \
claude -p "Add a CRUD resource for orders with fields name (string) and total (number), plus unit tests for the service." \
  > "$SCRATCH/red/R-typeorm-resource.md" 2>&1
```

- [ ] **Step 3: Score R1, R6, R9, R12, R13, R15, R17, R21**

```bash
cd /Users/christoffer/Privat/cb/easy-grocery/apps/server
grep -rn "provide: *Repository" src/ && echo "R12 FAIL: raw Repository token"
grep -rn "getRepositoryToken" src/ || echo "R12 FAIL: token absent"
grep -rn "should be defined" src/ && echo "R17 candidate FAIL"
grep -n "@Get(':id')" -A3 -B3 src/orders/orders.controller.ts
grep -rn "synchronize" src/ ormconfig* 2>/dev/null
grep -n "OrdersModule" src/app.module.ts || echo "R21 FAIL: not registered"
```

Record verbatim. Do not fix.

- [ ] **Step 4: Revert**

```bash
cd /Users/christoffer/Privat/cb/easy-grocery/apps/server && \
git checkout . && git clean -fd && git checkout - && git branch -D red-baseline-throwaway && git status --porcelain
```
Expected: no output.

- [ ] **Step 5: Commit findings**

```bash
git -C /Users/christoffer/Privat/cb/skills add docs/superpowers/plans/red-results.md
git -C /Users/christoffer/Privat/cb/skills commit -m "RED: TypeORM resource baseline

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 4: RED run — auth on the Prisma fixture

- [ ] **Step 1: Clean check and branch**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && git status --porcelain && git checkout -b red-baseline-throwaway
```
Expected: no status output.

- [ ] **Step 2: Run**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && \
claude -p "Add JWT login. Users authenticate with email and password." \
  > "$SCRATCH/red/R-prisma-auth.md" 2>&1
```

- [ ] **Step 3: Score R2, R3, R4, R5, R14**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend
grep -rn "from 'bcrypt'" src/ && grep -c '"bcryptjs"' package.json && echo "R2 FAIL: wrong package"
grep -rnE "secret: *'|secret: *\"" src/ && echo "R4 FAIL: literal secret"
grep -rn "password" src/auth/ | grep -vE "compare|hash|Dto|@|password:" && echo "R3 review needed"
grep -rn "validationSchema\|validate:" src/app.module.ts || echo "R5 FAIL: no startup validation"
grep -rn "forwardRef" src/auth/auth.module.ts src/users/users.module.ts || echo "R14 candidate FAIL"
```

- [ ] **Step 4: Revert**

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && \
git checkout . && git clean -fd && git checkout - && git branch -D red-baseline-throwaway && git status --porcelain
```
Expected: no output.

- [ ] **Step 5: Commit findings**

```bash
git -C /Users/christoffer/Privat/cb/skills add docs/superpowers/plans/red-results.md
git -C /Users/christoffer/Privat/cb/skills commit -m "RED: Prisma auth baseline

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 5: RED run — roles guard and Swagger

- [ ] **Step 1: Roles guard on F-TYPEORM**

```bash
cd /Users/christoffer/Privat/cb/easy-grocery/apps/server && git status --porcelain && git checkout -b red-baseline-throwaway && \
claude -p "Add a roles guard so only admins can delete an order." > "$SCRATCH/red/R-guard.md" 2>&1
grep -rn "getAllAndMerge" src/ && echo "R8 FAIL: merge"
grep -rnE "getAllAndOverride\([^,]+, *\[\s*context.getClass" src/ && echo "R8 FAIL: order reversed"
git checkout . && git clean -fd && git checkout - && git branch -D red-baseline-throwaway
```
Expected: `git status --porcelain` silent at start and end.

- [ ] **Step 2: Swagger annotation on F-SWAGGER**

```bash
cd /Users/christoffer/Privat/cb/fieldservice/apps/api && git status --porcelain && git checkout -b red-baseline-throwaway && \
claude -p "Add OpenAPI annotations to the controllers and DTOs." > "$SCRATCH/red/R-swagger.md" 2>&1
grep -rn "@nestjs/mapped-types" src/ && echo "R7 FAIL: wrong PartialType source"
git checkout . && git clean -fd && git checkout - && git branch -D red-baseline-throwaway
```

- [ ] **Step 3: Commit findings**

```bash
git -C /Users/christoffer/Privat/cb/skills add docs/superpowers/plans/red-results.md
git -C /Users/christoffer/Privat/cb/skills commit -m "RED: guard and swagger baselines

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 6: Prune the rule list

**Files:**
- Modify: `docs/superpowers/plans/red-results.md`

- [ ] **Step 1: Tabulate**

For R1–R21, mark OBSERVED-FAIL, PASS, or NOT-EXERCISED.

- [ ] **Step 2: Apply the cut**

- **OBSERVED-FAIL** → the rule ships. It has evidence.
- **PASS** → cut it. Plain Claude already does this; the rule is dead weight.
- **NOT-EXERCISED** → keep only if it guards a security or data-loss failure
  (R1, R3, R4, R5). Otherwise cut and note it for a later pass.

- [ ] **Step 3: Write the surviving list**

Write the final rule set to `docs/superpowers/plans/red-results.md` under
`## Rules that ship`, each with the verbatim failing line that justifies it.
**This list, not the spec's candidate list, is what Phase 3 and 4 implement.**

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/plans/red-results.md
git commit -m "Prune nest rule candidates to those with observed failures

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

## Phase 2 — Skeleton and triggering

### Task 7: Create the skill folder and frontmatter

**Files:**
- Create: `skills/nest/SKILL.md`

- [ ] **Step 1: Write frontmatter and title**

```markdown
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

Scaffold and modify NestJS code that matches the project's actual stack.
```

- [ ] **Step 2: Verify the character budget**

```bash
awk '/^description: >-/,/^---$/' skills/nest/SKILL.md | sed '1d;$d' | tr -d '\n' | sed 's/  */ /g' | wc -c
```
Expected: a number <= 900. (Measured at 779 during spec review.)

```bash
awk '/^---$/{n++} n==1' skills/nest/SKILL.md | wc -c
```
Expected: <= 1000.

- [ ] **Step 3: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest skill frontmatter

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 8: Trigger tests

**Files:**
- Create: `docs/superpowers/plans/trigger-results.md`

Triggering and behaviour are different failures. This tests only whether the
skill fires, which is the thing a technology skill most often gets wrong.

- [ ] **Step 1: Install the skill locally for testing**

```bash
mkdir -p ~/.claude/skills && cp -r skills/nest ~/.claude/skills/ && ls ~/.claude/skills/nest
```
Expected: `README.md  SKILL.md  references` (references may be absent this early).

- [ ] **Step 2: Must-fire cases — no NestJS vocabulary, inside a Nest project**

Run each in `/Users/christoffer/Privat/cb/epicly-aos/backend`, recording whether
the `nest` skill was invoked:

1. `add an endpoint for orders`
2. `users need to be able to log in`
3. `write tests for the payments service`

Expected: fires on all three. A miss here means the ALSO clause is not doing
its job — revise the description, do not proceed.

- [ ] **Step 3: Must-not-fire cases**

1. In `/Users/christoffer/Privat/cb/skills` (not a Nest project): `write a DTO for the user payload`
2. In any non-Nest TS project: `add a guard to this Express route`

Expected: does not fire. A hit means the exclusion clause is too weak.

- [ ] **Step 4: Sibling-collision check**

In `/Users/christoffer/Privat/cb/skills`: `write the api docs for this`

Expected: does not steal from `design-doc`. This is why bare `docs` was
excluded as a keyword.

- [ ] **Step 5: Record and commit**

```bash
git add docs/superpowers/plans/trigger-results.md
git commit -m "Record nest skill trigger test results

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

**Gate:** do not proceed to Phase 3 until must-fire and must-not-fire both pass.

---

## Phase 3 — `SKILL.md` body

### Task 9: Detection step

**Files:**
- Modify: `skills/nest/SKILL.md`

- [ ] **Step 1: Write Step 1**

Append the detection section. Order matters — layout resolves first, because
in monorepo mode `src/main.ts` does not exist.

```markdown
## Step 1 — Detect

Read before generating anything. Read **resolved** versions, not declared
ranges: `package.json` holds `^11.0.0`, which cannot distinguish 11.0.0 from
11.2.3. Read `node_modules/<pkg>/package.json` or the lockfile. pnpm
workspaces write `catalog:` and `workspace:*`, which carry no version at all.

**Resolve layout first.** In Nest monorepo mode sources live at
`apps/<name>/src/` per `sourceRoot` and the `projects` map in `nest-cli.json`.
Every write path in every mode depends on this.

| Read | Determines |
|---|---|
| `nest-cli.json` `projects` / `sourceRoot` | Monorepo layout; all write paths |
| Resolved `@nestjs/core` | v11 vs v12 |
| Resolved `@nestjs/config` | Standard Schema validation — peers `^11 \|\| ^12`, so gate on this package, not core |
| Resolved `typeorm` + `@nestjs/typeorm` | TypeORM 0.3 vs 1.x. `@nestjs/typeorm` must be >= 11.0.1 for TypeORM 1.x; its peer range spans both majors, so npm installs a broken pair silently |
| Resolved `@prisma/client`; generator `output`; `prisma.config.ts` | Prisma 6 vs 7; the generated client's import path |
| Installed `@prisma/adapter-*` | Prisma 7 driver adapter — refuse to guess if absent |
| `tsconfig.json` | `experimentalDecorators`, `emitDecoratorMetadata`, `strictPropertyInitialization`, `verbatimModuleSyntax`, `paths` |
| `package.json` `type` **and** tsconfig `module`/`moduleResolution` | Emitted module format — `"type": "module"` alone does not determine it |
| `jest` / `vitest` in devDependencies | Spec idiom. Both present: prefer the test script's runner |
| `class-validator` / `class-transformer` | Whether DTO decorators compile — not Nest dependencies |
| `bcrypt` vs `bcryptjs` | Which to import; the wrong one is a hard failure |
| `@nestjs/swagger`, `@nestjs/jwt`, `passport` | Whether to annotate; whether auth exists |
| Lockfile name | Package manager for the verify step |

**Both ORMs present:** ask. Do not guess.
**No `@nestjs/core`:** say so and stop. Never scaffold Nest into an Express
project; never offer to install NestJS unless asked.

Then, before routing:
- `@nestjs/core` v12 or later → read `references/version-matrix.md` now.
- An ORM detected → read `references/orm.md` now.
```

- [ ] **Step 2: Verify against a real fixture**

```bash
cat /Users/christoffer/Privat/cb/epicly-aos/backend/node_modules/@nestjs/core/package.json | grep '"version"'
```
Expected: `"version": "11.1.13"` — confirming resolved-version reads work and
differ from the declared `^11.0.1`.

- [ ] **Step 3: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest detection step

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 10: Routing

**Files:**
- Modify: `skills/nest/SKILL.md`

- [ ] **Step 1: Write Step 2 as a lookup, not a switch**

```markdown
## Step 2 — Route

**This is a lookup, not a switch.** Modes compose. Select *every* mode the
request touches.

| User mentions | Mode | Read |
|---|---|---|
| resource, entity, CRUD, controller, endpoint | Resource | `references/resource.md` |
| auth, login, JWT, passport, register, token | Auth | `references/auth.md` |
| test, spec, unit test, e2e | Testing | `references/testing.md` |
| swagger, openapi, api docs, `@Api` | Swagger | `references/resource.md` |
| guard, interceptor, custom decorator, filter, middleware | Pipeline | `references/pipeline.md` |
| setup, bootstrap, main.ts, config, env, migration, DataSource | Infrastructure | `references/infrastructure.md` |
| queue, job, worker, BullMQ, background | Queues | `references/infrastructure.md` |

Execute in dependency order:
**Infrastructure → Resource → Auth → Pipeline → Queues → Swagger → Testing.**
Swagger annotates code that must already exist; tests test code that must
already exist.

Generic verbs — `generate`, `scaffold`, `add` — select the skill, never a mode.

### Worked examples

| Request | Modes | Order |
|---|---|---|
| "Add a JWT-protected orders resource with Swagger and tests" | Resource, Auth, Swagger, Testing | Resource → Auth → Swagger → Testing |
| "Add an endpoint for orders" | Resource | — |
| "Add a roles guard so only admins can delete" | Pipeline | — |
| "Set up config validation and add a queue for emails" | Infrastructure, Queues | Infrastructure → Queues |
| "Write tests for the payments service" | Testing | — |

**No match:** answer directly from the rules and the detected versions. Do not
force a scaffold. This covers "why is my guard returning 403", "fix this DI
error", "review this controller", "upgrade us to v12". For the last, recommend
`nest upgrade --dry-run`, which mechanically applies most of the migration.
```

- [ ] **Step 2: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest routing as a composable lookup

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 11: Write-and-verify step

**Files:**
- Modify: `skills/nest/SKILL.md`

- [ ] **Step 1: Write Step 3**

```markdown
## Step 3 — Write and verify

### Writing

Files land at the resolved layout path, never a hardcoded `src/`.

Make the `app.module.ts` registration edit **yourself**. Telling the user to
add the import is a trap: the typecheck passes, the report says success, and
the module is unregistered at runtime.

### Verifying

1. **Baseline.** Run the typecheck *before* writing. Record the error set.
   Real repos have pre-existing errors; without a baseline you will either
   report failure on good output or "repair" files nobody mentioned.
2. **Write, then re-run.** Only errors absent from the baseline are in scope.
3. **Compile the module graph.** `tsc` cannot catch the most common scaffold
   failure — Nest resolves DI at runtime, so a module missing from `imports`,
   a provider missing from `exports`, or a cycle needing `forwardRef` all
   typecheck clean and throw on boot. Run:
   `Test.createTestingModule({ imports: [AppModule] }).compile()`.
   If it cannot run, say so.
4. **Repair, bounded.** Maximum two attempts. Stop if the new-error count does
   not strictly decrease. Edits are confined to files this invocation wrote,
   plus the announced `app.module.ts` edit. Never revert the user's existing
   code to silence an error.
5. **Report, fixed shape:**
   - Files written
   - Command run
   - Error count before → after
   - What remains unfixed

   Say "compiles" and "module graph resolves". Never say "works". If specs
   were generated but not run, say they were not run and do not claim they
   pass.

**Typecheck lookup order:** `package.json` scripts `typecheck` → `type-check`
→ `npx tsc --noEmit -p <resolved tsconfig>`.

**`build` is excluded.** `nest build` writes `dist/` and in many repos
triggers codegen, containers, or DB access. The one legitimate pre-step is
`prisma generate`, without which every generated-client import is unresolved
for reasons unrelated to what you wrote.

**Never run `npm install`.** If `node_modules` is absent, report and stop.
```

- [ ] **Step 2: Sanity-check the lookup order against fixtures**

```bash
grep -o '"typecheck"' /Users/christoffer/Privat/cb/shopper/apps/api/package.json || echo "no typecheck script"
grep -o '"typecheck"' /Users/christoffer/Privat/cb/epicly-aos/backend/package.json || echo "F-PRISMA has no typecheck script - falls through to tsc --noEmit"
```
Expected: F-V10 has one, F-PRISMA does not — exercising both branches.

- [ ] **Step 3: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest write-and-verify procedure with baseline diff

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 12: Hard rules

**Files:**
- Modify: `skills/nest/SKILL.md`
- Read: `docs/superpowers/plans/red-results.md`

- [ ] **Step 1: Write only the rules that survived Task 6**

Use the heading `## Hard rules` — both sibling skills use it literally.

Only security and data-loss rules go here. Every other surviving rule goes
into the reference file next to the template it governs, **stated exactly
once**. If a rule was cut in Task 6, it does not appear anywhere.

Template for each entry — state the mechanism, not the goal:

```markdown
## Hard rules

1. **`synchronize` is never `true` outside development.** Drive it from
   config, never a literal; always `false` in the migration DataSource. Warn
   only when it is hardcoded `true` or not environment-gated.
2. **Passwords compare with `bcrypt.compare()`, never `===`.** Import the
   package the project actually has — `bcrypt` and `bcryptjs` are not
   interchangeable.
3. **Never return `password`; never place it in a JWT payload.** Use
   `@Exclude()` plus a global `ClassSerializerInterceptor`, TypeORM
   `@Column({ select: false })` with `addSelect` at login, or an explicit
   Prisma `select`/`omit`. `ClassSerializerInterceptor` does nothing when the
   handler returns a plain object rather than a class instance — a silent leak.
4. **JWT secrets come from `ConfigService`, never a literal.**
5. **Every required env var appears in the `ConfigModule` validation schema.**
   `getOrThrow` throws at call time, not startup — a key read inside a handler
   boots green and dies on first traffic. Validation is the startup gate;
   `getOrThrow` is only the accessor. `ConfigService<Config, true>` makes
   `get<T>()` return `T`, removing the `!`.
```

- [ ] **Step 2: Verify single-sourcing**

```bash
for rule in "synchronize" "bcrypt.compare" "ClassSerializerInterceptor" "getOrThrow" "getRepositoryToken" "getAllAndOverride" "PartialType"; do
  echo -n "$rule: "; grep -rl "$rule" skills/nest/ | tr '\n' ' '; echo
done
```
Expected: each string appears in exactly one file. More than one means drift risk — consolidate before committing.

- [ ] **Step 3: Check the line budget**

```bash
wc -l skills/nest/SKILL.md
```
Expected: <= 220.

- [ ] **Step 4: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest hard rules, pruned to observed failures

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 13: Reference index

**Files:**
- Modify: `skills/nest/SKILL.md`

- [ ] **Step 1: Add the closing section**

Both sibling skills end with exactly this section. It tells the model what is
available to read.

```markdown
## Reference files

- `references/orm.md` — cross-cutting: TypeORM 0.3/1.x vs Prisma 6/7. Read during detection when an ORM is present.
- `references/version-matrix.md` — cross-cutting: Nest v11 vs v12 deltas. Read during detection when v12+ is present.
- `references/resource.md` — CRUD scaffold and Swagger annotation
- `references/auth.md` — strategies, guards, RBAC
- `references/testing.md` — service, controller, and e2e specs; Jest and Vitest
- `references/pipeline.md` — guards, interceptors, pipes, filters, custom decorators
- `references/infrastructure.md` — `main.ts`, `ConfigModule`, migrations, BullMQ queues
```

- [ ] **Step 2: Commit**

```bash
git add skills/nest/SKILL.md
git commit -m "Add nest reference index

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

## Phase 4 — Reference files

Each task below follows the same shape: write the file with a table of
contents at the top, keep it under budget, confirm no rule is restated from
`SKILL.md` or another reference, commit.

### Task 14: `references/orm.md`

**Files:**
- Create: `skills/nest/references/orm.md`

- [ ] **Step 1: Write the ORM comparison**

Targets current stable — TypeORM 1.x (`latest` 1.1.1) and Prisma 7.x
(`@prisma/client` `latest` 7.10.0) — while detecting older majors so existing
projects still generate correctly.

```markdown
# ORM

Contents: version detection · comparison table · TypeORM 1.x migration notes · Prisma 7 client construction

## Detect the major first

| Package | Majors handled |
|---|---|
| `typeorm` | 0.3.x, 1.x |
| `@nestjs/typeorm` | must be >= 11.0.1 for TypeORM 1.x |
| `@prisma/client` | 6.x, 7.x |

## Comparison

| Concern | TypeORM 1.x | Prisma 7.x |
|---|---|---|
| Definition | `*.entity.ts` decorators | `schema.prisma`; no entity file, but generated **types** are imported |
| Client | — | Not from `@prisma/client`; from the generator's `output` path, which must be somewhere `tsc` compiles |
| Service | `@InjectRepository(E) repo: Repository<E>` | `PrismaService extends PrismaClient` with a **mandatory driver adapter in the constructor**; `new PrismaClient()` with no adapter throws during DI resolution |
| Read one | `repo.findOneBy({ id })` | `findUnique` accepts **only `@id`/`@unique`** fields — `findFirst` is the general analogue |
| Get-or-404 | `findOneByOrFail` | `findUniqueOrThrow` throws `PrismaClientKnownRequestError` (P2025), not `NotFoundException` — convert explicitly |
| Module | `TypeOrmModule.forFeature([E])`, **re-exported** if another module injects it | `PrismaModule` provides **and exports** `PrismaService`; feature modules import it |
| DTOs | Entity decorators | Prisma model types are **not classes** and cannot be `@Body()` DTOs; hand-written class DTOs are still required |
| Spec mock | `getRepositoryToken(E)` as the provider token | Nested delegate object under `PrismaService` |
| Migrations | `migration:generate` + standalone DataSource | `prisma migrate dev` |

## TypeORM 1.x — what breaks in inherited templates

- `relations: ['profile']` and string-array `select` are removed → `{ profile: true }`
- `undefined` in `where` now throws (opt out via `invalidWhereValuesBehavior`)
- Removed: `findByIds`, `findOneById`, `exist`, `@EntityRepository`, `getCustomRepository`, `AbstractRepository`
- `@Column({ readonly: true })` → `@Column({ update: false })`
- Relations with `nullable: false` emit INNER JOIN, not LEFT JOIN

## Prisma 7 — client construction

`onModuleInit`/`$connect()` is the Prisma 6 form and is no longer the official
recipe. Prisma 7 passes an adapter to `super()`:

```ts
@Injectable()
export class PrismaService extends PrismaClient {
  constructor() {
    const adapter = new PrismaBetterSqlite3({ url: process.env.DATABASE_URL });
    super({ adapter });
  }
}
```

Detect which `@prisma/adapter-*` is installed — pg, better-sqlite3, mariadb,
neon, planetscale. **If none is installed, stop and ask.** Do not guess an
adapter.
```

- [ ] **Step 2: Verify against the live fixture**

```bash
grep -E '"@prisma/(client|adapter-[a-z0-9]+)"' /Users/christoffer/Privat/cb/epicly-aos/backend/package.json
grep -n "output" /Users/christoffer/Privat/cb/epicly-aos/backend/prisma/schema.prisma 2>/dev/null || echo "no output block - Prisma 6 style generator"
```
Record what the real project has; if it contradicts this file, the file is wrong and must be corrected before committing.

- [ ] **Step 3: Budget check and commit**

```bash
wc -l skills/nest/references/orm.md   # expect <= 150
git add skills/nest/references/orm.md
git commit -m "Add nest ORM reference for TypeORM 1.x and Prisma 7

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 15: `references/version-matrix.md`

**Files:**
- Create: `skills/nest/references/version-matrix.md`

- [ ] **Step 1: Write the matrix**

No major is named as a default. Absolute dates and version numbers stay in the
spec; they rot here.

```markdown
# Nest v11 → v12

Contents: what `require(esm)` does and does not cover · delta table · ESM authoring rules

## What `require(esm)` covers

Package **consumption** only: a CommonJS app can upgrade to v12 and stay
CommonJS. v11 output is source-compatible on v12 for **controllers, services,
and DTOs specifically**. Config, custom pipes, logging assertions, and CLI
config diverge regardless.

## Deltas

| Area | v12 |
|---|---|
| Validation | Standard Schema via `schema` on `@Body()`/`@Query()`/`@Param()`/`@RawBody()`, alongside class-validator. **Requires `StandardSchemaValidationPipe` registered** — without it the decorator attaches metadata and validates nothing. Response side: `StandardSchemaSerializerInterceptor` + `@SerializeOptions({ schema })` |
| `@nestjs/config` | Standard Schema; Joi >= 18 with settings under `validationOptions.libraryOptions`. Gate on the **config** major, which peers `^11 \|\| ^12` |
| Pipes | `ArgumentMetadata` is generic |
| Lifecycle | Hooks invoked by component hierarchy level |
| Exceptions | `HttpExceptionOptions.errorCode` |
| Logging | Structured params default-on; `structuredParams: false` restores |
| Routing | `routeConflictPolicy`, `routeResolutionStrategy: 'specificity'` |
| Decorators | `Reflector.createDecorator()` preferred over `SetMetadata`. Mixing `createDecorator` with `SetMetadata` string keys returns `undefined` |
| Generated projects | **oxlint for all** generated projects, not just ESM. Vitest only for ESM; CommonJS keeps Jest |
| Swagger | The CLI plugin is a `tsc` transformer and **does not run under Vitest/SWC**, the ESM default. Requires `PluginMetadataGenerator` + `SwaggerModule.loadPluginMetadata()`, or DTOs document as empty schemas |
| Monorepo | Rspack is the default bundler; `webpack` options in `nest-cli.json` are deprecated |
| Node | v20.19+/v22.12+ to run; **v22.22.3+/v24.15+/v26+ for the CLI**. The `engines` field says `>= 20` and understates both |
| Ecosystem | Every `@nestjs/*` moves major together; `@nestjs/graphql` went to 14 |

## ESM authoring

Generated ESM code that ignores these does not run:

- Relative imports carry a `.js` extension, even from `.ts`: `'./app.module.js'`
- `__dirname` and `__filename` do not exist → `import.meta.dirname`
- `require()` is unavailable → `createRequire(import.meta.url)`
- The TypeORM entity glob (`dist/**/*.entity{.ts,.js}`) breaks — it depends on `__dirname`
```

- [ ] **Step 2: Budget check and commit**

```bash
wc -l skills/nest/references/version-matrix.md   # expect <= 120
git add skills/nest/references/version-matrix.md
git commit -m "Add nest v11-v12 version matrix

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 16: `references/resource.md`

**Files:**
- Create: `skills/nest/references/resource.md`

- [ ] **Step 1: Write the CRUD scaffold and Swagger annotation procedures**

Cover both modes — they share a decorator set; only the workflow differs
(write new vs annotate existing).

Include, each stated **once**, only if it survived Task 6:
- DTOs are classes, value-imported (`import type` erases the class and
  `ValidationPipe` then validates nothing)
- `whitelist: true` silently strips any property lacking a validator
- `PartialType` from `@nestjs/swagger` when Swagger is present, **because**
  the `@nestjs/mapped-types` version does not re-apply `ApiProperty` and the
  update DTO renders as an empty schema — same for `PickType`, `OmitType`,
  `IntersectionType`
- `@Get(':id')` shadows `@Get('search')` when declared first
- `ParseUUIDPipe` for UUID keys, `ParseIntPipe` for integer keys
- Swagger CLI plugin detection via `nest-cli.json` — skip redundant
  `@ApiProperty` when the plugin is active, and see `version-matrix.md` for
  the Vitest/SWC caveat

Reference `orm.md` for the ORM fork rather than restating it.

- [ ] **Step 2: Budget check and commit**

```bash
wc -l skills/nest/references/resource.md   # expect <= 250
git add skills/nest/references/resource.md
git commit -m "Add nest resource and swagger reference

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 17: `references/auth.md`

**Files:**
- Create: `skills/nest/references/auth.md`

- [ ] **Step 1: Write the auth scaffold**

File set: `auth.module.ts`, `auth.service.ts`, `auth.controller.ts`,
`strategies/local.strategy.ts`, `strategies/jwt.strategy.ts`,
`guards/jwt-auth.guard.ts`, `guards/local-auth.guard.ts`,
`decorators/public.decorator.ts`, `dto/login.dto.ts`.

Rules stated here, once each (subject to Task 6 survival):
- `forwardRef()` on both sides of the `AuthModule` ↔ `UsersModule` cycle —
  this is the default shape and the default failure
- `JwtModule.registerAsync` with `ConfigService`, never `register` with a literal
- Guards throw `UnauthorizedException` for 401; `return false` yields 403
- When a global guard is chosen, generate the `@Public()` opt-out alongside it

The password-exclusion mechanism lives in `SKILL.md` hard rule 3 — reference
it, do not restate it.

- [ ] **Step 2: Budget check and commit**

```bash
wc -l skills/nest/references/auth.md   # expect <= 200
git add skills/nest/references/auth.md
git commit -m "Add nest auth reference

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 18: `references/testing.md`

**Files:**
- Create: `skills/nest/references/testing.md`

- [ ] **Step 1: Write the spec generator procedure**

Cover service, controller, and e2e specs, with the Jest ↔ Vitest identifier
mapping as a table rather than duplicated templates.

Rules stated here, once each:
- `getRepositoryToken(Entity)` as the provider token, not the `Repository`
  class — the most common reason a generated testing module fails to compile
- Prisma's equivalent token is `PrismaService`, mocked as a nested delegate object
- `app.useGlobal*()` bindings from `main.ts` do **not** apply to
  `Test.createTestingModule`, so e2e tests silently run without the global
  `ValidationPipe` — `APP_PIPE` does apply
- `await app.close()` in `afterAll`, or the runner hangs on open handles
- Never emit `should be defined` as a spec's only test
- Under Vitest, `supertest` may need a default import (see Open Issue 4 in the spec — verify before writing)

- [ ] **Step 2: Verify the Vitest fixture's runner**

```bash
grep -E '"(test|vitest|jest)"' /Users/christoffer/Privat/cb/doculogic/backend/package.json
```
Expected: `vitest` present, `jest` absent — confirming the detection branch.

- [ ] **Step 3: Budget check and commit**

```bash
wc -l skills/nest/references/testing.md   # expect <= 200
git add skills/nest/references/testing.md
git commit -m "Add nest testing reference

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 19: `references/pipeline.md`

**Files:**
- Create: `skills/nest/references/pipeline.md`

- [ ] **Step 1: Write guard, interceptor, pipe, filter, and decorator procedures**

Rules stated here, once each:
- `APP_*` providers over `app.useGlobal*()` for anything needing DI — but
  `app.useGlobalPipes(new ValidationPipe())`, `setGlobalPrefix`, `enableCors`,
  `enableVersioning` are legitimate and must not be rewritten. Registering
  both ways runs the pipe **twice**
- `Reflector.getAllAndOverride(Key, [context.getHandler(), context.getClass()])`
  in that order — **the failure is privilege escalation**: with
  `getAllAndMerge`, a class marked `@Roles('admin')` and a method marked
  `@Roles('user')` yields both, so a method meant to narrow access widens it.
  Reversing the array lets class metadata override the method
- Prefer `@UseFilters(FilterClass)` over an instance for DI and reuse — a
  preference, not a prohibition; instances are legitimate when the filter
  takes constructor arguments
- Middleware calls `next()` or sends a response
- Class middleware needs DI → apply via `MiddlewareConsumer`, not `app.use()`

On v12, see `version-matrix.md` for `Reflector.createDecorator()` and the
generic `ArgumentMetadata`.

- [ ] **Step 2: Budget check and commit**

```bash
wc -l skills/nest/references/pipeline.md   # expect <= 200
git add skills/nest/references/pipeline.md
git commit -m "Add nest pipeline reference

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 20: `references/infrastructure.md`

**Files:**
- Create: `skills/nest/references/infrastructure.md`

- [ ] **Step 1: Write bootstrap, config, migrations, and queues**

Four concerns, one file, because all four edit bootstrap and wiring.

- **`main.ts`**: `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })`,
  global prefix, CORS, `process.env.PORT ?? 3000`, Express vs Fastify
- **`ConfigModule`**: `isGlobal`, validation schema as the startup gate,
  typed namespaces, `.env.example`. See `SKILL.md` hard rule 5
- **Migrations**: TypeORM standalone DataSource — **`autoLoadEntities` does
  not exist here**; the DataSource runs outside Nest's DI and must list
  entities explicitly, with `synchronize: false`. Prisma: `prisma migrate dev`
- **Queues**: BullMQ. Detect `@nestjs/bullmq` vs the older `@nestjs/bull` —
  **different APIs**; do not assume. Processors, queue registration, DI in
  workers, failure handling

`autoLoadEntities: true` applies **only inside Nest**, and misses entities
reachable only through relations. State it here once; do not restate in
`resource.md`.

- [ ] **Step 2: Budget check and commit**

```bash
wc -l skills/nest/references/infrastructure.md   # expect <= 250
git add skills/nest/references/infrastructure.md
git commit -m "Add nest infrastructure reference

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

## Phase 5 — GREEN verification

### Task 21: Re-run the RED prompts with the skill installed

**Files:**
- Create: `docs/superpowers/plans/green-results.md`

- [ ] **Step 1: Reinstall the current skill**

```bash
rm -rf ~/.claude/skills/nest && cp -r skills/nest ~/.claude/skills/ && ls ~/.claude/skills/nest/references
```
Expected: all seven reference files listed.

- [ ] **Step 2: Re-run every prompt that produced an OBSERVED-FAIL**

Use the identical prompts and the identical fixture-safety protocol from
Tasks 2–5. For each rule marked OBSERVED-FAIL in `red-results.md`, re-run its
grep and record PASS or STILL-FAILING.

- [ ] **Step 3: Verify the module graph actually compiles**

On F-PRISMA, after the resource run:

```bash
cd /Users/christoffer/Privat/cb/epicly-aos/backend && npx tsc --noEmit 2>&1 | tail -20
```
Expected: no new errors beyond the pre-write baseline recorded in Task 2.

- [ ] **Step 4: Handle regressions**

Any STILL-FAILING rule means the rule is stated in a place the model does not
reach, or is stated too weakly. Move it closer to the template it governs, or
strengthen it to name the mechanism. Re-run. **Do not proceed with a
STILL-FAILING security rule (hard rules 1–5).**

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/green-results.md
git commit -m "GREEN: nest skill fixes observed RED failures

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

## Phase 6 — Repo wiring

### Task 22: `skills/nest/README.md`

**Files:**
- Create: `skills/nest/README.md`

- [ ] **Step 1: Write it in the house shape**

Sections, matching both siblings: `# nest` → tagline → `## What it does` →
`## What it enforces` → `## Scope` → `## Install` → `## Usage`.

The install block is reproduced verbatim from the siblings:

```markdown
## Install

See the [repository README](../../README.md) for the plugin install.

To copy this skill directly instead:

```bash
# personal, all projects
mkdir -p ~/.claude/skills && cp -r skills/nest ~/.claude/skills/

# project-local, shared via git
mkdir -p .claude/skills && cp -r skills/nest .claude/skills/
```

Both are safe to re-run to update an existing copy.
```

- [ ] **Step 2: Add the CLAUDE.md trigger snippet**

A technology skill's description is matched before any file is read, so
description-based triggering is best-effort. This is the reliable trigger:

```markdown
## Reliable triggering

The skill fires on NestJS vocabulary, and on plain requests like "add an
endpoint for orders" once it sees `@nestjs/core` in your project. To make it
certain, add this to your project's `CLAUDE.md`:

> This is a NestJS project. Use the `nest` skill for any server-side code
> change — resources, auth, guards, specs, config, migrations, queues.
```

- [ ] **Step 3: Budget check and commit**

```bash
wc -l skills/nest/README.md   # expect <= 80
git add skills/nest/README.md
git commit -m "Add nest skill README

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

### Task 23: Marketplace and plugin wiring

**Files:**
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.claude-plugin/plugin.json`
- Modify: `README.md`

Git history (`d273b14`) shows these two JSON files edited in lockstep with
character-identical description and version changes.

- [ ] **Step 1: Edit both descriptions identically**

Append to the existing sentence in **both** files:

`"; nest scaffolds NestJS resources, auth, and tests against your project's own stack."`

- [ ] **Step 2: Bump both versions**

`1.1.0` → `1.2.0` in both. History shows one minor bump per skill added.

- [ ] **Step 3: Add keywords to both**

Add `nest`, `nestjs`, `typeorm`, `prisma`.

**Preserve the pre-existing asymmetry:** `plugin.json` carries `productivity`
and `marketplace.json` does not. Do not normalise it — that is an unrelated
change.

- [ ] **Step 4: Add the README table row**

```markdown
| [nest](skills/nest/README.md) | Scaffolds NestJS resources, auth, guards, and specs matched to your project's actual Nest, ORM, and test-runner versions — then verifies the result compiles and its module graph resolves. |
```

- [ ] **Step 5: Validate the JSON**

```bash
node -e "JSON.parse(require('fs').readFileSync('.claude-plugin/marketplace.json'));JSON.parse(require('fs').readFileSync('.claude-plugin/plugin.json'));console.log('both parse')"
```
Expected: `both parse`

- [ ] **Step 6: Confirm the descriptions match exactly**

```bash
diff <(node -p "require('./.claude-plugin/marketplace.json').plugins[0].description") \
     <(node -p "require('./.claude-plugin/plugin.json').description") && echo "descriptions identical"
```
Expected: `descriptions identical`

- [ ] **Step 7: Commit**

```bash
git add .claude-plugin/marketplace.json .claude-plugin/plugin.json README.md
git commit -m "Wire nest skill into marketplace and plugin manifests

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
```

---

## Phase 7 — Close out

### Task 24: Remove the dead MCP entry

**Files:**
- Modify: `~/.claude.json`

Independent of this work and safe now — it points at
`/Users/christoffer/Privat/cb/NestJS/build/index.js`, a deleted directory, and
fails to connect every session.

- [ ] **Step 1: Confirm the target is really gone**

```bash
ls /Users/christoffer/Privat/cb/NestJS 2>&1
```
Expected: `No such file or directory`

- [ ] **Step 2: Back up before editing**

```bash
cp ~/.claude.json ~/.claude.json.bak-$(date +%Y%m%d)
```

- [ ] **Step 3: Remove the `nestjs-claude-plugin` key from `mcpServers`, then validate**

```bash
node -e "JSON.parse(require('fs').readFileSync(process.env.HOME+'/.claude.json'));console.log('parses')"
grep -c "nestjs-claude-plugin" ~/.claude.json || echo "entry removed"
```
Expected: `parses`, then `entry removed`

---

### Task 25: Retire the slash command

**Files:**
- Delete: `~/.claude/commands/nest.md`

**Gated on Task 8 and Task 21 both passing.** Do not delete a working artifact
in the same change that ships its replacement.

- [ ] **Step 1: Confirm the gates**

Verify `trigger-results.md` shows must-fire and must-not-fire passing, and
`green-results.md` shows no STILL-FAILING security rule.

- [ ] **Step 2: Archive rather than delete outright**

```bash
mv ~/.claude/commands/nest.md ~/.claude/commands/nest.md.retired-$(date +%Y%m%d)
ls ~/.claude/commands/ | grep nest
```
Expected: only the `.retired-` file listed.

---

### Task 26: Record limitations and merge

**Files:**
- Modify: `docs/superpowers/specs/2026-09-02-nest-skill-design.md`

- [ ] **Step 1: Update Open Issues with what testing actually established**

Resolve issues that RED/GREEN settled. For the rest, record honestly:

- **No Nest v12 fixture exists locally.** The v12 path in
  `version-matrix.md` is written from primary sources and is untested against
  real code.
- **No TypeORM 1.x fixture exists locally.** Same status. The local TypeORM
  project is 0.3.26.
- **Monorepo write paths are untested.** No Nest monorepo (`nest-cli.json`
  with `projects`) was available.

- [ ] **Step 2: State the limitations in the skill README too**

Users should know which paths are verified and which are not.

- [ ] **Step 3: Commit and merge**

```bash
git add -A
git commit -m "Record nest skill testing limitations

Claude-Session: https://claude.ai/code/session_01BmcLxhDBo1Trp3CQhsSWh3"
git checkout main && git merge --no-ff nest-skill
```

- [ ] **Step 4: Verify the marketplace still resolves from main**

```bash
node -e "const m=require('./.claude-plugin/marketplace.json');console.log(m.version, m.plugins[0].keywords.join(','))"
ls skills/
```
Expected: `1.2.0` with nest keywords, and three skill folders.

---

## Self-review

**Spec coverage:** every spec section maps to a task — editorial rule → Task 6
and Task 12; structure → Tasks 7–20; CLI relationship → Task 11 (write paths,
`app.module.ts` edit); frontmatter → Task 7; detection → Task 9; routing →
Task 10; verify → Task 11; hard rules → Task 12; ESM → Task 15; ORM → Task 14;
version handling → Task 15; testing → Tasks 1–6, 8, 21; repo wiring → Tasks
22–23; cleanup → Tasks 24–25; open issues → Task 26.

**Placeholders:** none. Tasks 16–20 describe file contents by listing the
exact rules each must carry and where each is single-sourced, rather than
reproducing full code templates — the templates are generated from those rules
during execution, and the rule list is fixed by Task 6.

**Type consistency:** rule IDs R1–R21 are used identically in Tasks 1, 2–5, 6,
and 21. Fixture IDs F-PRISMA, F-TYPEORM, F-SWAGGER, F-VITEST, F-V10 are used
identically throughout. File paths and line budgets match the File Structure
table.

**Known ordering dependency:** Task 6 gates Tasks 12 and 16–20 — the rule set
cannot be written before RED prunes it. Task 8 and Task 21 gate Task 25.
