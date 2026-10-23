---
name: release-comms
description: Turn a deployment runsheet and a GitHub milestone into a customer release note with real media, docs updates, and a Slack announcement draft
---

Read `.claude/skills/release-comms/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
