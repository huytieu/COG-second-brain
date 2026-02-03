---
name: "cog-daily-brief"
displayName: "COG Daily Brief"
description: "Generate personalized news intelligence with verified sources and 7-day freshness requirement"
keywords: ["daily brief", "news", "what's happening", "morning brief", "daily news", "intelligence briefing", "news update", "morning update"]
---

# COG Daily Brief Power

Find verified, relevant news for personalized daily briefings with strict verification standards and strategic relevance analysis tailored to user's specific interests and projects.

## When This Power Activates

- User wants their daily news briefing
- User mentions "daily brief", "news", "what's happening", "morning brief"
- Morning routine or regular check-in time

## Pre-Flight Check

1. Check for `00-inbox/MY-PROFILE.md` and `00-inbox/MY-INTERESTS.md`
2. If NOT found: Suggest onboarding or generate general brief
3. If found: Read interests, profile, and competitive watchlist

## Verification Standards (MANDATORY)

### Date Verification
- ALL news MUST be from last 7 days ONLY
- Verify publication dates with timestamps
- NEVER include older news without explicit disclosure

### Source Credibility Tiers
- **Tier 1 (Highest):** Reuters, AP, Bloomberg, WSJ, NYT, official announcements
- **Tier 2 (High):** Industry publications, credible tech/business blogs
- **Tier 3 (Moderate):** Verified social media, company blogs

### Fact Cross-Reference
- Minimum 2 credible sources for any claim
- Verify statistics before including
- Identify potential bias

## Strategic Relevance Analysis

### Direct Impact (High Priority)
- News directly affecting user's projects
- Regulatory changes in user's industry
- Competitive moves by direct competitors

### Strategic Impact (Medium Priority)
- Market trends affecting target customers
- Investment patterns in user's industry
- Partnership opportunities or threats

### Contextual Impact (Lower Priority)
- Broader economic trends
- Technology trends for future planning
- Industry thought leadership

## Output Structure

Generate comprehensive brief with:
- Executive Summary (2-3 sentences)
- High Impact News (direct impact items)
- Strategic Developments
- Market Intelligence
- Technology Watch
- Competitive Landscape (from watchlist)
- Opportunities & Recommendations
- Risks & Threats
- Verification Report (sources, fact-checking, freshness)
- Complete Sources list

## Output Location

`01-daily/briefs/daily-brief-YYYY-MM-DD.md`

## Special Cases

### No Recent News Found
```
**No significant news found in last 7 days**
Last significant development was [date] regarding [topic].
```

### Information Cannot Be Verified
Mark with warning, state what's uncertain, recommend monitoring.

### Sources Conflict
Present both perspectives, areas of agreement/disagreement, recommendation.

## Task Date Format

Action items use Obsidian Tasks emoji format with calculated due dates:
- **Today's actions:** `📅 [today's date]`
- **This week actions:** `📅 [end of week date]`

Example:
```markdown
### Immediate Actions (Today/This Week)
- [ ] Review competitor announcement 📅 2026-02-03
- [ ] Schedule team briefing 📅 2026-02-07
```

## Success Criteria

- All news within 7-day window (100% compliance)
- All sources verified and linked
- Confidence levels clearly stated
- Opportunities and risks identified
- Follow-up actions suggested with due dates
