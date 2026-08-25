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

**References:** `references/profile-templates.md` (the four profile document templates), `references/welcome-guide.md` (the WELCOME-TO-COG template).

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

**References:** `references/templates.md` (all five consolidation document templates).

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

### /loop-engineering

**Description:** Shared loop-engineering reference for COG skills - the agent loop, deterministic verifiers, termination conditions, in-loop context management, and named patterns.

**Triggers:**
- `/loop-engineering`
- "loop engineering"
- Designing or debugging a skill that iterates (search-verify-retry, scan-until-dry, fetch-retry-gate)

**Purpose:** Give every iterative COG skill one vocabulary for the act-observe-verify loop, so each one declares its verifier, its termination conditions, and its pattern instead of repeating the rules.

**What it provides:**
1. The COG loop cycle (gather, act, observe, verify, update, decide)
2. The five termination conditions (deterministic verifier, hard cap, budget guard, no-progress detection, human escalation)
3. The verification-first rule applied to loops (trust mechanical checks, never agent self-report)
4. In-loop context management (compaction, pruning, externalize-to-vault, sub-agent isolation)
5. A named-pattern table (ReAct, Reflexion, plan-execute-verify, evaluator-optimizer, orchestrator-workers, loop-until-dry, human-in-the-loop) and failure modes

**Used by:** daily-brief, knowledge-consolidation, url-dump, weekly-checkin (and applies to auto-research, scout, team-brief).

---

### /team-brief

**Description:** Generate a daily team intelligence brief by cross-referencing Linear, Slack, GitHub, PostHog, meetings, and braindumps — then sync the resulting intelligence back into Linear.

**Triggers:**
- `/team-brief`
- "team brief"
- "what did we ship?"
- "daily team update"
- "summarize the team's progress"

**Purpose:** Build an evidence-backed operating brief for product and engineering leads by combining multiple sources of truth, highlighting blockers and momentum, and writing the most important updates back to Linear.

**What it does:**
1. Pulls active initiatives, projects, and issues from Linear
2. Cross-references GitHub PRs, Slack discussions, meetings, PostHog, and braindumps
3. Summarizes shipped work, in-progress work, risks, and signals that matter
4. Writes initiative status updates and issue/project sync-backs into Linear where appropriate
5. Produces a concise brief with a Linear sync report

**Output location:** `03-professional/team-briefs/team-brief-YYYY-MM-DD.md`

**References:** `references/agent-prompts.md` (the six Phase-2 sub-agent prompts), `references/publish-templates.md` (HackMD + Slack payloads), `references/brief-frontmatter.md` (the metadata template).

---

### /meeting-transcript

**Description:** Process meeting transcripts into structured decisions, action items, and strategic themes.

**Triggers:**
- `/meeting-transcript`
- "process this meeting"
- "analyze this transcript"
- "summarize this meeting"
- "meeting notes from transcript"

**Purpose:** Turn noisy transcripts into clean decision records, action items, and key strategic signals without losing the substance of the conversation.

**What it does:**
1. Cleans transcript noise and identifies speakers/topics
2. Extracts decisions, action items, unresolved questions, and strategic themes
3. Highlights stakeholder concerns, alignment, and follow-up needs
4. Formats the result into a reusable meeting note

**Output location:** `03-professional/meetings/meeting-transcript-YYYY-MM-DD-[slug].md`

---

### /comprehensive-analysis

**Description:** Run a deep 7-day product, team, and strategy analysis for weekly reviews, board prep, or planning.

**Triggers:**
- `/comprehensive-analysis`
- "weekly analysis"
- "board prep"
- "comprehensive analysis"
- "deep weekly review"

**Purpose:** Synthesize the last week across product, engineering, customer signals, and strategy into a single high-signal analysis for leaders.

**What it does:**
1. Reviews recent team briefs, meetings, project artifacts, and external signals
2. Identifies what shipped, what changed, what is blocked, and what needs leadership attention
3. Surfaces trends, risks, opportunities, and recommended actions
4. Produces an executive-ready synthesis with confidence levels and open questions

**Output location:** `03-professional/analysis/comprehensive-analysis-YYYY-MM-DD.md`

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

### /memory-hygiene

