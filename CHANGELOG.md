# Changelog

All notable changes to COG (Claude + Obsidian + Git) will be documented in this file.

## [2.0.0] - 2025-10-17

### Major Architecture Overhaul

This release represents a complete restructuring of COG to follow proven subagent architecture patterns, emphasizing separation of concerns and configuration-as-knowledge principles.

### Added

#### Onboarding System
- **New `/onboarding` command** - First-run setup that personalizes COG in ~2 minutes
  - Asks 6 essential questions: name, role, interests, news sources, projects, competitive watchlist
  - Creates readable markdown profile files in vault
  - No JSON configuration files - everything is human-readable markdown

#### Configuration as Knowledge
- **`00-inbox/MY-PROFILE.md`** - User's basic info, role, and active projects
- **`00-inbox/MY-INTERESTS.md`** - Topics of interest and preferred news sources
- **`03-professional/COMPETITIVE-WATCHLIST.md`** - Companies/people to track
- **`04-projects/[project]/PROJECT-OVERVIEW.md`** - Per-project overview documents
- **`00-inbox/WELCOME-TO-COG.md`** - Personalized welcome guide (auto-generated)

All configuration is now part of the knowledge base - searchable, linkable, and editable like any other note.

#### Subagent Architecture
- **`.claude/subagents/brain-dump-analyst.md`** - Specialized subagent for braindump analysis
  - Stream-of-consciousness processing
  - Domain classification
  - Theme extraction
  - Competitive intelligence detection
  - Structured output generation

- **`.claude/subagents/news-curator.md`** - Specialized subagent for news curation
  - Verified news research (7-day freshness requirement)
  - Multi-source cross-referencing
  - Strategic relevance analysis
  - Personalized briefing generation

### Changed

#### Command Architecture
Commands are now **thin orchestration layers** that delegate to specialized subagents:

**`/braindump` - Redesigned**
- Collects user's stream-of-consciousness input
- Asks for domain classification
- **Delegates ALL processing to brain-dump-analyst subagent**
- Confirms completion and shows summary
- No longer handles analysis directly

**`/daily-brief` - Redesigned**
- Reads user profile files (MY-PROFILE.md, MY-INTERESTS.md)
- **Delegates ALL news curation to news-curator subagent**
- Confirms completion and shows executive summary
- No longer searches or curates news directly

**`/weekly-checkin` - Simplified**
- Guided conversational reflection
- Direct document generation based on user responses
- Pattern identification through conversation
- No template dependency

#### Configuration Philosophy
- **Before**: Hidden JSON config files (`.claude/config/user-config.json`)
- **After**: Markdown notes in vault that are part of knowledge base
- Benefits:
  - Human-readable and directly editable
  - Searchable in Obsidian
  - Linkable from other notes
  - Version controlled with Git
  - Can include personal notes and context

### Removed

- **Deleted `templates/` directory entirely**
  - `templates/braindump-template.md`
  - `templates/daily-brief-template.md`
  - `templates/weekly-checkin-template.md`

- **Removed JSON configuration system**
  - `.claude/config/` directory and all JSON files

- **Eliminated template dependencies**
  - All content now dynamically generated based on context
  - Templates were static; dynamic generation is more flexible

### Architecture Benefits

#### Separation of Concerns
- **Commands**: Simple orchestrators that handle user interaction and delegation
- **Subagents**: Complex processors with detailed analysis frameworks and verification protocols
- Clear responsibility boundaries make system easier to understand and extend

#### Maintainability
- Commands are now < 200 lines (vs 250+ before)
- Complex logic isolated in specialized subagents
- Changes to analysis logic don't affect command structure
- Easy to add new subagents without modifying commands

#### Transparency
- All configuration visible and editable as markdown notes
- No hidden JSON files to debug
- User can see exactly what COG knows about them
- Configuration becomes part of their thinking/knowledge

#### Extensibility
- New subagents can be added by creating new `.md` files in `.claude/subagents/`
- Commands can delegate to multiple subagents as needed
- Subagents can collaborate by reading each other's outputs

### Documentation

- **README.md** - Updated to reflect:
  - Subagent architecture explanation
  - Simplified installation (no templates to copy)
  - 2-minute onboarding flow
  - Configuration-as-knowledge philosophy

- **New CHANGELOG.md** - This file, documenting all changes

### Migration Guide

If upgrading from v1.x:

1. **Remove old configuration**:
   ```bash
   rm -rf .claude/config/
   ```

2. **Remove templates**:
   ```bash
   rm -rf templates/
   ```

3. **Pull new structure**:
   ```bash
   git pull origin main
   ```

4. **Run onboarding**:
   ```
   /onboarding
   ```
   This will create your new markdown-based profile.

5. **Your existing notes are safe** - Only `.claude/` structure changed, all your braindumps, briefs, and check-ins remain unchanged.

### Technical Details

#### File Changes
- Modified: `.claude/commands/braindump.md`
- Modified: `.claude/commands/daily-brief.md`
- Modified: `.claude/commands/weekly-checkin.md`
- Modified: `README.md`
- Added: `.claude/commands/onboarding.md`
- Added: `.claude/subagents/brain-dump-analyst.md`
- Added: `.claude/subagents/news-curator.md`
- Deleted: `templates/` (entire directory)
- Deleted: `.claude/config/` (entire directory)

#### Breaking Changes
- **Configuration format changed** - Old JSON configs no longer used
- **Template system removed** - Commands that relied on templates now generate content dynamically
- **Subagent delegation required** - Commands expect subagents to exist in `.claude/subagents/`

#### Backward Compatibility
- **Existing markdown files unchanged** - All your notes, briefs, braindumps remain compatible
- **Command names unchanged** - `/braindump`, `/daily-brief`, etc. work the same from user perspective
- **Directory structure unchanged** - `00-inbox/`, `01-daily/`, etc. remain the same

### Philosophy

This release embraces two key principles:

1. **Configuration is Knowledge** - Your preferences, interests, and setup are part of your second brain, not hidden config files.

2. **Commands Orchestrate, Subagents Process** - Commands handle user interaction and context gathering; specialized subagents handle complex analysis, verification, and generation.

These principles make COG more transparent, maintainable, and aligned with the "second brain" philosophy of making all knowledge visible and editable.

---

## [1.0.0] - 2025-10-15

### Initial Release

- Basic COG structure with commands and templates
- Brain dump, daily brief, and weekly check-in functionality
- Template-based content generation
- JSON configuration system

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/).
