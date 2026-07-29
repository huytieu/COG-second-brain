---
name: product-ui-taste
description: Anti-slop skill for PRODUCT UI - dashboards, data tables, forms, multi-step flows, settings, list/detail, app shells. The agent reads the surface, budgets the frame first, and ships dense interfaces that are correct at every edge case (overflow, long labels, empty/error/loading states, i18n expansion, keyboard/a11y). House-system-first; maps to Carbon/Polaris/Atlaskit/Fluent/Primer/Material3/Radix-shadcn/Ant. The counterpart to taste-skill, which owns landing/portfolio/marketing.
---

Read `.claude/skills/product-ui-taste/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