**Description:** Periodic trust sweep of persistent memory and durable knowledge notes - re-verifies environment-dependent claims against the live environment, stamps `last_verified` + `confidence`, and proposes archiving drifted entries.

**Triggers:**
- `/memory-hygiene`
- "audit my memories"
- "check for stale memories"
- After a memory misfires (a recalled fact turned out wrong)

**Purpose:** Prevent the **stale-but-confident** failure mode: an entry that was correct when written silently drifts after the environment changes, yet still ranks high at recall and gets acted on. Makes trust a runtime decision, not a property of the stored item.

**What it does:**
1. Sweeps agent memory files and environment-referencing notes in `05-knowledge/`
2. Classifies claims: environment-dependent (verify with `ls`/`curl`/`gh`) vs preference/judgment (check only for contradiction with newer entries)
3. Stamps `last_verified` + `confidence` (high/medium/low) into each entry's frontmatter
4. Fixes verified-wrong facts in place; proposes (never auto-applies) archiving obsolete entries
5. Writes one sweep report to `01-daily/` with a drift scorecard and deltas vs the previous sweep

**Budget:** ~1 minute per entry. Unverifiable ≠ drifted.

---

### /content-factory

**Description:** Autonomous content pipeline - scout announcements in your field, triage by trend momentum and personal angle, produce posts/blogs/videos in your voice with ledger-based dedup, hard volume caps, and screenshot-verified publishing.

**Triggers:**
- `/content-factory`
- "run the content factory"
- "turn today's news into content"
- Scheduled runs (e.g. nightly via cron)

**Purpose:** Act as the user's autonomous content creator with zero duplicates, hard per-night volume caps, and verification before anything counts as published. An empty run is a valid run; a low-quality post is not.

**What it does:**
1. SCOUT — web-search + watchlist fetch for last-24h announcements (timeboxed ~20 min)
2. TRIAGE — score candidates on trend momentum, beat fit, and unique angle; produce at ≥11/15, park 8-10, ignore <8; dedup against the ledger
3. PRODUCE — format ladder decided by substance: short post by default, blog only with ≥3 original things or a real PoC, short video only if demo-able
4. PUBLISH — environment gate, then post-condition check: screenshot/curl the live artifact before recording it as published
5. LEDGER + LOG — append to `04-projects/content-factory/ledger.md` and the tonight file, even for empty runs

**Output:** Published links in the ledger; parked ideas and proposals in the run log.

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

### Verification Harness Skills

The following 5 skills implement the V-model closed loop described in `WORKFLOW.md`: the worker never grades its own homework.

**They are opt-in.** None of them run unless you invoke the skill, ask for the closed loop / proper verification / an evidence trail in those words, or set `verification_harness: on` in `00-inbox/MY-PROFILE.md`. Ordinary work (notes, briefs, research, drafts, edits) carries no checkpoints, no lane classification, and no evidence ledger. `WORKFLOW.md` governs harness runs and nothing else.

---

### /closed-loop

**Description:** V-model execute pipeline: CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify → CP-5 acceptance. Every verify step emits evidence rows traced to acceptance criterion IDs (`AC-n`).

**Triggers:**
- `/closed-loop <task>` or `/closed-loop <spec-path>`
- "run this through the closed loop", "verify this properly", "give me an evidence trail"
- `verification_harness: on` in your profile, on a build task
- Another skill declaring a `normal`+ lane reaching its verify step

Not triggered by an ordinary request. A task that mutates external state still owes the post-condition check (observe the artifact) whether or not the full loop runs.

**Purpose:** Prevent the **confident-but-unchecked** failure mode. A worker reports success, nothing downstream validates it, and a plausible-but-wrong result ships. The loop makes success a *verified observation*, not a claim.

**What it does:**
1. Classifies the task into a risk lane (`bash .claude/lib/lane-classify.sh classify "<task>"`)
2. Runs the worker at CP-3, traced to `AC-n`
3. Dispatches a fresh-context, read-only `task-verifier` at CP-3v that observes the *artifact* (curl the URL, re-read the file, screenshot the page), never the worker's summary
4. On `FAIL:fixable`, dispatches `fix-agent` (max 2 retries), then re-verifies; on `FAIL:escalate`, stops
5. Runs `integration-verifier` at CP-4 for multi-task / `full`-lane work
6. Records checkpoints and evidence rows to the run's `evidence/ledger.md`

