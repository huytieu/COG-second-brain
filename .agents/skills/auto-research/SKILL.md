---
name: auto-research
description: Deep strategic research engine — decomposes questions into parallel research threads, spawns multiple agents, and synthesizes into actionable strategic analysis
---

Read `.claude/skills/auto-research/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
