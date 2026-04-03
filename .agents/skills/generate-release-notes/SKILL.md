---
name: generate-release-notes
description: Generate categorized release notes from any source (GitHub, Linear, Jira, or manual input) with optional publishing
metadata:
  roles: product-manager,engineering-lead,founder
  integrations: github,linear,jira,confluence,notion,hackmd
  keywords: release notes,changelog,what shipped,write release notes,generate release notes
  display-name: COG Generate Release Notes
---

# COG Generate Release Notes Skill

## When to Invoke
- User wants to create release notes for a version, sprint, or cycle
- User says "release notes", "changelog", "what shipped", "write release notes"
- A new version or milestone has been completed
- End of sprint/cycle documentation

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use parallel agents to collect data from all active sources simultaneously
- If `agent_mode: solo` — collect data sequentially from the primary tracker

## Command: `/generate-release-notes`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** to determine data sources and publishing options
2. **Read `00-inbox/MY-PROFILE.md`** for active projects
3. **Get current timestamp:** Run `date '+%Y-%m-%d %H:%M'` using Bash

4. **Ask the user** (if not already provided):
   - What version/release/cycle is this for?
   - What is the date range? (or: which milestone/cycle/sprint?)
   - Which project? (if multiple active)
   - Audience: internal team, customers, or both?


## Execution Strategy

### Phase 1: Collect Release Data

#### Team Mode (parallel agents)

Launch data collection agents using the Task tool with `run_in_background: true`:

**Agent: "github-release-collector"** (if GitHub is active)
```
Collect all merged PRs and release data for the specified version/period.
Repository: [CUSTOMIZE: your-org/your-repo]
Period: [START_DATE] to [END_DATE]

1. Get merged PRs in the period:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state merged --search "merged:[START_DATE]..[END_DATE]" --json number,title,author,labels,body,mergedAt --limit 200

2. Check for existing GitHub release (if version tag exists):
   gh release view [VERSION_TAG] --repo [CUSTOMIZE: your-org/your-repo] --json name,body,tagName,createdAt 2>/dev/null

3. Get commits between tags (if applicable):
   gh api repos/[CUSTOMIZE: your-org/your-repo]/compare/[PREV_TAG]...[CURRENT_TAG] --jq '.commits[] | {sha: .sha[:7], message: .commit.message, author: .author.login}'

Categorize each PR by its labels or title prefix:
- "feat"/"feature"/"enhancement" labels → Enhancements
- "fix"/"bug"/"bugfix" labels → Bug Fixes
- "tech"/"refactor"/"chore"/"infrastructure" labels → Technical Improvements
- "docs"/"documentation" labels → Documentation
- "security" labels → Security
- "breaking"/"breaking-change" labels → Breaking Changes
- "deprecation" labels → Deprecations

Return: categorized list of changes with PR numbers, titles, authors, and descriptions
```

**Agent: "linear-release-collector"** (if Linear is active)
```
Collect completed issues for the specified cycle/period.

1. Use ToolSearch to load Linear tools
2. List cycles: mcp__claude_ai_Linear_2__list_cycles
3. Find the target cycle or filter by date range
4. List all completed issues in the cycle/period: mcp__claude_ai_Linear_2__list_issues
5. For each issue, get details including labels and project

Categorize by label or issue type:
- Feature/Enhancement labels → Enhancements
- Bug labels → Bug Fixes
- Technical/Infrastructure labels → Technical Improvements
- Documentation labels → Documentation

Return: categorized list of changes with issue IDs, titles, assignees, and descriptions
```

**Agent: "jira-release-collector"** (if Jira is active)
```
Collect issues for the specified version/sprint.
Project: [CUSTOMIZE: YOUR-PROJECT-KEY]

1. Search by fixVersion:
   JQL: project = "[CUSTOMIZE: YOUR-PROJECT-KEY]" AND fixVersion = "[VERSION]" AND status = Done ORDER BY issuetype, priority DESC

   OR search by sprint:
   JQL: project = "[CUSTOMIZE: YOUR-PROJECT-KEY]" AND sprint = "[SPRINT_NAME]" AND status = Done ORDER BY issuetype, priority DESC

2. For each issue, collect: key, summary, issuetype, priority, assignee, labels, description

Categorize by issue type:
- Story/Feature → Enhancements
- Bug → Bug Fixes
- Task/Technical Task → Technical Improvements
- Documentation → Documentation

Return: categorized list with issue keys, titles, assignees, types, and descriptions
```

#### Solo Mode
Run the primary tracker collection sequentially.

#### Manual Input Fallback
If no tracker is active or the user prefers manual input:
```
No project tracker detected. You can provide release items manually.

Please list the changes in this release. I'll categorize them for you.
Format: one change per line, optionally prefix with [feature], [fix], [tech], [docs], [security], [breaking]
```

### Phase 2: Categorize and Organize

Organize collected items into standard categories:

1. **Breaking Changes** (always first if present)
2. **New Features & Enhancements**
3. **Bug Fixes**
4. **Technical Improvements**
5. **Security Updates**
6. **Documentation**
7. **Deprecations**
8. **Known Issues** (if any remain)

