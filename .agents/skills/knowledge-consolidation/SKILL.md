---
name: knowledge-consolidation
description: Build frameworks from scattered insights, or run a lightweight vault health audit with freshness scoring and orphan detection
metadata:
  roles: all
  keywords: consolidate knowledge,build frameworks,synthesize insights,extract patterns,knowledge consolidation,create framework,analyze patterns,vault health,vault audit,vault status,stale content,orphan notes
  display-name: COG Knowledge Consolidation
---

# COG Knowledge Consolidation Skill

## Purpose
Transform scattered insights from braindumps, daily briefs, research, bookmarks, and all other vault content into coherent frameworks and "single source of truth" knowledge documents through pattern recognition and systematic synthesis. Optionally run in **audit-only** mode for a lightweight vault health check without full synthesis.

## When to Invoke
- User wants to consolidate their insights
- User says "consolidate knowledge", "build frameworks", "synthesize insights"
- Time for periodic knowledge base maintenance (weekly, monthly, quarterly)
- User wants to extract patterns from accumulated braindumps
- Before major decisions that could benefit from framework consultation
- User asks about vault health, stale content, or what needs attention ("vault audit", "vault health", "vault status", "what needs attention?")

## Invocation Modes

This skill supports two modes. Determine which mode from user intent:

### Full Consolidation (default)
The complete pipeline: scan → pattern recognition → framework synthesis → cleanup. Use when the user says "consolidate", "build frameworks", "synthesize", or doesn't specify a mode.

### Audit Only (lightweight)
A quick vault health report without framework synthesis. Use when the user says "vault health", "vault audit", "vault status", "what needs attention", or explicitly asks for an audit without consolidation.

**Audit-only skips:** Steps 2 (Pattern Recognition), 3 (Framework Development), and 4 (Knowledge Integration). It runs Step 1 (Data Gathering) with expanded statistics, the Freshness & Decay Assessment, and generates a Vault Health Report instead of the full consolidation report.

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — delegate scanning and pattern extraction to parallel sub-agents (e.g., one per domain: personal braindumps, professional braindumps, project-specific content, daily briefs). Each agent identifies themes and patterns, then a synthesis agent combines findings into frameworks.
- If `agent_mode: solo` (default) — handle all scanning, pattern recognition, and framework building directly. No delegation.

## Pre-Flight Check

**Get current timestamp (REQUIRED before generating any files):**

1. Run `date '+%Y-%m-%d %H:%M'` using Bash to get the actual current date and time
2. Store this value and use it for the `created:` frontmatter field
3. NEVER guess or fabricate the time — always use the value returned by the `date` command

## Process Flow

### 1. Data Gathering

**Scan vault for ALL content (not just braindumps):**

- **Braindumps** (all domains):
  - `02-personal/braindumps/`
  - `03-professional/braindumps/`
  - `04-projects/*/braindumps/`
  - `00-inbox/braindump-*.md` (mixed domain)

- **Daily & team intelligence:**
  - `01-daily/briefs/` (daily briefs AND team briefs)
  - `01-daily/checkins/` (weekly check-ins)

- **Strategic research:**
  - `05-knowledge/research/` (auto-research output)

- **URL bookmarks & booklets:**
  - `05-knowledge/booklets/` (all categories)

- **Project artifacts:**
  - `04-projects/*/planning/` (meeting transcripts, planning docs)
  - `04-projects/*/resources/` (project resources)
  - `04-projects/*/PRDs/` (product requirements)
  - `04-projects/*/releases/` (release notes)
  - `04-projects/*/stories/` (user stories)
  - `04-projects/*/audits/` (issue audits)

- **Competitive intelligence:**
  - `04-projects/*/competitive/` (per-project competitive intel)
  - `03-professional/COMPETITIVE-WATCHLIST.md`

- **Existing knowledge base** (for staleness check):
  - `05-knowledge/consolidated/` (frameworks)
  - `05-knowledge/patterns/` (patterns)
  - `05-knowledge/timeline/` (timeline entries)

**Determine scope:**
- Ask user: "What time period should I analyze? (last week, last month, last quarter, all time, or custom range?)"
- If audit-only mode: default to "all time" without asking
- Identify unprocessed content (check for `status: "captured"` or missing consolidation metadata)

