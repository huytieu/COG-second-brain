# COG Second Brain - Skills Architecture Migration Plan

**Created:** 2025-10-31
**Source:** Light-Personal-Agent v2.0 Skills Architecture
**Target:** COG-second-brain (Generic, Reusable)

## Executive Summary

This document outlines the migration plan to create a generic, company-agnostic skills architecture for COG-second-brain based on the proven Light-Personal-Agent system, stripping out all personal/company-specific information while preserving the powerful autonomous skill framework.

---

## What's Being Removed/Generalized

### Personal/Company Information
- ❌ Scout AI, Katalon, specific company/product names
- ❌ Ghostship, Mabl, specific competitor names
- ❌ Personal names (Huy, Tom, Thanh, Sarah, Duke, etc.)
- ❌ Specific URLs, account details, API keys
- ❌ Spellar.ai, specific tool references
- ❌ Confluence-specific publishing (made optional/template)
- ❌ Hardcoded project structures
- ❌ Specific industry jargon (AI testing, QA-specific terms unless generic)

### Company-Specific Skills
- ❌ `scout-intelligence` (replaced with generic `project-intelligence` template)
- ❌ `confluence-publisher` (replaced with generic `content-publisher` template)

---

## What's Being Preserved

### Universal Frameworks
- ✅ Domain classification system (personal/professional/project/shared)
- ✅ Strategic analysis frameworks (SWOT, RICE, ICE, JTBD, etc.)
- ✅ Content processing pipelines
- ✅ Metadata standards and YAML structures
- ✅ Braindump processing workflows
- ✅ Meeting analysis patterns
- ✅ News curation methodology

### Core Architecture
- ✅ Skills-based autonomous activation
- ✅ Obsidian workspace integration
- ✅ File organization patterns
- ✅ Quality standards and verification protocols
- ✅ Error handling patterns
- ✅ Integration between skills

---

## Proposed COG-Second-Brain Skill Structure

### Core Skills (Universal - Always Included)

**1. obsidian-workspace**
- Purpose: Handle Obsidian vault operations
- Changes: Generic vault structure, no hardcoded project names
- Status: Adapt with COG-specific paths

**2. domain-classifier**
- Purpose: Classify content into appropriate domains
- Changes: Generic domain descriptions, user-configurable
- Status: Minimal changes needed

**3. braindump-processor**
- Purpose: Process stream-of-consciousness thoughts
- Changes: Remove Scout/company-specific examples
- Status: Generalize competitive intelligence detection

**4. strategic-analyst**
- Purpose: Apply strategic frameworks automatically
- Changes: Generic examples, no company-specific scenarios
- Status: Universal frameworks need no changes

---

### Content Skills (Universal - Always Included)

**5. content-analyzer**
- Purpose: Analyze articles, documents, web content
- Changes: Remove Scout-specific integration examples
- Status: Genericize domain examples

**6. meeting-processor**
- Purpose: Process meeting transcripts into insights
- Changes: Generic meeting examples, no company names
- Status: Universal methodology preserved

**7. news-curator**
- Purpose: Research and curate news with verification
- Changes: User-configurable interest areas
- Status: Remove Scout/testing-specific defaults

---

### Optional/Template Skills (User Configures)

**8. social-media-publisher**
- Purpose: Create platform-specific social posts
- Changes: Generic audience examples
- Status: Useful for many users, include as-is with generic examples

**9. project-intelligence (TEMPLATE)**
- Purpose: User fills in their own project context
- Changes: Template with placeholders for:
  - Project name
  - Competitors
  - Product positioning
  - Technical stack
  - Success metrics
- Status: New template based on scout-intelligence

**10. content-publisher (TEMPLATE)**
- Purpose: User configures their publishing destination
- Changes: Template with placeholders for:
  - Destination (Confluence, Notion, GitHub, etc.)
  - Authentication
  - Formatting rules
  - Audience adaptation
- Status: New template based on confluence-publisher

---

## File Structure for COG-Second-Brain

