---
name: closed-loop
description: Run one task through the V-model verification loop: CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify (full lane) → CP-5 acceptance. The worker never grades its own homework; evidence rows trace back to AC-n. Opt-in: invoke with /closed-loop or by asking for the closed loop, proper verification, or an evidence trail. Ordinary work does not run this.
---

Read `.claude/skills/closed-loop/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
