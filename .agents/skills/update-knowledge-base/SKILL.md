---
name: update-knowledge-base
description: Maintain and update product knowledge base from releases, features, and project changes with optional wiki sync
metadata:
  roles: product-manager,engineering-lead,founder
  integrations: github,linear,jira,confluence,notion
  keywords: update knowledge base,update KB,sync knowledge,update product docs
  display-name: COG Update Knowledge Base
---

# COG Update Knowledge Base Skill

## When to Invoke
- After a release — update product knowledge with new features and changes
- User says "update knowledge base", "update KB", "sync knowledge", "update product docs"
- Periodic maintenance — ensure knowledge base reflects current product state
- After major feature launches, architecture changes, or deprecations

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use parallel agents to scan multiple sources and update multiple knowledge files simultaneously
- If `agent_mode: solo` — process updates sequentially, one knowledge file at a time

## Command: `/update-knowledge-base`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** for active data sources and publishing targets
2. **Read `00-inbox/MY-PROFILE.md`** for active projects
3. **Get current timestamp:** Run `date '+%Y-%m-%d %H:%M'` using Bash
4. **Scan existing knowledge base:** Glob `05-knowledge/**/*.md` to understand current state


## Execution Strategy

### Phase 1: Determine Update Scope

Ask the user (or infer from context):

```
What triggered this knowledge base update?

a) New release shipped (I'll pull changes from release notes and tracker)
b) Feature launched or updated (I'll document the feature)
c) Architecture or technical change (I'll update technical knowledge)
d) Periodic review (I'll scan for anything that's changed since last update)
e) Custom — describe what needs updating
```

### Phase 2: Gather Update Data

#### Team Mode (parallel agents)

Launch data-gathering agents using the Task tool with `run_in_background: true`:

**Agent: "release-scanner"** (for release-triggered updates)
```
Scan recent releases and release notes for knowledge base updates.

1. Check vault for recent release notes:
   Glob: 04-projects/*/release-notes/*.md
   Read the most recent release notes for each active project

2. If GitHub is active:
   gh release list --repo [CUSTOMIZE: your-org/your-repo] --limit 5 --json tagName,name,body,publishedAt
   Get the latest release details

3. If Linear is active:
   Use ToolSearch to load Linear tools
   Check recently completed cycles and milestones for shipped features

Extract from each source:
- New features added (name, description, user impact)
- Features modified (what changed)
- Features deprecated or removed
- Technical changes (architecture, API, infrastructure)
- Bug fixes that affect documented behavior

Return: structured list of knowledge updates needed
```

**Agent: "existing-kb-auditor"**
```
Audit the current knowledge base for staleness and gaps.

1. Read all files in 05-knowledge/:
   Glob: 05-knowledge/**/*.md

2. For each file, extract:
   - Last updated date (from frontmatter or file modification)
   - Topics covered
   - Products/features documented
   - Any [TODO] or [OUTDATED] markers

3. Cross-reference with active projects from MY-PROFILE.md:
   - Are all active projects represented in the KB?
   - Are there KB entries for discontinued/inactive projects?

4. Check for:
   - Files not updated in >90 days (potentially stale)
   - Topics mentioned in recent release notes but missing from KB
   - Contradictions between KB entries and recent changes

Return: staleness report, gap analysis, and recommended updates
```

**Agent: "tracker-feature-collector"** (for feature-triggered updates)
```
Collect current feature/product state from project trackers.

If Linear is active:
1. Use ToolSearch to load Linear tools
2. List all projects and their current status: mcp__claude_ai_Linear_2__list_projects
3. List all initiatives: mcp__claude_ai_Linear_2__list_initiatives
4. For key initiatives, get details: mcp__claude_ai_Linear_2__get_initiative

If GitHub is active:
1. Check repo README and docs for current feature descriptions
2. Review recent PRs that touch documentation:
   gh pr list --repo [CUSTOMIZE: your-org/your-repo] --state merged --search "label:docs merged:>=[30_DAYS_AGO]" --json number,title,body --limit 20

Return: current product/feature state for knowledge base comparison
```

#### Solo Mode
Run the most relevant agent sequentially based on the update trigger.

### Phase 3: Identify Knowledge Updates

Compare gathered data against existing knowledge base to determine:

1. **New entries needed** — features, products, or topics not yet documented
2. **Updates needed** — existing entries that need modification
3. **Deprecation/removal** — entries for features that no longer exist
4. **Gap filling** — missing context, examples, or cross-references

Present the update plan to the user:

```
Knowledge Base Update Plan:

NEW entries to create:
1. [Topic] — [reason: new feature in v[X]]
2. [Topic] — [reason: gap identified]

UPDATES to existing entries:
1. 05-knowledge/[file].md — [what needs changing]
2. 05-knowledge/[file].md — [what needs changing]

DEPRECATION candidates:
1. 05-knowledge/[file].md — [reason: feature removed in v[X]]

STALE entries (>90 days, may need review):
1. 05-knowledge/[file].md — last updated [date]

Proceed with these updates? (yes / modify plan / skip specific items)
```

**Wait for user approval before making changes.**

### Phase 4: Execute Updates

#### 4.1 Create New Knowledge Entries

For each new entry, use this template:

