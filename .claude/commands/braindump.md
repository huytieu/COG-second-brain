# Brain Dump Command

## Purpose
Quick capture and initial processing of stream-of-consciousness thoughts, ideas, and insights with immediate domain classification and basic structuring.

## Command: `/braindump`

## Pre-Flight Check

**Before executing, check for user profile:**

1. Look for `00-inbox/MY-PROFILE.md` in the vault
2. If NOT found:
   ```
   Welcome to COG! It looks like this is your first time.

   Before we start, let's quickly set up your profile (takes 2 minutes).

   Type '/onboarding' to get started, or I can proceed with default settings.
   ```
3. If found:
   - Read the profile to get user's name and active projects
   - If user has active projects listed, offer them as domain options
   - Use user's name for friendly communication

## Process Flow

This command orchestrates the brain dump capture process by delegating to the specialized **brain-dump-analyst** subagent.

### 1. User Interaction & Input Collection
**Your role (Claude Code):**
- Greet user warmly (use their name from MY-PROFILE.md if available)
- Ask: "What's on your mind?" or "Ready for a brain dump?"
- Collect their stream-of-consciousness input (can be long, rambling, voice-to-text, etc.)
- Accept any format - no judgment, no filtering

### 2. Domain Classification
**Your role (Claude Code):**
Ask user to classify or auto-detect based on content:

**If user profile exists with projects:**
- **Personal:** Individual growth, relationships, wellness
- **Professional:** Work, leadership, career development
- **Project-Specific:** Related to specific projects
  - If MY-PROFILE.md lists projects, offer: "Which project? [list project names]"
  - Example: "Which project? (1) SaaS Product, (2) Book Writing, (3) Health App"
- **Mixed/Unclear:** Spans multiple areas

**If no profile:** Use standard personal/professional/mixed classification

### 3. Delegate to Brain Dump Analyst Subagent
**Your role (Claude Code):**

Once you have the raw braindump content and domain classification, **delegate ALL analysis and processing to the brain-dump-analyst subagent**:

```markdown
I'm passing this to the brain-dump-analyst subagent for processing...

**To brain-dump-analyst subagent:**

Process this braindump according to your analysis framework:

**Raw Content:**
[User's unfiltered braindump content]

**Domain:** [personal|professional|project-specific]
**Project:** [project-name if applicable]
**Date:** [current date]
**User Name:** [from MY-PROFILE.md if available]

**Competitive Watchlist:** [Read from 03-professional/COMPETITIVE-WATCHLIST.md if exists]

**Instructions:**
- Perform full braindump analysis per your protocol
- Check for competitive intelligence mentions (if watchlist exists)
- Generate structured output with metadata
- Save to appropriate domain folder:
  - Personal: `02-personal/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
  - Professional: `03-professional/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
  - Project: `04-projects/[project-slug]/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
  - Mixed: `00-inbox/braindump-YYYY-MM-DD-HHMM-<title>.md`

- If competitive intel detected, also update: `04-projects/[project]/competitive/[company-name].md`

- Use proper YAML frontmatter with quoted strings
- Include all analysis sections per your template
- Provide confidence assessment

Return the file path where you saved the braindump.
```

### 4. Confirm Completion
**Your role (Claude Code):**
- Wait for subagent to complete processing
- Confirm file was created
- Show user: "Braindump saved to [file path]"
- Optionally show quick summary of themes identified
- Ask: "Would you like me to run deeper analysis? (Type `/brain-dump-analysis`)"

## What NOT to Do

**Do NOT:**
- Process or analyze the content yourself
- Create the output file yourself
- Perform theme extraction yourself
- Do competitive intelligence detection yourself

**Instead:**
- Collect input from user
- Determine domain/project
- Delegate to brain-dump-analyst subagent
- Confirm completion

## Competitive Intelligence Detection

The brain-dump-analyst subagent will automatically:
- Read `03-professional/COMPETITIVE-WATCHLIST.md` if it exists
- Scan braindump content for mentions of tracked companies/people
- Extract competitive intel to `04-projects/[project]/competitive/[company].md`
- Cross-reference back to the original braindump

## Output File Structure

The brain-dump-analyst subagent creates files with this structure:

```markdown
---
type: "braindump"
domain: "[personal|professional|project-specific|mixed]"
project: "[project-name]" # Only if project-specific
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
themes: ["theme1", "theme2", "theme3"]
tags: ["#braindump", "#raw-thoughts", "#domain-tag"]
status: "captured"
---

# Braindump: [Auto-generated title]

## Raw Thoughts
[Original user content preserved]

## Main Themes
[Identified by subagent]

## Action Items
[Extracted by subagent]

## Questions
[Identified by subagent]

## Connections
[Identified by subagent]

## Processing Notes
[Subagent's analysis notes]
```

## Integration with Other Commands

### Immediate Follow-up
- `/brain-dump-analysis` - Deep analysis via brain-dump-analyst subagent
- `/daily-checkin` - Reflect on themes
- `/scout-project-analysis` - Project-specific insights (if applicable)

### Competitive Intelligence
If competitive mentions detected, the brain-dump-analyst will automatically update competitive files and mention this in the output.

## Success Metrics
- Speed of capture (minimize user friction)
- Successful delegation to subagent
- File saved to correct location
- User feels heard and understood
- Competitive intel auto-extracted when relevant
