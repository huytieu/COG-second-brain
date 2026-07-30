---
name: onboarding
description: Personalize COG for your workflow - creates profile, interests, and watchlist files with guided setup (run this first!)
---

Read `.claude/skills/onboarding/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
