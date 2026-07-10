# Skill Distillation: Explore Once, Execute Cheap

A COG meta-pattern for turning one expensive exploration by a strong model into a durable skill artifact that a small, cheap model can execute reliably. Field-validated on a web-app testing workload: one $4.63 / 150-turn exploration once → $0.11 per execution on a Haiku-class model afterwards, with correct verdicts on all sampled runs.

The pattern generalizes to any repetitive task against a stable-but-drifting environment: testing an app, filing reports into a system, operating a dashboard, running a recurring data pull.

## Core principle

**An executor reads O(1 task) of knowledge, not O(environment).** Layer knowledge by when it's needed:

```
always loaded      → SKILL.md router (<1K tokens: discipline, helpers, verdict contract)
per task           → one recipe (~200 tokens: steps + anchors + oracle, self-contained)
on failure only    → healing.md (decision tree)
on healing only    → ONE map shard (feature-level knowledge)
maintainer only    → CHANGELOG.md, friction inbox
```

## The four phases

### 1. Exploration (once, expensive, strong model)

One long background run that builds a full functional model of the environment: pages/screens, flows, computed behaviors **with worked examples**, validation rules, quirks. Record **durable anchors only** (labels, roles, stable IDs) — never ephemeral references. Read-only against real environments. Apply the Worker Output Rule: findings go to a staging file, the run returns one status line.

**Treat exploration output as fallible.** Expect at least one confidently-wrong claim; the evolution loop below is the truth filter, not the explorer's self-report.

### 2. Distillation (lead-session reasoning)

1. **Verify interaction mechanics BEFORE writing them into the skill** — run 1-2 cheap probe agents that test the exact helpers the recipes will use.
2. Write the router (`SKILL.md`, <1K tokens): discipline, verified helpers, result contract, verdict taxonomy, index.
3. Write `healing.md`: a capped decision tree for when a recipe's anchor fails (found-but-renamed → finish and report friction; gone → read the ONE relevant map shard; behavior contradicts oracle → re-verify, then fail-for-real; retry once before declaring a real failure, to filter flakes). Executors NEVER edit skill files.
4. Write map shards by feature + a one-line-per-shard index.
5. Write self-contained recipes (~150-250 tokens each). Recipes are **compiled artifacts** — regenerate them from the map when the map changes; the map is the source of truth.

### 3. Evolution loop (batched execution, mid-tier model)

Run recipes in parallel batches. After each batch: harvest verdicts + friction, patch the skill (single-writer: only the maintainer edits), bump the skill version, append a CHANGELOG entry. Loop until a batch produces **zero friction and zero staleness failures** (loop-until-dry — see /loop-engineering).

Structured friction is the ONLY feedback channel — every executor reports `{task, verdict, evidence, friction}` and nothing else.

### 4. Validation (proves the claim)

Run a sample of recipes — including deliberate failure-detectors whose oracles encode *intended* behavior — on a small model. Success = correct verdicts at a fraction of the cost. If the small model can't execute the skill, the distillation is not done.

## The verdict taxonomy (the contract between execution and triage)

- **PASS** — matches the oracle (may carry friction, e.g. "healed a stale anchor").
- **FAIL-REAL** — anchors work, environment reachable, behavior contradicts the oracle → a genuine finding; quote observed values.
- **FAIL-STALE** — the environment changed, the skill is outdated → maintainer patches the skill; no finding filed.
- **BLOCKED** — environment problem (down, auth, tooling error) → rerun, don't diagnose.

Separating FAIL-REAL from FAIL-STALE is the whole game: it routes "the world changed" to skill maintenance and "the world is wrong" to real reporting, instead of mixing both into noise.

**Adversarially verify FAIL-REAL verdicts whose oracle rests on exploration-derived knowledge** before reporting them — spawn one probe to independently re-check the claim. Oracles derived from requirements (math, stated rules) don't need this.

## Relationship to other COG pieces

- **/loop-engineering** — the evolution loop is a loop-until-dry with a deterministic verifier (batch friction count) and single-writer state.
- **Worker Output Rule** — explorers and executors write files, return status lines.
- **memory-hygiene** — a distilled skill is memory; FAIL-STALE is its drift signal, the CHANGELOG is its audit trail.
