# COG: Agentic Second Brain - Universal Agent Commands

This document defines the available commands/skills for AI agents interacting with COG (Cognition + Obsidian + Git) - a self-evolving agentic second brain system.

**Compatible with:** OpenAI agents, Claude (via this file), and any AI that reads markdown.

> **Note:** Claude Code users should use `.claude/skills/` and Kiro users should use `.kiro/powers/` for native support. This file serves as universal documentation for all other agents.

## Available Commands

### /onboarding

**Description:** Personalize COG for your workflow - creates profile, interests, and watchlist files with guided setup.

**Triggers:**
- `/onboarding`
- "onboarding"
- "setup COG"
- "setup my profile"
- "get started"

**Purpose:** Welcome new users and collect essential information to personalize their COG experience. Creates profile documents stored as markdown files within the vault.

**What it does:**
1. Collects user name, role, interests, and preferred news sources
2. Creates `00-inbox/MY-PROFILE.md` with basic preferences
3. Creates `00-inbox/MY-INTERESTS.md` with topics for daily briefs
4. Optionally creates project structures in `04-projects/`
5. Optionally creates `03-professional/COMPETITIVE-WATCHLIST.md`
6. Generates a welcome guide

**Run this first** if you're new to COG.

---

### /braindump

**Description:** Quick capture of raw thoughts with intelligent domain classification and competitive intelligence extraction.

**Triggers:**
- `/braindump`
- "braindump"
- "brain dump"
- "capture thoughts"
- "write down ideas"
- "get thoughts out of my head"

**Purpose:** Transform raw thoughts into strategic intelligence through quick capture, systematic analysis, pattern recognition, and domain-aware insight extraction with minimal user friction.

**What it does:**
1. Accepts stream-of-consciousness input (any format)
2. Classifies content by domain (personal/professional/project-specific)
3. Extracts themes, questions, decisions, and action items
4. Generates strategic insights and pattern recognition
5. Auto-extracts competitive intelligence if watchlist exists
6. Saves structured output to appropriate domain folder

**Output locations:**
- Personal: `02-personal/braindumps/`
- Professional: `03-professional/braindumps/`
- Project: `04-projects/[project-slug]/braindumps/`
- Mixed: `00-inbox/`

---

### /daily-brief

**Description:** Generate personalized news intelligence with verified sources (7-day freshness requirement).

**Triggers:**
- `/daily-brief`
- "daily brief"
- "news"
- "what's happening"
- "morning brief"
- "daily news"

**Purpose:** Find verified, relevant news for personalized daily briefings with strict verification standards and strategic relevance analysis tailored to user's specific interests and projects.

**What it does:**
1. Reads user interests from `00-inbox/MY-INTERESTS.md`
2. Searches for news within last 7 days only
3. Verifies sources with credibility assessment (Tier 1/2/3)
4. Analyzes strategic relevance to user's role and projects
5. Identifies opportunities and threats
6. Generates comprehensive briefing with sources

**Output location:** `01-daily/briefs/daily-brief-YYYY-MM-DD.md`

**Key features:**
- All news must be from last 7 days (mandatory)
- Minimum 2 credible sources per claim
- Confidence levels explicitly stated
- Action items and recommendations included

---

### /weekly-checkin

**Description:** Cross-domain pattern analysis and strategic reflection for weekly review.

**Triggers:**
- `/weekly-checkin`
- "weekly checkin"
- "weekly check-in"
- "weekly review"
- "reflect on my week"
- "week reflection"

**Purpose:** Comprehensive weekly review and analysis integrating insights across all domains (personal, professional, projects) with pattern recognition and strategic planning.

**What it does:**
1. Scans recent braindumps, briefs, and check-ins
2. Guides user through reflection questions
3. Reviews each domain (personal, professional, projects)
4. Identifies patterns across the week
5. Helps set priorities for next week
6. Generates structured check-in document

**Output location:** `01-daily/checkins/weekly-checkin-YYYY-MM-DD.md`

**Covers:**
- Overall week assessment and rating
- Personal wellness and growth
- Professional accomplishments
- Project progress for each active project
- Cross-domain patterns and insights
- Forward planning with priorities

---

### /knowledge-consolidation

**Description:** Build frameworks from scattered insights across all braindumps and notes.

**Triggers:**
- `/knowledge-consolidation`
- "consolidate knowledge"
- "build frameworks"
- "synthesize insights"
- "extract patterns"

**Purpose:** Transform scattered insights from braindumps, daily briefs, and check-ins into coherent frameworks and "single source of truth" knowledge documents through pattern recognition and systematic synthesis.

