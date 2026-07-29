---
name: generate-release-notes
description: Generate categorized release notes from any source (GitHub, Linear, Jira, or manual input) with optional publishing
---

Read `.claude/skills/generate-release-notes/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
