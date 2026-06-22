---
name: loop-engineering
description: Shared loop-engineering reference for COG skills - the agent loop, deterministic verifiers, termination conditions, in-loop context management, and named patterns. Invoke when designing or debugging a skill that iterates (search-verify-retry, scan-until-dry, fetch-retry-gate).
roles: [all]
integrations: []
---

# COG Loop Engineering

> **TL;DR:** Some COG skills are not one-shot prompts. They are loops: act, observe, verify, decide whether to continue. This skill is the shared vocabulary those skills use. The iron rule: **trust deterministic checks, never the agent's own "looks done" self-report.** Every loop must declare its verifier, its stopping conditions, and which pattern it follows.

This is a reference and design aid, not a content-generating workflow. Skills that loop (daily-brief, knowledge-consolidation, url-dump, weekly-checkin, and research/triage skills like auto-research and scout) link here instead of restating the rules. Invoke it directly when you are building or fixing an iterative skill.

## Why loops

A chain runs fixed steps: A then B then C. A loop is dynamic: the agent takes an action, reads real feedback (a fetched page, a date stamp, a file count), reasons about it, and repeats until a goal is met or a stop condition fires. Most knowledge-work that "keeps going until good enough" is a loop, and COG benefits from naming the loop explicitly rather than hoping a single prompt nails it.

## The COG loop

```
   ┌──────────────────────────────────────────────┐
   │  1. Gather    pull context (vault + sources)   │
   │  2. Act       one step: search / fetch / scan  │
   │  3. Observe   read the real result             │
   │  4. Verify    run the deterministic check      │
   │  5. Update    write progress to a vault file   │
   │  6. Decide    continue?  → loop                │
   │               stop?      → finish + report     │
   └──────────────────────────────────────────────┘
```

Step 4 is the load-bearing one. A loop without a verifier is just a chain that repeats.

## Termination conditions (use layers, never one)

A robust loop needs several exits so it always halts:

| Exit | What it is | Example |
|------|-----------|---------|
| **Deterministic verifier** | A mechanical pass/fail that confirms the goal | "Publication date is within 7 days" |
| **Hard iteration cap** | Max passes, no matter what | "Stop after 5 searches per topic" |
| **Budget guard** | Max time / tool calls / tokens | "Stop after 20 fetches total" |
| **No-progress detection** | Recent passes changed nothing | "2 searches in a row found nothing new" |
| **Human escalation** | Hand a stuck loop back to the user | "Asked twice, still unclear: ask the user" |

Pick the verifier plus at least one safety exit (cap or budget) for every loop. No-progress detection is what stops the quiet infinite loops that a cap alone misses.

## Verification first (COG's rule, applied to loops)

COG is verification-first: no hallucinations, sources required. Inside a loop that means:

- **Prefer mechanical checks.** A date comparison, a source count, a "required field is non-empty", a "file marked consolidated" check cannot be gamed and cannot be hallucinated.
- **Reserve judgment-based checks for the genuinely unquantifiable** (is this theme actually new? is this summary faithful?). When you must use judgment, state confidence and link evidence.
- **Never accept the agent's own "I think this is complete."** That is the single most common way loops produce confident garbage.

## In-loop context management

Long loops fill the window with old tool output and start to drift ("context rot"). Counter it:

- **Externalize state to the vault.** Write progress to the output file as you go. The vault file is the memory; the conversation is scratch.
- **Compact and prune.** Summarize finished passes into a line or two. Drop raw page text once you have extracted what you need.
- **Isolate sub-agents.** In `agent_mode: team`, give each worker only the slice it needs and take back only its conclusion, so one subtask runs in a clean window. Never paste one worker's raw output into the next worker's prompt.

## Named patterns

| Pattern | Shape | Where COG uses it |
|---------|-------|-------------------|
| **Act-observe (ReAct)** | reason → act → observe → repeat | base of every COG loop |
| **Reflect-retry (Reflexion)** | on failure, write the lesson, retry differently | url-dump / scout fetch retries, daily-brief re-search |
| **Plan-execute-verify** | plan steps, run them, verify each | knowledge-consolidation passes |
| **Evaluator-optimizer** | generate, score against criteria, repeat until it passes | daily-brief item verify, url-dump quality gate |
| **Orchestrator-workers** | split into subtasks, run in fresh windows, synthesize | team-mode scans, auto-research threads, team-brief |
| **Loop-until-dry** | keep going until K passes in a row surface nothing new | knowledge-consolidation theme extraction |
| **Human-in-the-loop** | escalate or ask when the loop is stuck or the call is the user's | weekly-checkin reflection, onboarding |

## Failure modes and fixes

| Failure | Fix |
|---------|-----|
| Context overflow / drift | compact, prune, externalize to vault, isolate sub-agents |
| Silent infinite loop | no-progress detection plus a hard cap |
| Hallucinated success | trust the deterministic verifier, never self-report |
| Compounding errors | verify early and every pass, not only at the end |
| Cost blowup | budget guard, and stop at "good enough", not "perfect" |
| Goal drift | keep the goal and stop conditions written at the top of the loop's state |

## How skills use this

A skill's `## Loop Engineering` section should be short and concrete. It names:

1. **The loop** in one or two lines (what repeats).
2. **The verifier** (the mechanical pass/fail).
3. **The termination conditions** (verifier plus safety exits).
4. **The pattern(s)** from the table above.

It does not restate this skill. It points here.