**What it does:**
1. Scans vault for unprocessed content (braindumps, briefs, check-ins)
2. Applies pattern recognition (frequency, temporal, domain correlation)
3. Identifies contradictions and cross-cutting patterns
4. Develops actionable frameworks from patterns
5. Updates existing frameworks or creates new ones
6. Generates consolidation report
7. Marks processed braindumps as consolidated

**Output locations:**
- Frameworks: `05-knowledge/consolidated/[framework-name]-framework.md`
- Patterns: `05-knowledge/patterns/pattern-[name].md`
- Timeline: `05-knowledge/timeline/[topic]-evolution-YYYY-MM.md`
- Reports: `05-knowledge/consolidated/consolidation-YYYY-MM-DD.md`

---

### /url-dump

**Description:** Quick capture URLs with automatic content extraction, insights, and categorization into knowledge booklets.

**Triggers:**
- `/url-dump`
- "url dump"
- "save this link"
- "bookmark this"
- "save for later"
- Pasting a URL

**Purpose:** Transform raw URLs into structured, insightful knowledge entries through intelligent content extraction, categorization, and integration with the user's knowledge base.

**What it does:**
1. Validates and fetches URL content
2. Extracts title, author, date, main content
3. Auto-categorizes (articles, tools, reference, research, etc.)
4. Generates summary and key insights
5. Assesses relevance to user interests/projects
6. Creates structured bookmark file

**Categories:**
- Articles & Blogs
- Tools & Resources
- Reference & Documentation
- Research & Papers
- Inspiration & Design
- Videos & Media
- News & Updates
- Project-Specific

**Output locations:**
- Standard: `05-knowledge/booklets/[category]/[title-slug]-YYYY-MM-DD.md`
- Project-specific: `04-projects/[project-slug]/resources/`
- Unclear: `00-inbox/`

---

## Vault Structure

```
COG-second-brain/
├── 00-inbox/              # Landing zone, profile files
│   ├── MY-PROFILE.md      # User profile (created by onboarding)
│   └── MY-INTERESTS.md    # User interests (created by onboarding)
├── 01-daily/              # Daily content
│   ├── briefs/            # Daily intelligence briefs
│   └── checkins/          # Weekly check-ins
├── 02-personal/           # Personal domain
│   └── braindumps/        # Personal braindumps
├── 03-professional/       # Professional domain
│   ├── braindumps/        # Work-related braindumps
│   └── COMPETITIVE-WATCHLIST.md
├── 04-projects/           # Project-specific content
│   └── [project-slug]/
│       ├── PROJECT-OVERVIEW.md
│       ├── braindumps/
│       ├── competitive/
│       └── resources/
├── 05-knowledge/          # Consolidated knowledge
│   ├── consolidated/      # Frameworks and reports
│   ├── patterns/          # Identified patterns
│   ├── timeline/          # Thinking evolution
│   └── booklets/          # URL bookmarks by category
└── 06-templates/          # Document templates
```

---

## Quick Start

1. **New user?** Run `/onboarding` first to set up your profile
2. **Capture thoughts?** Use `/braindump` anytime
3. **Morning routine?** Run `/daily-brief` for your intelligence briefing
4. **End of week?** Use `/weekly-checkin` to reflect
5. **Save a link?** Use `/url-dump` with the URL
6. **Build knowledge?** Run `/knowledge-consolidation` periodically

---

## Configuration

All configuration is stored as readable markdown files:
- `00-inbox/MY-PROFILE.md` - Basic profile and active projects
- `00-inbox/MY-INTERESTS.md` - Topics for news curation
- `03-professional/COMPETITIVE-WATCHLIST.md` - Companies/people to track

Edit these files anytime - changes take effect immediately.

---

## Task Format

All skills generate tasks with [Obsidian Tasks emoji format](https://publish.obsidian.md/tasks/Reference/Task+Formats/Tasks+Emoji+Format) for dashboard compatibility:

```markdown
- [ ] Action item 📅 YYYY-MM-DD
```

**Date calculation by context:**
- "Immediate (24-48 hours)" → tomorrow's date
- "Short-term (1-2 weeks)" → +1 week from today
- "Today/This Week" → today or end of week
- "Next Steps" → next Monday/Friday

This enables:
- Tasks dashboard queries ("due today", "due this week")
- Daily notes task views
- Date-based filtering and sorting

---

## Philosophy

COG follows these principles:
- **Verification-first:** All information sourced and verified
- **Transparency:** Confidence levels explicitly stated
- **Configuration as knowledge:** Preferences stored as editable notes
- **Self-evolving:** Patterns and frameworks grow over time
- **Low friction:** Quick capture, systematic organization
- **Obsidian Tasks compatible:** All tasks include emoji due dates