**Gather statistics:**
- Total documents by content type (braindumps, briefs, research, bookmarks, PRDs, release notes, competitive intel, etc.)
- Breakdown by domain and project
- Date range coverage
- Unprocessed vs. consolidated counts
- Oldest unprocessed document age

### 1b. Freshness & Decay Assessment

**Run in both modes (full consolidation and audit-only).**

Score each document on freshness using category-weighted decay. Content types that represent decisions and strategic thinking decay slower than transient data.

#### Category Weights

| Category | Weight | Decay Threshold | Examples |
|----------|--------|-----------------|----------|
| Frameworks & patterns | 1.5x | 90 days | `05-knowledge/consolidated/`, `05-knowledge/patterns/` |
| Decisions & PRDs | 1.3x | 60 days | `04-projects/*/PRDs/`, meeting decisions |
| Strategic research | 1.2x | 45 days | `05-knowledge/research/` |
| Braindumps | 1.0x | 30 days | All braindump locations |
| Bookmarks & URLs | 1.0x | 60 days | `05-knowledge/booklets/` |
| Release notes & audits | 0.8x | 90 days | `04-projects/*/releases/`, `04-projects/*/audits/` |
| Daily briefs & news | 0.5x | 14 days | `01-daily/briefs/` |

**Decay threshold** = the age after which content is flagged as potentially stale (needs review, not necessarily outdated). Use the `created:` or `last_updated:` frontmatter date, falling back to file modification time.

#### Connectivity Check

For each document, assess:
- **Inlinks:** How many other vault files reference this document? (search for `[[filename]]` patterns)
- **Outlinks:** How many wiki-links does this document contain?
- **Orphans:** Documents with zero inlinks AND zero outlinks (excluding profile/config files in `00-inbox/`)
- **Dead links:** Wiki-links pointing to files that don't exist

#### Health Scoring (per document)

Score each document 0-100 across four dimensions:
- **Completeness (30%):** Has frontmatter? Has required fields for its type? Non-empty body?
- **Connectivity (30%):** Inlink count + outlink count relative to vault average
- **Metadata quality (20%):** Valid frontmatter fields, consistent tagging, proper date formats
- **Freshness (20%):** Age relative to category decay threshold, weighted by category

**Vault health score** = weighted average of all document scores, reported as a single 0-100 number.

### 2. Pattern Recognition

**(Skip this step in audit-only mode.)**

Apply systematic pattern detection across all content:

#### Frequency Analysis
**What comes up repeatedly?**
- Identify themes mentioned across multiple documents
- Track topic frequency and clustering
- Recognize persistent questions or concerns
- Spot recurring action items or decisions

#### Temporal Clustering
**What insights emerged together?**
- Group related insights by time period
- Identify how thinking evolved over time
- Recognize inflection points where thinking shifted
- Map catalysts that triggered changes

#### Domain Correlation
**What patterns cross domains?**
- Personal insights affecting professional thinking
- Professional learnings applied to projects
- Project experiences informing personal growth
- Strategic themes spanning all domains

#### Contradiction Analysis
**Where does thinking conflict?**
- Identify contradictory thoughts or approaches
- Recognize evolution vs. inconsistency
- Understand resolution or ongoing tension
- Track perspective shifts over time

#### Cross-Cutting Patterns
**Meta-patterns across all dimensions:**
- Decision-making approaches
- Problem-solving strategies
- Learning patterns
- Emotional/energy patterns
- Relationship patterns
- Creative processes

### 3. Framework Development

**(Skip this step in audit-only mode.)**

Synthesize patterns into actionable frameworks:

#### Identify Core Principles
**From scattered insights to fundamental truths:**
- What patterns reveal deeper principles?
- What rules or heuristics emerge?
- What mental models are forming?
- What strategies are proving effective?

#### Test Against Evidence
**Validate frameworks with source material:**
- Do source insights support these principles?
- Are there counter-examples or exceptions?
- How confident can we be in this framework?
- What are the boundary conditions?

#### Define Boundaries
**When does framework apply/not apply?**
- What contexts does this framework serve?
- What are its limitations?
- When should it NOT be used?
- What assumptions does it rely on?

