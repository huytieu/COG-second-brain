---
name: social-media-kit
description: Attach native media (teaser video, GIF, card images) to every social post, with per-platform upload steps
---

Read `.claude/skills/social-media-kit/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
