# SPEC-NNN: <title>

> Lane: `tiny|normal|full|bug|backfill` · Run: `04-projects/harness/runs/<id>` · Date: YYYY-MM-DD

## Goal

One paragraph. What is true when this is done that is not true now.

## Non-goals

What this deliberately does not cover, so scope creep is visible.

## Acceptance criteria

Every criterion is **falsifiable**: a named observation either happens or it does not.
"Works well" is not a criterion. "`curl -s <url> | grep -q '<string>'` exits 0" is.

| ID | Criterion | Verify method |
|---|---|---|
| AC-01 | <observable statement> | <command, screenshot, re-fetch, diff> |
| AC-02 | | |

## Traceability matrix

Status: `pending` at CP-2, `built` at CP-3, `verified` once a PASS row exists in the ledger.

| AC | Task | Evidence row | Status |
|---|---|---|---|
| AC-01 | T-01 | | pending |
| AC-02 | T-02 | | pending |

## Tasks

| ID | Task | Covers |
|---|---|---|
| T-01 | <what gets built> | AC-01 |
| T-02 | | AC-02 |

## Phases (ultragoal only)

| Phase | Scope | Covers | State |
|---|---|---|---|
| P0 | | AC-01 | not started |

## Risks and open questions

- <risk>: mitigation or the decision needed.
