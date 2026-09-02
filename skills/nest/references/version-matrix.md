# NestJS v12 deltas

Contents: `nest upgrade` · what `require(esm)` covers · Standard Schema validation & serialization · @nestjs/config gating · custom pipes · lifecycle order · error codes · structured logging · route diagnostics · metadata decorators · generated-project defaults · Swagger CLI plugin · Node floors · ecosystem majors · ESM authoring rules.

Your training predates v12. For anything below, emit what is here — do not reconstruct v12 APIs from v11 recall. Everything not listed is unchanged from v11.

---

## Prefer `nest upgrade` over hand-migration

```bash
npm i -g @nestjs/cli@latest @nestjs/schematics@latest   # global CLI first — the command ships with it
nest upgrade --dry-run                                  # then without the flag
```
It moves every `@nestjs/*` package to its v12-compatible major at once and applies the mechanical parts: `nest-cli.json` webpack options → rspack, GraphQL `playground` → `graphiql` and `subscriptions-transport-ws` → `graphql-ws`, `nats` → `@nats-io/transport-node`, and the `@nestjs/config` `validationOptions.libraryOptions` move with a Joi bump to 18. It deliberately does **not** convert the project to ESM, Vitest, or oxlint.

## What `require(esm)` covers — and does not

v12 packages ship ESM-only. A CommonJS app consumes them through `require(esm)` and can upgrade **and stay CommonJS**; `nest upgrade` leaves the module format alone. Converting your own code to ESM is optional and not part of the upgrade.

That is package consumption only — it does **not** mean v11 idioms still hold. These diverge in a CommonJS v12 app just as much as an ESM one, so emit the v12 form regardless of module format: custom pipes (`ArgumentMetadata` generic) · providers whose ordering depends on lifecycle hooks · `ConsoleLogger` call sites · `@nestjs/config` validation.

## Standard Schema validation (additive, not a replacement)

`@Body()`, `@Query()`, `@Param()`, `@RawBody()` accept a `schema` option (`ParameterDecoratorOptions = { schema?, pipes? }`) for Standard Schema libraries (Zod, Valibot, ArkType):

```ts
@Post() create(@Body({ schema: createUserSchema }) body: CreateUserDto) {}
@Get(':id') findOne(@Param('id', { schema: z.coerce.number().int().positive() }) id: number) {}
```

**The decorator only attaches metadata.** Without a registered `StandardSchemaValidationPipe` it silently does not validate — no error, no warning, unvalidated input reaches the handler. If you emit a `schema` option anywhere, emit `app.useGlobalPipes(new StandardSchemaValidationPipe());` in the same change.

Response side: `@UseInterceptors(StandardSchemaSerializerInterceptor)` with `@SerializeOptions({ schema: userResponseSchema })`.

`ValidationPipe` + class-validator and `ClassSerializerInterceptor` remain fully supported with no removal planned. Do not rewrite existing class-based DTOs to schemas unasked; use `schema` when the project already uses a schema library.

## @nestjs/config — gate on the config package, not core

`validationSchema` accepts any Standard Schema (Zod recommended for new code). Keeping Joi requires **Joi >= 18** (the first release implementing Standard Schema), and library-specific settings move down a level:

```ts
// v11: validationOptions: { allowUnknown: false, abortEarly: true }
validationOptions: { libraryOptions: { allowUnknown: false, abortEarly: true } }
```
For Joi, `@nestjs/config` keeps its historical `allowUnknown: true` / `abortEarly: false` defaults and merges yours on top.

**Version gate.** `@nestjs/config` jumped from the 4.x line straight to 12.x, and its peer range is `^11.0.0 || ^12.0.0` — spanning two Nest majors. A v11 app may already be on config 12, and a v12 app may still be on config 4. Decide from `node -p "require('@nestjs/config/package.json').version"`, never from `@nestjs/core`.

## Custom pipes

`ArgumentMetadata<Metatype = any>` is generic, and carries `readonly schema?: StandardSchemaV1` alongside `type`/`metatype`/`data`. The default keeps v11 pipes compiling; hand-written signatures that name the type explicitly may need the parameter added.

## Lifecycle hook ordering

Hooks are invoked **by component hierarchy level**. Relative order of `onModuleInit`, `onApplicationBootstrap`, and shutdown hooks between interdependent providers or modules can differ from v11. Never generate code whose correctness depends on one provider's hook running before another's — do the work in the dependent provider's own hook, or inject and await explicitly.

## Machine-readable error codes

`HttpExceptionOptions` accepts `errorCode`, serialized into the response body so clients branch on an identifier rather than the message string: `throw new BadRequestException('Password is too weak', { errorCode: 'WEAK_PASSWORD' });`

## Structured logging params

