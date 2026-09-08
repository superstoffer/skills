# GenAI — OWASP LLM Top 10:2026  (v1.3, not yet implemented)

**Detection is wired** in `../framework-selection.md`; the review checklist is
**not implemented yet** (planned: v1.3). If a project triggers this module, say
the GenAI module is not yet available rather than improvising.

- Standard: **OWASP GenAI LLM Top 10 2026** (published 2026-08-04). Covers prompt
  injection, insecure output handling, excessive agency, unbounded consumption,
  hidden-context exposure, and related risks.
- Activation cues: OpenAI/Anthropic SDKs, prompt templates, RAG, vector DBs,
  tool/function calling, agent frameworks — the **application's own AI features**,
  not merely that an AI wrote the code.
- **Distinct from `agentic-security-review`**, which audits AI *skills/plugins/
  MCP/hooks* against the Agentic Skills Top 10. A separate **OWASP Top 10 for
  Agentic Applications (2026)** also exists and may inform this module.
