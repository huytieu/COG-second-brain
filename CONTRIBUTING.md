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
   - Keep the support matrix truthful in `README.md`, `SETUP.md`, `AGENTS.md`, and `docs/AGENT-SUPPORT.md`
   - Run `./scripts/validate-agent-surface.sh` before opening the PR

#### Making Changes

1. **Worker Agents**: New agents should be added to `.claude/agents/` with this format:
   - YAML frontmatter with `name`, `description`, and `model` (use `sonnet` for I/O tasks, `opus` only if reasoning is required)
   - Clear capability list and output rule
   - Add the file to `FRAMEWORK_FILES` in `cog-update.sh`
   - Document in `AGENTS.md` under "Worker Agents"
2. **Skills**: New skills should be added in every surface that claims to support them:
   - `.claude/skills/[name]/SKILL.md` - Claude Code format (required; include `roles` and `integrations` in frontmatter)
   - `AGENTS.md` - Universal documentation (required)
   - `.claude-plugin/plugin.json` - Packaged skill manifest (required)
   - `.kiro/powers/cog-[name]/POWER.md` - Kiro format (if Kiro supports the skill)
   - `.gemini/commands/[name].toml` + `.gemini/skills/[name].md` - Gemini CLI format (if Gemini supports the skill)
   - If the skill is role-specific, add it to relevant role packs in `.claude/roles/`
   - **If the skill mutates external state** (publishes, posts, deploys, transitions tickets), it MUST include a "Verify" step that observes the mutated artifact (curl the URL, screenshot the post) before reporting success — see the Skill Post-Condition Rule in `CLAUDE.md`
   - **Prompting note for reasoning models**: don't write "show your reasoning" / "think step by step" instructions into SKILL.md files — modern reasoning models handle this internally, and forcing it degrades output. State the goal and the constraints instead.
   - If the skill iterates, declare its loop per `/loop-engineering`; if it captures reusable environment knowledge, consider the [skill distillation pattern](docs/SKILL-DISTILLATION.md)
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
5. Run `./scripts/validate-agent-surface.sh` for packaging/manifest consistency

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

- **New Skills**: Useful skills for common workflows (add in all agent formats)
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
2. Create a test Obsidian vault
3. Copy COG files to your test vault
4. Make changes and test
5. Submit PR when ready

## Coding Conventions

### Claude Code Skills (`.claude/skills/[name]/SKILL.md`)

```markdown
---
name: skill-name
description: What this skill does
roles: [all]
integrations: [github, slack]
---

# Skill Name

## When to Invoke
[Trigger patterns]

## Process Flow
[Step-by-step process]

## Output Structure
[Expected output format]
```

### Kiro Powers (`.kiro/powers/cog-[name]/POWER.md`)

```markdown
---
name: "cog-skill-name"
displayName: "Skill Display Name"
description: "What this power does"
keywords: ["keyword1", "keyword2", "keyword3"]
---

# Skill Name

## When This Power Activates
[Trigger patterns]

## Process Flow
[Step-by-step process]
```

### Worker Agents (`.claude/agents/[name].md`)

```markdown
---
name: worker-name
description: What this worker does
model: sonnet
---

You are a [role]. Your job is [single responsibility].

## Capabilities
- **Source**: What it can access

## Output Rule
- Always write results to `/tmp/{task-slug}.md`
- Return ONLY a short status + file path

## Rules
- Never fabricate data
- [domain-specific rules]
```

### Universal Documentation (`AGENTS.md`)

Add new skills under "## Available Commands" with:
- Command name and triggers
- Description and purpose
- What it does (numbered list)
- Output locations

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