**Output:** Evidence ledger with one `EVIDENCE <AC-id> | <CP> | PASS|FAIL | <observation> | <artifact>` row per criterion, plus `.claude/logs/loop-ledger.tsv`.

---

### /ultragoal

**Description:** Run a goal too big to ship in one session: a chain of phases, each its own full closed-loop run, with cross-session state and a final north-star acceptance gate.

**Triggers:**
- `/ultragoal <goal>`
- "make this an ultragoal", "this is a multi-week thing"
- Resuming a long-running goal in a cold session

Never started unprompted. A big task is not an ultragoal until you call it one.

**Purpose:** Wrongness compounds across sessions. A goal spanning weeks accumulates unverified assumptions that no single run ever revisits. Ultragoals never downgrade the lane: every phase runs CP-1 → CP-6 with adversarial verification, and nothing is "done" until every `AC-n` has a PASS row.

**What it does:**
1. Interviews you for the **north-star** in one sentence, then writes falsifiable `AC-n` into `04-projects/<goal>/spec.md`
2. Decomposes into phases `P0…Pn`, each traced to criteria
3. Runs each phase as a complete closed-loop run with per-phase evidence in `04-projects/<goal>/evidence/P<n>/`
4. Maintains `04-projects/<goal>/STATUS.md` so any cold session resumes without re-reading history
5. Regenerates a self-contained `report.html` at every phase gate (north-star, phase timeline, `AC-n` traceability, evidence, next action)
6. Runs a final **north-star acceptance verifier** before the goal is declared done

**Output:** `04-projects/<goal>/` containing `spec.md`, `STATUS.md`, `evidence/`, and `report.html`.

---

### /harvest

**Description:** Capture durable session learnings, stage them for human promotion into `05-knowledge/`, and propose skill/CLAUDE.md patches. Never writes durable knowledge without your approval.

**Triggers:**
- `/harvest`
- After a correction, a rejected deliverable, or a surprising discovery, when you ask for it
- A scheduled self-enhancement job, if you set one up

COG ships no hooks, so nothing stages automatically until you wire it up yourself.

**Purpose:** Tacit knowledge dies in the transcript. Corrections you made, workarounds discovered, and patterns that worked are all lost when the session closes. Harvest catches them at the boundary, but stages rather than commits, because auto-promoting session noise into durable knowledge poisons the well.

**What it does:**
1. Scans the session for corrections, rejected outputs, non-obvious discoveries, and repeated friction
2. Writes candidates to `04-projects/harness/harvest/staging-<date>.md` with the evidence that motivated each
3. Optionally dispatches `harvest-curator` (Sonnet, propose-only) to shape candidates into adoption notes
4. Presents them for approval; flags contradictions with existing knowledge rather than silently overwriting
5. On `/harvest promote`, writes approved items into `05-knowledge/` and proposes skill/CLAUDE.md patches

**Output:** `04-projects/harness/harvest/staging-<date>.md` (staged) → `05-knowledge/` (promoted, after approval).

---

### /retro

**Description:** CP-7 retrospective: audit the run's checkpoints, evidence quality, action items, and harvest candidates. Closes the V-model cycle and feeds the next one.

**Triggers:**
- `/retro <run or spec>`
- After any ship (CP-6) or escalation
- After a significant session, whatever the outcome

**Purpose:** A closed loop that never inspects itself stops improving. Retro asks the question the verifiers can't: *was the evidence any good?* A run can pass every checkpoint and still have shipped on weak observations.

**What it does:**
1. Reads the run's evidence ledger and checkpoint log
2. Audits evidence *quality*. Did each row observe the artifact, or restate a tool return value?
3. Identifies which checkpoints caught real problems and which were ceremony
4. Extracts action items and harvest candidates
5. Writes `04-projects/harness/retro/YYYY-MM-DD-<slug>.md`

**Output:** A retro doc that feeds CP-0 of the next cycle. Advisory, but strongly expected.

---

### /review-cockpit

**Description:** One living review document per multi-item session: a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards you approve or request changes on directly in the doc.

