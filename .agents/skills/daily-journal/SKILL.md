---
name: daily-journal
description: A passive daily work journal that Claude keeps FOR you so you never have to write it yourself. Append short entries after meaningful work (what was done, what you focused on, artifacts touched) to 01-daily/journal/YYYY-MM-DD.md. Run a guided reflection at night or in the morning. Use when you run /daily-journal, say "log this to my journal", "add to today's journal", "reflect on today/yesterday", or when finishing a meaningful chunk of work in any session.
---

Read `.claude/skills/daily-journal/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
