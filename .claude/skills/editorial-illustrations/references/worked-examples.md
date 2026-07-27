# Worked examples — the method applied

These six are **case studies**, not a template menu. Each shows the same move:
*a sentence-length claim → the geometric primitive that makes the claim obvious →
the minimum markup that renders it.* Study the reasoning column; then build the
figure your post actually needs. HTML is the real extracted source (monotykamary,
2026-07-22), lightly cleaned. Swap the accent from `--ink` to `--accent` on the
one element that is the point.

Reduce every future figure to the same three questions:
1. **What is the claim?** (becomes the figcaption, verbatim)
2. **What is the claim's *structure*?** (spectrum? ranking? sequence-with-threshold?
   mutual causation? branch? transformation?) → picks the primitive.
3. **Where is the point?** → the one element that gets coral.

---

## 1. `autonomy-field` — claim has a SPECTRUM structure

**Claim:** "Autonomy isn't binary; the useful position slides with blast radius."
**Structure:** ordered positions on one axis → **cell grid with rising fill.**
**Point (coral):** the rightmost / highest-autonomy cell, or leave grayscale and let
fill-height carry it.

Why it works: the eye reads left→right as *more*, and the fill bars literally grow,
so "spectrum" is felt before it is read. The axis label pair ("More oversight → More
delegation") names the dimension; the stakes row underneath ("Throwaway prototype →
Production system") adds the second, orthogonal consideration without a second chart.

```html
<figure class="fig cells" style="--n:5">
  <div class="axis"><span>More oversight</span><i></i><span>More delegation</span></div>
  <div class="row">
    <section style="--v:.1"><span>01</span><b>Complete</b><small>Human decides every move</small><i></i></section>
    <section style="--v:.3"><span>02</span><b>Suggest</b><small>AI proposes local changes</small><i></i></section>
    <section style="--v:.5"><span>03</span><b>Pair</b><small>Shared iteration loop</small><i></i></section>
    <section style="--v:.75"><span>04</span><b>Delegate</b><small>AI executes bounded work</small><i></i></section>
    <section style="--v:1"><span>05</span><b>Roam</b><small>AI owns the trajectory</small><i></i></section>
  </div>
  <div class="stakes"><span>Throwaway prototype</span><b>Move deliberately, not permanently →</b><span>Production system</span></div>
  <figcaption>The useful position is contextual: autonomy moves with blast radius, expertise, and feedback quality.</figcaption>
</figure>
```

---

## 2. `bar-chart` — claim RANKS magnitudes

**Claim:** "Developers avoid handing AI the high-stakes work; trust is low."
**Structure:** comparable quantities, ordered → **horizontal bars** (never vertical;
labels stay readable). SVG, 720 viewBox, real axis 0–100.
**Point (coral):** the rows that prove the thesis (the "accent" rows). The one
surprising row (e.g. `2.6%`) is its own quiet punchline.

Why horizontal: long text labels; ranking is a vertical scan; the value sits at the
bar's end. The single tiny bar among big ones does more than any callout.

```html
<figure class="fig bars">
  <svg viewBox="0 0 720 336" role="img" aria-label="Share of respondents">
    <g class="grid">
      <g><line x1="246" x2="246" y1="18" y2="308"/><text x="246" y="12" text-anchor="middle">0</text></g>
      <g><line x1="459" x2="459" y1="18" y2="308"/><text x="459" y="12" text-anchor="middle">50</text></g>
      <g><line x1="672" x2="672" y1="18" y2="308"/><text x="672" y="12" text-anchor="middle">100</text></g>
    </g>
    <!-- row: y steps by 52; fill width = 426 * pct/100 -->
    <g class="row row--accent"><text class="label" x="0" y="56">Avoid deployment / monitoring</text>
      <rect class="track" x="246" y="38" width="426" height="24"/>
      <rect class="fill"  x="246" y="38" width="323.8" height="24"/>
      <text class="value" x="561" y="55" text-anchor="end">76%</text></g>
    <!-- ...more rows... the last, tiny one is the punchline -->
    <g class="row"><text class="label" x="0" y="264">Express high trust</text>
      <rect class="track" x="246" y="246" width="426" height="24"/>
      <rect class="fill"  x="246" y="246" width="11" height="24"/>
      <text class="value" x="274" y="263" text-anchor="end">2.6%</text></g>
  </svg>
  <figcaption>Selected developer-survey figures · share of respondents</figcaption>
</figure>
```

---

## 3. `process-diagram` — claim is a SEQUENCE with a THRESHOLD

**Claim:** "Nothing is billable until the work crosses the delivery boundary."
**Structure:** ordered stages + one that flips state → **stage grid + traveling dot
on a rail.** The committed stage inverts (coral fill).
**Point (coral):** the `is-committed` final stage — the moment the claim is about.

The dashed rail with a dot that pauses at 58% then completes *shows* the boundary:
the eye watches nothing commit until the dot crosses.

```html
<figure class="fig process">
  <div class="rail" aria-hidden="true"><i></i></div>
  <div class="stages">
    <section><span>01</span><b>Compose</b><small>Measured locally</small></section>
    <section><span>02</span><b>Queue</b><small>Staged, not billed</small></section>
    <section><span>03</span><b>Invoke</b><small>Tokens + tool time</small></section>
    <section><span>04</span><b>Deliver</b><small>Outcome lands</small></section>
    <section class="is-committed"><span>05</span><b>Commit</b><small>Receipt changes</small></section>
  </div>
  <figcaption>Nothing becomes billable until the work crosses the delivery boundary.</figcaption>
</figure>
```
`.stages section.is-committed{ background:var(--accent); border-color:var(--accent); color:var(--ground); }`
(match the `.stages section` specificity or the base cell background wins — real bug.)
`.rail i{ animation:travel 4.8s cubic-bezier(.5,0,.5,1) infinite; }`

---

## 4. `loop-field` — claim is MUTUAL CAUSATION

**Claim:** "Agent evidence sharpens human judgment; judgment decides which evidence
matters." (Two loops feeding each other.)
**Structure:** two cycles + a coupling → **two orbits + a pulsing bridge.**
**Point (coral):** the bridge pulse (the calibration signal moving between them).

A single loop would miss the reciprocity; two orbits side by side with a dot
pulsing across the gap encode "each feeds the other." Center term of each orbit =
the *output* of that loop (Evidence / Judgment).

```html
<figure class="fig loops">
  <div class="system">
    <section><span>Technical loop</span>
      <div class="orbit"><i>Context</i><i>Action</i><i>Tests</i><i>Repair</i><b>Evidence</b></div></section>
    <section><span>Human loop</span>
      <div class="orbit human"><i>Observe</i><i>Question</i><i>Review</i><i>Learn</i><b>Judgment</b></div></section>
    <div class="bridge"><i></i><span>Calibration</span></div>
  </div>
  <figcaption>Agent evidence sharpens human judgment; human judgment decides which evidence matters.</figcaption>
</figure>
```
`.bridge i{ background:var(--accent); border-radius:50%; width:6px; height:6px; animation:pulse 2.2s ease-in-out infinite alternate; }`

---

## 5. `condition-tree` — claim is a BRANCH under uncertainty

**Claim:** "A recursive evaluation preserves inspectable conditions at every branch
instead of one irreversible transcript."
**Structure:** a decision that forks → **node/branch SVG tree** with a signal that
falls from root to a leaf, and a blurred "ghost" of the same paths beneath for depth.
**Point (coral):** the falling signal dot.

The ghost path (blurred, low opacity) is the "irreversible transcript" the claim
argues against; the crisp branch tree on top is the inspectable alternative. Form
carries the argument's *contrast*.

```html
<figure class="fig tree">
  <svg viewBox="0 0 720 330" role="img" aria-labelledby="tree-cap">
    <g class="memory"><path d="M360 290V220M360 220 190 150M360 220 530 150M190 150 90 70M190 150 260 70M530 150 460 70M530 150 630 70"/></g>
    <g class="branches"><path d="M360 290V220M360 220 190 150M360 220 530 150M190 150 90 70M190 150 260 70M530 150 460 70M530 150 630 70"/></g>
    <g class="nodes"><circle cx="360" cy="290" r="9"/><circle cx="360" cy="220" r="7"/><circle cx="190" cy="150" r="6"/><circle cx="530" cy="150" r="6"/><circle cx="90" cy="70" r="5"/><circle cx="260" cy="70" r="5"/><circle cx="460" cy="70" r="5"/><circle cx="630" cy="70" r="5"/></g>
    <g class="labels"><text x="360" y="322" text-anchor="middle">OBSERVED STATE</text><text x="190" y="178" text-anchor="middle">VERIFIED</text><text x="530" y="178" text-anchor="middle">UNKNOWN</text><text x="90" y="48" text-anchor="middle">RECOMPUTE</text><text x="260" y="48" text-anchor="middle">REUSE</text><text x="460" y="48" text-anchor="middle">QUERY</text><text x="630" y="48" text-anchor="middle">DEFER</text></g>
    <circle class="signal" cx="360" cy="220" r="2"/>
  </svg>
  <figcaption id="tree-cap">A recursive evaluation tree preserves inspectable conditions at every branch instead of an irreversible reasoning transcript.</figcaption>
</figure>
```
`.memory path{ stroke:var(--quiet); stroke-width:11; opacity:.08; filter:blur(6px); fill:none; }`
`.branches path{ stroke:var(--line-strong); stroke-width:1; fill:none; }`
`.nodes circle{ fill:var(--ground); stroke:var(--ink); stroke-width:1.4; }`
`.signal{ fill:var(--accent); animation:signal 3.8s linear infinite; transform-box:view-box; }`

---

## 6. `state-flow` — claim is a TRANSFORMATION of representation

**Claim:** "Event history becomes observable conditions, which controllers reconcile
into state." (Data changing *form* through a pipeline.)
**Structure:** A → B → C where each stage looks *different* → **stage rail** where
each card contains a different mini-visual (pulsing bars → stacked conditions →
a readout chip).
**Point (coral):** the focus stage underline + the "READY" readout dot.

Each card's inner glyph *is* the data in that representation, so the reader sees the
transformation, not just labels with arrows.

```html
<figure class="fig flow">
  <div class="rail">
    <section><span>01 · events</span><b>Raw agent history</b>
      <i class="evt"><em></em><em></em><em></em><em></em></i></section>
    <span class="arrow">→</span>
    <section class="focus"><span>02 · observe</span><b>Compressed conditions</b>
      <div class="stack"><i data-tone="critical"></i><i data-tone="relevant"></i><i data-tone="info"></i></div></section>
    <span class="arrow">→</span>
    <section><span>03 · reconcile</span><b>Declarative state</b>
      <div class="readout"><i></i> READY</div></section>
  </div>
  <figcaption>Event history becomes observable conditions, which controllers reconcile into state.</figcaption>
</figure>
```

---

## 7. `lane-router` — claim is a DISPATCH / one-decision routing (NEW, shipped)

Built for a long-form blog post on agentic QA routing,
replacing an ASCII box diagram. **Light-themed to match the blog** (proof the method
+ elements adapt to a light host).

**Claim:** "One decision routes every task; the lane is chosen by where the work
already lives."
**Structure:** a single spine that fans to N mutually-exclusive outputs → **keyed
rows sharing one accent spine.** Each row = a key node (A/B/C) + its condition +
its destination. The coral vertical spine down the left connects all key nodes,
making "one branch, many lanes" literal.
**Point (coral):** the spine + the A/B/C key nodes (the routing itself is the point).

Why this over the branch tree (#5): a decision *tree* is for exploring uncertainty
(you don't know which leaf); a *router* is for dispatch (a known rule sends each task
to exactly one lane). Rows read faster than a fanned SVG when the lanes carry text.

```html
<figure class="edfig-lanes host" role="img" aria-label="One decision routes every test into one of three lanes">
  <div class="edfig-lanes__head">
    <span class="edfig-lanes__q">Which lane runs this test?</span>
    <span class="edfig-lanes__eyebrow">The one decision</span>
  </div>
  <div class="edfig-lanes__rows">   <!-- ::before draws the coral spine -->
    <div class="edfig-lane">
      <span class="edfig-lane__k">A</span>
      <span class="edfig-lane__cond">New behavior · no code yet · exploratory</span>
      <span class="edfig-lane__to"><span class="edfig-lane__name">Manual + Run with AI</span><span class="edfig-lane__act">Design cases → AI executes them</span></span>
    </div>
    <!-- B, C … -->
  </div>
  <figcaption class="edfig-lanes__cap">One branch routes every task; the lane is chosen by where the work already lives.</figcaption>
</figure>
```
Full CSS (light + dark override) lives in the post source
the post body, with a standalone preview page for review. Spine =
`.edfig-lanes__rows::before` (2px coral, left:14px aligns to node centers); nodes =
`.edfig-lane__k` (1.5px coral border, coral text, ground fill, z-index above spine).

---

## The point of these seven

They cover seven *claim structures*, not seven chart types:

| Claim structure             | Primitive           | Example |
|-----------------------------|---------------------|---------|
| a spectrum / gradient       | cell grid + fill    | 1 |
| ranked magnitudes           | horizontal bars     | 2 |
| sequence with a threshold   | stage grid + rail   | 3 |
| mutual causation            | coupled orbits      | 4 |
| branch under uncertainty    | node/branch tree    | 5 |
| transformation of form      | stage rail + glyphs | 6 |
| dispatch / one-rule routing | keyed rows + spine  | 7 |

Plus two more in the gallery (`assets/gallery.html`): accumulation-toward-a-target
(filling meter + threshold tick) and boundary/inside-vs-outside (framed region + a
crossing). If your post's claim doesn't match a row, **compose a new primitive** from
the atoms in `design-system.md §5`. The aesthetic is the tokens + typography law +
restraint; the *shape* is whatever makes your specific sentence obvious at a glance.
