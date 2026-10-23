# Semantic zoom: detail that changes with zoom level

Based on Arc UI's "Semantic zoom" block (uiarc.dev/components/blocks/semantic-zoom). Take the interaction model only; the code and the look stay the original's. Use it for roadmaps and other hierarchical overviews.

## The idea in three sentences

A map of nested boxes shows the whole organisation at once. Zooming into a box swaps in a richer representation of the same thing at each level. The summary numbers, the breadcrumb and the minimap all follow the camera, so the reader always knows where they are and what the numbers cover.

## When to use it

- Hierarchical work data where each level answers a different question: portfolio, then team or milestone, then project or bucket, then task.
- Management overviews where people move from "how is the whole plan doing" to "what exactly is this ticket" without losing their place.
- Skip it for plain scanning of a tree (use a tree view) and for working on tasks (use a board or table).

## Levels: each one shows something new

Observed hierarchy in the reference (company, team, project, task). What each level renders:

| Level | Box shows |
|---|---|
| Whole company | One block per team with name and % done. Inside each, tiny project cards with a strip of task tiles; blocked tasks tinted red; people as dots. No text beyond team name and %. |
| Team | Team name, lead avatar and name, "6 projects · 24 open tasks", % done. Project cards now readable. |
| Project | Project name, health dot and word ("At risk", "On track", "Off track") with due date, % and a progress bar, task tiles, owner avatars with names. |
| Task | A full card: status · due date · estimate, title, one-paragraph description, assignee with role, checklist "5 of 5" with a bar, comment count, and its parent path. |

Rules drawn from it:

- **Swap the representation per level and keep text at reading size.** A tiny box shows a colour and a number. A medium box shows a title and counts. A large box shows sentences.
- **Detail fades in once the box is big enough on screen.** Measure the rendered pixel size of each box after every camera move.
- **Rollups come from the leaves.** Team % and blocked counts derive from tasks, so every level agrees.
- **Health shows as a word plus a dot**, so it reads without colour.

## Context that follows the camera

- **Breadcrumb** at the top: `Company > Team > Project > Task`, each crumb clickable, current one marked `aria-current="location"`.
- **Stats panel re-scopes to the focus.** Same fields at every level, labelled with the level: Team / Project / Task, Open tasks, Blocked (red when above zero), Next due, Progress %, People. Numbers count to the new value.
- **Minimap** in a corner once zoomed in: the whole map in miniature with a rectangle for the viewport.
- **Zoom readout and controls**: `−`, current factor (1.0×, 1.6×, 4.0×), `+`, fit. Hint text: "Scroll to zoom, drag to pan, click anything to fly in".
- **Hover card** on any item with its key fields and "Click to open".
- **Guided tour** button that flies through the levels once; skippable.

## Input

| Input | Action |
|---|---|
| Click or tap an item | Fly into it |
| Wheel, pinch | Zoom around the pointer |
| Drag | Pan |
| Arrow keys | Move a cursor between nearby items |
| Enter / Space | Fly into the item under the cursor |
| Escape / Backspace | Fly out one level |
| + / − | Zoom in or out |
| 0 / Home | Fit the whole map |

## Accessibility and motion

- The stage is `role="application"` with an `aria-roledescription` of zoomable map and a text label summarising the whole.
- A polite live region announces each move: "Now viewing SSO for enterprise, on track, 63% complete, 4 open tasks, due Oct 22."
- A plain table of every leaf-parent (team, project, health, progress, open, blocked, due) sits in the DOM as the non-visual equivalent.
- Camera moves are eased flights of about 400 to 600 ms; under `prefers-reduced-motion` they jump instantly.
- Pause the render loop offscreen and in hidden tabs. Gotcha for agents: a background CDP tab never paints such a canvas, so screenshot it in a visible browser pane.

## Applying it without a canvas engine

For up to a few hundred items, a DOM version is enough: lay the boxes out once in a fixed "world" grid, move a camera with a CSS `transform: translate() scale()` on the world, and after each move compute every box's on-screen size to set a detail class (`lod-0` dot, `lod-1` label, `lod-2` card, `lod-3` full). Clicking a box fits it to the viewport. Keep the timeline or table view next to the map: the map gives orientation, the table supports scanning.

## Zoom inside an existing timeline

A separate box-map view (a "Zoom map" tab with cards per level) can read as ugly and redundant. A safer form puts the zoom interaction inside the timeline or table people already use:

- Clicking a milestone header widens that column to about 70% of the time axis; the other milestones stay visible as narrow columns with clamped names.
- A short horizontal camera move (scaleX from the old column to the new, about 380 ms, off under reduced motion) sells the zoom.
- Bar content is chosen by the bar's pixel width: under 90 px a number or blocked count, then status, then status, owner and criteria meter, then the first line of "What".
- Plan level shows buckets collapsed to per-milestone counts; zoomed level expands them, and bucket summaries gain "% done, n blocked" plus status tiles.
- A breadcrumb row (Whole plan › milestone) with Previous, Next, Zoom out; Esc zooms out, ← → move between milestones. Ticket detail opens in a side drawer.
