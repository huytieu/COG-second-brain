---
name: closed-loop
description: >
  V-model execute: CP-2 plan → CP-3 build → CP-3v component verify →
  CP-4 integration verify (full) → CP-5 acceptance. Worker never grades
  its own homework; evidence rows trace back to AC-n. Use via /execute.
---

# Closed-loop execute (V-model right arm)

Mechanical verification pipeline. Every verify step emits **evidence rows** tied to acceptance criterion IDs (`AC-n`).

## When to use

- `/execute <task>` or `/execute <spec-path>`
- Any skill at `normal`+ lane after implementation
- Code changes, deploys, multi-step vault deliverables

## Phase 0 — Lane + run folder

```bash
bash .claude/lib/lane-classify.sh explain "<task>"
bash .claude/lib/checkpoint.sh init 04-projects/harness/runs/<YYYY-MM-DD-HHmm>
```

| Lane | Checkpoints |
|---|---|
| `tiny` | CP-3 → CP-5 (if mutating) |
| `normal` | CP-1 → CP-2 → CP-3 → CP-3v → CP-5 |
| `full` | + CP-4 + claim-verifier + CP-6 |
| `bug` | root-cause ledger (CP-0) before CP-3 |

Record: `checkpoint.sh record <run-dir> CP-0 PASS|SKIP "<lane>"`

## Phase 1 — CP-1 Spec (acceptance criteria)

If spec exists, use its `## Acceptance criteria` + traceability matrix. Else write:

`04-projects/harness/runs/<id>/criteria.md` using `04-projects/harness/templates/SPEC-template.md` (criteria + matrix only).

Each criterion: **falsifiable** + `AC-n` ID + verify method.

Record: `checkpoint.sh record <run-dir> CP-1 PASS "N criteria"`

## Phase 2 — CP-2 Plan

Map tasks → AC IDs in `evidence/CP-2-plan.md`. Update matrix status to `pending`.

Record: `checkpoint.sh record <run-dir> CP-2 PASS`

## Phase 3 — CP-3 Build

Worker implements. Returns deliverable path only.

## Phase 4 — CP-3v Component verify

```
retry=0
loop:
  spawn task-verifier (fresh context, read-only)
  merge EVIDENCE rows into evidence/ledger.md
  if PASS → break
  if FAIL:escalate → record CP-3v FAIL, escalate
  if FAIL:fixable && retry < 2 → fix-agent → retry++
  else → escalate
```

Copy verifier EVIDENCE rows into `evidence/CP-3v-component.md`.

Record: `checkpoint.sh record <run-dir> CP-3v PASS|FAIL`

## Phase 5 — CP-4 Integration verify (`full` or multi-task)

Spawn `integration-verifier` (read-only). Append rows to ledger.

Skip for single-task `normal`.

Record: `checkpoint.sh record <run-dir> CP-4 PASS|SKIP`

## Phase 6 — CP-5 Acceptance (post-condition)

For each mutation, observe artifact (curl, screenshot, re-fetch). Emit:

`EVIDENCE AC-n | CP-5 | PASS | <observation> | <artifact>`

**UI/UX flow changes:** the post-condition is *visual*. Capture with browser-harness (`evidence_shot` per state; `FlowRecorder`→`.save_gif()` for a flow; `pixel_diff` against the intended/prior state), then read the image and confirm no overflow/misalignment/clipping/wrong-color/broken-responsive before PASS. The Observation must describe what you saw; the artifact is the screenshot/GIF in `evidence/`. Fix any visual defect and re-capture. See CLAUDE.md → Visual Verification.

Write `evidence/CP-5-acceptance.md`. **Traceability closure**: every AC in matrix has ≥1 PASS row in ledger.

Record: `checkpoint.sh record <run-dir> CP-5 PASS|FAIL`

## Phase 7 — Record + handoff

- Append to `.claude/logs/loop-ledger.tsv`
- Update spec traceability matrix statuses to `verified`
- **`full` lane / big task:** generate an HTML rollup from `04-projects/harness/templates/report.html` → `04-projects/harness/runs/<id>/report.html`, filled from `criteria.md` + `evidence/ledger.md` (criteria, AC traceability, verifier verdicts, post-condition observations). Self-contained; `SendUserFile` it or publish as an Artifact. Skip for `normal`/`tiny`.
- Suggest `/retro <run-dir>` for CP-7

## Integration

| Skill | Lane | CP-4 |
|---|---|---|
| ultragoal | `full` per phase (never downgraded) | integration-verifier + north-star acceptance |
| team-brief | full | claim-verifier |
| dogfood-release | full | Playwright cross-verify |
| blog-publish | normal | skip |
| content-factory | normal | skip |

## Escalation template

```
ESCALATED — <task>
Lane: <lane> | Last CP: <CP-n>
Evidence bundle: 04-projects/harness/runs/<id>/evidence/
Open AC IDs: <list without PASS rows>
Decision needed: <one question>
```
