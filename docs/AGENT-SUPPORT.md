# COG Agent Support Matrix

COG intentionally ships multiple agent surfaces. They do not all use the same packaging format, but every surface must describe its actual coverage truthfully.

This document is the packaging contract for contributors and maintainers: which surfaces are complete, which are intentionally partial, and what must stay in sync before publishing a release.

## Current Support Matrix

| Surface | Shipped format | Coverage | Status |
|---|---|---:|---|
| Claude Code | `.claude/skills/*/SKILL.md` + `.claude/agents/*.md` | 33 skills + 10 agents | Full authoritative surface |
| Antigravity | `.agents/skills/*/SKILL.md` + `.agents/agents/*.md` | 33 skills + 10 agents | Full pointer-stub surface; delegates to `.claude/` |
| Cursor | `.cursor-plugin/plugin.json` + `.cursorrules` | 33 skills + 10 agents | Full packaged metadata/rules surface |
| [Agent Plugins](https://agent-plugins.org) standard | Root `plugin.json` + generated `skills/` | 33 skills | Spec 1.0.0 standard surface |
| Universal agent docs | `AGENTS.md` | 33 commands | Full documented fallback |
| Kiro | `.kiro/powers/*/POWER.md` | 7 powers | Core workflows only |
| Gemini CLI | `.gemini/commands/*.toml` + `.gemini/skills/*.md` | 7 commands | Core workflows only |

## Full vs Core Surfaces

### Full surfaces

The complete public skill set is the 33 directories currently shipped under `.claude/skills/`. That directory is authoritative for skill names and playbook content.

The full surfaces are:
- Claude Code: authoritative skill and agent definitions
- Antigravity: complete pointer stubs for every Claude skill and agent
- Cursor: complete skill and agent declarations in the plugin manifest, with `.cursorrules` for operating guidance
- Agent Plugins: generated root `skills/` mirror for standard-aware clients
- `AGENTS.md`: documented fallback for the complete skill set

Do not maintain a separate hand-written skill-name list here. The validator compares the packaged surfaces to `.claude/skills/` so additions and removals cannot silently leave this contract behind.

### Core surfaces

Kiro and Gemini CLI intentionally expose seven common personal workflows:
- `onboarding`
- `braindump`
- `daily-brief`
- `weekly-checkin`
- `knowledge-consolidation`
- `url-dump`
- `update-cog`

## Packaging Rules

If you add, remove, rename, or materially change a public COG skill or agent:

1. Update the authoritative Claude definition under `.claude/`
2. Update the matching Antigravity pointer stub under `.agents/`
3. Update `AGENTS.md` for the universal command surface when a public skill changes
4. Update `.claude-plugin/plugin.json` so its skill manifest stays exact
5. Update `.cursor-plugin/plugin.json` so its skills and agents stay exact
6. Run `./scripts/build-agent-plugin.sh` after Claude skill changes so root `skills/` stays identical to `.claude/skills/`
7. Update Kiro or Gemini files only when that workflow belongs to their intentionally smaller core surface
8. Add every new framework file to `FRAMEWORK_FILES` in `cog-update.sh`
9. Update README, SETUP, marketplace docs, and this file when counts or support claims change
10. Run `./scripts/validate-agent-surface.sh`

## Validation

Run this before tagging a release, opening a packaging PR, or after using `./cog-update.sh`:

```bash
./scripts/validate-agent-surface.sh
```

The validator checks:
- JSON validity for Claude, Cursor, general marketplace, and Agent Plugins manifests
- Agent Plugins schema declaration and exact root `skills/` mirror parity
- exact Claude vs Antigravity skill and agent parity
- Antigravity pointer-stub source paths and required delegation substitutions
- exact Claude vs Cursor skill names, skill paths, and agent names
- duplicate manifest entries
- `AGENTS.md` coverage for all Claude skills
- `FRAMEWORK_FILES` coverage for shipped Claude and Antigravity surfaces
- version alignment across package manifests, `COG-VERSION`, and `.github/MARKETPLACE.md`
- common packaging drift such as `agents.md` vs `AGENTS.md`

## Safe Update Workflow

Recommended maintainer flow:

```bash
./cog-update.sh --check
./cog-update.sh
./scripts/validate-agent-surface.sh
```

The updater compares both file content and Git executable mode. If you have local framework customizations, use interactive mode so you can inspect or back up individual files before replacement.
