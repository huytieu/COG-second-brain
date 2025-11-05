---
name: onboarding
description: Personalize COG for your workflow - creates profile, interests, and watchlist files with guided setup (run this first!)
---

# COG Onboarding Skill

## Purpose
Welcome new users and collect essential information to personalize their COG experience. All configuration is stored as natural markdown files within the vault structure, following COG's philosophy of transparent, editable knowledge.

## When to Invoke
- User explicitly requests `/onboarding` or mentions "onboarding" or "setup COG"
- User is new and hasn't completed onboarding yet
- User wants to update their profile or add new projects
- Any time profile customization is needed

## Process Flow

### 1. Welcome Message
Greet the user warmly and explain what COG is:
```
Welcome to COG - your self-evolving second brain powered by Claude + Obsidian + Git!

COG helps you:
- Capture thoughts and insights through brain dumps
- Get daily intelligence briefings tailored to your interests
- Build and consolidate knowledge over time
- Track patterns in your thinking and development

Before we begin, I'll ask you a few questions to personalize your experience. This will take about 3-5 minutes.

All your preferences will be stored as readable markdown files in your vault, so you can edit them anytime.
```

### 2. Check for Existing Profile

Look for `00-inbox/MY-PROFILE.md`. If it exists:
```
I found an existing profile! Would you like to:
1. Update your profile
2. Add new projects
3. Update interest areas
4. View current profile
5. Start fresh (archive old profile)

What would you like to do? (1-5)
```

### 3. Information Collection (Keep it Simple!)

Ask only essential questions in a conversational way:

**Question 1: What's your name?**
- Just first name is fine, or full name if they prefer
- Store in: `00-inbox/MY-PROFILE.md`

**Question 2: What do you do? (Your job/role/main activity)**
- This helps personalize content relevance
- Examples: "Software engineer", "Product manager", "Student studying AI", "Entrepreneur"
- Store in: `00-inbox/MY-PROFILE.md`

**Question 3: What topics are you interested in?**
- Ask them to list 3-5 main topics they want to learn about or stay updated on
- Examples: "AI/ML, startups, health optimization", "leadership, product strategy, design"
- Store in: `00-inbox/MY-INTERESTS.md`
- Keep it natural - don't make them choose from categories

**Question 4: Where do you like to get your news and information?**
- Examples: "Hacker News, Twitter, research papers", "TechCrunch, newsletters, podcasts"
- Store in: `00-inbox/MY-INTERESTS.md` under "Preferred Sources"
- This helps COG understand what sources to prioritize

**Question 5: Do you have any active projects you're working on?**
- Optional - if yes, ask for project names (comma-separated)
- For each project, create:
  - `04-projects/[project-slug]/PROJECT-OVERVIEW.md` with basic structure
  - Full directory structure
- If no projects, skip this entirely

**Question 6: Any companies, competitors, or people you want to keep an eye on?** (Optional)
- Optional - if yes, collect the list
- Store in: `03-professional/COMPETITIVE-WATCHLIST.md`
- Used for automatic extraction in braindumps

### 4. Generate Profile Documents

Create the following markdown files:

#### `00-inbox/MY-PROFILE.md`
```markdown
---
type: profile
created: YYYY-MM-DD
onboarding_completed: true
tags: ["#profile", "#config", "#cog"]
---

# My COG Profile

## About Me
- **Name**: [Name]
- **Role**: [Job/role/main activity]
- **Profile Created**: [Date]

## Active Projects
[If they have projects:]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 1]]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 2]]

[If no projects:]
*No active projects yet. Add them anytime by editing this file or running the onboarding skill again.*

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
*Where I like to get information:*
- [Source 1]
- [Source 2]
- [Source 3]

## Notes
*Add any additional context about your interests here.*

---

*Update this file anytime as your interests evolve. Just edit and save—COG will pick up the changes.*
```

#### `03-professional/COMPETITIVE-WATCHLIST.md` (if applicable)
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

### 5. Create Directory Structure
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

### 6. Create Welcome Guide

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

- **[[MY-PROFILE]]** - Your basic info and workflow preferences
- **[[MY-INTERESTS]]** - Topics for your daily briefs
- **[[03-professional/COMPETITIVE-WATCHLIST]]** - Companies you're tracking *(if applicable)*

**You can edit these files anytime.** COG reads them when you use skills, so your changes take effect immediately.

## Quick Start Skills

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

## Tips for Success

- **Don't overthink it**: Just dump your thoughts, COG will help organize
- **Be consistent**: Daily briefs and braindumps work best as habits
- **Review weekly**: Use the weekly-checkin skill to see patterns emerge
- **Evolve your setup**: Edit your profile files anytime or run onboarding again to add projects

## Getting Help

- Check `SETUP.md` for detailed guides
- Visit the GitHub repo for documentation

**Your second brain is learning about you. Let's begin!**

---

*You can archive or delete this welcome guide once you're comfortable with COG.*
```

### 7. First Action Prompts
After setup, guide the user to their first action:

```
Great! Your COG is now configured.

I've created these profile documents for you:
- MY-PROFILE.md (your basic preferences)
- MY-INTERESTS.md (topics for daily briefs)
[If applicable:] - COMPETITIVE-WATCHLIST.md (companies to track)
[If applicable:] - PROJECT-OVERVIEW.md files for each project

All files are in your vault and can be edited anytime.

Would you like to:

1. **Try your first braindump** - Capture what's on your mind right now
2. **Get your daily brief** - See today's intelligence report
3. **Review your profile** - Open MY-PROFILE.md to see/edit settings
4. **Start later** - You're all set, invoke skills when ready

What would you like to do? (1-4)
```

## Configuration Update Mode

If user runs onboarding after initial setup (MY-PROFILE.md exists):

```
You've already completed onboarding! Would you like to:

1. **Update your profile** - Edit MY-PROFILE.md with new preferences
2. **Add new interests** - Update MY-INTERESTS.md with new topics
3. **Add new projects** - Create new project structures
4. **View current profile** - See your current MY-PROFILE.md

What would you like to do? (1-4)
```

## Success Criteria

Onboarding is successful when:
1. ✅ `MY-PROFILE.md` created in `00-inbox/`
2. ✅ `MY-INTERESTS.md` created in `00-inbox/`
3. ✅ Project directories and overviews created (if applicable)
4. ✅ `WELCOME-TO-COG.md` guide created
5. ✅ User understands next steps and where their profile is stored

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
- `00-inbox/MY-PROFILE.md` - Basic profile
- `00-inbox/MY-INTERESTS.md` - Interest areas
- `03-professional/COMPETITIVE-WATCHLIST.md` - Competitive tracking
- `04-projects/[project]/PROJECT-OVERVIEW.md` - Project details

Benefits of markdown storage:
- ✅ Human-readable and editable
- ✅ Version controlled with Git
- ✅ Searchable in Obsidian
- ✅ Linkable from other notes
- ✅ No parsing required, just read as text
- ✅ Can be archived, moved, organized like any other note

## Philosophy

COG's configuration is **knowledge, not configuration**. By storing preferences as markdown notes:
- They're part of your knowledge base, not hidden config files
- You can link to them, reference them, evolve them
- They have context and can include your own notes
- They're transparent and auditable
- They benefit from all of Obsidian's features (tags, links, search, graph view)

This is "configuration as knowledge" - your preferences are themselves notes in your second brain.
