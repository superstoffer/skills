# Classification Rubric

Use this when the inline classification table in SKILL.md isn't enough to make a confident call. This file has keyword lists, borderline rules, and 20 worked examples.

## Table of Contents

- [Keyword Signals](#keyword-signals)
- [Borderline Rules](#borderline-rules)
- [Worked Examples](#worked-examples)

---

## Keyword Signals

These aren't deterministic — they're signals that shift the probability. Always read the full input in context.

### Bug signals
- Error messages, stack traces, HTTP status codes (500, 404, 403)
- "doesn't work," "broken," "stopped working," "used to work," "regression"
- "expected X got Y," "should have," "instead it"
- Screenshots showing error states
- "after the last deploy," "since the update"

### Feature signals
- "I wish," "can we add," "it would be great if," "users are asking for"
- "there's no way to," "we need a way to," "how do I" (when the answer is "you can't")
- "competitor X has," "other tools let you"
- Jobs-To-Be-Done language: "when I'm trying to [goal], I have to [workaround]"

### Chore signals
- "upgrade," "bump," "update dependency," "migrate"
- "clean up," "remove dead code," "delete unused"
- "rename," "reorganize," "move to"
- EOL notices, deprecation warnings, security advisories

### Tech Debt signals
- "refactor," "decouple," "extract," "consolidate"
- "this is getting hard to maintain," "every time we change X we also have to change Y"
- "flaky," "brittle," "fragile," "tech debt"
- Coupling complaints, architecture concerns

### Spike / Investigation signals
- "should we," "evaluate," "investigate," "compare," "prototype," "benchmark"
- Open-ended research questions with no clear answer yet
- Architecture decision records, technology selection, feasibility studies
- "is it worth," "what if we," "can we," when the answer requires investigation

### Question signals
- Interrogative form: "how do I," "what's the," "where is," "is it possible to"
- Seeking clarification, not requesting action
- Could be answered by pointing to existing docs

### Noise signals
- Pure emotional expression: "ugh," "this sucks," "I hate this"
- No specific claim about what's wrong or what should change
- Complaints about things outside the team's control

---

## Borderline Rules

These resolve the ambiguous cases where signals from multiple classes are present.

### Feedback with specific repro → Bug, not Feature
If someone says "I wish the search worked when I type special characters" and can describe exact steps where it fails, that's a bug. The "I wish" framing is incidental — the behavior is broken.

### "How do I X?" where X is impossible → Feature, not Question
"How do I export my data as CSV?" — if there's no CSV export, this is a feature request. The interrogative framing is the user's polite way of requesting something.

### Vague frustration with a specific noun → ask one clarifying question
"The dashboard is so slow" — there's an actionable claim (performance issue) but not enough detail. Ask: "Which dashboard, and roughly how slow? Loading time, or interaction lag?" If they answer, it's likely a Bug. If they don't, let it go.

### Workaround description → Feature
"Every month I have to manually download each report one by one and merge them in Excel" — this is a feature request for batch export, even though the user didn't ask for anything. The pain is the signal.

### Multiple classes in one input → Split
"The export is broken AND we should add CSV support" — that's a Bug (broken export) and a Feature (CSV support). Create two issues.

### "We should really..." → check scope
- "We should really refactor the auth module" → Tech Debt (specific component)
- "We should really rethink our entire auth strategy" → too strategic for an issue. Suggest a Project.

### Duplicate with different severity → comment, don't create
If an open issue says "Search is slow" and the new input says "Search is completely broken for accounts with >10k records," that's the same root issue with new severity information. Add a comment to the existing issue with the new details and suggest bumping priority.

### Feature request that's actually a bug in disguise
"Can we add a loading spinner to the reports page?" — if the reports page currently shows a blank white screen for 8 seconds, the real issue is the performance bug. File the bug, not the spinner feature.

---

## Worked Examples

### 1. Clear Bug
**Input:** "The calendar widget won't load anymore. Started happening after yesterday's deploy. Getting a white screen with a console error about undefined properties."
**Class:** Bug
**Reasoning:** Specific broken behavior, temporal trigger (deploy), error message.

### 2. Clear Feature
**Input:** "Users keep asking if they can share dashboards with external stakeholders. Right now there's no way to share outside the org."
**Class:** Feature
**Reasoning:** Capability gap, user demand signal, no current workaround.

### 3. Clear Chore
**Input:** "Node 18 goes EOL in April, we need to upgrade to Node 20 across all services."
**Class:** Chore
**Reasoning:** Dependency lifecycle, mechanical upgrade, external deadline.

### 4. Clear Tech Debt
**Input:** "The payment processing code is scattered across 4 services with duplicated validation logic. Every pricing change requires touching all 4."
**Class:** Tech Debt
**Reasoning:** Coupling, duplication, maintenance cost.

### 5. Clear Question
**Input:** "Hey, does our API support pagination? I can't find it in the docs."
**Class:** Question
**Reasoning:** Seeking information, answerable from docs.

### 6. Clear Noise
**Input:** "UGH this codebase is such a mess, nothing makes sense"
**Class:** Noise
**Reasoning:** Emotional, no specific claim, no actionable request.

### 7. Borderline: Feature disguised as question
**Input:** "Is there a way to bulk-delete archived projects? I have 200 of them cluttering my sidebar."
**Class:** Feature
**Reasoning:** Interrogative form, but if bulk-delete doesn't exist, this is a feature request with clear user pain (clutter).

### 8. Borderline: Bug disguised as feature request
**Input:** "It would be nice if the search actually found results when I use quotes."
**Class:** Bug
**Reasoning:** "It would be nice" frames it as a wish, but quoted search is a standard feature — if it's not working, that's a bug.

### 9. Borderline: Vague but actionable
**Input:** "The onboarding flow feels really clunky."
**Class:** Ask one clarifying question
**Reasoning:** "Clunky" is too vague to act on. Ask: "Which step feels clunky, and what would you expect instead?"

### 10. Borderline: Workaround revealing a feature need
**Input:** "Every Friday I export all the tickets from Linear, paste them into a Google Sheet, and manually calculate the velocity metrics for the standup."
**Class:** Feature
**Reasoning:** The user didn't ask for anything, but the workaround reveals a need for built-in velocity reporting or at least a better export.

### 11. Multi-class input
**Input:** "Two things: the Slack integration is broken (no notifications since Monday) and we need to add a Webhook option for teams that don't use Slack."
**Class:** Split → Bug (Slack broken) + Feature (Webhook option)

### 12. Strategic ask, not an issue
**Input:** "I think we need to fundamentally rethink our approach to real-time collaboration. The current architecture won't scale to what we need for enterprise."
**Class:** Not an issue — suggest a Project or Initiative
**Reasoning:** Architectural rethink is roadmap-level, not task-level.

### 13. Chore vs. Tech Debt
**Input:** "We should consolidate the three different date formatting utilities into one."
**Class:** Tech Debt (not Chore)
**Reasoning:** This is about reducing duplication and maintenance burden, not a mechanical upgrade. Chores are usually "update X to Y."

### 14. Bug with vague repro
**Input:** "Login is broken for some users. Not sure which ones."
**Class:** Bug, but flag the missing repro
**Reasoning:** "Broken" + "login" is specific enough to be a bug, but the issue should note that reproduction steps are unknown and investigation is needed.

### 15. Feature request quoting a customer
**Input:** "Customer on Enterprise plan just wrote: 'We need SSO with Okta, our security team won't approve the tool without it. This is a dealbreaker for our renewal in March.'"
**Class:** Feature
**Reasoning:** Clear capability gap with business urgency. Preserve the quote verbatim — the "dealbreaker for renewal" context is critical.

### 16. Duplicate of existing issue
**Input:** "Search is really slow when you have a lot of results." (And there's an open issue: "Improve search performance for large result sets")
**Class:** Duplicate — add a comment to the existing issue
**Reasoning:** Same root concern. The new input adds a user voice that strengthens the existing issue.

### 17. Mixed feedback and noise
**Input:** "I love the new design but god the performance is terrible, it takes like 10 seconds to load the settings page. So frustrating."
**Class:** Bug (performance)
**Reasoning:** The emotional framing is noise, but "10 seconds to load settings page" is a specific, actionable performance bug.

### 18. Internal tooling request
**Input:** "Can we get a script that seeds the staging database with realistic test data? I'm tired of manually creating test accounts."
**Class:** Chore
**Reasoning:** Developer tooling improvement, mechanical task.

### 19. Too vague to act on
**Input:** "the dashboard thing"
**Class:** Not enough to create an issue
**Reasoning:** No verb, no context, no clear ask. Ask what they mean.

### 20. Security issue
**Input:** "I noticed that the API returns full user objects including hashed passwords in the /users endpoint response."
**Class:** Bug (security)
**Reasoning:** Data exposure is a bug, likely urgent. Consider flagging for elevated priority.
