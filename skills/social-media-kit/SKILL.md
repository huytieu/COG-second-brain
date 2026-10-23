---
name: social-media-kit
description: Produce and attach native media (video teaser, GIF, card images) for every social post to maximize reach and interaction. Use whenever you post to X, LinkedIn, Reddit, or prepare HN/IndieHackers handoffs, and whenever a social-publishing step runs. A text-only social post is a draft, not a post.
---

# Social media kit

Every social post carries a video, GIF, or image. Native media is the largest reach lever the feed algorithms give you. This skill defines the kit of assets, the visual rules that keep a campaign from looking templated, and the browser mechanics for attaching media on each platform.

## Configuration

Set these once. Scripts read them from environment variables, so nothing personal is hardcoded.

| Setting | Env var | Default |
|---|---|---|
| Signature shown bottom-right on cards | `BRAND_URL` | `yourblog.example` |
| Output folder for cards | `CARD_OUT_DIR` | `.` |
| Screenshot for the runner card | `CARD_SCREENSHOT` | unset (card skipped) |
| Quote card attribution | `QUOTE_ATTRIBUTION` | `Your Name · your role` |
| Pass / fail dot colors | `CARD_ACCENT_PASS`, `CARD_ACCENT_FAIL` | `3DD68C`, `F2555A` |
| Banner accent color | `BANNER_ACCENT` | `e13f5e` (coral, configurable) |
| Fonts | `HEADLINE_FONT`, `MONO_FONT` | macOS Helvetica Neue and Menlo, DejaVu on Linux |

Your handles, avatar and brand colors belong in your own config or prompt, never in this skill.

## Requirements

- Python 3 with Pillow (`pip install pillow`)
- ffmpeg, for teaser cuts and clips
- A browser automation tool that can drive your logged-in Chrome over CDP (for example the `browser-harness` skill, if you have it)

## The kit contract

Before posting, produce a kit folder (`<scratchpad>/social-kit-<slug>/`) with whichever of these the source material supports, in priority order:

| Asset | Spec | Best for |
|---|---|---|
| `teaser-16x9.mp4` | 30-60s cut of a master video, hook in the first 3s, H.264/AAC, captions burned in (feeds autoplay muted) | X thread root, LinkedIn |
| `teaser-1x1.mp4` | Same cut, 1080x1080 center-crop or pad | Mobile feeds |
| `hero-card.png` | 1600x900 card with a padded screenshot or lane art | X, LinkedIn, Reddit image |
| `terminal.gif` | Animated terminal replay, 15MB or less (X GIF cap), 2-6 frames or a reveal sequence | X, Reddit |
| `quote-card.png` | 1600x900 dark card with one strong line | Follow-up posts, LinkedIn comment |

Reuse before creating. If your blog pipeline already produces per-post assets (OG gif, screenshots, a deep-dive mp4), a 30-60s ffmpeg cut of an existing master video beats a new render.

## Style variety across a campaign

One visual language repeated on every asset reads as AI-generated. Rules:

- Never render every asset in a campaign in the same style. Rotate: lane-art card, terminal replica (see the `terminal-replica` skill), ASCII or OG gif, bare quote card, raw screenshot or recording.
- Match style to audience. Developer forums get terminal replicas or raw screenshots, because authentic beats polished. LinkedIn and X heroes get designed cards.
- PIL gotcha for terminal renders: Menlo lacks the TUI glyphs for the record dot, the elbow and the spinner. Draw them as vector shapes (filled circle, elbow lines), never ship tofu boxes.

## House card style

Cards follow a dark thin-line art language, inspired by linear.app/now. The renderer is `scripts/linearcard.py`. The accent colors and signature are configurable.

