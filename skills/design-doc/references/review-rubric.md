# Review rubric

What to check when critiquing a design doc, ordered by severity. Work top to bottom and stop escalating once you've found enough — a review that opens with comma placement while the goals are wrong is a failed review.

## How to deliver the review

**Big issues first, always.** Lead with the findings that could change the design. Wording, formatting, and typos go last, batched, or omitted entirely.

**Critique the doc, not the author.** "This goal describes an implementation" beats "you've confused goals with implementation."

**Every criticism carries a concrete alternative.** "Objective is unclear" is not actionable. "Objective doesn't say who this is for — suggest naming the audience in the first clause" is.

**Separate blocking from optional.** Say which findings must be resolved before approval and which are suggestions the author can decline. Reviewers who mark everything blocking get ignored.

**Missing sections are findings.** Check the trigger table in `SKILL.md`. A service with latency requirements and no SLOs section is a real gap, and so is a doc handling user data with no Privacy section.

## Severity 1 — the doc can't do its job

- **Goals stated as implementation.** Any goal naming a technology, library, or refactor rather than an outcome. Propose the rewrite, don't just flag it.
- **First page doesn't stand alone.** Read only the Title, Metadata, Objective, and Background, then ask: could a partner-team engineer who has never spoken to the author say what this is and why it exists? If not, this is the finding that matters most.
- **No Objective, or an Objective that needs the Background to parse.**
- **Uncertainty disguised as confidence.** Passages hedging with "we'll probably," "TBD," "some mechanism for," or "to be determined later" that aren't written up as Open Issues. Each one is a gap the doc is hiding. Convert it into an Open Issue with problem, options, and next step.
- **Scope is unbounded.** No Non-goals, in a doc where reviewers will obviously propose adjacent work.

## Severity 2 — decisions can't be evaluated

- **Expensive decisions asserted without rationale.** Language, storage, hosting, and interface boundaries need a reason, not just a statement. Apply the test: what's the penalty for being wrong? High penalty and no rationale is a finding.
- **Obvious alternative unaddressed.** If a competent reader would ask "why not X?" and the doc doesn't answer, that belongs in Alternatives Considered.
- **Alternatives are strawmen.** Every rejected option looking obviously bad means the space wasn't explored. Ask what each alternative would have been *good* at.
- **Interfaces without error semantics.** A contract that specifies the happy path only will be renegotiated during implementation, which defeats writing it down.
- **SLOs without numbers.** "Highly available" is not an objective.
- **Security section without enumerated threats.** Generic assurances ("inputs will be validated") show nothing was actually threat-modelled.
- **Missing section whose trigger clearly fired.** Handles user data, no Privacy. Regulated domain, no Legal. On-call service, no Monitoring.

## Severity 3 — the doc will be misread

- **Undefined jargon.** Any internal term used before it's defined, especially in the first two pages. Either define inline or add a Glossary.
- **No diagram where the data flow is non-obvious.** Multiple components with implicit relationships. Ask for Mermaid or D2 source, not an image.
- **Diagram as an image.** A linked or embedded PNG/SVG can't be reviewed in a diff and rots silently. Ask for source.
- **Detail wildly out of proportion.** Three paragraphs on button placement next to one sentence on the storage engine. Cuts and expansions are both valid findings.
- **Implementation smuggled in.** Full schemas, complete function bodies, or step-by-step build instructions. The design phase shouldn't contain the implementation.

## Severity 4 — polish

Batch these into a single note. Never lead with them.

- Inconsistent terminology for the same concept
- Passive constructions obscuring who does what
- Formatting, heading depth, table alignment
- Typos

## Process checks

These apply to how the review is being run, not the doc's content. Raise them when relevant.

- **Reviewers need at least two working days** for independent reading before any synchronous discussion. A meeting scheduled before anyone has read the doc produces reactions, not review.
- **Start with a single preliminary reviewer.** One person reading first catches the explanatory gaps cheaply. Sending a first draft to eight people triggers the bystander effect, where each assumes someone else is reading closely.
- **Threads must be driven to resolution.** A doc carrying dozens of unresolved margin comments that contradict the design leaves nobody able to say what was actually decided. After two or three exchanges, move the discussion into Open Issues and link it.
- **Confusion gets fixed in the doc.** When a reviewer misunderstands something, update the document rather than replying — the next reader will misunderstand it identically.
- **Meetings for contentious issues need a written agenda circulated beforehand,** and attendees should understand the meeting is not an invitation to reopen previously uncontroversial decisions.

## Approval

A doc is ready when: the first page stands alone, every goal states impact, every high-penalty decision has a rationale, every triggered section is present, and every remaining uncertainty is an Open Issue with a next step rather than a silence.

Open Issues remaining is not a blocker for approval — hidden ones are.
