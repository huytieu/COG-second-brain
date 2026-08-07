---
name: onboarding
description: Personalize COG for your workflow - creates profile, interests, and watchlist files with guided setup (run this first!)
roles: [all]
integrations: []
---

# COG Onboarding Skill

## Purpose
Welcome new users and collect essential information to personalize their COG experience. All configuration is stored as natural markdown files within the vault structure, following COG's philosophy of transparent, editable knowledge.

## When to Invoke
- User explicitly requests `/onboarding` or mentions "onboarding" or "setup COG"
- User is new and hasn't completed onboarding yet
- User wants to update their profile or add new projects
- Any time profile customization is needed

## Core Design Principle: Smart, Low-Friction Onboarding

**The onboarding MUST feel like a natural conversation, NOT a form to fill out.**

Key rules:
- **Ask open-ended questions, not option-pickers.** Never present numbered lists of choices for the user to pick from.
- **Ask as few questions as possible.** Infer what you can from context and the user's natural responses.
- **Never ask redundant questions.** If you can extract the answer from something the user already said, don't ask again.
- **Parse intelligently.** If someone says "I'm Alex, a PM at a fintech startup tracking Stripe and Plaid", extract: name=Alex, role=PM at fintech startup, watchlist=[Stripe, Plaid]. Don't ask follow-up questions for info already given.
- **Confirm, don't re-ask.** If you're unsure about something the user said, confirm your interpretation rather than asking the question fresh.

## Process Flow

### 1. Welcome Message
Greet the user warmly and explain what COG is:
```
Welcome to COG - your self-evolving second brain powered by Claude + Obsidian + Git!

COG helps you capture thoughts, get daily intelligence briefings, and build knowledge over time - all stored as simple markdown files you own.

Let's get you set up. Tell me a bit about yourself - your name, what you do, and what topics or areas you're most interested in staying sharp on. Feel free to share as much or as little as you'd like.
```

**This single open-ended prompt replaces the old sequential questions.** The user can naturally mention their name, role, interests, sources, projects, and competitors all at once - or just share a few things.

### 2. Check for Existing Profile

Look for `00-inbox/MY-PROFILE.md`. If it exists:
```
I found an existing COG profile! What would you like to update? Just tell me what you'd like to change - your interests, projects, profile info, or anything else.
```

**Don't present a numbered menu.** Let them describe what they want in natural language.

### 3. Intelligent Information Extraction

After the user responds, extract as much as possible from their natural language:

| Field | How to Extract |
|-------|---------------|
| **Name** | Look for self-introduction patterns ("I'm Alex", "My name is...", "Call me..."). Use first name by default. |
| **Role** | Look for job/activity mentions ("I'm a PM", "I work in...", "software engineer at..."). |
| **Interests** | Look for topic mentions ("interested in AI", "following crypto", "love design"). Also infer from role context. |
| **News Sources** | Look for source mentions ("I read HN", "follow on Twitter"). If not mentioned, skip - it's optional. |
| **Projects** | Look for project mentions ("working on a SaaS app", "building..."). If not mentioned, skip. |
| **Competitive Watch** | Look for company/person mentions ("tracking Stripe", "watching what OpenAI does"). If not mentioned, skip. |

### 4. Smart Follow-Up (Only If Needed)

After extracting what you can, check what's missing from the **required** fields only:
- **Name** (required)
- **Role** (required)
- **Interests** (required - need at least 2-3 topics)

If any required field is missing, ask ONE follow-up that covers all gaps. For example:
```
Thanks! I got your name and role. What topics are you most interested in staying updated on? (e.g., AI, startups, design, health - whatever matters to you)
```

**Optional fields** (news sources, projects, competitive watch) should NEVER generate follow-up questions. If the user didn't mention them, skip them. They can always add them later by editing the files or running onboarding again.

### 5. Confirm and Create

Before creating files, briefly confirm what you captured and ask about agent team mode:
```
Here's what I've got:

- **Name**: Alex
- **Role**: Product Manager at a fintech startup
- **Interests**: AI/ML, fintech trends, product strategy, UX design
- **Projects**: Payments dashboard revamp
- **Tracking**: Stripe, Plaid

One more thing - COG can run in two modes:
- **Solo mode** (default): I handle everything directly in our conversation.
- **Agent team mode**: I delegate research, analysis, and writing to specialist sub-agents for deeper, more thorough results. Works best with Claude Code.

Which do you prefer? (Solo is great for most people - team mode is for power users who want maximum depth.)
```

**Wait for confirmation**, then generate everything. If they say "looks good" or similar, proceed. If they correct something, update and proceed without re-confirming. Default to `solo` if they don't express a preference.

