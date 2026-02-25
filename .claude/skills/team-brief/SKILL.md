---
name: team-brief
description: Generate daily team intelligence brief by cross-referencing GitHub, Linear, Slack, PostHog, meetings, and braindumps with two-way Linear sync-back
---

# COG Team Intelligence Brief Skill

## When to Invoke
- User says "team brief", "team update", "what did we ship", "standup prep"
- User wants to know what the dev team is working on
- User needs cross-referenced GitHub + Linear + Slack intelligence
- Morning routine for product/engineering leads

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use the full parallel agent execution strategy below (6 agents)
- If `agent_mode: solo` — run data collection sequentially in the main conversation. Skip Phase 3.5 (Linear sync-back) and Phase 3.7 (HackMD publish) to keep it fast.

## Purpose
Generate a concise daily team intelligence brief focused on what we're doing, what needs attention, and what's falling through the cracks. Cross-references Linear work tracking, Slack discussions, GitHub activity, PostHog product analytics, braindumps, and recent meetings to surface insights, flag mismatches, and keep the team aligned.

**Monday = Week Start Brief:** If today is Monday, the brief covers Friday through Sunday (the full weekend window). All date ranges, queries, and language should reflect "since Friday" / "over the weekend" instead of "yesterday." This captures anything that happened Friday afternoon, weekend deploys, or async discussions.

**This is NOT an industry news report.** News/market intelligence belongs in the weekly brief.

## Command: `/team-brief`

## Voice & Tone

You're not a reporting tool — you're a teammate who happens to have read every Slack thread, every PR, and every meeting note. Write like someone who genuinely cares about the team succeeding.

**Do:**
- Be direct and opinionated. If something looks off, say it plainly.
- Celebrate wins. When the team ships something great, acknowledge it.
- Connect the dots. Don't just list facts — explain why they matter together.
- Use natural language. "We shipped v1.2.0 with 11 PRs — solid day" not "11 PRs were merged across the reporting period."
- Be concise but warm. Short sentences, clear thinking, no fluff.
- Flag risks honestly. "This worries me" or "worth keeping an eye on" — not corporate hedging.
- Show you understand the business context. Reference growth targets, customer feedback, strategy when relevant.

**Don't:**
- Write like a project management dashboard. No "REPORT_GENERATED_AT" energy.
- Be overly formal. No "It is recommended that the team consider..."
- Add filler. If there's nothing to say, don't pad it.
- Be passive. "The PR remains unreviewed" → "Nobody's reviewed this yet — it's been 3 days."
- Use unnecessary labels or tags. Let the writing speak for itself.

**Example tone:**
> Good day yesterday — we cut v1.2.0 with the new workflow, caching fix, and a bunch of UX polish. 11 PRs merged by 4 people. The team is shipping.
>
> But we have a problem: two discovery calls in a row ended with the prospect unable to log in. The onboarding flow just doesn't work. We're building features for users who can't get through the front door.

---

## Parallel Agent Team Execution Strategy

**The daily brief MUST use parallel agents to maximize speed and efficiency.**

When `/daily-brief` is invoked, the orchestrator (main agent) should:

### Phase 1: Setup (Orchestrator — Sequential, Fast)
1. Determine today's date and the **lookback start date**:
   - **If today is Monday:** lookback = last Friday (3 days ago). Set `LOOKBACK_DATE` to Friday's date. This is a **Week Start Brief**.
   - **Any other day:** lookback = yesterday. Set `LOOKBACK_DATE` to yesterday's date. This is a standard **Daily Brief**.
   - All dates in YYYY-MM-DD format.
2. Check available integrations via ToolSearch ("slack"), ToolSearch ("linear"), and ToolSearch ("posthog")
3. Check for meeting notes in `[CUSTOMIZE: path/to/meetings/]` matching dates from `LOOKBACK_DATE` through today
4. Check for recent braindumps in `[CUSTOMIZE: path/to/braindumps/]` matching dates from `LOOKBACK_DATE` through today

