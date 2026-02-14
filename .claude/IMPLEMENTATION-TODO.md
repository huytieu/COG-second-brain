# COG Second Brain - Implementation TODO

**Created:** 2025-10-31
**Purpose:** Step-by-step implementation guide for skills migration
**Estimated Time:** 4-6 hours for complete implementation

---

## Overview

This document provides detailed, actionable steps to migrate the Light-Personal-Agent skills architecture to COG-second-brain as a generic, reusable system.

**Prerequisites:**
- Light-Personal-Agent skills fully read and analyzed ✅
- Migration plan reviewed and approved
- Decision made on which skills to include

---

## Phase 1: Core Infrastructure Setup

### 1.1 Create Directory Structure

```bash
# Navigate to COG-second-brain
# e.g. cd "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/COG-second-brain"

# Create .claude/skills directory structure
mkdir -p .claude/skills/{obsidian-workspace,domain-classifier,braindump-processor,strategic-analyst}
mkdir -p .claude/skills/{content-analyzer,meeting-processor,news-curator,social-media-publisher}
mkdir -p .claude/skills/templates/{project-intelligence,content-publisher}

# Create vault directory structure
mkdir -p 00-inbox
mkdir -p 01-daily/{briefs,checkins}
mkdir -p 02-personal/{braindumps,goals,knowledge,resources}
mkdir -p 03-professional/{braindumps,knowledge,meetings,resources}
mkdir -p 04-projects/_project-template/{braindumps,competitive,knowledge,meetings}
mkdir -p 05-knowledge
```

**Estimated Time:** 5 minutes

---

### 1.2 Create Skills README

**File:** `.claude/skills/README.md`

**Content Summary:**
- Overview of skills architecture
- How skills activate automatically
- List of available skills
- Integration between skills
- How to customize or add new skills

**Todo:**
- [ ] Copy obsidian-workspace skill structure as reference
- [ ] Write general overview of autonomous skills
- [ ] Document skill activation triggers
- [ ] Explain skill integration patterns
- [ ] Add troubleshooting section

**Estimated Time:** 30 minutes

---

### 1.3 Create Customization Guide

**File:** `.claude/skills/CUSTOMIZATION-GUIDE.md`

**Content Summary:**
- How to modify existing skills
- How to create custom skills
- How to configure interests/projects
- Template usage instructions
- Best practices

**Todo:**
- [ ] Explain YAML frontmatter customization
- [ ] Document skill modification process
- [ ] Provide examples of customization
- [ ] Show how to add project-specific skills
- [ ] Include troubleshooting tips

**Estimated Time:** 45 minutes

---

## Phase 2: Core Skills (Priority 1)

### 2.1 Obsidian Workspace Skill

**File:** `.claude/skills/obsidian-workspace/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/obsidian-workspace/SKILL.md`

**Changes to Make:**
- [ ] Replace "Light-Personal-Agent" with "COG-second-brain" in vault structure
- [ ] Remove Scout AI references in examples
- [ ] Genericize project examples (use placeholders like [project-name])
- [ ] Update file paths to COG structure
- [ ] Keep all YAML standards (those are universal)
- [ ] Keep markdown formatting standards
- [ ] Keep domain classification references

**Specific Replacements:**
```
FIND: Light-Personal-Agent/
REPLACE: COG-second-brain/

FIND: scout-ai
REPLACE: [project-name]

FIND: Scout
REPLACE: [Your Project]

FIND: Katalon, Ghostship, Mabl (any company names)
REPLACE: [Company], [Competitor A], [Competitor B]
```

**Estimated Time:** 20 minutes

---

### 2.2 Domain Classifier Skill

**File:** `.claude/skills/domain-classifier/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/domain-classifier/SKILL.md`

**Changes to Make:**
- [ ] Keep domain framework exactly as-is (universal)
- [ ] Replace Scout AI example with generic project example
- [ ] Remove Katalon, Scout-specific keywords from project detection
- [ ] Update examples to use generic project names
- [ ] Keep all confidence triggers and scoring logic
- [ ] Keep privacy protection rules
- [ ] Keep cross-domain connection strategy

