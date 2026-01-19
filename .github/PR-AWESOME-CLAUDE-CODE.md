# Pull Request for awesome-claude-code

## Instructions

1. Fork https://github.com/hesreallyhim/awesome-claude-code
2. Edit `README.md`
3. Find the "Workflows & Knowledge Guides" section (around line 239)
4. Under the "General" subsection, find the alphabetically ordered list
5. Add COG entry after "ClaudoPro Directory" (around line 289)
6. Submit PR

## Entry to Add

Add this text after the ClaudoPro Directory entry:

```markdown
[`COG (Claude + Obsidian + Git)`](https://github.com/huytieu/COG-second-brain) &nbsp; by &nbsp; [Huy Tieu](https://github.com/huytieu)  &nbsp;&nbsp;⚖️&nbsp;&nbsp;MIT
A self-evolving second brain system that combines Claude Code with Obsidian and Git. Features specialized AI subagents for knowledge management (brain-dump-analyst, news-curator), daily intelligence briefings with verification-first approach, and automatic pattern recognition across notes. Privacy-first architecture with plain markdown files.

<details>
<summary>📊 GitHub Stats</summary>

![GitHub Stats for COG-second-brain](https://github-readme-stats-plus-theta.vercel.app/api/pin/?repo=COG-second-brain&username=huytieu&all_stats=true&stats_only=true)

</details>
<br>
```

## PR Title
```
Add COG - Self-Evolving Second Brain Workflow
```

## PR Description
```markdown
## COG (Claude + Obsidian + Git)

Adding a self-evolving second brain workflow that demonstrates advanced subagent usage and knowledge management patterns.

**Repository**: https://github.com/huytieu/COG-second-brain
**Category**: Workflows & Knowledge Guides > General
**License**: MIT

### What Makes This Workflow Notable

1. **Specialized Subagent Architecture**
   - `brain-dump-analyst`: Transforms stream-of-consciousness into structured insights
   - `news-curator`: Verification-first news curation with 7-day freshness requirement
   - Demonstrates separation of orchestration (commands) vs processing (subagents)

2. **Knowledge Management Features**
   - Self-evolving: Pattern recognition across all notes
   - Self-healing: Auto-updates cross-references when files move
   - Knowledge consolidation: Builds frameworks from scattered insights

3. **Privacy-First Architecture**
   - Strict domain separation (personal/professional/projects)
   - Plain markdown files (no database)
   - Multi-device sync via iCloud + Git version control

4. **Verification-First Approach**
   - All news requires sources + dates
   - Multi-source validation to prevent hallucinations
   - Explicit confidence levels for all analysis

### Components Included
- 5 custom slash commands (onboarding, daily-brief, braindump, weekly-checkin, knowledge-consolidation)
- 2 specialized subagents with domain-specific quality gates
- Configuration-as-knowledge (settings stored as editable markdown)
- Complete directory structure for Obsidian vault integration

I've been using this workflow daily for 3 months with excellent results. The subagent architecture might be particularly interesting for the community as an example of advanced Claude Code usage.
```

## Alternative: Via GitHub CLI

If you have `gh` CLI installed:

```bash
# Fork the repo
gh repo fork hesreallyhim/awesome-claude-code --clone=false

# Clone your fork
git clone https://github.com/huytieu/awesome-claude-code.git
cd awesome-claude-code

# Create a new branch
git checkout -b add-cog-second-brain

# Edit README.md (add the entry above at line 289)
# Then commit
git add README.md
git commit -m "Add COG - Self-Evolving Second Brain Workflow"

# Push to your fork
git push origin add-cog-second-brain

# Create PR
gh pr create --title "Add COG - Self-Evolving Second Brain Workflow" \
  --body "$(cat <<'EOF'
## COG (Claude + Obsidian + Git)

Adding a self-evolving second brain workflow that demonstrates advanced subagent usage and knowledge management patterns.

**Repository**: https://github.com/huytieu/COG-second-brain
**Category**: Workflows & Knowledge Guides > General
**License**: MIT

### What Makes This Workflow Notable

1. **Specialized Subagent Architecture**
   - brain-dump-analyst: Transforms stream-of-consciousness into structured insights
   - news-curator: Verification-first news curation with 7-day freshness requirement
   - Demonstrates separation of orchestration (commands) vs processing (subagents)

2. **Knowledge Management Features**
   - Self-evolving: Pattern recognition across all notes
   - Self-healing: Auto-updates cross-references when files move
   - Knowledge consolidation: Builds frameworks from scattered insights

3. **Privacy-First Architecture**
   - Strict domain separation (personal/professional/projects)
   - Plain markdown files (no database)
   - Multi-device sync via iCloud + Git version control

4. **Verification-First Approach**
   - All news requires sources + dates
   - Multi-source validation to prevent hallucinations
   - Explicit confidence levels for all analysis

### Components Included
- 5 custom slash commands (onboarding, daily-brief, braindump, weekly-checkin, knowledge-consolidation)
- 2 specialized subagents with domain-specific quality gates
- Configuration-as-knowledge (settings stored as editable markdown)
- Complete directory structure for Obsidian vault integration

I've been using this workflow daily for 3 months with excellent results. The subagent architecture might be particularly interesting for the community as an example of advanced Claude Code usage.
EOF
)"
```
