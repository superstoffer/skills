---
name: design-doc
description: >-
  Write, review, or revise a software design doc — the technical document an
  engineer writes BEFORE implementing, to settle decisions that are expensive
  to reverse. Use when someone is planning a build and asks "should I write
  this up first," proposes an architecture, drafts an RFC or tech spec, wants
  a plan documented before coding starts, or hands over someone else's
  proposal for review or feedback. Also use to decide whether a doc is
  warranted at all. NOT for documenting things that already exist — READMEs,
  API reference, after-the-fact ADRs, commit messages. NOT for the business
  case — PRDs, requirements docs, one-pagers, ROI, or Go/No-Go material
  belong to the project-initiation skill. The question is: is the user
  deciding HOW to build something costly to reverse, or justifying WHETHER
  to build it? How → this skill. Whether → project-initiation. Already
  built → neither.
---

# Design Doc

Decide whether a software design doc is warranted, draft one, review one, or drive one toward approval.

Based on Michael Lynch's *How to Write an Effective Software Design Document*. A design doc is written by an engineer, read by teammates and partner teams, and covers technical design only.

## The editorial rule

Everything in this skill follows from one question:

> **What's the penalty for being wrong?**

A decision belongs in the doc in proportion to the cost of reversing it. Programming language, storage backend, and interface boundaries are expensive to undo — they belong. Pagination style, button placement, and anything fixable in an afternoon do not.

This applies to detail **the user supplies**, not just detail you generate. When someone hands you a decision that fails the test, leave it out and tell them why in one line. Don't silently include it, and don't silently drop it.

## Hard rules

1. **Goals are impact, never implementation.** A goal states how the project benefits users, the team, or the company. When given an implementation-shaped goal, rewrite it into the outcome it serves and show the rewrite:
   - ✗ "Add Kubernetes to our infrastructure."
   - ✓ "Minimize outages related to deploying new app versions."
2. **The first page stands alone.** Some readers reach the doc before hearing a word from the author, including people on partner teams. Everything needed to understand what this is and why it exists goes on page one. Detail deepens further down — inverted pyramid, not a slow build.
3. **Gaps become Open Issues, never confident prose.** Where the design is genuinely unresolved, write an Open Issue with the problem, the visible options, and a concrete next step. Papering over uncertainty defeats the purpose of the exercise — an honest open issue is the point.
4. **Diagrams are source, never images.** Emit Mermaid or D2 in a fenced block so diagrams stay editable and reviewable in a diff. Never emit or link a PNG/SVG as the primary artifact.
5. **Detail is proportional to the penalty for being wrong.** See above.
6. **Never write the implementation.** *"If you specify every possible detail in a design doc, you've essentially written the implementation during the design phase. That would defeat the whole purpose of a design doc."* Name decisions and their rationale. Do not produce the code, the full schema, or step-by-step build instructions. Rule 5 prunes trivia from below; this rule caps depth from above.
7. **Stay on the technical side of the line.** No ROI, financial justification, or executive summary. If the request is really for a business case, say so plainly and point to the `project-initiation` skill rather than quietly producing a hybrid.

## Modes

Infer the mode from the request. Never ask which one.

| Mode | Signal |
|---|---|
| **TRIAGE** | "should I write this up," "is this worth a doc," scope described but no doc exists yet |
| **DRAFT** | "write a design doc for X," a plan that needs writing up |
| **REVIEW** | an existing doc supplied, feedback requested |
| **REVISE** | an existing doc plus new decisions, review comments, or resolutions |

When a request spans two modes ("is this worth a doc, and if so write it"), run TRIAGE first and report the verdict before drafting.

## TRIAGE

Screen against these six questions. Infer answers from what the user described rather than interrogating them; ask only where the answer is genuinely unknowable and would change the verdict.

1. Will multiple people coordinate work to implement the design?
2. Will the project take more than three months of full-time dev work?
3. Will the implementation run in production for several years?
4. Does the project involve cross-team collaboration?
5. Are the goals and requirements ambiguous?
6. Are there catastrophic risks preventable at design time (security flaws, legal exposure)?

