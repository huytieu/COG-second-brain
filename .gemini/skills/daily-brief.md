# COG Daily Brief Playbook

## Goal
Generate a personalized news intelligence briefing with verified sources.

## Pre-Flight
1. Read `00-inbox/MY-INTERESTS.md` for topics and preferred sources
2. Read `00-inbox/MY-PROFILE.md` for role context and agent_mode
3. Read `03-professional/COMPETITIVE-WATCHLIST.md` for entities to track
4. If no interests file, suggest running `/onboarding` first

## Verification Standards (MANDATORY)
- All news MUST be from within the last 7 days
- Minimum 2 credible sources per claim
- Confidence levels explicitly stated (High/Medium/Low)
- Source credibility assessed: Tier 1 (major outlets), Tier 2 (trade press), Tier 3 (blogs/social)

## Steps

### 1. Research
Search for news across user's interest areas using web search tools. Prioritize:
- User's preferred sources (from MY-INTERESTS.md)
- Tier 1 and Tier 2 sources
- Topics directly relevant to user's role and projects

### 2. Verify & Filter
- Confirm dates are within 7 days
- Cross-reference claims across multiple sources
- Discard unverifiable or outdated information
- Assess strategic relevance to user's role

### 3. Analyze
For each story:
- Strategic relevance to user's interests/projects
- Opportunities and threats
- Competitive implications (if watchlist entities involved)
- Recommended actions

### 4. Generate Brief
Save to `01-daily/briefs/daily-brief-YYYY-MM-DD.md` with:
```yaml
type: daily-brief
created: YYYY-MM-DD
topics_covered: [list]
sources_count: N
confidence: high|medium|mixed
tags: ["#daily-brief", "#intelligence"]
```

Include sections: Top Stories, Industry Updates, Competitive Intelligence, Opportunities & Threats, Action Items
