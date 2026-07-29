---
name: review-cockpit
description: Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any "do X, then plan/draft Y and Z"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses.
---

Read `.claude/skills/review-cockpit/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
