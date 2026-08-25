---
name: ultragoal
description: Run a large, multi-session goal (e.g. shipping a whole side product) through the full V-model closed loop, one phase at a time, with cross-session state and a final north-star acceptance gate. Ultragoals never downgrade the lane: every phase runs CP-1→CP-6 with adversarial verification. Opt-in: invoke with /ultragoal or by calling something a long-running goal. Ordinary work does not run this.
---

Read `.claude/skills/ultragoal/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
