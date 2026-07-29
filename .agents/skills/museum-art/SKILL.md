---
name: museum-art
description: Source authentic, high-res PUBLIC-DOMAIN artwork from museum open-access APIs (Met, Cleveland, SMK, Rijksmuseum, NGA, Art Institute of Chicago, Getty, Smithsonian) instead of AI-generated or generic-stock imagery. The default move whenever a visual needs an aesthetic, credible image (blog heroes, decks, social cards, essay/spec figures). Verified keyless recipes + licensing rules inside.
---

Read `.claude/skills/museum-art/SKILL.md` and execute it exactly as written — that file is the authoritative
playbook. Then follow `.agents/rules/cog.md`.

Antigravity substitution: where the playbook delegates to a `.claude/agents/<name>`
worker, invoke `.agents/agents/<name>.md` via `invoke_subagent` instead.
