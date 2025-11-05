---
name: daily-brief
description: Generate personalized news intelligence with verified sources (7-day freshness requirement)
---

# COG Daily Brief Skill

## Purpose
Find verified, relevant news for personalized daily briefings with strict verification standards and strategic relevance analysis tailored to user's specific interests and projects.

## When to Invoke
- User wants their daily news briefing
- User says "daily brief", "news", "what's happening", "morning brief"
- User wants to stay updated on their interests
- Morning routine or regular check-in time

## Pre-Flight Check

**Before executing, check for user profile:**

1. Look for `00-inbox/MY-PROFILE.md` and `00-inbox/MY-INTERESTS.md` in the vault
2. If NOT found:
   ```
   Welcome to COG! Daily briefs work best when personalized.

   Let's quickly set up your profile (takes 2 minutes).

   Would you like to run onboarding first, or should I generate a general brief?
   ```
3. If found:
   - Read `MY-INTERESTS.md` to get topics for news curation
   - Read `MY-PROFILE.md` to get user's name and active projects
   - Read `03-professional/COMPETITIVE-WATCHLIST.md` if exists for competitive tracking
   - Use topics to curate relevant news
   - Connect news to user's active projects when relevant

## Process Flow

### 1. Gather Context

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

### 2. News Research and Curation

Apply comprehensive news research methodology:

#### Interest-Based Research
- Search based on user's current interest profile
- Focus on strategic relevance to user's role and projects
- Identify emerging patterns and developments
- Diversify sources for balanced perspective

#### Verification Standards (MANDATORY)

**Date Verification:**
- ALL news MUST be from last 7 days ONLY
- Verify publication dates with verified timestamps
- NEVER include older news without explicit disclosure

**Source Credibility Assessment:**
- **Tier 1 Sources (Highest Credibility):** Major news organizations (Reuters, AP, Bloomberg, WSJ, NYT), official company announcements, government statements
- **Tier 2 Sources (High Credibility):** Industry publications, credible tech/business blogs, research reports from reputable firms
- **Tier 3 Sources (Moderate - Verify Carefully):** Social media from verified accounts, company blogs, community discussions
- Minimum 2 credible sources for any claim
- Cross-reference key facts and figures

**Fact Cross-Reference:**
- Verify claims across multiple independent sources
- Use WebFetch to verify any statistics before including them
- Identify potential bias and provide balanced perspective

#### Strategic Relevance Analysis

Assess impact on user:

**Direct Impact (High Priority):**
- News directly affecting user's projects or companies
- Regulatory changes affecting user's industry
- Competitive moves by direct competitors
- Technology developments affecting user's tech stack

**Strategic Impact (Medium Priority):**
- Market trends affecting user's target customers
- Investment patterns in user's industry
- Talent market changes affecting hiring
- Partnership opportunities or threats

**Contextual Impact (Lower Priority):**
- Broader economic trends affecting business climate
- Technology trends affecting future planning
- Industry thought leadership and opinion
- Educational content for professional development

#### Opportunity and Threat Identification

**Opportunities:**
- Market Opportunities: New markets or customer segments opening
- Technology Opportunities: New tools or platforms to leverage
- Partnership Opportunities: Potential collaboration partners
- Competitive Opportunities: Competitor weaknesses or market gaps

**Threats:**
- Competitive Threats: New competitors or competitive advantages
- Technology Threats: Disruptive technologies or obsolescence risks
- Market Threats: Market shifts or customer behavior changes
- Regulatory Threats: New regulations or compliance requirements

### 3. Generate Daily Brief

Create structured briefing document:

