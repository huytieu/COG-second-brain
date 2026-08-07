# Design system — the raw grammar

Reverse-engineered from the rendered source of **monotykamary.com** posts and
**linear.app/now** (2026-07-22). Both share one DNA; this file is the extracted,
coral-adapted building set. Copy tokens and base rules verbatim; invent the figure
markup per post (see `SKILL.md` for the method).

## 1. Tokens (coral house style)

Grayscale base (the mono DNA), **one** accent = Claude-coral. The accent marks the
*point* of the figure and nothing else. **Pick the token set that matches the host
page** (light page → light set), and ship the other as an override so the figure
adapts. Dark set first, then two light variants (a warm generic one and the exact
host-site-matched one).

```css
:root {
  /* surfaces */
  --ground:        #080807;   /* page / deepest field           */
  --ground-deep:   #030303;   /* recessed track behind fills    */
  --surface:       #080807cc; /* framed-figure background (alpha)*/
  --surface-solid: #0c0c0b;   /* solid card inside a figure      */
  /* ink ramp */
  --ink:       #f2f2ed;       /* primary text, strong marks      */
  --ink-soft:  #d0d0c9;       /* secondary fills, sub-headlines  */
  --muted:     #92928a;       /* labels                          */
  --quiet:     #5f5f59;       /* axis numbers, captions, index   */
  /* structure */
  --line:        #292925;     /* hairline borders, gridlines     */
  --line-strong: #54544e;     /* branch strokes, dashed rails    */
  /* THE one accent */
  --accent:      #D97757;     /* Claude-coral — the single color */
  --accent-soft: #e6a488;     /* coral tint for a second beat    */
  /* type */
  --sans: "Inter", "Inter Variable", system-ui, sans-serif;
  --mono: "JetBrains Mono", "JetBrains Mono Variable", ui-monospace,
          "SF Mono", Menlo, Consolas, monospace;
}

/* Light variant A — warm, monotykamary-flavored inverted field. */
:root[data-theme="light"], .light {
  --ground:#f7f7f2; --ground-deep:#ecece6; --surface:#f7f7f2cc; --surface-solid:#fbfbf7;
  --ink:#191917; --ink-soft:#3d3d38; --muted:#6a6a62; --quiet:#9a9a90;
  --line:#deded6; --line-strong:#b7b7ad;
  --accent:#c15f3c; --accent-soft:#d97757; /* coral darkened for AA on light */
}

/* Light variant B — EXACT host-site match. Use this for blog-embedded figures.
   Blog tokens: --bg:#f7f8fb, surface #fff, text #111827, muted #64748b,
   border #e2e8f0, body font JetBrains Mono. Cool grays, coral accent. */
:root[data-theme="host"], .host {
  --ground:#ffffff; --ground-deep:#f1f3f7; --surface:#ffffff; --surface-solid:#ffffff;
  --ink:#111827; --ink-soft:#334155; --muted:#64748b; --quiet:#94a3b8;
  --line:#e6e8ee; --line-strong:#cbd5e1;
  --accent:#c15f3c;      /* coral, AA-safe on white for text/strokes */
  --accent-node:#d97757; /* house coral for large node fills only    */
}
```

On a light ground, drop `backdrop-filter: blur()` (nothing to blur over white) and
add a faint `box-shadow: 0 1px 2px rgba(16,24,40,.04)` on the frame so it lifts off
the page. On dark, keep the blur and no shadow.

Original grayscale-faithful mode: set `--accent: var(--ink)` (accent == white). That
is monotykamary 1:1. Coral is our deviation, applied as a single token so it is
one line to switch.

## 2. Typography law

- **Display** = `--sans`, weight **480–540**, tight tracking **-0.03em to -0.06em**,
  line-height ~0.98. Big and quiet. (monotykamary h1 = 68px / weight 480 / -4px.)
- **Everything else in a figure is `--mono`**: labels, axis numbers, values,
  captions, the index numerals (`01 02 03`). Tiny — **7px to 11px**.
- **Labels & captions are UPPERCASE**, `letter-spacing: 0.04em–0.1em`.
- Values that carry the number are `font-weight: 700`, colored `--ink` or `--accent`.
- Never mix a second sans. Never use a display weight above ~560.

Observed sizes (use as the scale): caption/axis **7–8px**, label **10px**,
figure sub-headline (`<b>`) **11px**, index **8px**.

## 3. The framed figure (chrome)

Every illustration is a `<figure>` with a hairline frame and a mono UPPERCASE
`<figcaption>` that states the *meaning*, divided by a top rule.

```css
.fig {                       /* base frame for every illustration */
  border: 1px solid var(--line);
  background: color-mix(in srgb, var(--surface) 72%, transparent);
  backdrop-filter: blur(16px);
  margin: 52px 0;
  padding: 20px;
}
.fig figcaption {
  border-top: 1px solid var(--line);
  color: var(--quiet);
  font: 8px/1.6 var(--mono);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-top: 18px;
  padding-top: 13px;
}
.fig svg { width: 100%; height: auto; display: block; }
```

SVG figures use a **720-wide viewBox** (`viewBox="0 0 720 <h>"`) so labels stay
crisp and math is easy. Give every figure `role="img"` + `aria-label`, or
`aria-labelledby` pointing at the figcaption.

## 4. Restraint rules (what makes it not-slop)

