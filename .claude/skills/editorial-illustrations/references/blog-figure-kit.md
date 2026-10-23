# Blog figure kit

Starting kit for blog diagrams. Live reference: `../assets/blog-figure-kit.html` (all six figures plus the full `ef-` stylesheet). Open it through a local server, then copy the `<style>` block and the figure you need into the post.

**Rule:** a blog post body uses these HTML/SVG figures for diagrams. ASCII stays only in the animated header frames (`SLUG_ASCII_FRAMES` in `build.py`).

## Tokens and theme

- Prefix every class with a short post-specific namespace (`ef-` here) so two posts never collide on the index page.
- Light tokens on `:root`, dark override on `:root[data-theme="dark"]` using your site's dark palette (for example ground `#171b22`, line `#262c36`, ink `#f1f5f9`). On a site with its own theme toggle, never key dark mode off `prefers-color-scheme`.
- Accent `--ef-accent:#c15f3c` for text and strokes, `--ef-node:#d97757` for filled dots and cells. Coral marks the point of the figure, nowhere else.
- Kicker (`.ef__k`) and figcaption are mono, 9px, uppercase. The caption states the claim in one or two sentences.

## Six patterns

| Pattern | Use when the claim is | Motion |
|---|---|---|
| A. Fan-out rows | one artifact, several readers, some gaps | a dot pings each row in turn (`animation-delay` per row) |
| B. Step x run grid | behavior changes across runs or versions | a shaded column steps across runs (`steps(1)`) |
| C. Orbit vs relay | one owner vs a chain of handoffs | dot circles the orbit; underline fills each handoff in sequence |
| D. SVG tree + signal | identity or lineage from root to leaf | dot rides `offset-path` to the highlighted leaf |
| E. Stage rail | a pipeline with owners; some stages unbuilt | dot travels the rail and turns coral at the point stage; hatched = to build |
| F. Many-to-few mapping | information lost in a conversion | coral dashed edges animate `stroke-dashoffset` where states collapse |

## Screenshots and tweets

- `.ef-tw` (440px max, centered) for one tweet, `.ef-tw2` two-up grid that stacks under 700px. Link the image to the source post. Caption = author + date.
- `.ef-shot` for product or web screenshots, full column width, caption names the product and capture date.
- Crop tweet captures to the tweet card only: exclude the X sidebar, the reply box and the viewer's avatar.
- Product screenshots: reuse images already published on the site when they show the claim (for example `/assets/screens/*.png`). Mask customer PII.

## Gotchas (cost a retry)

- `.ef-grid>div{display:flex}` beats `.ef-col{display:none}` on specificity. Hide grid children with `.ef-grid>.ef-col`.
- SVG text labels and edges: leave about 15px between the end of a label and the next node's edge, or the line runs through the text. Check at 720 viewBox width.
- `text-transform:uppercase` on `.tag` changes IDs (`acct_8f2c91` becomes `ACCT_8F2C91`). Use `.lbl` for literal identifiers.
- Wrapped mono owner tags need `line-height:1.45`, or the two lines touch.
- Long run headers wrap badly at 375px. Break them as `Run 1<br>cold`.
- `scrollIntoView` on a site with smooth scrolling, so a screenshot taken right after shows the old position. Set `document.documentElement.style.scrollBehavior='auto'` and `scrollTo` first.
- If the preview server cannot read your build folder, copy it to a temp folder and serve it from there.
- Every motion block needs a `@media (prefers-reduced-motion:reduce)` kill, and the signal dots should be hidden (opacity 0) there.

## Verify before publishing

1. Build, serve the copy, and screenshot every figure at desktop width and at 375px.
2. Check that no `figure` has `scrollWidth > clientWidth`.
3. Read each image against its caption: is the coral element the one that proves the claim?

## Product UI recreations

Raster product screenshots can look soft on a blog. Rebuild them as HTML instead: a figure with a window bar, left nav, and the real layout, styled with your brand tokens. Copy the real values (names, durations, counts) from the source screenshot, and caption it "Recreated from <product>" with the date. Mask customer data. Never present a proposed feature as a recreation; label mockups as mockups.

## Tweet captures

Capture tweets from the official embed in a headless browser at 2x, light theme:
`https://platform.twitter.com/embed/Tweet.html?id=<id>&theme=light&dnt=true&hideThread=true`, then screenshot the first `article` with Playwright (`device_scale_factor=2`, viewport 560 wide) and save as JPEG q90. This renders logged out and gives about 1100px wide images.

- Do not capture through your everyday Chrome profile. Background windows never paint, so captures come out black, and an automation daemon attached to a real tab navigates that tab away.
- x.com status pages do not render in a logged-out headless browser. Use the embed URL.

## Markdown gotcha

A blank line inside the post's `<style>` block ends the raw-HTML block, and the markdown renderer then swallows the rest of the post into the style element (empty page). Keep every `<style>` block free of blank lines.