```markdown
---
type: "daily-brief"
curator: "news-curator"
domain: "shared"
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
sources_verified: true
news_age_verified: true
confidence: "high"
tags: ["#daily-brief", "#news", "#strategic-intelligence"]
interests: ["interest1", "interest2"]
projects_referenced: ["project1"]
items_count: [number]
---

# Daily Brief - [Date]

**Good [morning/afternoon], [Name]!**

## Executive Summary
[2-3 sentences highlighting the most important developments across all your interest areas]

---

## High Impact News

### [News Item 1 - Direct Impact]
**Relevance:** [Why this matters to you specifically]

[Detailed summary of the news]

**Impact Assessment:**
- **Projects Affected:** [Which of your projects this impacts]
- **Potential Effects:** [Specific implications]
- **Action Suggested:** [Recommended response or follow-up]

**Sources:**
- [Source Name 1] (Tier [1/2/3]) - [Publication Date] - [Link]
- [Source Name 2] (Tier [1/2/3]) - [Publication Date] - [Link]

**Confidence:** [High/Medium/Low] - [Reasoning]

---

### [News Item 2 - Direct Impact]
[Same structure as above]

---

## Strategic Developments

### [News Item 3 - Strategic Impact]
**Relevance:** [Why this matters strategically]

[Detailed summary]

**Strategic Implications:**
- [Implication 1]
- [Implication 2]
- [Implication 3]

**Sources:**
- [Source listings with credibility tiers and links]

**Confidence:** [High/Medium/Low] - [Reasoning]

---

## Market Intelligence

### [News Item 4 - Market Trends]
**Relevance:** [Why this market trend matters]

[Detailed summary]

**Market Impact:**
- [Impact on target customers]
- [Industry trends]
- [Investment patterns]

**Sources:**
- [Source listings with credibility tiers and links]

**Confidence:** [High/Medium/Low] - [Reasoning]

---

## Technology Watch

### [News Item 5 - Tech Developments]
**Relevance:** [Why this technology matters]

[Detailed summary]

**Technology Implications:**
- [Impact on tech stack]
- [New tools or platforms]
- [Emerging technologies]

**Sources:**
- [Source listings with credibility tiers and links]

**Confidence:** [High/Medium/Low] - [Reasoning]

---

## Competitive Landscape

### [Competitor/Company Name - From Watchlist]
**Recent Activity:**

[Summary of competitive intelligence gathered]

**Competitive Implications:**
- [What this means for your projects]
- [Opportunities or threats]
- [Recommended responses]

**Sources:**
- [Source listings with credibility tiers and links]

**Confidence:** [High/Medium/Low] - [Reasoning]

---

## Opportunities & Recommendations

### Immediate Actions (Today/This Week)
- [ ] [Specific action item 1]
- [ ] [Specific action item 2]
- [ ] [Specific action item 3]

### Research Needed
- [Area 1 requiring deeper investigation]
- [Area 2 to monitor closely]

### People to Inform/Consult
- [Stakeholder 1]: [About what]
- [Stakeholder 2]: [About what]

---

## Risks & Threats

### Active Threats
- **Threat 1:** [Description and mitigation approach]
- **Threat 2:** [Description and mitigation approach]

### Emerging Risks to Monitor
- [Risk 1 to watch]
- [Risk 2 to watch]

---

## Verification Report

### Source Analysis
- **Tier 1 Sources:** [count] - [list main ones]
- **Tier 2 Sources:** [count] - [list main ones]
- **Cross-References Performed:** [number]

### Fact-Checking Results
- **Verified Claims:** [count]
- **Unverified Claims:** [count with explanation if any]
- **Conflicting Information:** [count with resolution approach if any]

### Freshness Verification
- ✅ All news items verified within 7-day window
- Publication date range: [Oldest date] to [Newest date]

### Confidence Assessment
- **Overall Confidence:** [percentage]%
- **High Confidence Items:** [count]
- **Medium Confidence Items:** [count]
- **Low Confidence Items:** [count] - [reasons if any]

---

## Complete Sources

### Strategic News
1. [Full source citation with link]
2. [Full source citation with link]

### Market Intelligence
1. [Full source citation with link]
2. [Full source citation with link]

### Technology Watch
1. [Full source citation with link]
2. [Full source citation with link]

### Competitive Intelligence
1. [Full source citation with link]
2. [Full source citation with link]

---

*Curated by COG News Curator | All news verified within 7-day freshness window | Sources cross-referenced for accuracy*
```

Save to: `01-daily/briefs/daily-brief-YYYY-MM-DD.md`

### 4. Handle Special Cases

**When No Recent News Found:**
If no relevant news found in last 7 days for a particular interest area:

```markdown
### [Interest Area]
**No significant news found in last 7 days**

Last significant development was [date if known] regarding [topic if known].

**Suggestions:**
- Consider expanding search criteria
- Check [alternative sources suggested]
- This area may be experiencing a quiet period
```

**NEVER fabricate or use older news without explicit date disclosure.**

**When Information Cannot Be Verified:**
```markdown
### [Potential News Item]
**⚠️ Unable to verify from independent sources**

**Original Source:** [source] - Credibility: [assessment]

**What We Know:**
[What can be stated based on single source]

**What's Uncertain:**
[Specific claims that couldn't be verified]

**Recommendation:** Monitor for additional confirmation before acting

**Confidence:** Low - [reasoning]
```

**When Sources Conflict:**
```markdown
### [News Item with Conflicting Reports]
**⚠️ Conflicting information from multiple sources**

**Perspective 1:**
[Summary] - **Source:** [source with credibility tier]

**Perspective 2:**
[Summary] - **Source:** [source with credibility tier]

**Areas of Agreement:**
- [What sources agree on]

**Areas of Disagreement:**
- [Where sources conflict]

**Recommendation:** [Approach for resolution or further research]

**Confidence:** Medium - [reasoning]
```

### 5. Confirm Completion
- Confirm file was created
- Show user: "Daily brief saved to [file path]"
- Optionally show executive summary
- Ask if they want to explore any topic deeper or capture thoughts via braindump skill

## Integration with Other Skills

### Follow-up Actions
After daily brief, suggest:
- **braindump skill** - Capture thoughts sparked by news
- **weekly-checkin skill** - Reflect on news patterns over the week
- Project-specific analysis if news impacts active projects

## Performance Metrics

### Verification Quality
- Source Credibility Score: Average credibility rating of sources used
- Fact Accuracy Rate: Percentage of facts that remain accurate over time
- Cross-Reference Rate: Percentage of claims verified through multiple sources
- Date Accuracy: 100% compliance with 7-day freshness requirement (MANDATORY)

### Relevance Quality
- User Engagement: Percentage of news items user finds valuable
- Action Generation: Percentage of news items leading to user action
- Strategic Value: User assessment of strategic importance
- Timing Relevance: How well news timing aligns with user needs

## Learning and Adaptation

### Interest Profile Refinement
- Monitor which news items user finds most valuable
- Incorporate user feedback on relevance and importance
- Identify patterns in user interest evolution
- Anticipate interest changes based on project evolution

### Source Quality Learning
- Track accuracy of different sources over time
- Build understanding of source reliability patterns
- Learn to identify and account for source bias patterns
- Continuously improve source selection criteria

### Relevance Algorithm Improvement
- Improve ability to predict news impact on user
- Learn optimal framing for different types of news
- Better understanding of user's strategic context
- Improve identification of actionable news items

## Success Criteria
- All news within 7-day window (100% compliance)
- All sources verified and linked
- User finds briefing relevant and actionable
- Confidence levels clearly stated
- Opportunities and risks identified
- Follow-up actions suggested

## Philosophy

The daily brief skill embodies COG's verification-first approach:
- No AI hallucinations - everything sourced and verified
- Transparency in confidence levels
- Explicit uncertainty when information can't be verified
- User empowered to make informed decisions based on reliable intelligence
