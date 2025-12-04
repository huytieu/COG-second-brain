---
name: url-dump
description: Quick capture URLs with automatic content extraction, insights, and categorization into knowledge booklets
---

# COG URL Dump Skill

## Purpose
Transform raw URLs into structured, insightful knowledge entries through intelligent content extraction, categorization, and integration with the user's knowledge base. Quick capture with automatic insight generation.

## When to Invoke
- User shares a URL they want to save
- User says "save this link", "bookmark this", "url dump", or "save for later"
- User pastes a URL and wants to capture it
- User wants to organize web resources into their knowledge base

## Pre-Flight Check

**Before executing, check for user profile:**

1. Look for `00-inbox/MY-PROFILE.md` in the vault
2. If NOT found:
   ```
   Welcome to COG! It looks like this is your first time.

   Before we start, let's quickly set up your profile (takes 2 minutes).

   Would you like to run onboarding first, or should I proceed with default settings?
   ```
3. If found:
   - Read the profile to get user's interests and projects
   - Use interests to help with auto-categorization
   - Check for existing booklet categories in `05-knowledge/booklets/`

## Process Flow

### 1. User Interaction & Input Collection
- Accept URL(s) from the user (single URL or batch)
- Optionally accept user's quick note about why they're saving this
- Accept any format: bare URL, markdown link, or with notes

**Prompt:**
```
What URL(s) would you like to save?
(You can paste one or more URLs, optionally with a note about why you're saving it)
```

### 2. URL Validation & Fetch
- Validate URL format
- Check if URL is accessible
- Detect duplicate URLs in existing knowledge base
- Fetch the web page content

#### Content Extraction
Extract from the page:
- **Page Title:** [extracted-title]
- **Meta Description:** [if available]
- **Author:** [if detected]
- **Published Date:** [if detected]
- **Word Count:** [estimated]
- **Read Time:** [X minutes]
- **Main Content:** [extracted body text]
- **Key Headings:** [list of H1/H2s]

### 3. Category Selection

**Default Categories:**
- **Articles & Blogs:** Long-form content, tutorials, opinion pieces
- **Tools & Resources:** Software, utilities, services, APIs
- **Reference:** Documentation, specs, standards
- **Research:** Papers, studies, academic content
- **Inspiration:** Design, ideas, creative references
- **Videos & Media:** YouTube, podcasts, multimedia
- **News & Updates:** Industry news, announcements
- **Project-Specific:** Related to a specific project (offer project list from MY-PROFILE.md)
- **To Review:** Unsure, save for later categorization

**Custom Categories:**
- Check `05-knowledge/booklets/` for existing custom categories
- Offer to create new category if needed

**Auto-suggestion:** Based on content analysis, suggest the most likely category but let user confirm or change.

### 4. Content Analysis and Processing

#### Phase 1: Content Classification
Determine:
- **Content Category:** [article|tool|reference|research|video|news|etc]
- **Primary Topics:** [topic1, topic2, topic3]
- **Tone:** [informative|opinion|tutorial|news|etc]
- **Quality Assessment:** [high|medium|low]
- **Credibility Indicators:** [author credentials, citations, etc]

#### Phase 2: Insight Extraction
Generate:
- **Executive Summary:** [2-3 sentences]
- **Key Insights:**
  1. [Insight 1 with context]
  2. [Insight 2 with context]
  3. [Insight 3 with context]
- **Notable Quotes:** [if any stand out]
- **Action Items:** [practical takeaways]

#### Phase 3: Relevance Assessment
Analyze:
- **User Interest Match:** [high|medium|low] - [which interests from profile]
- **Project Relevance:** [project-name] - [why relevant]
- **Knowledge Gap:** [yes|no] - [what gap it fills]
- **Timeliness:** [evergreen|current|dated]
- **Uniqueness:** [novel|common|duplicate-adjacent]

#### Phase 4: Cross-Reference
Identify connections to:
- **Related Bookmarks:** [existing similar saves]
- **Related Braindumps:** [if content connects]
- **Related Projects:** [if applicable]
- **Suggested Tags:** [tag1, tag2, tag3]

