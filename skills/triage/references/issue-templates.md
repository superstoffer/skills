# Issue Templates

Full templates for each issue type. The SKILL.md has the canonical short template — this file has type-specific guidance and worked examples.

## Table of Contents

- [Bug](#bug)
- [Feature](#feature)
- [Chore](#chore)
- [Tech Debt](#tech-debt)
- [Spike / Investigation](#spike--investigation)

---

## Bug

**Title verbs:** Fix, Resolve, Patch, Handle
**Title pattern:** `Fix [broken thing] [where/when it breaks]`

### Template

```markdown
**Repro:**
1. <step>
2. <step>
3. <step>

**Expected:** <what should happen>
**Actual:** <what happens instead>
**Env:** <browser/OS/version/account type>

**Source:** <link>
```

### Example

**Title:** Fix payment modal crash on Safari 17

```markdown
**Repro:**
1. Open billing page on Safari 17.4
2. Click "Update payment method"
3. Enter any card number and submit

**Expected:** Payment method updates, modal closes
**Actual:** Modal freezes, console shows `TypeError: Cannot read property 'stripe' of undefined`
**Env:** Safari 17.4 / macOS Sonoma 14.4, Pro plan account

**Source:** https://company.slack.com/archives/C0123/p1234567890
```

### Guidance

- Number the repro steps. Unnumbered prose is harder to follow during debugging.
- "Expected" and "Actual" should each be one sentence. If you need more, the bug is probably two bugs.
- Include the exact error message or stack trace snippet when available — don't paraphrase errors.
- Environment matters more than you think. "Desktop" is not enough. Browser + version + OS + account type is the minimum.

---

## Feature

**Title verbs:** Add, Enable, Support, Introduce, Allow
**Title pattern:** `Add [capability] [for whom/where]`

### Template

```markdown
**Problem:** <one sentence — the user pain or gap, not the solution>

**Context:** <why now, or what changed; omit if obvious>

> <verbatim customer quote if the input was feedback>

**Acceptance criteria:**
- [ ] <observable outcome 1>
- [ ] <observable outcome 2>
- [ ] <observable outcome 3>

**Source:** <link>
```

### Example

**Title:** Add CSV export for audit log

```markdown
**Problem:** Compliance team needs to submit quarterly audit reports to external auditors, but currently has to screenshot the audit log page by page.

**Context:** New SOC 2 requirement starting Q3 — this is blocking certification renewal.

> "I literally spend two days every quarter screenshotting the audit log. Can we please just get a CSV export?"

**Acceptance criteria:**
- [ ] Audit log page has an "Export CSV" button
- [ ] Export includes all columns visible in the UI
- [ ] Export respects the current date filter
- [ ] File downloads within 10 seconds for up to 10k rows

**Source:** https://company.slack.com/archives/C0456/p9876543210
```

### Guidance

- Lead with the problem, not the solution. "Users can't export audit data in a portable format" beats "Add a CSV download button."
- Quote the customer verbatim when you have their words. The exact phrasing carries emotional and contextual signal.
- Acceptance criteria should be observable outcomes, not implementation details. "Button exists" and "file downloads" — not "use the `csv-writer` library."
- 2–4 acceptance criteria is the sweet spot. More than 5 suggests the issue should be split.

---

## Chore

**Title verbs:** Upgrade, Migrate, Clean up, Remove, Rename, Update
**Title pattern:** `Upgrade [dependency] to [version]` or `Clean up [thing]`

### Template

```markdown
**What:** <one sentence describing the mechanical change>

**Why:** <one sentence — what breaks, degrades, or becomes harder if we don't>

**Source:** <link if applicable>
```

### Example

**Title:** Upgrade Next.js to 15

```markdown
**What:** Bump Next.js from 14.2 to 15.0, update breaking API calls per migration guide.

**Why:** Next.js 14 drops out of security support in August. Two known CVEs already patched only in 15.x.

**Source:** https://nextjs.org/blog/next-15
```

### Guidance

- Chores are mechanical. Keep the description short — the "what" is usually obvious from the title.
- The "why" matters more than the "what." "Because it's old" is not a reason. "Because it's losing security support" is.
- No acceptance criteria needed unless the chore has non-obvious verification steps.

---

## Tech Debt

**Title verbs:** Refactor, Decouple, Extract, Consolidate, Replace
**Title pattern:** `Refactor [component] to [improvement]`

### Template

```markdown
**Problem:** <what's wrong with the current state — symptoms, not causes>

**Impact:** <what this debt costs us — slower development, bugs, incidents>

**Proposed direction:** <brief sketch of the fix, not a full design>

**Source:** <link if applicable>
```

### Example

**Title:** Refactor notification service to decouple from user model

```markdown
**Problem:** The notification service directly queries the user table and constructs its own user objects, bypassing the user service entirely. Changes to the user schema require updating notification code too.

**Impact:** Last three user model changes each required a parallel notification PR. The notification test suite mocks the user table directly and has broken twice on schema changes.

**Proposed direction:** Have the notification service accept a user DTO from the caller rather than querying the user table itself.
```

### Guidance

- Tech debt issues should make the cost concrete. "This is messy" is not enough. "This caused 3 incidents last quarter" is.
- Include a proposed direction, but keep it to one sentence. The implementer will design the actual solution.
- If the debt is large, this issue might be better as a Project with sub-issues. Flag that to the user.

---

## Spike / Investigation

**Title verbs:** Investigate, Evaluate, Explore, Prototype, Benchmark
**Title pattern:** `Investigate [question or hypothesis]`

### Template

```markdown
**Question:** <what we're trying to learn>

**Why it matters:** <what decision this unblocks>

**Timebox:** <suggested time limit>

**Expected output:** <what the spike should produce — a doc, a prototype, a recommendation>

**Source:** <link if applicable>
```

### Example

**Title:** Investigate WebSocket vs SSE for real-time updates

```markdown
**Question:** Should we use WebSockets or Server-Sent Events for the new real-time dashboard? We need to understand latency, connection limits, and infrastructure cost for each.

**Why it matters:** Architecture decision blocks the real-time dashboard project. Wrong choice means a rewrite in 6 months.

**Timebox:** 2 days

**Expected output:** One-page comparison doc with recommendation, shared in #eng-architecture.
```

### Guidance

- Spikes are not open-ended research. They have a question, a timebox, and a deliverable.
- The deliverable should be a concrete artifact (doc, prototype, benchmark results) — not "understanding."
- If you can't state the question in one sentence, the spike is too broad. Split it.
