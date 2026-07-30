---
description: COG framework operating policy
---

Read `CLAUDE.md` at the repository root and treat every section marked
`ALWAYS APPLY` / `MUST APPLY` as binding.

Antigravity substitutions:
- `.claude/skills/<name>/SKILL.md` → read that path directly; it is authoritative.
- `.claude/agents/<name>.md` workers → `.agents/agents/<name>.md`, invoked via `invoke_subagent`.
- Model Routing table: `sonnet` → `model: flash`; the lead/orchestrator role is this session.
