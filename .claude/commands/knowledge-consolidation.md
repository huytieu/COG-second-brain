# Knowledge Consolidation Command

## Purpose
Transform scattered insights from braindumps, daily briefs, and check-ins into coherent frameworks and "single source of truth" knowledge documents.

## Command: `/consolidate-knowledge`

## Process Flow

### 1. Data Gathering
- Scan all braindumps since last consolidation
- Review daily briefs and check-ins
- Analyze meeting transcripts and project documents
- Identify unprocessed or partially processed content

### 2. Pattern Recognition
- Identify recurring themes and concepts
- Detect evolution of thinking over time
- Recognize contradictions or shifts in perspective
- Group related insights across documents

### 3. Framework Development
- Synthesize scattered insights into coherent principles
- Build mental models from accumulated learnings
- Create decision-making frameworks
- Develop strategic approaches from patterns

### 4. Knowledge Integration
- Update existing "single source of truth" documents
- Create new consolidated knowledge files as needed
- Cross-reference with existing frameworks
- Maintain timeline of thinking evolution

### 5. Cleanup and Archival
- Mark processed braindumps appropriately
- Archive outdated or superseded insights
- Remove redundancy while preserving important context
- Maintain clean, current knowledge base

### 6. Output Generation
- Save consolidated insights to `05-knowledge/consolidated/`
- Create timeline entries in `05-knowledge/timeline/`
- Update pattern documentation in `05-knowledge/patterns/`

## Metadata Template
```yaml
---
type: knowledge-consolidation
domain: integrated
date: YYYY-MM-DD
consolidation_period: "YYYY-MM-DD to YYYY-MM-DD"
created: YYYY-MM-DD HH:MM
sources_analyzed: [number]
frameworks_updated: [framework1, framework2]
new_insights: [number]
tags: ["#consolidation", "#knowledge", "#frameworks"]
---
```

## Content Structure

### 1. Consolidation Summary
```markdown
## Executive Summary
- Period analyzed: [Start date] to [End date]
- Documents processed: [number] braindumps, [number] briefs, [number] check-ins
- Major themes identified: [list]
- Frameworks updated/created: [list]
- Key insights synthesized: [list]

## Processing Statistics
- Total documents analyzed: [number]
- New patterns identified: [number]
- Frameworks updated: [number]
- New frameworks created: [number]
- Archive actions taken: [number]
```

### 2. Pattern Analysis
```markdown
## Recurring Themes
### Theme 1: [Name]
- **Frequency**: Appeared in [X] documents
- **Evolution**: How thinking evolved over period
- **Key Insights**:
  - Insight 1 with source references
  - Insight 2 with source references
- **Framework Implications**: How this affects existing frameworks

### Theme 2: [Name]
[Same structure as Theme 1]

## Cross-Cutting Patterns
- Pattern 1: Description and significance
- Pattern 2: Description and significance

## Contradictions and Shifts
- What changed: Description of thinking evolution
- Why it changed: Contributing factors and insights
- Resolution: Current understanding or framework
```

### 3. Framework Updates
```markdown
## Updated Frameworks

### Framework 1: [Name]
**Location**: `05-knowledge/consolidated/[filename].md`

**What Changed**:
- Addition/modification 1
- Addition/modification 2

**Supporting Insights**:
- Source insight 1 [link to braindump]
- Source insight 2 [link to braindump]

**New Applications**:
- How to apply this framework
- Specific use cases

### Framework 2: [Name]
[Same structure as Framework 1]

## New Frameworks Created

### New Framework: [Name]
**Created**: Based on [X] insights from [timeframe]

**Core Principles**:
1. Principle 1
2. Principle 2
3. Principle 3

**Supporting Evidence**:
- Evidence 1 [link]
- Evidence 2 [link]

**Application**:
- Use case 1
- Use case 2
```

### 4. Timeline Entry
```markdown
## Thinking Evolution Timeline

### [Date Range]: [Major Theme/Shift]
**What Changed**: Description of evolution

**Catalysts**:
- Event/insight 1 that triggered change
- Event/insight 2 that triggered change

**Evidence Trail**:
- [Date] - Early thinking [link]
- [Date] - Intermediate development [link]
- [Date] - Current understanding [link]

**Impact**:
- How this shift affects decisions
- How this shift affects strategies
- How this shift affects frameworks
```

### 5. Action Items
```markdown
## Knowledge Base Maintenance

### Updates Made
- [X] Updated framework: [name]
- [X] Created new consolidated doc: [name]
- [X] Archived outdated insights: [list]

### Future Consolidation Needs
- [ ] Area 1 needs deeper analysis (target: [date])
- [ ] Area 2 has contradictions to resolve (target: [date])
- [ ] Area 3 ready for framework creation (target: [date])

### Cross-Reference Updates
- [ ] Update document 1 with new insights
- [ ] Link document 2 to consolidated framework
```

## Consolidation Guidelines

### Quality Over Quantity
- Don't force insights that aren't mature enough
- Let patterns emerge naturally from evidence
- Be patient with incomplete thinking
- Quality frameworks require time and evidence

### Preserve Nuance
- Don't over-simplify complex insights
- Maintain important context and conditions
- Note when frameworks have limitations
- Preserve contradictions that haven't resolved

### Maintain Traceability
- Always link back to source documents
- Show evidence trail for frameworks
- Document evolution of thinking
- Enable future validation or revision

### Living Documents
- Frameworks should evolve with new insights
- Regular updates better than perfect first draft
- Mark frameworks as "working" vs "stable"
- Encourage iteration and refinement

## Analysis Techniques

### Pattern Detection
1. **Frequency Analysis**: What comes up repeatedly?
2. **Temporal Clustering**: What insights emerged together?
3. **Domain Correlation**: What patterns cross domains?
4. **Contradiction Analysis**: Where does thinking conflict?

### Framework Synthesis
1. **Identify Core Principles**: What are the fundamental truths?
2. **Test Against Evidence**: Do source insights support principles?
3. **Define Boundaries**: When does framework apply/not apply?
4. **Create Applications**: How to use this framework?

### Timeline Construction
1. **Mark Inflection Points**: When did thinking shift?
2. **Identify Catalysts**: What triggered changes?
3. **Document Evolution**: How did understanding develop?
4. **Extract Learnings**: What does evolution teach us?

## Output Locations

### Consolidated Knowledge
`05-knowledge/consolidated/[domain]-[topic]-YYYY-MM-DD.md`
- Synthesized insights and frameworks
- "Single source of truth" documents
- Living documents that evolve

### Pattern Documentation
`05-knowledge/patterns/pattern-[name]-YYYY-MM-DD.md`
- Recurring patterns across domains
- Cross-domain correlations
- Behavioral and thinking patterns

### Timeline Narratives
`05-knowledge/timeline/[topic]-evolution-YYYY-MM-DD.md`
- Evolution of thinking over time
- Inflection points and catalysts
- Learning from thinking progression

## Success Metrics
- Completeness: All relevant insights processed
- Coherence: Frameworks logically consistent
- Traceability: Clear links to source material
- Actionability: Frameworks applicable to decisions
- Evolution: Documented thinking progression

## Common Use Cases
- Weekly consolidation of daily insights
- Monthly framework development
- Quarterly strategic synthesis
- Annual knowledge base cleanup
- Pre-decision framework consultation
