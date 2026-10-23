---
name: blog-publish
description: >
  Write and publish a post to your own static blog end to end: content checklist
  (embedded links, optional TL;DR), per-post ASCII art, an agent-readable markdown
  twin, deploy, and social distribution. Use when you say "write a blog post",
  "publish this to my blog", or "push this post to socials".
---

# blog-publish: static blog post pipeline

## Configuration

Set these once (`kit.toml`, `.env` or arguments).

| Setting | Meaning | Example |
|---|---|---|
| `BLOG_DIR` | Repo folder of your static blog | `./my-blog/` |
| `POSTS_DIR` | Markdown posts, relative to `BLOG_DIR` | `content/posts/` |
| `BUILD_CMD` | Command that builds the site | `python3 build.py` |
| `SITE_DIR` | Build output folder | `site/` |
| `BLOG_URL` | Public base URL | `https://blog.example.com` |
| `POST_PATH` | URL pattern for a post | `/blog/<slug>/` |
| `DEPLOY_CMD` | Your deploy command | see Deploy |
| `SOCIAL_HANDLES` | Accounts used for distribution | per platform |

The steps below assume a build script that renders `POSTS_DIR/<slug>.md` into `SITE_DIR`. Adjust names to your generator (Hugo, Eleventy, Astro, a custom script).

## Content checklist (every post)

1. **Front matter** with `title, subtitle, slug, date, description, tags, author, published`. Match existing posts. If the subtitle renders under the H1, keep it to one sentence stating what the post is about.
2. **TL;DR is optional.** Narrative, build and essay posts open problem-first with no summary box (see Narrative arc). Reserve a TL;DR for reference-style or scannable how-to posts, and then use a one or two sentence hook plus bullets, never one long paragraph.
3. **Embedded links for every reference.** Each tool, repo, prior post or source gets an inline link on first mention. Link your own posts with root-relative paths (`/blog/<slug>/`).
4. **Figures in most major sections.** Use diagrams, charts and product screenshots where they carry evidence. The `editorial-illustrations` skill generates meaning-carrying figures. Keep ASCII for header art (see below).
5. **No em dashes.** Use colons, commas or parentheses.
6. **Voice.** First person, concrete numbers and stories, no AI-slop vocabulary.
7. **Literal example prompts.** When a post walks through an AI tool, quote the actual prompt in a blockquote or fenced block instead of paraphrasing it.
8. **Final anti-slop pass (required).** Before deploy, run the draft through the `no-ai-slop` skill and self-check against its eval. Keep a contrast or colon setup only when it is a real reframe. Preserve your voice and make the smallest effective edit.

## Narrative arc (default for substantial posts)

Document what happened instead of writing a prescriptive summary:

1. **Open on the problem.** A confession, a bug, a bold claim or an observed pattern. Make the reader feel why the status quo breaks before any solution appears. A single diagram as an early anchor is fine.
2. **Narrate the process, including dead ends.** Show the first version, what broke, what you learned and what you changed. Bugs become features. Admit scope creep and reversed decisions.
3. **Cite prior art warmly and inline.** Link by author and work at the natural reading point. Treat references as conceptual anchors, not footnotes.
4. **Prove it with evidence.** Counts, costs, before/after deltas, traces, real artifacts, screenshots, all from the actual run. If the argument is theoretical, say so.
5. **Close reflectively.** End with a quiet claim, an open question or a few diagnostic questions the reader can apply. No call to action, no summary box.

Voice: first person, conversational but technically dense, understated. Short declaratives mixed with longer explanations. Headings are short and descriptive. Length follows the material.

## Per-post ASCII art

Each post gets an entry in an ASCII-frames table in your build script, keyed by slug: a list of 2 to 5 frames that loop (a cursor typing, a rocket lifting, a gear turning). Pad frames to a common size automatically so they need no hand alignment. Use pure ASCII, no Unicode box drawing.

Render it two ways from the one source:
- On the page, a `<pre class="post-ascii" data-frames="...">` element cycles frames with a small inline script (about 420 ms per frame) and shows a static first frame under `prefers-reduced-motion`.
- In the social card, an animated GIF (1200x630) where only the ASCII region changes per frame. Some chat apps animate it, others show the first frame. Set `og:image:type` to `image/gif`.

A playful frame set beats a corporate one. Never ship the generic fallback; add bespoke frames.

## Agent-readable output (automatic, but verify)

Have the build generate a clean markdown twin at `/blog/<slug>/index.md` and list every post in `/llms.txt`. After building, confirm both include the new post:

```bash
grep -i "<title fragment>" $SITE_DIR/llms.txt && head -5 "$SITE_DIR/blog/<slug>/index.md"
```

## Build and deploy

```bash
cd $BLOG_DIR && $BUILD_CMD
```

Deploy with your own command (`DEPLOY_CMD`). Examples, pick the one that matches your host:
- Railway: `railway up --detach`
- Netlify: `netlify deploy --prod --dir=$SITE_DIR`
- Vercel: `vercel deploy --prod`
- Cloudflare Pages: `wrangler pages deploy $SITE_DIR`
- GitHub Pages or any git-push host: commit `SITE_DIR` or push the source and let CI build.

Post-condition: fetch the live page and confirm the new post is there before reporting success:
`curl -s $BLOG_URL/blog/<slug>/ | grep '<title>'`. Builds can take a few minutes.

## Social distribution (after the post is live)

Voice follows your `publish-social` command if you have one. The `social-media-kit` skill covers asset recipes and upload mechanics, and `youtube-video-kit` covers video.

**Media is mandatory on every platform post.** Build the asset kit (teaser video cut, padded-card hero image, terminal GIF) and attach per platform before posting. On X, the thread root gets the strongest asset, and the canonical URL moves to the final reply so the link card still renders.

**Durable articles beat feed posts.** For substantive posts, publish an article on the platform (X Articles, LinkedIn "Write article") with the full body and the canonical blog link as the source. A short thread or feed post is fine as a pointer to it.

- **X:** prefer the Articles composer. For a thread, post tweet 1 and build the rest as self-replies (open each new tweet's detail page, use the reply box). The composer's multi-tweet flow can silently lose drafts. Two traps: typing an `@mention` opens an autocomplete that can swallow the submit click (press Escape first), and a link preview card can push the Reply button below the fold (scroll it into view before clicking). Screenshot every step and re-check the profile to confirm the final tweet posted.
- **LinkedIn:** prefer "Write article". For a feed post, type the full content with real paragraph breaks, wait for the link preview, then post, and confirm the success toast. Mentions only become links when picked from the autocomplete dropdown.
- **Reddit:** one genuine post in a relevant subreddit, not a mass crosspost. Check whether the subreddit requires flair before submitting.
- **Hacker News and IndieHackers:** if there is no logged-in session, stop at the auth wall, never type credentials, and hand the prepared title and URL to the user to submit.

Include the canonical URL in every platform's content and screenshot each post after submitting to verify it.

### X field notes
- Use a browser tool that can attach files to X's file input. Some embedded browser panes cannot, because the platform blocks fetching local images and clipboard paste does nothing.
- The compose route opens a modal over the home feed and a file-input lookup may return the inline composer's input. Close the empty modal and use the inline composer.
- Type the whole post in one call. Pressing Escape to close the mention menu can move the cursor and scramble the text.
- A banner can appear after typing and push the Post button down. Re-screenshot before clicking Post, and confirm the "Your post was sent" toast.
- Count length with URLs as 23 characters and stay at or under 280.
