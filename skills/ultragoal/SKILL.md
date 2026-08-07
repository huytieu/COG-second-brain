---
name: ultragoal
description: >
  Run a large, multi-session goal (e.g. shipping a whole side product) through the full V-model
  closed loop, one phase at a time, with cross-session state and a final
  north-star acceptance gate. Ultragoals never downgrade the lane: every
  phase runs CP-1→CP-6 with adversarial verification. Use via /ultragoal.
---

# Ultragoal — the closed loop for goals too big to ship in one run

An **ultragoal** is the term for a north-star that spans many sessions: fork the repos, combine the strong parts, ship one product. A normal `/execute` run is one task through the loop. An ultragoal is a *chain of phases*, each of which is its own full closed-loop run, tracked so any cold session can resume.

**Core rule (from dwarves-kit, adopted fully): the worker never grades its own homework, and wrongness compounds across sessions — so verify every phase, not just the end.**

## When to use

- `/ultragoal <name>` — resume or advance an existing ultragoal
- `/ultragoal new "<north-star>"` — charter a new one
- `/ultragoal status` — report all ultragoals from the registry
- Trigger phrases: "make this an ultragoal", "this is a long-running goal", "combine these into one product over time"

Do **not** use for single-run work — that is `/execute`. Rule of thumb: if it needs a phase decomposition and won't finish today, it is an ultragoal.

## Files (one goal = one folder)

| File | Role |
|---|---|
| `04-projects/harness/ultragoals.md` | Registry: every ultragoal, status, current phase |
| `04-projects/<goal>/spec.md` | Contract: north-star + `AC-n` acceptance criteria + phases `P0…Pn` + traceability matrix |
| `04-projects/<goal>/STATUS.md` | Living ledger: phase state, current phase, open `AC-n`, next action (resume from here) |
| `04-projects/<goal>/evidence/P<n>/` | Per-phase evidence bundle (ledger.md + CP-* files) |

Code, if any, lives outside the vault (e.g. `~/code/<goal>/`) — the spec/status/evidence stay in the vault.

## Phase 0 — Charter (`/ultragoal new`)

1. Interview the user for the **north-star** in one sentence (what "done" looks like).
2. Write `04-projects/<goal>/spec.md` from `04-projects/harness/templates/SPEC-template.md`:
   - North-star statement
   - Falsifiable `AC-n` acceptance criteria (these define done for the *whole* goal)
   - Phase decomposition `P0…Pn` — each phase is a shippable increment mapped to a subset of `AC-n`
   - Traceability matrix (`AC-n` ↔ phase ↔ status)
3. Create `STATUS.md` (see template below) and add a row to the registry.

Record: `bash .claude/lib/checkpoint.sh record 04-projects/<goal>/evidence/P0 CP-1 PASS "N criteria, M phases"`

## The phase loop (every phase, no lane downgrade)

Each phase runs the **full** closed loop. Do not shortcut with `tiny`. Ultragoals are `full` lane by construction.

```
select next phase from STATUS.md
        │
        ▼
CP-2 PLAN     tasks for this phase ↔ AC-n   → evidence/P<n>/CP-2-plan.md
        │
        ▼
CP-3 BUILD    worker implements (traced to AC-n); returns paths only
        │
        ▼
CP-3v VERIFY  task-verifier (fresh context, read-only) → evidence rows per AC-n
        │       ├── FAIL:fixable → fix-agent (max 2) → re-verify
        │       └── FAIL:escalate → stop, escalate to the user
        ▼
CP-4 INTEGRATE  integration-verifier → does this phase wire correctly with prior phases?
        │        (always run for ultragoals — cross-phase regression is the main risk)
        ▼
CP-5 ACCEPT   observe the artifact (curl / screenshot / re-fetch), not the tool return
        │       EVIDENCE AC-n | CP-5 | PASS | <observation> | <artifact>
        ▼
CP-6 SHIP     external mutation? → Review Gate: you approve. Internal? → auto.
        │
        ▼
update STATUS.md (phase → done, advance current phase, log open AC-n)
        │
        ▼
CP-7 RETRO    /retro 04-projects/<goal>/evidence/P<n>  → harvest + STATUS
```

Merge every verifier's `EVIDENCE` rows into `evidence/P<n>/ledger.md`.

## The two acceptance gates

