---
name: meeting-transcript
description: Process meeting recordings and notes into structured decisions, action items, and team dynamics with intelligent noise filtering
---

# COG Meeting Transcript Skill

## When to Invoke
- User shares a meeting transcript or recording notes
- User says "process meeting", "meeting notes", "meeting transcript"
- User has a block of text from a meeting they want structured
- User mentions wanting to extract action items from a meeting

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use the full parallel agent execution strategy below (3 agents)
- If `agent_mode: solo` — process sequentially: extract content first, then analyze dynamics, then enrich with context.

## Purpose
Extract strategic insights from meeting recordings and notes with intelligent content filtering to focus on substantive, actionable content while removing noise and irrelevant information.

## Command: `/meeting-transcript`

## Parallel Agent Team Execution Strategy

**Use parallel agents to process different aspects of the transcript simultaneously.**

### Phase 1: Setup (Orchestrator)
1. Receive transcript content from user
2. Detect content type (meeting vs braindump) and classify domain
3. Split transcript into logical sections for parallel processing

### Phase 2: Parallel Processing (Spawn 2-3 Agents Simultaneously)
**Launch ALL agents in a single message using Task tool with `run_in_background: true`:**

#### Agent 1: "content-extractor" (subagent_type: general-purpose)
```
Extract structured content from the meeting transcript.

1. Filter out side chats, technical difficulties, and irrelevant banter
2. Identify and extract: decisions made (with rationale), action items (with owners/deadlines), strategic themes
3. Capture key quotes and insights from participants
4. Note unresolved issues and follow-up needs

Return: Decisions list, action items list, strategic themes, key quotes, unresolved issues.
```

#### Agent 2: "dynamics-analyst" (subagent_type: general-purpose)
```
Analyze team dynamics and meeting effectiveness.

1. Assess communication patterns and participation levels
2. Identify leadership moments and collaboration quality
3. Evaluate decision-making process effectiveness
4. Assess meeting efficiency (time well spent vs wasted)
5. Note any tensions, disagreements, or alignment issues

Return: Team dynamics assessment, participation analysis, meeting effectiveness score.
```

#### Agent 3: "context-enricher" (subagent_type: general-purpose)
```
Enrich meeting content with project/product context.

1. If project-related: read recent braindumps and notes for context
2. Check if discussed topics relate to known issues/PRs on GitHub
3. Connect decisions to existing strategic priorities
4. Identify competitive intelligence if competitors mentioned

Return: Contextual connections, related documents, strategic alignment notes.
```

### Phase 3: Assembly (Orchestrator)
1. Collect results from all processing agents
2. Assemble structured meeting summary following Content Structure template
3. Add proper metadata (participants, duration, type, action item count)
4. Save to appropriate domain meeting folder
5. Flag urgent action items for immediate attention

## Content Filtering Guidelines

### EXCLUDE (Filter Out)
- **Side Conversations**: "Hey, did you see the game last night?"
- **Technical Difficulties**: "Can you hear me now?" "Your mic is muted"
- **Incomplete Thoughts**: "So I was thinking we should... never mind"
- **Casual Banter**: Weather, personal anecdotes unrelated to work
- **Interruptions**: "Sorry, I have to take this call"
- **Unclear Statements**: Mumbled or inaudible content

### INCLUDE (Keep and Analyze)
- **Strategic Discussions**: Market analysis, competitive positioning
- **Decision Points**: "We've decided to move forward with Option A"
- **Action Items**: "Alex will complete the analysis by Friday"
- **Problem Solving**: Discussion of challenges and proposed solutions
- **Planning**: Timeline discussions, resource allocation
- **Insights**: "The key insight is that customers want..."
- **Concerns**: "My concern is that this approach might..."

## Metadata Template
```yaml
---
type: meeting-transcript
domain: [personal|professional|project-specific]
project: [project-name] # Only for project-specific meetings
date: YYYY-MM-DD
created: YYYY-MM-DD HH:MM
meeting_type: [1-on-1|team-meeting|strategic-planning|project-review|other]
participants: [participant1, participant2, participant3]
duration: [minutes]
content_filtered: true
accuracy_verified: [true|false|pending]
action_items_count: [number]
decisions_count: [number]
tags:
  - meeting
  - transcript
  - domain-tag
  - project-tag
status: [processed|needs-follow-up|action-required]
---
```