```
COG-second-brain/
├── .claude/
│   ├── settings.local.json
│   ├── commands/
│   │   ├── braindump.md
│   │   ├── daily-brief.md
│   │   ├── link.md
│   │   └── brain-dump-analysis.md
│   └── skills/
│       ├── README.md                           # Skills overview and guide
│       ├── CUSTOMIZATION-GUIDE.md              # How to customize skills
│       │
│       ├── obsidian-workspace/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── domain-classifier/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── braindump-processor/
│       │   ├── SKILL.md
│       │   ├── KNOWLEDGE-EXTRACTION-GUIDE.md
│       │   └── README.md
│       │
│       ├── strategic-analyst/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── content-analyzer/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── meeting-processor/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── news-curator/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       ├── social-media-publisher/
│       │   ├── SKILL.md
│       │   └── README.md
│       │
│       └── templates/                          # User-customizable templates
│           ├── project-intelligence/
│           │   ├── SKILL-TEMPLATE.md
│           │   ├── CUSTOMIZATION-INSTRUCTIONS.md
│           │   └── EXAMPLE.md
│           │
│           └── content-publisher/
│               ├── SKILL-TEMPLATE.md
│               ├── CUSTOMIZATION-INSTRUCTIONS.md
│               └── EXAMPLE.md
│
├── 00-inbox/                                   # Temporary capture
├── 01-daily/                                   # Daily briefs and check-ins
│   ├── briefs/
│   └── checkins/
├── 02-personal/                                # Personal domain
│   ├── braindumps/
│   ├── goals/
│   ├── knowledge/
│   └── resources/
├── 03-professional/                            # Professional domain
│   ├── braindumps/
│   ├── knowledge/
│   ├── meetings/
│   └── resources/
├── 04-projects/                                # Project-specific
│   └── _project-template/                      # Template for new projects
│       ├── braindumps/
│       ├── competitive/
│       ├── knowledge/
│       ├── meetings/
│       └── README.md
├── 05-knowledge/                               # Consolidated knowledge
└── README.md                                   # Vault introduction
```

---

## Customization Strategy

### For Generic Users

**Out of Box:** Core skills (1-7) work immediately with zero configuration
- Obsidian workspace management
- Domain classification
- Braindump processing
- Strategic analysis
- Content analysis
- Meeting processing
- News curation (user specifies interests via commands)

**Optional:** Skills 8-10 activated if user wants them
- Social media publishing
- Project intelligence (user creates from template)
- Content publishing (user creates from template)

### For Advanced Users

**Project Intelligence Skill**
User copies template and fills in:
```yaml
---
name: [user-project]-intelligence
description: [User's project description]
---

# [User Project] Intelligence Skill

## Project Overview
[User fills in their product/project]

## Competitive Landscape
[User fills in their competitors]

## Strategic Framework
[User fills in positioning]
```

**Content Publisher Skill**
User copies template and configures:
```yaml
---
name: content-publisher-[destination]
description: Publish to [user's platform]
allowed-tools: [user's MCP tools]
---

# Content Publisher Skill

## Destination Configuration
[User specifies: Notion, Confluence, Blog, etc.]

## Authentication
[User configures their auth]
```

---

## Migration Benefits

### For You (Huy)
1. ✅ Portable system you can use across workspaces
2. ✅ No company-specific info leaked
3. ✅ Proven architecture from Light-Personal-Agent
4. ✅ Easy to share with others

### For Generic Users
1. ✅ Production-ready personal agent system
2. ✅ No configuration required for core functionality
3. ✅ Extensible with templates for advanced use
4. ✅ Privacy-first (no external services required)
5. ✅ Learn from your proven system

### For COG System
1. ✅ Second brain that learns and adapts
2. ✅ Autonomous skill activation
3. ✅ Strategic thinking built-in
4. ✅ Knowledge consolidation over time

---

## Deliverables

