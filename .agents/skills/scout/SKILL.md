---
name: scout
description: Evaluate URLs and tools — check vault coverage, assess relevance, recommend save or skip
---

Read `.claude/skills/scout/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
