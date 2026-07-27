# Vault Harness Workflow

> **V-model harness**: decompose on the left, verify with evidence on the right, build at the apex, retro closes the loop.
> Adapted from [dwarves-kit](https://github.com/dwarvesf/dwarves-kit) + V-model SDLC discipline.

## The V-model (primary mental model)

Every non-`tiny` task walks the V. Each **checkpoint (CP)** is a gate: you cannot descend the left arm past a failed CP, and you cannot ascend the right arm without **evidence** tied back to a criterion ID.

```
                    CP-0 INTAKE (think)
                   ╱  evidence: questions answered
                  ╱
         CP-1 SPEC ──────────────── CP-5 ACCEPTANCE
        ╱  criteria + trace matrix    ╲  post-condition artifacts
       ╱                               ╲
  CP-2 PLAN ───────────────────── CP-4 INTEGRATION
      task ↔ criterion map              cross-task wiring
              ╲                    ╱
               ╲   CP-3 BUILD   ╱
                ╲  (execute)  ╱
                 ╲────────────╱
                  component verify (task-verifier)
                           │
                      CP-6 SHIP
                           │
                      CP-7 RETRO ──► feeds CP-0 next cycle
```

### Two-way verification

| Direction | What | Artifact |
|---|---|---|
| **Down (left arm)** | Decompose goal → falsifiable criteria → tasks | Spec + traceability matrix (`AC-01` → task `T-01`) |
| **Up (right arm)** | Prove each task → prove wiring → prove acceptance | Evidence ledger rows (`AC-01` ← verifier observation) |
| **Bidirectional** | Every `AC-n` has ≥1 task AND ≥1 evidence row before ship | Matrix status = `traced` |

No criterion ships without a matching evidence row. No evidence row without a criterion ID.

## Checkpoints

| CP | Phase | Gate class | Pass requires | Evidence file |
|---|---|---|---|---|
| **CP-0** | Intake / think | advisory | Forcing questions answered or lane=`tiny` skip | `evidence/CP-0-intake.md` |
| **CP-1** | Spec | blocking (`normal`+) | `## Acceptance criteria` with IDs (`AC-01`…) | spec itself + matrix |
| **CP-2** | Plan | blocking (`normal`+) | Tasks reference `AC-n`; criteria falsifiable | `evidence/CP-2-plan.md` |
| **CP-3** | Build | — | Worker deliverable exists | deliverable path |
| **CP-3v** | Component verify | blocking | `task-verifier` PASS per task | `evidence/CP-3v-component.md` |
| **CP-4** | Integration verify | blocking (`full`+, multi-task) | `integration-verifier` PASS | `evidence/CP-4-integration.md` |
| **CP-5** | Acceptance | blocking (mutations) | Post-condition observed (not tool return) | `evidence/CP-5-acceptance.md` |
| **CP-6** | Ship | blocking (external) | Review Gate / your approval / deploy proof | `evidence/CP-6-ship.md` |
| **CP-7** | Retro | advisory | Retro doc + harvest staged | `04-projects/harness/retro/YYYY-MM-DD-<slug>.md` |

Record checkpoints: `bash .claude/lib/checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP <note>`

### Evidence row contract (every verify pass)

```text
EVIDENCE <AC-id> | <checkpoint> | PASS|FAIL | <observation> | <artifact-path-or-command>
```

Verifier and post-condition steps emit these rows. Consolidate in `evidence/ledger.md` per run.

## Gate classes

| Class | Examples | Behavior |
|---|---|---|
| **Blocking** | CP-1 spec, CP-3v verifier, CP-5 post-condition, CP-6 ship, safety-gate | Stops a bad outcome |
| **Advisory** | CP-0 think, roundtable, slop-cleaner, CP-7 retro, cross-model flagship gate | Surfaces findings; retro strongly expected |

### Cross-model flagship gate (`full`+ / ultragoal / irreversible)

The read-only verifiers (`task-verifier` CP-3v, `integration-verifier` CP-4) are **same-family mechanical** checks — they share the lead's blind spots. On high-stakes runs, overlay a **flagship model that is NOT the lead's own** (spin off `Agent(model="fable")` when the lead is Opus) as a cross-model second opinion. Fresh context (paths + question, never the lead's draft-reasoning), read-only, advisory.

| CP | Flagship role | What it checks |
|---|---|---|
| **CP-1 Spec** | advisor | Are the `AC-n` falsifiable, complete, the *right* criteria? (highest leverage — a wrong spec poisons the left arm) |
| **CP-4 Integration** | critic | Cross-task wiring / global acceptance holds up under a different reasoner |
| **CP-5 Acceptance** | critic | Artifact truly satisfies the north-star, not just a passing post-condition |
| **CP-6 Ship** | critic | Break it before the user sees it — last gate before external/irreversible |
| **Ultragoal** | critic | Per-phase gate AND final north-star acceptance (adversarial by default; wrongness compounds across sessions) |

Advisory, not hard-blocking — but a **critical** cross-model finding means do not auto-ship; escalate the disagreement to the user to adjudicate. Skip entirely on `tiny`/`normal` runs (pure overhead there). If the flagship hard-refuses (offensive-security / bio-adjacent), rerun the check on Opus 5 rather than dropping it.

## Risk lanes (checkpoint depth)

| Lane | Checkpoints required |
|---|---|
| `tiny` | CP-3 → CP-5 (if mutating) only |
| `normal` | CP-1 → CP-2 → CP-3 → CP-3v → CP-5 |
| `full` | all through CP-4 + claim-verifier + CP-6 Review Gate |
| `bug` | CP-0 root-cause ledger → CP-3 → CP-3v (3-fix wall) |
| `backfill` | CP-1 audit only; no CP-3 until approved |

Classifier: `bash .claude/lib/lane-classify.sh classify "<task>"`

## Verification pipeline (right arm detail)

```
orchestrator (/execute or skill)
        │
        ▼
   CP-3 BUILD: worker implements (traced to AC-n)
        │
        ▼
   CP-3v: task-verifier (read-only) ──► evidence rows per AC-n
        │
        ├── FAIL:fixable ─► fix-agent (max 2) ─► re-verify
        └── FAIL:escalate ─► stop
        │
        ▼
   CP-4: integration-verifier (multi-task / full lane only)
        │
        ▼
   CP-5: post-condition (observe artifact: curl, screenshot, re-fetch)
        │
        ▼
   CP-6: ship gate (Review Gate: you approve external / gstack / deploy proof)
        │
        ▼
   CP-7: /retro + /harvest
```

## Domain routing

| Work type | Primary skill | Right-arm verifiers |
|---|---|---|
| Long-running goal | `/ultragoal` | full closed-loop per phase + north-star acceptance verifier |
| Team intelligence | `/team-brief` | claim-verifier (CP-3v) + CP-6 |
| Code / deploy | `/execute` + gstack | CP-3v + tests + CP-5 curl |
| Product dogfood | `/dogfood-release` | Playwright cross-verify (CP-4) |
| Content | content-factory | voice checklist + screenshot (CP-5) |
| AUT skills | aut-skill-capture | verdict taxonomy (CP-3v) |
| Knowledge | `/memory-hygiene` | environment re-verify (CP-5) |
| Session learnings | `/harvest` | human promotes (CP-7 input) |

## Self-enhancement loops

| Loop | CP | Output |
|---|---|---|
| **V execute** | CP-3 → CP-5 | Evidence ledger + loop-ledger.tsv |
| **Evolution** | CP-7 → aut-skill-capture | Skill patches from friction |
| **Ultragoal** | CP-1 → CP-6 per phase | `04-projects/<goal>/STATUS.md` + evidence per phase + `report.html` |
| **Harvest** | CP-7 | staging → lizard |
| **Memory hygiene** | CP-5 on memory store | `last_verified` stamps |
| **Retro** | CP-7 | `04-projects/harness/retro/` |

## File homes

| Artifact | Path |
|---|---|
| Spec + traceability matrix | `04-projects/<project>/specs/SPEC-NNN-<slug>.md` |
| Run evidence bundle | `04-projects/harness/runs/<id>/evidence/` |
| HTML report (ultragoal / big run) | `04-projects/<goal>/report.html` · `04-projects/harness/runs/<id>/report.html` |
| Report template | `04-projects/harness/templates/report.html` |
| Spec template | `04-projects/harness/templates/SPEC-template.md` |
| Retro outputs | `04-projects/harness/retro/YYYY-MM-DD-<slug>.md` |
| Harness backlog | `04-projects/harness/BACKLOG.md` |
| Harvest staging | `04-projects/harness/harvest/staging-<date>.md` |
| Checkpoint + loop logs | `.claude/logs/checkpoint-ledger.tsv`, `loop-ledger.tsv` |

## Commands

| Command | V-model phase |
|---|---|
| `/execute` | CP-2 through CP-5 |
| `/retro <run or spec>` | CP-7 |
| `/harvest` | CP-7 input |
| `/ultragoal` | full V per phase, across sessions |
| `/memory-hygiene` | CP-5 on memory |

## Install

```bash
bash .claude/lib/install-harness.sh
bash .claude/lib/install-harness.sh --check
```
