---
name: "cog-create-user-story"
displayName: "COG Create User Story"
description: "Create user stories with duplicate checking across any project tracker (Linear, GitHub Issues, Jira)"
keywords: ["create story", "new story", "add issue", "write user story", "create ticket", "create user story"]
---


# COG Create User Story Skill

## When to Invoke
- User wants to create a new user story, feature request, or issue
- User says "create story", "new story", "add issue", "write user story", "create ticket"
- User describes a feature or requirement that should be tracked

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use parallel agents to check for duplicates across all active trackers simultaneously, then create the story
- If `agent_mode: solo` — check duplicates and create the story sequentially in the main conversation

## Command: `/create-user-story`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** to determine which project trackers are active:
   - **Linear** — use Linear MCP tools
   - **GitHub** — use `gh` CLI
   - **Jira** — use `jira` CLI or Jira API via WebFetch
   - If NO tracker is active, save the story as a markdown file in `04-projects/[project]/stories/` and inform the user

2. **Read `00-inbox/MY-PROFILE.md`** to get:
   - Active projects (to determine which project/repo/board to target)
   - User's name (for story author attribution)

3. **Ask the user** (if not already provided):
   - What is the feature or requirement? (free-form description)
   - Which project does this belong to? (if multiple active projects)
   - Priority level? (optional — default to medium)


## Execution Strategy

### Phase 1: Understand the Request

Parse the user's input to extract:
- **Feature description** — what the user wants built
- **Target users** — who benefits from this
- **Problem statement** — what problem this solves
- **Project context** — which project this belongs to

If the user provides a brief description, ask clarifying questions before proceeding:
- Who is the target user for this feature?
- What problem does this solve?
- Are there any specific acceptance criteria you have in mind?

### Phase 2: Duplicate Check

**CRITICAL: Always check for duplicates before creating.**

#### Team Mode (parallel agents)

Launch duplicate-check agents in parallel using the Task tool with `run_in_background: true`:

**Agent: "duplicate-checker-linear"** (if Linear is active)
```
Search Linear for potential duplicate issues.
1. Use ToolSearch to load Linear tools
2. Use mcp__claude_ai_Linear_2__list_issues to search for issues with similar keywords
3. Search across all active projects/teams
4. Return any issues that match by title similarity or description overlap

Search terms: [extracted keywords from user's description]
Return: list of potential duplicates with title, status, URL, and similarity assessment
```

**Agent: "duplicate-checker-github"** (if GitHub is active)
```
Search GitHub Issues for potential duplicates.
Repository: [CUSTOMIZE: your-org/your-repo]

1. gh search issues "[keywords]" --repo [CUSTOMIZE: your-org/your-repo] --json number,title,state,url,body --limit 20
2. Also search closed issues to check if this was already done:
   gh search issues "[keywords]" --repo [CUSTOMIZE: your-org/your-repo] --state closed --json number,title,state,url --limit 10

Return: list of potential duplicates with title, status, URL, and similarity assessment
```

**Agent: "duplicate-checker-jira"** (if Jira is active)
```
Search Jira for potential duplicate issues.
Project: [CUSTOMIZE: YOUR-PROJECT-KEY]

1. Use WebFetch or jira CLI to search:
   JQL: project = "[CUSTOMIZE: YOUR-PROJECT-KEY]" AND text ~ "[keywords]" ORDER BY created DESC
2. Check both open and recently resolved issues

Return: list of potential duplicates with key, title, status, URL, and similarity assessment
```

#### Solo Mode (sequential)
Run the same duplicate checks sequentially for whichever tracker is active.

### Phase 3: Report Duplicates (if found)

If potential duplicates are found, present them to the user:

```
I found [N] potential duplicate(s):

1. **[TITLE]** ([STATUS]) — [URL]
   Similarity: [High/Medium/Low] — [reason]

2. **[TITLE]** ([STATUS]) — [URL]
   Similarity: [High/Medium/Low] — [reason]

Options:
a) These are different — proceed with creating the new story
b) This is a duplicate of #[N] — skip creation
c) This is related to #[N] — create and link them
```

**Wait for user confirmation before proceeding.**

### Phase 4: Format the User Story

Generate the story in standard user story format:

```markdown
## Title
[Concise, descriptive title]

## User Story
**As a** [type of user],
**I want** [goal/desire],
**So that** [benefit/value].

## Description
[Expanded description of the feature, including context and background]

## Acceptance Criteria

### Scenario 1: [Happy path scenario name]
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

### Scenario 2: [Alternative scenario name]
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

### Scenario 3: [Edge case or error scenario name]
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

## Technical Notes
[Any implementation hints, constraints, or dependencies — if applicable]

## Out of Scope
[What this story explicitly does NOT cover — helps prevent scope creep]
```

**Present the formatted story to the user for review before creating it.**

### Phase 5: Create in Tracker

After user approves the story content:

#### Linear
```
1. Use ToolSearch to load Linear tools
2. Use mcp__claude_ai_Linear_2__get_team to find the target team
3. Use mcp__claude_ai_Linear_2__list_issue_labels to find appropriate labels
4. Use mcp__claude_ai_Linear_2__save_issue to create the issue with:
   - title: [story title]
   - description: [full story in markdown]
   - team: [target team]
   - priority: [user-specified or default medium]
   - labels: [appropriate labels]
```

#### GitHub Issues
```
gh issue create \
  --repo [CUSTOMIZE: your-org/your-repo] \
  --title "[story title]" \
  --body "[full story in markdown]" \
  --label "[appropriate labels]"
```

#### Jira
```
Use WebFetch to POST to Jira REST API or use jira CLI:
- Project: [CUSTOMIZE: YOUR-PROJECT-KEY]
- Issue Type: Story
- Summary: [story title]
- Description: [full story in markdown/Jira wiki format]
- Priority: [user-specified or default Medium]
- Labels: [appropriate labels]
```

#### Vault Fallback (no tracker active)
Save to `04-projects/[project]/stories/story-YYYY-MM-DD-[slug].md`

### Phase 6: Confirm and Link

1. Confirm creation with the user:
   ```
   Story created: **[TITLE]**
   [URL or file path]
   Priority: [priority]
   Labels: [labels]
   ```

2. If the user indicated this is related to another issue (Phase 3, option c), create a link/relation between them.

3. Also save a local copy to `04-projects/[project]/stories/` for vault reference.


## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No tracker active | Save as markdown in `04-projects/[project]/stories/` |
| Tracker API fails | Save locally, warn user, suggest manual creation with the formatted content |
| Duplicate check fails | Warn user that duplicate check was skipped, proceed with creation after confirmation |
| User doesn't specify project | List active projects from MY-PROFILE.md and ask which one |
| User provides minimal input | Ask clarifying questions to build a complete story |

## Error Handling

- **API rate limits**: Wait and retry once, then fall back to local save
- **Authentication failures**: Inform user their integration may need re-authentication
- **Large search results**: Limit duplicate check to top 10 most relevant matches
- **Context overflow**: Summarize duplicate results rather than showing full descriptions