Within each category, order by:
1. Priority (highest first)
2. User impact (most impactful first)

### Phase 3: Generate Release Notes

#### For Customer/External Audience:

```markdown
type: release-notes
project: [project-name]
version: [version]
date: [YYYY-MM-DD]
created: [YYYY-MM-DD HH:MM]
audience: external
tags: ["#release-notes", "#[project-name]", "#v[version]"]
items_count: [total count]
categories:
  enhancements: [count]
  bug_fixes: [count]
  technical: [count]
  security: [count]
  breaking_changes: [count]

# Release Notes — [Project Name] [Version]

**Release Date:** [Date]

## What's New

[2-3 sentence executive summary of the most important changes in this release]


### Breaking Changes

> **Action Required:** The following changes may require updates to your workflow.

- **[Change title]** — [User-friendly description of what changed and what to do]


### New Features & Enhancements

- **[Feature title]** — [User-friendly description focused on the benefit to users]
- **[Feature title]** — [User-friendly description]

### Bug Fixes

- **[Fix title]** — [What was broken and how it's fixed, in user terms]
- **[Fix title]** — [Description]

### Security Updates

- **[Update title]** — [Description without exposing vulnerability details]

### Deprecations

- **[Deprecated feature]** — [What's being deprecated, timeline, and migration path]


### Known Issues

- [Known issue description] — [Workaround if available]


*For questions or feedback, [CUSTOMIZE: contact info or link]*
```

#### For Internal/Team Audience:

```markdown
type: release-notes
project: [project-name]
version: [version]
date: [YYYY-MM-DD]
created: [YYYY-MM-DD HH:MM]
audience: internal
tags: ["#release-notes", "#[project-name]", "#v[version]"]
source_tracker: [github/linear/jira/manual]

# Release Notes — [Project Name] [Version] (Internal)

**Release Date:** [Date]
**Cycle/Sprint:** [Name if applicable]

## Summary
[Executive summary with key stats: N features, N fixes, N tech improvements]


### Breaking Changes
- **[Title]** ([PR/Issue #link]) — [Technical description] — @[author]

### New Features & Enhancements
- **[Title]** ([PR/Issue #link]) — [Description] — @[author]

### Bug Fixes
- **[Title]** ([PR/Issue #link]) — [Description] — @[author]

### Technical Improvements
- **[Title]** ([PR/Issue #link]) — [Description] — @[author]

### Documentation
- **[Title]** ([PR/Issue #link]) — [Description] — @[author]


### Stats
- **Total items:** [N]
- **Contributors:** [list of contributors]
- **PRs merged:** [N]
- **Issues resolved:** [N]


### Known Issues & Follow-ups
- [ ] [Issue description] — Owner: [name]
```

### Phase 4: Review Gate

Present the generated release notes to the user:

```
Release notes draft is ready for [Project] [Version].

Summary:
- [N] New Features & Enhancements
- [N] Bug Fixes
- [N] Technical Improvements
- [N] other items

Audience: [external/internal]

Would you like to:
a) Review the full release notes
b) Save as-is to the vault
c) Make changes
d) Publish to [active platform] (requires your approval)
```

**NEVER auto-publish. Always wait for explicit user approval.**

### Phase 5: Save to Vault

Save to: `04-projects/[project]/release-notes/release-[version]-YYYY-MM-DD.md`

```bash
mkdir -p "04-projects/[project]/release-notes"
```

### Phase 6: Publish (Optional, requires approval)

**Only proceed if the user explicitly approves.**

#### GitHub Release
```
gh release create [VERSION_TAG] \
  --repo [CUSTOMIZE: your-org/your-repo] \
  --title "[Project] [Version]" \
  --notes-file [path-to-release-notes]
```

#### Confluence
```
Use WebFetch to publish via Confluence REST API:
- Space: [CUSTOMIZE: YOUR-SPACE-KEY]
- Parent page: [CUSTOMIZE: Release-Notes-parent-page-id]
- Title: "Release Notes — [Project] [Version]"
```

#### Notion
```
1. Use ToolSearch to load Notion tools
2. Use mcp__claude_ai_Notion__notion-create-pages
```

#### HackMD
```
Use WebFetch to publish via HackMD API
```

After publishing, update the vault copy with the published URL.


## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No tracker active | Accept manual input, or scan git log for commits in the date range |
| Tracker API fails | Fall back to git log analysis: `git log --oneline [PREV_TAG]..[CURRENT_TAG]` |
| No version tag specified | Use date range instead, or list recent completed work |
| Mixed sources | Merge and deduplicate items from multiple trackers |
| No publishing platform | Save to vault only |
| Very large release | Split into "Highlights" section + full changelog |

## Error Handling

- **Too many items**: If >100 items, auto-summarize minor changes and list only significant ones in detail
- **Missing PR descriptions**: Use PR title and commit messages as fallback
- **Duplicate items across trackers**: Deduplicate by matching titles/descriptions
- **Context overflow**: Paginate data collection, summarize per-batch
