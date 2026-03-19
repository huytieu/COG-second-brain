# COG: Agentic Second Brain - Universal Agent Commands

This document defines the available commands/skills for AI agents interacting with COG (Cognition + Obsidian + Git) - a self-evolving agentic second brain system.

**Compatible with:** OpenAI agents, Claude (via this file), and any AI that reads markdown.

> **Note:** Claude Code users should use `.claude/skills/` and Kiro users should use `.kiro/powers/` for native support. This file serves as universal documentation for all other agents.

## Available Commands

### /onboarding

**Description:** Personalize COG for your workflow - creates profile, interests, and watchlist files with a smart, conversational setup.

**Triggers:**
- `/onboarding`
- "onboarding"
- "setup COG"
- "setup my profile"
- "get started"

**Purpose:** Welcome new users and collect essential information to personalize their COG experience through natural conversation - not sequential form-filling. Creates profile documents stored as markdown files within the vault.

**How it works:**
1. Asks ONE open-ended question: "Tell me about yourself - name, role, and what you're interested in"
2. Intelligently parses the response to extract name, role, interests, projects, news sources, and competitive watchlist
3. Only asks a follow-up if required info (name, role, interests) is still missing
4. Asks about agent mode preference (solo vs team) during confirmation
5. Confirms extracted info before creating files
6. Matches role to a role pack (`.claude/roles/*.md`) for personalized skill and integration recommendations
7. Discovers integrations — presents role-specific recommendations, asks which tools the user already uses
8. Creates `00-inbox/MY-PROFILE.md` with role_pack, agent_mode, and preferences
9. Creates `00-inbox/MY-INTERESTS.md` with topics for daily briefs
10. Creates `00-inbox/MY-INTEGRATIONS.md` with active/disabled integrations
11. Optionally creates project structures in `04-projects/` and `03-professional/COMPETITIVE-WATCHLIST.md` (only if mentioned)
12. Generates a welcome guide with role-ordered skills and integration status

**Agent modes:**
- **Solo** (default): All skills handle everything directly in one conversation
- **Team**: Skills delegate research, analysis, and writing to specialist sub-agents for deeper results (works best with Claude Code)

**Design principle:** Never ask redundant questions. Never show numbered option menus. Infer what you can from context.

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

### /scout

**Description:** Evaluate URLs and tools — check vault coverage, assess relevance, recommend save or skip.

**Triggers:**
- `/scout`
- "scout this"
- "evaluate this"
- "should I save this?"
- "is this relevant?"

**Purpose:** Lightweight triage that sits between "ignore" and `/url-dump`. Checks existing vault coverage, assesses relevance to your profile and interests, and recommends save or skip.

**What it does:**
1. Accepts URL(s) or tool name(s)
2. Searches the entire vault for existing coverage (duplicates, mentions)
3. If new — fetches content, detects type (tool, article, repo, research, news, reference)
4. Assesses relevance against your profile (projects, role, tech stack) and interests
5. Recommends **Save** (hands off to `/url-dump` with pre-filled category) or **Skip** (explains why)
6. Supports batch mode (multiple URLs in one invocation)

**Boundary with `/url-dump`:** Scout evaluates ("should I save this?"). URL-dump saves ("save this now"). If you already know you want to save, use `/url-dump` directly.

---

### /update-cog

**Description:** Check for and apply upstream COG framework updates without touching personal content.

**Triggers:**
- `/update-cog`
- "update COG"
- "check for updates"
- "get latest COG version"
- "upgrade COG"
- "new COG version"

**Purpose:** Safely update framework files (skills, docs, scripts) from the official upstream repository while leaving all personal content untouched.

**What it does:**
1. Reads `COG-VERSION` to determine current version
2. Adds/fetches the `cog-upstream` remote from the official repo
3. Compares each framework file against upstream
4. Detects customizations and offers per-file keep/overwrite/backup
5. Applies updates via surgical `git checkout` (no merge conflicts)
6. Reports updated files and suggests committing

**Shell script alternative:**
```bash
./cog-update.sh           # Interactive
./cog-update.sh --check   # Check for updates
./cog-update.sh --dry-run # Preview changes
./cog-update.sh --force   # Update all without prompting
```

