---
name: export-open-issues
description: Audit and export open issues from any project tracker with summary analysis and vault archival
---

Read `.claude/skills/export-open-issues/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
