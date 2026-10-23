---
name: feature-doc
description: >
  Closed-loop feature documentation for your product. Give it a feature (issue
  numbers or an id) and it reads the source, drives your live app to capture real
  screenshots and a screen recording, writes a docs article (Docusaurus or any
  markdown docs site) with both how-to steps and use-case content, then verifies
  the article with a fresh-context read-only verifier before reporting. Use when
  you say "write the doc for <feature>", "document issue #123", or "/feature-doc".
---

# feature-doc: closed-loop feature documentation

Produces one evidence-backed feature article end to end. Capture needs no manual
gesture: a bundled recorder grabs frames from the browser through the DevTools
protocol. Publishing the docs PR stays a gate for you at CP-6.

## Configuration

Set these once (a `.env`, your `kit.toml`, or pass them as arguments). Nothing below is hardcoded.

| Setting | Meaning | Example |
|---|---|---|
| `APP_URL` | Start page of the live app to drive | `https://app.example.com/projects/1` |
| `ISSUE_REPO` | Issue tracker holding the feature issues | `your-org/your-product` |
| `DOCS_REPO` | Local path of the docs repo | `../your-docs` |
| `DOCS_DIR` | Folder inside the docs repo for the article | `docs/features/` |
| `EVIDENCE_DIR` | Where screenshots and video land | `./evidence/<feature>/` |

Keep the docs repo in a folder your tools can always read. Some operating systems block background reads of the Documents folder mid-session, which breaks the verifier.

## When to use
- A shipped or shipping feature has no article, or an outdated one.
- You want a doc that works as a user manual and as a guide to what you can do with the feature, with real screenshots and a video.

Skip it for backend features with no user surface (write a short "no doc required" record instead).

## Closed loop
```
CP-1 spec (issues/repo)  -> CP-2 plan (AC-n)  -> CP-3 build (capture + write)
   -> CP-3v component verify (task-verifier, read-only)  -> fix-agent (max 2)
   -> CP-5 post-condition  -> CP-6 ship gate (you review, then open the docs PR)
```
The writer never grades its own work. The verifier is a fresh-context, read-only subagent that gets paths and AC-n only, never the writer's narration. See the `closed-loop` skill for the checkpoint mechanics.

## Inputs
- Feature id plus seed issue numbers in `ISSUE_REPO`, or a spec path.
- A browser already logged in to the app, reachable by a browser automation tool (Playwright, CDP, or your browser harness). If the app redirects to a login page, stop and ask the user to sign in. Never type credentials.
- The docs repo at `DOCS_REPO`. One article per feature: a new feature gets a new article, a changed one updates the existing article.

## Pipeline

