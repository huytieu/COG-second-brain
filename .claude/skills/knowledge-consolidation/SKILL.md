---
name: knowledge-consolidation
description: Build frameworks from scattered insights across all braindumps and notes
roles: [all]
integrations: []
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

For each framework that needs updating, use the consolidated-knowledge template in `references/templates.md`.

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Create New Frameworks

For newly identified frameworks, use the new-framework template in `references/templates.md`.

Save to: `05-knowledge/consolidated/[framework-name]-framework.md`

#### Update Pattern Documentation

Document the pattern using the pattern template in `references/templates.md`.

Save to: `05-knowledge/patterns/pattern-[name].md`

#### Create Timeline Entries

Build the timeline entry using the thinking-evolution template in `references/templates.md`.

Save to: `05-knowledge/timeline/[topic]-evolution-YYYY-MM.md`

### 5. Generate Consolidation Report

Create the master consolidation document using the report template in `references/templates.md`.

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

## Loop Engineering

Consolidation is a **loop-until-dry extraction with a completeness critic**, not a single scan. See `.claude/skills/loop-engineering/SKILL.md` for the shared vocabulary.

**The loop:** scan a batch of in-scope documents → extract themes, patterns, and candidate framework principles → run the completeness critic ("any in-scope doc not yet read? any theme recurring across N+ docs that no framework captures yet?") → if the critic surfaces something new, run another extraction pass → stop when 2 passes in a row surface nothing new (dry). In `agent_mode: team`, the first scan fans out as one worker per domain (personal / professional / per-project / briefs); each returns its conclusions only, and a synthesis pass merges them.

**The verifier (deterministic where it can be):**
- **Traceability:** every framework principle links at least one source document. A principle with no `[[source]]` is dropped, not published. This is mechanical and is COG's verification-first rule for consolidation.
- **Coverage:** every in-scope document ends marked `status: "consolidated"` with a `consolidated_in` backlink.
- **Dedup:** before creating a framework, check `05-knowledge/consolidated/` so an existing framework is updated, not duplicated.
- The completeness critic ("did we miss a theme?") is the one judgment-based check; keep it explicit and evidence-linked.

**Termination conditions (layered):**
- **Dry:** K=2 consecutive passes find no new theme or document.
- **Coverage complete:** all in-scope documents marked consolidated.
- **Hard cap:** a max number of extraction passes, so a noisy corpus cannot loop forever.

**Patterns:** loop-until-dry (the spine) + plan-execute-verify (each pass) + orchestrator-workers (team-mode domain scans) + completeness critic.

**In-loop context:** write the consolidation report incrementally and dedup new themes against the running set, not against the conversation. Externalizing to the report file is what keeps a large corpus from overflowing the window.

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
