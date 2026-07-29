---
name: team-brief
description: Generate daily team intelligence brief by cross-referencing GitHub, Linear, Slack, PostHog, meetings, and braindumps with two-way Linear sync-back
---

Read `.claude/skills/team-brief/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
