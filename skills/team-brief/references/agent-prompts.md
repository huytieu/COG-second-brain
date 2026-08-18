# Team Brief — Phase 2 Agent Prompts

Verbatim sub-agent prompts for the six Phase 2 parallel data-collection agents. Referenced from SKILL.md's `### Phase 2: Parallel Data Collection` section — read this file once you're ready to fill in and dispatch the actual Task calls.

## github-analyst
```
Query GitHub for dev team activity on [CUSTOMIZE: your-org/your-repo].
Lookback start date: [INSERT LOOKBACK_DATE].
Today's date: [INSERT TODAY_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]

Run these gh CLI commands (all date filters use LOOKBACK_DATE as the start):

1. PRs merged since lookback:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state merged --search "merged:>=[LOOKBACK_DATE]" --json number,title,author,mergedAt,labels --limit 50

2. PRs opened since lookback:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state open --search "created:>=[LOOKBACK_DATE]" --json number,title,author,createdAt,labels --limit 20

3. ALL open PRs (for stale PR detection):
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state open --json number,title,author,createdAt,reviewDecision,labels,updatedAt --limit 50

4. PR review comments since lookback (to cross-reference with Slack discussions):
   gh api repos/[CUSTOMIZE: your-org/your-repo]/pulls/comments --jq '[.[] | select(.created_at >= "[LOOKBACK_DATE]")] | .[] | {pr_url: .pull_request_url, body: .body[0:200], user: .user.login, created_at: .created_at}'

5. Issues closed since lookback:
   gh issue list --repo [CUSTOMIZE: your-org/your-repo] --state closed --search "closed:>=[LOOKBACK_DATE]" --json number,title,labels --limit 20

6. Issues opened since lookback:
   gh issue list --repo [CUSTOMIZE: your-org/your-repo] --state open --search "created:>=[LOOKBACK_DATE]" --json number,title,labels --limit 20

7. Commits since lookback:
   gh api repos/[CUSTOMIZE: your-org/your-repo]/commits --jq '[.[] | select(.commit.author.date >= "[LOOKBACK_DATE]")] | .[] | {sha: .sha[0:7], message: .commit.message | split("\n")[0], author: .commit.author.name, date: .commit.author.date}'

ANALYSIS REQUIRED — Don't just list data, provide insights:

A) **Stale PR Detection**: Flag any open PR created more than 3 days ago with no review decision or with CHANGES_REQUESTED for more than 2 days. Calculate days since creation/last update.

B) **Velocity Snapshot**: How many PRs merged, commits pushed, contributors active. If Monday (weekend window), note the multi-day period and don't compare to a single-day baseline — instead comment on weekend activity level (busy weekend vs. quiet weekend).

C) **Review Bottleneck**: Count PRs waiting for review (REVIEW_REQUIRED). If >5, flag as bottleneck.

D) **PR Comment Themes**: Summarize the key topics being discussed in PR reviews (architecture concerns, bugs, design patterns, etc.)

Return structured data AND insights.
```

## slack-monitor
```
Check Slack [CUSTOMIZE: your-team-channel] channel for key discussions since [LOOKBACK_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]
If Monday: cover Friday through Sunday — there may be more threads than usual.

Instructions:
1. Use ToolSearch to load Slack tools
2. Read recent messages from [CUSTOMIZE: your-team-channel] channel (get enough to cover since [LOOKBACK_DATE])
3. For each significant discussion thread, extract:
   - Topic / what was discussed
   - Decisions made or agreements reached
   - Action items mentioned (who agreed to do what)
   - Blockers raised
   - Customer feedback or external links shared
   - Any specific features, PRs, or technical topics referenced

CRITICAL: For each action item or decision, note:
- WHO is responsible
- WHAT they agreed to do
- Whether it references a specific PR, feature, or technical area

Also extract:
- Links shared (competitive intel, articles, tools)
- Questions that were asked but NOT answered
- Discussions that seemed unresolved

Return structured output with clear separation between:
1. Decisions & Agreements (with responsible person)
2. Action Items (with owner)
3. Blockers & Escalations
4. Unresolved Discussions
5. External Links & Intel Shared
6. Feature/Technical Topics Discussed (for cross-referencing with GitHub)
```

