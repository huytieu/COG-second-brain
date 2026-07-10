---
name: content-factory
description: Autonomous content pipeline - scout announcements in your field, triage by trend momentum and personal angle, produce posts/blogs/videos in your voice with ledger-based dedup, hard volume caps, and screenshot-verified publishing
roles: [all]
integrations: [web-search, web-fetch]
---

# COG Content Factory Skill

## Purpose

Act as the user's autonomous content creator: scout what just happened in their field, pick what is genuinely trending, and turn it into content in their voice — with zero duplicates, hard volume caps, and verification before anything counts as published. Designed to run unattended on a schedule (nightly) and to be safely re-runnable: **an empty run is a valid run; a low-quality post is not.**

## When to Invoke

- `/content-factory` / "run the content factory"
- Scheduled runs (e.g. 2-4 times a night via cron/launchd)
- "Turn today's news into content"

## Prerequisites

Reads the user's voice and beats from `00-inbox/MY-PROFILE.md` and topics from `00-inbox/MY-INTERESTS.md`. Publishing targets come from `00-inbox/MY-INTEGRATIONS.md` — skip disabled channels silently.

## State Files (read FIRST, update LAST — this is the dedup backbone)

- `04-projects/content-factory/ledger.md` — everything ever covered/published (topic slug, source URL, formats, links, date). NEVER cover a topic or source URL already in the ledger unless there is genuinely NEW news (a follow-up release counts; rephrasing the same launch does not).
- `04-projects/content-factory/tonight-<YYYY-MM-DD>.md` — tonight's run log (create on first run of the night). Records what earlier runs scouted, parked, produced, and published, plus the remaining volume budget.
- `04-projects/content-factory/sources.md` — the watchlist. Add sources you find valuable; prune dead ones.

## Volume Budget (across ALL runs of one night, hard caps)

| Channel | Max/night | Notes |
|---------|-----------|-------|
| Short social posts/threads | 2 | the volume channel; a thread counts as 1 |
| Blog post | 1 | only when substance justifies it |
| Short video | 1 | only if the idea is visual/demo-able |
| Long-form professional post | 1 | only for a strong professional angle |
| Long video / deep essay | 0 | never autonomous; propose in the run log |

Track the budget in the tonight file. Later runs inherit what is left. Adjust caps to taste — the invariant is that caps exist and are enforced across runs, not per run.

## Phase 1 — SCOUT (every run)

1. Web-search for last-24h announcements across the user's watchlist topics, plus anything already trending.
2. Fetch the watchlist blogs/changelogs in `sources.md`.
3. If a browser integration is available, skim the user's social feeds for engagement signals — raw engagement numbers are the best trend signal.
4. Timebox scouting to ~20 minutes of work.

## Phase 2 — TRIAGE (score, don't vibe)

Score each candidate 1-5 on:
- **(a) trend momentum** — are major accounts and aggregators talking about it NOW?
- **(b) beat fit** — does it fit one of the user's beats (from MY-PROFILE.md)?
- **(c) unique angle** — can we add something ONLY this user can add (an experiment, a practitioner take, a contrarian read) — not a summary anyone could write?

Sum ≥11 → produce. 8-10 → park in the tonight file for a later run to re-score. <8 → ignore.

Dedup check before producing: topic slug + source URL against the ledger AND against the user's recent published posts (last ~20) if reachable.

## Phase 3 — PRODUCE (format ladder — decide by substance, not ambition)

- **Default: one short post or thread** — hook line, media attached, link last, minimal hashtags.
- **Blog post** only when there are ≥3 original things to say or a real proof-of-concept with artifacts. If the user has a PoC beat: actually build the tiny PoC (timebox ~45 min) and publish the REAL result, including failures. Never fabricate PoC outcomes; "it broke here" is good content.
- **Short video** when the idea is visual or demo-able in ≤60s.
- Cross-link everything (video ↔ blog ↔ thread reference each other).

## Phase 4 — PUBLISH (safety gates)

1. **Environment gate**: if the publishing surface is unavailable, or the user appears to be actively using the browser/machine — DO NOT publish. Write finished bundles to `04-projects/content-factory/out/<date>/` and let a later run (or the user) publish.
2. **Post-condition check (mandatory)**: after every publish, observe the artifact — screenshot the live post, curl the live URL — before recording it as published. Never report success from the publish call alone.
3. Never engage in arguments, never quote-dunk, never reply to strangers. The factory only creates original posts on the user's own surfaces.
4. Any screenshot must pass a credentials check (no account emails, tokens, or internal URLs visible).
5. Never delete an already-engaged post; edit in place if a fix is needed.

## Phase 5 — LEDGER + LOG (always, even for empty runs)

- Append published items to `ledger.md`: `| date | slug | beat | formats | source URL | published links |`.
- Update `tonight-<date>.md`: scouted list, scores, parked items, budget left, what the next run should look at first.
- If a big announcement deserves long-form treatment the user should shape, write it as a proposal in the tonight file with a suggested outline — do not attempt it autonomously.

## Voice Checklist (delete the draft if any fail)

- [ ] Sounds like a builder sharing, not a news bot ("I tried", "I broke", "here's what surprised me")
- [ ] Contains at least one thing only this user could say (their setup, their numbers, their PoC, their lens)
- [ ] No AI-slop vocabulary ("game-changer", "revolutionary", "unleash"), no emoji walls, hashtags within caps
- [ ] Media attached; link present; nothing confidential
- [ ] Not a duplicate (ledger + recent posts checked)

## The Loop (see /loop-engineering)

Each night is a scan-until-budget-dry loop across runs: the tonight file is the shared loop state, the ledger is the dedup verifier, the volume budget is the hard cap, and the voice checklist is the quality gate. Termination: budget exhausted, nothing scores ≥11, or the environment gate blocks publishing.
