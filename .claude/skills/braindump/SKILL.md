---
name: braindump
description: Quick capture of raw thoughts with intelligent domain classification and competitive intelligence extraction
---

# COG Braindump Skill

## Purpose
Transform raw thoughts into strategic intelligence through quick capture, systematic analysis, pattern recognition, and domain-aware insight extraction with minimal user friction.

## When to Invoke
- User wants to capture stream-of-consciousness thoughts
- User says "braindump", "brain dump", "capture thoughts", or "write down ideas"
- User has ideas they want to quickly record
- User mentions wanting to get thoughts out of their head

## Pre-Flight Check

**Before executing, check for user profile:**

1. Look for `00-inbox/MY-PROFILE.md` in the vault
2. If NOT found:
   ```
   Welcome to COG! It looks like this is your first time.

   Before we start, let's quickly set up your profile (takes 2 minutes).

   Would you like to run onboarding first, or should I proceed with default settings?
   ```
3. If found:
   - Read the profile to get user's name and active projects
   - If user has active projects listed, offer them as domain options
   - Use user's name for friendly communication
   - Read `03-professional/COMPETITIVE-WATCHLIST.md` if it exists for competitive intelligence detection

## Process Flow

### 1. User Interaction & Input Collection
- Greet user warmly (use their name from MY-PROFILE.md if available)
- Ask: "What's on your mind?" or "Ready for a brain dump?"
- Collect their stream-of-consciousness input (can be long, rambling, voice-to-text, etc.)
- Accept any format - no judgment, no filtering

### 2. Domain Classification
Ask user to classify or auto-detect based on content:

**If user profile exists with projects:**
- **Personal:** Individual growth, relationships, wellness
- **Professional:** Work, leadership, career development
- **Project-Specific:** Related to specific projects
  - If MY-PROFILE.md lists projects, offer: "Which project? [list project names]"
  - Example: "Which project? (1) SaaS Product, (2) Book Writing, (3) Health App"
- **Mixed/Unclear:** Spans multiple areas

**If no profile:** Use standard personal/professional/mixed classification

### 3. Content Analysis and Processing

Apply the comprehensive analysis framework directly:

#### Phase 1: Content Ingestion
Analyze the input to understand:
- **Content Type:** [voice-transcript|written-notes|mixed]
- **Length:** [word-count]
- **Energy Level:** [high|medium|low]
- **Emotional Tone:** [excited|frustrated|curious|concerned|neutral|mixed]
- **Context:** [situational-background]

#### Phase 2: Structural Analysis
Extract and identify:
- **Main Themes:** [3-5 primary topics]
- **Supporting Ideas:** [related concepts and details]
- **Questions Raised:** [explicit and implicit questions]
- **Decisions Contemplated:** [choices being considered]
- **Action Items:** [tasks and commitments identified]

#### Phase 3: Domain Classification (with confidence)
Determine:
- **Primary Domain:** [personal|professional|project-specific] with confidence level
- **Secondary Domains:** [if content spans multiple areas]
- **Cross-Domain Elements:** [themes that apply across domains]
- **Privacy Considerations:** [sensitive content requiring protection]

#### Phase 4: Strategic Insight Extraction
Identify:
- **Key Insights:** [3-5 most important realizations]
- **Pattern Recognition:** [connections to previous thoughts/decisions]
- **Strategic Implications:** [what this means for goals and priorities]
- **Decision Framework:** [how this informs future choices]

#### Phase 5: Competitive Intelligence Detection
If COMPETITIVE-WATCHLIST.md exists:
- Scan braindump content for mentions of tracked companies/people
- Extract competitive intelligence to separate files
- Create cross-references back to original braindump

### 4. Generate Structured Output

Create braindump file with this structure:

```markdown
---
type: "braindump"
analyst: "brain-dump-analyst"
domain: "[personal|professional|project-specific|mixed]"
project: "[project-name]" # Only if project-specific
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
themes: ["theme1", "theme2", "theme3"]
tags: ["#braindump", "#raw-thoughts", "#domain-tag"]
status: "captured"
energy_level: "[high|medium|low]"
emotional_tone: "[primary-emotion]"
confidence: "[high|medium|low]"
---

# Braindump: [Auto-generated descriptive title]

## Raw Thoughts
[Original user content preserved exactly as provided]

## Content Analysis

### Main Themes
1. **Theme 1:** [description and significance]
2. **Theme 2:** [description and significance]
3. **Theme 3:** [description and significance]

### Supporting Ideas
- [Supporting concept 1]
- [Supporting concept 2]
- [Supporting concept 3]

### Questions Raised
- [Question 1 for deeper exploration]
- [Question 2 requiring consideration]

### Decisions Contemplated
- [Decision 1 being considered with options]
- [Decision 2 under evaluation]

## Strategic Intelligence

### Key Insights
1. **Insight 1:** [description and implications]
2. **Insight 2:** [description and implications]
3. **Insight 3:** [description and implications]

### Pattern Recognition
- **Connection to Previous Thinking:** [links to earlier braindumps or frameworks]
- **Recurring Patterns:** [themes that keep appearing]
- **Evolution:** [how thinking has developed]

### Strategic Implications
- [How this affects goals]
- [Impact on current projects]
- [Decision-making considerations]

## Action Items

### Immediate (24-48 hours)
- [ ] [specific action with deadline]

### Short-term (1-2 weeks)
- [ ] [specific action with deadline]

### Strategic Considerations
- [longer-term implications and considerations]

## Connections
- **Related Braindumps:** [[link1]], [[link2]]
- **Relevant Projects:** [[project1]], [[project2]]
- **Knowledge Base:** [[insight1]], [[framework1]]

## Domain Classification
- **Primary Domain:** [domain] ([confidence]%)
- **Reasoning:** [why this classification]
- **Cross-Domain Elements:** [if applicable]
- **Privacy Level:** [public|private|confidential]

## Processing Notes
### Emotional Context
- **Energy Level:** [assessment]
- **Emotional Tone:** [assessment]
- **Implications:** [what this suggests]

### Confidence Assessment
- **Overall Analysis:** [percentage] - [reasoning]
- **Domain Classification:** [percentage] - [reasoning]
- **Strategic Insights:** [percentage] - [reasoning]
- **Areas Requiring Clarification:** [specific questions if needed]

---

*Processed by COG Brain Dump Analyst*
```

