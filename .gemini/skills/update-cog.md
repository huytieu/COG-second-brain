# COG Update Playbook

## Goal
Update COG framework files (skills, docs, scripts) from the official upstream repo without touching personal content.

## Pre-Flight
1. Read `COG-VERSION` for the current local version
2. If no version file exists, inform the user they may be on a pre-3.2.0 version

## Steps

### 1. Ensure Upstream Remote
```bash
git remote get-url cog-upstream 2>/dev/null || \
  git remote add cog-upstream https://github.com/huytieu/COG-second-brain.git
git fetch cog-upstream main --quiet
```

### 2. Compare Versions
```bash
cat COG-VERSION                           # local
git show cog-upstream/main:COG-VERSION    # upstream
```

If versions match, tell the user everything is up to date. Done.

### 3. Identify Changed Framework Files
Compare each framework file against upstream:
- Core docs: `README.md`, `SETUP.md`, `AGENTS.md`, `GEMINI.md`, `CHANGELOG.md`, `CONTRIBUTING.md`
- Skills: `.claude/skills/*/SKILL.md`, `.kiro/powers/*/POWER.md`
- Gemini: `.gemini/commands/*.toml`, `.gemini/skills/*.md`
- Config: `.claude-plugin/plugin.json`, `marketplace-entry.json`, `.gitignore`
- Scripts: `cog-update.sh`, `COG-VERSION`

### 4. For Each Changed File
Ask the user:
- **Update** — replace with upstream version
- **Skip** — keep current version
- **Backup + update** — save `.backup-YYYYMMDD` copy, then replace

### 5. Apply Updates
```bash
git checkout cog-upstream/main -- <file>
```

### 6. Summary
Show:
- New version number
- Files updated
- Files skipped
- Suggested commit command

## Shell Script Alternative
```bash
./cog-update.sh           # Interactive
./cog-update.sh --check   # Check for updates
./cog-update.sh --dry-run # Preview changes
./cog-update.sh --force   # Update all without prompting
```

## Safety Guarantees
- Content folders (`00-inbox/`, `01-daily/`, `02-personal/`, `03-professional/`, `04-projects/`, `05-knowledge/`, `06-templates/`) are NEVER modified
- Uses `git checkout` for surgical file replacement — no merge, no rebase, zero conflict risk
- The update script itself is a framework file and self-updates
