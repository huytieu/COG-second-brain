# Brain Dump Command

## Purpose
Quick capture and initial processing of stream-of-consciousness thoughts, ideas, and insights with immediate domain classification and basic structuring.

## Command: `/braindump`

## Process Flow

### 1. Rapid Capture
- Accept any format: voice, text, scattered thoughts
- No judgment or filtering during initial capture
- Preserve original voice and spontaneity
- Capture timestamp and context

### 2. Initial Processing
- Basic cleanup and structure without losing authenticity
- Identify main themes and concepts
- Extract obvious action items or decisions
- Note emotional tone and energy level

### 3. Quick Domain Classification
- **Personal:** Individual growth, relationships, wellness
- **Professional:** Work, leadership, career development
- **Project-Specific:** Related to specific projects or initiatives
- **Mixed/Unclear:** Requires further analysis

### 4. Competitive Intelligence Detection (Optional)
**If user has projects with competitive tracking, automatically extract and update:**
- **Trigger Keywords**: User-defined competitor names, funding rounds, product launches
- **Action**: Extract competitor information to `04-projects/[project-name]/competitive/[competitor-name].md`
- **Update**: Add dated entry to existing competitor file or create new one
- **Cross-reference**: Link back to original braindump source

### 5. Immediate Structuring
- Separate different topics or themes
- Identify questions vs. statements vs. ideas
- Flag urgent items requiring immediate attention
- Note connections to existing knowledge

### 6. Output Generation
- Save to appropriate domain braindump folder
- Tag for later analysis by brain-dump-analysis command
- Create quick summary for immediate reference

## Metadata Template
```yaml
---
type: "braindump"
domain: "[personal|professional|project-specific|mixed]"
project: "[project-name]" # Only if project-specific
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
capture_method: "[voice|text|mixed]"
energy_level: "[high|medium|low]"
emotional_tone: "[excited|frustrated|curious|concerned|neutral]"
themes: ["theme1", "theme2", "theme3"]
urgency: "[immediate|soon|eventual|none]"
analysis_needed: [true|false]
tags: ["#braindump", "#raw-thoughts", "#domain-tag"]
status: "[captured|needs-analysis|processed]"
---
```

## Capture Guidelines

### What to Include
- **Stream of Consciousness:** Raw, unfiltered thoughts
- **Ideas and Insights:** Creative thoughts and realizations
- **Problems and Challenges:** Issues you're wrestling with
- **Questions:** Things you're wondering about
- **Decisions:** Choices you're considering
- **Observations:** Things you've noticed or learned
- **Emotions:** How you're feeling about situations
- **Connections:** Links between different concepts

### What NOT to Filter
- **Incomplete Thoughts:** Half-formed ideas are valuable
- **Contradictions:** Conflicting thoughts show thinking process
- **Repetition:** Recurring themes indicate importance
- **Tangents:** Side thoughts often contain insights
- **Emotions:** Feelings provide important context
- **Questions:** Uncertainty is part of the process

## Domain Classification Quick Guide

### Personal Domain Indicators
- Family, relationships, personal health
- Individual goals and aspirations
- Personal learning and growth
- Life balance and satisfaction
- Personal values and beliefs

### Professional Domain Indicators
- Work projects and responsibilities
- Team dynamics and leadership
- Career development and skills
- Professional relationships
- Industry trends and opportunities

### Project-Specific Indicators
- Specific product or initiative names
- Technical implementation details
- Project timelines and milestones
- Project team members
- Project-specific metrics or goals

### Mixed Domain Indicators
- Cross-cutting themes affecting multiple areas
- Life philosophy and principles
- Time management and productivity
- Learning and skill development
- Strategic thinking and planning

## Processing Levels

### Level 1: Raw Capture (This Command)
- Immediate capture with minimal processing
- Basic domain classification
- Simple structuring and cleanup
- Quick metadata tagging

### Level 2: Analysis Processing (brain-dump-analysis command)
- Deep thematic analysis
- Strategic insight extraction
- Knowledge base integration
- Actionable recommendation generation

### Level 3: Knowledge Integration (consolidation command)
- Pattern recognition across multiple braindumps
- Framework development from insights
- Timeline narrative creation
- Single source of truth updates

## Output Structure

### 1. Original Capture
```markdown
## Raw Thoughts
[Preserve original voice and flow]
```

### 2. Quick Structure
```markdown
## Main Themes
- Theme 1: Brief description
- Theme 2: Brief description
- Theme 3: Brief description

## Action Items
- [ ] Urgent item requiring immediate attention
- [ ] Important item for this week
- [ ] Future consideration

## Questions
- Question 1 requiring research or thought
- Question 2 needing discussion with others
- Question 3 for future exploration

## Connections
- Link to existing project or knowledge
- Relationship to previous braindumps
- Connection to current priorities
```

### 3. Processing Notes
```markdown
## Processing Notes
- Domain: [Classification reasoning]
- Energy: [Energy level during capture]
- Context: [Situational context if relevant]
- Next Steps: [Immediate follow-up needed]
```

## File Naming Convention
- **Personal:** `02-personal/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
- **Professional:** `03-professional/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
- **Project-Specific:** `04-projects/[project]/braindumps/braindump-YYYY-MM-DD-HHMM-<title>.md`
- **Mixed:** `00-inbox/braindump-YYYY-MM-DD-HHMM-<title>.md` (for later classification)

## Quality Guidelines

### Authenticity Preservation
- Maintain original voice and tone
- Preserve emotional context and energy
- Keep incomplete thoughts and questions
- Don't over-structure or sanitize

### Useful Structure
- Separate clearly different topics
- Identify actionable items
- Note time-sensitive elements
- Flag items needing follow-up

### Context Capture
- Note situational context if relevant
- Capture emotional state and energy level
- Record any triggering events or conversations
- Include relevant background information

## Integration with Other Commands

### Immediate Follow-up
- Use `/brain-dump-analysis` for deeper processing
- Use `/daily-checkin` to reflect on themes
- Use `/project-analysis` if project-specific insights emerge

### Scheduled Processing
- Weekly review of accumulated braindumps
- Monthly pattern analysis across braindumps
- Quarterly integration into knowledge consolidation

### Cross-Reference Creation
- Link to related previous braindumps
- Connect to relevant project documents
- Reference related insights and frameworks

## Common Use Cases

### Problem-Solving Sessions
- Capture all aspects of a complex problem
- Record different solution approaches
- Note pros and cons of various options
- Document decision-making process

### Creative Ideation
- Capture creative ideas without judgment
- Record inspiration sources and triggers
- Note connections between different concepts
- Preserve creative energy and enthusiasm

### Strategic Thinking
- Process complex strategic decisions
- Explore different scenarios and implications
- Consider stakeholder perspectives
- Work through strategic trade-offs

### Learning Integration
- Process new information and insights
- Connect learning to existing knowledge
- Identify application opportunities
- Note questions for further exploration

### Emotional Processing
- Work through challenging situations
- Process feedback or difficult conversations
- Explore personal reactions and responses
- Identify patterns in emotional responses

## Success Metrics

### Capture Effectiveness
- Speed of capture (minimize friction)
- Completeness of thought capture
- Preservation of original voice and energy
- Useful structure without over-processing

### Processing Value
- Actionable items identified
- Useful connections made
- Appropriate domain classification
- Effective preparation for deeper analysis

### Integration Success
- Successful handoff to analysis commands
- Useful input for knowledge consolidation
- Effective cross-referencing with existing content
- Valuable contribution to overall system learning
