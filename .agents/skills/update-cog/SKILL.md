---
name: update-cog
description: Check for and apply upstream COG framework updates (skills, docs, scripts) without touching personal content
---

Read `.claude/skills/update-cog/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