#### Create Applications
**How to use this framework:**
- Specific use cases
- Decision-making applications
- Problem-solving templates
- Practical implementation steps

### 4. Knowledge Integration

**(Skip this step in audit-only mode.)**

Update and create knowledge base documents:

#### Update Existing Frameworks

For each framework that needs updating:

```markdown
type: "consolidated-knowledge"
domain: "[primary-domain]"
framework: "[framework-name]"
created: "[original-date]"
last_updated: "YYYY-MM-DD"
consolidation_id: "[consolidation-session-id]"
source_documents: [count]
status: "stable|working|emerging"
tags: ["#framework", "#consolidated", "#[topic]"]

# [Framework Name]

## Framework Overview
[Clear description of what this framework is and what it helps with]

**Status:** [Stable | Working | Emerging]
**Last Updated:** [Date]
**Source Insights:** [count] documents analyzed


## Core Principles

### Principle 1: [Name]
**Statement:** [Clear, concise principle statement]

**Evidence:**
- [[braindump-YYYY-MM-DD]] - [supporting insight]
- [[daily-brief-YYYY-MM-DD]] - [supporting evidence]
- [[checkin-YYYY-MM-DD]] - [pattern observation]

**Evolution:** [How this principle has developed or been refined]

**Confidence:** [High|Medium|Low] - [reasoning]

### Principle 2: [Name]
[Same structure as Principle 1]

### Principle 3: [Name]
[Same structure as Principle 1]


## Applications & Use Cases

### Use Case 1: [Scenario]
**When to Apply:** [Specific situation]

**How to Apply:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Outcomes:** [What to expect]

**Example:** [Real example from user's experience]

### Use Case 2: [Scenario]
[Same structure as Use Case 1]


## Boundaries & Limitations

**This framework works when:**
- [Condition 1]
- [Condition 2]
- [Condition 3]

**This framework does NOT work when:**
- [Anti-condition 1]
- [Anti-condition 2]
- [Anti-condition 3]

**Common Pitfalls:**
- [Pitfall 1 to avoid]
- [Pitfall 2 to avoid]


## Evolution & History

### [Date Range 1]: [Initial Development]
**What Emerged:** [How this framework first appeared]

**Catalysts:**
- [Event or insight that triggered initial thinking]

**Early Insights:**
- [[link]] - [early thought]
- [[link]] - [formative insight]

### [Date Range 2]: [Refinement Phase]
**What Changed:** [How framework evolved]

**New Evidence:**
- [[link]] - [supporting experience]
- [[link]] - [refining insight]

**Adjustments Made:**
- [Change 1]
- [Change 2]

### Current State: [Date]
**Current Understanding:** [Latest refined version]

**Recent Validation:**
- [[link]] - [recent application]
- [[link]] - [current evidence]


## Related Frameworks

- [[framework-2]] - [How they relate]
- [[framework-3]] - [Connection or overlap]
- [[framework-4]] - [When to use which]


## Future Development

**Questions for Deeper Exploration:**
- [Question 1 to investigate]
- [Question 2 needing more evidence]

**Potential Extensions:**
- [Area 1 for expansion]
- [Area 2 for integration]

**Watch For:**
- [Pattern 1 to monitor]
- [Signal 2 that might invalidate or refine]


*Consolidated from [X] sources | Confidence: [High/Medium/Low] | Status: [Stable/Working/Emerging]*
```

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Create New Frameworks

For newly identified frameworks:

```markdown
type: "consolidated-knowledge"
domain: "[primary-domain]"
framework: "[framework-name]"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
consolidation_id: "[consolidation-session-id]"
source_documents: [count]
status: "emerging"
tags: ["#framework", "#consolidated", "#new", "#[topic]"]

# [New Framework Name]

## Framework Discovery

**Identified:** [Date]
**Based On:** [X] insights from [timeframe]
**Domain:** [Primary domain with cross-domain applications]

**Discovery Context:**
[What pattern recognition revealed this framework]


## Core Principles

[Same structure as framework updates above]


[Continue with Applications, Boundaries, Evolution sections...]
```

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Update Pattern Documentation

