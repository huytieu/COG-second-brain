---
name: editorial-illustrations
description: >
  Generate meaning-carrying editorial data-illustrations in the monotykamary /
  Linear aesthetic (near-black grayscale, Inter display + mono labels, hairline
  framed figures) with a single coral accent. This is a GENERATIVE GUIDE, not a
  template gallery: it teaches the "claim -> geometry" method so any session can
  invent the RIGHT figure for what a post actually argues, then render it as a
  self-contained, theme-aware, reduced-motion-safe HTML/SVG figure. Use when
  writing/illustrating a blog post, essay, spec, or slide and you want a chart,
  diagram, or illustration that carries a thesis (not decoration) in the house
  style. Triggers: "make a chart/diagram/illustration for this", "visualize this
  argument", "monotykamary/Linear style figure", "editorial graphic".
---

# Editorial illustrations — claim → geometry

The look you want (monotykamary.com, linear.app/now) is not a chart library. It is
a **discipline**: every figure is a single argument rendered as geometry, framed in
a hairline box, captioned in mono uppercase with the *meaning*, drawn in grayscale
with exactly one accent. Get the discipline right and any shape reads as "house."
Copy templates blindly and it reads as slop.

**Do not reach for a fixed set of charts.** Reach for the method below and build the
figure this specific sentence needs. The six worked examples in
`references/worked-examples.md` are proof the method generalizes, not a menu.

## The core move

> Take the one sentence the figure must prove. Find that sentence's *structure*.
> Render the structure so the reader believes the sentence before reading it.

The caption is the thesis, written first. If you can't state the figure's claim in
one sentence, you don't have a figure yet, you have decoration. Stop.

## Method (run this every time)

1. **Write the claim.** One declarative sentence. This becomes the `<figcaption>`
   verbatim. Example: "Nothing is billable until work crosses the delivery boundary."

2. **Name the claim's structure.** Which of these is the sentence really about?
   Match to a geometric primitive:

   | If the claim is about…                    | Render it as…                | Atom (§5) |
   |-------------------------------------------|------------------------------|-----------|
   | a spectrum / more-vs-less / a gradient    | ordered cells, rising fill   | 5a |
   | ranked magnitudes / shares / a comparison | horizontal bars, real axis   | 5b |
   | a sequence with a tipping point           | stage grid + traveling dot   | 5a + rail |
   | mutual causation / a feedback relationship| two coupled orbits + bridge  | 5d |
   | a branch / decision under uncertainty     | node-and-branch SVG tree     | 5c |
   | one thing changing form / a data pipeline | stage rail, a glyph per stage| 5e |
   | accumulation toward a target              | stacked / filling bar        | 5a/5b |
   | a boundary / inside-vs-outside            | a framed region + a crossing | compose |
   | a distribution / where mass sits          | dot-strip or small-multiples | compose |

   If nothing matches, **compose a new primitive** from the atoms in
   `references/design-system.md §5`. The novelty is expected and welcome; the
   *tokens and restraint* are what must stay constant.

3. **Locate the point.** Which single element proves the claim? That one gets
   `--accent` (coral). Everything else stays grayscale. One accent, maybe two.
   No point → the figure has no thesis → go back to step 1.

4. **Draw in the system.** Apply `references/design-system.md`: tokens, the
   typography law (display = Inter 480–540 tight; everything else mono, tiny,
   UPPERCASE labels), the framed-figure chrome, 720-wide SVG viewBox, hairlines
   only, no chartjunk.

5. **Add motion only if it demonstrates the claim.** A dot that pauses before a
   boundary; a pulse crossing between two loops; a signal falling down a branch.
   2–6s, `ease-in-out`, and always killed under `prefers-reduced-motion`. If motion
   doesn't *show* the argument, omit it. Static is fine and often better.

6. **Caption it.** Mono, 8px, uppercase, above-the-rule. State the meaning, not the
   data source alone. ("…because X," not "Figure 3.")

## The aesthetic in one breath

- **Field:** matches the host — near-black `--ground:#080807` on a dark page, white/
  off-white on a light page (both token sets in `design-system.md`). Framed figures
  on a faint surface; `backdrop-filter: blur(16px)` on dark, a hairline + faint
  shadow on light.
- **Type:** Inter for the rare big display; **mono for everything inside a figure**,
  7–11px, labels/captions UPPERCASE. Never a second sans, never a bold display.
- **Color:** grayscale ramp (`--ink → --quiet`) + **one** accent = Claude-coral
  `#D97757`, on the point only. (Set `--accent: var(--ink)` for monotykamary-faithful
  pure grayscale.)
