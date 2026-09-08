# skills

Claude Code skills by [Christoffer Baadsgaard](https://github.com/superstoffer).

## Install

```
/plugin marketplace add superstoffer/skills
/plugin install superstoffer@superstoffer-skills
```

Skills then appear namespaced as `superstoffer:<skill>`.

Each skill is a self-contained folder under `skills/`, so you can also copy one straight into `~/.claude/skills/` if you'd rather not install the whole collection.

## Skills

| Skill | What it does |
| --- | --- |
| [triage](skills/triage/README.md) | Turns messy, unstructured input — meeting notes, Slack threads, bug reports, customer feedback — into clean, well-formed issues in your tracker. Supports Linear. |
| [design-doc](skills/design-doc/README.md) | Decides whether a software design doc is warranted, drafts it, reviews an existing one, or drives it toward approval. Based on Michael Lynch's guide. |
| [nest](skills/nest/README.md) | Supplies the NestJS version facts Claude can't have from training — v12 deltas, TypeORM 1.x, Prisma 7 — then verifies generated code compiles and its module graph resolves. |
| [visual-design](skills/visual-design/README.md) | Encodes the visual craft Claude skips unaided — OKLCH palettes, a single emphasis device, and a mandatory optical pass — on anything with a visual surface, with the golden ratio ranked honestly. |
| [agentic-security-review](skills/agentic-security-review/README.md) | Audits a skill, plugin, MCP server, or hook against the OWASP Agentic Skills Top 10 and the lethal trifecta before you install it — running read-only and treating the reviewed material as data, never instructions. |
| [application-security-review](skills/application-security-review/README.md) | Reviews your own application code against the OWASP frameworks that apply — ASVS 5.0 and the Top 10:2025 always, the API Security Top 10 when an API is present — mapping each finding to a concrete standard with cheat-sheet remediation. Complements the built-in `/security-review`. |

## License

MIT
