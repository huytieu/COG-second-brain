---
name: slop-gate
description: Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks.
---

<!-- slop-ok: this skill quotes the tells it blocks -->

# slop-gate

`no-ai-slop` is an editor you invoke. This is a gate that runs whether or not anyone
remembers it. It scans outgoing text, refuses on a tell, and returns the hit list so
the rewrite is targeted.

Two rules make it usable rather than annoying: hard tells fail on a single hit, and
words that are decoration at volume but legitimate once are counted rather than
banned. Text inside quotes or backticks is stripped before scanning, so a piece that
quotes a tell as an exhibit does not fail on its own examples.

## Why a gate and not a rule

A rules file is advisory, and advisory rules fail in a specific, repeatable way: they
fire in the step the model thinks of as writing and not in the steps it thinks of as
something else. A deck built by an agent can carry clean paragraphs under headline
slide titles, because the titles were produced in a layout step where the writing
rules never ran. Every surface nobody named explicitly sits on the unchecked side:

    slide titles, kickers          table headers, row keys       commit messages
    tile and card labels           diagram node and edge labels  code comments
    chart titles and legends       button copy, subtitles        memory files
    alt text, image captions       Slack, email, issue bodies    PR descriptions

The gate closes that by scanning the text on its way out, whatever produced it.

## Run it

```bash
python3 scripts/scan.py DRAFT.md              # one file
python3 scripts/scan.py content/**/*.md       # many
cat draft.md | python3 scripts/scan.py -      # stdin
```

Exit code 0 is clear, 1 is tells found, so it drops into CI or a pre-commit hook
unchanged. Every hit prints its label and the surrounding text.

## Wire it as a hook (Claude Code, optional)

COG ships no hooks by default. If you want the check enforced rather than remembered,
add this to `.claude/settings.json` yourself. `--hook` reads the hook payload on stdin
and answers with a permission decision.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|mcp__.*slack.*send.*|mcp__atlassian__(create|update)Confluence.*",
        "hooks": [{ "type": "command",
                    "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/slop-gate/scripts/scan.py\" --hook" }]
      }
    ],
    "Stop": [
      { "hooks": [{ "type": "command",
                    "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/slop-gate/scripts/scan.py\" --hook" }] }
    ]
  }
}
```

The `Stop` entry scans the agent's own reply, which is where most of these land in a
working session. Expect it to fire on you within the hour; that is the point of it.

## What fails on one hit

| Tell | Specimen |
|---|---|
| Em dash | any `—` |
| Honesty framing | "honestly", "the honest part:", "if I'm being honest" |
| "not X, it's Y" | "It's not about speed, it's about trust" |
| "X, not Y" (trailing form) | "a test, not a permission", "machinery, not memory" |
| Rhetorical heading | "Why this matters", "The bottom line", "What comes next" |
| "The \<Noun\>" heading | "The Wedge", "The Shot", "The Gamechanger" |
| Verdict kicker | "That is the point.", "That is all a title is for." |
| Fake-profound closer | "let that sink in", "this changes everything" |
| Throat-clearing | "Here's the thing", "It's worth noting", "At the end of the day" |
| Sycophancy | "Great question", "You were right to push back", "That's on me" |
| Recap ending | a final paragraph opening "In conclusion" or "Ultimately" |
| Emoji heading | `## 🚀 Results` |

## What is counted, not banned

`robust, seamless, leverage, utilize, delve, empower, streamline, genuinely, quietly,
load-bearing, deep dive, clean, plain, simple, elegant, powerful, lightweight,
tapestry, game-changer, paradigm shift, cutting-edge`

Three or more in one piece fails, on the reading that density means decoration. One
is a word choice. The test for any single use: remove the adjective, and if the reader
would do nothing differently, it was decoration. "A robust retry" fails that test;
"a retry that survives a mail-slot timeout" passes, because it names the behaviour.
Keep the word when it is the term of art ("robust statistics").

## Exhibits

A piece that must quote a tell (a style guide, a post about slop, a test fixture)
carries `slop-ok: <reason>` anywhere in the file, usually as an HTML comment or a
front-matter key. Quoted and backticked spans are already exempt, so the marker is
only needed when a tell appears in the author's own voice on purpose.

Never add the marker to get past a gate you disagree with. Rewrite instead, or change
the pattern list and say why.

## What it cannot see

The gate is regular expressions, so it catches surface and near-surface tells. It is
blind to the structural ones: a declared count that the source does not contain, a
framework invented to organise two paragraphs, uniform sentence rhythm, a paragraph
that restates the previous one. Those need a reader. Use `no-ai-slop` in detect mode,
and prefer a reviewer from a different model family than the author, because a
same-family reviewer shares the author's sense of what a finished answer looks like
and waves through the same shapes.

For the tics that are yours rather than universal, measure them: `voice-baseline`.

## Comparing models against the gate

`scripts/model_compare.py` replays your own Claude Code transcripts through `scan.py` and reports, per model, the share of chat replies and Markdown writes the gate would have refused and the hit rate per rule. It also reports workload per human prompt (tool calls, active minutes, tool error rate, subagent spawns) and punctuation per 10k words. When a hook refuses a reply, the transcript keeps the refused attempt as well as the rewrite, so the counts include what the model wrote before the gate saw it.

```bash
python3 scripts/model_compare.py --since 2026-09-15T00:00:00+00:00 --rules
```

Pick a window in which the rules file and hook did not change. A rule that tightened mid-window makes the earlier model look worse than it was.
