# NestJS v12 deltas

Contents: `nest upgrade` · what `require(esm)` covers · Standard Schema validation & serialization · ValidationPipe `errorFormat` · @nestjs/config gating · custom pipes · `@Optional()` · lifecycle order · error codes · structured logging · route diagnostics · metadata decorators · v12.1 built-ins · Terminus · BullMQ · generated-project defaults · Swagger CLI plugin · Node floors · ecosystem majors · ESM authoring rules.

Your training predates v12. For anything below, emit what is here — do not reconstruct v12 APIs from v11 recall. Each `→ /path.md` names the chapter to fetch from `https://docs.nestjs.com` when you need more than the trap stated here.

---

## Prefer `nest upgrade` over hand-migration

```bash
npm i -g @nestjs/cli@latest @nestjs/schematics@latest   # global CLI first — the command ships with it
npm i -D @nestjs/cli@latest @nestjs/schematics@latest   # and locally, if the project pins the CLI
nest upgrade --dry-run --no-observe                      # then without --dry-run
```
It moves every recognized `@nestjs/*` package to its v12-compatible major at once, bumps TypeScript to 6 and Jest to 30 where present, raises `engines.node`, flags tsconfig settings TypeScript 6 dropped (legacy `moduleResolution`, missing `rootDir`), and applies the mechanical parts: `nest-cli.json` webpack options → rspack, GraphQL `playground` → `graphiql` and `subscriptions-transport-ws` → `graphql-ws`, `nats` → `@nats-io/transport-node`, and the `@nestjs/config` `validationOptions.libraryOptions` move. It deliberately does **not** convert the project to ESM, Vitest, or oxlint. Pass `--observe` or `--no-observe`: without either, a TTY prompts and a non-TTY run skips Observe. → `/cli/usages.md`

## What `require(esm)` covers — and does not

v12 packages ship ESM-only. A CommonJS app consumes them through `require(esm)` and can upgrade **and stay CommonJS**; `nest upgrade` leaves the module format alone. Converting your own code to ESM is optional and not part of the upgrade.

That is package consumption only — it does **not** mean v11 idioms still hold. These diverge in a CommonJS v12 app just as much as an ESM one, so emit the v12 form regardless of module format: custom pipes (`ArgumentMetadata` generic) · `@Optional()` in subclasses · providers whose ordering depends on lifecycle hooks · `ConsoleLogger` call sites · `@nestjs/config` validation.

## Standard Schema validation (additive, not a replacement)

`@Body()`, `@Query()`, `@Param()`, `@RawBody()` — plus `@MessageBody()`, `@Payload()`, and custom param decorators — accept a `schema` option for Standard Schema libraries (Zod, Valibot, ArkType):

```ts
@Post() create(@Body({ schema: createUserSchema }) body: CreateUserDto) {}
@Get(':id') findOne(@Param('id', { schema: z.coerce.number().int().positive() }) id: number) {}
```

**The decorator only attaches metadata.** Without a registered `StandardSchemaValidationPipe` (from `@nestjs/common`) it silently does not validate — no error, no warning, unvalidated input reaches the handler. If you emit a `schema` option anywhere, emit `app.useGlobalPipes(new StandardSchemaValidationPipe());` in the same change.

**Second silent trap: custom decorators.** The pipe skips `createParamDecorator` decorators unless constructed with `validateCustomDecorators: true` (default `false`). `@Headers()` takes no `schema` at all — validate a header through a custom decorator plus that flag.

- `transform` defaults to `true`: the handler receives the schema's *output*. With `false`, type the parameter as `z.input<typeof schema>`.
- There is no `whitelist`. Unknown keys are the schema's job: `z.object()` strips, `z.strictObject()` rejects, `z.looseObject()` keeps.
- Both pipes can be global together: `ValidationPipe` only validates class-typed parameters, `StandardSchemaValidationPipe` only those declaring a schema.

Response side: `@UseInterceptors(StandardSchemaSerializerInterceptor)` with `@SerializeOptions({ schema: userResponseSchema })`. Registered globally it needs the reflector: `new StandardSchemaSerializerInterceptor(app.get(Reflector))`. For a handler returning an array, pass the **item** schema — the interceptor applies it per element. A response that fails its schema becomes a **500**, not partial data. → `/application/validation.md`, `/application/serialization.md`

`ValidationPipe` + class-validator and `ClassSerializerInterceptor` remain fully supported with no removal planned. Do not rewrite existing class-based DTOs to schemas unasked; use `schema` when the project already uses a schema library.

## ValidationPipe `errorFormat`

New option, `'list'` (default) or `'grouped'`. `'grouped'` changes `message` from `string[]` to `Record<string, string[]>` — clients and e2e assertions that index into `message` break. Do not switch an existing API unasked.

## @nestjs/config — gate on the config package, not core

