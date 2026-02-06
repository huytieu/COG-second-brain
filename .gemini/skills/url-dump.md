# COG URL Dump Playbook

## Goal
Transform URLs into structured knowledge entries with automatic content extraction, insights, and categorization.

## Pre-Flight
1. Read `00-inbox/MY-PROFILE.md` for interests, projects, agent_mode
2. Read `00-inbox/MY-INTERESTS.md` for relevance assessment

## Steps

### 1. Accept URL(s)
User provides one or more URLs. Validate they are accessible.

### 2. Fetch & Extract
For each URL:
- Fetch page content
- Extract: title, author, publication date, main content
- Identify content type (article, tool, reference, research, video, etc.)

### 3. Categorize
Auto-assign to one of:
- Articles & Blogs
- Tools & Resources
- Reference & Documentation
- Research & Papers
- Inspiration & Design
- Videos & Media
- News & Updates
- Project-Specific (if relevant to an active project)

### 4. Analyze
Generate:
- **Summary** (2-3 sentences)
- **Key Insights** (3-5 bullet points)
- **Relevance** to user's interests and projects
- **Action items** if applicable: `- [ ] Task 📅 YYYY-MM-DD`
- **Related** links to existing vault content

### 5. Save
**Standard** → `05-knowledge/booklets/[category]/[title-slug]-YYYY-MM-DD.md`
**Project-specific** → `04-projects/[project-slug]/resources/[title-slug].md`
**Unclear** → `00-inbox/[title-slug].md`

File format:
```yaml
type: booklet
created: YYYY-MM-DD
source_url: [URL]
category: [category]
author: [if known]
tags: [auto-generated]
```

Include sections: Summary, Key Insights, Relevance, Full Notes, Source Info