Save to appropriate location:
- **Personal:** `02-personal/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Professional:** `03-professional/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Project:** `04-projects/[project-slug]/braindumps/braindump-YYYY-MM-DD-HHMM-<slug>.md`
- **Mixed:** `00-inbox/braindump-YYYY-MM-DD-HHMM-<slug>.md`

### 5. Competitive Intelligence Extraction

If competitive intelligence detected (mentions of companies/people from watchlist):

Create/update: `04-projects/[project]/competitive/[company-slug].md`

```markdown
---
type: "competitive-intelligence"
company: "[Company Name]"
project: "[project-name]"
last_updated: "YYYY-MM-DD"
sources: ["braindump"]
tags: ["#competitive", "#intelligence", "#[company-slug]"]
---

# Competitive Intelligence: [Company Name]

## Latest Update - [Date]
**Source:** [[braindump-file-reference]]

[Extracted competitive intelligence from braindump]

## Previous Intelligence
[Historical intel from earlier braindumps]

## Strategic Implications
[Analysis of what this means for the project]

## Action Items
- [ ] [Follow-up actions based on intel]

---

*Auto-extracted by COG Brain Dump Analyst*
```

### 6. Confirm Completion
- Confirm file was created
- Show user: "Braindump saved to [file path]"
- Show quick summary of main themes identified
- If competitive intel extracted, mention: "Also extracted competitive intelligence to [file path]"

## YAML Formatting Requirements

**CRITICAL:** All YAML frontmatter must use proper Obsidian-compatible formatting:
- All string values MUST be quoted with double quotes
- Arrays MUST use quoted strings: `["item1", "item2", "item3"]`
- Boolean values should NOT be quoted: `true` or `false`
- Numbers should NOT be quoted unless they are string identifiers
- Ensure proper YAML syntax to prevent parsing errors in Obsidian

**Examples:**
```yaml
# CORRECT
type: "braindump"
themes: ["automation", "testing", "ui-improvements"]
analysis_needed: true

# INCORRECT
type: braindump
themes: [automation, testing, ui-improvements]
analysis_needed: "true"
```

## Verification Protocols

### Content Accuracy
- **Interpretation Verification:** Confirm understanding matches intent
- **Context Validation:** Ensure situational context is accurately captured
- **Emotional Accuracy:** Verify emotional tone and energy level assessment
- **Completeness Check:** Confirm all major themes are identified

### Domain Classification Verification
- **Boundary Clarity:** Ensure domain classification is clear and defensible
- **Privacy Protection:** Verify personal content is properly protected
- **Cross-Domain Value:** Confirm cross-domain insights are valuable and appropriate
- **Classification Confidence:** State confidence level for domain assignments

### Strategic Insight Validation
- **Evidence-Based:** Ensure insights are supported by content evidence
- **Actionability:** Verify recommendations are specific and implementable
- **Priority Accuracy:** Confirm priority assessments align with stated goals
- **Timeline Realism:** Ensure recommended timelines are achievable

## Uncertainty Handling

### When to Request Clarification
- **Ambiguous Domain Classification:** Content could belong to multiple domains
- **Unclear Strategic Implications:** Insights have multiple possible interpretations
- **Conflicting Information:** Content contains contradictory elements
- **Missing Context:** Important background information seems to be missing

### Confidence Indicators
- **High Confidence (90%+):** Clear content with obvious domain and implications
- **Medium Confidence (70-89%):** Generally clear with some ambiguous elements
- **Low Confidence (50-69%):** Significant ambiguity requiring user input
- **Very Low Confidence (<50%):** Major uncertainty requiring clarification

Always explicitly state confidence levels and reasoning in the processing notes.

## Integration with Other Skills

### Immediate Follow-up
After braindump, suggest:
- Review patterns across multiple braindumps
- Weekly check-in to reflect on themes
- Knowledge consolidation to build frameworks

### Competitive Intelligence
If competitive mentions detected:
- Automatically update competitive files
- Mention this in the output
- Provide link to competitive intelligence file

## Success Metrics
- Speed of capture (minimize user friction)
- Accurate domain classification
- File saved to correct location
- User feels heard and understood
- Competitive intel auto-extracted when relevant
- High confidence in analysis accuracy

## Learning and Adaptation

### Pattern Learning
- Learn user's thinking patterns and communication style
- Understand user's specific domain separation preferences
- Recognize what types of insights user finds most valuable
- Learn which recommendations user typically implements

### Continuous Improvement
- Track accuracy of insights and recommendations over time
- Monitor user engagement with and implementation of recommendations
- Improve speed and accuracy of analysis through learning
- Refine analysis frameworks based on effectiveness
