# Publishing COG to Marketplaces & Directories

This guide covers packaging metadata, platform-specific requirements, and release checks for publishing COG across all supported directories.

## Supported Platforms

| Platform | Listing method | Status |
|---|---|---|
| **skills.sh** (Vercel) | Auto-detected via `npx skills add huytieu/COG-second-brain` | Ready — `.claude/skills/*/SKILL.md` files have required frontmatter |
| **agentskill.sh** | Submit repo URL at agentskill.sh/submit | Ready — SKILL.md files auto-indexed |
| **cursor.directory** | Submit at cursor.directory/plugins/new | Ready — `.cursor-plugin/plugin.json` + `.cursorrules` shipped |
| **Claude Code Marketplace** | `.claude-plugin/plugin.json` + `marketplace-entry.json` | Ready — canonical manifest shipped |
| **GitHub** | Repository topics and description | Ready — topics set via `gh` |

## Packaged Metadata

COG ships marketplace metadata in multiple formats:

| File | Platform | Purpose |
|---|---|---|
| `.claude-plugin/plugin.json` | Claude Code marketplace | Canonical skill manifest (33 skills, 10 agents) |
| `.cursor-plugin/plugin.json` | cursor.directory | Cursor-compatible manifest |
| `.cursorrules` | Cursor | Editor rules for Cursor users |
| `marketplace-entry.json` | General marketplaces | Lightweight catalog entry |
| `AGENTS.md` | Universal | Command reference for any markdown-reading agent |

Current packaged version: **3.8.1**

## Surface Model

COG is a **multi-agent package**, not a single-surface plugin:

| Surface | Coverage |
|---|---:|
| Claude Code (`.claude/skills/`) | 33 native skills + 10 agents (6 workers + 4 verifiers) |
| Cursor (`.cursor-plugin/`) | Plugin manifest + rules |
| Universal docs (`AGENTS.md`) | 33+ documented commands |
| Kiro (`.kiro/powers/`) | 7 core powers |
| Gemini CLI (`.gemini/commands/`) | 7 core commands |

For the detailed contract, see [`docs/AGENT-SUPPORT.md`](../docs/AGENT-SUPPORT.md).

## SEO/GEO Keywords

These keywords are set across all manifests and the GitHub repo for discoverability:

`second-brain`, `garry-tan`, `gstack`, `gbrain`, `ai-agents`, `obsidian`, `claude-code`, `cursor`, `kiro`, `gemini-cli`, `codex`, `worker-agents`, `people-crm`, `knowledge-management`, `specialist-sessions`, `agentic`, `self-evolving`, `loop-engineering`, `productivity`, `v-model`, `closed-loop`, `verification-harness`, `evidence-ledger`, `ultragoal`, `risk-lanes`, `verifier-agents`

## Before You Publish

Run the packaging validator from the repo root:

```bash
./scripts/validate-agent-surface.sh
```

Also validate Cursor manifest:
```bash
python3 -m json.tool .cursor-plugin/plugin.json > /dev/null
```

## Installation Guidance for Marketplace Descriptions

Preferred install flow:

```bash
git clone https://github.com/huytieu/COG-second-brain.git
cd COG-second-brain
# Open in Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex, or another AGENTS-compatible agent
```

Skills.sh install:
```bash
npx skills add huytieu/COG-second-brain
```

Do **not** describe installation as copying only `.claude/` into another folder — COG is a full vault/repo layout, not just a loose skill pack.

## Release Checklist

1. Bump `COG-VERSION`
2. Update `.claude-plugin/plugin.json` (version + any new skills/agents)
3. Update `.cursor-plugin/plugin.json` (version + skills list)
4. Update `marketplace-entry.json` (version)
5. Update `CHANGELOG.md`
6. Add any new framework files to `FRAMEWORK_FILES` in `cog-update.sh`
7. Run `./scripts/validate-agent-surface.sh`
8. Update GitHub repo topics if keywords changed
9. Smoke test onboarding from a clean clone
10. Update `.github/MARKETPLACE.md` "Current packaged version"
11. Cut a GitHub Release tagged `vX.Y.Z` with the CHANGELOG section as the body
12. Re-index the directories: skills.sh and agentskill.sh pull from the repo automatically; cursor.directory may need a resubmit if the manifest shape changed

## Support Links

- Issues: https://github.com/huytieu/COG-second-brain/issues
- Discussions: https://github.com/huytieu/COG-second-brain/discussions
- Setup guide: https://github.com/huytieu/COG-second-brain/blob/main/SETUP.md
