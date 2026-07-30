---
name: update-knowledge-base
description: Maintain and update product knowledge base from releases, features, and project changes with optional wiki sync
---

Read `.claude/skills/update-knowledge-base/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
