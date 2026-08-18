# design-doc

A Claude Code skill for software design docs — the technical document an engineer writes *before* implementing, to settle decisions that are expensive to reverse.

Based on Michael Lynch's [How to Write an Effective Software Design Document](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/), its [worked example](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/little-moments-design-doc/), and the companion piece on [useful feedback on design docs](https://refactoringenglish.com/excerpts/useful-feedback-on-design-docs/).

## What it does

Four modes, inferred from your request rather than selected:

| Mode | When |
| --- | --- |
| **Triage** | "Should I write this up first?" — screens against six questions and recommends a depth, or tells you plainly not to bother |
| **Draft** | Writes the doc, interviewing you only for what it can't infer |
| **Review** | Critiques an existing doc against a severity-ordered rubric |
| **Revise** | Moves items between Open and Resolved Issues, driving the doc toward approval |

## The governing rule

> What's the penalty for being wrong?

A decision earns a place in the doc in proportion to the cost of reversing it. Storage backend, language, and interface boundaries belong. Pagination style and button placement don't. This applies to detail *you* supply too — the skill will leave out a decision that fails the test and tell you why.

The counterweight: it never writes the implementation. Lynch's warning is that a doc specifying every detail has written the implementation during the design phase, defeating the point.

## Adaptive sections

Six sections are always present: Title, Metadata, Objective, Background, Goals, Non-goals. Everything else — SLOs, Security, Privacy, Legal, Interfaces, Timeline, and the rest — appears only when a stated trigger fires. After each draft the skill prints what it omitted and which trigger didn't fire, so you can override it.

## What it enforces

- Goals state impact on users, the team, or the company — never implementation. Implementation-shaped goals get rewritten, and you're shown the rewrite.
- The first page stands alone for a reader who has never spoken to you, including someone on a partner team.
- Design gaps become Open Issues with problem, options, and a next step — never confident prose over a hole.
- Diagrams are emitted as Mermaid or D2 source, never images, so they stay reviewable in a diff.

## Scope

Technical design only. It won't produce a business case, ROI analysis, or executive summary — that's the [project-initiation](https://github.com/superstoffer/project-initiation) skill's job. It also won't write READMEs, API reference, after-the-fact ADRs, or commit messages.

The dividing line: deciding **how** to build something costly to reverse → this skill. Justifying **whether** to build it → project-initiation. Documenting something already built → neither.

## Install

See the [repository README](../../README.md) for the plugin install.

To copy this skill directly instead:

```bash
# personal, all projects
mkdir -p ~/.claude/skills && cp -r skills/design-doc ~/.claude/skills/

# project-local, shared via git
mkdir -p .claude/skills && cp -r skills/design-doc .claude/skills/
```

Both are safe to re-run to update an existing copy.

## Usage

Invoke explicitly with `/design-doc`, or just describe what you're about to build and ask whether it's worth writing up.

Docs are written into whichever of `docs/`, `doc/`, `design/`, or `rfcs/` already exists, following the convention it finds there. If none exists, it creates `docs/design/`. It never overwrites an existing doc without asking.
