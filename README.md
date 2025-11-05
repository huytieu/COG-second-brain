# COG: The Easiest Second Brain That Actually Self-Evolves

**COG = Claude + Obsidian + Git**

A self-evolving second brain system using Claude Code, Obsidian markdown files, and Git version control. No database, no vendor lock-in—just `.md` files that think.

## What is COG?

COG is a personal productivity and knowledge management system that:

- 🧠 **Self-evolves**: Learns your patterns and auto-organizes content
- 🔄 **Self-heals**: Updates cross-references when you reorganize
- 📝 **Plain text**: Just markdown files (no database, no vendor lock-in)
- 📱 **Multi-device**: Syncs via iCloud to iPhone, iPad, Mac
- 🔒 **Privacy-first**: Your data, your files, your control
- 🎯 **Specialized agents**: Custom AI assistants for specific workflows
- ✅ **Verification-first**: No AI hallucinations, sources required

## Quick Start

### Prerequisites

- [Obsidian](https://obsidian.md/) installed
- [Claude Code](https://claude.ai/download) (or VSCode with Claude extension)
- Git (optional but recommended)

### Installation (3 Steps)

1. **Clone this repo into your Obsidian vault:**
   ```bash
   cd /path/to/your/obsidian-vault
   git clone https://github.com/huytieu/COG-second-brain.git
   ```

2. **Copy COG structure to your vault:**
   ```bash
   cp -r COG-second-brain/.claude .
   ```

3. **Open Claude Code in your vault and invoke onboarding:**
   ```bash
   code .
   # In Claude Code, ask: "Run onboarding" or "Set up my COG profile"
   ```

That's it! The onboarding will personalize COG for your needs in 3-5 minutes.

> **Note:** COG is also available in community plugin marketplaces. Once official Claude Code plugin support is released, marketplace installation will be the recommended method.

### Detailed Setup Guide

See [SETUP.md](SETUP.md) for step-by-step instructions with screenshots.

## What You Get

### 5 Powerful Skills

COG uses Claude's Agent Skills architecture - specialized capabilities that Claude automatically invokes when relevant to your request.

**Setup & Personalization:**
- **onboarding** - Personalize COG for your workflow (run this first!)

**Daily Operations:**
- **braindump** - Quick capture of raw thoughts with intelligent domain classification and competitive intelligence extraction
- **daily-brief** - Personalized news intelligence with verified sources (7-day freshness requirement)

**Weekly & Strategic:**
- **weekly-checkin** - Cross-domain pattern analysis and strategic reflection
- **knowledge-consolidation** - Build frameworks from scattered insights across all your notes

**How Skills Work:**

Skills are self-contained AI capabilities that combine orchestration and specialized processing. Unlike the old command/subagent split, each skill now:
- Automatically activates when Claude detects relevant user intent
- Handles the complete workflow from user interaction to file creation
- Contains all necessary instructions, analysis frameworks, and verification protocols
- Uses progressive disclosure to load information only as needed

For example:
- Ask "What's on my mind?" → Claude invokes the **braindump** skill
- Say "Give me my daily brief" → Claude invokes the **daily-brief** skill
- Request "Weekly review" → Claude invokes the **weekly-checkin** skill

This architecture leverages Claude Code's native skill system for better performance and simpler maintenance.

## Key Features

### 1. Self-Evolving Intelligence

COG doesn't just store notes—it actively learns:

- **Pattern recognition**: Identifies recurring themes across your notes
- **Auto-classification**: Categorizes content by domain (personal/professional/projects)
- **Knowledge consolidation**: Synthesizes scattered insights into frameworks
- **Adaptive learning**: Gets better at understanding your thinking patterns

**Weekly Evolution Cycle:**
```
Monday-Friday: Capture thoughts via braindump skill
Friday: Run knowledge-consolidation skill
→ COG analyzes ALL your notes
→ Builds frameworks you didn't explicitly create
→ Updates "single source of truth" files
→ Next week, it knows more about how you think
```

### 2. Self-Healing System

- Rename a file? COG updates all cross-references
- Change project structure? Auto-reclassifies content
- New project emerges? Auto-creates tracking folders
- Competitive intel mentioned? Auto-updates competitor files

### 3. Verification-First (No AI Hallucinations)

- All news must be verified with sources and dates
- 7-day freshness requirement for current events
- Explicit confidence levels for all analysis
- Multi-source cross-referencing required

### 4. Privacy-First Architecture

- **Strict domain separation**: Personal, professional, project-specific
- **Local-first**: Works offline, syncs when online
- **No servers**: Your data never leaves your devices
- **Version controlled**: Full history with Git

## Directory Structure

```
your-obsidian-vault/
├── .claude/
│   └── skills/                # 5 specialized skills
│       ├── onboarding/
│       │   └── SKILL.md
│       ├── braindump/
│       │   └── SKILL.md
│       ├── daily-brief/
│       │   └── SKILL.md
│       ├── weekly-checkin/
│       │   └── SKILL.md
│       └── knowledge-consolidation/
│           └── SKILL.md
├── 00-inbox/                  # Temporary processing area
│   ├── MY-PROFILE.md          # Your profile (created by onboarding)
│   ├── MY-INTERESTS.md        # Your topics & news sources
│   └── WELCOME-TO-COG.md      # Getting started guide
├── 01-daily/                  # Daily briefs and check-ins
│   ├── briefs/
│   └── checkins/
├── 02-personal/               # Personal domain (strict privacy)
│   ├── braindumps/
│   ├── development/
│   └── wellness/
├── 03-professional/           # Professional domain
│   ├── braindumps/
│   ├── leadership/
│   ├── strategy/
│   ├── skills/
│   └── COMPETITIVE-WATCHLIST.md  # Companies/people to track
├── 04-projects/               # Project-specific tracking
│   └── [your-project]/
│       ├── braindumps/
│       ├── competitive/       # Auto-updated intel
│       └── content/
└── 05-knowledge/              # Consolidated insights
    ├── consolidated/
    ├── patterns/
    └── timeline/
```

## Example Workflows

### First Time Setup

Ask Claude: "Run onboarding" or "Set up my COG profile"

The onboarding skill will ask:
- Your name
- What you do (your job/role)
- Topics you're interested in (3-5 main areas)
- Where you get your news (preferred sources)
- Active projects you're working on (optional)
- Companies/people you want to track (optional)

**Takes 2 minutes. Everything is stored as readable markdown files in your vault.**

It creates:
- `MY-PROFILE.md` - Your basic info and projects
- `MY-INTERESTS.md` - Your topics and news sources
- `COMPETITIVE-WATCHLIST.md` - Companies/people you're tracking (if any)
- Project folders for each active project

After onboarding, COG will:
- Personalize daily briefs to your topics
- Offer your projects in braindumps
- Auto-extract competitive intel you care about

### Daily Intelligence Briefing

Ask Claude: "Give me my daily brief" or "What's the news today?"

Generates a personalized briefing with:
- Verified news from the last 7 days
- Strategic analysis relevant to your interests
- Competitive intelligence auto-extracted
- Actionable next steps

### Brain Dump → Strategic Insights

Ask Claude: "I need to braindump" or "What's on my mind?"

Single integrated workflow:
1. **Quick capture**: Preserves spontaneity, no filtering
2. **Intelligent processing**: Automatically extracts themes, actions, connections

The system automatically:
- Classifies by domain
- Detects competitive intelligence
- Cross-references related content
- Identifies action items

### Knowledge Consolidation

Ask Claude: "Consolidate my knowledge" or "Build frameworks from my notes"

Weekly or monthly:
- Analyzes patterns across all braindumps
- Builds frameworks from scattered insights
- Updates "single source of truth" knowledge base
- Tracks evolution of thinking over time

## Why COG Works

### What Works
- ✅ **Setup is trivial**: Drop files in, done. No complex configuration.
- ✅ **Maintenance-free**: Self-heals and auto-organizes
- ✅ **Actually portable**: Works on iPhone, iPad, Mac via iCloud
- ✅ **Custom agents >> generic AI**: Specialized beats ChatGPT for repeated tasks
- ✅ **Git for thoughts**: Version control shows thinking evolution

### What Doesn't Work
- ⚠️ Requires discipline—system only works if used consistently
- ⚠️ Not for everyone—if you don't think in text files, this won't click
- ⚠️ Requires Claude Code (though adaptable to other AI environments)

### Unexpected Benefits
- 💡 **Thinking partner, not just storage**: Writing brain dumps knowing they'll be analyzed improves clarity
- 📊 **Pattern recognition**: Discover insights you'd miss manually
- 🔗 **Cross-domain insights**: Personal wellness affects professional productivity (tracked quantitatively)
- 📅 **Time patterns**: Git history reveals when you think best

## Advanced Configuration

### Customizing Commands

Edit `.claude/commands/*.md` to customize workflows:
```markdown
# Custom Command Example
/my-workflow

Your custom prompt here...
```

### Adding New Agents

Create `.claude/subagents/my-agent.md`:
```markdown
# My Custom Agent

## Purpose
[What this agent does]

## Process
[How it works]
```

### Template Customization

Modify `06-templates/*.md` to match your workflow:
```yaml
---
type: "custom-type"
domain: "personal|professional|project"
# Add your metadata fields
---
```

## Syncing Across Devices

### iCloud Sync (Recommended)
- Store vault in `iCloud Drive/Obsidian/`
- Automatically syncs to all Apple devices
- Obsidian mobile works perfectly

### Git Sync
```bash
# Daily workflow
git add .
git commit -m "Update knowledge base"
git push
```

Combine both: iCloud for instant sync, Git for version history.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

**Ideas for contributions:**
- New specialized agents
- Additional slash commands
- Template improvements
- Documentation enhancements
- Example workflows

## Roadmap

- [ ] Gemini support (in addition to Claude)
- [ ] Web interface for knowledge graph visualization
- [ ] Mobile-first commands (optimized for Obsidian mobile)
- [ ] Team collaboration features (with privacy preservation)
- [ ] Integration with calendar/task management tools

## Real-World Results

After 3 months of use:
- 120+ structured braindumps processed
- Daily briefs with 95%+ source accuracy
- 5 major strategic insights discovered
- 0 maintenance required
- 0 vendor lock-in anxiety

## FAQ

**Q: Why not just use Notion/Roam/Obsidian alone?**
A: COG adds self-evolving intelligence. It doesn't just store—it learns, analyzes, and synthesizes insights automatically.

**Q: Do I need Claude Code specifically?**
A: Claude Code is recommended, but you can adapt the commands for any AI environment (VSCode + Claude extension, custom API integration, etc.)

**Q: How much does it cost?**
A: COG is free (MIT license). You only pay for Claude Code usage (Anthropic's pricing).

**Q: Is my data private?**
A: Yes. Everything is local markdown files. COG uses Claude's API only when you invoke commands. No data stored on external servers.

**Q: Can I use this for team collaboration?**
A: Currently designed for personal use. Team features planned for future releases.

**Q: What if I don't use Git?**
A: Git is optional but recommended for version history. COG works fine without it using just iCloud sync.

## License

MIT License - see [LICENSE](LICENSE) for details.

Feel free to use COG for personal or commercial projects. If you build something cool with it, I'd love to hear about it!

## Support COG's Development

If COG has helped you build a better second brain, consider supporting its continued development:

- ⭐ Star this repo to increase visibility
- 💝 [Sponsor on GitHub](https://github.com/sponsors/huytieu) - Monthly support with perks
- ☕ [Buy me a coffee](https://buymeacoffee.com/0xlight) - One-time appreciation
- 🐛 [Report bugs](https://github.com/huytieu/COG-second-brain/issues)
- 💬 [Share ideas](https://github.com/huytieu/COG-second-brain/discussions)
- 📖 [Contribute](CONTRIBUTING.md)

COG is free and open-source (MIT license). Your support helps keep it that way while enabling new features and better documentation.

## Acknowledgments

Built with:
- [Claude Code](https://claude.ai/code) by Anthropic
- [Obsidian](https://obsidian.md/) for markdown management
- Inspiration from Zettelkasten, Building a Second Brain, and GTD methodologies

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=huytieu/COG-second-brain&type=date&legend=top-left)](https://www.star-history.com/#huytieu/COG-second-brain&type=date&legend=top-left)

---

**TL;DR:** COG is a self-evolving second brain using Claude Code + Obsidian + Git. Just `.md` files that sync via iCloud and learn your patterns. Setup in 3 steps, zero maintenance required.

⭐ Star this repo if you find it useful!
