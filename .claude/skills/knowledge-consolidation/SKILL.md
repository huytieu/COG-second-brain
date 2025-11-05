---
name: knowledge-consolidation
description: Build frameworks from scattered insights across all braindumps and notes
---

# COG Knowledge Consolidation Skill

## Purpose
Transform scattered insights from braindumps, daily briefs, and check-ins into coherent frameworks and "single source of truth" knowledge documents through pattern recognition and systematic synthesis.

## When to Invoke
- User wants to consolidate their insights
- User says "consolidate knowledge", "build frameworks", "synthesize insights"
- Time for periodic knowledge base maintenance (weekly, monthly, quarterly)
- User wants to extract patterns from accumulated braindumps
- Before major decisions that could benefit from framework consultation

## Process Flow

### 1. Data Gathering

**Scan vault for unprocessed or partially processed content:**

- All braindumps since last consolidation:
  - `02-personal/braindumps/`
  - `03-professional/braindumps/`
  - `04-projects/*/braindumps/`
  - `00-inbox/braindump-*.md` (mixed domain)

- Daily briefs and check-ins:
  - `01-daily/briefs/`
  - `01-daily/checkins/`

- Any meeting transcripts or project documents in:
  - `04-projects/*/planning/`
  - `04-projects/*/resources/`

**Determine scope:**
- Ask user: "What time period should I analyze? (last week, last month, last quarter, all time, or custom range?)"
- Identify unprocessed content (check for `status: "captured"` or missing consolidation metadata)

**Gather statistics:**
- Total documents to analyze
- Breakdown by domain and type
- Date range coverage

### 2. Pattern Recognition

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

Update and create knowledge base documents:

#### Update Existing Frameworks

For each framework that needs updating:

```markdown
---
type: "consolidated-knowledge"
domain: "[primary-domain]"
framework: "[framework-name]"
created: "[original-date]"
last_updated: "YYYY-MM-DD"
consolidation_id: "[consolidation-session-id]"
source_documents: [count]
status: "stable|working|emerging"
tags: ["#framework", "#consolidated", "#[topic]"]
---

# [Framework Name]

## Framework Overview
[Clear description of what this framework is and what it helps with]

**Status:** [Stable | Working | Emerging]
**Last Updated:** [Date]
**Source Insights:** [count] documents analyzed

---

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

---

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

---

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

---

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

---

## Related Frameworks

- [[framework-2]] - [How they relate]
- [[framework-3]] - [Connection or overlap]
- [[framework-4]] - [When to use which]

---

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

---

*Consolidated from [X] sources | Confidence: [High/Medium/Low] | Status: [Stable/Working/Emerging]*
```

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Create New Frameworks

For newly identified frameworks:

```markdown
---
type: "consolidated-knowledge"
domain: "[primary-domain]"
framework: "[framework-name]"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
consolidation_id: "[consolidation-session-id]"
source_documents: [count]
status: "emerging"
tags: ["#framework", "#consolidated", "#new", "#[topic]"]
---

# [New Framework Name]

## Framework Discovery

**Identified:** [Date]
**Based On:** [X] insights from [timeframe]
**Domain:** [Primary domain with cross-domain applications]

**Discovery Context:**
[What pattern recognition revealed this framework]

---

## Core Principles

[Same structure as framework updates above]

---

[Continue with Applications, Boundaries, Evolution sections...]
```

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Update Pattern Documentation

```markdown
---
type: "pattern-analysis"
pattern: "[pattern-name]"
created: "YYYY-MM-DD"
domains: ["domain1", "domain2"]
frequency: "[high|medium|low]"
tags: ["#pattern", "#analysis"]
---

# Pattern: [Pattern Name]

## Pattern Description
[Clear description of the recurring pattern]

**Frequency:** Appeared in [X] documents over [timeframe]

**Domains:** [Which domains this pattern appears in]

**Significance:** [Why this pattern matters]

---

## Occurrences

### [Date 1] - [[source-document-1]]
**Context:** [What was happening]

**Manifestation:** [How pattern appeared]

**Outcome:** [What resulted]

### [Date 2] - [[source-document-2]]
[Same structure]

### [Date 3] - [[source-document-3]]
[Same structure]

---

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

---

## Evolution Over Time

[How this pattern has changed or stayed consistent]

---

*Pattern identified through consolidation of [X] sources*
```