### 5.5. Role Pack Matching

After extracting the user's role text in Step 3, scan `.claude/roles/*.md` for a matching role pack:

1. Read each role pack file's YAML frontmatter (`role_id` and `aliases`)
2. Compare the user's extracted role text (case-insensitive) against:
   - Exact `role_id` match (e.g., "product-manager")
   - Any string in `aliases` (e.g., "pm", "product lead", "head of product")
   - Fuzzy substring match (e.g., "product manager at a fintech startup" contains "product manager")
3. If a match is found:
   - Store the matched `role_id` as `role_pack` in the MY-PROFILE.md frontmatter
   - Present role-specific recommendations:
   ```
   As a [Role Display Name], here are the skills and integrations that'll be most useful for you:

   **Recommended skills** (ordered by relevance for your role):
   [List top 5-6 skills from the role pack with the "Why it matters for you" context]

   **Recommended integrations**:
   [List integrations from the role pack with role-specific explanations]
   ```
   - Use the role pack's suggested `agent_mode` as the default (instead of `solo`)
4. If no match is found:
   - Set `role_pack: custom` in MY-PROFILE.md
   - Recommend core skills only (those with `roles: [all]`)
   - Ask about common integrations: "Do you use GitHub, Slack, or any other tools you'd like COG to connect with?"

### 5.6. Integration Discovery

After role pack matching, set up the user's integration preferences:

1. If a role pack was matched, present its recommended integrations with role-specific context:
   ```
   Based on your role, these integrations would give COG the most context:

   [For each integration in role pack:]
   - **[Integration]** — [Why it matters for you, from role pack]

   Which of these do you already use? And are there any other tools you'd like to connect?
   ```

2. Parse the user's response:
   - Services they confirm using → add to **Active** section of MY-INTEGRATIONS.md
   - Services they don't mention or say no to → add to **Disabled** section
   - Additional services they mention → add to **Active** section
   - Always add `ElevenLabs` to **Disabled** unless explicitly requested

3. Generate `00-inbox/MY-INTEGRATIONS.md`:
   ```markdown
   ---
   type: integrations
   created: YYYY-MM-DD
   tags: ["#integrations", "#config", "#cog"]
   ---

   # My Integrations

   *COG checks this file before using any external service. Edit anytime.*

   ## Active
   [For each confirmed integration:]
   - **[Service]**: [Brief description of how COG uses it]

   ## Disabled
   [For each declined/unmentioned integration:]
   - **[Service]**: Skipped during onboarding. Enable anytime by moving to Active section.

   ---

   *Move services between Active and Disabled sections to control what COG connects to.*
   ```

4. If no role pack was matched, ask about common integrations conversationally:
   ```
   COG can connect with tools like GitHub, Slack, Linear, Notion, and PostHog for richer analysis. Do you use any of these? (Totally optional - COG works great without them too.)
   ```

### 6. Generate Profile Documents

Create the following markdown files:

#### `00-inbox/MY-PROFILE.md`
```markdown
---
type: profile
created: YYYY-MM-DD
onboarding_completed: true
role_pack: [matched role_id or "custom"]
agent_mode: [solo or team, based on role pack suggestion]
tags: ["#profile", "#config", "#cog"]
---

# My COG Profile

## About Me
- **Name**: [Name]
- **Role**: [Job/role/main activity]
- **Role Pack**: [Display name from matched role pack, or "Custom" if no match]
- **Profile Created**: [Date]

## Settings
- **Agent Mode**: [solo/team] *(solo = handle everything directly; team = delegate to specialist sub-agents for deeper results)*

## Active Projects
[If they mentioned projects:]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 1]]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 2]]

[If no projects:]
*No active projects yet. Add them anytime by editing this file or running onboarding again.*

## Related
- [[MY-INTERESTS|My Interests & News Sources]]
- [[03-professional/COMPETITIVE-WATCHLIST|Competitive Watchlist]] *(if applicable)*

## Notes
*Feel free to add notes here about your COG usage, preferences, or anything else.*

---

*Edit this file anytime to update your profile. COG reads it when you use skills.*
```

#### `00-inbox/MY-INTERESTS.md`
```markdown
---
type: interests
created: YYYY-MM-DD
tags: ["#interests", "#daily-brief", "#config"]
---

# My Interests & News Sources

*These topics guide my daily intelligence briefings.*

## Topics I'm Interested In
- [Topic 1]
- [Topic 2]
- [Topic 3]
- [Topic 4]
- [Topic 5]

## Preferred News Sources
[If sources were mentioned:]
*Where I like to get information:*
- [Source 1]
- [Source 2]
- [Source 3]

[If no sources mentioned:]
*No specific sources set. COG will search broadly for your topics. Add preferred sources here anytime.*

## Notes
*Add any additional context about your interests here.*

---

*Update this file anytime as your interests evolve. Just edit and save—COG will pick up the changes.*
```