### Phase 1: Core Infrastructure (Priority 1)
- [ ] `.claude/skills/README.md` - Overview and architecture guide
- [ ] `.claude/skills/CUSTOMIZATION-GUIDE.md` - How to extend skills
- [ ] `obsidian-workspace/SKILL.md` - Generic Obsidian operations
- [ ] `domain-classifier/SKILL.md` - Universal classification
- [ ] `braindump-processor/SKILL.md` - Generic braindump processing

### Phase 2: Strategic & Content Skills (Priority 2)
- [ ] `strategic-analyst/SKILL.md` - Universal frameworks
- [ ] `content-analyzer/SKILL.md` - Generic content analysis
- [ ] `meeting-processor/SKILL.md` - Universal meeting processing
- [ ] `news-curator/SKILL.md` - Configurable news curation

### Phase 3: Optional Skills (Priority 3)
- [ ] `social-media-publisher/SKILL.md` - Generic social posting
- [ ] `templates/project-intelligence/` - Template + instructions + example
- [ ] `templates/content-publisher/` - Template + instructions + example

### Phase 4: Documentation (Priority 4)
- [ ] Main vault `README.md` - Introduction to COG-second-brain
- [ ] `04-projects/_project-template/` - Project folder template
- [ ] Individual skill `README.md` files for each skill
- [ ] YAML frontmatter templates

---

## Implementation Approach

### Option A: Full Migration (Recommended)
Generate all files in one go:
- All 8 core/content skills
- 2 template skills
- Complete documentation
- Ready to use immediately

**Pros:**
- Complete system ready to use
- All skills work together from day 1
- No gaps in functionality

**Cons:**
- Large output (10+ files)
- May need review/tweaking

### Option B: Phased Migration
Generate in phases:
1. Core infrastructure (3 skills + README)
2. Content skills (3 skills)
3. Optional skills (2 skills)
4. Templates and documentation

**Pros:**
- Can review each phase
- Easier to digest
- Can customize as we go

**Cons:**
- System incomplete until done
- May lose context between sessions

### Option C: Cherry-Pick
You tell me which specific skills you want:
- "Just give me braindump-processor and strategic-analyst"
- "I need the whole core set but skip social media"

**Pros:**
- Only get what you need
- Minimal setup

**Cons:**
- May miss skill integration benefits
- Skills expect each other to exist

---

## Recommended Next Steps

### Immediate (This Session)
1. **Review this plan** - Confirm approach aligns with your vision
2. **Choose implementation option** - Full, Phased, or Cherry-Pick
3. **Customize interests** - What domains/projects for news-curator?
4. **Begin generation** - Start creating skill files

### After Generation
1. **Test core skills** - Try `/braindump` command
2. **Verify skill activation** - Check Claude recognizes skills
3. **Customize optional skills** - Fill in project-intelligence template if needed
4. **Document your setup** - Add your specific interests/projects

### Long-Term
1. **Iterate based on usage** - Refine skills as you use them
2. **Add custom skills** - Create domain-specific skills
3. **Share with community** - Help others build personal agents

---

## Questions for You

Before I generate the files, please confirm:

1. **Implementation approach:** Full Migration, Phased, or Cherry-Pick?

2. **Social media skill:** Include or skip? (Useful even if you don't use all platforms)

3. **News interests:** What topics should news-curator monitor by default?
   - Technology trends?
   - Business strategy?
   - Specific industries?
   - (Can be configured later via commands)

4. **Vault structure:** Accept proposed structure or want changes?

5. **Custom projects:** Do you have specific projects to add to 04-projects/ now?

---

## Additional Notes

### Backward Compatibility
- This COG structure is similar enough to Light-Personal-Agent that you could migrate content
- File paths and metadata standards are preserved
- Skills would work if you copied files from Light-Personal-Agent

### Forward Compatibility
- Based on official Claude skills architecture (docs.claude.com)
- Will work with future Claude Code versions
- Portable to other Claude environments

### Privacy & Security
- All personal/company info removed
- No external services required (except optional publishing)
- Full local control
- Privacy-first domain classification

---

**Ready to proceed?** Let me know your preferred approach and I'll generate the complete skill system for COG-second-brain.
