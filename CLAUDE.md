# COG Second Brain — Framework Instructions

> Lifecycle: `WORKFLOW.md` (V-model harness) · Universal surface: `AGENTS.md`

## V-Model Checkpoints — ALWAYS APPLY

Work walks the **V**: decompose left (spec → plan), build at the apex, verify right with **evidence** traced to criterion IDs (`AC-n`). See `WORKFLOW.md` for the full diagram.

| CP | Phase | Blocking when |
|---|---|---|
| CP-1 | Spec + traceability matrix | `normal`+ |
| CP-2 | Plan (tasks ↔ AC-n) | `normal`+ |
| CP-3 | Build | always |
| CP-3v | Component verify (`task-verifier`) | `normal`+ |
| CP-4 | Integration verify (`integration-verifier`) | `full`+, multi-task |
| CP-5 | Acceptance (post-condition artifacts) | mutations |
| CP-6 | Ship (Review Gate / user approval) | external |
| CP-7 | Retro (`/retro`) + harvest | advisory, expected |

**Two-way verification:** every `AC-n` has a task on the left and ≥1 `EVIDENCE AC-n | CP-* | PASS | …` row on the right before ship. Record checkpoints with `bash .claude/lib/checkpoint.sh record <run-dir> <CP> PASS|FAIL "<note>"`. Evidence bundles live in `04-projects/harness/runs/<id>/evidence/ledger.md`.

**Cross-model flagship gate (`full`+ / ultragoal / irreversible):** overlay a flagship model that is NOT the lead's own as a cross-model advisor at CP-1 and critic at CP-4, CP-5, CP-6. Fresh context, read-only, advisory. Same-family verifiers share the lead's blind spots; a different model catches a different error class. A critical cross-model finding blocks auto-ship. Skip on `tiny`/`normal`.

## Closed-Loop Execute — ALWAYS APPLY (build tasks)