**Triggers:**
- Any session with **≥2 deliverables you need to review or approve**
- "process X, then plan/draft Y and Z"
- Multi-ticket work, briefs with several drafts

**Purpose:** Multi-file output makes review impossible. Instead of a meeting note here, a ticket there, and two drafts buried in chat, everything lands in one file you can open in a side panel and drive. The doc *is* the interaction surface, not a summary of it.

**What it does:**
1. Creates one doc: cockpit header (Progress / Working folder / Context) + one review card per item
2. Each card carries status, deliverable (linked or inlined for in-place review), a **🗒 Your call** approval slot, and an append-only decision log
3. Keeps the doc live as work progresses, using targeted edits so your inline approvals are never clobbered
4. Distinguishes **draft** items (agent proposes, waits) from **auto** items (agent executes directly); when unsure, leaves it draft
5. On approval, executes the item, marks it ✅, and logs the outcome with its external link

**Output:** One markdown doc that is both the deliverable index and the approval surface.

---

### Craft Skills

The following 7 skills raise output quality on writing and visual work. They encode taste as mechanical rules rather than vibes.

---

### /taste-skill

**Description:** Anti-slop frontend skill for **landing pages, portfolios, and redesigns**. Reads the brief, infers the right design direction, and ships interfaces that do not look templated.

**Triggers:**
- Building or redesigning a landing page, portfolio, marketing site, or editorial page
- "make this look less generic / less templated"
- A brief that names a vibe ("Linear-style", "brutalist", "editorial", "premium consumer") or links a reference

**Purpose:** Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room. This forces a **Design Read** first: page kind, audience, vibe signals, existing brand assets, and quiet constraints (accessibility-first, regulated, trust-first commerce) that override aesthetic preference.

**What it does:**
1. Infers the brief and states a one-line **Design Read** before writing any code
2. Sets explicit dials (variance, motion, density) rather than defaulting
3. Picks a real design system when one applies, instead of hand-rolling
4. Audit-first on redesigns: existing brand assets are starting material, not optional input
5. Runs a strict pre-flight check before shipping

**Boundary:** Landing, portfolio, marketing, editorial. It hands off dashboards, data tables, and multi-step product UI to `/product-ui-taste`. Never run both on the same component.

**References:** `references/pattern-vocabulary.md`, `references/motion-skeletons.md`, `references/design-systems-install.md`, `references/canonical-sources.md`, `references/liquid-glass.md`.

---

### /product-ui-taste

**Description:** Anti-slop skill for **dense product surfaces**: dashboards, data tables, forms, wizards, settings, list/detail, admin consoles, app shells. Budgets the frame first and ships interfaces that survive real data.

**Triggers:**
- Building a dashboard, index table, detail view, settings page, or multi-step flow
- "the table breaks with real data"
- Any admin console or internal tool

**Purpose:** Marketing UI lives on first impression. Product UI lives on the **hundredth** use, under real data, by someone doing a job. The slop failure mode is different: not "templated aesthetic" but **a prototype that dies on contact with real data**. A table that scrolls the page sideways, a button that truncates its own label, one grey "no data" box reused for three different situations.

**What it does:**
1. States a one-line **Product Read** (surface type, user, density, data volume, consequence level, host system)
2. Sets three dials: `DENSITY`, `DATA_COMPLEXITY`, `CONSEQUENCE`
3. Resolves the host design system's **real** API before writing UI, never inventing component props
4. Budgets the frame in pixels top-down before any content
5. Enforces the anti-defaults: rows not card-soup, real empty/error/loading/permission-denied states, correct scroll ownership, sticky headers, frozen columns, z-index tiers
6. Covers the states marketing UI never has: read-only, permission-denied, plan-locked

**Boundary:** The counterpart to `/taste-skill`. Maps to Carbon, Polaris, Atlaskit, Fluent, Primer, Material 3, Radix/shadcn, and Ant.

**References:** `references/block-skeletons.md`, `references/install-commands.md`, `references/canonical-sources.md`.

---

### /no-ai-slop

**Description:** Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting.

**Triggers:**
- "make this less AI-sounding"
- "sharpen this draft"
- "does this read as AI?"
- Final pass before publishing any blog post or social copy

