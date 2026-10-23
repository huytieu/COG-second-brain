---
name: blog-publish
description: Write and publish a post to your own static blog: TL;DR, ASCII art, markdown twin for agents, deploy, and social distribution
---

Read `.claude/skills/blog-publish/SKILL.md` and execute it exactly as written; that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
