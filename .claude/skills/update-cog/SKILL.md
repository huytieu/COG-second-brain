---
name: update-cog
description: Check for and apply upstream COG framework updates (skills, docs, scripts) without touching personal content
---

# COG Update Skill

## Purpose
Help the user update their COG framework files (skills, documentation, scripts) from the official upstream repository without risking their personal content (braindumps, profiles, notes).

## When to Invoke
- User asks to "update COG", "check for updates", or "get latest COG version"
- User mentions wanting new skills or features from upstream
- User asks about their COG version

## Process Flow

### 1. Check Current Version
Read `COG-VERSION` from the vault root. If it doesn't exist, inform the user they may be on an older version that predates version tracking.

### 2. Ensure Upstream Remote
```bash
# Add the upstream remote if not already present
git remote get-url cog-upstream 2>/dev/null || \
  git remote add cog-upstream https://github.com/huytieu/COG-second-brain.git

# Fetch latest
git fetch cog-upstream main --quiet
```

### 3. Compare Versions
```bash
# Local version
cat COG-VERSION

# Upstream version
git show cog-upstream/main:COG-VERSION
```

If versions match, tell the user they're up to date.

### 4. Show What Changed
For each framework file, compare local vs upstream:
```bash
git diff HEAD..cog-upstream/main -- <file>
```

**Framework files** (safe to update — never contain user content):
- Core docs: `README.md`, `SETUP.md`, `AGENTS.md`, `GEMINI.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
- Skills: `.claude/skills/*/SKILL.md`
- Powers: `.kiro/powers/*/POWER.md`
- Gemini: `.gemini/commands/*.toml`, `.gemini/skills/*.md`
- Config: `.claude-plugin/plugin.json`, `marketplace-entry.json`, `.gitignore`
- Scripts: `cog-update.sh`
- Version: `COG-VERSION`

### 5. Detect Customizations
Before updating, check if the user has customized any framework files:
```bash
# Compare user's file against the version they originally got
git diff cog-upstream/main -- <file>
```

If a file has local customizations, warn the user and offer options:
- **Keep yours**: Skip this file
- **Use upstream**: Overwrite with the new version
- **Backup + update**: Save current as `<file>.backup-YYYYMMDD` then update

### 6. Apply Updates
For files the user approves:
```bash
# Surgical file replacement — no merge, no rebase, zero conflict risk
git checkout cog-upstream/main -- <file>
```

### 7. Verify & Summarize
After updating:
- Show the new version number
- List all files that were updated
- List any files the user chose to skip
- Suggest committing the update:
  ```
  git add -A && git commit -m "Update COG framework to v<new-version>"
  ```

## Alternative: Shell Script
For users who prefer a non-AI update, mention the update script:
```bash
./cog-update.sh           # Interactive
./cog-update.sh --check   # Just check for updates
./cog-update.sh --dry-run # Preview changes
./cog-update.sh --force   # Update everything
```

## Important Notes
- **Content folders are NEVER touched**: `00-inbox/`, `01-daily/`, `02-personal/`, `03-professional/`, `04-projects/`, `05-knowledge/`, `06-templates/` contain user data and are always ignored
- **The .gitignore is designed** so content folders are excluded from upstream tracking (only `.gitkeep` files are tracked)
- **The update script updates itself** — `cog-update.sh` is in the framework file list
- **No merge conflicts possible** — this uses `git checkout` for surgical file replacement, not `git merge` or `git rebase`
