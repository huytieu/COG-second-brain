---
name: comprehensive-analysis
description: Deep-dive 7-day analysis across all data sources for weekly reviews, board prep, and strategic planning
roles: [product-manager, engineering-lead, founder]
integrations: [github, linear, slack, posthog]
---

# COG Comprehensive Analysis Skill

## When to Invoke
- User wants a weekly review or retro prep
- User says "weekly analysis", "comprehensive review", "board prep", "deep dive"
- User needs analysis across a longer time period (7+ days)
- User wants a full picture of team/product health

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use the full parallel agent execution strategy below (5 agents). This skill benefits greatly from team mode.
- If `agent_mode: solo` — run a lighter version: collect GitHub + Linear data sequentially, skip PostHog deep analysis, produce a single combined report instead of 3 documents.

## Purpose
Generate a deep-dive analysis across all data sources for weekly reviews, board prep, strategic planning, or any time you need the full picture. Unlike the team brief (which optimizes for speed and daily relevance), this skill intentionally pulls more data and spends more time synthesizing.

**Use this when:**
- Weekly team review / retro prep
- Board meeting or leadership update prep
- Strategic planning sessions
- Investigating a specific problem across all data sources
- Monthly/quarterly health check

**Don't use this daily** — it takes 8-12 minutes and pulls heavy payloads. Use `/daily-brief` for everyday intel.

## Command: `/comprehensive-analysis`

## Voice & Tone

Same as the daily brief — direct, opinionated, teammate energy. But with more depth and nuance. You're writing for a product leader who needs to make decisions, not just stay informed.

---

## Execution Strategy

### Phase 1: Deep Data Collection (~3-5 min)

**Launch ALL agents in parallel using the Task tool with `run_in_background: true`.**

#### Agent 1: "github-deep-analyst" (subagent_type: general-purpose)
```
Deep GitHub analysis for [CUSTOMIZE: your-org/your-repo].
Analysis period: last 7 days (from [7_DAYS_AGO] to [TODAY]).

Collect:
1. ALL PRs merged in the last 7 days:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state merged --search "merged:>=[7_DAYS_AGO]" --json number,title,author,mergedAt,labels,additions,deletions --limit 100

2. ALL open PRs with full detail:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state open --json number,title,author,createdAt,reviewDecision,labels,updatedAt,additions,deletions --limit 100

3. Contributor activity breakdown:
   For each contributor, count: PRs merged, PRs opened, commits, review comments given.
   gh api repos/[CUSTOMIZE: your-org/your-repo]/stats/contributors

4. Code frequency (additions/deletions per week):
   gh api repos/[CUSTOMIZE: your-org/your-repo]/stats/code_frequency

5. Commit activity by day:
   gh api repos/[CUSTOMIZE: your-org/your-repo]/stats/commit_activity

6. ALL PR review comments from the last 7 days:
   gh api repos/[CUSTOMIZE: your-org/your-repo]/pulls/comments --paginate --jq '[.[] | select(.created_at >= "[7_DAYS_AGO]")]'

DEEP ANALYSIS:
A) **Contributor Velocity Matrix**: For each contributor — PRs merged, lines changed, review comments given/received. Who's shipping? Who's reviewing? Who's doing both?
B) **Code Churn**: Are we rewriting the same files repeatedly? Flag files with >3 PRs touching them in one week.
C) **PR Lifecycle**: Average time from PR open → first review → merge. Where's the bottleneck?
D) **Review Quality**: Are reviews substantive (comments with suggestions) or rubber stamps (approved with no comments)?
E) **Week-over-Week Trends**: Compare this week's velocity to last week. Accelerating or decelerating?
F) **Technical Debt Signals**: Large PRs with no tests, PRs that touch >10 files, dependency-only PRs.

Return structured data AND insights.
```

#### Agent 2: "slack-deep-monitor" (subagent_type: general-purpose)
*Only spawn if Slack MCP is available*
```
Deep Slack analysis for last 7 days across key channels.
Analysis period: [7_DAYS_AGO] to [TODAY].

Instructions:
1. Use ToolSearch to load Slack tools
2. Read messages from [CUSTOMIZE: your-team-channel] for the full 7-day window
3. If you have access, also check: [CUSTOMIZE: additional-channels] (e.g., #general, #engineering, #product)

For EACH significant thread (>3 replies or involving decisions):
- Full topic summary
- Key participants
- Decision reached (or explicitly: "no decision reached")
- Action items with owners
- Sentiment (positive/negative/neutral/heated)
- Links to external resources shared

DEEP ANALYSIS:
A) **Communication Patterns**: Who's driving discussions? Who's mostly silent? Any asymmetry?
B) **Decision Velocity**: How many decisions were made vs. how many discussions ended without resolution?
C) **Topic Clustering**: Group discussions by theme (product, engineering, bugs, strategy, etc.)
D) **Unresolved Threads**: List all discussions that need follow-up — no decision, open question, blocked waiting for someone
E) **Sentiment Map**: Overall team mood. Are discussions constructive or frustrated?
F) **External Intel**: All links shared (articles, competitor news, tools) — categorize by relevance

Return structured data AND insights.
```

