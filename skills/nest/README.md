# nest

A Claude Code skill for NestJS work. It supplies the two things reading your project cannot: which package majors you are actually on, and a verification step that catches the failures a typecheck cannot see.

## What it does

Three steps, on every invocation:

1. **Detects** your stack from resolved versions rather than the ranges in `package.json` — Nest, `@nestjs/config`, TypeORM, Prisma, module format, test runner, and monorepo layout.
2. **Loads version deltas** only when they apply: NestJS v12 changes if you are on v12, ORM major changes if you have an ORM. Otherwise it stays out of the way.
3. **Verifies** what it wrote — baselines the typecheck first, then compiles the module graph.

## What it deliberately does not do

It does not teach NestJS idiom, because Claude already knows it.

That is not an assumption. Before this skill was written, four baseline runs against real NestJS projects recorded what Claude produces unaided. Of twenty-one candidate rules, fourteen passed and one failed. Claude independently used `getRepositoryToken` in spec providers, read a Prisma generator's `output` block to find the right import path, chose `findFirst` over `findUnique` for a non-unique lookup, imported `PartialType` from `@nestjs/swagger`, applied `ParseUUIDPipe` to uuid keys, kept `synchronize: false`, and kept the password hash out of both responses and the JWT payload.

Shipping rules for any of that would cost context on every invocation and change nothing. So this skill ships one rule, not twenty.

## Where Claude actually fails

The same baseline asked a tools-disabled model five version questions:

| Question | Answer |
| --- | --- |
| Latest NestJS major? | *"no reliable knowledge of a NestJS 12 release"* |
| v12 Standard Schema with Zod? | *"I won't invent a decorator name or a registration step"* |
| v12 `@nestjs/config` changes? | *"I won't guess at a migration step"* |
| TypeORM latest major? | *"TypeORM has never left `0.x`"* — labelled CERTAIN |
| Is string-array `relations` removed? | *"the array form was not removed"* — labelled CERTAIN |

The last two are false, and that is the more dangerous shape. Missing knowledge produces a refusal you notice; confident wrongness produces code you ship.

## The one rule it enforces

Required environment variables belong in the `ConfigModule` validation schema. `getOrThrow` throws at call time, not startup — a key read inside a request handler boots green and dies on first traffic. This was the single candidate rule that failed the baseline.

## Verification

A Nest module graph resolves at runtime, so a module missing from `imports` typechecks clean and throws on boot. The skill therefore baselines the typecheck before writing (so pre-existing errors are not mistaken for its own), re-runs it after, then compiles the module graph with `Test.createTestingModule`. Repairs are capped at two attempts and confined to files it wrote. It reports "compiles" and "module graph resolves" — never "works".

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

## Usage

Describe the change you want. The skill fires on NestJS vocabulary, and on plain requests like "add an endpoint for orders" once it sees `@nestjs/core` in your project.

A skill description is matched before any file is read, so that second path is best-effort. To make it certain, add this to your project's `CLAUDE.md`:

> This is a NestJS project. Use the `nest` skill for any server-side code change.

## Scope

NestJS server-side code only. Not general TypeScript, Express, or Fastify work. For deciding *whether* to build something rather than how, see [design-doc](../design-doc/README.md).

## What is verified

The TypeORM 1.x path, triggering, conditional reference loading, and resolved-version detection were all exercised against a fixture before release. The NestJS v12 and Prisma 6→7 content is verified against the release notes, the official migration guide, and the shipped type declarations — but **not against a real project**, because no v12 or Prisma-8 codebase was available to test on. Monorepo write paths are likewise unexercised.

Treat those three as the parts most likely to need correction, and report anything that looks wrong.
