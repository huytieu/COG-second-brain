---
name: harvest
description: >
  Capture durable session learnings, stage for human promotion to
  05-knowledge/lizard, and propose skill/CLAUDE.md patches. Triggered by
  /harvest, SessionEnd hook staging, or nightly enhance. Never writes
  durable knowledge without your approval.
---

# /harvest — session learning capture

Adapted from dwarves-kit `harvest` hook + vault lizard pipeline. Prevents tacit knowledge dying in the transcript.

## Triggers

- `/harvest` — manual end-of-session
- `/harvest promote` — curate staging → lizard drafts (uses harvest-curator)
- Staging file written by `stop` hook (`.cursor/hooks/harvest-stager.sh`)

## Phase 1 — Collect (automatic or manual)

Scan the current session for:

1. **Corrections you made** ("no, actually X", rejected deliverables)
2. **New stable facts** (IDs, URLs, decisions) not yet in 05-knowledge
3. **Process lessons** (what worked, what failed, friction)
4. **Skill gaps** (something that should be a Verify step or CLAUDE.md rule)

Append to `04-projects/harness/harvest/staging-<YYYY-MM-DD>.md`:

```markdown
## <HH:MM> — <trigger>
- type: correction|fact|process|skill-gap
- source: <file or "session">
- text: <one paragraph max>
- proposed_home: <path or "new lizard note">
```

Dedup: skip if same fact already in staging today or in 05-knowledge.

## Phase 2 — Curate (`/harvest promote`)

Spawn `harvest-curator` (Sonnet). It writes `/tmp/harvest-curate-<date>.md`.

Lead (Opus) presents to the user:

- **Promote** list → approve which become `05-knowledge/lizard/YYYY-MM-DD-<slug>.md`
- **Fold** list → approve inline edits to existing notes
- **Skill patches** → approve CLAUDE.md / SKILL.md diffs

Only after approval: write durable files. Update `05-knowledge/lizard/index.md`.

## Phase 3 — Retro line

One line to `01-daily/journal/<today>.md`:

```
Harvest: <n> staged, <m> promoted, <k> folded
```

## Rules

- Harvest is **advisory**. It never auto-writes 05-knowledge.
- Contradictions with existing knowledge → flag both, ask the user.
- Pair with `/memory-hygiene` monthly for environment-dependent facts in `~/.claude/.../memory/`.

## Nightly enhance (optional launchd)

```bash
# 04-projects/harness/scripts/nightly-enhance.sh
bash .claude/lib/install-harness.sh --check  # hooks alive
# /memory-hygiene (skill)
# /harvest promote if staging non-empty
# content-factory if scheduled
```