#### Agent 3: "linear-deep-tracker" (subagent_type: general-purpose)
*Only spawn if Linear MCP is available*
```
Deep Linear analysis for last 7 days.
Analysis period: [7_DAYS_AGO] to [TODAY].

Instructions:
1. Use ToolSearch to load ALL Linear tools
2. Collect comprehensive data:

   a) All issues updated in last 7 days (mcp__claude_ai_Linear__list_issues)
   b) All issues created in last 7 days
   c) All issues completed in last 7 days
   d) All blocked issues (any date)
   e) Full initiative list with projects (mcp__claude_ai_Linear__list_initiatives)
   f) Detailed status for each initiative (mcp__claude_ai_Linear__get_initiative)
   g) All active cycles (mcp__claude_ai_Linear__list_cycles)
   h) All milestones for active projects (mcp__claude_ai_Linear__list_milestones)
   i) All projects with progress (mcp__claude_ai_Linear__list_projects)
   j) Recent status updates (mcp__claude_ai_Linear__get_status_updates) for each initiative

DEEP ANALYSIS:
A) **Initiative Trajectory**: For each initiative, model whether current velocity will hit the target date. Use issues_completed_per_week vs. issues_remaining / weeks_remaining.
B) **Cycle History**: Compare current cycle progress to previous cycles. Are we improving?
C) **Scope Creep Quantified**: How many issues were added mid-cycle vs. planned at start?
D) **Priority Drift**: Issues that changed priority during the week. Why?
E) **Assignee Load Balance**: Distribution of issues across team members. Overloaded? Underutilized?
F) **Stale In-Progress**: Issues marked "In Progress" for >5 days with no status change.
G) **Dependency Map**: Issues that block other issues. What's the critical path?
H) **Label/Project Distribution**: Where is effort being spent? Does it align with initiative priorities?

Return structured data AND insights.
```

#### Agent 4: "posthog-deep-analyst" (subagent_type: general-purpose)
*Only spawn if PostHog MCP is available*

> **WARNING: PostHog can return very large payloads.** This agent is intentionally heavy — it's the reason this skill takes longer than the daily brief. Scope queries carefully.

```
Deep PostHog analysis for last 7 days.
Project ID: [CUSTOMIZE: your-posthog-project-id].
Analysis period: [7_DAYS_AGO] to [TODAY].

Instructions:
1. Use ToolSearch to load PostHog tools (search "+posthog")
2. Run these analyses:

   === CORE METRICS (7-day window) ===

   a) Daily visitors, sign-ups, and core events — broken out by day:
      Use mcp__posthog__query-run with HogQL:
      SELECT toDate(timestamp) as day, count(DISTINCT person_id) as unique_users, count() as events
      FROM events WHERE event = '$pageview' AND timestamp >= '[7_DAYS_AGO]'
      GROUP BY day ORDER BY day

   b) Same for sign-ups and core value events (separate queries)

   c) Week-over-week comparison:
      Compare [7_DAYS_AGO to TODAY] vs [14_DAYS_AGO to 7_DAYS_AGO]

   === FUNNEL ANALYSIS ===

   d) Key funnel (sign-up → first core action → repeat):
      Use mcp__posthog__insight-query or HogQL to build a funnel:
      - Step 1: user_signed_up
      - Step 2: [CUSTOMIZE: your_core_event] (first time)
      - Step 3: [CUSTOMIZE: your_core_event] (second time, >24h later)
      Compare this week's funnel to last week's.

   === FEATURE ADOPTION ===

   e) Feature usage matrix:
      SELECT event, count() as uses, count(DISTINCT person_id) as unique_users
      FROM events WHERE timestamp >= '[7_DAYS_AGO]' AND event NOT LIKE '$%'
      GROUP BY event ORDER BY unique_users DESC LIMIT 25

   f) New vs returning user behavior:
      Compare event types for users whose first_seen is within last 7 days vs. older users.

   === ERROR ANALYSIS ===

   g) Error trends:
      Use mcp__posthog__list-errors for the period. Group by error type.

   h) Error-to-deploy correlation:
      For each error spike, check the timestamp against known deploy times (from GitHub merged PR data).

DEEP ANALYSIS:
A) **Growth Trajectory**: At current rate, where will key metrics be in 30/60/90 days?
B) **Funnel Health**: Where do users drop off? Has it improved or degraded vs last week?
C) **Feature Value Matrix**: Which features correlate with retention? (users who use feature X come back more)
D) **New User Experience**: First-session behavior patterns. What do new users do? Where do they get stuck?
E) **Error Impact**: Which errors affect the most users? Which are increasing fastest?
F) **Engagement Segments**: Power users vs casual vs churned. How big is each segment?

Return structured data AND insights with trends.
```