- **Structure:** 1px hairlines, true-circle nodes, dashed = provisional/failure,
  no shadows, no gradients except a single axis-direction hairline.
- **Density:** small type, tight cells, edge-to-edge. Restraint is the style.

Full spec + copy-paste token blocks (dark AND light) + primitive CSS:
`references/design-system.md`. Worked examples with the claim→geometry reasoning:
`references/worked-examples.md`. Non-chart editorial elements (metric strip, status
aside, kicker+sigil, numbered chapter index, prose type, inline cards):
`references/elements.md`. Live rendered proof (coral house style, toggleable):
`assets/gallery.html`.

## The figure follows the host page's theme (ALWAYS)

A figure is a guest on someone's page. It must match that page's light/dark, not
impose its own. A dark exhibit panel dropped into a light article reads as a foreign
object (learned the hard way, 2026-07-22).

- **Look at the host first.** Light page → light figure. Dark page → dark figure.
  a host site may default **light** and carry its own **theme toggle** (e.g. Charter serif heads + Public Sans body,
  blue accent) that stamps `data-theme="light"|"dark"` on `<html>` — figures there
  must **follow `data-theme`**, defaulting light.
- **If the host has an explicit theme system, key the dark override off IT, not the
  media query.** Use `:root[data-theme="dark"] .yourfig { … }`, NOT
  `@media (prefers-color-scheme: dark)`. Real bug (2026-07-22): a figure keyed on the
  media query rendered **dark on the light blog** because the viewer's OS was dark and
  the page theme was light. The page's `data-theme` is the source of truth; the media
  query only applies on hosts that have no toggle. On a toggled host, match the site's own
  dark tokens (ground `#171b22`, line `#262c36`, ink `#f1f5f9`) so the figure's dark
  panel sits in the site's dark, not a foreign near-black.
- **Build token-based so it adapts.** Define the palette on the figure's own scope,
  default = the host's default theme, plus a `:root[data-theme="dark"] .fig` override
  (and a `@media (prefers-color-scheme: dark)` override too ONLY if the host has no
  toggle). Costs nothing, future-proofs the figure.
- **Coral is AA-safe per ground.** On white use `--accent:#c15f3c` for text/strokes
  (keep `#D97757` only for large node fills); on near-black use `#D97757` directly.
- The **claim→geometry method and the restraint rules are theme-independent.** Only
  the palette tokens swap. Grayscale-ramp + one coral accent holds on both grounds.

## Output contract

- One self-contained `<figure>` per illustration: inline `<style>` scoped to the
  figure (or shared token `:root`), inline SVG, no external requests.
- **Theme = host's** (see above): light default when embedded in a light page, but
  always token-based with `prefers-color-scheme` + `:root[data-theme]` overrides, and
  **reduced-motion-safe**. Both are house rules, not optional.
- For an **Artifact**: no external fonts/CDN (CSP blocks them); inline `@font-face`
  data-URIs or fall back to `system-ui`/`ui-monospace`.
- For **blog posts on your own site**: emit the figure HTML/CSS into the post body (markdown
  passes raw HTML through verbatim via `build.py`). The blog is **light**, so the
  light tokens apply; keep the dark override for portability. Rebuild with
  `python3 build.py`; the built page uses absolute asset paths so preview it via a
  local server or a self-contained standalone copy, never a bare `file://` open
  (that renders the post unstyled). See a local self-contained HTML preview.

## Verify (mandatory — this is a UI/UX output)

Per the Visual Verification rule, a DOM check is not enough. **Render it and look.**

1. Open the figure in browser-harness, screenshot it (`evidence_shot`).
2. Read the image against the claim: does the geometry make the sentence obvious?
   Is coral on the point and nowhere else? Any clipped mono text, misaligned SVG
   labels, off-by-one bar math, broken responsive stack at ≤720px?
3. Fix what you see, re-shot to prove it. Check the light variant too.
4. Confirm motion stops under reduced-motion.

## Anti-slop checklist (reject the figure if any fail)

- [ ] The figcaption is a real claim, stated in one sentence.
- [ ] The geometry encodes that claim's *structure* (not a generic chart pinned on).
- [ ] Exactly one accent element (coral), on the point.
- [ ] Every in-figure label/value/caption is mono + tiny; labels UPPERCASE.
- [ ] Hairlines only; no shadows, no gradients (bar-axis hairline excepted), no
      rounded rectangles.
- [ ] Gridlines present only if the figure is genuinely quantitative.
- [ ] Motion (if any) demonstrates the claim and dies under reduced-motion.
- [ ] Renders correctly in both dark and light, and stacks cleanly on mobile.