**Specific Replacements:**
```
FIND: Scout AI, Scout
REPLACE: [Project Name]

FIND: AI testing, automated testing product, Ghostship (competitor)
REPLACE: [Your domain], [Your product description], [Competitor]

FIND: scout-ai/
REPLACE: [project-name]/
```

**Estimated Time:** 15 minutes

---

### 2.3 Braindump Processor Skill

**File:** `.claude/skills/braindump-processor/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/braindump-processor/SKILL.md`

**Changes to Make:**
- [ ] Keep processing framework (universal)
- [ ] Remove Scout competitor detection examples
- [ ] Make competitive intelligence detection generic with user-configurable keywords
- [ ] Replace Scout/Katalon references with placeholders
- [ ] Keep theme extraction methodology
- [ ] Keep action item identification
- [ ] Keep emotional context detection
- [ ] Update file path examples

**Specific Section Changes:**

**Competitive Intelligence Detection (lines ~60-75):**
```markdown
# BEFORE (Scout-specific):
**Trigger Keywords**: Ghostship, Mabl, Testers.ai, TestSprite, QA.tech, Scout AI...

# AFTER (Generic):
**Trigger Keywords**: [User configures in project-intelligence skill]
**Action**: Extract competitor information to `04-projects/[project]/competitive/[competitor-name].md`
```

**Examples:**
```
FIND: Scout examples
REPLACE: Generic project examples

FIND: Specific competitor names
REPLACE: [Competitor A], [Competitor B], etc.
```

**Estimated Time:** 25 minutes

---

### 2.4 Strategic Analyst Skill

**File:** `.claude/skills/strategic-analyst/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/strategic-analyst/SKILL.md`

**Changes to Make:**
- [ ] Keep ALL frameworks as-is (SWOT, JTBD, First Principles, ICE, RICE, etc.)
- [ ] Replace Scout AI examples with generic product examples
- [ ] Replace Ghostship competitor with [Competitor A]
- [ ] Genericize all scenarios
- [ ] Keep framework selection logic
- [ ] Keep output standards
- [ ] Keep quality standards

**Specific Examples to Update:**

**Example 1 (lines ~516-521):**
```markdown
# BEFORE:
"We have three features we could build next for Scout: AI test generation..."

# AFTER:
"We have three features we could build next for [Product]: Feature A, Feature B, Feature C..."
```

**Example 2 (lines ~526-531):**
```markdown
# BEFORE:
"Ghostship just raised $10M..."

# AFTER:
"[Competitor A] just raised $XM and launched a feature that competes with our roadmap..."
```

**Estimated Time:** 20 minutes

---

## Phase 3: Content Skills (Priority 2)

### 3.1 Content Analyzer Skill

**File:** `.claude/skills/content-analyzer/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/content-analyzer/SKILL.md`

**Changes to Make:**
- [ ] Keep analysis framework (universal)
- [ ] Remove scout-intelligence integration references
- [ ] Genericize domain examples
- [ ] Replace Scout-specific examples with generic ones
- [ ] Keep quality standards
- [ ] Keep verification protocols
- [ ] Keep knowledge integration logic

**Specific Changes:**
```
FIND: scout-intelligence references
REPLACE: project-intelligence (if skill exists) or remove

FIND: Scout-specific examples
REPLACE: Generic product/project examples

FIND: Technical Article on AI Testing (example)
REPLACE: Technical Article on [Your Domain Topic]
```

**Estimated Time:** 20 minutes

---

### 3.2 Meeting Processor Skill

**File:** `.claude/skills/meeting-processor/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/meeting-processor/SKILL.md`

