---
name: create-user-story
description: Create user stories with duplicate checking across any project tracker (Linear, GitHub Issues, Jira)
---

Read `.claude/skills/create-user-story/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
