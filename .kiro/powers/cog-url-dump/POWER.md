---
name: "cog-url-dump"
displayName: "COG URL Dump"
description: "Quick capture URLs with automatic content extraction, insights, and categorization into knowledge booklets"
keywords: ["url dump", "save this link", "bookmark this", "save for later", "save url", "bookmark", "save link", "capture url"]
---

# COG URL Dump Power

Transform raw URLs into structured, insightful knowledge entries through intelligent content extraction, categorization, and integration with the user's knowledge base.

## When This Power Activates

- User shares a URL they want to save
- User mentions "save this link", "bookmark this", "url dump", "save for later"
- User pastes a URL and wants to capture it

## Pre-Flight Check

1. Check for `00-inbox/MY-PROFILE.md`
2. If found: Read interests and projects for auto-categorization
3. Check existing categories in `05-knowledge/booklets/`

## Process Flow

### 1. Input Collection

Accept URL(s) from user:
- Single URL or batch
- Optional user note about why they're saving it
- Any format: bare URL, markdown link, or with notes

### 2. URL Validation & Fetch

- Validate URL format
- Check if accessible
- Detect duplicates in existing knowledge base
- Fetch web page content

Extract:
- Page Title, Meta Description
- Author, Published Date (if available)
- Word Count, Read Time
- Main Content, Key Headings

### 3. Category Selection

**Default Categories:**
- Articles & Blogs
- Tools & Resources
- Reference & Documentation
- Research & Papers
- Inspiration & Design
- Videos & Media
- News & Updates
- Project-Specific (offer project list)
- To Review (unsure)

Auto-suggest category based on content, let user confirm or change.

### 4. Content Analysis

**Classification:**
- Content Category, Primary Topics, Tone
- Quality Assessment, Credibility Indicators

**Insight Extraction:**
- Executive Summary (2-3 sentences)
- Key Insights (3 items with context)
- Notable Quotes, Action Items

**Relevance Assessment:**
- User Interest Match (high/medium/low)
- Project Relevance
- Knowledge Gap filled
- Timeliness (evergreen/current/dated)

### 5. Generate Output

Create structured bookmark file with:
- YAML frontmatter (type, category, url, title, tags, relevance)
- Quick Summary
- Key Insights
- Why This Matters (connection to user's interests)
- Content Highlights
- Practical Takeaways
- Related Knowledge links
- Source Details table

### Tool/Resource Special Template

For tools and software, include:
- What It Does
- Key Features
- Use Cases
- Pricing
- Evaluation Status checklist

## Output Locations

- **Standard:** `05-knowledge/booklets/[category-slug]/[title-slug]-YYYY-MM-DD.md`
- **Project-specific:** `04-projects/[project-slug]/resources/[title-slug]-YYYY-MM-DD.md`
- **Unclear:** `00-inbox/url-[title-slug]-YYYY-MM-DD.md`

## Batch Processing

For multiple URLs, process and report:
```
1. [URL 1] → [category] → Saved to [path]
2. [URL 2] → [category] → Saved to [path]

Summary: X articles, Y tools saved
```

## Confidence Levels

- **High (90%+):** Clear content with obvious categorization
- **Medium (70-89%):** Generally clear with some ambiguity
- **Low (50-69%):** Significant ambiguity requiring user input
- **Very Low (<50%):** Major uncertainty, save to inbox

## Special Cases

- **Paywalled:** Note limitation, extract available preview
- **Dynamic Content:** Note content may change
- **Non-English:** Note language, provide translation if possible

## Success Metrics

- Speed of capture (< 30 seconds for single URL)
- Accurate categorization with user confirmation
- Useful insight extraction
- Proper integration with existing knowledge
- Easy retrieval and discovery later
