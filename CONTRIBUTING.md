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
   - Your environment (OS, Obsidian version, Claude Code version)

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

#### Making Changes

1. **Commands**: New commands should be self-contained `.md` files in `.claude/commands/`
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

- **New Commands**: Useful slash commands for common workflows
- **Improved Templates**: Better templates for specific use cases
- **Documentation**: Tutorials, examples, use cases
- **Bug Fixes**: Fixes for reported issues

### Medium Priority

- **Specialized Agents**: New subagents for specific domains
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

### Command Files

```markdown
# Command Name

## Purpose
[Clear one-sentence description]

## Command: `/command-name`

## Process Flow
[Step-by-step process]

## Metadata Template
[YAML template]

## Output Structure
[Expected output format]

## Guidelines
[Usage guidelines]
```

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
