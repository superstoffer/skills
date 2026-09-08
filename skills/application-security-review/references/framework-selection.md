# Framework selection

Inspect the project, then activate only the frameworks that apply. **ASVS 5.0 and
the Top 10:2025 are always on**; every other framework waits for a positive cue.
When you cannot tell whether a surface exists, say so and ask — do not assume it
into or out of scope.

## Always active

- **ASVS 5.0** (`asvs-5.md`) — the backbone of verifiable requirements.
- **OWASP Top 10:2025** (`web-top10-2025.md`) — the risk-classification label.

## API surface → API Security Top 10:2023

Activate `api-top10-2023.md` in addition to the backbone when the app exposes an
API. Cues:

```bash
grep -rniE "app\.(get|post|put|delete|patch)\(|@(Get|Post|Put|Delete|Patch|Controller)\(|router\.(get|post|route)|@app\.route|@RestController" src app 2>/dev/null
grep -rlniE "openapi:|swagger:|graphql|type Query|type Mutation" . 2>/dev/null
find . \( -name "*.proto" -o -name "*.graphql" -o -name "openapi*.y*ml" -o -name "swagger*.json" \) 2>/dev/null
grep -rn "/api/" . 2>/dev/null | head
```

Positive signals: Express/Fastify route handlers, Nest/Spring controllers, Flask
`@app.route` / FastAPI, Django REST, Rails controllers, OpenAPI/Swagger specs, a
GraphQL schema or `.graphql`, gRPC `.proto`, tRPC routers, or `/api/` paths.

## Mobile → MASVS/MASTG  (v1.1 — not yet implemented)

Cues: `android/`, `ios/`, `*.xcodeproj`, `build.gradle`, `AndroidManifest.xml`,
React Native, Flutter, Expo, Capacitor. See `future/mobile-masvs.md`.

## Desktop → Desktop App Security Top 10  (v1.2 — not yet implemented)

Cues: Electron, Tauri, .NET / WPF / WinUI, Qt, Swift/macOS, native Rust/C++
desktop. Electron and Tauri get **both** web and desktop checks. See
`future/desktop-top10.md`.

## GenAI → LLM Top 10:2026  (v1.3 — not yet implemented)

Cues: OpenAI/Anthropic SDKs, prompt templates, RAG pipelines, vector databases,
tool/function calling, agent frameworks. Activate on the **application's own AI
features** — not merely because an AI assistant wrote the code. See
`future/genai-llm-top10-2026.md`.

## Deep mode → WSTG

Not a project cue — a **request**. `--deep`, "test", "pentest plan", or an
explicit ask to test activates `wstg.md`. See the Modes section of `SKILL.md`.