### 5. Generate Structured Output

Create bookmark file with this structure:

```markdown
---
type: "url-bookmark"
category: "[category-name]"
domain: "[source-domain.com]"
date_saved: "YYYY-MM-DD"
date_accessed: "YYYY-MM-DD HH:MM"
url: "[original-url]"
title: "[page-title]"
author: "[author-if-available]"
published: "[publish-date-if-available]"
tags: ["#bookmark", "#category-tag", "#topic-tags"]
relevance: "[high|medium|low]"
status: "unread"
related_projects: ["project1", "project2"]
confidence: "[high|medium|low]"
---

# [Title]

## Quick Summary
[2-3 sentence summary of the content]

## Key Insights
- **Insight 1:** [description with context]
- **Insight 2:** [description with context]
- **Insight 3:** [description with context]

## Why This Matters
[Connection to user's interests/projects. What makes this worth saving?]

## User Note
[Original user note if provided, otherwise omit section]

## Content Highlights
[Key excerpts or quotes from the content - 200-400 words max]

## Practical Takeaways
- [ ] [Action item 1 if applicable]
- [ ] [Action item 2 if applicable]

## Related Knowledge
- **Similar Bookmarks:** [[bookmark1]], [[bookmark2]]
- **Connected Projects:** [[project1]]
- **Related Notes:** [[note1]], [[note2]]

## Source Details
| Field | Value |
|-------|-------|
| Domain | [domain] |
| Author | [author or "Unknown"] |
| Published | [date or "Unknown"] |
| Word Count | [~X words] |
| Read Time | [~X minutes] |

## Processing Notes
- **Extracted:** [timestamp]
- **Category Confidence:** [percentage]
- **Review Needed:** [yes|no] - [reason if yes]

---

*Processed by COG URL Curator*
```

Save to appropriate location:
- **Standard:** `05-knowledge/booklets/[category-slug]/[title-slug]-YYYY-MM-DD.md`
- **Project-specific:** `04-projects/[project-slug]/resources/[title-slug]-YYYY-MM-DD.md`
- **Mixed/Unclear:** `00-inbox/url-[title-slug]-YYYY-MM-DD.md`

### 6. Tool/Resource Special Handling

For tools and software, use enhanced template:

```markdown
---
type: "url-tool"
category: "tools"
domain: "[domain]"
url: "[url]"
title: "[tool-name]"
date_saved: "YYYY-MM-DD"
pricing: "[free|freemium|paid|enterprise]"
tags: ["#tool", "#category-tags"]
status: "to-evaluate"
---

# [Tool Name]

## What It Does
[1-2 sentence description]

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Use Cases
- Use case 1
- Use case 2

## Pricing
[Pricing details if available]

## Why It's Relevant
[Connection to user's work/interests]

## Evaluation Status
- [ ] Sign up / try demo
- [ ] Test key features
- [ ] Compare with alternatives
- [ ] Decision: [use|pass|revisit]

## Notes
[Space for user's evaluation notes]

---

*Processed by COG URL Curator*
```

### 7. Batch Processing

For multiple URLs:

```
Processing [X] URLs...

1. [URL 1] → [category] → Saved to [path]
2. [URL 2] → [category] → Saved to [path]
3. [URL 3] → [category] → Saved to [path]

Summary:
- Articles: 2 saved
- Tools: 1 saved
- Total: 3 URLs processed
```

### 8. Confirm Completion
- Confirm file(s) created
- Show user: "URL saved to [file path]"
- Show quick summary: title, category, key insight preview
- Ask if they want to:
  - Add another URL
  - Deep-dive into the content
  - Connect to specific project or braindump

## Booklet Structure

URLs are organized into "booklets" (category folders):