## Content Structure

### 1. Meeting Overview
- **Date/Time**: When the meeting occurred
- **Participants**: Who was present and their roles
- **Purpose**: Primary objective of the meeting
- **Duration**: Actual meeting length
- **Type**: Category of meeting

### 2. Key Decisions (Verified Content Only)
- **Decision**: What was decided
- **Rationale**: Why this decision was made
- **Owner**: Who is responsible for implementation
- **Timeline**: When decision takes effect
- **Impact**: Expected outcomes and implications

### 3. Action Items (Substantive Only)
- **Task**: Specific action to be taken
- **Owner**: Person responsible
- **Deadline**: When it's due
- **Dependencies**: What needs to happen first
- **Success Criteria**: How completion will be measured

### 4. Strategic Themes (From Substantial Discussion)
- **Theme**: Major topic or pattern discussed
- **Context**: Why this theme is important
- **Implications**: What this means for the team/project
- **Next Steps**: How to address or leverage this theme

### 5. Unresolved Issues
- **Issue**: Problem or question that remains open
- **Context**: Background and importance
- **Blocking Factors**: What's preventing resolution
- **Proposed Next Steps**: How to move forward

### 6. Team Dynamics Assessment
- **Communication Quality**: How effectively team communicated
- **Decision-Making Process**: How decisions were reached
- **Participation**: Who contributed and how
- **Meeting Efficiency**: Time management and focus
- **Areas for Improvement**: Suggestions for better meetings

## Domain-Specific Processing

### Personal Domain Meetings
- Focus on career development and personal growth
- Maintain strict privacy for personal discussions
- Extract learning and development opportunities
- Save to `[CUSTOMIZE: path/to/personal/]meetings/`

### Professional Domain Meetings
- Analyze leadership and team management aspects
- Extract strategic business insights
- Identify professional development opportunities
- Save to `[CUSTOMIZE: path/to/professional/]meetings/`

### Project-Specific Meetings
- Connect to project metrics and milestones
- Analyze progress against project goals
- Extract competitive and market intelligence
- Save to `[CUSTOMIZE: path/to/projects/][project-name]/meetings/`

## Content Filtering Protocol

### Step 1: Initial Scan
- Identify meeting phases (intro, main discussion, wrap-up)
- Mark obvious side conversations and technical issues
- Flag incomplete or unclear statements

### Step 2: Relevance Assessment
- Evaluate each segment for strategic value
- Determine if content relates to meeting objectives
- Assess completeness and accuracy of information

### Step 3: Accuracy Verification
- Cross-check contradictory statements
- Flag information that seems incorrect
- Note areas requiring clarification

### Step 4: Context Preservation
- Ensure decisions have sufficient context
- Maintain background for action items
- Preserve strategic discussion flow

## Quality Assurance

### Verification Standards
- All decisions must have clear context and rationale
- Action items must have specific owners and deadlines
- Strategic themes must be supported by substantial discussion
- Team dynamics assessment must be based on observable patterns

### Uncertainty Handling
- Flag potentially incorrect information for user confirmation
- State confidence levels for interpretations
- Request clarification for ambiguous content
- Explicitly note when information is incomplete

## Integration with Daily Brief

Meeting notes processed by this command feed directly into the daily brief:
- **Phase 2, Agent 3** (`meeting-reviewer`) scans for recent meeting files
- **Phase 3** cross-references action items against GitHub PRs and Linear issues
- **Section 13** (`Meeting Follow-Up Tracker`) tracks commitment completion

This creates accountability: decisions and action items from meetings are automatically tracked against actual execution in code and project management tools.

## Learning Integration
- Track meeting effectiveness patterns over time
- Identify successful decision-making processes
- Learn team communication preferences
- Adapt filtering based on user feedback on relevance