**Purpose:** Remove AI patterns without flattening distinctive writing into generic polished prose. The failure mode it guards against is the *other* direction too: an editor that strips voice along with slop.

**What it does:**
1. **Edit mode (default):** makes the minimum effective edit and returns the draft plus a "What changed" section
2. **Detect mode:** flags slop patterns without rewriting
3. Kills fake-profound kickers, summary-recap endings, hedge stacking, and formatting theater
4. Enforces concreteness, named sources, and active voice

**Attribution:** Vendored from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT). `LICENSE` and `SOURCE.md` ship alongside it.

---

### /editorial-illustrations

**Description:** Generate meaning-carrying editorial data-illustrations in a near-black grayscale + single-accent aesthetic. A **generative guide**, not a template gallery. It teaches the "claim → geometry" method.

**Triggers:**
- "make a chart/diagram/illustration for this"
- "visualize this argument"
- Writing or illustrating a blog post, essay, spec, or slide

**Purpose:** Most generated figures decorate; they don't argue. This teaches the session to derive the *right* geometry from what the text actually claims, then render it as a self-contained, theme-aware, reduced-motion-safe HTML/SVG figure.

**What it does:**
1. Extracts the claim, then asks "where is the point?", the one element that gets the accent
2. Selects geometry from the claim's shape (a rail, a ramp, a bridge, a lane split), not from a chart-type menu
3. Renders self-contained HTML/SVG with a grayscale ramp plus exactly one accent, AA-safe on both grounds
4. Runs a pre-flight checklist: one accent on the point, no clipped mono text, no misaligned SVG, theme toggle honored

**References:** `references/design-system.md`, `references/elements.md`, `references/worked-examples.md`, `assets/gallery.html`.

---

### /data-forms

**Description:** Pick the right way to represent a dataset so a reader gets the finding in three seconds: a catalog of 20+ chart and diagram forms with when-to-use and failure modes, plus the encoding decisions that make any of them readable.

**Triggers:**
- Charting survey results, benchmark data, usage metrics, or research findings
- "the default bar chart is burying the point"
- Building a post, brief, deck, or report with data in it

**Purpose:** A repertoire, not a style. What makes good data illustration work is not the palette. It is form selection and encoding discipline, both of which are portable to any visual language.

**What it does:**
1. Matches the dataset's question to a form from the catalog (with each form's failure modes stated)
2. Applies the encoding rules that carry across all of them: takeaway headline, direct labels, kill the axis, highlight-and-mute, show the caveat
3. Stays style-agnostic, handing off to `dataviz` (or your host design system) for palette and accessibility

**References:** `references/forms.md`.

---

### /museum-art

**Description:** Source authentic, high-res **public-domain** artwork from museum open-access APIs (Met, Cleveland, SMK, Rijksmuseum, NGA, Art Institute of Chicago, Getty, Smithsonian) instead of AI-generated or generic-stock imagery.

**Triggers:**
- Blog hero images, section breaks, mood imagery
- Deck backgrounds, social cards, essay figures, spec cover art
- Any visual that needs aesthetic weight and credibility

**Purpose:** Curated, historically significant art reads as credible and sophisticated; AI-generated imagery reads as slop. Stacks with `/no-ai-slop`. Does **not** replace `/editorial-illustrations`, which owns claim-driven diagrams. Museum art is for photographic, hero, decorative, and mood imagery.

**What it does:**
1. Queries museum open-access APIs (verified keyless recipes per institution)
2. Confirms public-domain status and records the licensing terms
3. Returns high-res source URLs with attribution metadata
4. Fetches fresh each time, so there is no reusable image pool, so visuals don't repeat across posts

**References:** one file per institution under `references/`.

---

### /daily-journal

**Description:** A passive daily work journal the agent keeps **for** you so you never have to write it. Appends short entries after meaningful work; runs a guided reflection on request.

**Triggers:**
- `/daily-journal` or `/daily-journal reflect [today|yesterday|YYYY-MM-DD]`
- "log this to my journal"
- Implicitly, after finishing a meaningful chunk of work in any session. The always-apply trigger lives in `CLAUDE.md` § Daily Journal so it is loaded in every session; this entry is the reference.