```
05-knowledge/
└── booklets/
    ├── articles/
    │   ├── _index.md (category overview - auto-created)
    │   └── [article-entries].md
    ├── tools/
    │   ├── _index.md
    │   └── [tool-entries].md
    ├── reference/
    │   ├── _index.md
    │   └── [reference-entries].md
    ├── research/
    │   ├── _index.md
    │   └── [research-entries].md
    ├── inspiration/
    │   ├── _index.md
    │   └── [inspiration-entries].md
    ├── videos/
    │   ├── _index.md
    │   └── [video-entries].md
    └── [custom-category]/
        ├── _index.md
        └── [entries].md
```

### Category Index Template

When creating a new category, also create an index file:

```markdown
---
type: "booklet-index"
category: "[category-name]"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
entry_count: 0
---

# [Category Name] Booklet

## Description
[What this category contains]

## Recent Additions
[Auto-updated list - most recent 10 entries]

## Top Entries
[Manually curated or most-accessed entries]

## Tags in This Category
[List of common tags used]

## Related Categories
- [[other-category-1]]
- [[other-category-2]]
```

## YAML Formatting Requirements

**CRITICAL:** All YAML frontmatter must use proper Obsidian-compatible formatting:
- All string values MUST be quoted with double quotes
- Arrays MUST use quoted strings: `["item1", "item2", "item3"]`
- URLs MUST be quoted to handle special characters
- Boolean values should NOT be quoted: `true` or `false`
- Ensure proper YAML syntax to prevent parsing errors in Obsidian

**Examples:**
```yaml
# CORRECT
type: "url-bookmark"
url: "https://example.com/path?query=value"
tags: ["#bookmark", "#article", "#ai"]
relevance: "high"
reviewed: false

# INCORRECT
type: url-bookmark
url: https://example.com/path?query=value
tags: [#bookmark, #article, #ai]
relevance: high
reviewed: "false"
```

## Verification Protocols

### Content Accuracy
- **Title Verification:** Ensure extracted title matches page
- **Author Attribution:** Verify author if stated
- **Date Accuracy:** Confirm publication date if shown
- **Summary Fidelity:** Ensure summary accurately represents content

### Categorization Verification
- **Category Fit:** Confirm content matches selected category
- **Tag Relevance:** Verify tags accurately describe content
- **Interest Alignment:** Confirm relevance assessment is accurate
- **Project Connection:** Verify project relevance if claimed

### Quality Checks
- **Completeness:** All required fields populated
- **Formatting:** Proper markdown and YAML syntax
- **Links:** All internal links valid
- **Metadata:** Frontmatter properly formatted

## Uncertainty Handling

### When Content is Unclear
- **Paywalled Content:** Note limitation, extract available preview
- **Dynamic Content:** Note if content may change
- **Complex Content:** Flag for manual review if needed
- **Non-English:** Note language, provide translation if possible

### Confidence Indicators
- **High Confidence (90%+):** Clear content with obvious categorization
- **Medium Confidence (70-89%):** Generally clear with some ambiguity
- **Low Confidence (50-69%):** Significant ambiguity requiring user input
- **Very Low Confidence (<50%):** Major uncertainty, save to inbox

Always explicitly state confidence levels and reasoning in processing notes.

## Integration with Other Skills

### Immediate Follow-up
After URL capture, suggest:
- `/braindump` - Capture thoughts about the URL
- `/knowledge-consolidation` - Integrate into knowledge frameworks
- Daily brief will surface relevant saved URLs

### Cross-Referencing
Automatically check for connections to:
- Active projects (from MY-PROFILE.md)
- Recent braindumps
- Competitive watchlist companies (if exists)
- User interests

## Success Metrics
- Speed of capture (< 30 seconds for single URL)
- Accurate categorization with user confirmation
- Useful insight extraction
- Proper integration with existing knowledge
- Easy retrieval and discovery later
- High confidence in extractions

## Learning and Adaptation

### Pattern Learning
- Track which bookmarks get revisited
- Learn user's categorization preferences
- Improve relevance scoring based on engagement
- Refine insight extraction based on what user finds useful

### Continuous Improvement
- Monitor categorization accuracy over time
- Adapt to user's preferred tag taxonomy
- Learn domain-specific terminology
- Improve cross-referencing accuracy