**Changes to Make:**
- [ ] Keep processing framework entirely (universal)
- [ ] Replace Scout meeting examples with generic ones
- [ ] Remove specific names (Tom, Thanh, Huy, etc.)
- [ ] Genericize project references
- [ ] Keep content filtering rules
- [ ] Keep team dynamics assessment
- [ ] Keep decision extraction logic

**Specific Changes:**
```
FIND: Tom, Thanh, Huy, John, Sarah (any specific names)
REPLACE: [Team Member A], [Team Member B], [Manager], etc.

FIND: Scout positioning discussion
REPLACE: [Product] strategy discussion

FIND: scout-intelligence applies
REPLACE: project-intelligence applies (if user has it)
```

**Estimated Time:** 15 minutes

---

### 3.3 News Curator Skill

**File:** `.claude/skills/news-curator/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/news-curator/SKILL.md`

**Changes to Make:**
- [ ] Keep verification standards (universal)
- [ ] Remove Scout AI-specific interest defaults
- [ ] Make interest areas user-configurable
- [ ] Genericize industry examples
- [ ] Keep source credibility framework
- [ ] Keep strategic relevance analysis
- [ ] Keep error handling for no news found

**Specific Changes:**

**Interest Profiling (lines ~82-110):**
```markdown
# BEFORE (Scout-specific):
### Industry-Specific
- [User's industry] developments  ← Keep this approach
- AI testing, QA platforms, etc.  ← Remove specifics

# AFTER (Generic with examples):
### Industry-Specific (User Configures)
- [Your industry] developments
- Examples: AI/ML, SaaS, Healthcare, Finance, etc.
- Configured via daily-brief command parameters
```

**Example Updates:**
```
FIND: Scout AI focus, Ghostship, Mabl
REPLACE: [Your Product], [Competitor A], [Competitor B]

FIND: AI testing platform news
REPLACE: [Your industry] news
```

**Estimated Time:** 25 minutes

---

## Phase 4: Optional/Social Skills (Priority 3)

### 4.1 Social Media Publisher Skill

**File:** `.claude/skills/social-media-publisher/SKILL.md`

**Source:** Light-Personal-Agent `.claude/skills/social-media-publisher/SKILL.md`

**Changes to Make:**
- [ ] Keep platform formatting rules (universal)
- [ ] Remove Scout-specific examples
- [ ] Genericize audience targeting examples
- [ ] Keep voice and tone guidelines
- [ ] Keep platform-specific structures
- [ ] Update content type examples

**Specific Changes:**

**Audience Keywords (lines ~230-255):**
```markdown
# Keep structure but make examples generic

### Keywords for [Your Audience]
- [Your domain keywords]
- [Your industry terms]
```

**Examples:**
```
FIND: Technical Article on AI Testing
REPLACE: Technical Article on [Your Topic]

FIND: Scout strategy case study
REPLACE: [Product] strategy case study

FIND: QA/Testers specific examples
REPLACE: [Your Target Audience] examples
```

**Estimated Time:** 20 minutes

---

## Phase 5: Template Skills (Priority 4)

### 5.1 Project Intelligence Template

**File:** `.claude/skills/templates/project-intelligence/SKILL-TEMPLATE.md`

**Source:** Light-Personal-Agent `.claude/skills/scout-intelligence/SKILL.md`

**Changes to Make:**
- [ ] Convert entire skill to template format
- [ ] Add [PLACEHOLDER] markers for user to fill in
- [ ] Keep structure and logic
- [ ] Add inline instructions
- [ ] Create sections for user customization

