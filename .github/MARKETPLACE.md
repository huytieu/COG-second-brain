# Publishing COG to Marketplaces & Directories

This guide covers packaging metadata, platform-specific requirements, and release checks for publishing COG across all supported directories.

## Supported Platforms

| Platform | Listing method | Status |
|---|---|---|
| **Agent Plugins** | Root `plugin.json` + generated `skills/` | Ready: spec 1.0.0 surface shipped |
| **skills.sh** (Vercel) | Auto-detected via `npx skills add huytieu/COG-second-brain` | Ready: skill frontmatter shipped |
| **agentskill.sh** | Submit repo URL at agentskill.sh/submit | Ready: SKILL.md files auto-indexed |
| **cursor.directory** | Submit at cursor.directory/plugins/new | Ready: `.cursor-plugin/plugin.json` + `.cursorrules` shipped |
| **Claude Code Marketplace** | `.claude-plugin/plugin.json` + `marketplace-entry.json` | Ready: canonical manifest shipped |
| **GitHub** | Repository topics and description | Ready |

## Packaged Metadata

COG ships marketplace metadata in multiple formats:

| File | Platform | Purpose |
|---|---|---|
| `plugin.json` | Agent Plugins standard | Root spec 1.0.0 manifest |
| `skills/` | Agent Plugins standard | Generated mirror of all 33 Claude skills |
| `.claude-plugin/plugin.json` | Claude Code marketplace | 33-skill packaged manifest |
| `.cursor-plugin/plugin.json` | cursor.directory | 33 skills + 10 agents |
| `.cursorrules` | Cursor | Cursor operating guidance |
| `marketplace-entry.json` | General marketplaces | Lightweight catalog entry |
| `AGENTS.md` | Universal | 33-command reference for markdown-reading agents |

Current packaged version: **3.10.1**

## Surface Model

COG is a multi-agent package with several distribution surfaces:

| Surface | Coverage |
|---|---:|
| Claude Code (`.claude/`) | 33 native skills + 10 agents |
| Antigravity (`.agents/`) | 33 skill stubs + 10 agent stubs |
| Cursor (`.cursor-plugin/` + `.cursorrules`) | 33 skills + 10 agents |
| Agent Plugins (`plugin.json` + `skills/`) | 33 skills |
| Universal docs (`AGENTS.md`) | 33 documented commands |
| Kiro (`.kiro/powers/`) | 7 core powers |
| Gemini CLI (`.gemini/commands/`) | 7 core commands |

For the detailed contract, see [`docs/AGENT-SUPPORT.md`](../docs/AGENT-SUPPORT.md).

## SEO/GEO Keywords

These keywords are set across manifests and repository metadata where supported:

`second-brain`, `garry-tan`, `gstack`, `gbrain`, `ai-agents`, `obsidian`, `claude-code`, `antigravity`, `cursor`, `kiro`, `gemini-cli`, `codex`, `worker-agents`, `people-crm`, `knowledge-management`, `specialist-sessions`, `agentic`, `self-evolving`, `loop-engineering`, `productivity`, `v-model`, `closed-loop`, `verification-harness`, `evidence-ledger`, `ultragoal`, `risk-lanes`, `verifier-agents`, `agent-plugins`

## Before You Publish

Run the framework validator from the repo root:

```bash
./scripts/validate-agent-surface.sh
```

The validator includes Claude, Antigravity, Cursor, Agent Plugins mirror parity, updater coverage, and packaged-version consistency checks. Do not duplicate those checks manually unless diagnosing a validator failure.

After any Claude skill change, regenerate the Agent Plugins mirror before validation:

```bash
./scripts/build-agent-plugin.sh
./scripts/validate-agent-surface.sh
```

## Installation Guidance for Marketplace Descriptions

Preferred full-repository install flow:

```bash
git clone https://github.com/huytieu/COG-second-brain.git
cd COG-second-brain
# Open in Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex, or another compatible agent
```

Skills.sh install:

```bash
npx skills add huytieu/COG-second-brain
```

Do not describe installation as copying only `.claude/` into another folder. COG is a full vault/repository layout with shared documentation, update tooling, and multiple packaged surfaces.

## Release Checklist

1. Bump `COG-VERSION`
2. Update `.claude-plugin/plugin.json` version and any skill metadata changes
3. Update `.cursor-plugin/plugin.json` version plus skills/agents when changed
4. Update root `plugin.json` version
5. Update `marketplace-entry.json` version
6. Update this file's `Current packaged version` line
7. Update `CHANGELOG.md`
8. Add any new framework files to `FRAMEWORK_FILES` in `cog-update.sh`
9. Regenerate root `skills/` if Claude skills changed
10. Run `./scripts/validate-agent-surface.sh`
11. Update GitHub repository topics if keywords changed
12. Smoke test onboarding from a clean clone
13. Cut a GitHub Release tagged `vX.Y.Z` with the matching CHANGELOG section
14. Re-index directories as required; cursor.directory may need a resubmit when its manifest shape changes

## Support Links

- Issues: https://github.com/huytieu/COG-second-brain/issues
- Discussions: https://github.com/huytieu/COG-second-brain/discussions
- Setup guide: https://github.com/huytieu/COG-second-brain/blob/main/SETUP.md