- Canvas 1600x900 (render at 2x, LANCZOS downscale). Background `#0A0B0D`, flat. No gradients, no glow, no dot grids.
- Art is thin-line lane fields: horizontal 1.5px `#43464C` strokes flowing left to right, dots `#9A9DA2` at start points, arrowheads at ends, lines breaking around thin circle nodes. Dashed lanes mean failures. The only accents are tiny green (pass) and red (fail) dots.
- Type: a bold sans for the big headline (white, 2-3 short lines, top-left). Mono for the eyebrow and data chips. Never set the headline in mono, and never bury the message in a caption.
- Real numbers in a chip row ("7 passed · 4 failed"), not decoration.
- Signature bottom-right: your URL in bold mono plus a cursor block. Nothing else.
- Screenshots sit on the art field with a 1px `#303338` border and 20px rounded corners. Never full-bleed. Keep a headline beside them.
- Anything terminal-looking follows the `terminal-replica` skill.

```bash
BRAND_URL="myblog.dev" CARD_OUT_DIR=./kit python3 .claude/skills/social-media-kit/scripts/linearcard.py
```

The three cards in the script are examples. Edit the copy and numbers for your post.

## Content type to visual treatment

Pick the treatment by what the post is, not by one default recipe.

| Post is about | Reach for | Why |
|---|---|---|
| A flagship or launch idea | `linearcard.py` art field, but invent one concrete metaphor object for this post first (a shape that puns the idea) | A bespoke metaphor is more scroll-stopping than the same background every time |
| "Watch it actually run" proof (a real terminal session, an agent run) | `cardrender.py` screenshot or clip without the padded card frame, raw footage | A card frame reads as marketing polish. Raw footage reads as "this is happening" |
| A tool or stack story with numbers | `linearcard.py` standard recipe with a mono data-chip row | The data chips carry the story |
| A long essay excerpt or killer quote | `quote-card.png`, and drop the lane art entirely: pure type on the dark field | Background linework competes with a typographic excerpt |

## Thread media placement

In any multi-message thread (X thread, LinkedIn post plus comments, Reddit post plus comments), media goes on the first message only, preferably a gif or video. Later messages stay text-only unless an illustration adds information (a chart under discussion, a before/after). Decorating every reply with a card reads as botting and dilutes the root asset.

## Production recipes

### Teaser cut from a master video

```bash
# pick the strongest 30-60s arc: hook section plus one payoff section
ffmpeg -i master.mp4 -ss <hook_start> -to <hook_end> -c copy a.mp4
ffmpeg -i master.mp4 -ss <payoff_start> -to <payoff_end> -c copy b.mp4
printf "file 'a.mp4'\nfile 'b.mp4'\n" > cut.txt
ffmpeg -f concat -safe 0 -i cut.txt -c:v libx264 -crf 21 -pix_fmt yuv420p teaser-16x9.mp4
# 1:1 variant
ffmpeg -i teaser-16x9.mp4 -vf "crop=ih:ih,scale=1080:1080" -c:a copy teaser-1x1.mp4
```

If the teaser relies on narration, burn subtitles (`-vf subtitles=teaser.srt:force_style='FontSize=22'`). Muted autoplay kills uncaptioned voice-over.

### Padded-card screenshots and cursor-animated clips

`scripts/cardrender.py` renders 1920x1080 frames: a screenshot floating on a gradient with rounded corners and shadow, an optional animated cursor with click ripples, row highlight pulses, and zoom. Use `Seg(...)` and `render()` for motion clips. For a static `hero-card.png`, render one frame:

```python
from cardrender import Seg
seg = Seg("screenshot.png", 1.0, waypoints=[(0.5, 800, 400)], clicks=[], highlights=[], zoom=None)
seg.frame(0.5).save("hero-card.png")
```

Edit the gradient colors at the top of `make_bg()` to match your brand.

### Terminal GIF

Author frames with PIL and a mono font on a dark background, reveal lines progressively, then `img.quantize(colors=64)` and `save(..., save_all=True, duration=[...], loop=0)`. Keep under 15MB for X: 64 colors and 20 frames or fewer does it.

### Terminal-style banner (article cover)