#### `03-professional/COMPETITIVE-WATCHLIST.md` (only if they mentioned companies/people to track)
```markdown
---
type: competitive-intelligence
created: YYYY-MM-DD
tags: ["#competitive", "#intelligence", "#tracking"]
---

# Competitive Watchlist

*Companies, people, or organizations I'm keeping an eye on.*

## Watching
- [Company/Person 1]
- [Company/Person 2]
- [Company/Person 3]

## Why I'm Tracking Them
*Add context here about why these matter to you or your projects.*

---

*When you mention these in braindumps, COG will automatically extract the intel to your project competitive folders.*
```

#### For Each Project: `04-projects/[project-slug]/PROJECT-OVERVIEW.md`
```markdown
---
type: project-overview
project: [project-name]
slug: [project-slug]
created: YYYY-MM-DD
status: active
tags: ["#project", "#overview"]
---

# [Project Name]

## What is this project?
[Brief description - leave for user to fill in]

## Current Status
*What phase are you in? What's happening now?*

## Project Resources
- [[braindumps/|Project Braindumps]]
- [[competitive/|Competitive Intelligence]]
- [[content/|Content & Assets]]
- [[planning/|Planning Documents]]

## Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]

---

*This overview helps COG organize your project-related thoughts and updates.*
```

### 7. Create Directory Structure
Based on configuration, create personalized structure:

**Base Structure (Always):**
```
00-inbox/
01-daily/
  briefs/
  checkins/
02-personal/
  braindumps/
  development/
  wellness/
03-professional/
  braindumps/
  leadership/
  strategy/
  skills/
04-projects/
05-knowledge/
  consolidated/
  patterns/
  timeline/
  booklets/
06-templates/
```

**Project-Specific (For each listed project):**
```
04-projects/[project-slug]/
  PROJECT-OVERVIEW.md
  braindumps/
  competitive/
  content/
  planning/
  resources/
```

### 8. Create Welcome Guide

Generate: `00-inbox/WELCOME-TO-COG.md`

```markdown
---
type: guide
created: YYYY-MM-DD
tags: ["#welcome", "#getting-started", "#cog"]
---

# Welcome to Your COG Second Brain, [Name]!

Your COG is now personalized and ready to use. Here's how to get started:

## Your Profile Documents

I've created these documents to store your preferences:

- **[[MY-PROFILE]]** - Your basic info, role pack, and workflow preferences
- **[[MY-INTERESTS]]** - Topics for your daily briefs
- **[[MY-INTEGRATIONS]]** - Your active and disabled integrations
- **[[03-professional/COMPETITIVE-WATCHLIST]]** - Companies you're tracking *(if applicable)*

**You can edit these files anytime.** COG reads them when you use skills, so your changes take effect immediately.

## Skills for Your Role

[If role pack was matched:]
As a **[Role Display Name]**, these skills are ordered by relevance for you:

[List skills from role pack in order, with brief "why it matters" from the role pack. Format as:]
1. **[skill-name]** — [Role-specific explanation]
2. **[skill-name]** — [Role-specific explanation]
[...continue for all recommended skills]

[If no role pack match:]
Here are COG's core skills available to everyone:

1. **daily-brief** — Personalized news intelligence
2. **braindump** — Capture and classify thoughts
3. **weekly-checkin** — Weekly pattern analysis
4. **knowledge-consolidation** — Build frameworks from scattered notes
5. **url-dump** — Save URLs with auto-extracted insights
6. **update-cog** — Keep COG framework current

## Your Integrations

[If integrations were configured:]
**Active**: [List active integrations]
**Disabled**: [List disabled integrations]

You can change these anytime by editing [[MY-INTEGRATIONS]].

[If no integrations configured:]
No integrations configured yet. COG works great standalone — add integrations anytime by editing `00-inbox/MY-INTEGRATIONS.md`.

## Quick Start

### 1. Daily Morning Routine
Invoke the daily-brief skill to get your personalized intelligence briefing covering:
[List their selected interest areas]

### 2. Capture Your Thoughts
Use the braindump skill to quickly capture ideas, insights, and thoughts. Your braindumps will automatically be categorized into:
[List their focus domains]

Choose from your active projects:
[List their projects with links]

### 3. Weekly Reflection
Every week, use the weekly-checkin skill to review your week's insights and patterns.

## Your Active Projects

[If they have projects]
You're tracking these projects:
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project 1]]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project 2]]

When you use the braindump skill, select the project to automatically file your thoughts in the right place.

## How COG Uses Your Profile

**Daily Briefs**: Uses [[MY-INTERESTS]] to curate relevant news
**Braindumps**: Offers your projects from [[MY-PROFILE]] as options
**Competitive Intel**: Auto-extracts mentions of companies in [[COMPETITIVE-WATCHLIST]]
**Weekly Check-ins**: Reviews progress across your domains

## Next Steps

1. **Try your first braindump**: Use the braindump skill and start writing
2. **Get your daily brief**: Invoke the daily-brief skill to see curated intelligence
3. **Explore your vault**: All your files are organized in the sidebar
4. **Edit your profile**: Open [[MY-PROFILE]] and customize anytime

## Keeping COG Updated

COG separates your content from framework files. When new versions are released:
- Run `/update-cog` to check for and apply updates
- Or use the shell script: `./cog-update.sh --check`
- Your braindumps, profiles, and notes are **never** touched by updates

Check your current version: `cat COG-VERSION`

## Tips for Success

- **Don't overthink it**: Just dump your thoughts, COG will help organize
- **Be consistent**: Daily briefs and braindumps work best as habits
- **Review weekly**: Use the weekly-checkin skill to see patterns emerge
- **Evolve your setup**: Edit your profile files anytime or run onboarding again to add projects
- **Stay updated**: Run `/update-cog` periodically to get new skills and improvements

## Getting Help

- Check `SETUP.md` for detailed guides
- Visit the GitHub repo for documentation

**Your second brain is learning about you. Let's begin!**

---

*You can archive or delete this welcome guide once you're comfortable with COG.*
```