## meeting-reviewer
```
Check for meeting notes and standup notes since [LOOKBACK_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]
If Monday: check Friday, Saturday, and Sunday for any meeting notes.

Instructions:
1. Look for meeting files in [CUSTOMIZE: path/to/meetings/] with dates from [LOOKBACK_DATE] through today
2. Use Glob to find files: [CUSTOMIZE: path/to/meetings/][LOOKBACK_DATE]*.md (and if Monday, also check Saturday and Sunday dates)
3. Also check [CUSTOMIZE: path/to/checkins/] for recent daily checkins
4. Read any found files

For each meeting/standup found, extract:
- Decisions made
- Action items assigned (WHO + WHAT)
- Features or changes discussed
- Priorities set
- Deadlines mentioned
- Any commitments like "I'll make a quick change to X" or "Let's update Y today"

Return structured list of:
1. Meeting summaries with date
2. All action items with owners
3. All discussed features/changes (for cross-referencing with GitHub PRs/commits and Linear issues)
4. Priorities and deadlines mentioned
```

## linear-tracker
```
Query Linear for work tracking data since [LOOKBACK_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]
If Monday: cover Friday through Sunday.

=== CONTEXT OPTIMIZATION RULES (CRITICAL — reduces token usage by ~70%) ===

**DEFAULT FILTERS — apply to ALL list_issues calls:**
- ALWAYS exclude issues with state "Done", "Completed", "Canceled", or "Archived" UNLESS they were updated since [LOOKBACK_DATE] (i.e., only show recently-completed wins, not old closed work).
- ALWAYS set limit: 50 on any list call to prevent overflow.
- NEVER make redundant queries — if you already fetched issues updated since lookback, do NOT re-fetch the same issues in a separate "completed" query. Filter from the data you already have.

**DATA EXTRACTION — from every API response, extract ONLY these fields per issue:**
- identifier (e.g., [CUSTOMIZE: PROJ]-123)
- title
- state (name only)
- priority (number + label)
- assignee (name only)
- updatedAt
- project (name only)
- labels (names only)

Discard everything else (full descriptions, URLs, metadata blobs, nested objects). This is critical — raw Linear responses are 50-100KB each and most of that data is unused.

**QUERY CONSOLIDATION — use minimal API calls:**
Do NOT make 5+ separate list_issues calls. Instead:

Instructions:
1. Use ToolSearch to load Linear tools (search "+linear list issues", "+linear list initiatives", "+linear list milestones", "+linear list projects")
2. Query the following data using Linear MCP tools:

   === ISSUE-LEVEL DATA (2-3 calls max) ===

   a) Issues updated since lookback (THE main query — covers most needs):
      Use mcp__claude_ai_Linear__list_issues with updatedAt: "[LOOKBACK_DATE]", limit: 50.
      From this ONE response, extract: recently completed issues (wins), issues that moved to In Progress, issues still in Todo, new issues created.

   b) High-priority/urgent + blocked issues (only if not already captured above):
      Use mcp__claude_ai_Linear__list_issues with priority: 1 (Urgent), limit: 30.
      Only query this separately if the main query didn't surface urgent items.

   c) Blocked/stuck issues:
      Look for issues with state "blocked" or "In Progress" with no updates in >2 days. Use the data from query (a) first — only make a separate query if needed.

   === CYCLE & SPRINT DATA (1 call) ===

   d) Current cycle progress:
      Use mcp__claude_ai_Linear__list_teams to get team IDs, then mcp__claude_ai_Linear__list_cycles with type: "current" for each team. This shows sprint/cycle health.

   === INITIATIVE DATA (1-2 calls) ===

   e) All active initiatives:
      Use mcp__claude_ai_Linear__list_initiatives with includeProjects: true to get initiative names, target dates, health status, progress, and linked projects.
      Do NOT call get_initiative for each individual initiative — the list call with includeProjects gives enough data.

   === PROJECT DATA (SKIP separate call) ===

   f) Project data comes from the initiatives query above (includeProjects: true). Do NOT make a separate list_projects call — it returns ~37KB of mostly unused data.

   === MILESTONE DATA (1 call only if needed) ===

   g) Only query milestones if an initiative is At Risk or has an approaching target date (≤14 days). Otherwise skip — milestone data is verbose and rarely actionable day-to-day.

3. For each significant issue, note ONLY:
   - Issue identifier, title, assignee name, status, priority, project name
   - Whether it has linked PRs (just note yes/no + PR number, don't include full URLs)

4. Build an INITIATIVE HEALTH MAP from the data you already have (do NOT make additional queries):
   For each initiative, compile:
   - Total issues across linked projects (completed / in-progress / todo / blocked)
   - Projects status breakdown
   - Key blockers
   - Days until target date

ANALYSIS REQUIRED:
A) **Cycle Health**: What % of the current cycle is complete? Are we on pace? How many issues remain vs. days left?
B) **Work Distribution**: Who has the most issues assigned? Anyone overloaded or idle?
C) **Blocked Items**: List anything stuck with reasons if available.
D) **Priority Mismatches**: Any urgent/high-priority issues with no recent activity? Flag them.
E) **New Work vs Planned**: How many issues were created since lookback vs. what was already planned in the cycle? Is scope creeping?
F) **Completed Work**: Celebrate — list what got done and by whom.
G) **Initiative Progress**: For each initiative, report health (on track / at risk / off track) based on:
   - % of issues completed vs. days remaining to target date
   - Number of blocked items
   - Whether projects under the initiative are progressing
H) **Milestone Status**: Only flag milestones that are overdue or at risk. Skip healthy milestones.
I) **Project Rollup**: For each project, summarize progress % and whether it's contributing to initiative goals.

Return structured data AND insights, including the initiative health map.
IMPORTANT: Your total output should be under 5KB of text. Summarize, don't dump raw data.
```

