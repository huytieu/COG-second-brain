---
name: generate-prd
description: Generate product requirements documents with optional publishing to Confluence or other wiki platforms
---

Read `.claude/skills/generate-prd/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
