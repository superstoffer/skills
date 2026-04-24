---
name: triage
description: >-
  Triage and file issues. Use when a user PASTES or SHARES raw content and
  wants it TRACKED as work items — not implemented. Inputs include meeting
  notes, retro action items, customer feedback, NPS responses, support
  threads, Slack forwards, or bug observations. Trigger phrases: "file
  this," "log this," "create issues," "triage this," "make tickets," "turn
  these into tickets." Also trigger when someone shares unstructured content
  and the implied goal is making it actionable — even without an explicit
  filing phrase. CRITICAL: technical content like errors, stack traces, or
  browser details is evidence FOR a ticket, never a request to debug or
  code. The question is: is the user handing you information to ORGANIZE,
  or asking you to BUILD something? Organize → this skill. Build → skip.
allowed-tools:
  - "mcp__linear*"
---

# Triage

Turn messy, unstructured input into clean, well-formed issues.

This skill classifies input, checks for duplicates, drafts issues, and creates them in your project tracker after your approval. Currently integrates with Linear via the Linear MCP server.

## Hard rules

1. **This skill is a product management tool, not a coding tool.** Never write code, generate scripts, create implementation files, or produce technical artifacts. The only output is issue drafts and project-tracker API calls.
   - If the input asks for code: extract the **requirement** and file it as an issue — don't implement it.
   - If the input contains code, stack traces, or error messages: treat them as **evidence for the bug report**. Quote the relevant snippet in the issue description — don't debug, fix, or rewrite it.
   - Acceptance criteria must describe observable outcomes, never implementation details. "Export downloads within 10s" is good. "Use the csv-writer library" is not.
   - Markdown formatting in issue descriptions is expected — that's not code.
2. **Always check for existing work first.** Before drafting any issue, search the project tracker for existing issues AND active projects that relate to the input. This is not optional — skipping dedup wastes the team's time and pollutes the backlog.
3. **The project tracker is the source of truth.** Use the Linear MCP tools for all reads (search, list teams, list projects, list labels, list states) and all writes (create issue, add comment). Never guess IDs — look them up.

## Workflow

Follow these steps in order for every input:

### 1. Ingest

Read the raw input. It might be pasted text, a file, a Slack thread, meeting notes, or a forwarded email. Accept whatever format it arrives in.

If the input is already well-structured (e.g., a GitHub issue with repro steps, labels, and assignee), preserve that structure — don't compress it into a shorter template. Map the existing fields to the tracker's equivalents.

### 2. Split

If the input contains multiple distinct concerns, list them as a numbered summary first. Then process each one separately through steps 3–8. Meeting notes routinely contain 3–10 asks — splitting is the norm, not the exception.

### 3. Classify

Assign each concern to one of these classes:

| Class | Signals | Action |
|---|---|---|
| **Bug** | "doesn't work," "broken," error codes, stack traces, "expected X got Y," regression language | Draft with repro/expected/actual template |
| **Feature** | "I wish," "can we add," "users are asking for," Jobs-To-Be-Done language | Draft as problem-first issue |
| **Chore** | "upgrade," "clean up," "migrate," dependency bumps, tooling requests | Draft terse issue |
| **Tech Debt** | Performance rot, architectural coupling, scaling concerns, duplication | Draft terse issue |
| **Spike** | "should we," "evaluate," "investigate," "compare," research questions | Draft with question/timebox/deliverable template |
| **Question** | Interrogative seeking information, FAQ-ish, answerable from existing docs | **Stop.** Suggest answering or linking to docs. Do not create an issue. |
| **Noise** | Emotional venting with no specific claim, compliments, congratulations | **Stop.** Acknowledge. Do not create an issue. |
| **Strategic** | "rethink," "reimagine," "pivot," broad architectural/roadmap scope | **Stop.** Suggest a Project or Initiative, not an issue. |

**Security bugs:** If a bug involves data leakage, unauthorized access, or credential exposure, flag it as security-sensitive. Note in the draft that it may need restricted visibility.

**Input that asks for code:** Classify by the underlying need (Feature, Chore, etc.), not by the request to "write" or "implement." See Hard Rule 1.

For ambiguous cases, read `references/classification-rubric.md`.

### 4. Extract

Pull out the core **problem** — not the proposed solution. Most feature requests are users pitching solutions; find the pain or gap behind the ask.

Extract and preserve:
- The problem from the user's perspective
- Affected user segment or product surface
- For bugs: reproduction steps, expected vs actual behavior, environment
- Direct customer quotes — **verbatim, in a blockquote.** The customer's exact words carry signal you can't paraphrase without losing.
- Source link (Slack permalink, doc URL, meeting recording)
- Pre-assigned owners and deadlines — if the input comes from a post-mortem or action-item list where people and dates were already agreed, preserve them. Don't strip what was explicitly decided.

### 5. Check for existing work

This step is mandatory. Never skip it, even if the input seems obviously new.

**If the input contains an issue identifier** (e.g., "ENG-1234"), fetch it directly via the Linear MCP rather than text-searching.

**Search for existing issues:**
1. Use the Linear MCP's search tool. Filter by team when possible and exclude completed/canceled states to reduce noise.
2. Try 2-3 keyword variations (the main noun, a synonym, a broader term) — search is literal, not semantic.
3. If the search returns many results, show only the top 3-5 most relevant (prefer open issues on the same team). Summarize the rest.
4. If a match exists: show it to the user and recommend **adding a comment** (with the new quote/context and source) rather than creating a duplicate.
5. Let the user override if they want a separate issue.

