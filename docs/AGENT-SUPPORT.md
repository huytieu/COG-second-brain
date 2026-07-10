# COG Agent Support Matrix

COG intentionally ships **multiple agent surfaces**. They are not all identical.

This document is the packaging contract: it tells contributors and maintainers which surfaces are first-class today, which ones are partial, and what must stay in sync before publishing a release.

## Current Support Matrix

| Surface | Shipped format | Coverage | Status |
|---|---|---:|---|
| Claude Code | `.claude/skills/*/SKILL.md` | 21 skills | Full native surface |
| Universal agent docs | `AGENTS.md` | 17 commands | Full documented fallback |
| Kiro | `.kiro/powers/*/POWER.md` | 7 powers | Core workflows only |
| Gemini CLI | `.gemini/commands/*.toml` + `.gemini/skills/*.md` | 7 commands | Core workflows only |

## What “Full” vs “Core” Means

### Full surfaces
These surfaces should expose the complete public COG command set:
- `onboarding`
- `braindump`
- `daily-brief`
- `weekly-checkin`
- `knowledge-consolidation`
- `url-dump`
- `team-brief`
- `meeting-transcript`
- `comprehensive-analysis`
- `update-cog`
- `auto-research`
- `create-user-story`
- `generate-prd`
- `generate-release-notes`
- `export-open-issues`
- `publish-to-confluence`
- `update-knowledge-base`

Today, **Claude Code** and **`AGENTS.md`** are the full surfaces.

### Core surfaces
These surfaces intentionally cover the most common personal workflows first:
- `onboarding`
- `braindump`
- `daily-brief`
- `weekly-checkin`
- `knowledge-consolidation`
- `url-dump`
- `update-cog`

Today, **Kiro** and **Gemini CLI** are core surfaces.

## Packaging Rules

If you add, remove, rename, or materially change a public COG skill:

1. Update the **Claude skill** in `.claude/skills/`
2. Update **`AGENTS.md`** for the universal surface
3. Update **`.claude-plugin/plugin.json`** so marketplace metadata stays truthful
4. Update **README / SETUP / this file** if counts or support levels change
5. If the skill is supported natively in Kiro or Gemini, update those files too
6. Add new framework files to `FRAMEWORK_FILES` in `cog-update.sh`
7. Run `./scripts/validate-agent-surface.sh`

## Validation

Run this before tagging a release, opening a packaging PR, or after using `./cog-update.sh`:

```bash
./scripts/validate-agent-surface.sh
```

The validator checks:
- manifest JSON validity
- declared skill paths in `.claude-plugin/plugin.json`
- plugin skill count vs actual shipped Claude skills
- `AGENTS.md` coverage for all manifest skills
- common packaging drift like `agents.md` vs `AGENTS.md`

## Safe Update Workflow

Recommended maintainer flow:

```bash
./cog-update.sh --check
./cog-update.sh
./scripts/validate-agent-surface.sh
```

If you have local framework customizations, prefer interactive update mode so you can backup per-file before replacing anything.