Save to: `05-knowledge/patterns/pattern-[name].md`

#### Create Timeline Entries

```markdown
---
type: "timeline-entry"
topic: "[major-theme-or-shift]"
date_range: "YYYY-MM-DD to YYYY-MM-DD"
created: "YYYY-MM-DD"
tags: ["#timeline", "#evolution", "#thinking"]
---

# Thinking Evolution: [Major Theme/Shift]

## Timeline Period
**From:** [Start Date]
**To:** [End Date]
**Duration:** [X weeks/months]

---

## What Changed

**Initial State:**
[How thinking/approach started]

**End State:**
[Where thinking/approach ended up]

**Key Shift:**
[The fundamental change that occurred]

---

## Catalysts & Triggers

### [Date] - [Trigger Event 1]
**Source:** [[link-to-document]]

**What Happened:** [Description]

**Impact:** [How this triggered change]

### [Date] - [Trigger Event 2]
[Same structure]

---

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

---

## Impact of This Evolution

**On Decisions:**
[How this shift affects decision-making]

**On Strategies:**
[How this shift affects strategic approach]

**On Frameworks:**
[Which frameworks were created or updated]

**On Actions:**
[What changed in behavior or practice]

---

## Lessons Learned

**What This Evolution Teaches:**
- [Learning 1]
- [Learning 2]
- [Learning 3]

**Future Implications:**
[What this suggests for future development]

---

*Timeline constructed from [X] source documents spanning [timeframe]*
```

Save to: `05-knowledge/timeline/[topic]-evolution-YYYY-MM.md`

### 5. Generate Consolidation Report

Create master consolidation document:

```markdown
---
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
---

# Knowledge Consolidation - [Date]

## Executive Summary

**Period Analyzed:** [Start date] to [End date]

**Documents Processed:**
- [X] braindumps
- [X] daily briefs
- [X] weekly check-ins
- [X] project documents

**Major Outcomes:**
- **Frameworks Updated:** [count] - [list]
- **New Frameworks Created:** [count] - [list]
- **Patterns Identified:** [count]
- **Timeline Entries:** [count]

**Key Insights Synthesized:**
1. [Major insight 1]
2. [Major insight 2]
3. [Major insight 3]

---

## Processing Statistics

- **Total documents analyzed:** [number]
- **Date range:** [start] to [end]
- **Domains covered:** [list]
- **New patterns identified:** [number]
- **Frameworks updated:** [number]
- **New frameworks created:** [number]
- **Timeline entries added:** [number]
- **Archive actions taken:** [number]

---

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

---

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

---

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

---

## Patterns Identified

### Pattern 1: [Name]
**Frequency:** [High|Medium|Low]

**Domains:** [Which domains]

**Description:** [What the pattern is]

**Implications:** [Why it matters]

**Documentation:** [[05-knowledge/patterns/[filename]]]

### Pattern 2: [Name]
[Same structure]

---

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

---

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

---

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

---

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

---

## Quality Assessment

**Completeness:** [All relevant insights processed?]

**Coherence:** [Frameworks logically consistent?]

**Traceability:** [Clear links to source material?]

**Actionability:** [Frameworks applicable to decisions?]

**Evolution Documented:** [Thinking progression captured?]

---

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

---

*Consolidation completed: [Date] | Processed [X] documents | Created/updated [X] frameworks*
```

Save to: `05-knowledge/consolidated/consolidation-YYYY-MM-DD.md`

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
