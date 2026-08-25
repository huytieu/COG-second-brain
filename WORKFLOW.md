# Vault Harness Workflow

> **V-model harness**: decompose on the left, verify with evidence on the right, build at the apex, retro closes the loop.
> Adapted from [dwarves-kit](https://github.com/dwarvesf/dwarves-kit) + V-model SDLC discipline.

## Scope: opt-in only

**This document governs harness runs, and nothing else.** A session that never invoked the harness owes it no checkpoints, no lane classification, and no evidence ledger. Notes, briefs, research, drafts, and ordinary edits are not harness runs.

You are in a harness run when you invoked `/closed-loop`, `/ultragoal`, `/retro`, `/harvest`, or `/review-cockpit`; asked for the closed loop, proper verification, or an evidence trail in those words; or set `verification_harness: on` in `00-inbox/MY-PROFILE.md`. Otherwise you are not, and the two rules in `CLAUDE.md` § Verification Harness are the whole of what applies.

Nothing here needs installing. The two helper scripts (`.claude/lib/checkpoint.sh`, `.claude/lib/lane-classify.sh`) ship executable, and the run directories are created on first use.

## The V-model (primary mental model)

Inside a harness run, every non-`tiny` task walks the V. Each **checkpoint (CP)** is a gate: you cannot descend the left arm past a failed CP, and you cannot ascend the right arm without **evidence** tied back to a criterion ID.

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

Record checkpoints: `bash .claude/lib/checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP <note>` (`init <run-dir>` first to lay down the evidence dir and ledger header)

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

The read-only verifiers (`task-verifier` CP-3v, `integration-verifier` CP-4) are **same-family mechanical** checks that share the lead's blind spots. On high-stakes runs, overlay a **flagship model that is NOT the lead's own** (spawn the verifier with an explicit `model` override from a different family) as a cross-model second opinion. Fresh context (paths + question, never the lead's draft-reasoning), read-only, advisory.

| CP | Flagship role | What it checks |
|---|---|---|
| **CP-1 Spec** | advisor | Are the `AC-n` falsifiable, complete, the *right* criteria? (highest leverage — a wrong spec poisons the left arm) |
| **CP-4 Integration** | critic | Cross-task wiring / global acceptance holds up under a different reasoner |
| **CP-5 Acceptance** | critic | Artifact truly satisfies the north-star, not just a passing post-condition |
| **CP-6 Ship** | critic | Break it before the user sees it — last gate before external/irreversible |
| **Ultragoal** | critic | Per-phase gate AND final north-star acceptance (adversarial by default; wrongness compounds across sessions) |

Advisory, not hard-blocking, but a **critical** cross-model finding means do not auto-ship; escalate the disagreement to the user to adjudicate. Skip entirely on `tiny`/`normal` runs (pure overhead there). If the cross-model reviewer hard-refuses (offensive-security / bio-adjacent), rerun the check on the lead's own family rather than dropping it.

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
orchestrator (/closed-loop or a skill that invokes it)
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
   CP-6: ship gate (you approve anything external / deploy proof)
        │
        ▼
   CP-7: /retro + /harvest
```

## Domain routing

| Work type | Primary skill | Right-arm verifiers |
|---|---|---|
| Single task through the loop | `/closed-loop` | CP-3v `task-verifier` + CP-5 post-condition |
| Long-running goal | `/ultragoal` | full closed-loop per phase + north-star acceptance verifier |
| Team intelligence | `/team-brief` | claim-verifier (CP-3v) + CP-6 |
| Research / analysis | `/auto-research`, `/comprehensive-analysis` | citation verbatim check (CP-3v) |
| Content | `/content-factory` | voice checklist + screenshot (CP-5) |
| Memory store | `/memory-hygiene` | environment re-verify (CP-5) |
| Session learnings | `/harvest` | human promotes (CP-7 input) |
| Multi-item review | `/review-cockpit` | your approval per card (CP-6) |

## Self-enhancement loops

| Loop | CP | Output |
|---|---|---|
| **Closed loop** | CP-3 → CP-5 | Evidence ledger + `loop-ledger.tsv` |
| **Ultragoal** | CP-1 → CP-6 per phase | `04-projects/<goal>/STATUS.md` + evidence per phase + `report.html` |
| **Harvest** | CP-7 | Staging file the human promotes into `05-knowledge/` |
| **Retro** | CP-7 | `04-projects/harness/retro/` + skill patches from friction |
| **Memory hygiene** | CP-5 on memory store | `last_verified` stamps |

## File homes

Run output lives under `04-projects/harness/`, which is created on the first harness run. Templates ship with the skills, so `/update-cog` keeps them current.

| Artifact | Path |
|---|---|
| Spec + traceability matrix | `04-projects/<project>/specs/SPEC-NNN-<slug>.md` |
| Run evidence bundle | `04-projects/harness/runs/<id>/evidence/` |
| HTML report (ultragoal / big run) | `04-projects/<goal>/report.html` · `04-projects/harness/runs/<id>/report.html` |
| Retro outputs | `04-projects/harness/retro/YYYY-MM-DD-<slug>.md` |
| Harness backlog | `04-projects/harness/BACKLOG.md` |
| Ultragoal registry | `04-projects/harness/ultragoals.md` |
| Harvest staging | `04-projects/harness/harvest/staging-<date>.md` |
| Checkpoint + loop logs | `.claude/logs/checkpoint-ledger.tsv`, `loop-ledger.tsv` |
| Spec template | `.claude/skills/closed-loop/references/spec-template.md` |
| Report template | `.claude/skills/closed-loop/references/report-template.html` |
| Retro template | `.claude/skills/retro/references/retro-template.md` |
| Review cockpit template | `.claude/skills/review-cockpit/references/session-review-template.md` |

## Commands

| Command | V-model phase |
|---|---|
| `/closed-loop` | CP-2 through CP-5 |
| `/retro <run or spec>` | CP-7 |
| `/harvest` | CP-7 input |
| `/ultragoal` | full V per phase, across sessions |
| `/memory-hygiene` | CP-5 on memory |

## No install step

The harness has no installer. `.claude/lib/*.sh` ship executable, run directories are created on demand, and COG ships no hooks. If a skill body ever tells you to run `install-harness.sh`, that reference is stale; report it.