Every **build task** (`normal` lane and above) runs the verification pipeline before reporting success. Skill: `.claude/skills/closed-loop/SKILL.md`. Inspired by [dwarves-kit](https://github.com/dwarvesf/dwarves-kit).

```
worker → task-verifier (read-only) → fix-agent (max 2 retries) → escalate to the user
```

| Lane | Ceremony | Classifier |
|---|---|---|
| `tiny` | worker + post-condition if mutating | `bash .claude/lib/lane-classify.sh classify "<task>"` |
| `normal` | full pipeline above | default |
| `full` | pipeline + claim-verifier for auditable claims | briefs, publishes |
| `bug` | evidence ledger before fix; 3-fix wall | regressions |
| `backfill` | audit/plan only until approved | doc retrofits |

**Rules:**
- `task-verifier` and `fix-agent` are **fresh-context** subagents (paths only, never paste worker output into a verifier).
- Verifier agents are **read-only** — they cannot edit files or mutate external state.
- **Dispatch a verifier subagent when there is external state, or when a fresh pair of eyes is the point** — mutations (publishes, pushes, tracker transitions, deploys), auditable claims, `full`+ lanes, every ultragoal phase.
- **On `normal`-lane read-only work, the lead verifies inline instead.** Spawning a verifier to re-read a file the lead just wrote buys nothing.
- Verification means **observing the artifact** (curl the URL, screenshot the page, re-fetch the issue, diff the file), never re-reading the worker's own summary of it.
- Max **2** fix-agent retries per task, then `ESCALATE` with evidence. Log outcomes to `.claude/logs/loop-ledger.tsv`.

## Risk Lanes — ALWAYS APPLY

Classify before executing: `bash .claude/lib/lane-classify.sh explain "<task>"`.

- **tiny**: skip verifier unless external mutation.
- **normal**: closed-loop + single-file deliverable. Verifier subagent only when the task mutates external state.
- **full**: closed-loop + adversarial claim-verifier + Review Gate for external.
- **bug**: root cause before patch.
- **backfill**: no behavior change without approval.

## Ultragoal — ALWAYS APPLY (long-running goals)

An **ultragoal** is a large, multi-session goal that can't ship in one run. It gets the closed loop applied in full and is never lane-downgraded. Skill: `.claude/skills/ultragoal/SKILL.md`.

- **One spec, north-star + `AC-n`.** `04-projects/<goal>/spec.md` holds the north-star, falsifiable acceptance criteria, and a phase decomposition (`P0…Pn`).
- **Every phase is a full closed-loop run** (CP-1 → CP-6). No `tiny` shortcut inside an ultragoal.
- **Living status ledger.** `04-projects/<goal>/STATUS.md` tracks phase state, current phase, open `AC-n`, and next action so any session resumes cold.
- **Two acceptance gates.** Per-phase acceptance (CP-5) AND a final **north-star acceptance verifier** that checks every `AC-n` has a PASS row.
- **Adversarial by default.** Wrongness compounds across sessions, so verify every phase, not only the end.

## Visual Verification — ALWAYS APPLY (UI/UX tasks)

Any task that **implements or changes a UI/UX flow** is not verified by a DOM/selector check. The DOM can be present and the pixels still wrong: overflow, misalignment, clipped text, wrong contrast, broken responsive layout, z-index overlap.

- **Capture visual evidence.** Screenshot every meaningful state; record multi-step flows.
- **Actually read the image, then compare** against the intended design (mock, spec wireframe, prior state, house style). Name the discrepancy; never declare pass on "element exists."
- **Fix the UI error you spot** — part of the task, not a follow-up. Re-capture to prove it.
- Evidence lands in the run evidence dir and feeds the CP-5 post-condition row.

## Delegation Cap — ALWAYS APPLY

Delegation is not free: each subagent re-establishes context, re-explores, and reports back, and the lead then re-reads the report. Delegate when the payoff clearly exceeds that overhead — not by reflex.

- **Don't delegate work the lead can finish in a handful of tool calls.**
- **Fan out only for genuinely independent, sizeable tracks** — ≥3 unrelated items, a wide multi-source sweep, or parallel workers that would conflict on the same file.
- **If one subagent can do it, use one.** Keep spawn counts low.
- **Brief precisely the first time.** Avoid launch → wait → re-brief; never redo a subagent's work after it reports.
- Independent agents launched together go in **one message with multiple tool calls** so they run concurrently.

## Model Routing — ALWAYS APPLY

When spawning subagents, use the correct model for the task:

| Task type | Model | Agent definition |
|-----------|-------|-----------------|
| Data collection (GitHub, Slack, Jira, Linear, file reads) | **Sonnet** | `worker-data-collector` |
| Web research (search, fetch URLs, extract facts) | **Sonnet** | `worker-researcher` |
| Publishing (Slack, Confluence, Notion, webhooks) | **Sonnet** | `worker-publisher` |
| File operations (vault reads/writes, metadata, profiles) | **Sonnet** | `worker-file-ops` |
| Pre-approved mutations (Jira transitions, Linear updates, API calls) | **Sonnet** | `worker-executor` |
| People profile updates from brief/meeting data | **Sonnet** | `brief-people-updater` |
| Read-only verification (acceptance criteria, post-conditions) | **Sonnet** | `task-verifier` |
| Cross-task integration verify (CP-4) | **Sonnet** | `integration-verifier` |
| Targeted fixes after verifier FAIL:fixable | **Sonnet** | `fix-agent` |
| Harvest staging curation (propose-only) | **Sonnet** | `harvest-curator` |
| Reasoning, synthesis, cross-referencing, writing | **Opus** | Lead session (no delegation) |
| Editorial judgment, tone, strategic decisions | **Opus** | Lead session (no delegation) |

**Rule:** If a task doesn't require reasoning or judgment, delegate it to a Sonnet worker. The lead session (Opus) handles thinking, synthesis, and writing only.

Agent definitions live in `.claude/agents/`.

### Worker Output Rule — ALWAYS APPLY

Workers must **write results to a file** and return only a short status + file path. Never have a worker return large text as output.

| Output size | What to do |
|------------|------------|
| < 2K tokens | Return inline (short status, confirmation, error) |
| >= 2K tokens | Write to `/tmp/{task-slug}-{context}.md`, return path |

**Why:** Generating thousands of tokens as agent output is sequential and extremely slow. Writing to file is instant. The orchestrator or next agent reads the file via the Read tool.

**Pattern:**
```
# Worker prompt must include:
"Write your results to /tmp/{descriptive-name}.md and return ONLY a short status message with the file path."

# Worker returns:
"OK: /tmp/slack-data.md (gathered 47 messages, 12 threads)"

# Orchestrator reads:
Read("/tmp/slack-data.md")
```

**Applies to:** All `worker-*` agents, all `brief-*` agents, any subagent that collects, extracts, or processes data.

### Single-File Deliverable Rule — ALWAYS APPLY

The user reviews **one file per run**. Multi-file outputs (staging files, per-worker dumps, split reports) make review impossible.

- **Default: work in a single file.** If the task fits in one file, never split it.
- **Fan-out is allowed mid-run** (parallel workers must write separate staging files to avoid conflicts), **but the final step always consolidates**: one deliverable file with the main content (TL;DR, synthesis, plan) on top, then an `## Appendix — sources` section containing each sub-file's content (or a condensed version + link if a sub-file is bulky raw data).
- **After consolidating, delete the staging files.** The run folder ends with exactly one file (or zero, if the deliverable lives elsewhere).
- Never present the user with "see files A, B, C, D" — present one file.

### Fresh-Context Isolation — ALWAYS APPLY when fanning out workers

When the orchestrator dispatches multiple workers in parallel, pass each worker ONLY the digested context it needs — never paste a prior worker's raw output into the next worker's prompt. Pasted context induces *narrativisation*: the worker treats the preamble as "the orchestrator already framed the findings, I just classify them" instead of independently reading the source. Observed failure mode: a 5× speedup coupled with hallucinated findings and mis-cited references.

---

## Brain-First Knowledge Protocol (MUST APPLY)

Before answering any question about people, projects, strategy, decisions, or historical context:
1. Read relevant notes from `05-knowledge/` first (especially `05-knowledge/people/` for people questions).
2. If project-specific, also read related files in `04-projects/<project>/`.
3. Only then synthesize an answer.

If the user corrects a factual statement, write/update the correction in the relevant knowledge note immediately.

### Citation Rule
For factual statements written into durable notes (`05-knowledge/**`, people profiles, consolidated docs), include source attribution inline:

`[Source: [[path/to/note]] | YYYY-MM-DD | confidence: high|medium|low]`

Use one citation per distinct factual claim block where practical.

### Citation Verbatim & Verifier Pass — When Accuracy Matters

For skills that produce auditable claims about external sources (Slack threads, tickets, PRs, meeting transcripts — e.g. `team-brief`, `comprehensive-analysis`, `auto-research`), apply two additional disciplines:

1. **Verbatim quote alongside the citation.** Every cited reference should carry the actual line text in backticks, not just a link. Pattern: `[<short>] (<link>) — \`<verbatim quote>\``. If you can't quote the source verbatim, drop the claim — that's the failure mode this discipline prevents.

2. **Opt-in adversarial verifier pass before publishing.** For high-stakes briefs/reviews, after the draft is assembled, spawn one `worker-data-collector` (Sonnet) whose only job is to re-fetch each cited URL and tag every claim `Verified | Weakened | Falsified` against the verbatim quote. Falsified claims are dropped; Weakened are demoted (e.g. "blocker" → "heads up"). Output contract: `CLAIM <id> | <tag> | <one-sentence justification with link>`.

This is opt-in per skill — not a hard rule for every output. Apply it where wrongness costs the most.

---

## Engineering Discipline — ALWAYS APPLY

### Code Comments
- Never use decorative comment separator blocks of any kind — `// ====`, `// ----`, `// ---- Section Name ----`, `// -----------` full-line dividers, `/* ==== Section Name ==== */`, etc. Use plain single-line comments and blank lines to separate sections instead.

### Git
- Never `git reset --hard` or `git commit --amend` unless the user explicitly asks. Always create new commits and push normally. If changes get wiped, recover from `git reflog` — do not destroy history.
- Always commit with commitlint standards (Conventional Commits: `type(scope): subject`).
- When a command requires interactive input (e.g. `git rebase --continue`, editor prompts), supply the non-interactive flag or set `GIT_EDITOR=true` / `EDITOR=true` / `--no-edit` as appropriate.

### Pull Requests
- Before opening a PR, check the repository for a PR template (e.g. `.github/PULL_REQUEST_TEMPLATE.md` or similar) and always follow it when composing the PR description.
- PR review replies must be in-thread via `gh api repos/{owner}/{repo}/pulls/comments/{id}/replies`, never a new parent comment, then resolve the thread via the GraphQL `resolveReviewThread` mutation. No pleasantries ("great catch", etc.) — state what changed, which commit, and why.

### Interaction
- Read every file the user provides (images, screenshots, code, text) with the read tool before responding — never assume its contents.
- Answer the user before acting. Explanatory questions should be answered verbally without first invoking tools or editing code. Wait for the user to explicitly request investigation, a fix, or changes.

---

## Skill Post-Condition Rule — ALWAYS APPLY

Every skill run that **mutates external state** (publishes a page, deploys, posts to Slack/socials, transitions a ticket, pushes commits, fires a webhook) must end with an explicit **post-condition check**: fetch back or observe the mutated artifact and confirm it matches intent before reporting success.

The failure mode this prevents is **confident-but-unchecked**: a step returns plausible output that no downstream layer validates. Rules:

- The check must observe the *artifact*, not the tool's return value (curl the URL, re-fetch the ticket, screenshot the post).
- Read-only skills are exempt.
- If the check fails, report the failure plainly — never report success from the mutation call alone.
- New skills that mutate external state must include a "Verify" step in their SKILL.md.

---

## Integration Preferences

Before using any external integration in a skill, check `00-inbox/MY-INTEGRATIONS.md`:

- **Active integrations**: Use normally.
- **Disabled integrations**: Skip silently. Do not attempt to call their tools, do not suggest setting them up, do not mention them in output.
- **Unknown integrations** (not listed in either section): Ask the user if they want to set it up. If they say no, add it to the Disabled section.

## Role Packs

COG uses role packs (`.claude/roles/*.md`) to personalize skill recommendations and integration suggestions per user role.

### How role matching works
1. During onboarding, the user's role text is matched against `role_id` and `aliases` in each role pack's YAML frontmatter.
2. The matched role pack is stored as `role_pack` in `00-inbox/MY-PROFILE.md` frontmatter.
3. When suggesting skills or workflows, check the user's `role_pack` and order recommendations by role relevance.

### Role-aware behavior
- **Skill suggestions**: When a user asks "what can COG do?" or similar, prioritize skills listed in their role pack. Show role-specific explanations from the pack.
- **Integration prompts**: When a skill needs an integration the user hasn't set up, check their role pack to provide role-specific context for why it matters.
- **No role pack match**: If the user's role doesn't match any pack, recommend core skills (`roles: [all]`) and let them discover team skills organically.

### Available role packs
Role packs live in `.claude/roles/`. New roles can be added by dropping a file following the `_template.md` format.

## Vault Structure

### User configuration files (`00-inbox/`)
- `MY-PROFILE.md` — User info, role pack, agent mode, active projects
- `MY-INTERESTS.md` — Topics for daily briefs
- `MY-INTEGRATIONS.md` — Active/disabled external service integrations

### Professional tracking (`03-professional/`)
- `COMPETITIVE-WATCHLIST.md` — Companies/people being tracked

### Framework files (updated via `cog-update.sh` or `/update-cog`)
- `.claude/skills/` — Claude Code skills (31 skills)
- `.claude/agents/` — Worker agent definitions (6 agents)
- `.claude/roles/` — Role packs for personalized recommendations
- `.kiro/powers/` — Kiro powers
- `.gemini/commands/` — Gemini CLI commands
- `AGENTS.md` — Universal agent documentation

### Knowledge system (`05-knowledge/`)
- `people/` — People CRM profiles (progressive, evidence-based)
- `consolidated/` — Frameworks and synthesis documents
- `patterns/` — Identified patterns
- `timeline/` — Thinking evolution
- `booklets/` — URL bookmarks by category

### Content directories (never touched by updates)
- `00-inbox/` — Profiles, interests, integrations
- `01-daily/` — Briefs and check-ins
- `02-personal/` — Personal braindumps (private)
- `03-professional/` — Professional braindumps and strategy
- `04-projects/` — Per-project tracking
- `05-knowledge/` — Consolidated insights and patterns
