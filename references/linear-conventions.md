# Linear Workspace Conventions

Customize this file for your workspace. The skill reads it to set the right team, labels, and defaults when creating issues.

If this file is unconfigured, the skill will ask you to fill it in the first time you use it.

---

## Teams

Map your Linear teams here. The skill uses `default_team` unless the input clearly belongs elsewhere.

```yaml
default_team: ""          # e.g., "Engineering"
teams:
  # - name: "Engineering"
  #   id: ""              # Linear team ID (find in team settings URL)
  #   areas:              # What this team owns
  #     - "backend"
  #     - "API"
  #     - "infrastructure"
  #
  # - name: "Product"
  #   id: ""
  #   areas:
  #     - "roadmap"
  #     - "strategy"
  #
  # - name: "Design"
  #   id: ""
  #   areas:
  #     - "UI"
  #     - "UX"
  #     - "design system"
```

## Triage status

Does your default team have Triage enabled? New issues will be created in Triage if yes, Backlog if no.

```yaml
triage_enabled: true      # Set to false if your team doesn't use Triage
```

## Labels

### Type labels (one per issue)

These should match your workspace's existing label names exactly.

```yaml
type_labels:
  bug: "Bug"
  feature: "Feature"
  chore: "Chore"
  tech_debt: "Tech Debt"
  spike: "Spike"
```

### Area labels (at most one per issue, optional)

```yaml
area_labels:
  # - "Frontend"
  # - "Backend"
  # - "Mobile"
  # - "API"
  # - "Billing"
  # - "Auth"
  # - "Onboarding"
```

## Projects

Active projects that the skill should know about. If input clearly relates to one of these, the skill can suggest attaching the issue to the project.

```yaml
active_projects:
  # - name: "Q3 Enterprise Push"
  #   id: ""
  #   keywords: ["enterprise", "SSO", "permissions", "SAML", "SCIM"]
  #
  # - name: "Performance Sprint"
  #   id: ""
  #   keywords: ["performance", "speed", "latency", "loading"]
```

## Area contacts

People to @-mention in issue comments (not assignees) when an issue touches their area. This helps triage owners route issues.

```yaml
area_contacts:
  # frontend: "@sarah"
  # backend: "@jake"
  # billing: "@maria"
  # infrastructure: "@dev-ops"
```

---

## How to fill this in

1. **Teams:** Go to Linear Settings → Teams. Copy the team name and ID (visible in the URL).
2. **Labels:** Go to Settings → Labels. Copy the exact label names your workspace uses.
3. **Triage:** Check your team settings — if you see "Triage" as a workflow state, set `triage_enabled: true`.
4. **Projects:** List any currently active projects. The `keywords` help the skill match inputs to projects.
5. **Area contacts:** List who owns what. These are used for @-mentions in comments, not auto-assignment.

If your workspace uses different conventions (e.g., different label names for types), update the `type_labels` section to match.
