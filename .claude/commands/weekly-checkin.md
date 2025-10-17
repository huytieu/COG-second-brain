# Weekly Check-in Command

## Purpose
Comprehensive weekly review and analysis integrating insights across all domains (personal, professional, projects) with pattern recognition and strategic planning.

## Command: `/weekly-checkin`

## Pre-Flight Check

**Check for user profile (optional but enhances experience):**

1. Look for `00-inbox/MY-PROFILE.md` in the vault
2. If found:
   - Read user's name for personalization
   - Read active projects to review project-specific progress
   - Tailor reflection questions to user's role and projects

## Process Flow

This command helps you reflect on your week through guided conversation and structured output.

### 1. Gather Context
**Your role (Claude Code):**

- Read `00-inbox/MY-PROFILE.md` if available for personalization
- Scan recent files from the past week:
  - Daily briefs in `01-daily/briefs/`
  - Braindumps in `02-personal/braindumps/`, `03-professional/braindumps/`, `04-projects/*/braindumps/`
  - Check-ins in `01-daily/checkins/`

### 2. Guided Reflection
**Your role (Claude Code):**

Lead user through reflection questions:

**Overall Week Assessment**
- "How would you rate this week on a 1-5 scale? Why?"
- "What were your biggest wins?"
- "What were your main challenges?"

**Domain Reviews**
- **Personal:** "How did you take care of yourself this week?"
- **Professional:** "What did you accomplish at work? Any standout moments?"
- **Projects:** [If they have projects] "How did [project name] progress?"

**Pattern Recognition**
- "Did you notice any recurring themes in your braindumps?"
- "How did your energy levels vary throughout the week?"
- "Any connections between different areas of your life?"

**Forward Planning**
- "What are your top 3 priorities for next week?"
- "Anything from this week you want to carry forward?"
- "What do you want to do differently?"

### 3. Generate Weekly Check-in Document
**Your role (Claude Code):**

Based on the conversation, create a structured check-in document:

```markdown
---
type: "weekly-checkin"
domain: "integrated"
date: "YYYY-MM-DD"
week_of: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
tags: ["#weekly-checkin", "#reflection", "#planning"]
domains_analyzed: ["personal", "professional", "projects"]
rating: [1-5]
---

# Weekly Check-in - Week of [Date]

## Executive Summary
**Week Rating:** [1-5] - [User's reasoning]

**Key Highlights:**
- [Win 1]
- [Win 2]

**Main Challenges:**
- [Challenge 1]
- [Challenge 2]

## Domain Reviews

### Personal
- [User's reflection on personal wellness, relationships, growth]

### Professional
- [User's reflection on work accomplishments, challenges, team dynamics]

### Projects
[If applicable, for each project:]
#### [Project Name]
- **Progress:** [What moved forward]
- **Blockers:** [What's in the way]
- **Next Steps:** [What's coming]

## Pattern Recognition

### Recurring Themes
- [Theme 1 identified]
- [Theme 2 identified]

### Energy Patterns
- [Observations about energy levels, productive times]

### Cross-Domain Insights
- [Connections between personal/professional/projects]

## Forward Planning

### Priorities for Next Week
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### Carry Forward Items
- [ ] [Unresolved item from this week]
- [ ] [Ongoing task]

### What to Change
- [Experiment or adjustment to try next week]

## Success Criteria for Next Week
- [Measurable outcome 1]
- [Measurable outcome 2]
```

Save to: `01-daily/checkins/weekly-checkin-YYYY-MM-DD.md`

### 4. Confirm Completion
**Your role (Claude Code):**
- Confirm file was created
- Show user: "Weekly check-in saved to [file path]"
- Offer to review any patterns spotted across recent weeks

## What to Focus On

**Do:**
- Have a warm, conversational tone
- Ask follow-up questions based on user's answers
- Help identify patterns they might not see themselves
- Be honest and objective in summarizing their reflections
- Celebrate wins genuinely
- Acknowledge challenges without sugar-coating

**Don't:**
- Rush through the questions
- Make assumptions about what matters to them
- Judge their answers or week rating
- Over-structure their free-form reflections

## Integration with Other Commands

### Pattern Analysis
- Review multiple weekly check-ins monthly to spot long-term patterns
- Use `/knowledge-consolidation` to extract frameworks from check-ins

### Project Tracking
- Weekly check-ins provide historical record of project progress
- Useful for `/scout-project-analysis` to understand evolution

## Success Metrics
- User completes meaningful reflection
- Patterns identified and documented
- Clear priorities set for next week
- User feels heard and understood
- File saved with complete information
