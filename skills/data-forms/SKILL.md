---
name: data-forms
description: Pick the right way to represent a dataset so a reader gets the finding in three seconds — a catalog of 20+ chart and diagram forms with when-to-use and failure modes, plus the encoding decisions that make any of them readable (takeaway headline, direct labels, kill the axis, highlight-and-mute, show the caveat). Style-agnostic — use with whatever palette or design system the destination already has. Use when charting survey results, benchmark data, usage metrics, or research findings for a post, brief, deck, or report, and whenever the default bar chart feels like it's burying the point.
---

# data-forms

A repertoire, not a style. Distilled from Lenny's Newsletter data illustrations
(2025-2026 survey issues) — what makes those charts work is not the palette, it's the
form selection and the encoding discipline. Both are portable to any visual language.

For the visual layer, use whatever the destination already has: your product's brand
tokens for in-product surfaces, the built-in `dataviz` skill for palette construction and
accessibility, your house style for personal sites. This skill decides *what shape the data
takes* — the layer above color.

## Start here: the picker

| What the data does | Reach for | Form # |
|---|---|---|
| One question, 3-6 ordered answers | Ordered column · Waffle · Nested bands | 1 · 6 · 7 |
| One question, many multi-select answers | Ranked bar · Valence bar | 3 · 4 |
| Same metric, two points in time | Paired columns · Slope | 2 · 9 |
| Same metric, 3+ points in time | Time-series area · Bump | 13 · 18 |
| One metric across 7-10 ordered buckets | Staircase column | 14 |
| One metric across many unordered segments | Small multiples · Dot plot | 8 · 17 |
| Signed score (-100…+100, net, delta) | Diverging bar | 5 |
| Two groups compared across many rows | Dumbbell | 16 |
| Agreement / Likert across several statements | Centered stacked row | 19 |
| Segments × several metrics | Pill matrix | 10 |
| Open-text answers | Word cloud · Coded theme bar | 11 · 3 |
| A relationship the numbers can't carry | Metaphor diagram · Two-column flow | 12 · 20 |
| A named segmentation from clustering | Persona cards | 15 |
| Two dimensions, few labeled points | Named-quadrant scatter | 21 |

Full catalog with mockups and failure modes: `references/forms.md`.

## Six decisions that matter more than the form

**1. Write the takeaway before you pick a form.**
Finish the sentence "The point of this chart is ___." If you can't, you have a table,
not a chart, and no form will save it. That sentence becomes the headline. Two legal
headline modes:

- *Claim*, for comparisons and analysis — "Burnout is surging, and optimism is fading"
- *Question verbatim*, when the chart is the answer distribution — "How worried are you
  about layoffs?"

Never a field name. "Burnout by company size" is a spreadsheet tab.

**2. Print every value.** The reader should never estimate against an axis. Number sits
adjacent to its mark. This is what earns you the right to do #3.

**3. Delete the axis.** Baseline only — no y-axis, no gridlines, no ticks. Exceptions:
time series and slope charts, where the *shape* is the message and needs a reference
grid. Everywhere else the axis is scaffolding you forgot to remove.

**4. No legend when a direct label fits.** Category name goes on or beside its mark. A
legend is justified only when one key serves several panels (small multiples) or encodes
a dimension orthogonal to position (valence, group membership).

**5. Highlight two, mute the rest.** In a nine-category comparison, only the one or two
subjects named in the headline get emphasis; everyone else recedes. The chart should
argue the headline, not present the table. If the highlighted subject isn't actually the
outlier, the chart just disproved your headline — change the headline, not the data.

**6. Show the caveat in-frame.** Small n, margin of error, non-response, "percentages
sum past 100 because multi-select" — put it in the chart, not a footnote. A dashed
outline on a non-significant bar with a bracket reading "difference within margin of
error" is more credible than a clean chart plus a disclaimer nobody reads.

And one restraint: **at most one annotation.** Point at the thing a reader would
otherwise miss. Zero is fine. Two is clutter.

## Encoding rules of thumb

- **Color means something or it isn't there.** Don't color bars that a label already
  distinguishes. Reserve saturation for the subject of the headline.
- **Sequential ramp = magnitude or rank. Diverging ramp = signed. Categorical = identity.**
  Mixing these is the most common way a chart lies.
- **Per-column scales in a matrix.** In form 10, each metric gets its own ramp and its own
  direction, otherwise "dark = high" fights "dark = bad."
- **Neutral is an unfilled outline, not grey.** Grey reads as missing data.
- **Redundant encoding is fine where there's no axis** — a word cloud can size *and* color
  by frequency; nothing is being wasted.
- **Order carries meaning.** Sort by value unless the categories are inherently ordered
  (time, buckets, Likert). Keep the same order across every panel of a small multiple.
- **Bars start at zero, always.** If zero isn't meaningful for the metric, you wanted a
  dot plot (form 17), not a bar.
- **Anthropomorphize only when the subject is human.** Waffle grids of people, emoji
  anchors, persona illustrations — these earn their keep for sentiment and headcount, and
  read as cheap for latency and revenue.

## Workflow

1. State the takeaway in one sentence.
2. Classify what the data does (distribution / ranking / comparison / trend /
   correlation / composition / qualitative) and pick from the picker table.
3. Read that form's entry in `references/forms.md` — especially its failure mode. If your
   data triggers the failure mode, take the alternative listed there.
4. Apply the six decisions and the encoding rules.
5. Build it in whatever the destination uses.
6. **Render it and look at the image.** Not the DOM, not the spec — the pixels. Run the
   checklist. Fix what you see and re-render.

## Pre-ship checklist

Read the rendered image and answer each. A "no" is a fix, not a note.

- [ ] Headline states a finding or asks the literal question — not a field name
- [ ] Every mark carries its value, legible at 50% zoom
- [ ] No legend that direct labels could have replaced
- [ ] Emphasis lands on the subject of the headline; everything else recedes
- [ ] Longest label doesn't collide with, wrap under, or overflow its mark
- [ ] Bars start at zero; no truncated scale
- [ ] ≤1 annotation
- [ ] Squint test: at 25% zoom the shape of the answer still reads
- [ ] Caveats (n, margin of error, multi-select) visible in-frame
- [ ] The form's own failure mode from `references/forms.md` does not apply

## Reference

`references/forms.md` — 21 forms, each with an ASCII mockup, when to use it, and the
condition under which it stops working.