**Template Structure:**
```markdown
---
name: [YOUR-PROJECT]-intelligence
description: [DESCRIBE YOUR PROJECT CONTEXT]
---

# [YOUR PROJECT NAME] Intelligence Skill

## Purpose
[DESCRIBE WHAT THIS SKILL DOES FOR YOUR PROJECT]

## When This Skill Activates
- Mentions of "[YOUR PROJECT NAME]", "[YOUR PRODUCT]"
- [ADD YOUR TRIGGER KEYWORDS]

## Project Context

### Product Overview
**[YOUR PROJECT NAME]** is [DESCRIBE YOUR PROJECT]

**Core Value Proposition:**
- [VALUE PROP 1]
- [VALUE PROP 2]
- [VALUE PROP 3]

**Target Market:**
- [TARGET CUSTOMER 1]
- [TARGET CUSTOMER 2]

### Key Competitive Differentiators
1. **[DIFFERENTIATOR 1]**: [Description]
2. **[DIFFERENTIATOR 2]**: [Description]

## Competitive Landscape

### Primary Competitors

#### [Competitor 1 Name]
**Positioning:** [How they position]
**Strengths:**
- [Strength 1]
- [Strength 2]

**Weaknesses:**
- [Weakness 1]
- [Weakness 2]

**Our Response:**
- [How we respond]

**Monitoring:**
- [What to track]

[REPEAT FOR OTHER COMPETITORS]

## Strategic Framework for [YOUR PROJECT]
[FILL IN YOUR POSITIONING STRATEGY]

## Technical Architecture Context
[FILL IN YOUR TECH STACK AND DECISIONS]

## Product Roadmap Context
[FILL IN FEATURES AND PRIORITIES]

## Automatic Processing Rules

### Trigger Keywords
- [Your project name]
- [Your product features]
- [Your competitor names]
- [Your domain terms]

### Auto-Actions
[KEEP STRUCTURE FROM SCOUT-INTELLIGENCE, BUT USER FILLS IN SPECIFICS]
```

**Estimated Time:** 45 minutes

---

### 5.2 Project Intelligence Instructions

**File:** `.claude/skills/templates/project-intelligence/CUSTOMIZATION-INSTRUCTIONS.md`

**Content:**
```markdown
# How to Customize Project Intelligence Skill

## Step 1: Copy Template
1. Copy `SKILL-TEMPLATE.md` to `.claude/skills/[your-project]-intelligence/SKILL.md`
2. Rename to match your project (e.g., `my-saas-intelligence`)

## Step 2: Fill in Project Details
Search for ALL `[PLACEHOLDER]` markers and replace:
- `[YOUR PROJECT NAME]` → Your actual project name
- `[YOUR PRODUCT]` → Your product description
- `[Competitor 1]` → Your actual competitor names
- `[YOUR TECH STACK]` → Your technologies

## Step 3: Configure Trigger Keywords
Add your specific keywords that should activate this skill:
- Project names
- Product features
- Competitor names
- Domain terminology

## Step 4: Add Competitive Intelligence
Fill in competitor sections:
- Who are they?
- What are their strengths/weaknesses?
- How do you respond?
- What should you monitor?

## Step 5: Test Activation
Try mentioning your project name in a braindump and verify:
- Skill activates automatically
- Content routes to correct domain
- Competitive intelligence extracted properly

## Examples
See `EXAMPLE.md` for a filled-in template example.
```

**Estimated Time:** 15 minutes

---

### 5.3 Project Intelligence Example

**File:** `.claude/skills/templates/project-intelligence/EXAMPLE.md`

**Content:**
Create a fictional example project (e.g., "Acme SaaS Platform") with the template fully filled in to show users what a completed project-intelligence skill looks like.

**Estimated Time:** 30 minutes

---

### 5.4 Content Publisher Template

**File:** `.claude/skills/templates/content-publisher/SKILL-TEMPLATE.md`

**Source:** Light-Personal-Agent `.claude/skills/confluence-publisher/SKILL.md`

**Changes to Make:**
- [ ] Convert to generic template
- [ ] Replace Confluence-specific with [DESTINATION]
- [ ] Add placeholders for authentication
- [ ] Keep markup conversion logic as examples
- [ ] Add instructions for different platforms

