---
name: weekly-checkin
description: Cross-domain pattern analysis and strategic reflection for weekly review
---

# COG Weekly Check-in Skill

## Purpose
Comprehensive weekly review and analysis integrating insights across all domains (personal, professional, projects) with pattern recognition and strategic planning.

## When to Invoke
- User wants to do their weekly review
- User says "weekly checkin", "weekly review", "reflect on my week"
- End of week reflection time
- User wants to analyze patterns across the week

## Pre-Flight Check

**Check for user profile (optional but enhances experience):**

1. Look for `00-inbox/MY-PROFILE.md` in the vault
2. If found:
   - Read user's name for personalization
   - Read active projects to review project-specific progress
   - Tailor reflection questions to user's role and projects

## Process Flow

### 1. Gather Context

Scan recent files from the past week:
- Daily briefs in `01-daily/briefs/`
- Braindumps in `02-personal/braindumps/`, `03-professional/braindumps/`, `04-projects/*/braindumps/`
- Previous check-ins in `01-daily/checkins/`

If `MY-PROFILE.md` available:
- Use user's name for personalization
- Reference their active projects
- Tailor questions to their role

### 2. Guided Reflection

Lead user through reflection questions in a warm, conversational tone:

#### Overall Week Assessment
**Ask:**
- "How would you rate this week on a 1-5 scale? Why that rating?"
- "What were your biggest wins this week?"
- "What were your main challenges?"

**Listen for:**
- Overall sentiment and energy
- Key accomplishments they're proud of
- Obstacles they faced
- Emotional tone of the week

#### Domain Reviews

**Personal Domain:**
**Ask:**
- "How did you take care of yourself this week?"
- "Any personal growth or insights?"
- "How were your energy levels and well-being?"

**Professional Domain:**
**Ask:**
- "What did you accomplish at work? Any standout moments?"
- "How did things go with your team or colleagues?"
- "Any professional development or learning?"

**Projects Domain (if applicable):**
For each active project from MY-PROFILE.md:
**Ask:**
- "How did [project name] progress this week?"
- "What moved forward? What's blocking you?"
- "Any new insights or direction changes?"

#### Pattern Recognition

**Ask:**
- "Looking at your braindumps this week, did you notice any recurring themes?"
- "How did your energy levels vary throughout the week?"
- "Any connections between different areas of your life - personal, professional, projects?"
- "What surprised you this week?"

**Help identify:**
- Themes they might not see themselves
- Patterns across domains
- Evolution of thinking
- Cross-domain connections

#### Forward Planning

**Ask:**
- "What are your top 3 priorities for next week?"
- "Anything from this week you want to carry forward?"
- "What do you want to do differently next week?"
- "What success would look like next week?"

**Help with:**
- Clarifying priorities
- Being specific about goals
- Identifying experiments to try
- Setting measurable outcomes

### 3. Generate Weekly Check-in Document

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
braindumps_reviewed: [count]
briefs_reviewed: [count]
---

# Weekly Check-in - Week of [Date]

## Executive Summary

