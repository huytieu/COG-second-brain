---
name: vector-cover
description: >
  Generate flat vector editorial cover illustrations in a warm editorial style:
  near-black canvas, cream organic blob, serif display type, one terracotta
  accent, and thin line-art concept motifs (grids, node charts, dashed
  "unknown" paths, mountains, question marks). Output is code (HTML + inline
  SVG) rendered to a crisp 2400x960 PNG via headless Chrome. Use when you want
  a blog, article or X-article cover image, a "hero graphic", or "make a cover
  for <title>".
---

# Vector cover

## Configuration

The palette below is a default. Swap the hex values in `template.html` for your own brand, and keep the rule of exactly one accent color. Cover copy (eyebrow, title) comes from your article, not from this skill.

## Requirements

- Google Chrome or Chromium. `render.sh` finds it in the standard macOS locations or on `PATH`. Set `CHROME` to override.
- No other dependencies, and no browser automation setup.

## What this is

A designed vector graphic built as code: flat SVG on a small set of color tokens, rendered and screenshotted. It is not a diffusion image.

- Yes: flat vector, geometric line-art, precise serif type, one accent color.
- No: photorealism, gradients, glow, drop shadows, 3D, texture. If a request needs a photo, this is the wrong tool.

## Design system (default palette, configurable)

| Token   | Hex        | Use                                          |
|---------|------------|----------------------------------------------|
| ink     | `#141413`  | background canvas                            |
| ivory   | `#FAF9F5`  | the organic blob and primary headline text   |
| clay    | `#D97757`  | accent: eyebrow, rule, the "unknown" motif   |
| grid    | `rgba(20,20,19,.09)` | faint grid drawn inside the blob   |
| undercurve | `#E7D9C4` | faint warm curves near the blob's base     |

Rules:

- Exactly one accent color (clay by default). Never add a second hue.
- Serif for the eyebrow (italic) and the headline (bold). Sans only for tiny annotations.
- Keep the dark field mostly empty. 3-5 decorative marks at most, low opacity.
- Everything on the cream is clipped to the blob. Nothing floats half off it except the intentional motif that escapes (for example the dashed unknown path).

## Canvas

`1200 x 480` logical (2.5:1), rendered at 2x → **2400x960 PNG** (X-article cover
size). For a square social card use `1200x1200`; for a 16:9 slide use `1280x720`
and pass those to `render.sh`.

## Layout skeleton (every cover)

```
+--------------------------------------------------------------+
|                                          ? (clay, top-right) |
|  A Field Guide:   (eyebrow, italic clay)   .-''''-. |
|                                                   /  BLOB   \|
|  Finding Your              (headline, bold ivory)|  + grid   |
|  Unknowns                                        |  + MOTIF  |
|  ___ (clay rule)                                  \        / |
|                                                    '-....-'  |
+--------------------------------------------------------------+
   left ~40% = type            right ~60% = blob + concept motif
```

## The concept motif is the whole point

Every cover encodes the article's *idea* as a small line-art diagram inside the
blob. Pick / adapt from this library (or invent one in the same visual grammar):

| Article theme | Motif |
|---------------|-------|
| journey, growth, unknowns, "map vs territory" | rising curve, solid→dashed, node dots, a `?` and mountains at the frontier (the shipped `template.html`) |
| agents, systems, networks | 5-7 nodes joined by thin lines; one node filled clay = the active one |
| architecture, layers, stack | 3-4 stacked rounded rects, offset, one outlined clay |
| search, exploration, discovery | scattered dots + a dashed search path weaving between them + one magnifier ring |
| tradeoff, comparison, A vs B | two curves crossing; the winner solid, the other dashed |
| pipeline, process, workflow | left→right stages (small circles) joined by arrows; last one clay |
| iteration, loops, refinement | a spiral / concentric arcs tightening toward a center dot |

Motif drawing rules: strokes `#141413` at 2–2.6px, `stroke-linecap="round"`;
hollow nodes = `fill=ivory stroke=ink`; filled nodes = `fill=ink`; anything
"uncertain / future / unknown" is **dashed and clay**.

## Workflow

1. Get inputs from the user, or infer them from the article:
   - `eyebrow` (italic kicker, e.g. "A Field Guide:") - optional.
   - `title` (1–2 short lines; break it yourself for balance).
   - `theme` → pick a motif from the table above.
   - `size` (default 1200x480).
2. **Copy the template**: start from `template.html` in this folder. It already
   has the tokens, blob, grid, type block, and the journey motif wired up.
3. **Edit three regions only**:
   - the `<text>` nodes (eyebrow / two headline lines / rule width),
   - the CONCEPT MOTIF group (swap for the theme's motif),
   - the 3–5 decorative marks on the dark field.
   Leave the blob path, grid, and token colors alone unless deliberately restyling.
4. **Render**:
   ```bash
   .claude/skills/vector-cover/render.sh <in.html> <out.png> [W] [H]
   # e.g. render.sh cover.html cover.png            -> 2400x960
   #      render.sh cover.html card.png 1200 1200    -> 2400x2400
   ```
   `render.sh` launches its own headless Chrome. It needs no remote-debugging port and no browser automation setup.
5. **Verify visually**: Read the PNG. Check nothing is clipped off-canvas
   (the escaping motif must land on the dark field, not get cut), text fits the
   left ~40%, and the blob doesn't collide with the headline. Iterate on coords.
6. Deliver the single PNG. Keep working files in your project folder.

## Font note

The template uses a system serif stack (`Charter`/`Iowan Old Style`/Georgia).
For a pixel-exact editorial look, drop a `@font-face` (e.g. a Tiempos/Copernicus-
like serif) as a base64 `data:` URI at the top of the HTML - headless Chrome
renders embedded fonts fine. Do not link remote fonts (offline render).

## Gotchas

- **Off-canvas clipping**: `<text>` anchored past x=1200 (or the escaping motif)
  gets cut. Keep the "unknown" cluster inside the canvas on the dark strip right
  of the blob (~x 1120–1195).
- **Headline overflow**: at 72px the serif eats ~11 chars/line. Longer titles →
  drop to 60px or add a third line; re-check against the blob's left edge (~x498).
- **Blob edge vs grid**: the grid is clipped to the blob, so extend grid lines
  well past the blob bounds - clipping handles the rest.
- **Never** add gradients, shadows, blur, or a second accent color. One clay.
```
