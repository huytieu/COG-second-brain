---
name: publish-to-confluence
description: Publish any markdown file from the vault to Confluence with format conversion and approval gate
---

Read `.claude/skills/publish-to-confluence/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