```markdown
type: "pattern-analysis"
pattern: "[pattern-name]"
created: "YYYY-MM-DD"
domains: ["domain1", "domain2"]
frequency: "[high|medium|low]"
tags: ["#pattern", "#analysis"]

# Pattern: [Pattern Name]

## Pattern Description
[Clear description of the recurring pattern]

**Frequency:** Appeared in [X] documents over [timeframe]

**Domains:** [Which domains this pattern appears in]

**Significance:** [Why this pattern matters]


## Occurrences

### [Date 1] - [[source-document-1]]
**Context:** [What was happening]

**Manifestation:** [How pattern appeared]

**Outcome:** [What resulted]

### [Date 2] - [[source-document-2]]
[Same structure]

### [Date 3] - [[source-document-3]]
[Same structure]


## Analysis

**What Triggers This Pattern:**
- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

**What Follows This Pattern:**
- [Consequence 1]
- [Consequence 2]

**Cross-Domain Implications:**
[How this pattern affects different areas]

**Potential Actions:**
- [Action to amplify if positive]
- [Action to mitigate if negative]
- [Action to understand better]


## Evolution Over Time

[How this pattern has changed or stayed consistent]


*Pattern identified through consolidation of [X] sources*
```

Save to: `05-knowledge/patterns/pattern-[name].md`

#### Create Timeline Entries

```markdown
type: "timeline-entry"
topic: "[major-theme-or-shift]"
date_range: "YYYY-MM-DD to YYYY-MM-DD"
created: "YYYY-MM-DD"
tags: ["#timeline", "#evolution", "#thinking"]

# Thinking Evolution: [Major Theme/Shift]

## Timeline Period
**From:** [Start Date]
**To:** [End Date]
**Duration:** [X weeks/months]


## What Changed

**Initial State:**
[How thinking/approach started]

**End State:**
[Where thinking/approach ended up]

**Key Shift:**
[The fundamental change that occurred]


## Catalysts & Triggers

### [Date] - [Trigger Event 1]
**Source:** [[link-to-document]]

**What Happened:** [Description]

**Impact:** [How this triggered change]

### [Date] - [Trigger Event 2]
[Same structure]


## Evidence Trail

### Early Thinking: [Date Range]
- [[YYYY-MM-DD]] - [Initial thoughts]
- [[YYYY-MM-DD]] - [Early explorations]

### Intermediate Development: [Date Range]
- [[YYYY-MM-DD]] - [Evolving understanding]
- [[YYYY-MM-DD]] - [Testing and refinement]

### Current Understanding: [Date Range]
- [[YYYY-MM-DD]] - [Mature thinking]
- [[YYYY-MM-DD]] - [Latest application]


## Impact of This Evolution

**On Decisions:**
[How this shift affects decision-making]

**On Strategies:**
[How this shift affects strategic approach]

**On Frameworks:**
[Which frameworks were created or updated]

**On Actions:**
[What changed in behavior or practice]


## Lessons Learned

**What This Evolution Teaches:**
- [Learning 1]
- [Learning 2]
- [Learning 3]

**Future Implications:**
[What this suggests for future development]


*Timeline constructed from [X] source documents spanning [timeframe]*
```

Save to: `05-knowledge/timeline/[topic]-evolution-YYYY-MM.md`

### 5. Generate Consolidation Report

Create master consolidation document:

```markdown
type: "knowledge-consolidation"
domain: "integrated"
date: "YYYY-MM-DD"
consolidation_period: "YYYY-MM-DD to YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
sources_analyzed: [number]
frameworks_updated: ["framework1", "framework2"]
frameworks_created: ["new-framework1"]
patterns_identified: [number]
tags: ["#consolidation", "#knowledge", "#frameworks"]

# Knowledge Consolidation - [Date]

## Executive Summary

**Period Analyzed:** [Start date] to [End date]

**Documents Processed:**
- [X] braindumps
- [X] daily/team briefs
- [X] weekly check-ins
- [X] strategic research
- [X] URL bookmarks
- [X] project documents (PRDs, release notes, stories, audits)
- [X] competitive intelligence
- [X] meeting notes

**Major Outcomes:**
- **Frameworks Updated:** [count] - [list]
- **New Frameworks Created:** [count] - [list]
- **Patterns Identified:** [count]
- **Timeline Entries:** [count]

**Key Insights Synthesized:**
1. [Major insight 1]
2. [Major insight 2]
3. [Major insight 3]


## Processing Statistics

- **Total documents analyzed:** [number]
- **Date range:** [start] to [end]
- **Domains covered:** [list]
- **New patterns identified:** [number]
- **Frameworks updated:** [number]
- **New frameworks created:** [number]
- **Timeline entries added:** [number]
- **Archive actions taken:** [number]


## Major Themes This Period

### Theme 1: [Name]
**Frequency:** Appeared in [X] documents

**Evolution:** [How thinking evolved]

**Key Insights:**
- [[source]] - [insight 1]
- [[source]] - [insight 2]
- [[source]] - [insight 3]

**Framework Implications:**
[How this theme affected or created frameworks]

**Status:** [Stable understanding | Still exploring | Needs more evidence]

### Theme 2: [Name]
[Same structure as Theme 1]


## Frameworks Updated

### Framework 1: [Name]
**Location:** [[05-knowledge/consolidated/[filename]]]

**What Changed:**
- [Addition/modification 1]
- [Addition/modification 2]

**New Evidence Added:**
- [[source]] - [insight]
- [[source]] - [insight]

**Confidence Change:** [Before] → [After]

**New Applications:**
- [Use case 1]
- [Use case 2]

### Framework 2: [Name]
[Same structure]


## New Frameworks Created

### New Framework: [Name]
**Location:** [[05-knowledge/consolidated/[filename]]]

**Created:** Based on [X] insights from [timeframe]

**Core Principles:**
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

**Primary Use Cases:**
- [Use case 1]
- [Use case 2]

**Status:** Emerging (needs more evidence and validation)

**Future Development:**
[What's needed to mature this framework]


## Patterns Identified

### Pattern 1: [Name]
**Frequency:** [High|Medium|Low]

**Domains:** [Which domains]

**Description:** [What the pattern is]

**Implications:** [Why it matters]

**Documentation:** [[05-knowledge/patterns/[filename]]]

### Pattern 2: [Name]
[Same structure]


## Thinking Evolution

### Major Shift: [Topic]
**Timeline:** [Date range]

**What Changed:** [Description]

**Catalysts:**
- [Event 1]
- [Event 2]

**Impact:**
[How this shift affects frameworks, decisions, actions]

**Documentation:** [[05-knowledge/timeline/[filename]]]


## Cross-Cutting Insights

**Connections Across Domains:**
- [Cross-domain insight 1]
- [Cross-domain insight 2]
- [Cross-domain insight 3]

**Contradictions Identified:**
- [Contradiction 1] - [Resolution approach]
- [Contradiction 2] - [Still unresolved]

**Strategic Implications:**
[Higher-level observations about trajectory and direction]


## Knowledge Base Maintenance

### Updates Made
- ✅ Updated framework: [name]
- ✅ Created new framework: [name]
- ✅ Documented pattern: [name]
- ✅ Added timeline entry: [topic]
- ✅ Archived outdated insights: [list]

### Archive Actions
**Braindumps Processed:**
- Updated metadata from `status: "captured"` to `status: "consolidated"`
- Added consolidation references: `consolidated_in: "[[consolidation-YYYY-MM-DD]]"`

**Superseded Content:**
- Archived: [list of old framework versions or outdated insights]
- Location: `00-inbox/archive/`


## Future Consolidation Needs

### Ready for Framework Creation
- [ ] [Area 1] - Sufficient evidence gathered - Target: [date]
- [ ] [Area 2] - Pattern established - Target: [date]

### Needs Deeper Analysis
- [ ] [Area 3] - Contradictions to resolve - Target: [date]
- [ ] [Area 4] - Emerging but not yet clear - Target: [date]

### Monitoring Required
- [ ] [Pattern 1] - Watch for additional occurrences
- [ ] [Theme 2] - Track evolution over next [period]


## Quality Assessment

**Completeness:** [All relevant insights processed?]

**Coherence:** [Frameworks logically consistent?]

**Traceability:** [Clear links to source material?]

**Actionability:** [Frameworks applicable to decisions?]

**Evolution Documented:** [Thinking progression captured?]


## Next Steps

**Immediate Actions:**
- [Action 1 based on consolidation insights]
- [Action 2 to apply new frameworks]

**Future Consolidation:**
- **Next Consolidation:** [Suggested date]
- **Focus Areas:** [What to emphasize next time]

**Framework Applications:**
- [Decision 1 that could benefit from framework]
- [Situation 2 to apply framework to]


*Consolidation completed: [Date] | Processed [X] documents | Created/updated [X] frameworks*
```