```markdown
type: knowledge
domain: [product/technical/process/architecture]
project: [project-name]
topic: [topic name]
created: [YYYY-MM-DD HH:MM]
last_updated: [YYYY-MM-DD]
source: [release-notes/feature-launch/manual/periodic-review]
version: "1.0"
tags: ["#knowledge", "#[project]", "#[topic-area]"]
related:
  - [path to related KB entry]
  - [path to related project file]

# [Topic Title]

## Overview
[Clear, concise description of the topic — what it is, why it matters]

## Current State
[How this feature/system/process works as of the last update]

### Key Details
- **[Detail 1]:** [Value/description]
- **[Detail 2]:** [Value/description]
- **[Detail 3]:** [Value/description]

## History
| Date | Version | Change | Source |
|------|---------|--------|--------|
| [Date] | [Version] | [What changed] | [Release notes / PR / manual] |

## Related
- [Link to related KB entries]
- [Link to PRDs if applicable]
- [Link to project files]

## Notes
[Additional context, caveats, or open questions]


*Last updated: [YYYY-MM-DD] | Source: [what triggered this update]*
```

Save to: `05-knowledge/[domain]/[topic-slug].md`

```bash
mkdir -p "05-knowledge/[domain]"
```

#### 4.2 Update Existing Entries

For each update:
1. Read the existing file
2. Update the relevant sections
3. Add a row to the History table
4. Update `last_updated` in frontmatter
5. Update `version` (increment minor version)

#### 4.3 Mark Deprecations

For deprecated entries:
1. Add `status: deprecated` to frontmatter
2. Add a deprecation notice at the top of the file:
   ```markdown
   > **DEPRECATED:** This feature was removed/replaced in [version/date]. See [replacement link] for the current approach.
   ```
3. Do NOT delete the file — historical context is valuable

### Phase 5: Generate Update Summary

Create an update log:

```markdown
type: kb-update-log
date: [YYYY-MM-DD]
created: [YYYY-MM-DD HH:MM]
trigger: [release/feature/periodic/manual]
tags: ["#knowledge", "#update-log"]

# Knowledge Base Update — [YYYY-MM-DD]

## Trigger
[What caused this update: release X.Y.Z / feature launch / periodic review]

## Changes Made

### New Entries
| File | Topic | Domain | Source |
|------|-------|--------|--------|
| [path] | [topic] | [domain] | [source] |

### Updated Entries
| File | Changes | Previous Version | New Version |
|------|---------|-----------------|-------------|
| [path] | [summary of changes] | [old ver] | [new ver] |

### Deprecated Entries
| File | Reason | Replacement |
|------|--------|-------------|
| [path] | [reason] | [link to replacement or N/A] |

## Knowledge Base Health
- **Total entries:** [N]
- **Updated this session:** [N]
- **Created this session:** [N]
- **Deprecated this session:** [N]
- **Stale entries remaining (>90 days):** [N]
- **Coverage:** [assessment of how well the KB covers active projects]


*Generated by COG Knowledge Base Updater*
```

Save to: `05-knowledge/_logs/kb-update-YYYY-MM-DD.md`

```bash
mkdir -p "05-knowledge/_logs"
```

### Phase 6: Optional Wiki Sync (requires approval)

If Confluence or Notion is active, offer to sync updated entries:

```
Knowledge base updated locally. Would you like to sync to your wiki?

Active wiki platforms:
- [Confluence / Notion — whichever is active]

Options:
a) Sync all changed entries to [platform]
b) Sync specific entries only
c) Skip wiki sync (vault-only)
```

**NEVER auto-publish. Wait for explicit approval.**

#### Confluence Sync
Use the `/publish-to-confluence` skill pattern for each entry being synced.

#### Notion Sync
```
1. Use ToolSearch to load Notion tools
2. Search for existing pages matching the KB entry: mcp__claude_ai_Notion__notion-search
3. If exists: update with mcp__claude_ai_Notion__notion-update-page
4. If new: create with mcp__claude_ai_Notion__notion-create-pages
```


## Knowledge Base Organization

Recommended `05-knowledge/` structure:

```
05-knowledge/
  _logs/                    # Update logs
    kb-update-YYYY-MM-DD.md
  product/                  # Product features, capabilities, roadmap
    [feature-name].md
  technical/                # Architecture, APIs, infrastructure
    [system-name].md
  process/                  # Team processes, workflows, conventions
    [process-name].md
  domain/                   # Domain knowledge, industry context
    [topic-name].md
  integrations/             # Integration docs, API references
    [integration-name].md
```


## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No trackers active | Work from vault data only (release notes, PRDs, project files) |
| No existing KB entries | Create the initial knowledge base structure and first entries |
| Wiki sync fails | All changes are already saved locally; inform user to sync manually |
| Very large KB (>50 files) | Process in batches, prioritize most recently changed entries |
| No recent changes found | Report that KB is up to date; suggest periodic review topics |
| Conflicting information | Flag conflicts for user resolution rather than auto-resolving |

## Error Handling

- **File conflicts**: If an update would contradict a recent manual edit, present both versions to the user
- **Context overflow**: Process knowledge files in batches of 10
- **Stale data sources**: Warn if tracker data seems outdated (API issues)
- **Missing project context**: Ask user to clarify which project the knowledge relates to
