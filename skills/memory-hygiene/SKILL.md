---
name: memory-hygiene
description: Periodic trust sweep of persistent memory and durable knowledge notes - re-verifies environment-dependent claims against the live environment, stamps last_verified + confidence, and proposes archiving drifted entries
roles: [all]
integrations: []
---

# COG Memory Hygiene Skill

## Purpose

Prevent the **stale-but-confident** failure mode: a memory or knowledge note that was correct when written ("the webhook lives at X", "the board ID is Y") silently drifts after the environment changes, yet still ranks high at recall and gets acted on.

The system move (adapted from "From Model Scaling to System Scaling: Scaling the Harness in Agentic AI", Gu, UC Berkeley, arXiv:2605.26112): **make trust a runtime decision, not a property of the stored item**. Re-verify against the live environment, and keep per-entry `last_verified` and `confidence` as first-class fields so future recalls can weigh trust.

## When to Invoke

- `/memory-hygiene`
- "Audit my memories" / "check for stale memories"
- After a memory misfires (a recalled fact turned out wrong)
- Default cadence: monthly

## Scope

Sweep two stores:

1. **Agent memory** — wherever your agent keeps persistent memory files (e.g. Claude Code's auto-memory directory). Sweep every entry except the index itself.
2. **Durable knowledge notes** — `05-knowledge/**` files whose claims reference the environment (paths, URLs, IDs, tool names).

A partial sweep ("just the reference entries") is fine when asked.

## Claim Classification

For each entry, split its claims into two buckets:

| Bucket | Examples | Action |
|---|---|---|
| **Environment-dependent** | file/dir paths, repo names, branch names, channel IDs, board IDs, URLs, API endpoints, cron/routine IDs, CLI names, version numbers, "X lives at Y" | Verify against the live environment |
| **Preference / judgment** | tone rules, formatting rules, "never do X", people facts, strategy context | No environment check possible; verify only for internal contradiction with newer entries |

## Verification Moves (cheap first)

- Paths and files: `ls` / `test -e`. Skills, commands, and agents named in an entry must still exist at the stated path.
- URLs: resolve with a HEAD/GET (`curl -sI`); flag 404 or redirect-to-login.
- Repos/branches: `gh repo view`, `git ls-remote` when cheap.
- IDs (channels, boards, routine triggers): verify only if an MCP/CLI check is one call; otherwise mark `unverifiable-cheaply` and leave confidence untouched.
- Cross-entry contradiction: newer entry wins; flag the older one.

Never spend more than ~1 minute per entry. This is hygiene, not an investigation. **Unverifiable ≠ drifted.**

## Stamping

After checking an entry, update its frontmatter `metadata:` block in place (do not touch body text unless fixing a verified-wrong fact):

```yaml
metadata:
  type: reference
  last_verified: 2026-07-10
  confidence: high   # high = verified now | medium = unverifiable cheaply | low = partially drifted
```

- Verified clean → `confidence: high`, stamp date.
- Unverifiable cheaply → keep prior confidence (or `medium`), stamp date.
- Partially drifted → fix the drifted fact directly in the body (reviewable via the report); set `confidence: low` only if unsure the fix is complete.
- Fully obsolete → **propose archive, don't delete.** List it in the report's "Propose archive" section; only archive after the user confirms.

## The Loop (see /loop-engineering)

Scan-until-done over the entry list with a per-entry budget guard (~1 min). The deterministic verifier is the environment itself (`test -e`, `curl`, `gh`) — never the agent's own recollection of whether something "should" still exist. Human escalation: all deletions/archives.

## Report (single file)

Write one report per sweep to `01-daily/YYYY-MM-DD-memory-hygiene.md`, structured around four evolution questions:

1. **What persists?** — counts by type (user/feedback/project/reference).
2. **What updated?** — entries whose body was corrected, with old → new.
3. **What is measured?** — scorecard: `verified / unverifiable / drifted / propose-archive` counts, plus deltas vs the previous sweep report (the drift *trend* is the longitudinal signal one-shot checks miss).
4. **What is auditable?** — every change in this sweep is a line in this report; for stores Git does not track, the report IS the audit trail.

End the report with a **Propose archive** section (explicit list, one line of evidence each) and a **Waiting on you** line if anything needs a decision.

## Rules

- Propose-only for deletions/archives; direct-apply for stamps and verified factual corrections.
- Never rewrite an entry's voice or restructure it during a sweep.
- If the memory index points at renamed/missing files, fix the index.
- Keep the sweep itself out of memory: the report file is the record.
