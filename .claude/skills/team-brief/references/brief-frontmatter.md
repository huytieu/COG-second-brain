# Team Brief — Metadata Template

Verbatim YAML frontmatter template for the saved daily-brief markdown file, referenced from SKILL.md's `## Metadata Template` heading.

```yaml
---
type: daily-brief
brief_type: daily / week-start  # "week-start" if Monday, "daily" otherwise
domain: shared
date: YYYY-MM-DD
lookback_from: YYYY-MM-DD  # Friday's date if Monday, yesterday otherwise
created: YYYY-MM-DD HH:MM
tags:
  - daily-brief
  - team-intelligence
data_sources:
  github: true
  slack: true/false
  linear: true/false
  posthog: true/false
  meetings: true/false
  braindumps: true/false
linear_sync:
  issues_synced: X
  prs_linked: X
  initiative_updates_posted: X
  milestones_flagged: X
  errors: []
initiatives:
  - name: "[CUSTOMIZE: Your Initiative 1]"
    health: on_track / at_risk / off_track
    progress_pct: X
    days_remaining: X
    projects_count: X
    blocked_issues: X
  - name: "[CUSTOMIZE: Your Initiative 2]"
    health: on_track / at_risk / off_track
    progress_pct: X
    days_remaining: X
    projects_count: X
    blocked_issues: X
linear_cycle:
  name: "Cycle X"
  progress_pct: X
  days_remaining: X
  scope_changes: X  # issues added mid-cycle
posthog_metrics:
  visitors: X
  visitors_change_pct: X  # vs previous period
  signups: X
  signups_change_pct: X
  core_events: X
  core_events_change_pct: X
  new_errors: X
  top_feature: "feature_name"
  anomalies: []  # list of metrics with >20% change
hackmd_url: ""  # HackMD publish link, populated in Phase 3.7
stale_prs: X
review_bottleneck: true/false
missing_followups: X
linear_blocked_issues: X
---
```
