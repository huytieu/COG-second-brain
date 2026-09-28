---
name: release-video
description: Turn a product release (the list of shipped items plus real screen recordings) into a motion recap video and one explained demo per feature, with sound effects tied to on-screen motion and a composed music bed. Use when asked for a release video, a changelog video, a feature recap reel, or demo clips for release notes and docs.
---

Read `.claude/skills/release-video/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
