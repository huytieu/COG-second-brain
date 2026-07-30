---
name: loop-engineering
description: Shared loop-engineering reference for COG skills - the agent loop, deterministic verifiers, termination conditions, in-loop context management, and named patterns. Invoke when designing or debugging a skill that iterates (search-verify-retry, scan-until-dry, fetch-retry-gate).
---

Read `.claude/skills/loop-engineering/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