### Phase 2: Parallel Data Collection (Spawn 6 Agents Simultaneously)
**Launch ALL of these agents in a single message using the Task tool with `run_in_background: true`:**

#### Agent 1: "github-analyst" (subagent_type: general-purpose)
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

#### Agent 2: "slack-monitor" (subagent_type: general-purpose)
*Only spawn if Slack MCP is available*
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

#### Agent 3: "meeting-reviewer" (subagent_type: general-purpose)
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

#### Agent 4: "linear-tracker" (subagent_type: general-purpose)
*Only spawn if Linear MCP is available*
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

#### Agent 5: "braindump-reviewer" (subagent_type: general-purpose)
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

#### Agent 6: "posthog-analyst" (subagent_type: general-purpose)
*Only spawn if PostHog MCP is available*
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

### Phase 3: Assembly & Cross-Reference Synthesis (Orchestrator — After All Agents Complete)

This is the most critical phase. The orchestrator must:

1. **Collect results** from all background agents using Read on their output files

2. **Cross-reference Linear ↔ GitHub** (the core alignment check):
   - Match Linear issues to corresponding PRs/commits (by title, description, or explicit references)
   - Flag Linear issues marked "In Progress" with NO corresponding PR or commit (work claimed but not started in code)
   - Flag PRs that have NO corresponding Linear issue (untracked work — could be fine, just note it)
   - Flag Linear issues marked "Done" but PR still open or unmerged (status mismatch)
   - Note issues where Linear priority doesn't match PR urgency (e.g., Urgent in Linear but PR unreviewed for days)

3. **Cross-reference Slack ↔ GitHub ↔ Linear**:
   - Match Slack discussion topics to related PRs/commits AND Linear issues
   - Combine related insights into unified items (e.g., "Credit system: [CUSTOMIZE: PROJ]-45 in progress + discussed in Slack 22 replies + PR #930 has CHANGES_REQUESTED")
   - Flag if Slack discussions mention work that has NO corresponding PR, commit, OR Linear issue
   - Flag if PRs exist that were NOT discussed in Slack (silent work — could be fine, just note it)

4. **Cross-reference Meetings ↔ GitHub ↔ Linear**:
   - Check if action items from yesterday's meetings/standups have corresponding PRs, commits, OR Linear issues
   - Flag any discussed changes with NO GitHub or Linear activity
   - Note completed action items (discussed AND shipped AND tracked)
   - Check if meeting-assigned priorities match Linear priority settings

5. **Cross-reference Braindumps ↔ Current Work**:
   - Connect strategic thinking from braindumps to active Linear issues and GitHub PRs
   - Surface braindump concerns that aren't reflected in any current tracked work
   - Flag if braindumps mention direction changes that contradict current sprint priorities

6. **Cross-reference Linear Cycle ↔ Overall Progress**:
   - Report cycle health (% complete, days remaining, pace)
   - Flag if scope is creeping (new issues added mid-cycle)
   - Highlight blocked items that are holding up cycle completion

7. **Cross-reference Initiatives ↔ Projects ↔ Issues**:
   - For each initiative, roll up project and issue data to compute real health:
     - Count completed vs total issues across all linked projects
     - Check if milestones are on track or overdue
     - Identify which projects are driving progress vs. stalled
   - Flag initiatives where computed health differs from reported health
   - Flag initiatives approaching target date with low completion %

8. **Cross-reference PostHog ↔ GitHub ↔ Slack**:
   - **Feature Releases ↔ Metrics**: Correlate recently merged PRs with PostHog metric changes. Did a feature ship and usage go up? Or did it ship and nothing changed (adoption problem)?
   - **Error Spikes ↔ Deployments**: Match PostHog error spikes to recently merged PRs. If errors increased after a specific merge, flag it as a potential regression.
   - **Slack Complaints ↔ PostHog Data**: If Slack discussions mention user issues, check if PostHog error data or funnel drop-offs confirm the problem.
   - **Metric Anomalies ↔ Known Changes**: If visitors/sign-ups changed significantly, cross-reference with GitHub activity and Slack.
   - **Feature Adoption ↔ Initiative Goals**: Map PostHog feature usage data to Linear initiative KPIs. Flag gaps.
   - **Activation Funnel ↔ Onboarding Work**: If the funnel is leaking, check if any PRs or Linear issues address it. Flag the gap if nothing is being worked on.