**Safety:** Content folders (`00-inbox/`, `01-daily/`, `02-personal/`, etc.) are NEVER touched. Only framework files (skills, docs, scripts) are updated.

---

### /auto-research

**Description:** Deep strategic research engine — decomposes questions into parallel research threads, spawns multiple agents, and synthesizes into actionable strategic analysis.

**Triggers:**
- `/auto-research`
- "research [topic]"
- "investigate [question]"
- "strategic analysis"
- "deep dive into [topic]"

**Purpose:** Take a high-level strategic question, decompose it into 5-7 parallel research threads, investigate each with real web sources, and synthesize findings into an actionable strategic analysis with scenarios and recommendations.

**What it does:**
1. Decomposes the question into independent research threads (market forces, historical precedent, player analysis, technology trajectory, emerging tech, contrarian view, etc.)
2. Presents decomposition for user approval before launching research
3. Spawns parallel research agents (team mode) or runs sequential research passes (solo mode)
4. Each thread searches 8-12 high-quality sources via web search
5. Synthesizes all threads into a unified strategic analysis with scenarios, options, and recommendations
6. Saves to vault with executive summary

**Output location:** `05-knowledge/research/YYYY-MM-DD-[slug].md`

**Key features:**
- No hallucinated sources — every claim traces to real web search results
- Emerging tech thread always included — surfaces pre-mainstream concepts
- Contrarian view section challenges consensus
- Confidence levels and gaps explicitly stated

---

### PM Workflow Skills

The following 6 skills form a complete product management lifecycle:
**Research** → **PRD** → **Stories** → Development → **Release Notes** → **Knowledge Base**

### /create-user-story

**Description:** Create user stories with duplicate checking across Linear, GitHub Issues, or Jira.

**Triggers:**
- `/create-user-story`
- "create a user story"
- "create a story for"
- "new user story"

**Purpose:** Create well-structured user stories in your project tracker with automatic duplicate detection, standard As a/I want/So that format, and Given/When/Then acceptance criteria.

**What it does:**
1. Accepts problem statement and solution from user
2. Checks active integrations (Linear, GitHub, Jira) in `00-inbox/MY-INTEGRATIONS.md`
3. Searches for potential duplicate issues in the active tracker
4. If duplicates found, stops and shows candidates
5. If no duplicates, creates story with user story format and acceptance criteria
6. Saves a copy to `04-projects/[project]/stories/`

**Output:** Issue created in active tracker + local copy in vault

---

### /generate-prd

**Description:** Draft product requirement documents with an approval gate before publishing.

**Triggers:**
- `/generate-prd`
- "generate a PRD"
- "draft PRD"
- "product requirements"

**Purpose:** Generate structured PRDs from problem context, save to vault, and optionally publish to Confluence/Notion with explicit human approval.

**What it does:**
1. Collects problem statement, goals, user context from user
2. Reads existing project context from `04-projects/` and `05-knowledge/`
3. Drafts PRD with standard sections (Problem, Goals, Non-goals, User workflows, Functional requirements, Iterations, Dependencies, Risks, Success metrics)
4. Saves to `04-projects/[project]/PRDs/PRD-[slug].md`
5. Presents summary and asks for explicit approval before any publishing
6. Only publishes to Confluence/Notion if user explicitly approves

**Output location:** `04-projects/[project]/PRDs/PRD-[slug].md`

---

### /generate-release-notes

**Description:** Generate release notes from GitHub milestones, Linear cycles, or manual input.

**Triggers:**
- `/generate-release-notes`
- "generate release notes"
- "release notes for"
- "what shipped in"

**Purpose:** Compile release notes by pulling completed issues/PRs from your tracker, categorizing into enhancements, improvements, and bug fixes.

**What it does:**
1. Identifies release scope (GitHub milestone, Linear cycle, or manual list)
2. Fetches all completed issues/PRs in the release
3. Categorizes into Enhancements, Technical Improvements, Bug Fixes
4. Generates formatted release notes markdown
5. Saves to `04-projects/[project]/releases/`
6. Optionally publishes to Confluence with approval

