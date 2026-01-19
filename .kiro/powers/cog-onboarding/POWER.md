---
name: "cog-onboarding"
displayName: "COG Onboarding"
description: "Personalize COG second brain for your workflow - creates profile, interests, and watchlist files with guided setup"
keywords: ["onboarding", "setup COG", "setup profile", "get started", "configure COG", "personalize", "my profile"]
---

# COG Onboarding Power

Welcome new users and collect essential information to personalize their COG (Claude + Obsidian + Git) second brain experience.

## When This Power Activates

- User mentions "onboarding", "setup", or "get started"
- User is new and hasn't completed onboarding yet
- User wants to update their profile or add new projects

## Onboarding Steps

### 1. Check for Existing Profile

Look for `00-inbox/MY-PROFILE.md` in the vault:
- If exists: Offer update mode (update profile, add interests, add projects, view current, start fresh)
- If not found: Proceed with full onboarding

### 2. Collect Information (Keep it Simple!)

Ask only essential questions conversationally:

1. **Name** - First name or full name
2. **Role** - Job/role/main activity (e.g., "Software engineer", "Product manager")
3. **Interests** - 3-5 topics to learn about or stay updated on
4. **News Sources** - Preferred information sources (e.g., "Hacker News, Twitter")
5. **Active Projects** - Optional, comma-separated project names
6. **Competitive Watch** - Optional, companies/people to track

### 3. Generate Profile Documents

Create these markdown files:

**`00-inbox/MY-PROFILE.md`** - Basic profile with name, role, active projects
**`00-inbox/MY-INTERESTS.md`** - Topics and preferred news sources
**`03-professional/COMPETITIVE-WATCHLIST.md`** - If tracking competitors
**`04-projects/[project-slug]/PROJECT-OVERVIEW.md`** - For each project

### 4. Create Directory Structure

```
00-inbox/
01-daily/briefs/, checkins/
02-personal/braindumps/, development/, wellness/
03-professional/braindumps/, leadership/, strategy/, skills/
04-projects/[project-slug]/braindumps/, competitive/, content/, planning/, resources/
05-knowledge/consolidated/, patterns/, timeline/, booklets/
06-templates/
```

### 5. Generate Welcome Guide

Create `00-inbox/WELCOME-TO-COG.md` with quick start instructions.

## Success Criteria

- MY-PROFILE.md created in 00-inbox/
- MY-INTERESTS.md created in 00-inbox/
- Project directories created if applicable
- Welcome guide created
- User understands next steps

## Configuration Philosophy

All configuration is stored as readable markdown files:
- Human-readable and editable
- Version controlled with Git
- Searchable in Obsidian
- Linkable from other notes

**Run this first** if you're new to COG.
