---
name: closed-loop
description: V-model execute: CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify (full) → CP-5 acceptance. Worker never grades its own homework; evidence rows trace back to AC-n. Use via /execute.
---

Read `.claude/skills/closed-loop/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
