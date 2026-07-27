# Editorial elements — the non-chart vocabulary

Beyond the figures, monotykamary.com and linear.app carry a set of reusable **page
elements** that give a post its editorial density: stat strips, status asides,
kickers, numbered chapter indexes, prose typography, inline cards. All extracted
from rendered source (2026-07-22). Same rules as the figures: mono for labels/data,
UPPERCASE micro-labels, hairlines, one coral accent, tokens from `design-system.md`
(pick the set matching the host page — light for a light blog).

Use these to lift a whole article, not just its charts.

---

## 1. Metric strip — a row of headline numbers

For 3–5 punchy figures (throughput, cost, counts). Big mono number + tiny uppercase
mono label, hairline-divided cells, ruled top and bottom.

```html
<figure class="metric-strip">
  <div>
    <div class="metric"><strong>75</strong><span>reference tokens / second</span></div>
    <div class="metric"><strong>3s</strong><span>typing burst gap</span></div>
    <div class="metric"><strong>50ms</strong><span>held-key collapse</span></div>
    <div class="metric"><strong>$0</strong><span>idle without output</span></div>
  </div>
</figure>
```
```css
.metric-strip{border-block:1px solid var(--line);margin:52px 0;padding:24px 0}
.metric-strip>div{display:grid;grid-template-columns:repeat(4,1fr)}
.metric{display:flex;flex-direction:column;justify-content:space-between;min-height:78px;padding:0 22px;border-right:1px solid var(--line)}
.metric:first-child{padding-left:0}.metric:last-child{border:0;padding-right:0}
.metric strong{font:490 30px/1.1 var(--mono);letter-spacing:-.05em;color:var(--ink)}
.metric span{font:7.5px/1.6 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--quiet)}
```
Accent one number (`color:var(--accent)`) only if one is the point.

---

## 2. Status aside — the "state of this piece" sidebar

A sticky metadata rail: STATUS (with a live dot), last revision, active repo/branch.
Signals a living document. On monotykamary it sits in a `post-grid` two-column layout
(`minmax(0,760px) minmax(200px,260px)`, gap 80px).

```html
<aside class="post-context">
  <div><span>Status</span><b><i></i>Still testing this</b></div>
  <div><span>Last substantial revision</span><b>July 20, 2026</b></div>
  <div><span>Active branch or repository</span>
    <a href="…">inloopstudio-team/pi-ledger<small>branch / main</small></a></div>
</aside>
```
```css
.post-context{display:grid;position:sticky;top:30px;border-top:1px solid var(--line-strong)}
.post-context>div{border-bottom:1px solid var(--line);padding:17px 0}
.post-context span{display:block;margin-bottom:8px;font:8px/1.5 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--quiet)}
.post-context b,.post-context a{display:block;font-weight:450;color:var(--ink-soft);overflow-wrap:anywhere}
.post-context b i{display:inline-block;width:5px;height:5px;margin-right:8px;background:currentColor;box-shadow:0 0 0 3px color-mix(in srgb,currentColor 12%,transparent)}
.post-context a small{display:block;margin-top:5px;font-size:8px;color:var(--quiet)}
```
The dot `i` can be colored by state (coral = active, quiet = settled).

---

## 3. Kicker + sigil — the eyebrow above a title

A tiny hand-drawn SVG mark + an uppercase mono status word. The sigil is a 32-box
with two hairline "trace" paths (one faint "memory" ghost) and a node dot; it's the
site's recurring signature. Cheap to redraw per post with a different trace.

```html
<div class="post-kicker">
  <svg class="post-sigil" viewBox="0 0 32 32" aria-hidden="true">
    <rect x=".5" y=".5" width="31" height="31" class="frame"/>
    <path class="trace trace--memory" d="M5 25C10 23 10 11 16 9S23 14 28 5"/>
    <path class="trace" d="M5 23C11 21 10 13 16 11S22 16 28 5"/>
    <circle cx="16" cy="11" r="1.6"/>
  </svg>
  <p>Still testing this</p>
</div>
```
```css
.post-kicker{display:flex;align-items:center;gap:10px;margin-bottom:28px}
.post-kicker p{margin:0;font:9px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.post-sigil{width:26px;height:26px;overflow:visible}
.post-sigil .frame{fill:var(--surface);stroke:var(--line)}
.post-sigil .trace{fill:none;stroke:var(--ink);stroke-width:1}
.post-sigil .trace--memory{stroke:var(--quiet);opacity:.35}
.post-sigil circle{fill:var(--accent);stroke:var(--ink);stroke-width:1}
```