#### Agent 5: "meeting-deep-reviewer" (subagent_type: general-purpose)
```
Review ALL meeting notes from the last 7 days.
Analysis period: [7_DAYS_AGO] to [TODAY].

Instructions:
1. Glob for ALL meeting files in [CUSTOMIZE: path/to/meetings/] from the last 7 days
2. Also check [CUSTOMIZE: path/to/checkins/] for daily checkins
3. Read all found files

For EACH meeting, extract the same items as the daily brief agent.

DEEP ANALYSIS:
A) **Action Item Completion Rate**: Of all action items assigned in meetings this week, how many have corresponding GitHub/Linear activity?
B) **Decision Log**: Comprehensive list of every decision made this week, with context and who made it.
C) **Priority Shifts**: Did priorities change during the week? Track what was said Monday vs. Friday.
D) **Commitment Tracking**: Did people do what they said they'd do? (Cross-reference with GitHub/Linear data)
E) **Meeting Effectiveness**: Are meetings producing decisions and action items, or just discussion?

Return structured data AND insights.
```

### Phase 2: Deep Synthesis (~2-3 min)

After all agents complete, the orchestrator performs deep cross-referencing:

1. **All 23 cross-reference patterns from the daily brief** (see daily-brief.md)

2. **Additional comprehensive patterns:**
   - **Week-over-week velocity trend**: Is the team accelerating or decelerating? Why?
   - **Initiative trajectory modeling**: At current pace, will each initiative hit its target? What needs to change?
   - **Team capacity assessment**: Based on actual output this week, what's realistic for next week?
   - **Risk register**: Compile all risks from all sources into a unified risk register with severity/likelihood/owner
   - **Strategic alignment check**: Is what the team is building aligned with what leadership discussed in meetings?
   - **Product-market signal synthesis**: Combine PostHog data + Slack user feedback + meeting customer discussions into a coherent product signal

3. **Generate three output documents:**

#### Output 1: Executive Summary (for leadership)
- 1-page max
- Key metrics with trends
- Initiative health dashboard
- Top 3 risks
- Top 3 wins
- Recommendation for next week's focus

#### Output 2: Team Report (for engineering)
- What shipped this week (celebrate!)
- Velocity and contributor stats
- Review health (bottlenecks, rubber stamps)
- Stale PRs and blocked issues
- Technical debt signals
- Next week's priorities from meetings

#### Output 3: Product Report (for stakeholders)
- User metrics with trends
- Funnel analysis
- Feature adoption
- Customer feedback synthesis (from Slack)
- Growth trajectory
- Product risks and opportunities

4. **Save** all three to `[CUSTOMIZE: path/to/briefs/]`:
   - `comprehensive-analysis-YYYY-MM-DD.md` (full report)
   - `executive-summary-YYYY-MM-DD.md` (leadership version)
   - `product-report-YYYY-MM-DD.md` (stakeholder version)

### Phase 3: Output & Distribution (~1-2 min)

1. Present the executive summary to the user
2. Offer to publish to HackMD (same pattern as daily brief Phase 3.7)
3. Offer to post highlights to Slack (same pattern as daily brief Phase 4)

---

## Metadata Template

```yaml
---
type: comprehensive-analysis
domain: shared
date: YYYY-MM-DD
analysis_period:
  start: YYYY-MM-DD
  end: YYYY-MM-DD
  days: 7
created: YYYY-MM-DD HH:MM
tags:
  - comprehensive-analysis
  - weekly-review
  - team-intelligence
data_sources:
  github: true
  slack: true/false
  linear: true/false
  posthog: true/false
  meetings: true/false
  braindumps: true/false
metrics:
  prs_merged: X
  prs_opened: X
  commits: X
  active_contributors: X
  issues_completed: X
  issues_created: X
  visitors: X
  visitors_wow_change_pct: X
  signups: X
  core_events: X
  new_errors: X
initiatives:
  - name: "[CUSTOMIZE: Initiative 1]"
    health: on_track / at_risk / off_track
    progress_pct: X
    trajectory: will_hit / at_risk / will_miss
    days_remaining: X
team_velocity:
  this_week: X  # PRs merged
  last_week: X
  trend: accelerating / stable / decelerating
risks:
  - severity: high/medium/low
    description: ""
    owner: ""
    source: ""
---
```

## Fallback Behavior

Same as daily brief — each data source is optional. The analysis degrades gracefully.

The minimum useful configuration is **GitHub only** — you'll still get velocity analysis, PR lifecycle metrics, contributor stats, and code churn detection.

## Error Handling

Same safety rules as the daily brief, with one addition:

- **Context overflow protection**: If any agent returns data that seems too large (>50k tokens estimated), log a warning and ask the agent to summarize more aggressively. This is most likely to happen with PostHog (large dashboard dumps) or Jira (broad JQL queries).
