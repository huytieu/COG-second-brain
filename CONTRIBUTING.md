# Contributing to COG

Thank you for your interest in contributing to COG! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in [GitHub Issues](https://github.com/huytieu/COG-second-brain/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Obsidian version, AI agent used: Claude Code/Kiro/Other)

### Suggesting Enhancements

We welcome ideas for new features or improvements:

1. Create an issue with the "enhancement" label
2. Describe the feature and why it would be useful
3. Provide examples or mockups if applicable
4. Be open to discussion and feedback

### Pull Requests

#### Before You Start

1. Fork the repository
2. Create a new branch for your feature/fix
3. Ensure your changes align with COG's philosophy:
   - Simplicity over complexity
   - Plain text over proprietary formats
   - Self-evolving intelligence
   - Verification-first approach
4. **If your PR changes the framework** (skills, docs, scripts):
   - Bump the version in `COG-VERSION` (e.g., `3.2.0` → `3.3.0`)
   - Add a changelog entry in `CHANGELOG.md`
   - If adding a new file, add it to the `FRAMEWORK_FILES` array in `cog-update.sh`
   - Update `marketplace-entry.json` and `.claude-plugin/plugin.json` version fields

#### Making Changes

1. **Skills**: Add new skills to `.agents/skills/[name]/SKILL.md` only (single source of truth):
   - Follow the [agentskills.io](https://agentskills.io/specification) standard format
   - Include `metadata.keywords` and `metadata.display-name` for Kiro compatibility
   - Run `./cog-sync.sh` to generate tool-specific files (Claude Code, Gemini CLI, Kiro)
   - If the skill is role-specific, add it to relevant role packs in `.cog/user-roles/`
   - **Never hand-edit** generated files — see [How skills are discovered](#how-skills-are-discovered) below
2. **Templates**: Follow existing YAML frontmatter conventions
3. **Documentation**: Update README.md if adding major features
4. **Examples**: Provide examples of your feature in action

#### Code Style

- **Markdown**: Use consistent formatting
- **YAML**: Follow existing metadata structure
- **Comments**: Explain complex logic or non-obvious decisions
- **Naming**: Use clear, descriptive names

#### Testing

Before submitting:

1. Test your command/feature in actual COG setup
2. Ensure it works with existing commands
3. Verify it doesn't break existing functionality
4. Check that documentation is accurate
5. Run `./cog-sync.sh --check` to verify all files are in sync

#### Submitting

1. Commit your changes with clear, descriptive messages
2. Push to your fork
3. Create a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Examples or screenshots if applicable
   - Testing you've done

## Types of Contributions We're Looking For

### High Priority

- **New Skills**: Useful skills for common workflows (add to `.agents/skills/`, sync generates all formats)
- **Agent Format Support**: Improve support for additional AI agents
- **Documentation**: Tutorials, examples, use cases
- **Bug Fixes**: Fixes for reported issues

### Medium Priority

- **Specialized Skills**: New skills for specific domains
- **Integration Scripts**: Scripts for connecting COG with other tools
- **Workflow Examples**: Real-world workflow demonstrations
- **Performance Improvements**: Optimizations for large vaults

### Welcome But Lower Priority

- **UI/Visual**: Visual improvements (COG is text-first)
- **Platform-Specific**: Features for specific platforms (keep it universal)
- **Advanced Features**: Complex features that increase learning curve

## Development Setup

1. Fork and clone the repository
2. Edit skills in `.agents/skills/[name]/SKILL.md` (the single source of truth)
3. Run `./cog-sync.sh` to generate tool-specific files
4. Run `./cog-sync.sh --check` to verify parity
5. Test your changes in an actual COG vault with your preferred AI agent
6. Submit PR when ready

## Coding Conventions

### Skills (`.agents/skills/[name]/SKILL.md` — single source of truth)

Skills follow the [agentskills.io](https://agentskills.io/specification) open standard:

```markdown
---
name: skill-name
description: What this skill does and when to use it. Include trigger keywords.
metadata:
  roles: all
  integrations: github,slack
  keywords: keyword1,keyword2,keyword3
  display-name: COG Skill Name
---

# Skill Name

## When to Invoke
[Trigger patterns]

## Process Flow
[Step-by-step process]

## Output Structure
[Expected output format]
```

After creating or editing a skill, run `./cog-sync.sh` to generate tool-specific files.

### How skills are discovered

Each AI tool discovers skills from its own native folder. `cog-sync.sh` generates these from the single source of truth in `.agents/skills/`:

| Generated file | What sync produces | How the tool uses it |
|---|---|---|
| `.claude/skills/[name]/SKILL.md` | Copy of source skill (as-is) | Claude Code loads skills from this folder natively |
| `.gemini/skills/[name].md` | Skill body only (no frontmatter) | Referenced by `.gemini/commands/[name].toml` via `@{path}` |
| `.gemini/commands/[name].toml` | Entry point with description + prompt | Gemini CLI registers these as `/commands` |
| `.kiro/powers/cog-[name]/POWER.md` | Kiro frontmatter (`displayName`, `keywords` array) + body | Kiro activates powers by keyword matching |
| `CLAUDE.md` | Pure copy of AGENTS.md, or header + AGENTS.md if marker present | Claude Code reads as project instructions |
| `GEMINI.md` | Pure copy of AGENTS.md, or header + AGENTS.md if marker present | Gemini CLI reads as project context |

**When adding a new skill**, also add a row to the skill table in `AGENTS.md`. This table is the skill catalog for agents without native skill discovery (e.g., OpenAI Codex). Tools with native folders (Claude Code, Gemini CLI, Kiro) discover skills automatically from their generated folders.

**Context files (CLAUDE.md, GEMINI.md)** support two modes:
- **Pure copy**: No marker — the file becomes an exact copy of AGENTS.md
- **Header + AGENTS.md**: If the file contains a `<!-- AUTO-GENERATED -->` marker, content above it is preserved and AGENTS.md is appended below. Use this for tool-specific notes (e.g., Gemini's `.gemini/commands/` path hint).

**Never hand-edit** files in `.claude/skills/`, `.gemini/skills/`, `.gemini/commands/`, or `.kiro/powers/` — they are overwritten on every sync. Also never edit content below the `<!-- AUTO-GENERATED -->` marker in context files.

### Template Files

```yaml
---
type: "template-type"
domain: "domain"
date: "{{date:YYYY-MM-DD}}"
# Standard metadata fields
---

# {{title}}

[Template structure]
```

## Community Guidelines

### Be Respectful

- Treat all contributors with respect
- Provide constructive feedback
- Be open to different perspectives
- Help newcomers get started

### Be Clear

- Write clear commit messages
- Explain your reasoning
- Provide context in PRs
- Ask questions when unclear

### Be Patient

- Maintainers are volunteers
- Reviews may take time
- Be responsive to feedback
- Iterate based on suggestions

## Questions?

- **General Questions**: [Discussions](https://github.com/huytieu/COG-second-brain/discussions)
- **Bug Reports**: [Issues](https://github.com/huytieu/COG-second-brain/issues)
- **Feature Requests**: [Issues](https://github.com/huytieu/COG-second-brain/issues) with "enhancement" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to COG! Your help makes this project better for everyone.
