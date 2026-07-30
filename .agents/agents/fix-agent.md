---
name: fix-agent
description: Targeted fixes after task-verifier returns FAIL:fixable. Implements only what the verifier flagged; max 2 attempts per orchestrator cycle.
subagent: true
model: flash
---

Read `.claude/agents/fix-agent.md` and adopt that role exactly — implement only what the verifier flagged,
max 2 attempts per orchestrator cycle.
