---
name: "cog-generate-prd"
displayName: "COG Generate Prd"
description: "Generate product requirements documents with optional publishing to Confluence or other wiki platforms"
keywords: ["generate PRD", "write PRD", "product requirements", "spec doc", "feature spec", "generate prd"]
---


# COG Generate PRD Skill

## When to Invoke
- User wants to create a PRD, product spec, or requirements document
- User says "generate PRD", "write PRD", "product requirements", "spec doc", "feature spec"
- User has a feature or project that needs formal documentation before development

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use parallel agents to gather context from multiple sources (existing PRDs, related issues, competitive research) while drafting
- If `agent_mode: solo` — gather context and draft sequentially in the main conversation

## Command: `/generate-prd`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** to determine publishing options:
   - **Confluence** — can publish PRD to team wiki
   - **Notion** — can publish PRD to Notion workspace
   - **HackMD** — can publish PRD as shared markdown doc
   - If none active, PRD stays in the vault only (still fully useful)

2. **Read `00-inbox/MY-PROFILE.md`** for:
   - Active projects
   - User's name and role (for PRD author field)

3. **Get current timestamp:**
   Run `date '+%Y-%m-%d %H:%M'` using Bash for the `created:` frontmatter field


## Execution Strategy

### Phase 1: Gather Requirements