### 1. Enrich (CP-1)
Read each seed issue (`gh issue view <n> --repo $ISSUE_REPO --json title,body,state,labels,milestone`, or your tracker's CLI) and any matching spec files. Establish the concrete user surface, the ship status per issue (an OPEN issue is not a shipped surface, so do not claim it), and the exact flow to demo. Never invent UI. Where a detail is unknown, mark it `TODO` and flag it.

### 2. Plan (CP-2)
Map the article's sections to AC-n (see Post-conditions). Grep the docs repo for existing coverage to decide between a new article and an update.

### 3. Capture (CP-3)
Drive the live flow and save real evidence into `EVIDENCE_DIR`.

- **Screenshots** of each meaningful state, using your browser tool's screenshot call.
- **A real video** of the end-to-end flow with the bundled recorder (no gesture, no ffmpeg needed for the capture):
  ```bash
  SR_OUT=$EVIDENCE_DIR/<feature>-demo \
  SR_URL=$APP_URL \
  SR_FPS=8 \
  SR_STEPS='[{"at":0.5,"do":"click_testid","testid":"..."},{"at":2.0,"do":"click_text","text":"..."}]' \
  browser-harness < .claude/skills/feature-doc/tools/screenrec.py
  ```
  `screenrec.py` runs inside a CDP-based Python harness that exposes the page (`browser-harness` is one such tool; adapt the launcher to Playwright or your own). It writes frames, `<out>.manifest.json` (fps, viewport, per-action events with cursor coordinates and captions) and a quick `<out>.raw.mp4` preview. Step actions are `click_xy|click_testid|click_text|type|key|scroll`, each with `at` (seconds) and an optional `caption`.

  The deliverable is a clean, complete recording of the real workflow: set up, configure, use, get the result. Finish it with `tools/recompose.py`, which places the real viewport in a simple browser window on a gradient background and speeds up long waits instead of cutting them. No captions, no intro or outro cards, no synthetic cursor.
  ```bash
  RC_MANIFEST=<base>.manifest.json RC_OUT=<feature>-walkthrough.mp4 \
  RC_SEGMENTS='[[0,9,1],[9,58,8],[58,70,1]]'  # [from_s,to_s,speed]; ramp the waits \
  RC_ADDR="app.example.com" python3 .claude/skills/feature-doc/tools/recompose.py
  ```
  `recompose.py` needs ffmpeg and Pillow. Embed the result with a plain video tag:
  `<video controls preload="metadata" style="width:100%;border-radius:8px;"><source src="..." type="video/mp4" /></video>`.
  - Length follows the task: long enough to teach setup and usage.
  - The usage payoff must work on camera. If the payoff step is broken, do not record a stub. Use screenshots for the working part and hold the video until the full flow works.
  - A clip of a few seconds is worse than a screenshot. Use a screenshot instead.
  - `tools/videokit.py` makes a branded, captioned teaser with intro and outro cards. Use it only for marketing teasers, never for walkthroughs.
- **Optional polish:** an interactive demo (Arcade or similar). Browsers require a trusted user gesture to start such recorders, so `tools/arcade-record.py` drives the flow while you press the start and stop shortcut yourself.
- **Look at every capture.** Open the images and the video, name any UI discrepancy, fix the flow, and re-capture. Never pass on "the element exists".
- If a flow is gated (a broken backend path, an unshipped surface), capture what works, file the blocker in your tracker, and mark the rest pending. Do not fake a working demo.
- Mask any customer data or personal data visible in a capture before it leaves your machine.

### 4. Write (CP-3)
Write the article as markdown (MDX-safe when the docs site is Docusaurus) with both layers:
- **How-to:** overview, why it matters, step-by-step usage.
- **Use-case layer:** at least 3 use cases with sample workflows (each a concrete prompt or step list plus the expected result), prompting techniques where the feature takes input, best practices, limitations.
- Embed the captured media (`![alt](path)` for images, a video tag for the recording). Cross-link to related articles.
- Run the draft through the `no-ai-slop` skill before verification.

### 5. Verify (CP-3v then CP-5)
Spawn a `task-verifier` with only the article path, the evidence directory and the AC-n list. It re-opens the files and media itself and returns one row per AC:
`EVIDENCE AC-n | CP-3v | PASS|FAIL | <one line + path/observation>`.
On `FAIL:fixable`, spawn `fix-agent` (max 2 attempts) with just the failed AC-n, then re-verify. After 2 attempts, escalate with the evidence.

### 6. Report and ship gate (CP-6)
Summarize the article path, the media (with accessible URLs once uploaded), the AC-n PASS table, and open TODOs or gated items. Opening the docs PR waits for the user.

## Post-conditions
- **AC-1** The article exists at the planned path under `DOCS_DIR` with valid frontmatter for your docs site.
- **AC-2** It contains how-to steps and the use-case layer (at least 3 use cases, prompting where relevant, best practices).
- **AC-3** Every UI or behavior claim is grounded in a captured screenshot or an issue body. Unknowns are `TODO`, not invented. Surfaces from OPEN issues are marked gated, not shipped.
- **AC-4** Either (a) a clean, complete walkthrough recording exists (real setup, usage and result, no decoration, valid mp4 by `ffprobe`) and the article embeds it, or (b) screenshots cover the working parts and the article notes the video is pending. A short decorated clip does not satisfy this.
- **AC-5** Evidence that ships is accessible (uploaded to the PR or issue, not a local path).
- **AC-6** A limitations section states any gated, blocked or unshipped parts.

## Rules
- No fabrication. Follow your house writing rules (no em dashes, TL;DR first, scannable).
- Visual verification is mandatory for UI docs: read the pixels, fix what is wrong, re-capture.
- Use relative paths or config values in all output, never machine-specific absolute paths.

## Escape hatches
- **Auth wall:** stop and ask the user to sign in. Never enter credentials.
- **CDP will not connect:** point your harness at the browser's remote-debugging URL (for example `http://localhost:9222`) and reload it. If the browser prompts for permission, the user clicks Allow.
- **Flow gated by a bug:** file it, capture the working portion, mark the rest pending.
- **ffmpeg absent:** the recorder falls back to a GIF preview. Install ffmpeg for the mp4.

## Tools
- `tools/screenrec.py`: flow recorder (CDP frame-grab loop to frames, manifest and raw preview).
- `tools/recompose.py`: walkthrough finisher. Manifest to a clean 1920x1080 h264 mp4 with a browser window, gradient and speed ramps. Options: `RC_FIT=1` fits a phone or tall capture, `RC_CROP=x0,y0,x1,y1` crops the source, `RC_NOBAR=1` drops the browser bar, `RC_SPEED_BADGE=1` labels sped-up segments, `RC_REDACT` pixelates boxes such as a person's name.
- `tools/videokit.py`: branded teaser cut with captions and cards (teaser only).
- `tools/arcade-record.py`: hybrid interactive-demo recorder. Set `APP_URL` and add flows to its `FLOWS` table.
