# COG Braindump Playbook

## Goal
Capture raw thoughts and transform them into structured, classified intelligence.

## Pre-Flight
1. Read `00-inbox/MY-PROFILE.md` for name, role, projects, agent_mode
2. Read `03-professional/COMPETITIVE-WATCHLIST.md` for tracked entities
3. If no profile exists, suggest running `/onboarding` first

## Steps

### 1. Prompt for Input
Ask the user to share their thoughts. Accept any format — stream of consciousness is fine.

### 2. Classify Domain
Analyze content and classify into:
- **Personal** → `02-personal/braindumps/`
- **Professional** → `03-professional/braindumps/`
- **Project-specific** → `04-projects/[project-slug]/braindumps/`
- **Mixed/unclear** → `00-inbox/`

### 3. Extract & Analyze
From the raw input, extract:
- **Key themes** (3-5 main topics)
- **Questions raised** (explicit or implicit)
- **Decisions needed** (with options if apparent)
- **Action items** with Obsidian Tasks dates: `- [ ] Task 📅 YYYY-MM-DD`
- **Competitive intelligence** (if entities from watchlist are mentioned)
- **Emotional context** (energy level, stress indicators)
- **Connections** to previous braindumps or knowledge

### 4. Generate Output File
Save to appropriate domain folder as `braindump-YYYY-MM-DD-[slug].md` with:
```yaml
type: braindump
created: YYYY-MM-DD
domain: personal|professional|project
project: [if applicable]
themes: [list]
tags: [auto-generated]
```

Include sections: Raw Capture, Key Themes, Strategic Insights, Questions & Decisions, Action Items, Connections

### 5. Extract Competitive Intelligence
If watchlist entities are mentioned, save intel to `04-projects/[project]/competitive/[entity-slug].md`
