---
name: comprehensive-analysis
description: Deep-dive 7-day analysis across all data sources for weekly reviews, board prep, and strategic planning
---

Read `.claude/skills/comprehensive-analysis/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