**Week Rating:** [1-5] ⭐ - [User's reasoning in their words]

**In Three Words:** [word1], [word2], [word3]

**Key Highlights:**
- [Win 1 - specific and celebratory]
- [Win 2 - acknowledge effort and outcome]
- [Win 3 if applicable]

**Main Challenges:**
- [Challenge 1 - honest and clear]
- [Challenge 2 - what made it difficult]

---

## Domain Reviews

### 💭 Personal

**Wellness & Self-Care:**
[User's reflection on personal wellness, relationships, health]

**Energy Patterns:**
- [Observations about energy levels throughout the week]
- [What energized them]
- [What drained them]

**Personal Growth:**
- [Insights or realizations]
- [New habits or changes]

**Rating:** [1-5] ⭐

---

### 💼 Professional

**Accomplishments:**
[User's reflection on work accomplishments, projects completed, milestones reached]

**Team & Collaboration:**
[Insights about team dynamics, meetings, relationships]

**Challenges & Learnings:**
[What was difficult and what they learned]

**Professional Development:**
[Skills developed, knowledge gained]

**Rating:** [1-5] ⭐

---

### 🎯 Projects

[For each active project:]

#### [Project Name]

**Progress This Week:**
- [What moved forward - be specific]
- [Milestones achieved]
- [Decisions made]

**Current Status:** [On track | Needs attention | Blocked | Pivoting]

**Blockers:**
- [What's in the way - if any]
- [Dependencies waiting on]

**Insights & Direction:**
[Any strategic insights or direction changes]

**Next Steps:**
- [ ] [Specific next action 1]
- [ ] [Specific next action 2]
- [ ] [Specific next action 3]

**Rating:** [1-5] ⭐

---

## 🔍 Pattern Recognition

### Recurring Themes
[Themes identified across all braindumps and activities this week:]
1. **[Theme 1]:** [Description and significance]
2. **[Theme 2]:** [Description and significance]
3. **[Theme 3]:** [Description and significance]

### Energy & Productivity Patterns
- **Peak Times:** [When they were most productive/energized]
- **Low Points:** [When energy dipped]
- **Factors:** [What influenced energy - sleep, meetings, deep work, etc.]

### Cross-Domain Insights
[Connections between personal, professional, and project domains:]
- [Connection 1 - e.g., "Personal stress affecting project focus"]
- [Connection 2 - e.g., "Professional wins boosting personal confidence"]
- [Connection 3 - e.g., "Project learning applying to work"]

### Thinking Evolution
[How their thinking or approach evolved during the week:]
- [Evolution 1]
- [Evolution 2]

---

## 📅 Forward Planning

### Priorities for Next Week

**Top 3 Must-Do:**
1. [Priority 1 - specific and actionable]
2. [Priority 2 - specific and actionable]
3. [Priority 3 - specific and actionable]

**Why These Matter:**
[Brief explanation of strategic importance]

### Carry Forward Items
- [ ] [Unresolved item from this week - with context]
- [ ] [Ongoing task - with next action]
- [ ] [Follow-up needed - with who/what]

### Experiments & Changes

**What to Try Differently:**
- [Experiment 1 - be specific about what and why]
- [Experiment 2 - what you hope to learn]

**What to Keep Doing:**
- [Practice 1 that's working well]
- [Habit 2 to maintain]

**What to Stop:**
- [Thing 1 that's not serving you]
- [Practice 2 to eliminate]

### Success Criteria for Next Week

**I'll know next week was successful if:**
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Qualitative measure 3]

---

## 📊 Week in Review

**Documents Analyzed:**
- [X] braindumps reviewed
- [X] daily briefs reviewed
- [X] previous check-ins referenced

**Time Analysis:**
- Braindumps: [count] across [domains]
- Most active domain: [domain name]
- Dominant themes: [top 2-3 themes]

**Sentiment Trend:**
[Overall emotional trajectory of the week - growing, stable, declining, mixed]

---

## 💡 Insights & Notes

### Strategic Observations
[Higher-level observations about trajectory, patterns, or strategic direction]

### Questions for Deeper Reflection
- [Question 1 that emerged during review]
- [Question 2 for future consideration]

### Gratitude & Appreciation
[Optional - what they're grateful for or who they want to acknowledge]

---

*Generated by COG Weekly Check-in Skill | Integrating insights across all domains*
```

Save to: `01-daily/checkins/weekly-checkin-YYYY-MM-DD.md`

### 4. Confirm Completion

After creating the check-in:
- Confirm file was created
- Show user: "Weekly check-in saved to [file path]"
- Highlight 1-2 key patterns spotted
- Offer to review patterns across multiple weeks if helpful
- Ask if they want to capture any follow-up thoughts via braindump skill

## Conversational Guidelines

### Do:
- Have a warm, empathetic, conversational tone
- Ask thoughtful follow-up questions based on user's answers
- Help identify patterns they might not see themselves
- Be honest and objective in summarizing their reflections
- Celebrate wins genuinely and specifically
- Acknowledge challenges without sugar-coating or minimizing
- Show curiosity about their experiences
- Reflect back what you're hearing for validation

### Don't:
- Rush through the questions
- Make assumptions about what matters to them
- Judge their answers or week rating
- Over-structure their free-form reflections
- Force positivity if they had a tough week
- Dismiss their challenges or concerns
- Skip the emotional/energy assessment
- Be clinical or robotic in tone

## Pattern Recognition Techniques

### Frequency Analysis
- What themes come up repeatedly across braindumps?
- Which topics get the most attention?
- What's mentioned but not deeply explored?

### Temporal Clustering
- What insights emerged together in time?
- How did thinking evolve from Monday to Friday?
- Were there inflection points during the week?

### Domain Correlation
- What patterns cross personal/professional/project boundaries?
- How do domains influence each other?
- Where is there alignment or tension?

### Contradiction Analysis
- Where does thinking conflict with actions?
- Are there competing priorities?
- What tensions exist between domains?

### Energy Pattern Detection
- When was energy highest/lowest?
- What activities energized vs. drained?
- How did energy affect productivity and insights?

## Integration with Other Skills

### Pattern Analysis
Review multiple weekly check-ins to:
- Spot long-term patterns (monthly, quarterly)
- Track goal progress over time
- Identify seasonal or cyclical patterns
- Use knowledge-consolidation skill to extract frameworks

### Project Tracking
Weekly check-ins provide:
- Historical record of project progress
- Evolution of thinking on projects
- Correlation between project work and other domains
- Context for future project analysis

### Knowledge Building
Check-ins feed into:
- Personal development patterns
- Strategic thinking evolution
- Decision-making frameworks
- Life/work balance insights

## Success Metrics
- User completes meaningful reflection
- Patterns identified and documented
- Clear priorities set for next week
- User feels heard and understood
- File saved with complete information
- Cross-domain insights revealed
- Actionable next steps defined

## Philosophy

The weekly check-in skill embodies COG's integrated intelligence approach:
- Holistic view across all life domains
- Pattern recognition over isolated events
- Strategic reflection driving tactical planning
- Emotional and practical dimensions both honored
- Thinking evolution tracked and celebrated
- Self-awareness as foundation for growth