**Template Structure:**
```markdown
---
name: content-publisher-[DESTINATION]
description: Publish content to [YOUR PLATFORM]
allowed-tools: [YOUR MCP TOOLS OR APIs]
---

# Content Publisher to [DESTINATION] Skill

## Purpose
Publish content from COG-second-brain to [YOUR DESTINATION]

## Destination Configuration

### Platform
**Platform:** [Confluence | Notion | WordPress | GitHub Pages | etc.]
**Authentication:** [How you authenticate]
**Base URL:** [Your platform URL]

### Publishing Targets
**Primary:** [Where content goes by default]
**Secondary:** [Alternative locations]

## Markup Conversion

### [Source Format] → [Destination Format]
[USER FILLS IN CONVERSION RULES]

Examples:
- Markdown → Confluence: [rules]
- Markdown → Notion: [rules]
- Markdown → HTML: [rules]

## Content Adaptation
[HOW TO ADAPT FOR YOUR AUDIENCE]

## Publishing Workflow
[YOUR SPECIFIC WORKFLOW]

## Error Handling
[PLATFORM-SPECIFIC ERROR HANDLING]
```

**Estimated Time:** 40 minutes

---

### 5.5 Content Publisher Instructions & Example

**Files:**
- `.claude/skills/templates/content-publisher/CUSTOMIZATION-INSTRUCTIONS.md`
- `.claude/skills/templates/content-publisher/EXAMPLE.md`

**Similar approach to project-intelligence above**

**Estimated Time:** 45 minutes (both files)

---

## Phase 6: Documentation (Priority 5)

### 6.1 Main Vault README

**File:** `README.md` (root of COG-second-brain)

**Content:**
```markdown
# COG Second Brain

Your personal AI-powered second brain system with autonomous skills.

## What is This?

COG-second-brain is an Obsidian vault with integrated Claude Code skills that:
- ✅ Automatically processes your thoughts and ideas
- ✅ Classifies content into appropriate domains
- ✅ Applies strategic frameworks to your decisions
- ✅ Curates personalized news briefings
- ✅ Analyzes meetings and extracts insights
- ✅ Builds consolidated knowledge over time

## Quick Start

1. **Capture Thoughts:** Use `/braindump` command
2. **Daily Brief:** Use `/daily-brief` for curated news
3. **Analyze Content:** Share URLs for analysis
4. **Process Meetings:** Share transcripts for insights

## Vault Structure

[DESCRIBE FOLDER STRUCTURE]

## Skills System

See `.claude/skills/README.md` for complete skills documentation.

Available skills:
- `obsidian-workspace` - Vault management
- `domain-classifier` - Content organization
- `braindump-processor` - Thought processing
- `strategic-analyst` - Strategic frameworks
- `content-analyzer` - Article analysis
- `meeting-processor` - Meeting insights
- `news-curator` - Personalized briefings
- `social-media-publisher` - Social content creation

## Customization

See `.claude/skills/CUSTOMIZATION-GUIDE.md` for:
- How to add your projects
- How to configure interests
- How to create custom skills

## Privacy

All processing happens locally. No external services required (except optional publishing).
```

**Estimated Time:** 30 minutes

---

### 6.2 Project Template README

**File:** `04-projects/_project-template/README.md`

**Content:**
```markdown
# Project Template

## How to Use This Template

1. **Copy this folder:** `cp -r _project-template your-project-name`
2. **Rename folders:** Update to match your project
3. **Create project-intelligence skill:** See `.claude/skills/templates/project-intelligence/`
4. **Start capturing:** Use `/braindump` and mention your project

## Folder Structure

- `braindumps/` - Raw project thoughts and ideas
  - `analysis/` - Processed strategic analysis
- `competitive/` - Competitor intelligence files
  - Each competitor gets own file: `competitor-name.md`
- `knowledge/` - Consolidated project knowledge
- `meetings/` - Project-specific meeting notes

## Integration with Skills

When you mention your project name:
- Content automatically routes here
- `project-intelligence` skill activates
- Competitive intelligence extracted
- Strategic analysis applied

## Best Practices

[ADD PROJECT MANAGEMENT BEST PRACTICES]
```

**Estimated Time:** 20 minutes

