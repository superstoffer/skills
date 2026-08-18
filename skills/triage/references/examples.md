# Input → Issue Examples

Eight complete transformations showing what the skill produces from real-world inputs.

---

## 1. Slack bug report

### Input
> @channel heads up — the invoice PDF download has been broken since this morning. Clicking the download button does nothing. Tried Chrome and Firefox. Console shows a CORS error. Multiple customers have reported this in #support.

### Output

**Title:** Fix invoice PDF download CORS error

```markdown
**Repro:**
1. Open any invoice page
2. Click "Download PDF"
3. Nothing happens; console shows CORS error

**Expected:** PDF downloads successfully
**Actual:** Download silently fails. CORS error in console.
**Env:** Chrome and Firefox (both confirmed by reporter)

**Source:** #support — multiple customer reports since morning of [date]
```

**Labels:** Bug
**Priority:** High (multiple customers, revenue-adjacent feature)

---

## 2. Customer feedback via sales

### Input
> Hey team — just got off a call with Acme Corp (Enterprise, $180k ARR). Their IT lead said: "We've been waiting six months for SAML SSO. Our security policy requires it for all SaaS tools, and we have a compliance audit in Q3. If this isn't available by June we'll have to evaluate alternatives." Can we prioritize this?

### Output

**Title:** Add SAML SSO support

```markdown
**Problem:** Enterprise customers with strict security policies cannot adopt or retain the product without SAML SSO. Currently the only auth options are email/password and Google OAuth.

**Context:** Acme Corp ($180k ARR) has a Q3 compliance audit with a June hard deadline. This is a retention risk.

> "We've been waiting six months for SAML SSO. Our security policy requires it for all SaaS tools, and we have a compliance audit in Q3. If this isn't available by June we'll have to evaluate alternatives."

**Acceptance criteria:**
- [ ] SAML 2.0 SSO configuration available in admin settings
- [ ] Works with at least Okta and Azure AD
- [ ] Existing users can be migrated to SSO without losing data

**Source:** Sales call with Acme Corp IT lead, [date]
```

**Labels:** Feature

---

## 3. Meeting notes with multiple concerns

### Input
> Product sync notes 4/15:
> - Dashboard loading times have regressed, Sarah saw 8s load on the analytics page
> - We need to add team-level permissions before the Q3 enterprise push
> - The old onboarding flow can be removed, nobody's on it anymore
> - Jake asked about whether we support webhooks (we do, it's in the docs)
> - Someone mentioned we should "rethink our whole data pipeline" but no specifics

### Output

**Extracted concerns:**
1. Dashboard performance regression — **Bug**
2. Team-level permissions — **Feature**
3. Remove old onboarding flow — **Chore**
4. Webhook support question — **Question** (don't create, answer directly)
5. "Rethink data pipeline" — **Strategic** (roadmap-level, suggest a Project)

**Issue 1 — Title:** Fix analytics dashboard load time regression

```markdown
**Repro:** Open the analytics dashboard
**Expected:** Page loads in under 2 seconds (previous baseline)
**Actual:** 8-second load time observed by Sarah
**Env:** Not specified — needs investigation

**Source:** Product sync notes, 2026-04-15
```

**Labels:** Bug

**Issue 2 — Title:** Add team-level permissions

```markdown
**Problem:** No way to restrict access by team. All users see everything, which doesn't work for enterprises with multiple departments.

**Context:** Needed before Q3 enterprise push — this is a blocker for the enterprise sales motion.

**Acceptance criteria:**
- [ ] Admins can create teams and assign users
- [ ] Resources can be scoped to specific teams
- [ ] Users only see resources for their team(s)

**Source:** Product sync notes, 2026-04-15
```

**Labels:** Feature

**Issue 3 — Title:** Remove old onboarding flow

```markdown
**What:** Delete the legacy onboarding flow code and feature flag. All users have been migrated to the new flow.

**Why:** Dead code that adds maintenance surface and confusion when navigating the codebase.

**Source:** Product sync notes, 2026-04-15
```

**Labels:** Chore

**For concern 4:** "We do support webhooks — see [docs link]. You might reply to Jake directly."

**For concern 5:** Skipped — this is a strategic/roadmap-level ask, not an issue. Suggest creating a Project in Linear if someone has a concrete proposal. Could also warrant a dedicated discussion to scope the work before filing anything.

---

## 4. Vague feature request from stakeholder

### Input
> We need better reporting.

### Output

**Clarifying question:** "What reporting is falling short today? For example: are you missing specific metrics, is the data not exportable, or is the current UI hard to navigate? One sentence on what you're trying to accomplish would help me file the right issue."

(No issue created — too vague.)

---

## 5. Customer vent that contains a real bug

### Input
> I am SO frustrated with your product. Every single time I try to save a project it just spins forever and then loses all my work. I've lost HOURS of work this week. This is completely unacceptable. I'm seriously considering canceling.

### Output

**Title:** Fix project save hanging and data loss

```markdown
**Repro:**
1. Work on a project (adding/editing content)
2. Click save
3. Spinner appears indefinitely
4. Work is lost on reload

**Expected:** Project saves successfully within a few seconds
**Actual:** Save hangs indefinitely, unsaved work is lost

> "Every single time I try to save a project it just spins forever and then loses all my work. I've lost HOURS of work this week."

**Env:** Not specified — follow up with customer for browser/OS

**Source:** Customer complaint, [date]
```

**Labels:** Bug
**Priority:** Urgent (data loss)

---

## 6. Tech debt identified during code review

### Input
> Found during review of PR #847: the email sending logic is duplicated in three places — the signup flow, the password reset handler, and the invitation service. Each one constructs the SMTP connection differently. The invitation service doesn't even handle errors. We should consolidate this.

### Output

**Title:** Consolidate email sending into shared service

```markdown
**Problem:** Email sending logic is duplicated across signup, password reset, and invitation flows with inconsistent SMTP configuration and error handling. The invitation service has no error handling at all.

**Impact:** Any change to email behavior requires updating three locations. The missing error handling in invitations means failed sends are silent — users don't know their invitation wasn't delivered.

**Proposed direction:** Extract a shared email service that all three flows call into.

**Source:** Code review on PR #847
```

**Labels:** Tech Debt

---

## 7. Dependency upgrade with security context

### Input
> Dependabot flagged lodash 4.17.20 with a prototype pollution CVE (CVE-2021-23337). We're pinned to it in three packages.

### Output

**Title:** Upgrade lodash to patch CVE-2021-23337

```markdown
**What:** Bump lodash from 4.17.20 to latest in all three packages that pin it.

**Why:** CVE-2021-23337 (prototype pollution) — actively exploited vulnerability.

**Source:** Dependabot alert
```

**Labels:** Chore
**Priority:** High (security CVE)

---

## 8. Near-duplicate of existing issue

### Input
> "The search is basically unusable for our team. We have 15,000 projects and search takes 20+ seconds to return anything."

**Existing open issue found:** "Improve search performance for large workspaces" (filed 2 weeks ago, currently in Backlog)

### Output

**Recommendation:** Don't create a new issue. Add a comment to the existing issue:

```markdown
New report from a customer with 15k projects — search taking 20+ seconds.

> "The search is basically unusable for our team. We have 15,000 projects and search takes 20+ seconds to return anything."

This adds urgency to the existing issue. Consider bumping priority.
```

(Show the existing issue URL and ask the user whether to add the comment or create a separate issue.)