Save to: `05-knowledge/consolidated/consolidation-YYYY-MM-DD.md`

### 5b. Generate Vault Health Report (audit-only mode)

**Use this instead of step 5 when running in audit-only mode.**

```markdown
type: "vault-health-audit"
domain: "integrated"
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
vault_health_score: [0-100]
total_documents: [number]
tags: ["#vault-health", "#audit"]

# Vault Health Audit - [Date]

## Overall Health Score: [X]/100

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | [X]/100 | [% of docs with valid frontmatter and non-empty body] |
| Connectivity | [X]/100 | [avg links per doc, orphan ratio] |
| Metadata Quality | [X]/100 | [% with valid types, dates, tags] |
| Freshness | [X]/100 | [% within decay threshold for their category] |


## Content Inventory

| Content Type | Count | Unprocessed | Oldest Unprocessed | Avg Age |
|---|---|---|---|---|
| Braindumps (personal) | [X] | [X] | [date or "—"] | [X days] |
| Braindumps (professional) | [X] | [X] | [date or "—"] | [X days] |
| Braindumps (project) | [X] | [X] | [date or "—"] | [X days] |
| Daily briefs | [X] | — | — | [X days] |
| Team briefs | [X] | — | — | [X days] |
| Weekly check-ins | [X] | — | — | [X days] |
| Strategic research | [X] | [X] | [date or "—"] | [X days] |
| URL bookmarks | [X] | [X] | [date or "—"] | [X days] |
| PRDs | [X] | — | — | [X days] |
| Release notes | [X] | — | — | [X days] |
| User stories | [X] | — | — | [X days] |
| Issue audits | [X] | — | — | [X days] |
| Competitive intel | [X] | — | — | [X days] |
| Meeting notes | [X] | — | — | [X days] |
| Frameworks | [X] | — | — | [X days] |
| Patterns | [X] | — | — | [X days] |
| Timeline entries | [X] | — | — | [X days] |
| **Total** | **[X]** | **[X]** | | |


## Freshness Report

### Stale Content (past decay threshold)
[List documents past their category's decay threshold, sorted by staleness]

| Document | Type | Age | Threshold | Action Needed |
|---|---|---|---|---|
| [[path/to/file]] | [type] | [X days] | [X days] | Review / Update / Archive |

### Frameworks Needing Evidence
[Frameworks with status "emerging" that haven't received new evidence in 30+ days]

| Framework | Status | Last Updated | Days Since Update |
|---|---|---|---|
| [[framework-name]] | [emerging/working] | [date] | [X days] |


## Connectivity Report

### Orphaned Documents (no inlinks, no outlinks)
[Documents with zero connections — candidates for linking or archival]

- [[path/to/orphan-1]] — [type], created [date]
- [[path/to/orphan-2]] — [type], created [date]

### Dead Links
[Wiki-links pointing to files that don't exist]

- `[[broken-reference]]` in [[path/to/source-file]]

### Most Connected (hub documents)
[Top 5 documents by inlink + outlink count — these are your knowledge hubs]

| Document | Inlinks | Outlinks | Total |
|---|---|---|---|
| [[path/to/hub]] | [X] | [X] | [X] |


## Recommended Actions

### Immediate (this session)
- [ ] [Most urgent action — e.g., "Process 5 unprocessed braindumps from January"]
- [ ] [Fix broken links]
- [ ] [Archive stale content]

### Next Consolidation
- [ ] [Areas ready for framework creation]
- [ ] [Frameworks needing evidence refresh]

### Maintenance
- [ ] [Orphans to link or archive]
- [ ] [Metadata gaps to fill]


*Vault health audit completed: [Date] | [X] documents scanned | Score: [X]/100*
```

