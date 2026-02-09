# COG Setup Guide

Complete step-by-step instructions for setting up your COG (Cognition + Obsidian + Git) agentic second brain system.

## Quick Start (Easiest Way)

### What You Need

1. **AI Agent** (choose one or more):
   - [Claude Code](https://claude.ai/download) - Uses `.claude/skills/`
   - [Kiro](https://kiro.dev/) - Uses `.kiro/powers/`
   - Any OpenAI-compatible agent - Uses `agents.md`
2. **Obsidian** ([Download here](https://obsidian.md/)) - Recommended (optional)
3. **Git** - Already on your system if you can run clone commands

### Installation (2 Steps)

**Step 1: Clone the repo to where you want your second brain**
```bash
git clone https://github.com/huytieu/COG-second-brain.git
cd COG-second-brain
```

**Step 2: Open your AI agent and run onboarding**

**Claude Code:**
```bash
code .
# Ask: "Run onboarding"
```

**Kiro:**
- Open the folder in Kiro
- Say "onboarding" or "setup COG"
- Kiro will activate the cog-onboarding power

**Other Agents:**
- Point the agent to `agents.md` for skill documentation
- Ask it to run the onboarding workflow

That's it! You now have a working second brain.

**What just happened?**
- The cloned `COG-second-brain` folder IS your second brain
- 6 AI skills are available in multiple formats:
  - `.claude/skills/` - For Claude Code
  - `.kiro/powers/` - For Kiro
  - `agents.md` - For any agent
- Onboarding will create your personalized directory structure

**Optional: Use with Obsidian**

If you want to view/edit your notes in Obsidian:
1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `COG-second-brain` folder
4. Done! Now you have both Claude Code AI features AND Obsidian's visual interface

**Recommended: Install Obsidian Tasks Plugin**

COG generates tasks with [Obsidian Tasks emoji format](https://publish.obsidian.md/tasks/Reference/Task+Formats/Tasks+Emoji+Format) (`📅 YYYY-MM-DD`). To use task dashboards and date-based queries:
1. Open Obsidian Settings → Community plugins
2. Browse and install "Tasks" plugin
3. Enable the plugin
4. COG tasks will now appear in your Tasks queries (due today, due this week, etc.)

## First Use

### Day 1: Personalize COG

**In Claude Code, ask:** "Run onboarding"

Onboarding will ask you:
- Your name
- What you do (role/job)
- Topics you're interested in (3-5 areas)
- Where you get your news
- Active projects (optional)
- Companies/people to track (optional)

**Takes 2 minutes. Everything is stored as markdown files you can edit.**

Onboarding creates:
- `00-inbox/MY-PROFILE.md` - Your info and projects
- `00-inbox/MY-INTERESTS.md` - Topics for daily briefs
- `03-professional/COMPETITIVE-WATCHLIST.md` - Tracking list (if any)
- Project folders in `04-projects/`

### Test Your Setup

**Try your first braindump:**
Ask Claude: "I need to braindump"

Share any thoughts on your mind. The system will:
- Capture your raw thoughts
- Analyze themes and patterns
- Extract action items
- Save to appropriate domain folder

**Get your first daily brief:**
Ask Claude: "Give me my daily brief"

COG will generate personalized news based on your interests.

### Week 1: Build the Habit

Use these skills daily:
- **Morning:** "Give me my daily brief" - Get personalized intelligence
- **Throughout day:** "I need to braindump" - Capture thoughts
- **Evening:** Open Obsidian to review your braindumps

### Week 2: Start Reflecting

After a week of braindumps:
- **Weekly:** "Weekly review" or "Weekly checkin" - Pattern analysis
- **Monthly:** "Consolidate my knowledge" - Build frameworks

## Understanding the Directory Structure

After running onboarding, you'll have this structure:

```
COG-second-brain/              # This is your second brain folder
├── agents.md                  # Universal agent documentation
├── .claude/
│   └── skills/                # 6 Claude Code skills
│       ├── onboarding/
│       ├── braindump/
│       ├── daily-brief/
│       ├── weekly-checkin/
│       ├── knowledge-consolidation/
│       └── url-dump/
├── .kiro/
│   └── powers/                # 6 Kiro powers
│       ├── cog-onboarding/
│       ├── cog-braindump/
│       ├── cog-daily-brief/
│       ├── cog-weekly-checkin/
│       ├── cog-knowledge-consolidation/
│       └── cog-url-dump/
├── 00-inbox/                  # Temporary & profile files (created by onboarding)
├── 01-daily/                  # Daily briefs and check-ins
│   ├── briefs/
│   └── checkins/
├── 02-personal/               # Personal domain (private)
│   └── braindumps/
├── 03-professional/           # Professional domain
│   └── braindumps/
├── 04-projects/               # Project-specific (created by onboarding)
├── 05-knowledge/              # Consolidated insights
│   ├── consolidated/
│   ├── patterns/
│   ├── booklets/              # URL bookmarks
│   └── timeline/
└── 06-templates/              # Markdown templates
```

## Optional: Advanced Configuration

### Git Version Control

Your second brain is already a Git repo (you cloned it). To track your changes:

**Track your personal changes:**
```bash
git add .
git commit -m "Updated my braindumps and profiles"
```

**Create your own GitHub backup:**
```bash
# Remove the original remote
git remote remove origin

# Add your own GitHub repo
git remote add origin https://github.com/yourusername/my-second-brain.git
git push -u origin main
```

**Keep `.gitignore` updated:**
The repo includes a `.gitignore` that excludes Obsidian cache files. If you notice unwanted files being tracked, add them:
```bash
echo "unwanted-folder/" >> .gitignore
git add .gitignore
git commit -m "Update gitignore"
```

### iCloud Sync (Apple Devices)

Want your second brain on iPhone, iPad, and Mac?

**Step 1: Move to iCloud**
```bash
# Move the COG folder to iCloud Obsidian folder
mv COG-second-brain ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/
```

**Step 2: Update Obsidian**
- Open Obsidian on Mac
- "Open folder as vault" → Navigate to iCloud location
- Select the COG folder

**Step 3: Install Obsidian Mobile**
- Install Obsidian on iPhone/iPad
- Open the same vault
- iCloud will sync automatically

**Step 4: Claude Code on Mac**
```bash
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/COG-second-brain
code .
```

Now your braindumps sync across all Apple devices!

### Customizing Your Interests

**Option 1: Edit directly**
Open `00-inbox/MY-INTERESTS.md` and edit the topics and sources.

**Option 2: Re-run onboarding**
In Claude Code, ask: "Run onboarding" and select "Update interests"

### Adding Projects

**Option 1: Via onboarding**
In Claude Code, ask: "Run onboarding" → "Add new projects"

**Option 2: Manual**
Create project folder manually:
```bash
mkdir -p 04-projects/my-new-project/{braindumps,competitive,content,planning,resources}
```

Then create `04-projects/my-new-project/PROJECT-OVERVIEW.md`:
```markdown
---
type: project-overview
project: My New Project
created: 2025-01-15
status: active
---

# My New Project

## What is this project?
[Brief description]

## Current Status
[What phase you're in]

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

Update `00-inbox/MY-PROFILE.md` to include the new project in your active projects list.

## Customizing Skills

Want to customize how COG works? Skills are defined in multiple formats for different agents.

### For Claude Code

**Edit existing skills:**
```bash
code .claude/skills/braindump/SKILL.md
```

Each `SKILL.md` file contains:
- `name` and `description` (tells Claude when to invoke)
- `When to Invoke` section (trigger patterns)
- `Process Flow` (detailed instructions)

**Create new skills:**
```bash
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md
```

### For Kiro

**Edit existing powers:**
```bash
code .kiro/powers/cog-braindump/POWER.md
```

Each `POWER.md` file contains:
- `name`, `displayName`, `description`, `keywords` in frontmatter
- Onboarding and steering instructions in body

**Create new powers:**
```bash
mkdir -p .kiro/powers/my-power
touch .kiro/powers/my-power/POWER.md
```

### For Other Agents

Edit `agents.md` to add or modify skill documentation. This file serves as universal documentation that any AI agent can read.

### Keeping Skills in Sync

When you modify a skill, update all formats:
1. `.claude/skills/[name]/SKILL.md` - Claude Code
2. `.kiro/powers/cog-[name]/POWER.md` - Kiro
3. `agents.md` - Universal documentation

## Troubleshooting

### Skills Not Recognized

**Problem:** Agent doesn't recognize skill invocations

**Solutions for Claude Code:**
1. Check `.claude/skills/` folder exists in your COG folder
2. Verify each skill folder has a `SKILL.md` file
3. Make sure you're running Claude Code from the COG folder root
4. Try restarting Claude Code

**Solutions for Kiro:**
1. Check `.kiro/powers/` folder exists
2. Verify each power folder has a `POWER.md` file
3. Try mentioning specific keywords from the power's `keywords` list

**Solutions for Other Agents:**
1. Ensure `agents.md` exists in the root folder
2. Point the agent to read `agents.md` for available commands

### Files Saving to Wrong Location

**Problem:** Braindumps or briefs save to unexpected directories

**Solutions:**
1. Make sure you're in the COG folder when running Claude Code
2. Check that all required directories exist (run onboarding if you haven't yet)
3. The directory structure should match the layout shown above

### Obsidian Not Showing Files

**Problem:** Files created by COG don't appear in Obsidian

**Solutions:**
1. In Obsidian, make sure you opened the COG folder as a vault
2. Try refreshing Obsidian (Cmd/Ctrl+R)
3. Check Obsidian settings → Files & Links → "Excluded files" doesn't block COG files

### iCloud Sync Issues

**Problem:** Changes don't sync across devices

**Solutions:**
1. Check iCloud Drive is enabled in System Settings
2. Ensure Obsidian mobile points to the same iCloud vault
3. Wait a few minutes - iCloud can be slow
4. Check available iCloud storage space
5. Try turning iCloud sync off and on again

### Git Conflicts

**Problem:** Git shows merge conflicts

**Solutions:**
COG files are just markdown - conflicts are easy to resolve:
1. Open the conflicted file in a text editor
2. Look for `<<<<<<<`, `=======`, and `>>>>>>>` markers
3. Keep the version you want, delete conflict markers
4. Save the file
5. Run: `git add [filename] && git commit -m "Resolved conflict"`

## Daily Workflow Examples

### Morning Routine (5 minutes)
```
In Claude Code:
"Give me my daily brief"

Review the intelligence, note any actions needed
```

### Throughout the Day
```
Whenever you have thoughts:
"I need to braindump"

Just dump your thoughts - no structure needed
The system will analyze and organize automatically
```

### End of Week (30 minutes)
```
Friday afternoon:
"Weekly review" or "Let's do my weekly checkin"

Reflect on patterns, plan next week
```

### Monthly (1 hour)
```
First of the month:
"Consolidate my knowledge" or "Build frameworks from my notes"

Analyze accumulated braindumps, build frameworks
```

## Keeping COG Updated

When new COG versions are released (new skills, improved docs, bug fixes), you can safely update framework files without touching your personal content.

### Method 1: AI Agent (Recommended)

Ask any supported agent:
```
"Update COG" or /update-cog
```

The agent will:
1. Check your current version against upstream
2. Show what's changed
3. Let you approve updates per-file (with backup option for customized files)
4. Apply updates and suggest a commit

### Method 2: Shell Script

```bash
# Check for available updates (no changes made)
./cog-update.sh --check

# Preview what would change (no changes made)
./cog-update.sh --dry-run

# Interactive update — prompts for each file
./cog-update.sh

# Update everything without prompting
./cog-update.sh --force
```

### Method 3: Manual Git

```bash
# One-time setup: add the upstream remote
git remote add cog-upstream https://github.com/huytieu/COG-second-brain.git

# Fetch latest
git fetch cog-upstream main

# Update specific files (surgical replacement, no merge needed)
git checkout cog-upstream/main -- README.md SETUP.md AGENTS.md
git checkout cog-upstream/main -- .claude/skills/ .kiro/powers/ .gemini/
git checkout cog-upstream/main -- COG-VERSION cog-update.sh

# Commit the update
git add -A && git commit -m "Update COG framework to v$(cat COG-VERSION)"
```

### What Gets Updated vs What Doesn't

| Updated (framework files) | Never touched (your content) |
|---|---|
| Skills (`.claude/skills/`, `.kiro/powers/`, `.gemini/`) | `00-inbox/` (profiles, notes) |
| Docs (`README.md`, `SETUP.md`, `AGENTS.md`, etc.) | `01-daily/` (briefs, checkins) |
| Scripts (`cog-update.sh`) | `02-personal/` (braindumps) |
| Config (`.gitignore`, `plugin.json`) | `03-professional/` (braindumps) |
| Version (`COG-VERSION`) | `04-projects/` (project files) |
| | `05-knowledge/` (consolidated) |
| | `06-templates/` (your templates) |

### Checking Your Version

```bash
cat COG-VERSION
# or ask any agent: "What version of COG am I running?"
```

## Getting Help

- **Issues:** https://github.com/huytieu/COG-second-brain/issues
- **Discussions:** https://github.com/huytieu/COG-second-brain/discussions
- **Updates:** Watch the repo for improvements

## Next Steps

Once you're comfortable:

1. ✅ Use COG daily for 2 weeks to build the habit
2. ✅ Customize skills to match your workflow
3. ✅ Set up Git backup to your own GitHub
4. ✅ Try iCloud sync for multi-device access
5. ✅ Explore knowledge consolidation features
6. ✅ Share your improvements with the community

---

**Welcome to COG!** Your agentic second brain is ready to learn and evolve with you—powered by whichever AI agent you choose.