1. **Grayscale + exactly one accent.** Coral appears on 1–2 elements: the row that
   is the point, the committed state, the live signal. If everything is coral,
   nothing is.
2. **Hairlines only.** 1px borders, 1px gridlines. No drop shadows except the
   `inset 0 2px var(--ink)` focus underline. No rounded corners except true circles
   (nodes, orbit).
3. **No chartjunk.** Gridlines only when the figure is quantitative (a real axis).
   No legend if labels sit on the marks. No 3D, no gradients except a single
   axis-direction hairline gradient (`--quiet → --ink`).
4. **Density is the aesthetic.** Small mono type, tight cells, edge-to-edge. White
   space is structural, not padding.
5. **Motion is meaning or nothing.** One subtle loop that *demonstrates the claim*
   (a signal travelling a pipeline, a bridge pulse between two loops). 2–6s,
   `ease-in-out`. Always wrap in `@media (prefers-reduced-motion: reduce)` to kill it.

## 5. Reusable primitives (CSS blocks)

These are the atoms observed across the six worked examples. Compose them into new
figures; do not treat them as fixed charts.

### 5a. Cell grid (spectrum / pipeline / rail)
Row of bordered cells, each with an index, a bold label, a small descriptor, and an
optional bottom "fill" bar whose height/opacity encodes a value.

```css
.cells { display:grid; grid-template-columns:repeat(var(--n,5),1fr); }
.cells section { position:relative; overflow:hidden; display:flex; flex-direction:column;
  min-height:145px; padding:12px; border:1px solid var(--line); border-right:0; }
.cells section:last-child { border-right:1px solid var(--line); }
.cells section > span  { color:var(--quiet); font:8px/1 var(--mono); }        /* index */
.cells section > b     { margin-top:auto; color:var(--ink); font-size:11px; font-weight:540; }
.cells section > small { margin-top:5px; min-height:32px; color:var(--muted); font:7px/1.4 var(--mono); }
/* value-as-fill: set --v (0..1) per cell */
.cells section > i { position:absolute; inset:auto 0 0; height:calc(var(--v)*100%);
  background:var(--accent); opacity:calc(.10 + var(--v)*.5); transition:height .4s; }
.cells section:hover > i { opacity:calc(.25 + var(--v)*.6); }
```

### 5b. Horizontal bars (ranked magnitude)
SVG, 720 viewBox. Track = `--ground-deep`, fill = `--ink-soft`; the **point row**
fill = `--accent`. Value label mono-bold, right-aligned inside/after the bar.

```css
.bars .track { fill:var(--ground-deep); }
.bars .fill  { fill:var(--ink-soft); transition:opacity .18s; }
.bars .row--accent .fill { fill:var(--accent); }
.bars .row:hover .fill, .bars .row:focus .fill { opacity:.72; }
.bars .label { fill:var(--muted); font:10px var(--mono); }
.bars .grid line { stroke:var(--line); }
.bars .grid text { fill:var(--quiet); font:8px var(--mono); }
.bars .value { fill:var(--ink); font:700 8px var(--mono); }
.bars .row--accent .value { fill:var(--accent); }
```
Bar math (viewBox 720, plot x0=246 → x1=672, so width=426): `fill_w = 426 * pct/100`.

### 5c. Node + branch (tree / decision)
SVG circles on `--ground` with `--ink` stroke; branch paths `--line-strong` 1px;
an optional blurred "memory" path underneath (same path, `--quiet`, blur(6px),
opacity .08) for depth; a small animated `--accent` signal dot travelling a branch.

### 5d. Orbit (a cyclic loop)
A `border-radius:50%` ring (`--line-strong`) with a dashed inner ring (`inset:20%`),
four mono labels pinned N/E/S/W, and a bold center term. Breathe animation optional.
Two orbits + a pulsing bridge line = *coupled* loops.

### 5e. Stage rail (transformation flow)
`grid-template-columns:1fr 28px 1fr 28px 1fr` — cards separated by mono `→` arrows.
The focus stage gets `box-shadow: inset 0 2px var(--accent)`. Inside a card, tiny
animated glyphs (bars pulsing = event stream; stacked bars = compressed conditions;
a `state-readout` chip = reconciled state).

## 6. Animations (opt-in, reduced-motion-safe)

```css
@keyframes travel   { 0%{left:0} 45%,65%{left:58%} 100%{left:calc(100% - 7px)} }
@keyframes pulse    { 0%{opacity:.25;left:0} 100%{opacity:1;left:calc(100% - 6px)} }
@keyframes breathe  { 50%{transform:rotate(2deg) scale(1.015)} }
@keyframes signal   { 0%,12%{opacity:0;transform:translateY(0)} 24%{opacity:1}
                      72%,82%{opacity:1;transform:translateY(70px)}
                      94%,100%{opacity:0;transform:translateY(70px)} }
@keyframes evt      { 0%,100%{opacity:.25} 50%{opacity:1} }
@media (prefers-reduced-motion: reduce){ * { animation:none !important; } }
```
SVG-animated marks need `transform-box: view-box`.

## 7. Fonts

Self-host or `@font-face` Inter + JetBrains Mono for fidelity. Acceptable fallback:
`system-ui` + `ui-monospace`. Linear uses Berkeley Mono; monotykamary uses JetBrains
Mono — both read identically at these sizes. Do **not** ship Google-Fonts `<link>`
in an Artifact (CSP blocks it); inline `@font-face` with data-URIs or fall back.
