# Publishing COG to Claude Code Plugin Marketplaces

This guide explains how to publish COG to Claude Code plugin marketplaces.

## What's Included

COG is now marketplace-compatible with the following files:

- **`plugin.json`** - Complete plugin manifest with all commands, agents, and metadata
- **`marketplace-entry.json`** - Example marketplace entry for marketplace maintainers

## Plugin Manifest (`plugin.json`)

The `plugin.json` file contains:

### Required Fields
- `name`: "cog-second-brain" (plugin identifier)
- `version`: "1.0.0" (semantic versioning)
- `description`: Full description of COG's capabilities

### Metadata
- `author`: Author information with GitHub URL
- `homepage`: GitHub repository URL
- `repository`: Git repository details
- `license`: "MIT"
- `keywords`: Search keywords for discoverability
- `category`: "productivity"
- `tags`: Additional categorization tags

### Components

#### Skills (6 total)
1. `onboarding` - Personalization workflow
2. `daily-brief` - News intelligence
3. `braindump` - Thought capture
4. `weekly-checkin` - Pattern analysis
5. `knowledge-consolidation` - Framework building
6. `url-dump` - Quick URL capture with auto-extraction

### Extended Metadata
- `features`: List of key COG features
- `requirements`: Prerequisites (Obsidian, Git, Claude Code)
- `installation`: Quick start guide
- `directoryStructure`: Vault organization

## Marketplace Entry (`marketplace-entry.json`)

This is what marketplace maintainers would add to their marketplace catalog:

```json
{
  "name": "cog-second-brain",
  "source": "https://github.com/huytieu/COG-second-brain",
  "owner": {
    "name": "Huy Tieu",
    "email": "tqhuy1991@gmail.com",
    "url": "https://github.com/huytieu"
  },
  "description": "Self-evolving second brain with AI agents for knowledge management",
  "version": "1.0.0"
}
```

## How to Publish

### Option 1: Submit to Official Claude Code Marketplace

1. Wait for Anthropic to launch the official Claude Code plugin marketplace
2. Follow their submission process (to be announced)
3. Provide the GitHub repository URL: `https://github.com/huytieu/COG-second-brain`

### Option 2: Third-Party Marketplace

If a third-party marketplace exists:

1. **Fork or contact the marketplace repository**
2. **Add the marketplace entry** to their catalog file
3. **Submit a pull request** with:
   - Your `marketplace-entry.json` content
   - Link to your repository
   - Verification that `plugin.json` exists and is valid

### Option 3: Self-Hosted Marketplace

Create your own marketplace JSON file:

```json
{
  "marketplaces": [
    {
      "name": "cog-second-brain",
      "source": "https://github.com/huytieu/COG-second-brain",
      "owner": {
        "name": "Huy Tieu",
        "email": "tqhuy1991@gmail.com",
        "url": "https://github.com/huytieu"
      },
      "version": "1.0.0"
    }
  ]
}
```

Host this file publicly and users can add your marketplace URL to their Claude Code settings.

## Validation

To validate your plugin manifest:

```bash
# Check JSON syntax
cat .claude-plugin/plugin.json | python3 -m json.tool > /dev/null && echo "✓ JSON is valid"

# Verify all skill files exist
ls .claude/skills/onboarding/SKILL.md
ls .claude/skills/daily-brief/SKILL.md
ls .claude/skills/braindump/SKILL.md
ls .claude/skills/weekly-checkin/SKILL.md
ls .claude/skills/knowledge-consolidation/SKILL.md
ls .claude/skills/url-dump/SKILL.md
```

All paths should exist relative to the repository root.

## Installation for Users

Once published to a marketplace, users can install COG:

### Via Marketplace (Future)
1. Open Claude Code in their Obsidian vault
2. Open plugin marketplace interface
3. Search for "cog-second-brain"
4. Click install
5. Run `/onboarding` to personalize

### Via Manual Installation (Current)
```bash
cd /path/to/your/obsidian-vault
git clone https://github.com/huytieu/COG-second-brain.git
cp -r COG-second-brain/.claude .
cp COG-second-brain/plugin.json .
```

## Versioning

COG follows semantic versioning:

- **Major** (1.0.0): Breaking changes (architecture overhaul)
- **Minor** (1.1.0): New features (new commands/agents)
- **Patch** (1.0.1): Bug fixes, documentation

Update both `plugin.json` and `marketplace-entry.json` when releasing new versions.

## Support and Issues

- Report bugs: https://github.com/huytieu/COG-second-brain/issues
- Discussions: https://github.com/huytieu/COG-second-brain/discussions
- Documentation: https://github.com/huytieu/COG-second-brain/wiki

## License

COG is licensed under MIT - free for personal and commercial use.