---

## 4. Numbered chapter index (Linear /method)

For a long piece with real sections: uppercase group label, then rows of
`title …… N.N` with dotted dividers between groups. The decimals are mono +
`tabular-nums`. Only use when the content genuinely is an ordered sequence.

```html
<nav class="chapter-index">
  <div class="chapter">
    <span class="chapter__group">Direction</span>
    <a><b>Set the product direction</b><em>2.1</em></a>
    <a><b>Set useful goals</b><em>2.2</em></a>
    <a><b>Prioritize enablers and blockers</b><em>2.3</em></a>
  </div>
</nav>
```
```css
.chapter{border-top:1px dashed var(--line-strong);padding-top:18px;margin-top:26px}
.chapter__group{font:9px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.chapter a{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:9px 0;color:var(--muted);text-decoration:none}
.chapter a:hover b{color:var(--ink)}
.chapter b{font-weight:400;font-size:16px}
.chapter em{font:10px/1 var(--mono);font-style:normal;font-variant-numeric:tabular-nums;color:var(--quiet)}
```

---

## 5. Inline invitation card — a link that matters

A full-width bordered CTA row: label, mono sub-detail, animated arrow. For "go look
at the repo / read the next thing."

```html
<a class="article-invitation" href="…">
  <span>Have a look</span><small>inloopstudio-team/pi-ledger / main</small><b>→</b>
</a>
```
```css
.article-invitation{display:grid;grid-template-columns:1fr auto 30px;align-items:center;gap:20px;border-block:1px solid var(--line-strong);margin-top:76px;padding:22px 0;text-decoration:none;color:var(--ink)}
.article-invitation>span{font-size:20px;letter-spacing:-.025em}
.article-invitation small{font:8px/1.5 var(--mono);color:var(--quiet)}
.article-invitation b{font-weight:400;transition:transform .2s}
.article-invitation:hover b{transform:translateX(5px)}
```
Same skeleton, smaller, makes the **next-post** footer nav.

---

## 6. Prose typography (the body around the figures)

So embedded figures don't clash with the running text, match this scale. Body in
`--sans` (a host site may pin its own stack, e.g. Charter serif heads, Public Sans
body, JetBrains Mono for labels/code), heads
tight `--sans`.

```css
.prose{font:16px/1.72 var(--sans);color:var(--muted)}
.prose h2{margin:70px 0 18px;font:540 27px/1.18 var(--sans);letter-spacing:-.03em;color:var(--ink)}
.prose h3{margin:52px 0 13px;font:540 20px/1.25 var(--sans);letter-spacing:-.03em;color:var(--ink)}
.prose strong{font-weight:620;color:var(--ink-soft)}
.prose a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--line-strong);text-underline-offset:3px}
.prose a:hover{text-decoration-color:var(--ink)}
.prose blockquote{border-left:1px solid var(--ink);padding:4px 0 4px 20px;color:var(--ink-soft)}
.prose code{font:.86em/1.6 var(--mono);color:var(--ink)}
.prose pre{border:1px solid var(--line);background:var(--surface);padding:17px;overflow-x:auto}
.prose hr{border:0;border-top:1px solid var(--line);margin:52px 0}
```

---

## 7. Obsession / lede block — a bordered manifesto opener

Left-hairline headline block for the top of a flagship post: big display headline,
one-line description, a `dt/dd` meta row. The `::before`/`::after` draw an L-bracket
on the left edge.

Key CSS: `border-block:1px solid var(--line-strong)`, a `1px` absolute bar down the
left, headline `clamp(42px,5.5vw,68px)/0.98` weight 480 letter-spacing -.06em, meta
row of `dt` (8px mono uppercase quiet) + `dd` (10px mono ink-soft).

---

## When to reach for these vs a figure

- The claim has a **structure** (spectrum, ranking, branch, loop…) → a figure
  (`worked-examples.md`).
- You just need **editorial furniture** (headline numbers, status, section index,
  a strong link) → an element here.
- A flagship post uses both: obsession lede → prose with 1–2 figures → metric strip
  → invitation card → next-post nav, with a status aside in the margin.
