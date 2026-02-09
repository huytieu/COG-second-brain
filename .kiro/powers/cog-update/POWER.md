---
name: "cog-update"
displayName: "COG Update"
description: "Check for and apply upstream COG framework updates without touching personal content"
keywords: ["update COG", "check updates", "new version", "upgrade COG", "latest COG", "update skills"]
---

# COG Update Power

Check for and apply upstream COG framework updates (skills, docs, scripts) without touching your personal content.

## When This Power Activates

- User mentions "update COG", "check for updates", or "upgrade"
- User asks about their COG version or wants new features
- User wants the latest skills or documentation

## Update Steps

### 1. Check Current Version
Read `COG-VERSION` in the vault root to determine the local version.

### 2. Fetch Upstream
```bash
git remote get-url cog-upstream 2>/dev/null || \
  git remote add cog-upstream https://github.com/huytieu/COG-second-brain.git
git fetch cog-upstream main --quiet
```

### 3. Compare Versions
```bash
cat COG-VERSION                           # local
git show cog-upstream/main:COG-VERSION    # upstream
```

If versions match, report that everything is up to date.

### 4. Review Changed Files
Compare each framework file (skills, docs, scripts) against upstream. Framework files are safe to update — they never contain user content.

For each changed file, offer the user:
- **Update**: Replace with upstream version
- **Skip**: Keep the current local version
- **Backup + update**: Save a `.backup-YYYYMMDD` copy, then update

### 5. Apply Updates
```bash
git checkout cog-upstream/main -- <file>
```

### 6. Summarize
Report the new version, list updated files, and suggest committing:
```
git add -A && git commit -m "Update COG framework to v<version>"
```

## Shell Script Alternative
Users can also update without an AI agent:
```bash
./cog-update.sh           # Interactive
./cog-update.sh --check   # Check only
./cog-update.sh --dry-run # Preview
./cog-update.sh --force   # Update all
```

## Safety
- Content folders (`00-inbox/`, `01-daily/`, `02-personal/`, etc.) are NEVER touched
- Uses surgical `git checkout` — no merge conflicts possible
- Backs up customized files before overwriting
