---
name: retro
description: CP-7 retrospective: audit checkpoints, evidence quality, action items, and harvest candidates. Closes the V-model cycle and feeds the next run. Use via /retro after ship, escalate, or significant session.
---

Read `.claude/skills/retro/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
