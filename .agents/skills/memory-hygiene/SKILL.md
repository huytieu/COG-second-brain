---
name: memory-hygiene
description: Periodic trust sweep of persistent memory and durable knowledge notes - re-verifies environment-dependent claims against the live environment, stamps last_verified + confidence, and proposes archiving drifted entries
---

Read `.claude/skills/memory-hygiene/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