## braindump-reviewer
```
Check for recent braindumps since [LOOKBACK_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]
If Monday: check Friday through Sunday.

Instructions:
1. Use Glob to find braindump files matching recent dates:
   - [CUSTOMIZE: path/to/braindumps/]braindump-[LOOKBACK_DATE through TODAY]*.md
2. Read any found files

For each braindump found, extract:
- Core themes and strategic thinking
- Decisions being considered or made
- Product direction signals
- Concerns or risks flagged
- Ideas that should be connected to current work
- Any references to specific features, PRs, or team members

Return structured list of:
1. Braindump summaries with date and source
2. Strategic insights and product direction signals
3. Concerns/risks that should appear in the brief
4. Connections to current engineering work (for cross-referencing with GitHub/Linear)
```

## posthog-analyst
```
Query PostHog for HIGH-LEVEL product metrics only.
Project ID: [CUSTOMIZE: your-posthog-project-id], Dashboard ID: [CUSTOMIZE: your-posthog-dashboard-id].
Lookback start date: [INSERT LOOKBACK_DATE].
Today's date: [INSERT TODAY_DATE].
Brief type: [Daily Brief / Week Start Brief (Monday)]

=== CONTEXT OPTIMIZATION RULES (CRITICAL) ===
- DO NOT query for errors or error details. Skip list-errors entirely.
- DO NOT fetch insights-get-all (returns huge payload of all saved insights). Only use the dashboard.
- DO NOT include raw query results in your output. Summarize into 1-2 lines per metric.
- Your total output should be under 3KB of text.

Instructions:
1. Use ToolSearch to load PostHog tools (search "+posthog")
2. Run ONLY these queries:

   === DASHBOARD OVERVIEW (1 call) ===

   a) Get the main dashboard:
      Use mcp__posthog__dashboard-get with dashboard_id: [CUSTOMIZE: your-posthog-dashboard-id].
      Extract only: visitor count, signup count, core event count, and any trend data shown.

   === KEY METRICS (3 HogQL queries — combine into period comparison) ===

   b) Current period metrics (single combined query):
      Use mcp__posthog__query-run with a HogQL query:
      SELECT
        countIf(DISTINCT person_id, event = '$pageview') as visitors,
        countIf(event = '$pageview') as pageviews,
        countIf(DISTINCT person_id, event = 'user_signed_up') as signups,
        countIf(event = '[CUSTOMIZE: your_core_event]') as core_events,
        countIf(DISTINCT person_id, event = '[CUSTOMIZE: your_core_event]') as core_event_users
      FROM events
      WHERE timestamp >= '[LOOKBACK_DATE]'

   c) Previous period metrics (for % change calculation):
      Run the same query for the PREVIOUS equivalent period.
      If daily: day before lookback. If Monday (Fri-Sun): previous Fri-Sun.

   d) Top features (lightweight):
      Use mcp__posthog__query-run:
      SELECT event, count() as count, count(DISTINCT person_id) as unique_users
      FROM events
      WHERE timestamp >= '[LOOKBACK_DATE]' AND event NOT LIKE '$%'
      GROUP BY event ORDER BY count DESC LIMIT 10

ANALYSIS — Return ONLY high-level insights (no raw data dumps):

A) **Metric Summary**: 1 line each for visitors, sign-ups, core events with ↑↓→ trend and % change.
B) **Anomalies**: Only flag metrics with >20% change. If none, say "No anomalies."
C) **Top Features**: List top 5 features by usage, 1 line each.
D) **One-liner Assessment**: "Product health: [good/concerning/needs attention] — [why in 1 sentence]"

Return a concise summary, NOT raw query results. Target ~1KB output max.
```