### 9. Wrap-Up (No Menu!)
After setup, summarize what was created and suggest a natural next action:

```
You're all set! I've created your profile, interests, and project files. Everything is in your vault and editable anytime.

If you want to jump right in, try a braindump - just tell me what's on your mind and I'll capture it. Or ask for your daily brief to see what's happening in your interest areas today.
```

**Don't present a numbered menu of next actions.** Just suggest one or two natural things and let them decide.

## Configuration Update Mode

If user runs onboarding after initial setup (MY-PROFILE.md exists):

Don't show a menu. Just ask:
```
You've already completed onboarding! What would you like to update? Just tell me what needs changing.
```

Then intelligently handle whatever they say - whether it's adding projects, changing interests, updating their role, etc.

## Success Criteria

Onboarding is successful when:
1. `MY-PROFILE.md` created in `00-inbox/` with `role_pack` in frontmatter
2. `MY-INTERESTS.md` created in `00-inbox/`
3. `MY-INTEGRATIONS.md` created in `00-inbox/` with active/disabled sections
4. Role pack matched (or set to `custom`) and recommendations presented
5. Project directories and overviews created (if applicable)
6. `WELCOME-TO-COG.md` guide created with role-specific skill ordering
7. User understands next steps and where their profile is stored

## Error Handling

**If profile already exists:**
- Don't overwrite, offer update mode instead
- Preserve existing content, only append/modify requested sections
- Archive old version to `00-inbox/archive/MY-PROFILE-YYYY-MM-DD.md` if starting fresh

**If directory creation fails:**
- Report which directories couldn't be created
- Provide manual creation instructions
- Continue with rest of setup

**If user exits mid-onboarding:**
- Create partial profile with note: "Onboarding incomplete - run onboarding skill to finish"
- Save what was collected so far
- Resume from last completed step on next run

## Privacy & Data

All configuration data is stored as markdown files in:
- `00-inbox/MY-PROFILE.md` - Basic profile with role pack
- `00-inbox/MY-INTERESTS.md` - Interest areas
- `00-inbox/MY-INTEGRATIONS.md` - Active/disabled external service integrations
- `03-professional/COMPETITIVE-WATCHLIST.md` - Competitive tracking
- `04-projects/[project]/PROJECT-OVERVIEW.md` - Project details

Benefits of markdown storage:
- Human-readable and editable
- Version controlled with Git
- Searchable in Obsidian
- Linkable from other notes
- No parsing required, just read as text
- Can be archived, moved, organized like any other note

## Philosophy

COG's configuration is **knowledge, not configuration**. By storing preferences as markdown notes:
- They're part of your knowledge base, not hidden config files
- You can link to them, reference them, evolve them
- They have context and can include your own notes
- They're transparent and auditable
- They benefit from all of Obsidian's features (tags, links, search, graph view)

This is "configuration as knowledge" - your preferences are themselves notes in your second brain.