`scripts/terminal_banner.py <out.png>` draws a 5:2 (1500x600) terminal-window banner with a prompt line, a big wordmark with a block cursor, status lines and a feature list. Edit the CONFIG block per product. Use it when a raw app screenshot makes a poor cover.

## Attaching media per platform

These mechanics assume a CDP-driven Chrome. Coordinates drift, so resolve elements through JS or `getBoundingClientRect()` each time. Screenshots can be a few percent larger than CSS pixels on retina displays, so never click straight from image coordinates.

### Stream a file into the page

The raw `DOM.setFileInputFiles` call is the cleanest path when an `input[type=file]` exists (see below). When it does not work, stream the file in:

1. Base64 the asset, split it into 50KB chunks, and append each chunk with a `js("window.__g += '<chunk>'")` call. The JS pipe breaks above about 60KB.
2. In the page, build the file: `atob`, then `Uint8Array`, then `new File`, then `DataTransfer`.
3. Hand it to the composer as described per platform.

### X

- Media, image or mp4: `DOM.getDocument(depth=-1, pierce=True)`, then `DOM.querySelector('input[data-testid="fileInput"]')`, then `DOM.setFileInputFiles(files=[path], nodeId=...)`. An 8MB 64s mp4 was ready in about 20s. Wait until the attachments strip stops showing upload progress.
- Fallback: a synthetic `DragEvent('drop')` (with dragenter and dragover first) on `[data-testid="tweetTextarea_0"]` works. Click the reply box first, wait about 2s, type the text, verify via innerText, then drop.
- Text entry: use CDP `Input.insertText`, not `document.execCommand('insertText')`. The draft editor silently mangles long multi-paragraph strings with execCommand. Focus the textarea via JS, call `Input.insertText`, then verify innerText (marker count, length range, URL present) before clicking Post.
- Self-reply chain: go to the parent status URL, focus `tweetTextarea_0`, insert text, verify, click `tweetButtonInline` by its rect, then find the new reply's status href by matching the first 40 characters of its text.
- Attach media to the thread root. Media plus a link in the same tweet suppresses the link card, which is fine: keep the canonical URL in the final reply, which then renders the card. Limits: mp4 2:20 or shorter, GIF 15MB, images 5MB. Screenshot-verify the media preview before clicking Post.
- Deleting your own tweet: the caret menu needs a real coordinate click, and it soft-rate-limits after several opens. Fallback is the web client's own delete GraphQL call from the page context with the session's csrf cookie. Look up the current query id in the web client's network log, because it changes.

### LinkedIn

- Feed Photo and Video buttons both open a native file chooser. Use the file-chooser intercept below.
- Comments: drop does not work, and the visible `input[type=file]` elements belong to the messaging widget (attaching there sends it to a chat draft). Correct flow: patch `HTMLInputElement.prototype.click` to capture the input instead of opening the picker, click the comment box's "Add a photo" button (capture lands about 1s later), then set `input.files = dt.files` and dispatch `change`. Restore the prototype afterwards.
- Video post: set a thumbnail before Next (image icon under the preview, then "Add video thumbnail"). Otherwise the feed shows a black first frame.
- Native video beats a link preview card for reach. The URL can stay in the body text. 30-90s is the sweet spot.
- The create composer text box is reachable through `.ql-editor, [contenteditable=true][role=textbox]` with `focus()` plus `Input.insertText`. Some composers are closed shadow roots, so click by coordinates and verify by screenshot.
- LinkedIn rewrites links to `lnkd.in` shorteners. Verify an edit by curling the shortener, not by matching the raw URL.

### Reddit

- The composer lives in shadow DOM: walk `el.shadowRoot` recursively. `input[type=file][accept*=image]` exists without clicking: assign `files` and dispatch `input` and `change` (bubbles and composed).
- The reopened composer restores old drafts. Clear it with real keys (click the editor, Select All, Backspace, verify innerText length 0) before typing, or new text interleaves with the stale draft.
- Read each subreddit's rules before posting. Image or video post types get more feed surface where allowed.