---

### 6.3 Individual Skill READMEs

**Files:** Each skill folder needs a `README.md`

**Template:**
```markdown
# [Skill Name] Skill

## Overview
[Brief description of what this skill does]

## When It Activates
[Trigger conditions]

## What It Does
[Key capabilities]

## Configuration
[How to customize, if applicable]

## Integration
[Which other skills it works with]

## Examples
[Usage examples]

## Troubleshooting
[Common issues and solutions]
```

**Todo:**
- [ ] Create README for obsidian-workspace
- [ ] Create README for domain-classifier
- [ ] Create README for braindump-processor
- [ ] Create README for strategic-analyst
- [ ] Create README for content-analyzer
- [ ] Create README for meeting-processor
- [ ] Create README for news-curator
- [ ] Create README for social-media-publisher

**Estimated Time:** 10 minutes each (80 minutes total)

---

## Phase 7: Commands Migration

### 7.1 Update Daily Brief Command

**File:** `.claude/commands/daily-brief.md`

**Changes:**
- [ ] Already updated in previous session ✅
- [ ] Verify it references generic interests, not Scout-specific
- [ ] Ensure it works with generic news-curator skill

**Estimated Time:** 5 minutes (verification only)

---

### 7.2 Update Braindump Command

**File:** `.claude/commands/braindump.md`

**Changes:**
- [ ] Already updated in previous session ✅
- [ ] Remove Scout competitor detection from examples
- [ ] Make competitive intelligence detection generic
- [ ] Update file paths to COG structure

**Estimated Time:** 10 minutes

---

### 7.3 Other Commands

**Files to review:**
- `.claude/commands/brain-dump-analysis.md`
- `.claude/commands/link.md` (if exists)
- Any other custom commands

**Changes:**
- [ ] Remove Scout/company-specific references
- [ ] Genericize examples
- [ ] Update file paths

**Estimated Time:** 15 minutes each

---

## Phase 8: Testing & Validation

### 8.1 Skill Activation Testing

**Todo:**
- [ ] Test `/braindump` command - verify braindump-processor activates
- [ ] Test domain classification - verify content routes correctly
- [ ] Test strategic analysis - try SWOT or RICE framework
- [ ] Test `/daily-brief` - verify news curation works
- [ ] Test content analysis - share a URL
- [ ] Test meeting processing - share transcript

**Estimated Time:** 30 minutes

---

### 8.2 Integration Testing

**Todo:**
- [ ] Verify skills work together (e.g., braindump → domain-classifier → obsidian-workspace)
- [ ] Test cross-domain connections
- [ ] Verify metadata consistency
- [ ] Check file organization

**Estimated Time:** 20 minutes

---

### 8.3 Documentation Review

**Todo:**
- [ ] Read through all READMEs
- [ ] Verify examples are clear
- [ ] Test customization instructions
- [ ] Check all links work

**Estimated Time:** 30 minutes

---

## Implementation Checklist

### Phase 1: Core Infrastructure ⏱️ ~2 hours
- [ ] 1.1 Create directory structure (5 min)
- [ ] 1.2 Create skills README (30 min)
- [ ] 1.3 Create customization guide (45 min)
- [ ] 2.1 Obsidian workspace skill (20 min)
- [ ] 2.2 Domain classifier skill (15 min)
- [ ] 2.3 Braindump processor skill (25 min)
- [ ] 2.4 Strategic analyst skill (20 min)

### Phase 2: Content Skills ⏱️ ~1 hour
- [ ] 3.1 Content analyzer skill (20 min)
- [ ] 3.2 Meeting processor skill (15 min)
- [ ] 3.3 News curator skill (25 min)

### Phase 3: Optional Skills ⏱️ ~20 min
- [ ] 4.1 Social media publisher skill (20 min)