**Purpose:** Distinct from `/weekly-checkin`, where you supply the input. Here **the agent is the author** and the log accrues in the background, so the record exists even on days you'd never sit down to write one.

**What it does:**
1. **`log` (default, mostly implicit):** appends one entry after meaningful work: what was done, focus thread, artifacts touched, optional signal
2. Skips trivia: one-line lookups, scratch work, its own writes, anything you asked to keep out
3. **`reflect`:** reads the day's log plus recent days, summarizes the day back to you, asks 2-4 light questions adapted to what the log shows, then writes your answers plus a synthesis into the day's file
4. On request, synthesizes the last 7 files into a week-in-review

**Output location:** `01-daily/journal/YYYY-MM-DD.md`.

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

## Worker Agents

COG includes 10 specialized agents (`.claude/agents/`) that handle data-heavy and verification tasks using Sonnet while the lead session (Opus) handles reasoning and synthesis. Inspired by [garrytan/gstack](https://github.com/garrytan/gstack) specialist sessions and [garrytan/gbrain](https://github.com/garrytan/gbrain) knowledge patterns.

**Workers** handle the gathering and the mutating:

| Agent | What it does | When it's used |
|---|---|---|
| **worker-data-collector** | Structured extraction from GitHub, Slack, Jira, Linear, or files | Team briefs, issue audits, data gathering |
| **worker-researcher** | Web research with source citations and evidence | Auto-research threads, daily brief sourcing |
| **worker-file-ops** | Vault reads/writes, metadata, profile updates | Knowledge consolidation, profile maintenance |
| **worker-executor** | Pre-approved mutations (Jira transitions, Linear updates) | Team brief sync-back, issue management |
| **worker-publisher** | Publishing to Slack, Confluence, Notion, webhooks | Brief publishing, wiki sync |
| **brief-people-updater** | Batch-update people profiles from meetings/briefs | After team briefs, meeting processing |

**Verifiers** are read-only and fresh-context, and they cannot edit files or mutate external state:

| Agent | What it does | Checkpoint |
|---|---|---|
| **task-verifier** | Checks a worker's output against acceptance criteria by observing the artifact, not the worker's summary | CP-3v |
| **integration-verifier** | Cross-task wiring and global acceptance for multi-task specs | CP-4 |
| **fix-agent** | Targeted fixes after `task-verifier` returns `FAIL:fixable`; max 2 attempts | CP-3v retry |
| **harvest-curator** | Shapes session learnings into adoption notes; propose-only, never writes durable knowledge | CP-7 |

**Key rules:**
- Workers write results to `/tmp/{task-slug}.md` and return only a short status + file path. The lead session reads the file for synthesis.
- Verifiers receive **paths only**. Never paste a worker's output into a verifier's prompt. Pasted context induces narrativisation: the verifier classifies the framing instead of independently reading the source.

---

## People CRM

COG tracks the people you work with using progressive, evidence-based profiles stored in `05-knowledge/people/`.

**Profile structure:** Each person has a two-layer file:
1. **Compiled Truth** (top) — current best understanding, updated as evidence changes
2. **Timeline** (bottom) — append-only dated entries with source citations

**Tiered enrichment** — profiles auto-escalate:
- **Tier 3 (Stub):** 1 mention → name, role, one-line context
- **Tier 2 (Moderate):** 3+ mentions → executive snapshot, working style, strengths
- **Tier 1 (Full):** 8+ mentions or direct meeting → complete profile

**Citation format:** Every observation must include:
`[Source: [[path/to/source-note]] | YYYY-MM-DD | confidence: high|medium|low]`

Create profiles manually using the template at `06-templates/people-profile-template.md` or run the `brief-people-updater` agent for batch updates.

---

## Vault Structure

```
COG-second-brain/
├── .claude/agents/        # Worker agent definitions (6)
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
│   ├── people/            # People CRM profiles
│   ├── timeline/          # Thinking evolution
│   └── booklets/          # URL bookmarks by category
└── 06-templates/          # Document templates (incl. people profile)
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

COG tracks its version in `COG-VERSION` (currently 3.5.0). To check for updates:
- Run `/update-cog` in any supported agent
- Or use the shell script: `./cog-update.sh --check`
- Validate packaged agent surfaces with `./scripts/validate-agent-surface.sh`

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
