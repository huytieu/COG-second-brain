# Daily Brief Command

## Purpose
Generate personalized daily news briefing with verified, current information tailored to user's interests and strategic priorities.

## Command: `/daily-brief`

## Process Flow

### 1. Interest Analysis
- Scan user files to build/update interest profile
- Analyze recent braindumps and project activities
- Identify current strategic priorities and focus areas
- Update interest weighting based on recent patterns

### 2. News Curation (VERIFICATION REQUIRED)
- Search for verified news from **last 7 days ONLY**
- Cross-reference multiple credible sources
- Verify publication dates and source credibility
- Filter for strategic relevance to user's interests

### 3. Strategic Analysis
- Connect news to user's specific projects and goals
- Identify potential impacts on current initiatives
- Highlight opportunities and threats
- Generate strategic insights

### 4. Verification Protocol
- Confirm all dates are within last 7 days
- Verify sources are credible and cross-referenced
- If information cannot be verified, explicitly state uncertainty
- Ask user for clarification on unclear interests or priorities

### 5. Output Generation
- Save to `01-daily/briefs/daily-brief-YYYY-MM-DD.md`
- Include proper Obsidian metadata
- Structure for easy scanning and action
- Include clickable source links for ALL claims
- Add comprehensive Sources section

## Metadata Template
```yaml
---
type: daily-brief
domain: shared
date: YYYY-MM-DD
created: YYYY-MM-DD HH:MM
sources_verified: true
news_age_verified: true
confidence: high
tags: ["#daily-brief", "#news", "#strategic-intelligence"]
interests: [interest1, interest2, interest3]
projects_referenced: [project1, project2]
---
```

## Content Structure
1. **Executive Summary** - Key themes and priorities for the day
2. **Strategic News** - Verified news relevant to user's projects (with source links)
3. **Market Intelligence** - Industry trends and competitive landscape (with source links)
4. **Opportunities** - Notable insights and potential initiatives
5. **Risks & Threats** - Potential challenges requiring attention
6. **Follow-Up Actions** - Suggested next steps based on intelligence
7. **Sources** - Comprehensive categorized list of all referenced materials

## Verification Standards
- **News Age**: Must be from last 7 days with verified publication dates
- **Source Credibility**: Cross-reference minimum 2 credible sources
- **Source Attribution**: Every claim, statistic, and reference MUST include clickable source link
- **Statistical Verification**: ALL statistics must be verified by reading the cited source
  - Use WebFetch tool to retrieve and verify source content
  - If statistic cannot be found, DO NOT include it or find correct source
  - Document verification method in metadata
- **Uncertainty Handling**: Explicitly state when information cannot be verified
- **User Clarification**: Request clarification for ambiguous interests

## Error Handling
- If no recent news found, state explicitly rather than fabricate
- If sources cannot be verified, mark as unverified and explain
- If user interests are unclear, ask for clarification
- If external APIs fail, inform user and suggest manual verification

## Learning Integration
- Track which news types user engages with most
- Adapt content focus based on user feedback
- Build understanding of strategic priorities over time
- Refine interest profile automatically

## Quality Metrics
- All news from last 7 days (100% compliance)
- Minimum 2 source cross-references per major claim
- Strategic relevance score (based on user engagement)
- Actionability index (% of insights leading to action)

## Common Use Cases
- Morning intelligence briefing before workday starts
- Pre-meeting preparation with relevant industry context
- Competitive intelligence gathering
- Opportunity identification and threat monitoring
- Strategic decision support
