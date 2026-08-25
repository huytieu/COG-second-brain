# Changelog

All notable changes to COG (Cognition + Obsidian + Git) will be documented in this file.

## [3.12.0] - 2026-08-25

### Changed

#### The verification harness is opt-in, not mandated
Reported in [#43](https://github.com/huytieu/COG-second-brain/issues/43): `CLAUDE.md` carried four **ALWAYS APPLY** sections mandating the V-model harness on every task, while `WORKFLOW.md` opened by asserting that "every non-`tiny` task walks the V." Nothing in a normal COG session does that, and a mandate no session honors teaches the model to discount every other rule in the file. The harness is good machinery for the runs that want it and pure ceremony on a braindump.

- `CLAUDE.md`: the four sections (V-Model Checkpoints, Closed-Loop Execute, Risk Lanes, Ultragoal) collapse into one **Verification Harness (opt-in, off by default)**. It names the three ways to turn the harness on and states plainly that a session which never invoked it owes no checkpoints, no lane classification, and no evidence ledger. Two rules survive as always-on because they cost nothing: verification observes the artifact, and a worker never grades its own homework.
- `WORKFLOW.md`: new **Scope: opt-in only** section at the top. The V-model text now reads "inside a harness run, every non-`tiny` task walks the V."
- Third opt-in path: `verification_harness: on` in `00-inbox/MY-PROFILE.md` makes the `normal`-lane pipeline the default for build tasks. Absent or `off` means per-request. Added to the onboarding profile template.
- `AGENTS.md`, `README.md`: the harness section leads with opt-in; per-skill trigger lists no longer claim the loop fires "automatically, whenever a task mutates external state".

### Fixed

#### Harness references that pointed at files COG never shipped
Also from [#43](https://github.com/huytieu/COG-second-brain/issues/43): the skills instructed the model to copy templates from `04-projects/harness/templates/`, a directory that does not exist in a COG checkout, and `WORKFLOW.md` closed with an **Install** block calling `.claude/lib/install-harness.sh`, a script that does not exist either. `checkpoint.sh init` would have failed on the same missing template path.

- Templates now ship with the skills, so `/update-cog` keeps them current: `closed-loop/references/spec-template.md`, `closed-loop/references/report-template.html` (self-contained, theme-aware), `retro/references/retro-template.md`, `review-cockpit/references/session-review-template.md`. All four added to the updater's framework file list.
- `checkpoint.sh init` writes the evidence-ledger header inline instead of copying a missing file.
- The Install block is replaced by **No install step**: the two `.claude/lib` scripts ship executable, run directories are created on demand, and COG ships no hooks. The `harvest` nightly block no longer calls the phantom installer, and the `harvest` trigger list no longer claims a SessionEnd hook stages automatically.
- `/execute` never existed as a command; every reference now points at `/closed-loop`. `WORKFLOW.md`'s domain-routing and self-enhancement tables listed skills COG does not ship (`dogfood-release`, `aut-skill-capture`, gstack, lizard) and now list the ones it does.
- Vault-specific leakage removed from the harness surface: the `browser-harness` Python helpers in `closed-loop`, and the `Agent(model="fable")` call shape in `WORKFLOW.md`.
- `CLAUDE.md` said `.claude/agents/` holds 6 agents; it holds 10, and `.claude/lib/` was missing from the framework file list.

## [3.11.0] - 2026-08-24

### Added

#### Structural slop: composition-level anti-slop rules
Word bans catch surface slop ("delve", em dashes); the deeper LLM tell is composition — predictable rhetorical structure with low information gain. Community evidence converged on this: large-scale analyses of perceived AI writing found flat rhythm and polished-but-empty paragraphs outrank word-level tells, and recurring complaints target invented frameworks ("the gate: four decisions"), rhetorical-function headings ("What this is not", "Why this matters"), and straw-man contrasts ("It's not X, it's Y").

- `no-ai-slop` skill: new **Structural slop** section — frameworkification, rhetorical-function headings, negative runway, straw-man corrections, symmetrical exposition, section scaffolding over thin content, artificial resolution, and the master check of marginal information density per paragraph. Composition order: finding → evidence → reasoning → decision, not principle → framework → exposition → takeaway.
- `no-ai-slop` eval: six matching structural checks.
- CLAUDE.md + .cursorrules: **Response Style (ALWAYS APPLY)** section so the rules govern every response, not only draft-editing runs (same hoisting rationale as 3.10.1 — behavioral rules cannot live only in a lazily-loaded skill).
- All 10 agent definitions: compact Response Style block, so subagent reports follow the same composition rules as the lead.

## [3.10.2] - 2026-08-18

### Changed

#### Oversized skill bodies split into bundled `references/`
Everything after a skill's frontmatter loads into context the moment the skill triggers. Five SKILL.md bodies ran past the 500-line figure in the Agent Skills best-practices guidance, the largest at 87 KB, so a task that never touched the appendix material paid for it anyway. Lookup tables and document templates now live in `references/` files the model reads only when it needs them, following the shape `museum-art`, `data-forms` and `editorial-illustrations` already use.

| skill | body before | body after |
|---|---|---|
| `knowledge-consolidation` | 870 | 293 |
| `onboarding` | 553 | 304 |
| `team-brief` | 886 | 473 |
| `product-ui-taste` | 649 | 515 |
| `taste-skill` | 1204 | 786 |

Every move is verbatim. `product-ui-taste` lands just above the guideline and `taste-skill` well above it: what remains in both is live instruction rather than lookup material, and condensing it would be an editorial rewrite with real behavioral risk, not a mechanical move. Stated plainly rather than forced under the number.

### Fixed

#### Bundled reference files now actually ship to installed users
`cog-update.sh` enumerates individual files in `FRAMEWORK_FILES`, and no `references/*.md` had ever been listed. The 13 files under `museum-art/references/`, `data-forms/references/` and `editorial-illustrations/references/` therefore never reached anyone who installed COG — `museum-art`'s own `## References` section pointed at files those users did not have. All 27 reference files are now registered.

**Existing installs: run `./cog-update.sh` twice for this release.** Your local copy of the updater carries the old `FRAMEWORK_FILES` array, so the first run delivers the trimmed skills and the new updater but not the reference files the new array names; the second run picks them up.

Reported in #29, with the measurements reproduced exactly.

## [3.10.1] - 2026-08-18

### Fixed

#### The daily journal is actually ambient now
`daily-journal` described itself as an automatic, passive log the agent keeps for you, but it logged nothing until you invoked it. The cause was architectural, not a missing instruction: the behavioral trigger ("append after finishing a meaningful unit of work") lived inside `SKILL.md`, and a skill body is lazily loaded, so the instruction telling the agent to act ambiently was itself locked behind the manual trigger.

A behavioral trigger cannot live in a lazily loaded file. The trigger now lives on the always-loaded surfaces and the skill body keeps the procedure.

- **`CLAUDE.md`** gains a `## Daily Journal (ALWAYS APPLY)` section carrying the trigger, the do-not-log list, and an explicit opt-out.
- **`.cursorrules`** gains the same rule in its own register, since Cursor does not read `CLAUDE.md`.
- **`AGENTS.md`** names `CLAUDE.md` as the trigger's home so the surfaces agree.
- **`SKILL.md`** stops claiming to be its own trigger and points at where the trigger actually lives.
- `01-daily/journal/` now ships with a `.gitkeep` so the destination exists on a fresh clone.

Also fixes a dangling reference in `daily-journal`'s purpose line: it compared itself to `/daily-checkin`, which this repo does not ship. The skill is `/weekly-checkin`.

Reported in #26, with the correct diagnosis.

## [3.10.0] - 2026-08-07

### Added

#### Agent Plugins standard adoption
COG now conforms to the [Agent Plugins specification 1.0.0](https://agent-plugins.org), the open, vendor-neutral plugin format governed by a Technical Steering Committee with representatives from Amazon, Cursor, Microsoft, OpenAI, and Vercel. Any standard-conformant client can load COG as a plugin directly from a checkout.

- **`plugin.json`** at the repo root: the standard manifest, validated against the published 1.0.0 schema.
- **`skills/`** at the repo root: generated mirror of `.claude/skills/` (the spec's fixed skill location; skills follow the [Agent Skills](https://agentskills.io) format). `.claude/skills/` stays canonical: regenerate with `./scripts/build-agent-plugin.sh`, never edit `skills/` by hand.
- **`scripts/build-agent-plugin.sh`**: one-command mirror rebuild, wired into `cog-update.sh` so framework updates regenerate the surface automatically.
- **Validator coverage**: `validate-agent-surface.sh` now checks the manifest declares the 1.0.0 schema, the mirror matches `.claude/skills/` exactly, and the version is aligned across all four packaging manifests.

### Changed
- Version alignment check now spans `.claude-plugin/plugin.json`, `plugin.json`, `marketplace-entry.json`, and `COG-VERSION`.

## [3.9.0] - 2026-07-29

### Added

#### Antigravity agent format support
A full native surface for Antigravity (agy CLI + IDE), matching Claude Code's coverage: all 33 skills and all 10 agents (6 workers + 4 verifiers).

- **`.agents/skills/<name>/SKILL.md`** — one pointer stub per skill. Each stub carries the same `name`/`description` frontmatter as its Claude Code counterpart, then delegates: "Read `.claude/skills/<name>/SKILL.md` and execute it exactly as written — that file is the authoritative playbook." `.claude/skills/` stays the single source of truth; the Antigravity surface never forks the playbook content.
- **`.agents/agents/<name>.md`** — one pointer stub per agent, same pattern. Read-only verification gates (`task-verifier`, `integration-verifier`) get accurate, non-templated pointer text rather than the generic worker "Output Rule" line, since they don't write files.
- **`.agents/rules/cog.md`** — the Antigravity operating-policy entry point. Reads `CLAUDE.md` at the repo root and applies it, with explicit substitutions: `.claude/agents/<name>` workers → `.agents/agents/<name>.md` via `invoke_subagent`; the Model Routing table's `sonnet` → `model: flash`.

### Changed
- **Agent Support Matrix** (`README.md`, `docs/AGENT-SUPPORT.md`) now lists Antigravity as a full surface alongside Claude Code and `AGENTS.md`.
- `cog-update.sh` `FRAMEWORK_FILES` gained all 44 `.agents/*` paths, so `/update-cog` keeps the Antigravity surface current going forward.
- Packaging rule 2 in `docs/AGENT-SUPPORT.md` now requires updating the matching Antigravity stub whenever a Claude Code skill changes.

### Known follow-up
- `scripts/validate-agent-surface.sh` does not yet check `.agents/` parity against `.claude/skills/` — drift between the two surfaces would currently go undetected by the validator. Left out of this change to keep it scoped to adding the surface itself.

## [3.8.1] - 2026-07-27

### Added

#### Paired anti-slop design skills (2)
The two skills held back from v3.8.0 pending a provenance check, now confirmed original and shipped. They are a **pair with a hard boundary**, because the two surfaces fail in opposite ways and a single "make it look good" skill gets both wrong.

- **`taste-skill`**: landing pages, portfolios, marketing, editorial. Most model design output is bad because it jumps to a default aesthetic instead of reading the room, so this forces a one-line **Design Read** (page kind, audience, vibe signals, existing brand assets, quiet constraints) before any code. Explicit variance/motion/density dials, real design systems where they apply, audit-first on redesigns, strict pre-flight check.
- **`product-ui-taste`**: dashboards, data tables, forms, wizards, settings, list/detail, admin consoles, app shells. Marketing UI lives on first impression; product UI lives on the hundredth use, under real data, by someone doing a job. The failure mode is not a templated aesthetic, it is a prototype that dies on contact with real data. Forces a **Product Read** and three dials (`DENSITY`, `DATA_COMPLEXITY`, `CONSEQUENCE`), budgets the frame in pixels top-down before content, and enforces the anti-defaults: rows instead of card-soup, correct scroll ownership, sticky headers, frozen-column offsets, z-index tiers, plus the states marketing UI never has (read-only, permission-denied, plan-locked).

**The boundary is the point.** `taste-skill` hands dense product UI to `product-ui-taste`; never run both on the same component. On a mixed brief (a landing page with an embedded live dashboard), `taste-skill` takes the hero and `product-ui-taste` takes the product surface.

Both resolve the host design system's **real** API before writing UI rather than inventing component props, and map across Carbon, Polaris, Atlaskit, Fluent, Primer, Material 3, Radix/shadcn, and Ant.

### Changed
- **Skill count 31 → 33** across all manifests, `AGENTS.md`, `README.md`, `SETUP.md`, `.github/MARKETPLACE.md`, and `docs/AGENT-SUPPORT.md`.
- `.gitignore` now covers harness runtime artifacts (`.claude/logs/`, `04-projects/harness/runs/`), which `checkpoint.sh` and `/execute` write per-user and which should never land in a user's commits.
- `.github/MARKETPLACE.md` release checklist gained the three steps that were being done by hand: refresh the packaged-version line, cut a GitHub Release, re-index the directories.

## [3.8.0] - 2026-07-27

### The Closed-Loop Harness

v3.7.0 made trust a runtime decision for stored facts and mutations. v3.8.0 asks the harder question: **who checks the checker?**

The unit of work in v3.7.0 was a skill run. A skill run reports success. Nothing above it decides whether that success was real, because the only thing that ever looked at the result was the agent that produced it. That is not a verification problem, it is a *structural* one. The worker grades its own homework.

v3.8.0 replaces the flat skill run with a **V-model lifecycle**. Work descends the left arm (goal → falsifiable criteria → tasks), builds at the apex, and ascends the right arm through gates that each demand **evidence traced back to a criterion ID**. A criterion with no evidence row does not ship. An evidence row with no criterion is noise. The verifier is a separate agent, read-only, with fresh context and no access to the worker's narrative. It looks at the artifact.

Two ideas do most of the work:

- **The worker never grades its own homework.** Verification is a different agent, observing the artifact (curl the URL, re-read the file on disk, screenshot the page), never the summary the worker wrote about it.
- **Ceremony scales with blast radius.** Five risk lanes mean a one-line fix doesn't pay for a spec and an integration verifier, while a publish does.

Closed-loop execution and the risk-lane concept are adapted from [dwarves-kit](https://github.com/dwarvesf/dwarves-kit); the V-model framing comes from SDLC practice.

### Added

#### New Skills: Verification Harness (5)
- **`closed-loop`**: the execute pipeline is CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify → CP-5 acceptance. Dispatches a fresh-context, read-only `task-verifier`, routes `FAIL:fixable` to `fix-agent` (max 2 retries), escalates otherwise. Every verify step emits `EVIDENCE <AC-id> | <CP> | PASS|FAIL | <observation> | <artifact>`.
- **`ultragoal`**: for goals too big to ship in one session. One spec with a north-star and `AC-n` criteria, decomposed into phases, each phase a complete closed-loop run with its own evidence bundle. A living `STATUS.md` lets a cold session resume without re-reading history. Two acceptance gates: per-phase, and a final north-star verifier that checks every criterion has a PASS row. Ultragoals never downgrade the lane, because wrongness compounds across sessions.
- **`harvest`**: captures durable session learnings (corrections, rejected outputs, non-obvious discoveries, repeated friction) at the session boundary and **stages** them. Auto-promoting session noise into durable knowledge poisons the well, so nothing reaches `05-knowledge/` without approval.
- **`retro`**: CP-7. Audits not just whether checkpoints passed but whether the **evidence was any good**: did each row observe an artifact, or restate a tool return value? Identifies which gates caught real problems and which were ceremony.
- **`review-cockpit`**: one living review doc per multi-item session. Cockpit header (Progress / Working folder / Context) plus per-item cards with a **🗒 Your call** approval slot you edit in place. The doc is the interaction surface, not a summary of it.

#### New Skills: Craft (5)
- **`no-ai-slop`**: edit a draft sharper while preserving voice, or detect slop without rewriting. Guards both failure directions: leaving AI patterns in, and stripping distinctive voice out along with them. Vendored from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT, with `LICENSE` and `SOURCE.md`).
- **`editorial-illustrations`**: a generative guide, not a template gallery. Teaches the **claim → geometry** method: extract what the text argues, find where the point is, derive the right geometry from the claim's shape, then render a self-contained, theme-aware, reduced-motion-safe HTML/SVG figure with a grayscale ramp and exactly one accent.
- **`data-forms`**: 20+ chart and diagram forms with when-to-use and failure modes, plus the encoding decisions that carry across all of them (takeaway headline, direct labels, kill the axis, highlight-and-mute, show the caveat). Style-agnostic: a repertoire, not a palette.
- **`museum-art`**: source real public-domain artwork from museum open-access APIs (Met, Cleveland, SMK, Rijksmuseum, NGA, Art Institute of Chicago, Getty, Smithsonian) instead of AI-generated or stock imagery. Keyless recipes per institution, licensing rules included, fetched fresh so visuals don't repeat.
- **`daily-journal`**: a passive work journal the agent keeps *for* you. Appends entries after meaningful work; the record exists even on days you'd never sit down to write one.

#### New Agents (4)
All read-only except `fix-agent`, all fresh-context, none can mutate external state:
- **`task-verifier`** (CP-3v): checks worker output against acceptance criteria by observing the artifact.
- **`integration-verifier`** (CP-4): cross-task wiring and global acceptance for multi-task specs.
- **`fix-agent`**: targeted fixes after a `FAIL:fixable` verdict; implements only what the verifier flagged, max 2 attempts.
- **`harvest-curator`** (CP-7): shapes session learnings into adoption notes; propose-only.

#### New Framework Files
- **`WORKFLOW.md`**: the V-model lifecycle covers checkpoint table, gate classes (blocking vs advisory), the evidence row contract, risk-lane checkpoint depth, the verification pipeline, and file homes for specs, evidence bundles, and retro output.
- **`.claude/lib/checkpoint.sh`**: records checkpoint results to a run's evidence ledger.
- **`.claude/lib/lane-classify.sh`**: classifies a task into a risk lane (`classify` for the verdict, `explain` for the reasoning).

#### New Protocols in CLAUDE.md
- **V-Model Checkpoints**: CP-1 through CP-7 with per-lane blocking rules, the two-way verification requirement, and the **cross-model flagship gate**: on high-stakes runs, overlay a flagship model that is *not* the lead's own as advisor at CP-1 and critic at CP-4/5/6. Same-family verifiers share the lead's blind spots; a different family catches a different error class.
- **Closed-Loop Execute**: the pipeline, the five lanes, and when a verifier subagent is actually warranted. Notably: on `normal`-lane read-only work the lead verifies inline, because spawning an agent to re-read a file the lead just wrote buys nothing.
- **Risk Lanes**: `tiny` / `normal` / `full` / `bug` / `backfill`, classified before executing.
- **Ultragoal**: one spec, phases as full closed-loop runs, a living status ledger, two acceptance gates.
- **Visual Verification**: UI/UX work is not verified by a DOM check. The DOM can be present and the pixels still wrong. Capture the render, *read the image*, name the discrepancy, fix it, re-capture.
- **Delegation Cap**: delegation costs context re-establishment on both ends. Fan out only for genuinely independent, sizeable tracks; if one subagent can do it, use one.

### Changed
- **Skill count 21 → 31**, **agents 6 → 10** across `plugin.json`, `.cursor-plugin/plugin.json`, `marketplace-entry.json`, `AGENTS.md`, `README.md`, `SETUP.md`, `.cursorrules`, `.github/MARKETPLACE.md`, and `docs/AGENT-SUPPORT.md`.
- **Model Routing table** extended with the four new agents (all Sonnet).
- **`cog-update.sh`**: `FRAMEWORK_FILES` now covers the 10 new skills, 4 new agents, `WORKFLOW.md`, and both `.claude/lib/` scripts.
- Version bumped to **3.8.0** across `COG-VERSION` and all manifests.

## [3.7.1] - 2026-07-10

### Added

#### Engineering Discipline protocol in CLAUDE.md
Operating rules for agents doing engineering work through COG:

- **Code comments** — no decorative comment separator blocks (`// ====`, `/* ==== Section ==== */`, full-line dividers); plain comments and blank lines separate sections.
- **Git** — never `git reset --hard` or `git commit --amend` unless explicitly asked; new commits only, recover via `git reflog`. Commitlint / Conventional Commits standards. Non-interactive flags (`GIT_EDITOR=true`, `--no-edit`) for commands that would prompt.
- **Pull requests** — check for and follow the repo's PR template; review replies in-thread via `gh api .../pulls/comments/{id}/replies` (never a new parent comment), resolve threads via GraphQL `resolveReviewThread`, no pleasantries — state what changed, which commit, and why.
- **Interaction** — read every user-provided file before responding; answer explanatory questions verbally before invoking tools, and wait for an explicit request before investigating or changing code.

### Changed
- Version bumped to **3.7.1** across `COG-VERSION` and all plugin manifests.

## [3.7.0] - 2026-07-10

### Runtime Trust

v3.6.0 taught iterative skills to trust mechanical checks over self-report. v3.7.0 extends the same philosophy to everything COG stores and everything COG publishes: **trust is a runtime decision, not a property of a stored item or a returned status code.** Two failure modes drive this release (adapted from "From Model Scaling to System Scaling: Scaling the Harness in Agentic AI", Gu, UC Berkeley, arXiv:2605.26112):

- **stale-but-confident** — a memory that was correct when written silently drifts after the environment changes, yet still ranks high at recall and gets acted on.
- **confident-but-unchecked** — a mutation step returns plausible output that no downstream layer validates.

### Added

#### New Skills
- **`memory-hygiene`** (`.claude/skills/memory-hygiene/SKILL.md`) — periodic trust sweep of persistent memory and durable knowledge notes. Classifies claims (environment-dependent vs preference/judgment), re-verifies the former against the live environment with cheap checks (`ls`, `curl`, `gh`), stamps `last_verified` + `confidence` into frontmatter, fixes verified-wrong facts in place, and proposes (never auto-applies) archiving obsolete entries. One sweep report per run with a drift scorecard and deltas vs the previous sweep.
- **`content-factory`** (`.claude/skills/content-factory/SKILL.md`) — autonomous content pipeline designed for unattended scheduled runs: scout → triage (scored 1-5 on trend momentum, beat fit, unique angle) → produce (format ladder decided by substance) → publish (environment gate + mandatory post-condition check) → ledger. Ledger-based dedup, hard per-night volume caps shared across runs, and a voice checklist where any failure deletes the draft. An empty run is a valid run.

#### New Protocols in CLAUDE.md
- **Skill Post-Condition Rule** — every skill run that mutates external state must end by observing the mutated *artifact* (curl the URL, re-fetch the ticket, screenshot the post), never just the tool's return value. Read-only skills exempt. New mutating skills must ship a "Verify" step.
- **Citation Verbatim & Verifier Pass** — for skills producing auditable claims about external sources: (1) every citation carries the actual line text in backticks — if you can't quote it verbatim, drop the claim; (2) opt-in adversarial verifier pass that re-fetches each cited URL and tags claims `Verified | Weakened | Falsified` before publishing.
- **Fresh-Context Isolation** — when fanning out parallel workers, pass each only the digested context it needs; pasting a prior worker's raw output induces *narrativisation* (the worker classifies the orchestrator's framing instead of independently reading the source).
- **Single-File Deliverable Rule** — one deliverable file per run: fan-out staging is fine mid-run, but the final step consolidates (synthesis on top, appendix of sources) and deletes staging files.

#### New Documentation
- **`docs/SKILL-DISTILLATION.md`** — the "explore once, execute cheap" meta-pattern: one expensive exploration by a strong model distilled into a layered skill artifact (router / recipes / healing tree / map shards) that a small model executes at a fraction of the cost. Includes the PASS / FAIL-REAL / FAIL-STALE / BLOCKED verdict taxonomy that routes "the world changed" to skill maintenance and "the world is wrong" to real reporting. Field-validated: $4.63 exploration once → $0.11 per execution on a Haiku-class model.

### Changed
- Skill count 19 → **21** across README, SETUP, AGENTS.md, CLAUDE.md, MARKETPLACE.md, docs/AGENT-SUPPORT.md, and all plugin manifests.
- CONTRIBUTING.md skill guidelines: mutating skills must ship a Verify step; don't write "show your reasoning" instructions into skills (reasoning models handle it internally — state goals and constraints instead).
- Version bumped to **3.7.0** across `COG-VERSION`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `marketplace-entry.json`; added runtime-trust keywords for marketplace discoverability.

## [3.6.0] - 2026-06-22

### Loop Engineering for Iterative Skills

Skills whose work is genuinely iterative now carry explicit loop-engineering structure: a named loop, a deterministic verifier, layered termination conditions, and in-loop context management. This extends COG's verification-first philosophy from "sources required" to "trust mechanical checks, never the agent's own self-report."

### Added

#### New Skill
- **`loop-engineering`** (`.claude/skills/loop-engineering/SKILL.md`) — canonical COG loop vocabulary and design aid: the act-observe-verify cycle, the five termination conditions (deterministic verifier, hard cap, budget guard, no-progress detection, human escalation), in-loop context management (compaction, pruning, externalize-to-vault, sub-agent isolation), a named-pattern table, and failure modes. Documented in AGENTS.md and registered across all marketplace manifests.

#### Per-Skill Loop Sections
- **daily-brief**: verify-retry loop. Search → fetch → deterministic verify (7-day window + source tier + 2-source minimum + dedup) → re-search until enough verified items or stop condition. No-progress detection replaces backfilling with stale news.
- **knowledge-consolidation**: loop-until-dry extraction with a completeness critic. Traceability and coverage are mechanical checks; per-domain worker isolation in team mode.
- **url-dump**: fetch-retry loop with a quality gate. Retry failed fetches a different way, gate on extraction quality and confidence, escalate to the user instead of filing low-confidence guesses.
- **weekly-checkin**: per-domain scan loop plus human-in-the-loop reflection, gated by a coverage checklist over active projects and domains.

### Fixed

#### Marketplace Manifest Consistency
- **`scout`** skill is now registered in `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `cog-update.sh` (it shipped as a skill but was missing from the manifests, which failed `scripts/validate-agent-surface.sh`).
- Skill count corrected to **19** across plugin.json, cursor manifest, MARKETPLACE.md, and architecture metadata.
- `marketplace-entry.json` version realigned with `plugin.json` and `COG-VERSION`.

### Changed
- Version bumped to **3.6.0** across `COG-VERSION`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `marketplace-entry.json`.
- Added `loop-engineering` / `agent-loop` keywords to manifests for marketplace discoverability (skills.sh, agentskill.sh, cursor.directory).

### Skills Skipped (loops add little)
- **braindump** (linear capture), **onboarding** (already conversational human-in-the-loop).

## [3.5.0] - 2026-04-16

### Specialist Sessions, People CRM & Worker Agents

COG now includes a worker agent architecture (inspired by [garrytan/gstack](https://github.com/garrytan/gstack) specialist sessions and [garrytan/gbrain](https://github.com/garrytan/gbrain) knowledge patterns), a people CRM system with tiered enrichment for progressive team knowledge, and operational protocols that make multi-agent workflows faster and more reliable.

### Added

#### Worker Agent Architecture (`.claude/agents/`)
- **`worker-data-collector`** — Structured extraction from GitHub, Slack, Jira, Linear, or file system (Sonnet)
- **`worker-researcher`** — Web research with source citations and evidence extraction (Sonnet)
- **`worker-file-ops`** — Vault file operations, metadata updates, profile maintenance (Sonnet)
- **`worker-executor`** — Pre-approved mutations: Jira transitions, Linear updates, API calls (Sonnet)
- **`worker-publisher`** — Publishing to Slack, Confluence, Notion, webhooks (Sonnet)
- **`brief-people-updater`** — Batch-update people profiles from meetings, briefs, and Slack data (Sonnet)

#### People CRM System
- **`05-knowledge/people/README.md`** — People CRM documentation with design principles, file naming, citation format
- **`06-templates/people-profile-template.md`** — Two-layer profile template (Compiled Truth + append-only Timeline)
- Progressive, evidence-based profiles built from meetings, Slack, PRs, and daily interactions
- Mandatory source citations with confidence levels (high/medium/low)

#### Operational Protocols in CLAUDE.md
- **Model Routing** — Sonnet workers for data collection/publishing, Opus lead for reasoning/synthesis
- **Worker Output Rule** — Workers write to `/tmp/` files and return only a status + path (eliminates slow token generation)
- **Brain-First Knowledge Protocol** — Read `05-knowledge/` before answering people/project/strategy questions
- **Citation Rule** — Source attribution required for factual statements in durable notes

### Changed (includes v3.4.1 packaging fixes)

- **`README.md`** — Added Worker Agents section, People CRM section, updated vault structure and mermaid diagrams, added agent support matrix
- **`AGENTS.md`** — Added Worker Agents documentation, People CRM commands, updated vault structure with people/ and agents/
- **`SETUP.md`** — Added worker agents and people CRM to directory structure, updated skill counts
- **`CLAUDE.md`** — Major additions: model routing, worker output rule, brain-first protocol, citation rule, knowledge system in vault structure
- **`CONTRIBUTING.md`** — Added agent contribution guidelines and coding conventions for `.claude/agents/`
- **`.claude-plugin/plugin.json`** — Bumped version, added agents metadata, updated architecture description
- **`marketplace-entry.json`** — Bumped version to 3.5.0
- **`cog-update.sh`** — Added 8 new framework files (6 agents + people README + profile template)
- **`COG-VERSION`** — Bumped 3.4.0 → 3.5.0
- **`docs/AGENT-SUPPORT.md`** — Canonical support matrix for all agent surfaces
- **`scripts/validate-agent-surface.sh`** — Release/install validator
- **`.github/MARKETPLACE.md`** — Rewritten for current package model

### Design Decisions
- **gstack-inspired specialist lanes**: Capture, Synthesis, Publishing, Team Intelligence, Repo Maintenance — clear operating gears instead of one generic agent session
- **Sonnet for I/O, Opus for thinking**: Workers handle data-heavy tasks cheaply and in parallel; the lead session does reasoning and editorial judgment
- **File-based worker output**: Writing to `/tmp/` then reading is instant; generating thousands of tokens as agent output takes minutes
- **People profiles are append-only**: Timeline history is never rewritten — only the Compiled Truth section updates as understanding evolves
- **Citation-first culture**: Every factual claim in knowledge notes traces to a source with confidence level

## [3.4.0] - 2026-03-12

### PM Workflow Skills & Auto-Research

COG now includes a complete product management workflow (6 skills) and a deep strategic research engine. PM skills cover the full lifecycle from PRD to release notes to knowledge base maintenance, with multi-tracker support (Linear, GitHub Issues, Jira) and optional Confluence/Notion publishing.

### Added

#### Auto-Research Skill
- **`auto-research`** — Deep strategic research engine inspired by Karpathy's autoresearch
  - Decomposes strategic questions into 5-7 parallel research threads
  - Spawns parallel agents (team mode) for simultaneous web research
  - Synthesizes into actionable analysis with scenarios, options, and recommendations
  - Always includes emerging tech thread for pre-mainstream concepts
  - Saves to `05-knowledge/research/`

#### PM Workflow Skills (6 new skills)
- **`create-user-story`** — Create user stories with duplicate checking
  - Multi-tracker: Linear (MCP), GitHub Issues (`gh` CLI), Jira (API)
  - Standard As a/I want/So that format with Given/When/Then acceptance criteria
  - Automatic duplicate detection before creation
- **`generate-prd`** — Draft product requirement documents
  - Standard sections: Problem, Goals, Non-goals, User workflows, Requirements, Risks, Metrics
  - Approval gate before any external publishing
  - Saves to `04-projects/[project]/PRDs/`
- **`generate-release-notes`** — Generate release notes from any source
  - GitHub milestones, Linear cycles, or manual input
  - Auto-categorizes: Enhancements, Technical Improvements, Bug Fixes
  - Saves to `04-projects/[project]/releases/`
- **`export-open-issues`** — Audit and export open issues
  - Multi-tracker support with stale issue detection
  - Priority distribution and assignee load analysis
  - Saves structured report to `04-projects/[project]/audits/`
- **`publish-to-confluence`** — Publish vault markdown to Confluence
  - Create or update pages with approval gate
  - Requires Confluence integration active
- **`update-knowledge-base`** — Maintain product knowledge base
  - Accepts feature updates, release data, or both
  - Cross-references PRDs and release notes
  - Optional Confluence/Notion sync with approval

#### Skill Metadata
- All 7 new skills have `roles` and `integrations` fields in YAML frontmatter
- PM skills: `roles: [product-manager, engineering-lead, founder]`
- Auto-research: `roles: [product-manager, engineering-lead, founder, all]`

### Changed

#### Documentation
- **`README.md`** — Added PM Workflow Skills section, Strategic Research section, updated mermaid diagrams, vault structure (17 skills), roadmap
- **`AGENTS.md`** — Added 7 new skill commands with full documentation, PM Workflow lifecycle description
- **`SETUP.md`** — Updated skill counts (10 → 17), updated directory structure
- **`GEMINI.md`** — Updated available skills list
- **`CLAUDE.md`** — Updated skill count to 17
- **`CONTRIBUTING.md`** — No structural changes needed (existing conventions apply)
- **`CHANGELOG.md`** — This entry

#### Version & Metadata
- **`COG-VERSION`** — Bumped 3.3.0 → 3.4.0
- **`.claude-plugin/plugin.json`** — Bumped version, updated skill count to 17, added 7 new skills
- **`marketplace-entry.json`** — Bumped version to 3.4.0
- **`cog-update.sh`** — Added 7 new skills to FRAMEWORK_FILES array

### Design Decisions
- **Multi-tracker architecture**: PM skills check `MY-INTEGRATIONS.md` and work with Linear, GitHub, or Jira — graceful degradation when trackers are unavailable
- **Approval gates**: Publishing to external services (Confluence, Notion) always requires explicit user confirmation
- **Vault-first output**: All PM artifacts save to vault (`04-projects/`, `05-knowledge/`) before any external publishing
- **PM lifecycle flow**: Skills designed as a pipeline: Research → PRD → Stories → Development → Release Notes → KB Update

---

## [3.3.0] - 2026-02-25

### Role Packs & Integration Discovery

COG now matches your role during onboarding to personalize skill recommendations and integration suggestions. A PM and an engineer see different skill priorities. New roles can be added by dropping a file.

### Added

#### Role Packs (`.claude/roles/`)
- **7 role pack files** — each defines per-role skill recommendations and integration needs:
  - `_template.md` — starter for custom roles
  - `product-manager.md` — skills: team-brief, comprehensive-analysis, meeting-transcript, daily-brief, braindump, etc. Integrations: GitHub, Linear, Slack, PostHog, Notion, HackMD
  - `engineering-lead.md` — engineering-focused with team management emphasis. Integrations: GitHub, Linear, Slack, PostHog
  - `engineer.md` — individual contributor focus. Integrations: GitHub
  - `designer.md` — design and UX research focus. Integrations: Slack, Notion
  - `founder.md` — all skills, all integrations recommended
  - `marketer.md` — growth and content focus. Integrations: Slack, Notion, PostHog
- Each role pack contains YAML frontmatter with `role_id`, `display_name`, and `aliases` for fuzzy matching during onboarding

#### Onboarding Enhancements
- **Step 5.5 — Role Pack Matching**: After extracting role text, scans `.claude/roles/*.md` for matching `role_id` or `aliases`. Presents role-specific skill and integration recommendations
- **Step 5.6 — Integration Discovery**: Presents role pack's recommended integrations with role-specific explanations. Generates `00-inbox/MY-INTEGRATIONS.md` with Active/Disabled sections
- **Updated MY-PROFILE.md template**: Now includes `role_pack` in YAML frontmatter
- **Updated WELCOME-TO-COG.md template**: New "Skills for Your Role" section with role-ordered skills, and "Your Integrations" section

#### Skill Metadata
- All 10 skills now have `roles` and `integrations` fields in YAML frontmatter
  - Core skills (onboarding, braindump, daily-brief, etc.): `roles: [all]`
  - Team skills (team-brief, comprehensive-analysis): `roles: [product-manager, engineering-lead, founder]`
  - Meeting-transcript: `roles: [product-manager, engineering-lead, founder, designer]`

#### Framework Configuration
- **`CLAUDE.md`** rewritten as universal framework file with Role Packs and Integration Preferences sections (no longer personal config)

### Changed

#### Documentation
- **`README.md`** — Added "Role Packs" section, updated vault structure diagram with `.claude/roles/`, updated roadmap
- **`SETUP.md`** — Updated skill counts, added role packs to onboarding output, added MY-INTEGRATIONS.md
- **`AGENTS.md`** — Updated onboarding command with role matching and integration discovery, added team intelligence skills, updated vault structure and configuration section
- **`GEMINI.md`** — Updated vault structure with role packs and integrations file
- **`CONTRIBUTING.md`** — Updated skill frontmatter convention to include `roles` and `integrations` fields, added role pack contribution guidelines
- **`CHANGELOG.md`** — This entry

#### Version & Metadata
- **`COG-VERSION`** — Bumped 3.2.0 → 3.3.0
- **`.claude-plugin/plugin.json`** — Bumped version, updated skill count to 10, added `rolePacks: 7` metadata
- **`marketplace-entry.json`** — Bumped version to 3.3.0
- **`cog-update.sh`** — Added 7 role pack files, CLAUDE.md, and 3 team intelligence skills to FRAMEWORK_FILES array

### Design Decisions
- **File-based role packs**: New roles added by dropping a `.md` file — no code changes needed
- **Alias-based matching**: Fuzzy matching via aliases handles variations like "PM", "product lead", "head of product"
- **Integration discovery during onboarding**: Rather than skills failing at runtime, integrations are configured upfront
- **CLAUDE.md as framework file**: Moves from personal config to universal instructions that work for any user

---

## [3.2.0] - 2026-02-09

### Upstream Update System

Users who fork or clone COG can now safely pull framework updates (skills, docs, scripts) without risking merge conflicts with their personal content.

### Added

#### Update Tooling
- **`cog-update.sh`** — Interactive bash script for updating framework files
  - `--check`: See available updates without making changes
  - `--dry-run`: Preview what would change
  - `--force`: Update all framework files at once
  - Interactive mode: Per-file prompts with diff, backup, and skip options
- **`/update-cog` skill** — Available in all 4 agent formats:
  - `.claude/skills/update-cog/SKILL.md` (Claude Code)
  - `.kiro/powers/cog-update/POWER.md` (Kiro)
  - `.gemini/commands/update-cog.toml` + `.gemini/skills/update-cog.md` (Gemini CLI)
  - `AGENTS.md` updated with `/update-cog` command (OpenAI Codex, others)
- **`COG-VERSION`** — Single-line version tracking file (currently `3.2.0`)

#### Content/Framework Separation
- **`.gitkeep` files** in all 15 content directories — preserves directory structure in upstream while `.gitignore` excludes user content
- **`.gitignore` rewrite** — Content folder ignores now active by default with `.gitkeep` whitelisting

#### Directory Structure Preservation
- `.gitkeep` added to: `00-inbox/`, `01-daily/`, `01-daily/briefs/`, `01-daily/checkins/`, `02-personal/`, `02-personal/braindumps/`, `03-professional/`, `03-professional/braindumps/`, `04-projects/`, `05-knowledge/`, `05-knowledge/consolidated/`, `05-knowledge/patterns/`, `05-knowledge/timeline/`, `05-knowledge/booklets/`, `06-templates/`

### Changed

#### Documentation
- **`README.md`** — Added "Keeping COG Updated" section, FAQ entries for updates, updated roadmap
- **`SETUP.md`** — Added comprehensive "Keeping COG Updated" section with all 3 update methods
- **`AGENTS.md`** — Added `/update-cog` command, version & updates configuration section
- **`GEMINI.md`** — Added `/update-cog` to available skills list
- **`CONTRIBUTING.md`** — Added version bump protocol to "Before You Start" section
- **`CHANGELOG.md`** — This entry

#### Integration
- **`.claude-plugin/plugin.json`** — Added update-cog skill, bumped version to 3.2.0
- **`marketplace-entry.json`** — Bumped version to 3.2.0
- **`.claude/skills/onboarding/SKILL.md`** — Added "Keeping COG Updated" to welcome guide template
- **`.kiro/powers/cog-onboarding/POWER.md`** — Added update mention to wrap-up section

### Removed
- **`example-vault/`** — Removed empty directory (contained only `.DS_Store`), replaced by `.gitkeep` files

### Design Decisions
- **Remote name `cog-upstream`**: Works for both fork and clone users without conflicting with `origin`
- **`git checkout <remote>/<branch> -- <file>`**: Surgical file replacement with zero conflict risk
- **Self-updating script**: `cog-update.sh` is in the framework file list, so it updates itself
- **Active .gitignore**: Content folder ignores are on by default so new users get safe defaults

---

## [3.1.0] - 2026-02-03

### Obsidian Tasks Plugin Integration

Tasks generated by COG skills now use the Obsidian Tasks emoji format, making them queryable in Tasks dashboards, daily notes, and date-based filters.

### Added

#### Obsidian Tasks Emoji Format
- All task items now include `📅 YYYY-MM-DD` due dates calculated from context
- **braindump**: "Immediate (24-48 hours)" → tomorrow's date, "Short-term (1-2 weeks)" → +1 week
- **daily-brief**: "Immediate Actions (Today/This Week)" → today or end of week
- **url-dump**: Practical takeaways → +1 week, Evaluation tasks → progressive dates (3 days to 2 weeks)
- **weekly-checkin**: Next steps and carry forward items → next week dates

### Changed

#### Skill Templates Updated
- `.claude/skills/braindump/SKILL.md` - Action Items section with calculated due dates
- `.claude/skills/daily-brief/SKILL.md` - Opportunities & Recommendations with due dates
- `.claude/skills/url-dump/SKILL.md` - Practical Takeaways and Evaluation Status with due dates
- `.claude/skills/weekly-checkin/SKILL.md` - Next Steps and Carry Forward Items with due dates

#### Kiro Powers Updated
- `.kiro/powers/cog-braindump/POWER.md` - Matching emoji date format
- `.kiro/powers/cog-daily-brief/POWER.md` - Matching emoji date format
- `.kiro/powers/cog-url-dump/POWER.md` - Matching emoji date format
- `.kiro/powers/cog-weekly-checkin/POWER.md` - Matching emoji date format

#### Documentation Updated
- `agents.md` - Universal documentation now mentions Obsidian Tasks format
- `README.md` - Added Obsidian Tasks compatibility to features
- `SETUP.md` - Added optional Obsidian Tasks plugin recommendation

### Example Output

Before:
```markdown
### Immediate (24-48 hours)
- [ ] Check regional availability
```

After:
```markdown
### Immediate (24-48 hours)
- [ ] Check regional availability 📅 2026-02-04
```

### Benefits

- Tasks now appear in Obsidian Tasks dashboard queries
- "Due today", "Due this week" filters work correctly
- Daily notes can pull in relevant tasks automatically
- Full compatibility with Tasks plugin workflows

### Reference

- [Obsidian Tasks Emoji Format](https://publish.obsidian.md/tasks/Reference/Task+Formats/Tasks+Emoji+Format)

---

## [3.0.0] - 2026-01-19

### Multi-Agent Support - COG Goes Agentic

This release transforms COG from a Claude Code-only system to a truly agent-agnostic second brain that works with multiple AI platforms.

### Added

#### Multi-Agent Architecture
- **`agents.md`** - Universal agent documentation for OpenAI and other agents
  - Documents all 6 skills with triggers, purposes, and outputs
  - Works with any AI that reads markdown
  - Includes vault structure and quick start guide

- **`.kiro/powers/`** - Native Kiro support with 6 powers
  - `cog-onboarding/POWER.md` - Profile setup
  - `cog-braindump/POWER.md` - Thought capture
  - `cog-daily-brief/POWER.md` - News intelligence
  - `cog-weekly-checkin/POWER.md` - Weekly reflection
  - `cog-knowledge-consolidation/POWER.md` - Framework building
  - `cog-url-dump/POWER.md` - URL bookmarking

#### New Skill
- **url-dump** - Quick capture URLs with automatic content extraction
  - Fetches and extracts content from URLs
  - Auto-categorizes into booklets (articles, tools, reference, etc.)
  - Generates insights and key takeaways
  - Saves to `05-knowledge/booklets/` or project resources

### Changed

#### Rebranding
- **COG = Cognition + Obsidian + Git** (previously Claude + Obsidian + Git)
- Positioned as "agentic second brain" rather than Claude-specific
- Updated all documentation to reflect multi-agent support

#### Documentation Updates
- **README.md** - Complete rewrite for multi-agent support
  - New prerequisites section with agent options
  - Updated directory structure showing all agent formats
  - Agent-agnostic installation instructions
  - FAQ updated for multi-agent questions

- **SETUP.md** - Multi-agent setup instructions
  - Separate setup steps for Claude Code, Kiro, and other agents
  - Updated troubleshooting for each agent type
  - Skill customization guide for all formats

- **CONTRIBUTING.md** - Multi-format contribution guidelines
  - How to add skills in all agent formats
  - Coding conventions for each format
  - Keep-in-sync guidance

### Architecture

#### Skill Formats
COG skills are now defined in three parallel formats:

| Format | Location | Agent |
|--------|----------|-------|
| SKILL.md | `.claude/skills/[name]/` | Claude Code |
| POWER.md | `.kiro/powers/cog-[name]/` | Kiro |
| agents.md | Root directory | OpenAI, others |

#### Benefits
- **Agent flexibility**: Use whichever AI agent you prefer
- **Future-proof**: Easy to add support for new agents
- **Consistent experience**: Same 6 skills across all platforms
- **No lock-in**: Switch agents without losing functionality

### Migration Guide

If upgrading from v2.x:

1. **Pull new files**:
   ```bash
   git pull origin main
   ```

2. **New files added automatically**:
   - `agents.md` - Universal documentation
   - `.kiro/powers/` - Kiro support
   - `.claude/skills/url-dump/` - New skill

3. **No breaking changes** - All existing skills and content remain compatible

---

## [2.0.0] - 2025-10-17

### Major Architecture Overhaul

This release represents a complete restructuring of COG to follow proven subagent architecture patterns, emphasizing separation of concerns and configuration-as-knowledge principles.

### Added

#### Onboarding System
- **New `/onboarding` command** - First-run setup that personalizes COG in ~2 minutes
  - Asks 6 essential questions: name, role, interests, news sources, projects, competitive watchlist
  - Creates readable markdown profile files in vault
  - No JSON configuration files - everything is human-readable markdown

#### Configuration as Knowledge
- **`00-inbox/MY-PROFILE.md`** - User's basic info, role, and active projects
- **`00-inbox/MY-INTERESTS.md`** - Topics of interest and preferred news sources
- **`03-professional/COMPETITIVE-WATCHLIST.md`** - Companies/people to track
- **`04-projects/[project]/PROJECT-OVERVIEW.md`** - Per-project overview documents
- **`00-inbox/WELCOME-TO-COG.md`** - Personalized welcome guide (auto-generated)

All configuration is now part of the knowledge base - searchable, linkable, and editable like any other note.

#### Subagent Architecture
- **`.claude/subagents/brain-dump-analyst.md`** - Specialized subagent for braindump analysis
  - Stream-of-consciousness processing
  - Domain classification
  - Theme extraction
  - Competitive intelligence detection
  - Structured output generation

- **`.claude/subagents/news-curator.md`** - Specialized subagent for news curation
  - Verified news research (7-day freshness requirement)
  - Multi-source cross-referencing
  - Strategic relevance analysis
  - Personalized briefing generation

### Changed

#### Command Architecture
Commands are now **thin orchestration layers** that delegate to specialized subagents:

**`/braindump` - Redesigned**
- Collects user's stream-of-consciousness input
- Asks for domain classification
- **Delegates ALL processing to brain-dump-analyst subagent**
- Confirms completion and shows summary
- No longer handles analysis directly

**`/daily-brief` - Redesigned**
- Reads user profile files (MY-PROFILE.md, MY-INTERESTS.md)
- **Delegates ALL news curation to news-curator subagent**
- Confirms completion and shows executive summary
- No longer searches or curates news directly

**`/weekly-checkin` - Simplified**
- Guided conversational reflection
- Direct document generation based on user responses
- Pattern identification through conversation
- No template dependency

#### Configuration Philosophy
- **Before**: Hidden JSON config files (`.claude/config/user-config.json`)
- **After**: Markdown notes in vault that are part of knowledge base
- Benefits:
  - Human-readable and directly editable
  - Searchable in Obsidian
  - Linkable from other notes
  - Version controlled with Git
  - Can include personal notes and context

### Removed

- **Deleted `templates/` directory entirely**
  - `templates/braindump-template.md`
  - `templates/daily-brief-template.md`
  - `templates/weekly-checkin-template.md`

- **Removed JSON configuration system**
  - `.claude/config/` directory and all JSON files

- **Eliminated template dependencies**
  - All content now dynamically generated based on context
  - Templates were static; dynamic generation is more flexible

### Architecture Benefits

#### Separation of Concerns
- **Commands**: Simple orchestrators that handle user interaction and delegation
- **Subagents**: Complex processors with detailed analysis frameworks and verification protocols
- Clear responsibility boundaries make system easier to understand and extend

#### Maintainability
- Commands are now < 200 lines (vs 250+ before)
- Complex logic isolated in specialized subagents
- Changes to analysis logic don't affect command structure
- Easy to add new subagents without modifying commands

#### Transparency
- All configuration visible and editable as markdown notes
- No hidden JSON files to debug
- User can see exactly what COG knows about them
- Configuration becomes part of their thinking/knowledge

#### Extensibility
- New subagents can be added by creating new `.md` files in `.claude/subagents/`
- Commands can delegate to multiple subagents as needed
- Subagents can collaborate by reading each other's outputs

### Documentation

- **README.md** - Updated to reflect:
  - Subagent architecture explanation
  - Simplified installation (no templates to copy)
  - 2-minute onboarding flow
  - Configuration-as-knowledge philosophy

- **New CHANGELOG.md** - This file, documenting all changes

### Migration Guide

If upgrading from v1.x:

1. **Remove old configuration**:
   ```bash
   rm -rf .claude/config/
   ```

2. **Remove templates**:
   ```bash
   rm -rf templates/
   ```

3. **Pull new structure**:
   ```bash
   git pull origin main
   ```

4. **Run onboarding**:
   ```
   /onboarding
   ```
   This will create your new markdown-based profile.

5. **Your existing notes are safe** - Only `.claude/` structure changed, all your braindumps, briefs, and check-ins remain unchanged.

### Technical Details

#### File Changes
- Modified: `.claude/commands/braindump.md`
- Modified: `.claude/commands/daily-brief.md`
- Modified: `.claude/commands/weekly-checkin.md`
- Modified: `README.md`
- Added: `.claude/commands/onboarding.md`
- Added: `.claude/subagents/brain-dump-analyst.md`
- Added: `.claude/subagents/news-curator.md`
- Deleted: `templates/` (entire directory)
- Deleted: `.claude/config/` (entire directory)

#### Breaking Changes
- **Configuration format changed** - Old JSON configs no longer used
- **Template system removed** - Commands that relied on templates now generate content dynamically
- **Subagent delegation required** - Commands expect subagents to exist in `.claude/subagents/`

#### Backward Compatibility
- **Existing markdown files unchanged** - All your notes, briefs, braindumps remain compatible
- **Command names unchanged** - `/braindump`, `/daily-brief`, etc. work the same from user perspective
- **Directory structure unchanged** - `00-inbox/`, `01-daily/`, etc. remain the same

### Philosophy

This release embraces two key principles:

1. **Configuration is Knowledge** - Your preferences, interests, and setup are part of your second brain, not hidden config files.

2. **Commands Orchestrate, Subagents Process** - Commands handle user interaction and context gathering; specialized subagents handle complex analysis, verification, and generation.

These principles make COG more transparent, maintainable, and aligned with the "second brain" philosophy of making all knowledge visible and editable.

---

## [1.0.0] - 2025-10-15

### Initial Release

- Basic COG structure with commands and templates
- Brain dump, daily brief, and weekly check-in functionality
- Template-based content generation
- JSON configuration system

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/).