9. **Generate the brief** following the Content Structure below, with insights FIRST and details LAST. **Use the Voice & Tone guidelines** — write like a teammate, not a dashboard.

10. **Save** to `[CUSTOMIZE: path/to/briefs/]daily-brief-YYYY-MM-DD.md` with proper metadata

11. **Present** a concise summary to the user

### Phase 3.5: Linear Sync-Back (Orchestrator — After Cross-Reference, Before Slack)

**This phase writes data BACK to Linear to keep it up-to-date with reality from GitHub, Slack, and meetings.**

Use ToolSearch to load the necessary Linear update tools: "+linear update issue", "+linear update initiative", "+linear update project", "+linear create comment", "+linear create attachment", "+linear save status update", "+linear update milestone".

#### Step 1: PR ↔ Issue Linkage
For each merged or open PR found in the GitHub data:
1. Extract Linear issue references from PR title/body/branch (patterns: `[CUSTOMIZE: PROJ]-123`)
2. For each matched Linear issue:
   - Use `mcp__claude_ai_Linear__create_attachment` to attach the PR URL to the issue (if not already linked). Use format:
     - url: `https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX`
     - title: "PR #XXX: [PR title]"
   - Check if the issue already has this PR attached (via `get_issue` attachments) — skip if already linked to avoid duplicates

#### Step 2: Issue Status Sync from GitHub
Based on the cross-reference data from Phase 3:
1. **PR merged → Issue still "In Progress"**: Use `mcp__claude_ai_Linear__update_issue` to transition the issue to "Done" state. Add a comment: "Automatically marked done — PR #XXX merged on [date]."
2. **PR opened → Issue still "Todo"/"Backlog"**: Use `mcp__claude_ai_Linear__update_issue` to transition to "In Progress". Add a comment: "Marked in progress — PR #XXX opened."
3. **PR has CHANGES_REQUESTED → Issue marked "In Review"**: Keep issue status, but add a comment noting the review feedback if not already commented.

