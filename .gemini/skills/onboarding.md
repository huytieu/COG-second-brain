# COG Onboarding Playbook

## Goal
Welcome the user and create their COG profile through natural conversation.

## Design Principle
Ask open-ended questions, not option menus. Infer what you can. Never ask redundant questions.

## Steps

### 1. Check for Existing Profile
- Look for `00-inbox/MY-PROFILE.md`
- If exists: Ask "What would you like to update? Just tell me what needs changing."
- If not: Proceed with setup below

### 2. Single Open-Ended Prompt
```
Welcome to COG - your self-evolving second brain!

Tell me a bit about yourself - your name, what you do, and what topics you're most interested in staying sharp on. Feel free to share as much or as little as you'd like.
```

### 3. Extract from Response
Required: **Name**, **Role**, **Interests** (2-3 minimum)
Optional (only if mentioned): News Sources, Projects, Competitive Watchlist

### 4. Follow-Up (Only If Needed)
Only ask ONE follow-up if required fields are missing. Never ask about optional fields.

### 5. Ask About Agent Mode
During confirmation, ask:
- **Solo** (default): Handle everything directly in the conversation
- **Team**: Delegate to specialist sub-agents for deeper results

### 6. Confirm and Create
Show summary, wait for confirmation, then create:

**`00-inbox/MY-PROFILE.md`** with frontmatter:
```yaml
type: profile
created: YYYY-MM-DD
onboarding_completed: true
agent_mode: solo
tags: ["#profile", "#config", "#cog"]
```
Include: Name, Role, Profile Created date, Agent Mode setting, Active Projects (if any)

**`00-inbox/MY-INTERESTS.md`** with topics and preferred sources

**`03-professional/COMPETITIVE-WATCHLIST.md`** (only if they mentioned competitors)

**`04-projects/[project-slug]/PROJECT-OVERVIEW.md`** for each mentioned project

### 7. Create Directory Structure
```
00-inbox/, 01-daily/briefs/ + checkins/, 02-personal/braindumps/ + development/ + wellness/
03-professional/braindumps/ + leadership/ + strategy/ + skills/
04-projects/, 05-knowledge/consolidated/ + patterns/ + timeline/ + booklets/, 06-templates/
```

### 8. Create Welcome Guide
Generate `00-inbox/WELCOME-TO-COG.md` with quick start instructions.

### 9. Wrap Up
Suggest a natural next action (braindump or daily brief). No numbered menus.