**Search for related projects:**
1. Use the Linear MCP to list projects (filter to non-completed/non-canceled).
2. If the input relates to an ongoing project, note it in the draft so the issue can be attached.
3. If the input is too broad for a single issue and maps to an existing project, suggest adding sub-issues to that project instead.

### 6. Draft

Render the issue. Read `references/issue-templates.md` for the full template per type, including worked examples.

**Title format:** imperative, verb-first, under 10 words, no period, no brackets.
- Bug: `Fix [object] [qualifier]`
- Feature: `Add [capability]`
- Chore: `Upgrade/Migrate/Clean up [object]`
- Spike: `Investigate [question]`

**Description:** Use the type-specific template from `references/issue-templates.md`. Target: 3–6 lines for standard issues. Omit empty sections entirely. For already-structured input, preserve the original detail rather than compressing.

### 7. Confirm

Present the draft to the user as a formatted preview. Wait for explicit approval (`ok`, `create`, `ship it`, or similar). Allow inline edits.

For multi-issue batches: present all drafts together, let the user approve, edit, or reject each individually. If the batch is large (8+ issues), confirm before starting creation: "That's N issues — want me to create them all, or in smaller batches?"

### 8. Create

Use the Linear MCP to create the issue. Look up all IDs via the MCP — don't hardcode or guess.

1. **Team:** Use Linear MCP to list teams. Match against `references/linear-conventions.md` or ask the user on first use. Remember the team within this conversation.
2. **Labels:** Use Linear MCP to list workspace labels. Match the type label and area label by name. Labels are workspace-scoped in Linear, not team-scoped.
3. **State:** Use Linear MCP to list workflow states for the team. Prefer the `triage`-type state if one exists; fall back to a `backlog`-type state. Match on state **type**, not state name — workspaces customize names.
4. **Priority:** Use Linear's integer scale: 0=None, 1=Urgent, 2=High, 3=Medium, 4=Low. Default is 0.
5. **Project:** If step 5 identified a related project, include the project ID.
6. **Assignee:** If the input explicitly names an owner (especially from post-mortems or action items), look up their user ID via the Linear MCP. Otherwise leave unset.

Create the issue and return the URL. If creation fails, report the specific error — don't retry automatically.

For batches: create in sequence, returning each URL. If one fails, report which succeeded and which failed. Don't silently skip.

## Field defaults

| Field | Default | Override when... |
|---|---|---|
| Team | User's default team | Input explicitly mentions another area |
| Status | `triage`-type state (fallback: `backlog`-type) | Never `unstarted`/Todo unless user signals immediate work |
| Priority | 0 (none) | Revenue risk, churn language, customer tier, "blocking," "P0," "ASAP," contractual deadlines |
| Labels | Type label + max one area label | Never use labels to encode priority or status — the tracker has fields for those |
| Assignee | Unset | Input explicitly names an owner, or comes from a post-mortem with pre-assigned actions |
| Estimate | Unset | Let the implementing engineer set this |
| Project | Unset | Set if step 5 found a matching active project |
| Due date | Unset | Only if input names a real external deadline (not an internal wish) |

## Do NOT create an issue when

1. **Question already answered** — route to docs or suggest a reply
2. **Vent with no actionable claim** — acknowledge, offer feedback-theme tracking
3. **Compliments or congratulations** — acknowledge, do not file
4. **Exact duplicate of open issue** — add a comment to the existing issue instead
5. **Strategic/roadmap-level ask** — suggest a Project or Initiative, not an issue
6. **Too vague to act on** ("the dashboard thing") — ask one clarifying question; if no answer, don't force it
7. **Meta-requests about the skill itself** ("change how you format titles") — explain the conventions and point to `references/linear-conventions.md` for customization

## Handling ambiguity

Ask at most **one** clarifying question. If the user doesn't answer, proceed with your best-guess draft and flag the assumption explicitly:

> **Assumption:** [what you assumed and why]. Triage owner: reject if wrong.

If the user disagrees with your classification ("that's not a bug, it's a feature"), defer to them. Your classification is a suggestion, not a mandate.

## Sensitive information

Be specific about what to strip and what to keep:
- **Strip:** API keys, tokens, passwords, personal email addresses, personal phone numbers, account IDs that could enable unauthorized access.
- **Keep:** Company names, deal sizes/ARR, job titles, product surface areas. These are business context, not PII �� they're essential for triage.
- **Warn the user** if the input contained credentials that were redacted.

## When the project tracker is unavailable

If MCP calls fail (auth expired, server unreachable, permissions error):
1. Stop and tell the user what went wrong.
2. You can still draft issue text as a preview, but you cannot search for duplicates or create issues.
3. Do not guess team IDs, label IDs, or any other identifiers.
4. Suggest the user check their MCP configuration.

## Reference files

- `references/issue-templates.md` — Full templates with worked examples for each issue type (including Spike)
- `references/classification-rubric.md` — 20 worked input→class examples, keyword lists, borderline rules
- `references/examples.md` — 8 complete before/after transformations across input types
- `references/linear-conventions.md` — **Customize this:** your workspace's teams, labels, projects, and area contacts. The `allowed-tools` pattern assumes your Linear MCP server is named "linear" in your Claude Code MCP settings.
