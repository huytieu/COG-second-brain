# COG: The Agentic Second Brain That Actually Self-Evolves

**COG = Cognition + Obsidian + Git**

A self-evolving second brain powered by AI agents, Obsidian markdown files, and Git version control. Works with **Claude Code**, **Kiro**, **Gemini CLI**, **OpenAI Codex**, and any AI that reads markdown. No database, no vendor lock-in—just `.md` files that think.

## What is COG?

COG is a personal productivity and knowledge management system that:

- 🧠 **Self-evolves**: Learns your patterns and auto-organizes content
- 🔄 **Self-heals**: Updates cross-references when you reorganize
- 📝 **Plain text**: Just markdown files (no database, no vendor lock-in)
- 📱 **Multi-device**: Syncs via iCloud to iPhone, iPad, Mac
- 🔒 **Privacy-first**: Your data, your files, your control
- 🤖 **Agent-agnostic**: Works with Claude Code, Kiro, Gemini CLI, OpenAI Codex, and more
- 🎯 **Specialized skills**: Custom AI capabilities for specific workflows
- ✅ **Verification-first**: No AI hallucinations, sources required
- 📋 **Obsidian Tasks compatible**: Tasks include `📅 YYYY-MM-DD` emoji format for dashboard queries

## Quick Start

### Prerequisites

