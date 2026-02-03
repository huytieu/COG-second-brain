---
name: "cog-braindump"
displayName: "COG Braindump"
description: "Quick capture of raw thoughts with intelligent domain classification and competitive intelligence extraction"
keywords: ["braindump", "brain dump", "capture thoughts", "write down ideas", "thoughts", "get thoughts out", "dump my thoughts", "idea capture"]
---

# COG Braindump Power

Transform raw thoughts into strategic intelligence through quick capture, systematic analysis, pattern recognition, and domain-aware insight extraction with minimal user friction.

## When This Power Activates

- User wants to capture stream-of-consciousness thoughts
- User mentions "braindump", "brain dump", "capture thoughts", or "write down ideas"
- User has ideas they want to quickly record

## Pre-Flight Check

1. Check for `00-inbox/MY-PROFILE.md`
2. If NOT found: Suggest running onboarding first or proceed with defaults
3. If found: Read profile for user's name, active projects, and competitive watchlist

## Process Flow

### 1. Input Collection

- Greet user warmly (use their name if available)
- Ask: "What's on your mind?" or "Ready for a brain dump?"
- Accept any format - long, rambling, voice-to-text, etc.

### 2. Domain Classification

Ask user to classify or auto-detect:
- **Personal:** Individual growth, relationships, wellness
- **Professional:** Work, leadership, career development
- **Project-Specific:** Offer project list from MY-PROFILE.md
- **Mixed/Unclear:** Spans multiple areas

### 3. Content Analysis

Extract and analyze:
- **Main Themes:** 3-5 primary topics
- **Supporting Ideas:** Related concepts
- **Questions Raised:** Explicit and implicit
- **Decisions Contemplated:** Choices being considered
- **Action Items:** Tasks and commitments

### 4. Strategic Insight Extraction

Identify:
- **Key Insights:** 3-5 most important realizations
- **Pattern Recognition:** Connections to previous thoughts
- **Strategic Implications:** Impact on goals and priorities

### 5. Competitive Intelligence Detection

If COMPETITIVE-WATCHLIST.md exists:
- Scan for mentions of tracked companies/people
- Extract to separate competitive intelligence files
- Create cross-references back to braindump

### 6. Generate Output

Create structured braindump file with:
- YAML frontmatter (type, domain, date, themes, tags, status)
- Raw Thoughts section (preserved exactly)
- Content Analysis (themes, questions, decisions)
- Strategic Intelligence (insights, patterns, implications)
- Action Items with Obsidian Tasks emoji dates (📅 YYYY-MM-DD)
- Connections (related braindumps, projects, knowledge)

## Output Locations

- **Personal:** `02-personal/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Professional:** `03-professional/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Project:** `04-projects/[project-slug]/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Mixed:** `00-inbox/braindump-YYYY-MM-DD-HHMM-<slug>.md`

## Confidence Levels

- **High (90%+):** Clear content with obvious domain
- **Medium (70-89%):** Generally clear with some ambiguity
- **Low (50-69%):** Significant ambiguity requiring user input

Always state confidence levels explicitly in processing notes.

## Task Date Format

Action items use Obsidian Tasks emoji format with calculated due dates:
- **Immediate (24-48 hours):** `📅 [tomorrow's date]`
- **Short-term (1-2 weeks):** `📅 [date +1 week]`

Example:
```markdown
### Immediate (24-48 hours)
- [ ] Review competitor announcement 📅 2026-02-04
```

## Follow-up Suggestions

After braindump, suggest:
- Review patterns across multiple braindumps
- Weekly check-in to reflect on themes
- Knowledge consolidation to build frameworks
