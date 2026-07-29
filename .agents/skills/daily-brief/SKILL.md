---
name: daily-brief
description: Generate personalized news intelligence with verified sources (7-day freshness requirement)
---

Read `.claude/skills/daily-brief/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