1. **Per-phase (CP-5):** every `AC-n` this phase claims has a PASS row before the phase is marked done.
2. **North-star (final):** before the ultragoal is declared complete, spawn a fresh-context verifier whose only job is to check the spec matrix — **every** `AC-n` across all phases has ≥1 PASS evidence row. Any `AC-n` without one is a gap, not a ship. This is the ultragoal-level analogue of CP-5.

```
North-star acceptance:
  read spec.md matrix (all AC-n)
  read every evidence/P*/ledger.md
  for each AC-n: assert ≥1 PASS row exists, artifact re-observed
  any miss → list open AC-n, STATUS stays "in progress", do NOT declare done
```

## The HTML report (regenerate at every phase gate + final)

Every ultragoal carries a single self-contained HTML report that **covers everything**: north-star, live status, all phases, the full `AC-n` traceability table with pass/open/fail, evidence rows per phase (with screenshots embedded as `data:` URIs), and the open-items / next-action block. It is the human-readable face of the evidence ledger.

- **Template:** `04-projects/harness/templates/report.html` (house style, theme-aware, rows-not-cards). Copy it, then fill every `{{token}}` and `<!-- FILL -->` / `<!-- REPEAT -->` block from `spec.md` + `STATUS.md` + `evidence/P*/`. You fill it by editing — do not build a parser.
- **Deliverable path:** `04-projects/<goal>/report.html`. One file, overwritten each phase (it always reflects current truth).
- **When:** regenerate at each phase gate (CP-6) and again at final north-star acceptance. The final report must show every `AC-n` with a PASS row — if any pill is `open`, the goal is not done.
- **Self-contained only:** inline everything, embed screenshots as `data:` URIs, so it also works when published as an Artifact (external hosts are blocked). Before publishing as an Artifact, load the `artifact-design` skill.
- **Surface it:** `SendUserFile 04-projects/<goal>/report.html` (display: render) so the user can open it, or publish via `Artifact` for a shareable link.

## STATUS.md template

```markdown
# <Goal> — status ledger

North-star: <one sentence>
Spec: 04-projects/<goal>/spec.md · Registry: 04-projects/harness/ultragoals.md
Current phase: P<n> · Overall: <not-started|in-progress|blocked|done>

## Phases
| Phase | AC covered | State | Evidence | Notes |
|---|---|---|---|---|
| P0 | AC-1,AC-2 | done | evidence/P0/ | <one line> |
| P1 | AC-3 | in-progress | evidence/P1/ | <what's left> |

## Open AC-n (no PASS row yet)
- AC-3 — <why still open>

## Next action (resume cold from here)
<the single next concrete step + any user-gated decision waiting>
```

## Resuming cold (most common entry)

`/ultragoal <name>` with no other context:
1. Read `04-projects/<goal>/STATUS.md` → "Next action" and "Open AC-n".
2. Read the spec's phase for the current phase only (progressive disclosure).
3. Run the phase loop for the current phase.
4. Never re-do a phase already marked `done` unless integration verify caught a regression.

## Rules

- **Never downgrade the lane.** Even a one-line phase inside an ultragoal runs CP-3v + CP-4. The point is compounding correctness.
- **UI/UX phases verify visually.** If a phase touches a UI/UX flow, capture rendered evidence with browser-harness (`evidence_shot` / `FlowRecorder.save_gif` / `pixel_diff`), read the image, fix any visual defect, and re-capture — do not accept a DOM check. Media lands in `evidence/P<n>/` and feeds `report.html`. See CLAUDE.md → Visual Verification.
- **Fresh-context verifiers.** `task-verifier`, `integration-verifier`, north-star verifier get paths only — never paste worker output in (CLAUDE.md fresh-context isolation).
- **Read-only verifiers.** They cannot edit files or mutate external state.
- **Gate all external.** Any publish / deploy / push waits at CP-6 for the user (Review Gate = your approval).
- **One STATUS.md is the source of truth** for where the goal stands. Update it at the end of every phase or it drifts.
- Model routing per CLAUDE.md: Sonnet workers build/collect/verify; Opus lead reasons, decomposes, synthesizes.

## Escalation template

```
ULTRAGOAL ESCALATED — <goal> / P<n>
Last CP: <CP-id> | Open AC: <list without PASS rows>
Evidence: 04-projects/<goal>/evidence/P<n>/
Decision needed: <one question>
```

## Registered ultragoals

Live list: `04-projects/harness/ultragoals.md`. Each ultragoal gets its own `04-projects/<goal>/` folder holding `spec.md`, `STATUS.md`, `evidence/`, and `report.html`.
