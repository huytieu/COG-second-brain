# COG Setup Guide

Complete step-by-step instructions for setting up your COG (Claude + Obsidian + Git) second brain system.

## Prerequisites

Before you begin, ensure you have:

1. **Obsidian** installed ([Download here](https://obsidian.md/))
2. **Claude Code** or VSCode with Claude extension ([Download here](https://claude.ai/download))
3. **Git** (optional but recommended) - Check if installed: `git --version`
4. **iCloud Drive** (optional, for multi-device sync on Apple devices)

## Installation Methods

### Method 1: Quick Setup (Recommended)

1. **Clone COG into your Obsidian vault:**
   ```bash
   cd /path/to/your/obsidian-vault
   git clone https://github.com/huytieu/COG-second-brain.git
   cd COG-second-brain
   ```

2. **Copy COG structure to your vault root:**
   ```bash
   # Copy Claude configuration
   cp -r .claude ../

   # Copy templates
   cp -r templates ../06-templates

   # Copy example vault structure
   cp -r example-vault/* ../
   ```

3. **Open your vault in Obsidian:**
   - Launch Obsidian
   - Open your vault (or create new vault first)
   - You should now see the COG directory structure

4. **Configure Claude Code:**
   ```bash
   # In your vault root directory
   code .
   ```

   - In Claude Code, test the setup: Type `/braindump`
   - If command is recognized, COG is working!

### Method 2: Manual Setup

If you prefer to understand each step:

#### Step 1: Create Directory Structure

In your Obsidian vault, create these folders:

```bash
mkdir -p 00-inbox
mkdir -p 01-daily/briefs
mkdir -p 01-daily/checkins
mkdir -p 02-personal/braindumps
mkdir -p 02-personal/development
mkdir -p 02-personal/wellness
mkdir -p 03-professional/braindumps
mkdir -p 03-professional/leadership
mkdir -p 03-professional/strategy
mkdir -p 03-professional/skills
mkdir -p 04-projects
mkdir -p 05-knowledge/consolidated
mkdir -p 05-knowledge/patterns
mkdir -p 05-knowledge/timeline
mkdir -p 06-templates
```

#### Step 2: Set Up Claude Commands

1. Create `.claude` directory in your vault root:
   ```bash
   mkdir -p .claude/commands
   mkdir -p .claude/subagents
   ```

2. Download command files from the COG repository:
   - Navigate to https://github.com/huytieu/COG-second-brain/.claude/commands/
   - Download each `.md` file to your `.claude/commands/` folder

#### Step 3: Set Up Templates

1. Download template files from repository
2. Place them in `06-templates/` folder in your vault

#### Step 4: Test Your Setup

1. Open Claude Code in your vault directory:
   ```bash
   cd /path/to/your/vault
   code .
   ```

2. Try a command:
   ```
   /braindump
   ```

3. If it works, you're ready to go!

## Configuration

### Customizing Your Interests

Edit `.claude/commands/daily-brief.md` to customize your interest areas for news curation.

### Adding Projects

When starting a new project:

1. Create project folder:
   ```bash
   mkdir -p 04-projects/your-project-name/{braindumps,competitive,content,planning}
   ```

2. Projects will be automatically detected by COG commands

### Setting Up Git (Optional but Recommended)

1. Initialize git in your vault:
   ```bash
   cd /path/to/your/vault
   git init
   ```

2. Create `.gitignore`:
   ```bash
   echo ".obsidian/workspace*" >> .gitignore
   echo ".obsidian/cache" >> .gitignore
   echo ".trash/" >> .gitignore
   echo "*.tmp" >> .gitignore
   ```

3. Make your first commit:
   ```bash
   git add .
   git commit -m "Initial COG setup"
   ```

4. (Optional) Connect to GitHub for backup:
   ```bash
   git remote add origin https://github.com/yourusername/your-vault.git
   git branch -M main
   git push -u origin main
   ```

### Setting Up iCloud Sync (Apple Devices)

1. Move your Obsidian vault to iCloud Drive:
   ```bash
   mv /path/to/your/vault ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/
   ```

2. Open Obsidian and point it to the new location

3. Install Obsidian Mobile on iPhone/iPad

4. Open the same vault - it will sync automatically via iCloud

## First Use Workflow

### Day 1: Set Up Your Profile

1. **Create your first braindump:**
   ```
   /braindump
   ```

   Paste this to get started:
   ```
   I'm setting up COG to help me with:
   - [Your main goals]
   - [Your current projects]
   - [Your areas of interest]
   - [What you want to track]
   ```

2. **Test daily brief:**
   ```
   /daily-brief
   ```

   This will generate your first intelligence briefing based on your braindump

### Week 1: Build the Habit

Use these commands daily:
- Morning: `/daily-brief` for intelligence
- Throughout day: `/braindump` for capturing thoughts
- Evening: Quick review of your braindumps

### Week 2: Start Consolidating

After a week of braindumps:
- Run `/weekly-checkin` for pattern analysis
- Try `/consolidate-knowledge` to build frameworks

## Troubleshooting

### Command Not Recognized

**Problem**: Typing `/braindump` shows "command not found"

**Solutions**:
1. Ensure `.claude/commands/` folder exists in vault root
2. Check that command files are `.md` format
3. Restart Claude Code
4. Verify you're in the correct vault directory

### Files Saving to Wrong Location

**Problem**: COG creates files in unexpected directories

**Solutions**:
1. Ensure all required directories exist (see directory structure above)
2. Check that you're running commands from vault root
3. Verify directory structure matches COG expectations

### iCloud Sync Not Working

**Problem**: Changes don't sync across devices

**Solutions**:
1. Check iCloud Drive is enabled in System Settings
2. Ensure Obsidian mobile is pointing to same vault
3. Wait a few minutes - iCloud can be slow
4. Check available iCloud storage space

### Git Conflicts

**Problem**: Git shows merge conflicts

**Solutions**:
1. COG files are markdown - conflicts are easy to resolve
2. Open conflicted file in text editor
3. Look for `<<<<<<` and `>>>>>>` markers
4. Keep the version you want, remove conflict markers
5. Commit the resolved file

## Advanced Configuration

### Customizing Commands

1. Edit any `.claude/commands/*.md` file
2. Modify the prompts to match your workflow
3. Save and test the changes

Example: Customize `/braindump` to always ask specific questions:
```markdown
# Brain Dump Command

## Purpose
[Your custom description]

## Command: `/braindump`

## Custom Questions
Always ask the user:
1. What domain is this? (personal/professional/project)
2. What energy level? (high/medium/low)
3. Any urgent actions?

[Rest of command]
```

### Creating New Commands

1. Create new file in `.claude/commands/`:
   ```bash
   touch .claude/commands/my-custom-command.md
   ```

2. Add command definition:
   ```markdown
   # My Custom Command

   ## Purpose
   What this command does

   ## Command: `/my-custom-command`

   ## Process
   1. Step 1
   2. Step 2

   [Your custom prompt]
   ```

3. Test it in Claude Code:
   ```
   /my-custom-command
   ```

### Adding Specialized Agents

Create custom subagents for specific tasks:

1. Create file in `.claude/subagents/`:
   ```bash
   touch .claude/subagents/my-agent.md
   ```

2. Define agent purpose and process
3. Reference agent in command files

## Daily Workflow Examples

### Morning Routine (5 minutes)
```bash
/daily-brief
# Review the intelligence
# Note any actions needed
```

### Throughout Day
```bash
/braindump
# Capture any thoughts, ideas, insights
# No structure needed - just dump it
```

### Weekly Review (30 minutes)
```bash
/weekly-checkin
# Reflect on the week
# Identify patterns
# Plan next week
```

### Monthly Consolidation (1 hour)
```bash
/consolidate-knowledge
# Build frameworks from insights
# Update knowledge base
# Archive processed content
```

## Getting Help

- **Issues**: https://github.com/huytieu/COG-second-brain/issues
- **Discussions**: https://github.com/huytieu/COG-second-brain/discussions
- **Documentation**: https://github.com/huytieu/COG-second-brain/wiki

## Next Steps

Once you're comfortable with the basics:

1. Explore advanced commands (see README.md)
2. Customize templates for your workflow
3. Add new projects and tracking areas
4. Experiment with knowledge consolidation
5. Share your improvements with the community!

---

**Welcome to COG!** Your second brain is now ready to learn and evolve with you.
