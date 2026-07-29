---
name: harvest
description: Capture durable session learnings, stage for human promotion to 05-knowledge/lizard, and propose skill/CLAUDE.md patches. Triggered by /harvest, SessionEnd hook staging, or nightly enhance. Never writes durable knowledge without your approval.
---

Read `.claude/skills/harvest/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
