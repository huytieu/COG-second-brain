---
name: terminal-replica
description: Reproduce your real terminal and CLI agents (Claude Code, Codex, Gemini CLI) faithfully in graphics and video frames
---

Read `.claude/skills/terminal-replica/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