Save to: `05-knowledge/consolidated/vault-health-YYYY-MM-DD.md`

After generating, present the user with:
- The overall health score and a one-line assessment
- Top 3 most urgent recommended actions
- Offer to run full consolidation if unprocessed backlog is significant

### 6. Cleanup and Archival

**Mark processed braindumps:**
Update frontmatter in processed braindumps:
```yaml
status: "consolidated"
consolidated_in: "[[consolidation-YYYY-MM-DD]]"
consolidated_date: "YYYY-MM-DD"
```

**Archive outdated content:**
Move superseded frameworks or insights to:
`00-inbox/archive/[filename]-archived-YYYY-MM-DD.md`

Add note explaining why archived and what supersedes it.

**Maintain clean knowledge base:**
- Remove redundancy while preserving important context
- Update cross-references
- Fix broken links
- Ensure consistent tagging

### 7. Confirm Completion

After consolidation:
- Show user: "Knowledge consolidation complete! Processed [X] documents"
- Highlight: "[X] frameworks updated, [X] new frameworks created"
- Show: "Consolidation report saved to [file path]"
- Suggest reviewing key frameworks created/updated
- Offer to explain any specific framework in detail

## Consolidation Guidelines

### Quality Over Quantity
- Don't force insights that aren't mature enough
- Let patterns emerge naturally from evidence
- Be patient with incomplete thinking
- Quality frameworks require time and evidence
- Mark frameworks as "emerging" vs "working" vs "stable"

### Preserve Nuance
- Don't over-simplify complex insights
- Maintain important context and conditions
- Note when frameworks have limitations
- Preserve contradictions that haven't resolved yet
- Acknowledge uncertainty explicitly

### Maintain Traceability
- Always link back to source documents
- Show evidence trail for frameworks
- Document evolution of thinking
- Enable future validation or revision
- Make it easy to audit framework claims

### Living Documents
- Frameworks should evolve with new insights
- Regular updates better than perfect first draft
- Clear status indicators (emerging/working/stable)
- Encourage iteration and refinement
- Version history through Git

## Analysis Techniques Reference

### Pattern Detection Methods
1. **Frequency Analysis:** Count mentions, cluster topics
2. **Temporal Clustering:** Group by time, track evolution
3. **Domain Correlation:** Cross-domain connections
4. **Contradiction Analysis:** Identify conflicts, track resolution
5. **Energy Pattern Detection:** Emotional and practical patterns

### Framework Synthesis Process
1. **Identify Core Principles:** Extract fundamental truths
2. **Test Against Evidence:** Validate with sources
3. **Define Boundaries:** Establish applicability
4. **Create Applications:** Develop use cases
5. **Document Evolution:** Track development over time

### Timeline Construction Method
1. **Mark Inflection Points:** When thinking shifted
2. **Identify Catalysts:** What triggered changes
3. **Document Evolution:** How understanding developed
4. **Extract Learnings:** What evolution teaches

## Success Metrics
- Completeness: All relevant insights processed
- Coherence: Frameworks logically consistent
- Traceability: Clear links to source material
- Actionability: Frameworks applicable to decisions
- Evolution: Documented thinking progression
- User Value: Frameworks actually used in practice

## Common Use Cases
- **Weekly Consolidation:** Process week's insights into patterns
- **Monthly Framework Development:** Build strategic frameworks
- **Quarterly Strategic Synthesis:** Big-picture consolidation
- **Annual Knowledge Base Cleanup:** Maintain quality and relevance
- **Pre-Decision Framework Consultation:** Apply frameworks to major decisions
- **Project Retrospective:** Extract learnings for frameworks

## Philosophy

The knowledge consolidation skill embodies COG's self-evolving intelligence:
- Transforms scattered thoughts into strategic frameworks
- Honors the evolution of thinking over time
- Builds "single source of truth" living documents
- Maintains traceability and evidence-based reasoning
- Creates actionable knowledge for better decision-making
- Respects nuance while seeking patterns
- Values iteration and continuous refinement
