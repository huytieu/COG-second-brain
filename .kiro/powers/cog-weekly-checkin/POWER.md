---
name: "cog-weekly-checkin"
displayName: "COG Weekly Check-in"
description: "Cross-domain pattern analysis and strategic reflection for weekly review"
keywords: ["weekly checkin", "weekly check-in", "weekly review", "reflect on my week", "week reflection", "weekly planning", "end of week"]
---

# COG Weekly Check-in Power

Comprehensive weekly review and analysis integrating insights across all domains (personal, professional, projects) with pattern recognition and strategic planning.

## When This Power Activates

- User wants to do their weekly review
- User mentions "weekly checkin", "weekly review", "reflect on my week"
- End of week reflection time

## Pre-Flight Check

1. Check for `00-inbox/MY-PROFILE.md`
2. If found: Use name for personalization, reference active projects

## Process Flow

### 1. Gather Context

Scan recent files from the past week:
- Daily briefs in `01-daily/briefs/`
- Braindumps in `02-personal/`, `03-professional/`, `04-projects/*/braindumps/`
- Previous check-ins in `01-daily/checkins/`

### 2. Guided Reflection

Lead user through reflection with warm, conversational tone:

**Overall Week Assessment:**
- "How would you rate this week on a 1-5 scale? Why?"
- "What were your biggest wins this week?"
- "What were your main challenges?"

**Personal Domain:**
- "How did you take care of yourself this week?"
- "Any personal growth or insights?"
- "How were your energy levels?"

**Professional Domain:**
- "What did you accomplish at work?"
- "How did things go with your team?"
- "Any professional development?"

**Projects Domain (for each active project):**
- "How did [project name] progress this week?"
- "What moved forward? What's blocking you?"

**Pattern Recognition:**
- "Notice any recurring themes in your braindumps?"
- "How did your energy vary throughout the week?"
- "Any connections between different areas of your life?"

**Forward Planning:**
- "What are your top 3 priorities for next week?"
- "What do you want to do differently?"
- "What would success look like next week?"

### 3. Generate Check-in Document

Create structured document with:
- Executive Summary (rating, highlights, challenges)
- Domain Reviews (personal, professional, projects)
- Pattern Recognition (recurring themes, energy patterns, cross-domain insights)
- Forward Planning (priorities, carry forward items, experiments)
- Success Criteria for next week

## Output Location

`01-daily/checkins/weekly-checkin-YYYY-MM-DD.md`

## Conversational Guidelines

### Do:
- Warm, empathetic, conversational tone
- Ask thoughtful follow-up questions
- Help identify patterns they might not see
- Celebrate wins genuinely
- Acknowledge challenges honestly

### Don't:
- Rush through questions
- Make assumptions
- Judge their week rating
- Force positivity if they had a tough week
- Skip emotional/energy assessment

## Pattern Recognition Techniques

- **Frequency Analysis:** What themes come up repeatedly?
- **Temporal Clustering:** How did thinking evolve through the week?
- **Domain Correlation:** What crosses personal/professional/project boundaries?
- **Contradiction Analysis:** Where does thinking conflict with actions?
- **Energy Pattern Detection:** When was energy highest/lowest?

## Task Date Format

Action items use Obsidian Tasks emoji format with calculated due dates:
- **Next steps:** `📅 [next Monday/Friday/+1 week]`
- **Carry forward items:** `📅 [next week dates]`

Example:
```markdown
**Next Steps:**
- [ ] Complete project milestone 📅 2026-02-09
- [ ] Review team feedback 📅 2026-02-10

### Carry Forward Items
- [ ] Follow up with client 📅 2026-02-10
```

## Success Metrics

- User completes meaningful reflection
- Patterns identified and documented
- Clear priorities set for next week
- User feels heard and understood
- Cross-domain insights revealed
