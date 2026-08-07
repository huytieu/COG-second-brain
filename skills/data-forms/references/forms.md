# Form catalog

21 ways to represent a dataset. Each entry: what it's for, the shape, and the condition
under which it stops working. Mockups show structure only — apply the destination's
visual language on top.

Forms 1-15 are observed working in the wild (Lenny's Newsletter survey issues, 2025-2026).
Forms 16-21 obey the same grammar and fill gaps the first fifteen leave.

---

## 1. Ordered column chart

**For** one question with 3-6 answers on an ordered scale, where the *shape* of the
distribution is the finding.

```
              How has AI shifted your professional identity?

     Amplified
        49%
     ┌───────┐
     │       │        Redefined
     │       │           27%
     │       │        ┌───────┐    Destabilized
     │       │        │       │        14%
     │       │        │       │     ┌───────┐    Diminished
     │       │        │       │     │       │       5%      Unchanged
     │       │        │       │     │       │    ┌──────┐      3%
   ──┴──😄───┴────────┴──🤩───┴─────┴──😵───┴────┴──😞──┴────┬──😐─┬──
```

Label and value stack *above* each column, left-aligned to it, so nothing sits in the
plot area. An icon on the baseline gives each column an identity the eye can grab before
it reads. Magnitude runs the ramp by rank.

**Stops working when** the categories aren't ordered — then ranking by value matters more
than sequence, and you want form 3. Also breaks past ~6 columns: they go thin and the
stacked labels collide.

---

## 2. Paired columns

**For** exactly two time points, on one or two metrics, where direction is the story.

```
              Burnout is surging, and optimism is fading

         HOW BURNED                      HOW OPTIMISTIC
         OUT ARE YOU?                     ARE YOU?
                    ╭─→                ╲
              55.7%                     ╲__→
      44.7%   ┌────┐            54.8%    48.7%
      ┌────┐  │    │            ┌────┐   ┌────┐
      │2025│  │2026│            │2025│   │2026│
    ──┴────┴──┴────┴────────────┴────┴───┴────┴──
```

Period labels go *inside* the bars, values above — that removes the x-axis entirely. One
arrow per pair showing direction. Encode "up is bad" vs "up is good" differently so both
pairs read as the same news without a sentence of explanation.

**Stops working when** you have three or more time points. Two columns imply a line the
reader draws themselves; three imply a trend you should actually draw (form 9 or 13).

---

## 3. Ranked horizontal bar

**For** multi-select questions, or any ranking of 5-15 items. The workhorse. Percentages
summing past 100 is expected — say so in a subhead.

```
              The underlying fear is of being overworked

   ┌─────────────────────────────────────────────────┐ 51%
   │ Expected to do more for same pay                │
   └─────────────────────────────────────────────────┘
   ┌───────────────────────────────────────────┐ 46%
   │ Pace is becoming unsustainable            │
   └───────────────────────────────────────────┘
   ┌───────────────────────────────────────┐ 43%
   │ Becoming too dependent on AI          │
   └───────────────────────────────────────┘
   ┌────────────────────────────┐ 30%
   │ Skills becoming less valuable                    ← label overflows,
   └────────────────────────────┘                       see failure mode
```

Label **inside** the bar at the left, value **outside** at the right. One treatment for
every bar — length already ranks them, so color would be noise. Common left edge.

**Stops working when** the top bar is more than ~4× the bottom one: short bars can't hold
their label. Fix by moving all labels outside-left, right-aligned in a fixed gutter.

---

## 4. Valence bar

Form 3 plus a categorical encoding orthogonal to length.

```
              What emotions describe how you feel about AI at work?

   ┌─🙂─────────────────────────────────────────┐ 71%
   │ Curious                                    │        ██ Positive
   ┌─😀───────────────────────────────────┐ 64%          ▢▢ Neutral
   │ Excited                              │              ▓▓ Negative
   ┌─😵──────────────────────────┐ 54%
   │ Overwhelmed                 │
   ┌─🙃────────────────────┐ 51%
   │ Conflicted            │   ← unfilled outline = neutral
```

One of the few places a legend is correct: the second dimension repeats down the rows and
can't be direct-labeled without repeating a word eleven times. Render neutral as an
*unfilled outline* rather than grey — grey reads as missing data.

**Stops working when** the valence assignment is arguable. If reasonable people would sort
the categories differently, don't encode it; you're smuggling an opinion into a channel
the reader will trust as fact.

---

## 5. Diverging bar

**For** a metric with a real, meaningful zero on both sides: NPS, net sentiment, change
vs. baseline, net promoter/detractor.

```
        How likely are you to recommend a career in your role?

                         ┊ detractor side      │  promoter side
     Founder / Executive ┊                 -3 ▐│
             Sales / GTM ┊          -32 ▐▐▐▐▐▐▐│
                      PM ┊         -35 ▐▐▐▐▐▐▐▐│
              Operations ┊       -46 ▐▐▐▐▐▐▐▐▐▐│
             Engineering ┊      -48 ▐▐▐▐▐▐▐▐▐▐▐│
               Marketing ┊      -49 ▐▐▐▐▐▐▐▐▐▐▐│
        Data / Analytics ┊     -54 ▐▐▐▐▐▐▐▐▐▐▐▐│
                  Design ┊  -67 ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐│
                Research ┊  -68 ▐▐▐▐▐▐▐▐▐▐▐▐▐▐▐│
                         -100   Detractors   0   Promoters   100
```

Tint each half-plane faintly and name it under the axis. Keep the zero line heavy.
**Keep the scale symmetric even when every value sits on one side** — the empty half is
the finding, and cropping it to "use the space" destroys the whole point.

**Stops working when** zero is arbitrary. A diverging form on a metric with no natural
midpoint invents a judgment.

---

## 6. Waffle / dot matrix

**For** making a percentage feel like people. 100 marks, one per point.

```
        How worried are you about layoffs?

   😐 28%      😔 31%     😟 21%      😧 12%      😱 8%
   Not at all  Slightly   Moderately  Very        Extremely

                 ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
                 ○ ○ ○ ○ ○ ○ ○ ○ ○ ○
             ┌─  ○ ○ ○ ○ ○ ○ ○ ○ ◐ ◐
         72% │   ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐
          of │   ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐
      people │   ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◐ ◔
         are │   ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔   ─┐  41.2%
     worried │   ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔ ◔    │  are at least
             │   ◑ ◑ ◑ ◑ ◑ ◑ ◑ ◑ ◑ ◑    │  moderately
             └─  ◑ ◑ ● ● ● ● ● ● ● ●   ─┘  worried
```

Fill bottom-up so the heavy end is grounded. The brackets are the reason this beats a
bar: they call out *cumulative* groupings the reader would otherwise have to add up, and
you can run two overlapping ones (72% worried at all, 41% at least moderately) without
drawing a second chart.

**Stops working when** you need decimal precision — a waffle rounds to whole points — or
past ~5 categories, where the grid turns to static.

---

## 7. Nested bands

**For** categories that genuinely nest, where the headline is a cumulative figure.

```
        How much better are you at your job?

   Drawn as concentric circles; the nesting logic is what matters:

   ┌─ 97.2% say AI is making them better ─────────────────────────┐
   │                                                              │
   │   ┌─ 81.7% moderately better or more ──────────────────┐     │
   │   │                                                    │     │
   │   │   ┌─ 49.4% "very much" or "extremely" ───────┐     │     │
   │   │   │                                          │     │     │
   │   │   │   ┌─ 15.3% "extremely better" ───┐       │     │     │
   │   │   │   └──────────────────────────────┘       │     │     │
   │   │   └──────────────────────────────────────────┘     │     │
   │   └────────────────────────────────────────────────────┘     │
   └──────────────────────────────────────────────────────────────┘
     2.8% not at all    15.5% slightly    32.3% moderately    34.1% very
     └── each band's own share, labelled inside its ring ──┘
```

Concentric bands, each one a category, drawn so the eye reads "and also, and also."
Leader lines carry the cumulative claims outside the shape. This is the honest
replacement for a pie chart on ordered data: it shows both the parts and the running
total, which a pie cannot.

**Stops working when** the categories don't actually nest — then the geometry is claiming
a containment relationship that doesn't exist, which is worse than a plain column chart.

---

## 8. Small multiples

**For** proving "X is consistently the outlier" when no single chart can.

```
        Designers and researchers are the most negative across the board

                          61% 57%                63% 60% 55% 53%
                          ██  ██  51% 50% 49%    ██  ██  ░░  ░░  52%
   33%                    ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░
   ██  25% 24% 23% 23%    ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░
   ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░
   ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░     ██  ██  ░░  ░░  ░░
   ──────────────────     ──────────────────     ──────────────────
   AI-identity:           Emotion: Tired         Emotion: Overwhelmed
   Destabilized

   ██ Design  ██ Research  ░░ Engineering  ░░ Operations  ░░ PM  …

   Shared 0-70 scale across all three panels — never per-panel maxima.
```

Same category order in every panel, non-negotiable. Emphasis only on the subjects named
in the headline; everyone else recedes into one muted ramp. Panel titles name the
*metric*; the headline carries the claim. One shared legend.

**Stops working when** panels use different scales without saying so, or when the
highlighted subject isn't consistent across panels. The second case means the chart
disproves the headline — which is useful information, so change the headline.

---

## 9. Slope chart

**For** two series moving in opposite directions, where the crossing is the story.

```
        A great manager changes everything

   5
                                                    ● 4.04
   4                              ● 3.31    ● 3.63 ╱   Job enjoyment
        ● 3.22          ● 2.95 ╱───────────────────
   3      ╲        2.90 ●───╲╱────● 2.70
             ╲───────╱          ╲──────● 2.46  ● 2.33  Burnout
   2    ● 2.44
   1
   0  Not at all  Slightly  Moderately   Very   Extremely
                     Manager effectiveness
```

One of two forms that keeps a grid, because slope needs a reference. Value labels on
every point, offset *above* the rising series and *below* the falling one so they never
collide at the crossing. Series named at their right endpoint beats a legend.

**Stops working when** the x-axis is categorical and unordered. Connecting those points
implies a progression that doesn't exist.

---

## 10. Pill matrix

**For** a small table (4-8 rows × 3-5 metrics) that would otherwise get skipped. Each
cell becomes a mini bar carrying its own number.

```
   ┌──────────────┬───────────────┬──────────────┬────────────────┐
   │ Company size │ Career optim. │   Burnout    │ Would recommend│
   │              │     (1–5)     │    (1–5)     │     (NPS)      │
   ├──────────────┼───────────────┼──────────────┼────────────────┤
   │      1–10    │ (3.55▓▓▓▓░░░) │ (2.33▓░░░░░) │ (6.19▓▓▓▓▓░░░) │
   │     11–50    │ (3.37▓▓▓▓░░░) │ (2.61▓▓░░░░) │ (6.09▓▓▓▓▓░░░) │
   │    51–200    │ (3.30▓▓▓░░░░) │ (2.68▓▓░░░░) │ (5.98▓▓▓▓░░░░) │
   │     1K–5K    │ (3.14▓▓▓░░░░) │ (2.85▓▓▓░░░) │ (5.70▓▓▓░░░░░) │
   │    10,000+   │ (3.04▓▓░░░░░) │ (2.90▓▓▓░░░) │ (5.79▓▓▓░░░░░) │
   └──────────────┴───────────────┴──────────────┴────────────────┘
```

**Each column gets its own scale and its own ramp direction** — high-is-good and
high-is-bad must not share an encoding. Scale stated once in the header, never repeated
in cells. Sort rows by whichever metric carries the story; the monotonic staircase down
one column is what the reader will notice.

**Stops working when** you apply one ramp across all columns, or when rows exceed ~8 and
it reverts to being a table with decoration.

---

## 11. Word cloud

**For** an open-text question that asked for a single word, where the pile is the point.

```
                 The industry is "chaotic"

         mess    moving    layoffs   flux    tools
    unstable   hype                        pace
      huge        c h a n g e            better
   leadership   exciting        costs    bubble
      quality   uncertain   fast   shift  pressure
        evolving        opportunity      money
```

Size by frequency; colouring by frequency too is correct here — with no axis, redundant
encoding costs nothing and gains legibility. Cap at ~25 words. Headline quotes the modal
word so the reader gets the answer even if they don't scan the cloud.

**Stops working when** the question allowed a phrase. Code the responses into themes
first, then use form 3 — a cloud of phrases is unreadable and a cloud of their constituent
words is meaningless.

---

## 12. Metaphor diagram

**For** a relationship the numbers can't carry: surface vs. hidden, stated vs. actual,
what's measured vs. what matters.

```
        The productivity iceberg

    ┌──────────────┐                ╱╲
    │On the surface│               ╱  ╲       97.2%
    │"We're doing  │              ╱    ╲      say AI is making
    │  better!"    │             ╱      ╲     them better
    └──────────────┘  ~~~~~~~~~~╱~~~~~~~~╲~~~~~~~~~~~~~~~~~
    ┌──────────────┐          ╱            ╲
    │  Just below  │         │  "I CAN DO    │
    │Output quality│         │  MORE, FASTER │
    └──────────────┘         │  BUT NOT      │
    ┌──────────────┐         │  BETTER."     │
    │The deep cost │          ╲              ╱
    │Thinking and  │           ╲ "MY BRAIN  ╱
    │  judgment    │            ╲IS ROTTING"╱
    └──────────────┘             ╲_________╱
```

Left rail names the tiers; the shape carries verbatim quotes. **One statistic maximum** —
the metaphor is doing the work, and a second number turns it into a bad chart instead of
a good diagram.

**Stops working when** the metaphor implies a proportion the data doesn't have. An
iceberg asserts "most of it is hidden." Don't use one for a 60/40 split.

---

## 13. Time-series area

**For** many points over time where the current value matters as much as the shape.

```
   Most open PM jobs since 2022                     ← headline, left-aligned
   ( 7,379 open PM jobs )  ↑ 79% from low (4,113)   ← current value + delta

   12K ┼─────────────────────────────────────────  as of March 2026
   10K ┤╲                            MOST OPEN PM
    8K ┤ ╲                           ROLES IN 3+ YEARS ╲
    6K ┤  ╲___              ______________________────→●
    4K ┤▓▓▓▓▓▓▓╲__________╱▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    2K ┤▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
     0 ┴────┬──────┬──────┬──────┬──────
         2023   2024   2025   2026
```

The other exception to "delete the axis": keeps faint gridlines and a filled area, both
of which help the eye read slope. Lead with the current value as a standalone figure and
a delta-from-reference, so a reader who never looks at the curve still leaves with the
number. Stamp the as-of date in-frame.

**Stops working when** the y-axis is truncated. Never truncate here — this form is
entirely about honest slope, and a cropped baseline exaggerates every move.

---

## 14. Staircase column

**For** one metric across 7-10 *ordered* buckets, where monotonicity is the finding.

```
        Burnout climbs by company size
                                              ┌ Difference within
                                              │  margin of error
                                          ┌────┴─────┐
                                           65%
                                    61%   ┌───┐   61%
                             56%   ┌───┐  │   │  ┌╌╌╌┐  ← dashed cap =
                      54%   ┌───┐  │   │  │   │  ┆   ┆    not significant
               52%   ┌───┐  │   │  │   │  │   │  ┆   ┆
        42%   ┌───┐  │   │  │   │  │   │  │   │  ┆   ┆
       ┌───┐  │   │  │   │  │   │  │   │  │   │  ┆   ┆
       │   │  │   │  │   │  │   │  │   │  │   │  ┆   ┆
     ──┴───┴──┴───┴──┴───┴──┴───┴──┴───┴──┴───┴──┴───┴──
       1–10   11–50 51–200 201–1K  1–5K   5–10K  10K+
```

Single treatment, intensity rising with value, so the staircase reads as one trend rather
than seven facts. The dashed cap plus bracket is the honest way to keep a
non-significant final bar instead of quietly dropping it.

**Stops working when** the buckets aren't ordered — then sort by value and use form 3.

---

## 15. Persona cards

**For** a segmentation where the reader should remember the *names*, not the shares.

```
        The four tech workers of 2026

    ╭────────────╮  ╭────────────╮  ╭────────────╮  ╭────────────╮
    │     💪     │  │     🤷     │  │     😵     │  │     😠     │
    │            │  │            │  │            │  │            │
    │    THE     │  │    THE     │  │    THE     │  │    THE     │
    │  ENERGIZED │  │ CONFLICTED │  │DISORIENTED │  │ RESENTFUL  │
    │  All-in    │  │ Ambivalent │  │ Role keeps │  │ Pressured, │
    │  adopters  │  │   middle   │  │  shifting  │  │ checked-out│
    │    41%     │  │    35%     │  │    12%     │  │    12%     │
    ╰────────────╯  ╰────────────╯  ╰────────────╯  ╰────────────╯
```

Name, one-line descriptor, share — in that order of prominence, because that's the order
of what you want retained. A distinct image per card does more for recall than any
encoding. Cards laid out in share order.

**Stops working when** the segments came from a hunch rather than a clustering. This form
radiates rigor; using it on made-up groups is the most expensive lie in the catalog.

---

## 16. Dumbbell

**For** two groups compared on one metric across many rows, where the *gap* is the point.

```
        Enterprise buyers care about compliance; SMBs don't

   Compliance      SMB ●───────────────────────────● Ent   gap 42
   Onboarding      SMB ●──────────────● Ent                gap 19
   Price               Ent ●──────● SMB                    gap  9
   Integrations    SMB ●────● Ent                          gap  4
```

Direct-label both endpoints, weight the connector by gap size so the ranking of gaps
reads before the values do. Sort by gap, not by either endpoint.

**Stops working when** the two groups cross rank frequently — the crossing connectors
become spaghetti. Use paired small multiples instead.

---

## 17. Dot plot

**For** a ranking where zero is not meaningful: averages, indexes, scores, years, rates.

```
        Average time-to-first-value, by plan

   Enterprise    ────────────────────●  18.2 days
   Business      ──────────●            11.4
   Pro           ───────●                8.9
   Free          ─────●                  6.1
                 6    9    12   15   18
```

Bars imply a zero baseline and make a 6-vs-8 difference look like nothing. Dots don't
carry that promise, so you can start the scale where the data lives without lying.

**Stops working when** the reader will read the dots as a count. Anything that *is* a
total or a share should be a bar.

---

## 18. Bump chart

**For** ranking over time — who moved up, who fell.

```
        Claude overtook Perplexity in the assistant stack

   rank    2023           2024           2025           2026
    1    ChatGPT ────── ChatGPT ────── ChatGPT ────── ChatGPT
    2    Perplex ──╮ ╭─ Claude ─────── Claude ─────── Claude
    3    Claude ───╯ ╰─ Perplex ──╮ ╭─ Gemini ─────── Gemini
    4    Gemini ─────── Gemini ───╯ ╰─ Perplex ────── Perplex
```

Cap at ~8 series. Highlight the one or two whose movement is the headline; mute the rest
into a single background treatment, or the chart becomes a plate of noodles.

**Stops working when** ranks barely change — a bump chart of four parallel lines says
"nothing happened" in the most expensive possible way. Use a table.

---

## 19. Centered stacked row

**For** Likert agreement across several statements. The classic survey form.

```
        Where teams agree — and where they don't

                                 ◄ disagree │ agree ►
   AI saves me time                     ▓▓▓░│░████████████████████  82% agree
   Quality has improved          ▓▓▓▓▓▓▓▓░░░│░░░████████████        48%
   I trust the output         ▓▓▓▓▓▓▓▓▓▓▓▓░░│░░░████████            31%
   My role is secure       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░│░░██████               22%
                                   ▓ disagree  ░ neutral  █ agree
```

Center each row on the neutral midpoint rather than at 0%, so agree and disagree extend
in opposite directions and the rows are comparable at a glance. Sort by net agreement.
Put the summary percentage outside the row.

**Stops working when** the neutral bucket is large and you hide it. Split neutral across
the midpoint or show it explicitly; suppressing it inflates both wings.

---

## 20. Two-column flow

**For** paired transformations: intention → result, promise → reality, input → outcome.
The honest small-scale alternative to a Sankey.

```
        What teams intend vs. what they get

        INTENTION                    RESULT
        get noticed        ▶         make mediocre work
        make good work     ▶         get noticed
        ship faster        ▶         ship more rework
```

Two columns, a repeated connector glyph, nothing else. Its power is the *reversal* the
reader notices between rows one and two.

**Stops working when** the mapping is many-to-many. Then you need a real flow diagram,
and you should question whether the reader will follow it.

---

## 21. Named-quadrant scatter

**For** two dimensions and few enough points to label every one.

```
        High impact, low effort: three obvious bets

   high   │  DO LATER              │  DO FIRST
   impact │    ● Multi-tenant      │    ● SSO
          │    ● Audit log         │    ● Bulk import
          │────────────────────────┼─────────────────────
          │  DON'T                 │  QUICK WINS
    low   │    ● Theme editor      │    ● CSV export
          └────────────────────────┴─────────────────────
               high effort              low effort
```

Every quadrant gets a verb, not a coordinate description — the label should tell the
reader what to *do*, which is the only reason to draw quadrants. Label every point.

**Stops working when** there are more than ~20 points, or the axes are estimates dressed
as measurements. An unlabeled scatter belongs in analysis, not in a deliverable.

---

## Never

- **Pie and donut charts.** Form 7 shows the same composition plus cumulative totals;
  form 1 shows it with comparable lengths. A pie is strictly worse than both.
- **Dual y-axes.** The correlation is manufactured by whatever scaling you chose.
- **Radar / spider charts.** Area scales with the square of the values and the shape
  changes when you reorder the axes. Use form 10.
- **Gauges and speedometers.** Enormous ink for one number. Just write the number.
- **3D anything, gradient fills as decoration, drop shadows on data marks.**
- **Treemaps under ~15 items.** Use a ranked bar; area is harder to compare than length.
- **Truncated y-axes**, anywhere, ever.