Report which fired and the count. Then:

| Yes count | Verdict |
|---|---|
| 0 | **Don't write one.** Say so plainly and name the lighter alternative: a thorough PR description, an issue with acceptance criteria, or an ADR once it's built. |
| 1 | Probably worth it → **one-pager** |
| 2–3 | Almost certainly worth it → **standard** |
| 4+, or any yes on Q4 or Q6 | **Heavyweight, with formal signoff** |

Zero yes answers is a real and useful outcome. Deliver it without hedging.

## DRAFT

1. **Interview only for what you can't infer**, and only where the answer changes an expensive decision. Read the codebase first — existing language, storage, and deploy target are usually discoverable without asking.
2. **Select sections** per the trigger table below.
3. **Write** to the output location determined below, using `templates/design-doc.md` as the skeleton.
4. **Print the omission report.**

## REVIEW

Load `references/review-rubric.md` and work through it. Order findings big-to-small — a goal stated as implementation, or a first page a partner team can't follow, outranks any wording issue. Never open with line edits.

## REVISE

Move items between Open Issues and Resolved Issues. On resolution, preserve the original discussion and append the rationale and who decided — a Resolved Issue is a decision record, not a deletion.

When a reviewer misunderstood something, fix it **in the doc**, not in a reply. *"Resolve their confusion in the doc itself. Don't explain things 'out of band.'"* When a comment thread has run past two or three exchanges, drain it into an Open Issue rather than letting it sprawl.

## Section selection

Always include: **Title, Metadata, Objective, Background, Goals, Non-goals.**

Everything else fires only on its trigger:

| Section | Include when |
|---|---|
| Related Documents | prior specs, designs, or test plans exist |
| Scenarios | user- or system-facing workflows aren't obvious from Goals |
| Diagrams | multiple components, non-obvious data flow, or a protocol |
| Glossary | internal jargon that can't be defined inline |
| Constraints | something real is imposed from outside (budget, infra, contract, deadline) |
| SLOs | production availability, latency, or scale requirements exist |
| Monitoring / Alerting | the SLO trigger fired — a service someone is on call for |
| Timeline | multiple people coordinate, or milestones are externally committed |
| Interfaces | an API, UI, file format, or protocol others code against |
| Dependencies / Infrastructure | the design picks a language, storage, hosting, or third-party service |
| Security | there's an attack surface or a trust boundary |
| Privacy | user or otherwise sensitive data is handled |
| Legal | regulated domain, contractual constraints, or an OSS licensing choice |
| Logging | a long-lived service whose failures must be debuggable after the fact |
| Open Issues | any decision is genuinely unresolved — expect this on most first drafts |
| Resolved Issues | anything has moved out of Open Issues |
| Alternatives Considered | a reader would reasonably ask "why not X?" |

For each section's purpose, the questions it answers, and a worked example, read `references/sections.md`.

## Output location

Look for an existing convention before inventing one. Check in order: `docs/`, `doc/`, `design/`, `rfcs/`. If one exists, match whatever is already there — filename style, numbering scheme, front matter, heading depth.

Only if none exists, create `docs/design/` and derive a kebab-case filename from the title.

**Never overwrite an existing doc without asking.**

## Omission report

After every draft, print what you left out and which trigger didn't fire, so it can be overridden:

```
Omitted:
  SLOs, Monitoring   — no production availability or latency requirement stated
  Legal              — no regulated domain, contract, or licensing choice
  Glossary           — no jargon that couldn't be defined inline

Say the word to add any of these.
```

If you dropped user-supplied detail under the editorial rule, list it here too, with the reason.

## Reference files

- `references/sections.md` — full section catalog: purpose, questions answered, trigger, worked example
- `references/review-rubric.md` — what to check when critiquing a doc, ordered by severity
- `templates/design-doc.md` — the skeleton, core sections live and conditionals commented out