`validationSchema` accepts any Standard Schema (Zod recommended for new code; use `z.coerce.number()` — env vars arrive as strings, and `ConfigService` serves the schema's output). Keeping Joi requires **Joi >= 18**, and library-specific settings move down a level:

```ts
// v11: validationOptions: { allowUnknown: false, abortEarly: true }
validationOptions: { libraryOptions: { allowUnknown: false, abortEarly: true } }
```
For Joi, `@nestjs/config` keeps its historical `allowUnknown: true` / `abortEarly: false` defaults and merges yours on top.

**Version gate.** `@nestjs/config` jumped from the 4.x line straight to 12.x, and its peer range is `@nestjs/common ^11.0.0 || ^12.0.0` — spanning two Nest majors. A v11 app may already be on config 12, and a v12 app may still be on config 4. Decide from `node -p "require('./node_modules/@nestjs/config/package.json').version"`, never from `@nestjs/core`. → `/application/configuration.md`

## Custom pipes

`ArgumentMetadata<Metatype = any>` is generic, and carries `readonly schema?: StandardSchemaV1` alongside `type`/`metatype`/`data`. Hand-written signatures that name the type explicitly may need the parameter added. (The `/pipes` chapter still shows the non-generic form; the migration guide and the shipped types are current.)

## `@Optional()` is no longer inherited

Optional markers are read with `Reflect.getOwnMetadata`, so a subclass does not inherit its parent's. A subclass whose parent marks a constructor parameter `@Optional()` must declare its own constructor and repeat the marker, or Nest throws `UnknownDependenciesException` when the dependency is absent.

## Lifecycle hook ordering

Hooks run module by module, by distance from the root in the import graph: the most deeply imported modules (and global modules) first, the root module last; shutdown hooks run in reverse. Relative order between interdependent providers can differ from v11. Never generate code whose correctness depends on one provider's hook running before another's — do the work in the dependent provider's own hook, or inject and await explicitly. → `/fundamentals/lifecycle-events.md`

## Machine-readable error codes

`HttpExceptionOptions` accepts `errorCode`, serialized into the response body so clients branch on an identifier rather than the message string: `throw new BadRequestException('Password is too weak', { errorCode: 'WEAK_PASSWORD' });`. From the shipped source, not the docs: when the first argument is an **object**, that object is the body as-is and `errorCode` is dropped — put the code inside the object instead.

## Structured logging params

`ConsoleLogger` treats a plain object after the message as structured params on the same log entry rather than a separate record — `logger.log('User created', { userId: 1, email: 'foo@bar.com' })`. JSON mode nests them under `params`, or spreads them into the root with `flattenParams: true`. On by default; `structuredParams: false` restores v11 behaviour. **This breaks tests that assert on log output** — a v11 suite expecting two records now sees one.

## Route conflict diagnostics (opt-in, defaults unchanged)

```ts
NestFactory.create(AppModule, {
  routeConflictPolicy: { duplicate: 'error', shadow: 'warn' },
  routeResolutionStrategy: 'specificity',   // default 'declaration'
});
```
`'specificity'` registers literal segments before parametric/wildcard ones on order-sensitive adapters (Express; Fastify already ranks by specificity). `'error'` aggregates every offending pair into one `RouteConflictException` at init. Worth suggesting whenever you generate a controller carrying both `@Get('me')` and `@Get(':id')`.

## Metadata decorators

The `decorator` schematic emits `Reflector.createDecorator()`; the docs keep both forms. **Mixing the two silently returns `undefined`.** `createDecorator()` generates a random metadata key (`uid(21)`) unless you pass `{ key: 'roles' }`. So `reflector.get('roles', handler)` against a `createDecorator` decorator yields `undefined`, and so does `reflector.get(Roles, handler)` against `@SetMetadata('roles', …)`. Pick one form per decorator and read it back by decorator reference, not by string.

## v12.1 built-ins — gate on `@nestjs/common` ≥ 12.1

On 12.1+, do **not** add `helmet`, `csurf`/`csrf-csrf`, or `cookie-parser`/`@fastify/cookie` for new work; these ship in the framework, identical on Express and Fastify. Below 12.1 they do not exist.

- `app.useSecurityHeaders()` — Helmet 8 defaults, removes `X-Powered-By`. Call it right after `NestFactory.create()`: calling it after `init()`/`listen()`, or twice, throws, and `app.use()` middleware registered before it runs without the headers. → `/security/helmet.md`
- `app.enableCsrfProtection()` — Fetch-Metadata (`Sec-Fetch-Site`/`Origin`) check, no tokens, sessions, or client changes. Same placement rule; rejections are `ForbiddenException` (403) before routing, so guards and controller filters never see them. → `/security/csrf.md`
- `@Cookies('name')` / `@SignedCookies()` from `@nestjs/common` read cookies; the HTTP adapter's `setCookie()` / `clearCookie()` write them; the `cookies` application option enables signing. Existing `cookie-parser` setups keep working. → `/http/cookies.md`
- File uploads (`FileInterceptor` and friends) now work on Fastify with the same API. → `/http/file-upload.md`

## Terminus

The legacy `HealthIndicator` base class and `HealthCheckError` are **removed**. Inject `HealthIndicatorService`, call `.check(key)`, and return `.up()` / `.down(details)` — or hand the work to `.attempt()`. Throwing no longer reports unhealthy. The `timeout` option of built-in indicators is deprecated: chain `.withTimeout(1500)` on the returned attempt. → `/recipes/terminus.md`

## BullMQ

`Queue.add()` no longer accepts a `repeat` option. For repeating or cron jobs, emit `queue.upsertJobScheduler(...)`. → `/application/queues.md`

## Observability

`@nestjs/observe` (via the `instrument` option of `NestFactory.create()`) is first-party and opt-in, and `nest new` defaults its prompt to yes. Never add it unasked; never remove it from a project that has it. → `/observability/sdk.md`

## Generated-project defaults

`nest new` prompts for CommonJS or ESM; **ESM is the default**, and there is no flag to choose non-interactively.
- **oxlint is the default linter for all generated projects** — both variants.
- **Vitest is the default test runner for ESM projects only**; CommonJS projects keep Jest.
- Rspack is the default monorepo bundler. `--webpack` / `--webpackPath`, and `webpack` / `webpackConfigPath` in `nest-cli.json`, are deprecated in favour of `--builder rspack` (`--rspackPath`; `builder.options.configPath`). The `angular` schematic is removed; `bun` is a supported package manager.

## Swagger CLI plugin does not run outside tsc

`@nestjs/swagger/plugin` is a **tsc AST transformer**. Vitest, `@swc/jest`, `ts-jest`, and the SWC builder compile without it, so no `@ApiProperty` metadata is synthesised and **DTOs document as empty schemas**. Since ESM projects default to Vitest, this bites by default there.
- SWC, standard (non-monorepo) setup: `nest start -b swc --type-check` (or `"typeCheck": true`) runs the plugin.
- ts-jest: register the plugin as an `astTransformers.before` entry.
- Otherwise run `PluginMetadataGenerator` from `@nestjs/cli/lib/compiler/plugins/plugin-metadata-generator.js` with `ReadonlyVisitor` from `@nestjs/swagger/plugin` — both exact; the `dist/plugin` and extension-less paths fail under ESM — to emit `metadata.ts`, then `await SwaggerModule.loadPluginMetadata(metadata)` before `SwaggerModule.createDocument(app, config)`.
- `esmCompatible` is detected per file from compiler options and `package.json`; set it only if detection is wrong.
- v12 monorepos build with Rspack; whether it runs the plugin is not documented — verify before relying on it. → `/openapi/cli-plugin.md`, `/recipes/swc.md`

## Node floors — the `engines` field understates both

| Task | Minimum Node |
| --- | --- |
| Running a v12 app | **20.19+**, or **22.12+** on the 22.x line |
| Running Jest against v12 packages | **24.9+** — older fails with `ERR_REQUIRE_ASYNC_MODULE` |
| `nest new` / `nest generate` / `nest upgrade` (`@nestjs/schematics`) | **22.22.3+**, **24.15+**, or **26+** |

21.x never got unflagged `require(esm)` and is unsupported; 23.x, 25.x, and early 22.x and 24.x releases are excluded from the CLI floor. `@nestjs/core` still declares `>= 20` and `@nestjs/cli` `>= 20.11` — both understate the real requirement, so do not read the floor off `engines`. `nest upgrade` refuses to run on an older release. **AWS Lambda** disables `require(esm)` on its Node 20/22/24 runtimes: a CommonJS v12 app needs `NODE_OPTIONS=--experimental-require-module` (appended to any existing value).

## Ecosystem majors move together

Every `@nestjs/*` package advances to its v12-compatible major at once — never pin a v11-era major alongside core 12. The majors are not all the same number: `@nestjs/graphql`, `@nestjs/apollo`, and `@nestjs/mercurius` go to **14**, and `@nestjs/config` to **12** from its 4.x line.

## ESM authoring rules (only when `package.json` has `"type": "module"`)

Generated code fails at runtime without these:
- Relative imports carry a **`.js` extension even in `.ts` sources** — `import { AppModule } from './app.module.js'`. The specifier names the emitted file.
- `__dirname` / `__filename` do not exist. Use `import.meta.dirname` (or `fileURLToPath(import.meta.url)`).
- `require()` does not exist. Build one with `createRequire(import.meta.url)` from `node:module`.
- **The TypeORM entity glob breaks** for exactly that reason: `entities: [__dirname + '/**/*.entity{.ts,.js}']` has no `__dirname`. Emit `autoLoadEntities: true` (see its caveat in `orm.md`) or rebuild the path from `import.meta.dirname`.
- `tsconfig.json` needs `"module": "nodenext"`, `"moduleResolution": "nodenext"`, `"resolvePackageJsonExports": true`, `"target": "ES2023"`. Projects from `@nestjs/schematics` ≥ 11.0.6 already have the first two, so adding `"type": "module"` is the whole switch; earlier v11 and v10 projects still say `"module": "commonjs"` and need both changed first.
- If your Vitest setup expects default imports, import supertest as `import request from 'supertest'`.