### Phase 4: Templates ⏱️ ~2.5 hours
- [ ] 5.1 Project intelligence template (45 min)
- [ ] 5.2 Project intelligence instructions (15 min)
- [ ] 5.3 Project intelligence example (30 min)
- [ ] 5.4 Content publisher template (40 min)
- [ ] 5.5 Content publisher instructions & example (45 min)

### Phase 5: Documentation ⏱️ ~2 hours
- [ ] 6.1 Main vault README (30 min)
- [ ] 6.2 Project template README (20 min)
- [ ] 6.3 Individual skill READMEs (80 min)

### Phase 6: Commands & Testing ⏱️ ~1.5 hours
- [ ] 7.1 Verify daily brief command (5 min)
- [ ] 7.2 Update braindump command (10 min)
- [ ] 7.3 Review other commands (15 min)
- [ ] 8.1 Skill activation testing (30 min)
- [ ] 8.2 Integration testing (20 min)
- [ ] 8.3 Documentation review (30 min)

---

## Total Estimated Time: 9-10 hours

**Breakdown:**
- Core infrastructure: 2 hours
- Content skills: 1 hour
- Optional skills: 20 minutes
- Templates: 2.5 hours
- Documentation: 2 hours
- Testing: 1.5 hours

---

## Quick Reference: Files to Create

### Skills (8 + 2 templates)
1. `.claude/skills/obsidian-workspace/SKILL.md`
2. `.claude/skills/domain-classifier/SKILL.md`
3. `.claude/skills/braindump-processor/SKILL.md`
4. `.claude/skills/strategic-analyst/SKILL.md`
5. `.claude/skills/content-analyzer/SKILL.md`
6. `.claude/skills/meeting-processor/SKILL.md`
7. `.claude/skills/news-curator/SKILL.md`
8. `.claude/skills/social-media-publisher/SKILL.md`
9. `.claude/skills/templates/project-intelligence/SKILL-TEMPLATE.md`
10. `.claude/skills/templates/content-publisher/SKILL-TEMPLATE.md`

### Documentation (12 files)
1. `.claude/skills/README.md`
2. `.claude/skills/CUSTOMIZATION-GUIDE.md`
3. `.claude/skills/templates/project-intelligence/CUSTOMIZATION-INSTRUCTIONS.md`
4. `.claude/skills/templates/project-intelligence/EXAMPLE.md`
5. `.claude/skills/templates/content-publisher/CUSTOMIZATION-INSTRUCTIONS.md`
6. `.claude/skills/templates/content-publisher/EXAMPLE.md`
7. `README.md` (vault root)
8. `04-projects/_project-template/README.md`
9-16. Individual skill `README.md` files (8 total)

### Total: 22 files

---

## Notes

### Automation Opportunities
- Could create a script to do find/replace for common substitutions
- Could use Claude to batch-process multiple skills in one session
- Could create diff files showing exact changes needed

### Flexibility
- Can skip social-media-publisher if not needed
- Can skip template skills if you don't need them
- Can add custom skills later

### Maintenance
- Review skills quarterly and update
- Add new frameworks to strategic-analyst as you discover them
- Update competitive intelligence templates based on usage

---

## When Ready to Execute

**Option 1: Do it yourself**
- Follow this TODO step-by-step
- Use Light-Personal-Agent skills as reference
- Make changes as documented

**Option 2: Ask Claude to help**
- Ask Claude: "Generate Phase 1 skills (obsidian-workspace, domain-classifier, braindump-processor, strategic-analyst)"
- Review output
- Ask for next phase
- Continue until complete

**Option 3: One-shot generation**
- Ask Claude: "Generate all 22 files according to IMPLEMENTATION-TODO.md"
- Review complete system
- Make tweaks as needed

---

## Success Criteria

✅ All skills load without errors
✅ Skills activate on appropriate triggers
✅ Content routes to correct domains
✅ No company/personal information in skills
✅ Documentation is clear and helpful
✅ System works out of the box for new users
✅ Customization is straightforward

---

**Ready when you are!** Use this document to implement COG-second-brain skills system at your own pace.
