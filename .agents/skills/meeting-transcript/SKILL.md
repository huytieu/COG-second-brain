---
name: meeting-transcript
description: Process meeting recordings and notes into structured decisions, action items, and team dynamics with intelligent noise filtering
---

Read `.claude/skills/meeting-transcript/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
