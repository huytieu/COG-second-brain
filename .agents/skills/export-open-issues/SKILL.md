---
name: export-open-issues
description: Audit and export open issues from any project tracker with summary analysis and vault archival
metadata:
  roles: product-manager,engineering-lead,founder
  integrations: github,linear,jira
  keywords: export issues,open issues,backlog audit,issue report,what's open,export open issues
  display-name: COG Export Open Issues
---

# COG Export Open Issues Skill

## When to Invoke
- User wants to audit open issues or backlog health
- User says "export issues", "open issues", "backlog audit", "issue report", "what's open"
- Sprint/cycle planning prep — need a clear picture of what's in flight
- Stakeholder reporting — need a snapshot of current work status

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use parallel agents to collect from all active trackers simultaneously and produce a unified report
- If `agent_mode: solo` — collect from the primary tracker sequentially

## Command: `/export-open-issues`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** to determine which trackers are active
2. **Read `00-inbox/MY-PROFILE.md`** for active projects
3. **Get current timestamp:** Run `date '+%Y-%m-%d %H:%M'` using Bash

4. **Ask the user** (if not already provided):
   - Which project? (if multiple active)
   - Scope: all open issues, or filtered by label/milestone/assignee?
   - Include additional analysis? (aging, priority distribution, assignee load)


## Execution Strategy

### Phase 1: Collect Open Issues

#### Team Mode (parallel agents)

Launch collection agents using the Task tool with `run_in_background: true`:

**Agent: "github-issues-collector"** (if GitHub is active)
```
Export all open issues from GitHub.
Repository: [CUSTOMIZE: your-org/your-repo]

1. Get all open issues:
   gh issue list --repo [CUSTOMIZE: your-org/your-repo] --state open --json number,title,author,assignees,labels,createdAt,updatedAt,milestone,url --limit 500

2. Get all open PRs (separate from issues):
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state open --json number,title,author,labels,createdAt,updatedAt,reviewDecision,url --limit 200

For each issue, calculate:
- Age in days (today - createdAt)
- Days since last update (today - updatedAt)
- Staleness flag: >30 days since last update = stale

Return: full issue list with calculated fields
```

**Agent: "linear-issues-collector"** (if Linear is active)
```
Export all open issues from Linear.

1. Use ToolSearch to load Linear tools
2. List all teams: mcp__claude_ai_Linear_2__list_teams
3. For each relevant team, list open issues: mcp__claude_ai_Linear_2__list_issues
4. Get current cycles: mcp__claude_ai_Linear_2__list_cycles
5. Get milestones: mcp__claude_ai_Linear_2__list_milestones

For each issue, collect:
- ID, title, status, priority, assignee, labels, project
- Created date, updated date
- Cycle membership
- Blocked status

Return: full issue list with metadata
```

**Agent: "jira-issues-collector"** (if Jira is active)
```
Export all open issues from Jira.
Project: [CUSTOMIZE: YOUR-PROJECT-KEY]

1. Search open issues:
   JQL: project = "[CUSTOMIZE: YOUR-PROJECT-KEY]" AND status NOT IN (Done, Closed, Resolved) ORDER BY priority DESC, created ASC

2. For each issue, collect:
   key, summary, issuetype, status, priority, assignee, reporter, labels, components, fixVersion, created, updated, duedate

Return: full issue list with metadata
```

#### Solo Mode
Run collection sequentially for the primary tracker.

### Phase 2: Analyze and Categorize

Process the collected data to produce:

#### 2.1 Summary Statistics
```
Total Open Issues: [N]
  - By Priority: Critical [N], High [N], Medium [N], Low [N], None [N]
  - By Type: Feature [N], Bug [N], Task [N], Other [N]
  - By Status: To Do [N], In Progress [N], In Review [N], Blocked [N]
  - By Assignee: [Name] ([N]), [Name] ([N]), Unassigned ([N])
```

#### 2.2 Health Indicators
- **Stale issues** (no update in >30 days): list with age
- **Unassigned issues**: list with priority
- **Blocked issues**: list with blocker details
- **Overdue issues** (past due date): list with days overdue
- **Oldest open issues**: top 10 by age
- **In-progress bottleneck**: issues in "In Progress" for >7 days

#### 2.3 Distribution Charts (text-based)
```
Priority Distribution:
  Critical  ████░░░░░░  12%
  High      ████████░░  38%
  Medium    ██████░░░░  28%
  Low       ████░░░░░░  22%

Age Distribution:
  <7 days   ██████████  45%
  7-30 days ██████░░░░  30%
  30-90 d   ███░░░░░░░  15%
  >90 days  ██░░░░░░░░  10%
```