Ask the user for the following (skip what they've already provided):

**Required:**
- Feature/product name
- Problem statement — what problem are we solving?
- Target users — who is this for?
- High-level solution — what are we building?

**Optional (will generate reasonable defaults if not provided):**
- Success metrics — how do we measure success?
- Constraints — technical, time, budget, or regulatory constraints
- Dependencies — what does this depend on?
- Related documents — links to designs, research, prior art
- Target timeline — when does this need to ship?

### Phase 2: Context Gathering

#### Team Mode (parallel agents)

Launch context-gathering agents using the Task tool with `run_in_background: true`:

**Agent: "existing-prd-scanner"**
```
Scan the vault for existing PRDs and related documents.

1. Glob for PRDs: 04-projects/*/PRDs/*.md
2. Glob for related project files: 04-projects/[project]/**/*.md
3. Read recent PRDs to understand the user's preferred format and level of detail
4. Look for any existing docs related to the feature being specified

Return: relevant existing content, user's PRD style preferences, and any related docs
```

**Agent: "issue-context-gatherer"**
```
Gather related issues and feature requests from active trackers.

Check 00-inbox/MY-INTEGRATIONS.md for active trackers, then:

If Linear is active:
1. Use ToolSearch to load Linear tools
2. Search for issues related to [feature keywords]
3. Check current initiatives and projects for context

If GitHub is active:
1. gh search issues "[feature keywords]" --repo [CUSTOMIZE: your-org/your-repo] --json number,title,body,labels --limit 15
2. Check for related discussions or feature requests

Return: related issues, existing feature requests, and any prior discussion context
```

#### Solo Mode
Run the same context gathering sequentially.

### Phase 3: Generate PRD

Create the PRD using this template:

```markdown
type: prd
project: [project-name]
feature: [feature-name]
status: draft
author: [user name]
created: [YYYY-MM-DD HH:MM]
last_updated: [YYYY-MM-DD]
version: "1.0"
approvers: [CUSTOMIZE: list of approvers]
tags: ["#prd", "#product", "#[project-name]"]

# PRD: [Feature Name]

## Overview

| Field | Value |
|-------|-------|
| **Author** | [Name] |
| **Status** | Draft |
| **Created** | [Date] |
| **Target Release** | [Timeline or TBD] |
| **Priority** | [High/Medium/Low] |


## 1. Problem Statement

[Clear description of the problem being solved. Include data or evidence where available.]

### Who is affected?
[Target users and how they're impacted]

### What is the current experience?
[How users currently deal with this problem]

### Why now?
[Why this is important to solve at this time]


## 2. Goals & Success Metrics

### Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

### Success Metrics
| Metric | Current Baseline | Target | Measurement Method |
|--------|-----------------|--------|-------------------|
| [Metric 1] | [Current] | [Target] | [How to measure] |
| [Metric 2] | [Current] | [Target] | [How to measure] |

### Non-Goals
- [What this project explicitly does NOT aim to solve]
- [Scope boundaries]


## 3. User Stories

### Primary User: [User Type]

**Story 1:** As a [user type], I want [goal] so that [benefit].

**Story 2:** As a [user type], I want [goal] so that [benefit].

### Secondary User: [User Type] (if applicable)

**Story 3:** As a [user type], I want [goal] so that [benefit].


## 4. Proposed Solution

### 4.1 Solution Overview
[High-level description of the proposed solution]

### 4.2 Key Features
1. **[Feature 1]** — [Description]
2. **[Feature 2]** — [Description]
3. **[Feature 3]** — [Description]

### 4.3 User Flow
[Step-by-step description of the primary user flow]

1. User [action]
2. System [response]
3. User [action]
4. System [response]

### 4.4 Edge Cases & Error Handling
| Scenario | Expected Behavior |
|----------|------------------|
| [Edge case 1] | [How the system handles it] |
| [Edge case 2] | [How the system handles it] |


## 5. Technical Considerations

### Architecture Impact
[How this fits into the existing system architecture]

### Dependencies
- [Dependency 1] — [Status: available/needs work]
- [Dependency 2] — [Status: available/needs work]

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation plan] |

### Performance Requirements
- [Performance requirement 1]
- [Performance requirement 2]


## 6. Design & UX

[Link to designs or describe UX requirements]

### Key UX Principles
- [Principle 1]
- [Principle 2]

### Accessibility Requirements
- [Requirement 1]
- [Requirement 2]


## 7. Release Strategy

### Rollout Plan
- **Phase 1:** [Description] — [Timeline]
- **Phase 2:** [Description] — [Timeline]

### Feature Flags
- [Feature flag 1] — [Purpose]

### Rollback Plan
[How to roll back if issues arise]


## 8. Open Questions

- [ ] [Question 1] — Owner: [Name]
- [ ] [Question 2] — Owner: [Name]
- [ ] [Question 3] — Owner: [Name]


## 9. References

- [Link to related PRDs]
- [Link to designs]
- [Link to research]
- [Link to related issues/tickets]


## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

### Phase 4: Review Gate

**Present the generated PRD to the user:**

```
PRD draft is ready for review.

Sections generated:
1. Problem Statement
2. Goals & Success Metrics
3. User Stories
4. Proposed Solution
5. Technical Considerations
6. Design & UX
7. Release Strategy
8. Open Questions
9. References

Would you like to:
a) Review the full PRD (I'll display it)
b) Save as-is to the vault
c) Make changes to specific sections
d) Publish to [active wiki platform] (requires your approval)
```

**NEVER auto-publish. Always wait for explicit user approval.**

### Phase 5: Save to Vault

Save the PRD to: `04-projects/[project]/PRDs/prd-[feature-slug]-YYYY-MM-DD.md`

Create the directory structure if it doesn't exist:
```bash
mkdir -p "04-projects/[project]/PRDs"
```

### Phase 6: Publish (Optional, requires approval)

**Only proceed if the user explicitly approves publishing.**

#### Confluence
```
Use WebFetch to publish via Confluence REST API:
- POST /wiki/rest/api/content
- Space: [CUSTOMIZE: YOUR-SPACE-KEY]
- Parent page: [CUSTOMIZE: PRDs-parent-page-id]
- Title: "PRD: [Feature Name]"
- Body: [converted to Confluence storage format]

Note: Convert markdown to Confluence XHTML storage format before publishing.
```

#### Notion
```
1. Use ToolSearch to load Notion tools
2. Use mcp__claude_ai_Notion__notion-create-pages to create the PRD page
3. Place under [CUSTOMIZE: PRDs database or parent page]
```

#### HackMD
```
Use WebFetch to publish via HackMD API:
- POST to create a new note
- Set permissions as configured
```

After publishing, update the vault copy with the published URL:
```markdown
published_url: [URL]
published_at: [timestamp]
```


## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No wiki platform active | Save to vault only — PRD is still fully useful as a local document |
| Publishing API fails | Save to vault, provide the formatted content for manual publishing |
| User doesn't specify project | List active projects from MY-PROFILE.md and ask |
| Minimal input provided | Generate a skeleton PRD with [TODO] markers for the user to fill in |
| Existing PRD found for same feature | Ask if this is an update/revision or a new PRD |

## Error Handling

- **Context overflow**: If gathering too much context from existing docs, summarize rather than include full text
- **API failures**: Always save to vault first, then attempt publishing as a separate step
- **Large PRDs**: If the PRD exceeds typical wiki page limits, suggest splitting into sub-pages