`ConsoleLogger` treats a plain object after the message as structured params on the same log entry rather than a separate record — `logger.log('User created', { userId: 1, email: 'foo@bar.com' })`. JSON mode nests them under `params`, or spreads them into the root with `flattenParams: true`. On by default; `structuredParams: false` restores v11 behaviour. **This breaks tests that assert on log output** — a v11 suite expecting two records now sees one.

## Route conflict diagnostics (opt-in, defaults unchanged)

```ts
NestFactory.create(AppModule, {
  routeConflictPolicy: { duplicate: 'error', shadow: 'warn' },
  routeResolutionStrategy: 'specificity',   // default 'declaration'
});
```
`'specificity'` registers literal segments before parametric/wildcard ones on order-sensitive adapters (Express). Worth suggesting whenever you generate a controller carrying both `@Get('me')` and `@Get(':id')`.

## Metadata decorators

The `decorator` schematic emits `Reflector.createDecorator()`; prefer it over `SetMetadata`. **Mixing the two silently returns `undefined`.** `createDecorator()` generates a random metadata key (`uid(21)`) unless you pass `{ key: 'roles' }`. So `reflector.get('roles', handler)` against a `createDecorator` decorator yields `undefined`, and so does `reflector.get(Roles, handler)` against `@SetMetadata('roles', …)`. Pick one form per decorator and read it back by decorator reference, not by string.

## Generated-project defaults

`nest new` prompts for CommonJS or ESM.
- **oxlint is the default linter for all generated projects** — both variants.
- **Vitest is the default test runner for ESM projects only**; CommonJS projects keep Jest. (`tsconfig` `types` is the only difference: `["vitest/globals", "node"]` vs `["node", "jest"]`.)
- Rspack is the default monorepo bundler. `--webpack` / `--webpackPath`, and `webpack` / `webpackConfigPath` in `nest-cli.json`, are deprecated in favour of `--builder rspack` (`--rspackPath` replaces the path flag). The `angular` schematic is removed; `bun` is a supported package manager.

## Swagger CLI plugin does not run outside tsc

`@nestjs/swagger/plugin` is a **tsc AST transformer**. Vitest, `@swc/jest`, `ts-jest`, and the SWC builder compile without it, so no `@ApiProperty` metadata is synthesised and **DTOs document as empty schemas**. Since ESM projects default to Vitest, this bites by default there.
- SWC, standard (non-monorepo) setup: `nest start -b swc --type-check` runs the plugin.
- Otherwise run `PluginMetadataGenerator` (`@nestjs/cli/lib/compiler/plugins/plugin-metadata-generator`, with `ReadonlyVisitor` from `@nestjs/swagger/dist/plugin`) to emit `metadata.ts`, then `await SwaggerModule.loadPluginMetadata(metadata)` before `SwaggerModule.createDocument(app, config)`.
- In ESM projects set the plugin option `esmCompatible: true`.

## Node floors — the `engines` field understates both

| Task | Minimum Node |
| --- | --- |
| Running a v12 app | **20.19+**, or **22.12+** on the 22.x line |
| `nest new` / `nest generate` / `nest upgrade` (`@nestjs/schematics`) | **22.22.3+**, **24.15+**, or **26+** |

21.x never got unflagged `require(esm)` and is unsupported; 23.x, 25.x and early 24.x are excluded from the CLI floor. `@nestjs/core` still declares `>= 20` and `@nestjs/cli` `>= 20.11` — both understate the real requirement, so do not read the floor off `engines`. `nest upgrade` refuses to run on an older release.

## Ecosystem majors move together

Every `@nestjs/*` package advances to its v12-compatible major at once — never pin a v11-era major alongside core 12. The majors are not all the same number: `@nestjs/graphql`, `@nestjs/apollo`, and `@nestjs/mercurius` go to **14**, and `@nestjs/config` to **12** from its 4.x line.

## ESM authoring rules (only when `package.json` has `"type": "module"`)

Generated code fails at runtime without these:
- Relative imports carry a **`.js` extension even in `.ts` sources** — `import { AppModule } from './app.module.js'`. The specifier names the emitted file.
- `__dirname` / `__filename` do not exist. Use `import.meta.dirname` (or `fileURLToPath(import.meta.url)`).
- `require()` does not exist. Build one with `createRequire(import.meta.url)` from `node:module`.
- **The TypeORM entity glob breaks** for exactly that reason: `entities: [__dirname + '/**/*.entity{.ts,.js}']` has no `__dirname`. Emit `autoLoadEntities: true` (picks up everything registered via `forFeature()`) or rebuild the path from `import.meta.dirname`.
- `tsconfig.json` needs `"module": "nodenext"`, `"moduleResolution": "nodenext"`, `"resolvePackageJsonExports": true`, `"target": "ES2023"`. v11-generated projects already have the first two, so adding `"type": "module"` is the whole switch.
- Under Vitest, import supertest as a default import: `import request from 'supertest'`.
