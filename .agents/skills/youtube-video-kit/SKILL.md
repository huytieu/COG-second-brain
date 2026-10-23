---
name: youtube-video-kit
description: YouTube packaging: thumbnail, animated opening title, ElevenLabs music bed, and the upload metadata bundle
---

Read `.claude/skills/youtube-video-kit/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
