---
name: review-cockpit
description: Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any "do X, then plan/draft Y and Z"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses.
---

# review-cockpit

## Purpose

A single, living **review document** that doubles as the control surface for a session. Instead of scattering a meeting note here, a ticket there, two drafts in chat, everything lands in **one file** you can open in the Obsidian side panel (or Claude side panel) and drive: see progress at a glance, review each item in place, approve or request changes inline, and watch the doc update as the agent works. Mirrors a "co-work" cockpit (Progress / Working folder / Context).

## When to use

- Any session with **≥2 things you need to review or approve** (the default for "process X then plan/draft Y, Z").
- Meeting-processing + pod planning, multi-ticket runs, briefs with several drafts, spec + plan + drafts.
- NOT for a single trivial deliverable (one file, no approval loop) — a plain file is fine there.

Pairs with `closed-loop` (verification), `harvest` (learnings), and the V-model checkpoints. This skill governs **how the deliverable is presented and driven**, not the verification pipeline.

## The one rule

**One doc per session.** It opens with a cockpit, then one review card per item. Every artifact the session produces is linked from the **Working folder** table (fan-out to sub-files mid-run is fine; the cockpit is the single front door). Never hand the user "see files A, B, C" — hand them the cockpit.

## Structure

Copy `references/session-review-template.md`. Save the working copy in the relevant project folder as `YYYY-MM-DD-<slug>-review.md` (or `-plan.md`).

**Cockpit (top):**
1. **Status line** — one line: how many items await review + last-updated timestamp.
2. **🧭 Progress** — a checklist, one row per item, each with a status glyph; a text progress bar + "X/N done · A awaiting review · B pending". **Make each item a clickable anchor to its review card** — `[N. Title](#n-title)` using GitHub-slug rules (lowercase, spaces→`-`, drop punctuation/emoji). Keep item headings free of `+ # ← → ( )` so slugs stay clean single-hyphen and the links resolve in Obsidian + the Claude side panel.
3. **📁 Working folder** — table of every artifact produced this session with its `~/vault/...` path or link (meeting note, this doc, evidence dir, external issues/PRs, posted messages).
4. **🔌 Context** — sources the work is grounded in (recordings, Slack threads, issues), tools/connectors used, related tickets.

**Review items (below):** one card per item:
- **Status** — glyph + word (see vocabulary).
- **Action** — what was done or is proposed.
- **Deliverable** — link/path, or an inline draft placed directly under the card so you review it in place (messages to send, doc bodies).
- **Checklist** — the item's acceptance criteria as checkboxes.
- **🗒 Your call** — the approval slot you edit (`approve` / your requested changes).
- **Decision log** — append-only record of what happened / what you decided.

**Footer:** "How to drive this doc" (approve/change mechanics + status vocabulary), so the doc is self-explaining.

**Status vocabulary:** ⏳ pending · 🔄 in progress · 📝 needs review · ✏️ changes requested · ✅ done · ⛔ blocked

## Update protocol (keep it live)

- **After every meaningful step**, refresh: the Progress checklist + bar, the affected item's Status, the Working folder (add new artifacts), and the item's Decision log. Bump the `updated:` frontmatter + status line.
- Prefer targeted `Edit`s over full rewrites so your inline edits/approvals are never clobbered. **Before editing, re-read the file** — you may have typed approvals or change requests into **🗒 Your call** or ticked boxes.
- When you approve an item, execute it, move it to ✅, and log the outcome (with the external link — issue/PR/message URL) in the Decision log.
- When you request changes, set the item to ✏️ changes requested, apply them, re-draft in place, then return it to 📝 needs review.

## Interaction contract

The doc is the shared surface; you drive it two ways, both valid:
- **In the doc / side panel:** you edit **🗒 Your call** or tick checkboxes. Re-read and act.
- **In chat:** "3 is ok", "approve 2 and 4", "change the tone on the requirement comms". Map to item numbers and act.

Distinguish **draft** items (agent proposes, waits — e.g. a Slack message you own sending) from **auto** items (agent may execute directly — e.g. filing a GitHub issue you explicitly asked for). Draft items stay 📝 until approved; auto items go straight to ✅ with the artifact linked. When unsure whether an item is draft or auto, leave it 📝.

## Post-condition

Read-only for the doc itself, but the items it tracks often mutate external state — obey each item's own post-condition (fetch back the issue, confirm the Slack message landed, etc.) and record the verified link in the Decision log. Never mark ✅ from a mutation call alone.

## Optional: rendered view

The markdown doc is primary (you edit it to approve). If you want a richer at-a-glance view, additionally render an HTML **Artifact** of the cockpit (Progress + Working folder + Context + item statuses) — but the markdown stays the source of truth and the editable surface.