- **AI Agent** (choose one or more):
  - [Claude Code](https://claude.ai/download) - Uses `.claude/skills/`
  - [Kiro](https://kiro.dev/) - Uses `.kiro/powers/`
  - [Gemini CLI](https://github.com/google-gemini/gemini-cli) - Uses `GEMINI.md` + `.gemini/commands/`
  - [OpenAI Codex](https://github.com/openai/codex) - Uses `AGENTS.md`
  - Any other AI agent - Uses `AGENTS.md`
- [Obsidian](https://obsidian.md/) - Recommended for viewing/editing your notes
- Git - Already on your system if you can run the clone command below

### Installation (2 Steps)

1. **Clone this repo to where you want your second brain:**
   ```bash
   git clone https://github.com/huytieu/COG-second-brain.git
   cd COG-second-brain
   ```

2. **Open your AI agent and run onboarding:**
   ```bash
   # Claude Code:
   code .  # Then ask: "Run onboarding"

   # Kiro:
   # Open folder, mention "onboarding" or "setup COG"

   # Gemini CLI:
   gemini  # Then type: /onboarding

   # OpenAI Codex:
   codex  # Then ask: "Run onboarding"

   # Other agents:
   # Reference AGENTS.md and ask to run onboarding
   ```

That's it! The onboarding will personalize COG for your needs in 2-3 minutes.

**What just happened?**
- The cloned repo IS your second brain - all files are ready to use
- Skills are defined in multiple formats for agent compatibility:
  - `.claude/skills/` - 6 Claude Code skills
  - `.kiro/powers/` - 6 Kiro powers
  - `GEMINI.md` + `.gemini/commands/` - 6 Gemini CLI commands
  - `AGENTS.md` - Universal agent documentation (OpenAI Codex and others)
- Onboarding will create your personalized directory structure

**Want Obsidian integration?**
- Open Obsidian → "Open folder as vault" → Select the `COG-second-brain` folder
- Now you can view/edit notes in Obsidian while using Claude Code for AI features

### Detailed Setup Guide

See [SETUP.md](SETUP.md) for optional configurations (Git sync, iCloud, etc.).

## What You Get

### 6 Powerful Skills

COG provides specialized AI capabilities that work across different agents. The same skills are available whether you use Claude Code, Kiro, or other AI agents.

**Setup & Personalization:**
- **onboarding** - Personalize COG for your workflow (run this first!)

**Daily Operations:**
- **braindump** - Quick capture of raw thoughts with intelligent domain classification and competitive intelligence extraction
- **daily-brief** - Personalized news intelligence with verified sources (7-day freshness requirement)
- **url-dump** - Quick capture URLs with automatic content extraction, insights, and categorization

**Weekly & Strategic:**
- **weekly-checkin** - Cross-domain pattern analysis and strategic reflection
- **knowledge-consolidation** - Build frameworks from scattered insights across all your notes

**How Skills Work:**

Skills are self-contained AI capabilities that combine orchestration and specialized processing. Each skill:
- Automatically activates when the AI agent detects relevant user intent
- Handles the complete workflow from user interaction to file creation
- Contains all necessary instructions, analysis frameworks, and verification protocols
- Works across all supported agents (Claude Code, Kiro, Gemini CLI, OpenAI Codex)

For example:
- Ask "What's on my mind?" → Agent invokes the **braindump** skill
- Say "Give me my daily brief" → Agent invokes the **daily-brief** skill
- Request "Weekly review" → Agent invokes the **weekly-checkin** skill

**Agent-Specific Formats:**
| Agent | Skill Format | Invocation |
|-------|-------------|------------|
| Claude Code | `.claude/skills/*/SKILL.md` | Auto-detected from intent |
| Kiro | `.kiro/powers/*/POWER.md` | Auto-detected from intent |
| Gemini CLI | `.gemini/commands/*.toml` → `.gemini/skills/*.md` | `/command` slash commands |
| OpenAI Codex | `AGENTS.md` | Natural language request |

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

### 4. Obsidian Tasks Integration

COG skills generate tasks with [Obsidian Tasks emoji format](https://publish.obsidian.md/tasks/Reference/Task+Formats/Tasks+Emoji+Format):

```markdown
### Immediate (24-48 hours)
- [ ] Check competitor pricing 📅 2026-02-04

### Short-term (1-2 weeks)
- [ ] Schedule team discussion 📅 2026-02-10
```

Tasks automatically appear in:
- Tasks dashboard queries ("due today", "due this week")
- Daily notes task views
- Any date-based task filtering

### 5. Privacy-First Architecture

- **Strict domain separation**: Personal, professional, project-specific
- **Local-first**: Works offline, syncs when online
- **No servers**: Your data never leaves your devices
- **Version controlled**: Full history with Git

## Directory Structure

*This structure is created automatically when you run onboarding.*

```
your-obsidian-vault/
├── AGENTS.md                  # Universal agent documentation (OpenAI Codex, etc.)
├── GEMINI.md                  # Gemini CLI context file
├── .claude/
│   └── skills/                # 6 Claude Code skills
│       ├── onboarding/
│       ├── braindump/
│       ├── daily-brief/
│       ├── weekly-checkin/
│       ├── knowledge-consolidation/
│       └── url-dump/
├── .gemini/
│   ├── commands/              # 6 Gemini CLI slash commands
│   │   ├── onboarding.toml
│   │   ├── braindump.toml
│   │   ├── daily-brief.toml
│   │   ├── weekly-checkin.toml
│   │   ├── knowledge-consolidation.toml
│   │   └── url-dump.toml
│   └── skills/                # 6 Gemini skill playbooks
├── .kiro/
│   └── powers/                # 6 Kiro powers
│       ├── cog-onboarding/
│       ├── cog-braindump/
│       ├── cog-daily-brief/
│       ├── cog-weekly-checkin/
│       ├── cog-knowledge-consolidation/
│       └── cog-url-dump/
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
    ├── booklets/              # URL bookmarks by category
    └── timeline/
```

## Example Workflows

### First Time Setup (After Cloning)

In Claude Code, ask: "Run onboarding" or "Set up my COG profile"

The onboarding skill asks ONE open-ended question: "Tell me about yourself." It intelligently extracts your name, role, interests, projects, and competitive watchlist from your natural response — no sequential form-filling. It also asks about **agent mode** (solo vs team) for power users.

**Takes 2 minutes. Everything is stored as readable markdown files.**

Onboarding creates:
- `00-inbox/MY-PROFILE.md` - Your basic info, projects, and agent mode setting
- `00-inbox/MY-INTERESTS.md` - Your topics and news sources
- `03-professional/COMPETITIVE-WATCHLIST.md` - Companies/people you're tracking (if any)
- `04-projects/[project-name]/` folders for each active project

**Agent modes** (set during onboarding, changeable anytime in MY-PROFILE.md):
- **Solo** (default): Skills handle everything directly in one conversation
- **Team**: Skills delegate research, analysis, and writing to specialist sub-agents for deeper results (works best with Claude Code)

After onboarding, COG will:
- Personalize daily briefs to your topics
- Offer your projects when you braindump
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
- ✅ **Setup is trivial**: Clone repo, run onboarding. Done in 2 minutes.
- ✅ **Maintenance-free**: Self-heals and auto-organizes
- ✅ **Actually portable**: Works on iPhone, iPad, Mac via iCloud
- ✅ **Custom skills >> generic AI**: Specialized beats ChatGPT for repeated tasks
- ✅ **Git for thoughts**: Version control shows thinking evolution

### What Doesn't Work
- Requires discipline—system only works if used consistently
- Not for everyone—if you don't think in text files, this won't click
- Requires an AI agent (Claude Code, Kiro, or compatible agent)

### Unexpected Benefits
- 💡 **Thinking partner, not just storage**: Writing brain dumps knowing they'll be analyzed improves clarity
- 📊 **Pattern recognition**: Discover insights you'd miss manually
- 🔗 **Cross-domain insights**: Personal wellness affects professional productivity (tracked quantitatively)
- 📅 **Time patterns**: Git history reveals when you think best

## Advanced Configuration

### Customizing Skills

Edit `.claude/skills/[skill-name]/SKILL.md` to customize workflows:
```markdown
---
name: my-custom-skill
description: What this skill does
---

# My Custom Skill

## When to Invoke
[When Claude should use this skill]

## Process Flow
[How it works]
```

### Adding New Skills

Create `.claude/skills/my-skill/SKILL.md`:
```markdown
---
name: my-skill
description: Brief description for Claude to know when to invoke this
---

# My Custom Skill

## Purpose
[What this skill does]

## When to Invoke
[User intent patterns that should trigger this]

## Process Flow
[Detailed instructions]
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
A: No! COG supports multiple AI agents with native integrations:
- **Claude Code**: Uses `.claude/skills/` (native support)
- **Kiro**: Uses `.kiro/powers/` (native support)
- **Gemini CLI**: Uses `GEMINI.md` + `.gemini/commands/` (native slash commands)
- **OpenAI Codex**: Uses `AGENTS.md` (auto-loaded at startup)
- Any AI that reads markdown can use COG's skills via `AGENTS.md`

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
- [Kiro](https://kiro.dev/) by AWS
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) by Google
- [OpenAI Codex](https://github.com/openai/codex) by OpenAI
- [Obsidian](https://obsidian.md/) for markdown management
- Inspiration from Zettelkasten, Building a Second Brain, and GTD methodologies

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=huytieu/COG-second-brain&type=date&legend=top-left)](https://www.star-history.com/#huytieu/COG-second-brain&type=date&legend=top-left)

---

**TL;DR:** COG is a self-evolving agentic second brain using AI agents + Obsidian + Git. Works with Claude Code, Kiro, Gemini CLI, OpenAI Codex, and more. Just `.md` files that sync via iCloud and learn your patterns. Setup in 2 steps, zero maintenance required.

⭐ Star this repo if you find it useful!