**Safety rules:**
- Only auto-transition issues where the PR-to-issue link is unambiguous (exact issue prefix match)
- Never transition issues backward (e.g., don't move "Done" back to "In Progress")
- If multiple PRs reference the same issue, only mark "Done" when ALL related PRs are merged
- Log every status change made for the brief summary

#### Step 3: Initiative Status Updates
For each active initiative, compose and post a status update using `mcp__claude_ai_Linear__save_status_update`:
1. Gather from the cross-reference:
   - What shipped since lookback (merged PRs mapped to this initiative's projects)
   - Current blockers across the initiative's projects
   - Cycle progress for the initiative's issues
   - Key Slack discussions relevant to this initiative
2. Compose a concise status update (3-5 bullet points):
   ```
   **[DATE] Daily Update**
   • Shipped: [list key PRs/features merged]
   • In Progress: [key items being worked on]
   • Blocked: [any blockers, or "None"]
   • Health: [On Track / At Risk / Off Track] — [1-line reasoning]
   • Next: [what's expected to ship next]
   ```
3. Use `mcp__claude_ai_Linear__save_status_update` to post the update to the initiative
4. If the initiative health has clearly changed based on data, use `mcp__claude_ai_Linear__update_initiative` to update the health field

#### Step 4: Milestone Progress Check
For each milestone in active projects:
1. Count completed vs total issues within the milestone
2. If a milestone's target date is approaching (≤7 days away) and completion is <70%, flag it
3. If a milestone is overdue (past target date with incomplete issues), use `mcp__claude_ai_Linear__update_milestone` to update its status/description with a note
4. Include milestone health in the initiative status update

#### Step 5: Project Status Sync
For each active project:
1. If all issues in a project are "Done" and the project status is still "In Progress", flag for status update
2. If a project has >50% blocked issues, note this in the initiative status update
3. Update project descriptions or summaries only if there's a significant status change

#### Sync-Back Summary
After all sync-back operations, compile a summary of what was updated:
- Issues status-synced: [count] (list issue IDs and new states)
- PRs linked: [count] (list PR#→issue mappings)
- Initiative updates posted: [count]
- Milestones flagged: [count]
- Any errors encountered during sync

Include this summary in the brief under a "Linear Sync Report" section.

### Phase 3.7: HackMD Publish (After Linear Sync-Back, Before Slack)

**This phase publishes the full daily brief to HackMD so it can be shared with the team via a link.**

The HackMD API token is stored in `.claude/settings/hackmd-token` (one line, no whitespace). Read it with: `cat .claude/settings/hackmd-token | tr -d '\n'`. Alternatively check env var `HACKMD_API_TOKEN`.

**API Details:**
- Base URL: `https://api.hackmd.io/v1`
- Auth header: `Authorization: Bearer <HACKMD_API_TOKEN>`

**Steps:**

1. **Create the note** via `POST https://api.hackmd.io/v1/notes` with:
   ```json
   {
     "title": "Daily Brief — [DAY_NAME], [FULL_DATE]",
     "readPermission": "signed_in",
     "writePermission": "owner",
     "commentPermission": "disabled",
     "content": "placeholder"
   }
   ```
   - `readPermission: "signed_in"` means any HackMD user with the link can view
   - Extract the `id` and `publishLink` from the response

2. **Update the note content** via `PATCH https://api.hackmd.io/v1/notes/<id>` with the full brief markdown content:
   - Read the saved brief from `[CUSTOMIZE: path/to/briefs/]daily-brief-YYYY-MM-DD.md`
   - Use Python to JSON-encode the content and write to a temp file
   - Send via `curl -X PATCH ... -d @/tmp/hackmd-payload.json`

3. **Store the HackMD link** for use in the Slack message AND the local brief file:
   - The `publishLink` from step 1 (format: `https://hackmd.io/@[CUSTOMIZE: your-hackmd-username]/<shortId>`)
   - This link will be included in the Slack highlight message
   - **Write the link back into the local `.md` file's frontmatter** by adding/updating `hackmd_url: <publishLink>` in the YAML frontmatter. Insert it after the `created:` field. Use the Edit tool to do this — do NOT rewrite the entire file.

4. **If HackMD API fails**, log the error and continue — the brief should still be posted to Slack without the link. Note in the Slack message: "(HackMD link unavailable)"

**Implementation pattern (Bash):**
```bash
# Step 1: Create note
curl -s -X POST 'https://api.hackmd.io/v1/notes' \
  -H "Authorization: Bearer $HACKMD_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"...","readPermission":"owner","writePermission":"owner","commentPermission":"disabled","content":"placeholder"}'

# Step 2: Prepare payload and update
python3 -c "
import json
with open('[CUSTOMIZE: path/to/briefs/]daily-brief-YYYY-MM-DD.md') as f:
    content = f.read()
with open('/tmp/hackmd-payload.json', 'w') as f:
    json.dump({'content': content}, f)
"
curl -s -X PATCH "https://api.hackmd.io/v1/notes/<id>" \
  -H "Authorization: Bearer $HACKMD_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d @/tmp/hackmd-payload.json
```

### Phase 4: Slack Highlights (After brief is saved — preview before posting)

After presenting the brief summary to the user, **always compose and show the Slack highlight message for preview**. Display the exact message the user will see in Slack, then ask: "Ready to post this to #[CUSTOMIZE: your-team-channel]? (or edit anything first)"

**Do NOT post until the user explicitly confirms.** If they suggest edits, adjust and show the updated preview. Only post after they say yes/confirm/looks good/send it/etc.

1. **Compose a Slack-native highlight message** — NOT the full brief, just the most important bits the team should see. Keep it short enough that people actually read it.

2. **Once user confirms**, use ToolSearch to load Slack send tool, then post via `mcp__claude_ai_Slack__slack_send_message` to the [CUSTOMIZE: your-team-channel] channel.

3. **Slack message format** (adapt based on actual content — this is a template, not a rigid format):

**For Monday (Week Start Brief):**
```
:calendar: *Week Start Brief — [DATE] (covering Fri–Sun)*

*Weekend recap:* [X] PRs merged since Friday. [Brief summary of what got done.] :rocket:

*What shipped:*
• [Feature/PR 1 with <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> link] — [1-line description]
• [Feature/PR 2 with link] — [1-line description]
• [Feature/PR 3 with link] — [1-line description]

---

:rotating_light: *Heads up:*
• [Most important alert with PR links and context]
• [Second alert — include who's involved and what's needed]
• [Third alert if relevant]

---

:mag: *Key discussions from Slack:*
• *[Topic 1]:* [2-3 sentence summary of the discussion, decisions made, and any open questions.]
• *[Topic 2]:* [Summary with context]

:clipboard: *Open action items:*
• [Person] — [What they need to do] ([source: meeting/Slack thread])
• [Person] — [What they need to do]

---

:bar_chart: *Product pulse:*
• [X] visitors ([↑/↓X%]), [X] sign-ups, [X] core events ([↑/↓X%]) | [Any notable anomaly]

:chart_with_upwards_trend: *This week's focus:*
• [Key priority or theme for the week]

:zap: *Quick wins:*
• <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> and <...|#YYY> are approved — just need someone to merge.

:link: *Full brief:* [HACKMD_PUBLISH_LINK]
```

**For regular days:**
```
:newspaper: *Daily Brief — [DATE]*

*What shipped:* [X] PRs merged. :rocket:
• [Feature/PR 1 with <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> link] — [1-line description]
• [Feature/PR 2 with link] — [1-line description]

---

:rotating_light: *Heads up:*
• [Alert 1 with PR links, context, and who needs to act]
• [Alert 2 with details]

---

:mag: *Key discussions:*
• *[Topic]:* [2-3 sentence summary — what was discussed, any decisions, open questions.]

:clipboard: *Action items:*
• [Person] — [Task] ([from meeting/Slack])

---

:bar_chart: *Product pulse:* [X] visitors ([↑/↓X%]) | [X] core events ([↑/↓X%]) | [Any notable anomaly]

:zap: *Quick wins:*
• <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> and <...|#YYY> are approved — just need someone to merge.

:link: *Full brief:* [HACKMD_PUBLISH_LINK]
```

4. **Rules for the Slack message:**
   - Max 30 lines for Monday briefs, max 20 lines for regular days. More detail than before, but still scannable.
   - Lead with the positive (what shipped) before the problems.
   - Only include alerts that actually need the team's attention today.
   - Don't dump raw PR tables, but DO list shipped PRs with 1-line descriptions so people know what actually changed.
   - Summarize key Slack discussions — the team often misses threads. A 2-3 sentence recap of important conversations adds real value.
   - Include action items with owners so people know what's expected of them.
   - Use plain language, no project-management-speak. "Nobody's reviewed #930 yet" not "REVIEW_REQUIRED status persists."
   - If there's nothing urgent, keep it short: "Good day, we shipped X, nothing on fire."
   - Reference specific people only when it's constructive (celebrating a win or when they're the clear owner of a follow-up). Don't publicly call people out for missing deadlines.
   - **ALWAYS embed GitHub links for PR references.** Use Slack link format: `<https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX>`. Never use bare `#930` — make it clickable.
   - **ALWAYS include the HackMD link** at the end of the Slack message as `:link: *Full brief:* [HACKMD_URL]`. This is how the team accesses the full detailed brief.

### Phase Timing
- Phase 1: ~10 seconds
- Phase 2: ~60-90 seconds (all 6 agents run in parallel)
- Phase 3: ~45 seconds (6-way cross-referencing and assembly, including PostHog ↔ GitHub correlation)
- Phase 3.5: ~30-45 seconds (Linear sync-back — PR linkage, status sync, initiative updates)
- Phase 3.7: ~10 seconds (HackMD publish — create private note, upload full brief content)
- Phase 4: ~10 seconds (Slack post with HackMD link, after user confirms)
- **Total: ~3-4 minutes** (+ Slack post if requested)

---

## Content Structure (PRIORITY ORDER — Important First, Details Last)

### 1. Opening (1-2 sentences)
Quick vibe check. Was it a good shipping day? Quiet? Lots of discussion but no merges? Set the context in plain language.

**If Monday (Week Start Brief):** Frame the opening around the weekend + set the tone for the week ahead. Example: "Happy Monday — the team stayed busy over the weekend with 6 PRs merged. Here's what happened since Friday and what's on deck for the week."

**Regular day example:**
> Solid day — v1.2.0 shipped with 11 PRs merged. The team is moving fast on features. But we've got a growing problem on the onboarding side that needs attention before we lose more prospects.

### 2. Heads Up (Top Alerts)
Things that need attention today. Keep to 3-5 max. Write them as things a teammate would flag in standup, not as system alerts.

**Types (in priority order):**
- Initiative health degradation (initiative moved from On Track to At Risk, or milestone overdue)
- Blocked/urgent Linear issues with no progress
- Stale PRs (open > 3 days without review, or CHANGES_REQUESTED > 2 days)
- Linear ↔ GitHub status mismatches (e.g., Linear says "Done" but PR still open)
- Milestone approaching deadline with low completion (≤7 days, <70%)
- Missing follow-through (discussed in meeting/Slack but no GitHub/Linear activity)
- Review bottlenecks (>5 PRs waiting for review)
- Cycle health warnings (behind pace, scope creep)
- Mismatches between agreements and actions
- Unresolved blockers from Slack
- Critical bugs or issues
- PRs not linked to Linear issues (untracked work)
- PostHog error spikes correlated with recent deploys (potential regression)
- Significant metric drops (visitors, sign-ups down >20%)
- Funnel drop-offs with no corresponding Linear issue (untracked product gap)

**Example:**
> **Onboarding is broken** — Two prospects in a row got stuck at sign-up during discovery calls. No fix PR exists for either issue.
>
> **Review backlog is getting out of hand** — 22 open PRs, 16 of them stale. Some are 100+ days old. We should do a quick triage to close the dead ones.
>
> **API docs (#930)** need reviewer feedback resolved before we merge the implementation (#933). Let's not build on an uncertain foundation.

### 3. Key Insights (Synthesized, Cross-Referenced)
Combined intelligence from Slack + GitHub + Meetings. Group RELATED items together. This is where the cross-referencing shines — connect the dots between what was discussed and what actually happened in code.

### 4. What Shipped
Celebrate the wins. Brief summary of merged PRs. Group by theme if possible rather than just listing.

### 5. What's In Progress
Open PRs with review status AND corresponding Linear issue status. Flag age and anything that looks stuck. Show alignment between Linear status and actual PR state.

### 6. Initiative Health Dashboard
For each active initiative, show a quick-glance status:

**Format:**
> **Initiative Name** — Health: On Track | 23% complete | 76 days remaining
> - Projects: Project A (In Progress, 40%), Project B (In Progress, 15%)
> - Milestones: Milestone 1 (due Mar 15 — on track), Milestone 2 (due Mar 30 — at risk)
> - Shipped today: PR #945 (feature X), PR #948 (feature Y)
> - Blockers: None

### 7. Cycle & Sprint Health
Current Linear cycle progress — % complete, days remaining, scope changes. Flag if the team is on pace or falling behind.

### 8. Team Snapshot
Quick velocity numbers — not exhaustive, just enough to get a pulse. Include both GitHub metrics (PRs, commits) and Linear metrics (issues completed, cycle progress).

### 9. Product Metrics (from PostHog)
Quick snapshot of how the product is actually performing with real user data. This grounds the engineering activity in business reality.

**Format:**
> **Visitors:** 342 (↑12% vs previous day) | **Sign-ups:** 8 (↓25%) | **Core Events:** 156 (↑34%) | **Errors:** 3 new
>
> **What the numbers say:** Core events jumped after we shipped the loop detection fix (PR #942) — users are getting further into workflows without hitting errors. Sign-ups dipped but that might just be a quiet day.
>
> **Feature adoption:** `new-feature` used by 23 unique users (good early traction). `onboarding-flow` still showing 40% drop-off at email verification step.
>
> **Error watch:** 3 new `TypeError` errors in `/api/execute` since yesterday's deploy. Correlates with PR #935 merge.

**Rules:**
- Only include this section if PostHog data is available
- Always show trend direction (↑ ↓ →) with % change
- Correlate metric changes with shipped PRs when possible
- Flag error spikes and link them to recent deployments
- Keep it to 4-6 lines max — detailed analytics belong in a separate analysis

### 10. Linear Sync Report
Summary of what the daily brief sync-back updated in Linear:
- **Issues synced**: X issues had status updated (list issue IDs and new states)
- **PRs linked**: X PRs linked to Linear issues (list mappings)
- **Initiative updates posted**: X initiatives received status updates
- **Milestones flagged**: X milestones at risk or overdue
- **Errors**: Any sync failures (or "All clean")

### 11. Strategic Context (from Braindumps)
Key insights from recent braindumps that connect to current work. This gives the brief depth beyond just "what happened" — it adds "why it matters" from the product lead's own thinking.

### 12. Yesterday's Discussions (Reference)
Detailed Slack discussion summaries. This is the appendix — people who want depth can read here.

### 13. Meeting Follow-Up Tracker
Action items from recent meetings tracked against actual GitHub/Slack/Linear activity. Use status indicators to show progress at a glance.

---

## Metadata Template
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

## Synthesis Rules

### Cross-Referencing Logic
1. **Linear issue + corresponding PR** → Link them together in Linear (Phase 3.5). Flag status mismatches (e.g., Linear says "Done" but PR is still open)
2. **Linear issue "In Progress" + No PR/commit** → Flag as "claimed but no code yet" (could be early, but worth noting if >1 day)
3. **PR exists + No Linear issue** → Note as untracked work. Not necessarily bad, but should be in Linear going forward
4. **Slack topic mentions a PR number or Linear issue** → Link them together in Key Insights
5. **Slack discussion about a feature** + **PR and/or Linear issue exists** → Unified insight combining all three signals
6. **Meeting action item** + **No matching PR/commit AND no Linear issue** → Flag as missing follow-up (nothing tracked anywhere)
7. **Meeting action item** + **Linear issue exists but no PR** → Tracked but not started — note status
8. **Slack agreement** + **GitHub/Linear activity contradicts it** → Flag as mismatch
9. **Multiple Slack threads about same topic** → Consolidate into single insight
10. **Braindump mentions a feature/direction** + **Linear/GitHub has related work** → Connect strategic thinking to execution
11. **Braindump raises concern** + **No Linear issue or PR addressing it** → Flag as "strategic gap — thinking exists but no tracked work"
12. **Linear urgent/high-priority issue** + **No recent activity (>2 days)** → Flag as stalled critical work
13. **PR merged + Linear issue still open** → Auto-transition to "Done" in Phase 3.5 and note in sync report
14. **PR opened + Linear issue in "Todo"** → Auto-transition to "In Progress" in Phase 3.5
15. **Initiative target date approaching + low project completion** → Flag initiative health as "At Risk" and update in Linear
16. **Milestone overdue + incomplete issues** → Flag milestone and update in Linear
17. **Completed work maps to an initiative's project** → Include in initiative status update posted to Linear
18. **Merged PR + PostHog metric spike** → Correlate — the feature likely drove the change. Include in "What Shipped" with impact data
19. **Merged PR + PostHog error spike** → Flag as potential regression in Heads Up. Include error details and PR link
20. **PostHog sign-up/core-event drop + No obvious cause** → Flag as anomaly in Product Metrics. Check if it's a weekend/holiday pattern or a real problem
21. **PostHog feature low adoption + Related initiative targets growth** → Flag gap between what's being built and what users are actually using
22. **PostHog funnel drop-off + No Linear issue addressing it** → Flag as untracked product gap — users are struggling but nobody's working on it
23. **Slack user complaint + PostHog error data confirms** → Elevated priority — real user impact verified by data

### Stale PR Rules
- **> 3 days old** with REVIEW_REQUIRED → Flag as stale
- **> 2 days** with CHANGES_REQUESTED and no new commits → Flag as stale
- **> 5 days old** regardless of status → Flag as long-hanging
- Include link and responsible person in alert

### Initiative Health Rules
- **On Track**: ≥60% of expected pace (issues completed proportional to time elapsed vs target date), no critical blockers
- **At Risk**: 40-60% of expected pace, OR ≥2 blocked issues, OR milestone overdue
- **Off Track**: <40% of expected pace, OR ≥3 blocked issues across projects, OR multiple milestones overdue
- Health assessment uses REAL data (issue counts, milestone dates) not just reported status

### Priority Ordering
When multiple alerts exist, order by:
1. Initiative health degradation (initiative moved to At Risk or Off Track)
2. Blockers (Linear blocked issues or something that can't proceed)
3. PostHog error spikes correlated with recent deploys (potential regression — users affected NOW)
4. Milestone overdue or at risk (time-sensitive, affects initiative health)
5. Linear ↔ GitHub mismatches (status drift between systems)
6. Significant metric drops (visitors, sign-ups down >20% — could indicate a real problem)
7. Stale/aging PRs (time-sensitive, getting worse)
8. Missing follow-ups (commitments not met — no Linear issue AND no PR)
9. Cycle health warnings (behind pace, scope creep)
10. Review bottlenecks (slowing team velocity)
11. Strategic gaps (braindump concerns with no tracked work)
12. Funnel drop-offs with no tracked work (product gap)
13. Informational mismatches (good to know)

---

## Fallback Behavior
- **Slack unavailable**: Skip Slack sections, run GitHub + Linear + meetings only. Note: `slack: unavailable`
- **Linear unavailable**: Skip Linear sections, run GitHub + Slack + meetings. Note: `linear: unavailable`. Flag this — Linear is now the primary work tracker
- **PostHog unavailable**: Skip Product Metrics section, run other agents. Note: `posthog: unavailable`. The brief will still be useful without it.
- **No meetings found**: Skip meeting follow-up section, proceed with other sources
- **No braindumps found**: Skip strategic context section — this is optional enrichment, not critical
- **GitHub unavailable** (rare): Note error, skip dev activity
- **Never fabricate data** — if a query fails, say so explicitly

## Error Handling
- If gh CLI commands fail, report the error and skip that data point
- If Linear MCP tools fail, report the error and note which queries failed. Try individual queries even if batch fails
- If Slack MCP is slow, set a reasonable timeout and proceed without it
- If no meeting files found for yesterday, check day-before-yesterday as fallback
- If no braindump files found, skip silently — braindumps are written ad-hoc, not every day
- **Linear sync-back errors**: If a write-back operation fails, log the error in the sync report but do NOT retry aggressively — continue with remaining sync operations. The brief should still be generated even if some sync-back steps fail.
- **Duplicate prevention**: Before creating an attachment (PR link) on an issue, check existing attachments to avoid duplicates. Before posting an initiative status update, check if one was already posted today to avoid spam.
- **Status transition safety**: Never auto-transition an issue to a state that would lose information. If unsure about a transition, log it as "recommended" in the sync report rather than executing it.