### Native file-chooser intercept

Cleanest path when a real picker opens: `cdp("Page.setInterceptFileChooserDialog", enabled=True)`, real-click the upload button, drain events, grab `Page.fileChooserOpened`'s `backendNodeId`, call `cdp("DOM.setFileInputFiles", files=[path], backendNodeId=bid)`, then disable the intercept. No base64 needed.

### Hacker News and IndieHackers

HN is link-only: the OG image on the blog page does the work, so verify `og:image` renders before submitting. IndieHackers allows images in the body: include `hero-card.png`.

### Facebook groups

Check the group's language and rules on its About page first, and confirm you are a member. Then:

1. Click "Write something..." and confirm the `div[role=dialog]` with a `div[role=textbox]` exists before typing. Closing the dialog preserves the draft.
2. Focus the textbox via JS and call `Input.insertText`.
3. The dialog already contains `input[type=file]`. Do not click Photo/video. Use `DOM.querySelector('div[role=dialog] input[type=file]')` plus `DOM.setFileInputFiles` with 2-4 images, and wait for blob `<img>` previews.
4. Click the `div[aria-label="Post"]` button. Posting shows a spinner for 15-25s in big groups.
5. Verify under the group's "my posted content" page. Large groups hold new posts as Pending (admin approval). Pending is success. Never repost while pending.

### X Articles (long-form)

- Route: sidebar "Articles", then Write (not a direct compose URL). Drafts autosave server-side, so a browser restart loses nothing.
- Title: `textarea[placeholder="Add a title"]`. `Input.insertText` doubles text here, so set it with the native value setter plus an `input` event.
- Body: the single `div[contenteditable=true]`. `Input.insertText` works and preserves paragraphs.
- Cover (5:2, 1500x600): `input[data-testid="fileInput"]`, then `DOM.setFileInputFiles`, then Apply in the crop dialog. Generate a banner with `scripts/terminal_banner.py` instead of using a raw app screenshot.
- Publish: Publish, then the audience dialog's Publish. The redirect to the article's status URL means it is live.

## Session discipline

- Never delete an engaged post. Edit in place (LinkedIn: control menu, Edit post, which exposes a real `.ql-editor`).
- If you use the same Chrome the agent drives, the agent can re-attach to your focused tab between calls. Before any click batch, list tabs, switch to the target by URL, and assert `location.href` inside the same call. Do whole flows in one script, and prefer JS or API actions over coordinate clicks while you are working in the browser.
- Close leftover agent tabs before starting. Gate any Post click behind a content-verify loop that refuses to fire on a mismatch.

## Post-shape rules that compound with media

1. Hook line above the media: one sentence, no link. The media stops the scroll, the first line earns the click.
2. One asset per post, root-only by default (see Thread media placement).
3. Match the asset to the claim. "Watch the agent work" gets the run clip. "One command" gets the terminal GIF.
4. Verify visually after posting. Screenshot each item and confirm the media rendered, because uploads fail silently during composer timeouts.
5. Reddit: verify with the JSON API. Moderator removal is invisible to the author: the post looks live while `removed_by_category` is `moderator`. Fetch `/r/<sub>/comments/<id>.json` and check `removed_by_category` and `is_robot_indexable`. A shadow-DOM file-input assign can also report success while attaching nothing, so check `media_metadata` on the live post JSON. If a subreddit removes your posts, move to a sibling community.
6. Keep your voice and content rules from your own publishing checklist: canonical URL everywhere, no marketing speak on Reddit, and hand off at auth walls.

## Definition of done

- [ ] Kit folder produced, or an explicit note why no media exists for this topic
- [ ] Every posted item has native media attached and visually verified
- [ ] X thread: the root has the strongest asset and the final tweet carries the link
- [ ] Handoff files (HN, IndieHackers) reference the OG image or include `hero-card.png`
