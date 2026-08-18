---
name: daily-journal
description: A passive daily work journal that Claude keeps FOR you so you never have to write it yourself. Append short entries after meaningful work (what was done, what you focused on, artifacts touched) to 01-daily/journal/YYYY-MM-DD.md. Run a guided reflection at night or in the morning. Use when you run /daily-journal, say "log this to my journal", "add to today's journal", "reflect on today/yesterday", or when finishing a meaningful chunk of work in any session.
---

# Daily Journal

## Purpose
Keep an **automatic, passive** journal of your workdays so you don't have to write one. Claude logs what got done as it happens; you optionally run a reflection later. This is distinct from `/weekly-checkin` (which is a manual reflection where you supply the input) — here **Claude is the author** and the log accrues in the background.

Two modes:
1. **`log`** (default, mostly invoked implicitly) — append a short entry to today's journal.
2. **`reflect`** — read the day's log (+ recent days) and run a guided reflection with you.

## Storage
- One file per day: `01-daily/journal/YYYY-MM-DD.md` (use `date +%F` for today's date; never guess).
- Create the file from the template below on the first entry of the day.
- Append only — never rewrite earlier entries. Newest entries go at the bottom of the Log section.

## When to log (procedure for the always-apply trigger)
The trigger itself lives in `CLAUDE.md` § Daily Journal (ALWAYS APPLY), because a skill body is lazily loaded and cannot fire itself. This section is the procedure that trigger runs.

After finishing a **meaningful** unit of work, append one entry. Meaningful = would matter to future-you or shows how the day was spent. Examples:
- Shipped/committed something, published a note/brief/slide, filed or moved tracker issues (Linear/Jira/GitHub).
- Made a decision, changed direction, or hit a notable blocker.
- Produced a deliverable file (spec, plan, analysis, report).
- A substantive research/synthesis session that produced an artifact.

**Do NOT log:** trivial reads, one-line lookups, mid-task scratch work, this journal's own writes, or anything you asked to keep out. When in doubt, one concise line is better than none. Do not interrupt the flow to announce logging — just append and carry on.

## Entry format
Append under the `## Log` section:

```
### HH:MM — <short title of what got done>
- **Focus:** <the thread/project this served, e.g. a product line, a squad, the blog>
- **Did:** <1-3 bullets, concrete, past tense>
- **Artifacts:** <files/PRs/links touched, or "—">
- **Signal:** <optional: decision made, blocker hit, mood/energy if you mentioned it, or omit>
```

Keep it tight. Times use 24h local (`date +%H:%M`). Match memory/CLAUDE.md conventions: no em-dashes, your product naming rules, no self-authored next-steps (only record what actually happened or what you explicitly said).

## Daily file template (first entry of the day)
```markdown
---
date: YYYY-MM-DD
type: journal
---

# Journal — YYYY-MM-DD (Weekday)

> Auto-kept by Claude. Reflection appended below when you run it.

## Focus of the day
_Inferred from entries; leave blank until there's signal._

## Log

## Reflection
_Empty until you run `/daily-journal reflect`._
```

## Mode: reflect
Triggered by `/daily-journal reflect [today|yesterday|YYYY-MM-DD]` (default: today), or when you say "reflect on today/yesterday" or "let's do the journal".

1. Read the target day's journal file. If it doesn't exist or the Log is thin, say so and offer to reconstruct from other signals (today's brief in `01-daily/briefs/`, recent commits, braindumps) before proceeding — but do NOT fabricate.
2. Read the previous 2-3 journal files for continuity (recurring threads, carried-over blockers).
3. Summarize the day back to you in a few lines: main focus, what shipped, what stalled. Then ask 2-4 light reflection questions adapted to what the log shows (e.g. "The eval work ate the afternoon — did it move?" rather than generic prompts). Keep it conversational, low-friction; this is meant to be a 2-minute thing at night or in the morning.
4. Write your answers + a short synthesis into the `## Reflection` section of that day's file. Fill in `## Focus of the day` if still blank.
5. If the reflection surfaces a durable fact (a decision, a changed priority, a lesson), also write/update the relevant `05-knowledge/` note or a memory per the Brain-First protocol — the journal is ephemeral daily context, not the durable store.

## Weekly roll-up (optional)
If you ask for a "week in review" or on a weekly reflection, read the last 7 journal files and synthesize themes into `01-daily/weekly/` (match the existing naming there). Do not auto-run this.

## Guardrails
- Single-file discipline: everything for a day lives in that one journal file. Never split into per-entry files.
- Privacy: personal/1:1 content stays in the journal only; never leaks into team-facing briefs.
- Never publish the journal anywhere external.
- This is your private log. Write plainly and honestly; if the day stalled, say so.
