# Daily Brief Command

## Purpose
Generate personalized daily news briefing with verified, current information tailored to user's interests and strategic priorities.

## Command: `/daily-brief`

## Pre-Flight Check

**Before executing, check for user profile:**

1. Look for `00-inbox/MY-PROFILE.md` and `00-inbox/MY-INTERESTS.md` in the vault
2. If NOT found:
   ```
   Welcome to COG! Daily briefs work best when personalized.

   Let's quickly set up your profile (takes 2 minutes).

   Type '/onboarding' to get started, or I can generate a general brief.
   ```
3. If found:
   - Read `MY-INTERESTS.md` to get topics for news curation
   - Read `MY-PROFILE.md` to get user's name and active projects
   - Use topics to curate relevant news
   - Connect news to user's active projects when relevant

## Process Flow

This command orchestrates the daily brief generation by delegating to the specialized **news-curator** subagent.

### 1. Gather Context
**Your role (Claude Code):**

Collect the information needed for personalized curation:

- Read `00-inbox/MY-PROFILE.md` for:
  - User's name
  - User's role/job
  - Active projects

- Read `00-inbox/MY-INTERESTS.md` for:
  - Topics they're interested in
  - Preferred news sources

- Read `03-professional/COMPETITIVE-WATCHLIST.md` (if exists) for:
  - Companies/people to track

### 2. Delegate to News Curator Subagent
**Your role (Claude Code):**

Once you have the context, **delegate ALL news research and curation to the news-curator subagent**:

```markdown
**To news-curator subagent:**

Generate a personalized daily news briefing using your verification and curation framework:

**User Context:**
- Name: [from MY-PROFILE.md]
- Role: [from MY-PROFILE.md]
- Active Projects: [list from MY-PROFILE.md]

**Interest Areas:**
[Topics from MY-INTERESTS.md]

**Preferred News Sources:**
[Sources from MY-INTERESTS.md]

**Competitive Watchlist:**
[Companies/people from COMPETITIVE-WATCHLIST.md if it exists]

**Date:** [Today's date]

**Instructions:**
- Search for verified news from **last 7 days ONLY**
- Focus on topics from the user's interest areas
- Prioritize news relevant to their role and active projects
- Include competitive intelligence on watchlist items
- Cross-reference multiple credible sources
- Use WebFetch to verify any statistics before including them
- Include clickable source links for ALL claims

- Generate briefing with:
  - Executive Summary
  - Strategic News (relevant to projects/role)
  - Market Intelligence (industry trends)
  - Opportunities & Risks
  - Comprehensive Sources section

- Save to: `01-daily/briefs/daily-brief-YYYY-MM-DD.md`

- Use proper YAML frontmatter with quoted strings
- Ensure 100% compliance with 7-day freshness requirement
- Provide confidence assessment for all claims

Return the file path where you saved the brief.
```

### 3. Confirm Completion
**Your role (Claude Code):**
- Wait for subagent to complete research and curation
- Confirm file was created
- Show user: "Daily brief saved to [file path]"
- Optionally show executive summary
- Ask if they want to explore any topic deeper

## What NOT to Do

**Do NOT:**
- Search for news yourself
- Curate or analyze news yourself
- Create the output file yourself
- Verify sources yourself

**Instead:**
- Gather user context from profile files
- Delegate to news-curator subagent
- Confirm completion

## Verification Standards (Enforced by Subagent)

The news-curator subagent will:
- **News Age**: Only include news from last 7 days
- **Source Credibility**: Cross-reference minimum 2 credible sources
- **Source Attribution**: Include clickable links for ALL claims
- **Statistical Verification**: Use WebFetch to verify statistics
- **Uncertainty Handling**: Explicitly state when info can't be verified

## Output File Structure

The news-curator subagent creates files with this structure:

```markdown
---
type: "daily-brief"
domain: "shared"
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
sources_verified: true
news_age_verified: true
confidence: "high"
tags: ["#daily-brief", "#news", "#strategic-intelligence"]
interests: ["interest1", "interest2"]
projects_referenced: ["project1"]
---

# Daily Brief - [Date]

## Executive Summary
[2-3 sentences highlighting most important developments]

## Strategic News
### [News Item 1]
[With source links]

## Market Intelligence
### [Trend 1]
[With source links]

## Opportunities
[Actionable opportunities identified]

## Risks & Threats
[Potential challenges flagged]

## Sources
### Strategic News
- [Source 1 with link]
- [Source 2 with link]

### Market Intelligence
- [Source 3 with link]
```

## Error Handling

If news-curator subagent cannot find recent news:
- It will state explicitly: "No significant news found in [interest area] in last 7 days"
- It will never fabricate or use older news
- It will suggest expanding search criteria or alternative sources

## Integration with Other Commands

### Follow-up Actions
- `/braindump` - Capture thoughts sparked by news
- `/scout-project-analysis` - Analyze impact on specific project
- `/weekly-checkin` - Reflect on news patterns over the week

## Success Metrics
- Successful delegation to subagent
- File saved to correct location
- All news within 7-day window
- All sources verified and linked
- User finds briefing relevant and actionable
