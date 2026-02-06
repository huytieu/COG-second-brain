# COG Knowledge Consolidation Playbook

## Goal
Transform scattered insights from braindumps, briefs, and check-ins into coherent frameworks and knowledge documents.

## Pre-Flight
1. Read `00-inbox/MY-PROFILE.md` for context and agent_mode
2. Identify last consolidation date (check `05-knowledge/consolidated/` for most recent report)

## Steps

### 1. Scan Vault
Gather all unprocessed content since last consolidation:
- `02-personal/braindumps/`
- `03-professional/braindumps/`
- `04-projects/*/braindumps/`
- `01-daily/briefs/`
- `01-daily/checkins/`

### 2. Pattern Recognition
Apply multi-layer analysis:
- **Frequency patterns**: Topics that appear 3+ times
- **Temporal patterns**: How thinking evolves over time
- **Domain correlations**: Insights that span personal + professional
- **Contradictions**: Where thinking conflicts across notes

### 3. Framework Building
For significant patterns, create or update frameworks:
- Name the pattern/framework
- Define its components
- Provide actionable application guidelines
- Link to source braindumps

### 4. Generate Outputs

**Frameworks** → `05-knowledge/consolidated/[framework-name]-framework.md`
```yaml
type: framework
created: YYYY-MM-DD
sources: [list of source braindumps]
tags: ["#framework", "#knowledge"]
```

**Patterns** → `05-knowledge/patterns/pattern-[name].md`

**Timeline** → `05-knowledge/timeline/[topic]-evolution-YYYY-MM.md`

**Report** → `05-knowledge/consolidated/consolidation-YYYY-MM-DD.md`

### 5. Mark Processed
Add `consolidated: YYYY-MM-DD` to frontmatter of processed braindumps.