**Output location:** `04-projects/[project]/releases/release-notes-[version]-YYYY-MM-DD.md`

---

### /export-open-issues

**Description:** Audit and export open issues from any project tracker.

**Triggers:**
- `/export-open-issues`
- "export open issues"
- "issue audit"
- "open issues report"

**Purpose:** Generate a structured audit of all open issues from your active tracker for review, grooming, or stakeholder reporting.

**What it does:**
1. Checks active integrations for available trackers
2. Fetches all open issues with metadata (assignee, priority, labels, dates)
3. Generates summary statistics and categorized breakdown
4. Identifies stale issues, unassigned work, and priority imbalances
5. Saves structured report to vault

**Output location:** `04-projects/[project]/audits/open-issues-YYYY-MM-DD.md`

---

### /publish-to-confluence

**Description:** Publish any vault markdown file to Confluence.

**Triggers:**
- `/publish-to-confluence`
- "publish to Confluence"
- "push to Confluence"

**Purpose:** Publish a local markdown file from the vault to a Confluence page (create or update), with explicit approval before publishing.

**What it does:**
1. Accepts path to local markdown file
2. Requires Confluence integration to be active
3. Converts markdown to Confluence-compatible format
4. Creates new page or updates existing page
5. Returns published page URL

**Requires:** Confluence integration active in `00-inbox/MY-INTEGRATIONS.md`

---

### /update-knowledge-base

**Description:** Maintain product knowledge base from releases, features, and project changes.

**Triggers:**
- `/update-knowledge-base`
- "update knowledge base"
- "update KB"
- "sync knowledge base"

**Purpose:** Keep your product knowledge base in `05-knowledge/` current by incorporating release data, feature updates, and project changes.

**What it does:**
1. Reads current knowledge base files from `05-knowledge/`
2. Accepts feature updates and/or release version as input
3. Cross-references with project PRDs and release notes in `04-projects/`
4. Updates knowledge base with factual, thorough changes
5. Optionally syncs to external wiki (Confluence/Notion) with approval

**Output location:** `05-knowledge/consolidated/product-knowledge-base.md`

---

## Vault Structure

```
COG-second-brain/
├── .claude/roles/         # Role packs for personalized recommendations
├── 00-inbox/              # Landing zone, profile files
│   ├── MY-PROFILE.md      # User profile with role pack (created by onboarding)
│   ├── MY-INTERESTS.md    # User interests (created by onboarding)
│   └── MY-INTEGRATIONS.md # Active/disabled integrations (created by onboarding)
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
6. **Evaluate a tool?** Use `/scout` to check relevance before saving
7. **Build knowledge?** Run `/knowledge-consolidation` periodically
8. **Create user stories?** Use `/create-user-story` with a problem/solution
9. **Draft a PRD?** Use `/generate-prd` with your problem context
10. **Release notes?** Use `/generate-release-notes` with a version
11. **Strategic research?** Use `/auto-research` with your question

---

## Configuration

All configuration is stored as readable markdown files:
- `00-inbox/MY-PROFILE.md` - Profile, role pack, agent mode, and active projects
- `00-inbox/MY-INTERESTS.md` - Topics for news curation
- `00-inbox/MY-INTEGRATIONS.md` - Active/disabled external service integrations
- `03-professional/COMPETITIVE-WATCHLIST.md` - Companies/people to track

Edit these files anytime - changes take effect immediately.

### Role Packs

COG matches your role to a role pack during onboarding. Role packs (in `.claude/roles/`) define:
- Which skills are most relevant for your role
- Which integrations to recommend
- Suggested agent mode (solo vs team)

Available packs: Product Manager, Engineering Lead, Engineer, Designer, Founder, Marketer. Create custom packs from `_template.md`.

## Version & Updates

COG tracks its version in `COG-VERSION` (currently 3.3.0). To check for updates:
- Run `/update-cog` in any supported agent
- Or use the shell script: `./cog-update.sh --check`

Updates only touch framework files (skills, docs, scripts) — your personal content is never modified.

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
