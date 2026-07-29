---
name: content-factory
description: Autonomous content pipeline - scout announcements in your field, triage by trend momentum and personal angle, produce posts/blogs/videos in your voice with ledger-based dedup, hard volume caps, and screenshot-verified publishing
---

Read `.claude/skills/content-factory/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
