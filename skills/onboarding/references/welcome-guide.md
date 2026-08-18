# Welcome guide template

Verbatim markdown template for `00-inbox/WELCOME-TO-COG.md`, generated in onboarding Step 8 (Create Welcome Guide).

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