### Phase 3: Generate Report

```markdown
type: open-issues-audit
project: [project-name]
date: [YYYY-MM-DD]
created: [YYYY-MM-DD HH:MM]
source: [github/linear/jira/multi]
tags: ["#issues-audit", "#[project-name]", "#backlog"]
summary:
  total_open: [N]
  critical: [N]
  high: [N]
  stale: [N]
  unassigned: [N]
  blocked: [N]
  oldest_days: [N]

# Open Issues Audit — [Project Name]

**Date:** [YYYY-MM-DD]
**Source:** [Tracker(s) used]
**Total Open Issues:** [N]


## Executive Summary

[2-3 sentences: overall backlog health, biggest concerns, and recommended actions]


## Summary Statistics

| Category | Count | % of Total |
|----------|-------|-----------|
| **By Priority** | | |
| Critical | [N] | [%] |
| High | [N] | [%] |
| Medium | [N] | [%] |
| Low | [N] | [%] |
| No Priority | [N] | [%] |
| **By Status** | | |
| To Do | [N] | [%] |
| In Progress | [N] | [%] |
| In Review | [N] | [%] |
| Blocked | [N] | [%] |
| **By Type** | | |
| Feature/Story | [N] | [%] |
| Bug | [N] | [%] |
| Task | [N] | [%] |
| Other | [N] | [%] |


## Assignee Load

| Assignee | Open Issues | Critical/High | In Progress | Oldest Issue (days) |
|----------|-------------|---------------|-------------|-------------------|
| [Name] | [N] | [N] | [N] | [N] |
| [Name] | [N] | [N] | [N] | [N] |
| Unassigned | [N] | [N] | — | [N] |


## Health Alerts

### Stale Issues (>30 days without update)
| # | Title | Assignee | Priority | Age (days) | Last Updated |
|---|-------|----------|----------|-----------|-------------|
| [#] | [Title] | [Name] | [Priority] | [N] | [Date] |

### Blocked Issues
| # | Title | Assignee | Blocked By | Days Blocked |
|---|-------|----------|-----------|-------------|
| [#] | [Title] | [Name] | [Reason] | [N] |

### Unassigned High-Priority Issues
| # | Title | Priority | Age (days) | Labels |
|---|-------|----------|-----------|--------|
| [#] | [Title] | [Priority] | [N] | [Labels] |

### Overdue Issues
| # | Title | Assignee | Due Date | Days Overdue |
|---|-------|----------|----------|-------------|
| [#] | [Title] | [Name] | [Date] | [N] |


## Full Issue List

### Critical Priority
| # | Title | Status | Assignee | Age | Labels | URL |
|---|-------|--------|----------|-----|--------|-----|
| [#] | [Title] | [Status] | [Name] | [N]d | [Labels] | [URL] |

### High Priority
[Same table format]

### Medium Priority
[Same table format]

### Low Priority
[Same table format]


## Recommendations

1. **[Recommendation 1]** — [Specific action with rationale]
2. **[Recommendation 2]** — [Specific action with rationale]
3. **[Recommendation 3]** — [Specific action with rationale]


*Generated by COG Open Issues Audit | [Date]*
```

### Phase 4: Save to Vault

Save to: `04-projects/[project]/audits/open-issues-YYYY-MM-DD.md`

```bash
mkdir -p "04-projects/[project]/audits"
```

### Phase 5: Present Results

Show the user:
1. Executive summary
2. Key health alerts (stale, blocked, unassigned)
3. Top recommendations
4. File location

Ask if they want:
- Full detailed view
- Export as CSV (generate a simple CSV file alongside the markdown)
- Share to a specific channel or wiki


## CSV Export (Optional)

If user requests CSV, generate alongside the markdown:

```
#,Title,Type,Status,Priority,Assignee,Labels,Created,Updated,Age(days),URL
[data rows]
```

Save to: `04-projects/[project]/audits/open-issues-YYYY-MM-DD.csv`


## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No tracker active | Inform user that a project tracker integration is needed; offer to set one up |
| Tracker API fails | Retry once, then report partial results with error note |
| Too many issues (>500) | Paginate collection, warn user, offer to filter by label/milestone/assignee |
| Multiple trackers active | Collect from all and produce a unified report, noting the source for each item |
| No open issues found | Report clean backlog status (this is good news!) |

## Error Handling

- **Rate limits**: Paginate requests and add delays if needed
- **Large payloads**: Summarize rather than list all items if >200 issues
- **Missing fields**: Mark as "N/A" rather than failing
- **Context overflow**: Process in batches, summarize per batch
