---
name: product-ui-taste
description: Anti-slop skill for PRODUCT UI - dashboards, data tables, forms, multi-step flows, settings, list/detail, app shells. The agent reads the surface, budgets the frame first, and ships dense interfaces that are correct at every edge case (overflow, long labels, empty/error/loading states, i18n expansion, keyboard/a11y). House-system-first; maps to Carbon/Polaris/Atlaskit/Fluent/Primer/Material3/Radix-shadcn/Ant. The counterpart to taste-skill, which owns landing/portfolio/marketing.
---

# product-ui-taste: Anti-Slop Skill for Dense Product Surfaces

> Dashboards, data tables, forms, wizards, settings, list/detail, admin consoles, app shells. NOT landing pages, portfolios, or marketing (that is `taste-skill`). NOT charts (that is `dataviz`). NOT native mobile.
> Every rule is **contextual and mechanical**. It fires from the surface you are building, not automatically. Read the surface, budget the frame, then pull only what fits.
> **Companion contract:** `taste-skill` explicitly hands off "dashboards / dense product UI / data tables / multi-step forms" to "the right tool." This skill is that tool. If a brief is half marketing and half product (a landing page with an embedded live dashboard), use `taste-skill` for the hero/marketing sections and this skill for the product surface. Never run both on the same component.

---

## 0. PRODUCT READ (Read the Surface Before Anything Else)

Marketing UI lives on first impression. Product UI lives on the **hundredth** use, under real data, by someone doing a job. The slop failure mode is different: not "templated aesthetic," but **prototype that dies on contact with real data** - a table that scrolls the whole page sideways, a button that truncates its own label, a single grey "no data" box reused for three different situations, a form that clears itself when the user fat-fingers one field.

### 0.A Read these signals first
1. **Surface type** - the single most important read. One of: **index/table** (list of records to scan, filter, select), **detail/record** (one entity, its fields and related data), **dashboard/overview** (KPIs + widgets + a table or two), **form/settings** (input and configuration), **multi-step flow/wizard** (a sequential task), **console/observability** (logs, metrics, deploys), **feed/messaging** (stream of items). Most real screens are a composition of two or three (index + detail drawer; dashboard + drill-in table).
2. **Data shape and volume** - how many rows at p95, how wide is a row, are cells uniform or ragged, is the data live/streaming or static, can a field be empty/null/very-long.
3. **Density need** - a trader's cockpit and a consumer settings page are both "product UI" and want opposite densities. Read: expert-daily-driver (compact, keyboard-first) vs. occasional-consumer (comfortable, forgiving).
4. **Consequence level** - is the primary action informational (view), reversible (rename, move), or destructive/irreversible (delete, deploy, charge a card). This drives confirmation, focus defaults, and autosave eligibility.
5. **Who is the user and what are they permitted to do** - roles, read-only viewers, plan/license tiers. Product UI has states marketing UI never has: permission-denied, read-only, plan-locked (Section 6.G). Read this now, not after building the happy path.
6. **Existing system** - is there already a Carbon/Fluent/Polaris/Atlaskit app, or a house token set? Product UI is almost never greenfield. Match the host system before importing taste.

### 0.B Output a one-line "Product Read" before generating
Before any code, state: **"Reading this as: a \<surface type> for \<user> at \<density>, \<data volume>, consequence \<level>, built on \<design system | house tokens | none>."**

Examples:
- *"Reading this as: an index+detail-drawer for internal ops at compact density, ~2k rows (virtualize), consequence reversible, built on the house system (Table + side-panel inspector)."*
- *"Reading this as: a settings/form surface for end customers at comfortable density, low volume, consequence mixed (billing = destructive), built on the house system's form layout."*

### 0.C The anti-default that matters most: rows, not cards
The single fastest way to make a product screen look like an AI prototype is to **wrap every record in a Card with a Badge**. Dense data that the user scans, filters, sorts, or selects belongs in **rows** (Table for columnar, List/Item for single-line), edge-to-edge, with dividers and 32-40px row height. Card is a **widget container** (KPI tile, chart panel, settings group, gallery entry), never a list-item wrapper. [Material3 lists; Carbon] If your first instinct on a list of records is a Card grid, stop and re-read this line.

### 0.D If the brief is ambiguous, ask ONE question, then proceed
The one question worth asking is almost always about **data volume or consequence** (they change the architecture): "roughly how many rows at the high end?" or "is this action reversible?" Everything else, infer from the Product Read and state your assumption. Do not interview.

### 0.E Anti-default discipline
The model's defaults for product UI are: Card-soup, fixed-width `<table>` that overflows the page, `disabled` submit button as the only validation, one generic empty state, `z-index: 9999`, and a full-page spinner on every load. Each has a specific correct replacement below. When you catch yourself reaching for one, that is the signal to open the matching section.

---

## 1. THE THREE DIALS (Core Configuration)

After the Product Read, set three dials. Unlike taste-skill (VARIANCE / MOTION / DENSITY tuned for expressive marketing), product dials are tuned for **information work**. Motion is deliberately near-absent in product UI; it is feedback, not decoration.

* **`DENSITY: 2`** - 1 = comfortable/consumer, 2 = standard, 3 = compact/cockpit. Drives row height, padding scale, font size, and whether you offer a density switcher.
* **`DATA_COMPLEXITY: 2`** - 1 = simple list (plain Table/List), 2 = sortable+filterable+selectable table, 3 = enterprise grid (frozen columns, virtualization, column management, live data).
* **`CONSEQUENCE: 2`** - 1 = informational/read, 2 = reversible mutations, 3 = destructive/irreversible/financial. Drives confirmation defaults, autosave eligibility, error tone, and how loud "unsaved changes" gets.

**Baseline: `2 / 2 / 2`** (a standard SaaS product table with a detail view). Override from the Product Read.

### 1.A Dial inference
| Signal | DENSITY | DATA_COMPLEXITY | CONSEQUENCE |
|---|---|---|---|
| "internal admin / ops tool / expert daily driver" | 3 | 2-3 | 2 |
| "enterprise data console / grid / analytics" | 3 | 3 | 2 |
| "consumer settings / account / onboarding" | 1 | 1 | 1-2 |
| "SaaS product dashboard (default)" | 2 | 2 | 2 |
| "billing / delete / deploy / permissions surface" | match | match | 3 |
| "observability / logs / live metrics" | 3 | 3 | 1 |

### 1.B Use-case presets
| Preset | DENSITY | DATA_COMPLEXITY | CONSEQUENCE | Frame |
|---|---|---|---|---|
| Internal admin tool | 3 | 2 | 2 | AppShell + SideNav, inspector on select |
| SaaS product dashboard | 2 | 2 | 2 | AppShell + SideNav or TopNav + TabList |
| Enterprise data console | 3 | 3 | 2 | AppShell + SideNav, full-height grid |
| Consumer settings/account | 1 | 1 | 1-2 | AppShell + settings template (nav + form panels) |
| Multi-step wizard | 1 | 1 | 2-3 | Centered column, stepper, no distracting chrome |

### 1.C How the dials drive output
Use these exact names as global variables in reasoning. `DENSITY` gates row height and the density-switcher decision (Section 10.A). `DATA_COMPLEXITY` gates how far down the table deep-dive (Section 7) you go. `CONSEQUENCE` gates Sections 6.G, 8.E, 8.F, 9.A. Do not invent aliases.

---

## 2. PRODUCT ARCHETYPE → DESIGN SYSTEM MAP

Product UI is almost never hand-rolled CSS. Pick the foundation from the host app first, the archetype second. **One system per app.** Do not mix Carbon with Fluent, or drop shadcn into a Polaris tree.

### 2.A House system first (discover, do not guess)
If the app already has a design system, that system wins, and your first job is to **find out what it actually ships** rather than assuming. Most mature systems already solve the dense-surface problems this skill is about, so you rarely drop to raw CSS. Guessing at component names and props is the single most common way an agent produces code that looks right and does not compile.

Before writing UI, resolve each of these against the host system's real API (its CLI, its docs site, or its `.d.ts` files):

| Need | What to look for | How to resolve it |
|---|---|---|
| Full-page shell | An app-shell primitive plus its nav slots | System docs "layout" or "app shell" page |
| Multi-pane tool / inspector | A layout + side-panel pair, not two floated divs | Docs "layout" page; check whether the panel is resizable |
| Columnar data | The system's Table and its sort/select/pagination plugins | Component reference, not a blog example |
| Sticky / frozen columns | A dedicated hook or plugin (most systems ship one) | Search the docs for "sticky" or "frozen" before hand-rolling |
| Resizable columns | A column-resize hook | Same |
| Pagination footer | Table pagination + page-size control | Component reference |
| Search + filter toolbar | A toolbar/filter component distinct from plain search | Component reference |
| Single-line records | A List / Item pair | Component reference |
| Empty region | An EmptyState component | Component reference |
| Status / metadata | A status indicator distinct from Badge | Token/status docs |

**Workflow, always:** find the closest page or block template the system already ships, study its layout skeleton, then read the real props for every component you use. **Never invent props.** Prefer the system's own layout components over raw `<div>`s so spacing stays on the system's scale. Use design tokens for every value (`var(--color-*)`, spacing tokens), never raw hex or px. Reserve Badge for counts and enumerated states; status belongs on a status indicator.

**The house-system bridge (resolve the tension):** the CSS mechanics in Sections 5-10 (scroll ownership, `position:sticky` headers, frozen-column offsets, z-index tiers, `min-width:0`) are the **contract a mature system's hooks already satisfy** under the hood. Inside such a system, reach for the hook or plugin first, because a real sticky-column hook gives you the offset, the solid background, and the shadow divider correctly. Drop to the raw CSS contract only (a) to verify the system did it right when something bleeds through, or (b) when you are outside a design system entirely. Never hand-roll a sticky column with inline styles inside a system Table when the hook exists.

### 2.B External systems (match the host, or pick by archetype)
| Archetype / brief | Reach for | Why |
|---|---|---|
| IBM-style enterprise analytics, dense grids | `@carbon/react` + `@carbon/styles` | Most mature data-density + 2x-grid + empty/loading patterns [carbon] |
| Microsoft / enterprise SaaS, DataGrid | `@fluentui/react-components` (v9) | Official Fluent 2, Overflow primitives, tokens [fluent] |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Semantic spacing tokens chosen by meaning [atlaskit] |
| Merchant/admin, resource lists | Polaris (`@shopify/polaris` or web components) | IndexTable, four-states philosophy, error content [polaris] |
| GitHub-style devtool chrome | `@primer/react` / `@primer/css` | PageLayout landmarks, Blankslate, Truncate [primer] |
| Adaptive/canonical layouts, consumer-ish | `@material/web` + Material 3 tokens | Window-size classes, list-detail/supporting-pane [material3] |
| Own-the-code lean internal tool | Radix Primitives + shadcn/ui + TanStack Table | Headless a11y primitives, you own styling [radix, tanstack] |
| Enterprise React data-dense fast | Ant Design or Mantine + Mantine React Table | Batteries-included Table/Form [ant, mantine] |
| Lean keyboard-first (Linear/Vercel vibe) | Radix/shadcn + custom tokens | Density + command palette + restraint [linear, vercel] |

**Honesty rule:** if the app is one of these, use the official package and its Table/Form/Dialog. Do not recreate Carbon's data table in raw CSS. Do not import a system's tokens then override 90% of them.

---

## 3. FRAME-FIRST APP-SHELL ARCHITECTURE

**Budget the frame in pixels before writing one line of content.** Real applications are built top-down: pick the shell, name its regions, give each an explicit px budget, decide its container policy and responsive behavior, then fill. Content-first layout (write sections, wrap each in a Card) produces a padded scroll column that reads as a prototype. [most systems' layout docs]

### 3.A Pick the shell
- **AppShell** (header and/or side nav) - the default full-page product frame.
- **Layout + LayoutContent + LayoutPanel** - multi-pane tools: explorers, consoles, master-detail with an inspector.
- **Plain content column** - a single form, a settings section, a wizard.

### 3.B Region px budgets (memorize these)
| Region | Budget |
|---|---|
| Side nav | 240-280px |
| Icon rail (collapsed nav) | 64-72px |
| Detail / inspector panel | 340-420px (resizable 320-480) |
| Filter / facet rail | 220-260px |
| Row height | 32px compact / 40px standard / 48px comfortable [dense systems budget 32-40; Carbon ships 5 relative tiers, no fixed px] |
| Header / top nav | 48-64px (common app-bar convention) |

### 3.C Landmark regions (do not conflate them)
Name every region with a real landmark and know the difference [primer PageLayout]:
- **Header** - full width, top, app chrome.
- **Content** - the primary region, flexes to fill.
- **Pane** - a secondary region **beside** Content, content-height only. Use for an inspector or supporting info.
- **Sidebar** - **full-height** navigation, distinct from Pane. Never build a "sidebar" that is really a content-height pane, or a "pane" that is really full-height nav.
- **Footer** - full width, bottom (status bar, pagination context).

### 3.D Canonical layouts (recognize and scaffold) [material3]
- **List-detail** - list on the left, selected record on the right. Below ~1024px, detail overlays or becomes a separate route.
- **Supporting-pane** - primary content ~2/3, supporting pane ~1/3.
- **Feed** - a single scrolling stream (rows/bubbles, no cards in the stream).
- **Master-detail with inspector** (the tool backbone) - selecting a row opens a **fixed-width LayoutPanel inspector**, it does not navigate away. Add `resizable`. Overlay it below ~1024px instead of compressing Content.

### 3.E App-shell chrome that marketing UI never has
- **Workspace / org switcher** - almost every SaaS shell needs one, anchored top of the side nav or header-left, showing the current tenant's name/avatar. On click, a dropdown (not a modal) lists workspaces with a search field once there are 8+, a "recent workspaces" group, and a "create/join" action at the bottom. It switches context (data scope), it is not a nav destination. Keep it one element; never scatter tenant choice into the nav list. Persist the last-active workspace per user.
- **Global command palette** (Cmd/Ctrl-K) - for DATA_COMPLEXITY >= 2 keyboard-first tools, this is the fastest navigation. Recognize it as a first-class shell affordance, not a nice-to-have.
- **Background-job / async status tray** - when the app kicks off concurrent long-running operations (imports, exports, deploys), a persistent notification tray (a header icon with a count badge opening a dropdown of jobs) beats a modal per job. Each job row shows a determinate progress bar, a cancel affordance, and terminal success/error with a result link. Carbon's rule: for waits over a few minutes, let the user leave and notify on completion. Never block the whole UI on one background job. [carbon loading]

### 3.F Container policy per region (Cards vs Rows, decided per archetype)
| Archetype | Container policy |
|---|---|
| Tracker / work tool (issues, tickets, CRM) | Rows only. Grouped edge-to-edge lists, zero cards. |
| Console / observability | Card grid for dashboard widgets; Table for everything else. |
| Messaging / feed | Rows and bubbles. No cards in the stream. |
| Media / gallery | Card grid (ClickableCard) + dense metadata rows in detail. |
| Settings / forms | FormLayout sections; Card only to group dangerous/billing actions. |

Banned: a Card per list item (card soup), stacked full-width Cards as page structure, nested Cards, Badge as decoration.

---

## 4. LAYOUT HARD RULES (Failing any of these ships broken work)

* **SCROLL OWNERSHIP (the #1 product-UI layout bug).** Exactly **one** wrapper owns each scroll axis (`overflow:auto`). The page `<body>` must **never** scroll horizontally. A wide table scrolls inside its own container, not by pushing the whole app sideways. Sticky headers use `position:sticky` scoped to that scroll wrapper, **never** `position:fixed` to the viewport. [carbon, ant table-scroll, tanstack] If two nested elements both scroll the same axis, you have a bug.
* **Every sticky element needs a bounded-height ancestor.** `position:sticky` silently does nothing if no ancestor establishes a scroll boundary. A sticky table header requires the table's scroll container to have a real max-height. [css mechanics]
* **min-width:0 on flex children that hold text.** A flex/grid child defaults to `min-width:auto`, which refuses to shrink below content size, so `text-overflow:ellipsis` silently no-ops and the child pushes the layout wider instead. Any truncating text inside a flex row needs `min-width:0` on the text-holding child. This is the most common reason "my ellipsis isn't working." [overflow-truncation]
* **Responsive contract declared up front, per region.** Before filling, write which regions collapse, overlay, or drop at which breakpoints. No "Tailwind will handle it" assumptions. Nav collapses to an icon rail or off-canvas MobileNav; the inspector overlays below ~1024px; a wide table keeps horizontal scroll rather than reflowing columns.
* **Breakpoints: use size classes, not device names.** Compact / medium / expanded (Material 3) or Carbon's exact 2x-grid breakpoints (320 / 672 / 1056 / 1312 / 1584, 8px mini-unit, 16px padding, 32px gutter) as a fallback grid. [material3, carbon 2x-grid]
* **Container queries for reusable components.** A card or panel that appears in a wide Content region and a narrow Pane must respond to **its own** width, not the viewport. Use `container-type` + `@container`, not viewport media queries, for anything that renders in more than one region width. [joshwcomeau, responsive-layout]
* **Sidebar collapse = off-canvas or icon-rail, not in-place shrink.** Collapsing a 260px nav to 180px just cramps it. Collapse to a 64-72px icon rail (with tooltips) or slide it off-canvas with a persistent reopen strip. Persist which panes were shown across a resize/fold so the user does not lose context.
* **Density is a layout MODE, not a CSS zoom.** Offer at least the density presets the DENSITY dial calls for as a real switch (row height + padding token swap), not a browser-zoom hack. [i18n-a11y-density, carbon 5 row heights]
* **Never hardcode a fixed width on a text container.** Badges, buttons, table headers, chips, tags must be auto-layout (flex/grid, hug-contents) so text can reflow or expand. A fixed-width text container clips under real data and under translation (Section 10.B).
* **Tabular numbers for compared numbers.** Any column or list of numbers the user compares vertically uses `font-variant-numeric: tabular-nums` so digits align. Proportional digits in a metrics column is a Tell.

---

## 5. OVERFLOW & TRUNCATION CATALOG (Deep-Dive)

Product UI is where real strings arrive: a 90-character file path, a German button label, a customer name that is one word or forty. Truncation is a scalpel, not a default.

### 5.A The never-truncate list (mandatory)
**Never truncate primary/identifying content**: titles, entity names, unique IDs, error and validation messages, page headers, button labels. Truncation is for **secondary/supplementary** content only (descriptions, secondary metadata, breadcrumb middles). [carbon overflow, primer truncate] If an identifying string is too long, wrap it, give it more space, or use middle-truncation that preserves both ends (for paths/IDs) - never a trailing ellipsis that hides the part that distinguishes two records.

### 5.B Every truncated string needs a real full-text fallback
A hover-only `title` tooltip is **not** an accessible fallback: it fails keyboard-only users, touch users, and speech-recognition users. Provide the full text on focus as well as hover, or expandable inline, or in the detail view. [carbon, primer]

### 5.C Long button labels (mandatory, a signature product-UI Tell)
**Never truncate a button label.** Size the button to its content ("hug contents") with a `min-width` floor for tap-target accessibility. If the label is long (or translated), wrap to at most 2 lines before you ever truncate, and re-evaluate the label copy. A button reading "Save chang..." is broken work. Icon-only buttons need an `aria-label` and a tooltip. [overflow-truncation, i18n]

### 5.D Single-line ellipsis recipe
`overflow:hidden; text-overflow:ellipsis; white-space:nowrap;` **plus** `min-width:0` on every flex ancestor between the text and the scroll/row container (Section 4). Without the `min-width:0` chain, the CSS is inert.

### 5.E Multi-line clamp recipe (`-webkit-line-clamp`)
All four properties together or none work: `display:-webkit-box; -webkit-line-clamp:N; -webkit-box-orient:vertical; overflow:hidden;`. **Never put padding on the clamped element itself** - the clamp math ignores padding and text bleeds. If you need padding, wrap the clamp in a padded parent, or use a fixed-height fallback (`line-height * N`). [css-tricks line-clampin]

### 5.F Content edge cases: counts, big numbers, missing data (mandatory)
Real data is 0, 1, or 1,000,000 - design all three, not just the demo's "3."
- **Zero / one / many (pluralization):** every count string handles 0, 1, and N with correct grammar - "0 items," "1 item," "24 items," never "1 items" or "24 item." Use an ICU/plural-aware formatter, never string concatenation; some languages have up to 6 plural forms. The zero case usually routes to an empty state (Section 6.C), not "0 items" sitting in a full layout.
- **Very large / very precise numbers:** abbreviate for scannability in dense contexts (1.2k, 3.4M, 1.1B) but keep the exact value reachable on hover/focus and in the detail view; **never abbreviate a number the user must act on precisely** (an invoice total, an account balance). Locale-aware grouping (1,234.56 vs 1.234,56), tabular-nums for compared columns (Section 4), and a consistent threshold before switching to abbreviation.
- **Missing / null / not-applicable (general rule, not just table cells):** a null field renders a consistent, quiet placeholder ("Not set," "-," "Unknown") that is visually distinct from an empty string and from zero. Decide per field whether null means "not set yet" (invite input), "not applicable" (explain briefly), or "hidden by permission" (Section 6.G) - three different placeholders, never one blank that reads as a render bug.
- **Long unbroken tokens** (URLs, hashes, file paths, IDs with no spaces): use middle-truncation that keeps both ends, or `overflow-wrap:anywhere`, never a trailing ellipsis that hides the distinguishing tail, and never let the token blow out its column width.

### 5.G Column-header and chrome overflow
- **Column headers**: wrap to 2 lines, then truncate with a tooltip carrying the full header. [carbon]
- **Breadcrumbs**: collapse the middle to an ellipsis/overflow-menu, keep first and last. [carbon overflow]
- **Toolbars / action bars / tabs**: use priority-plus overflow (Fluent Overflow): declare a visible-priority order and a `minimumVisible` floor, move the rest into a "More" menu, render in reverse DOM order so the first item wins. [fluent]
- **Long free content blocks**: "Show more / Show less" for expandable prose, "Load more" for lists (Section 7.D).

---

## 6. STATE MATRIX (Deep-Dive)

Every data surface has more than a happy path. Design the full matrix at **three granularities**: page, component/region, and field. The slop failure is reusing one grey box for every non-happy state.

### 6.A The four base states, always designed together
For any region that loads data, design **ideal / loading / empty / error** before you ship the ideal. [polaris four-states, nngroup]

### 6.B Loading timing thresholds (mandatory)
- **< 1s**: show nothing. A flash-and-vanish skeleton is worse than a beat of stillness.
- **1-10s, full-page/region load**: a **skeleton that mirrors the real layout shape** (the actual rows/fields it will become), never a frame-only grey box, never a spinner for structured content. [nngroup skeleton, carbon loading]
- **> 10s, or unknown-length work** (uploads, downloads, conversions, deploys): a **determinate progress bar**, never an indeterminate spinner or skeleton. For multi-minute work, let the user leave and notify on done. [carbon]
- **Background refresh of already-shown data**: keep the old content visible with a subtle inline indicator. **Never re-blank** cached content to a spinner/skeleton on refresh.

### 6.C Empty states are three distinct states (mandatory)
Never reuse one empty component/message across these:
1. **Never-used-yet (first run)** - onboarding tone: what this is + a primary CTA to create the first record. [primer empty-states, pencilandpaper]
2. **Filtered/searched to nothing** - "no results for X," with a clear-filters action. The data exists; the filter is the cause.
3. **Zero-as-a-win** - "inbox zero," "no alerts." Positive tone, no guilt CTA.
[carbon empty-states, atlaskit empty-state] For tiny tiles/side-panels, a centered text-only empty state is the exception to "mirror the layout."

### 6.D Error states are never empty states
A load failure is **always** an ErrorState, never an EmptyState. Error copy is specific, plain-language, actionable (what to do next), and carries an error code/id for support. Route all of them through one shared ErrorState component so tone and layout stay consistent; never ship a bare "An error occurred." [polaris error-messages, nngroup]

### 6.E Field and inline states
Fields have their own micro-states: pending async validation (Section 8.D), inline error, success confirmation, saving/saved (autosave, Section 8.E). Do not let a field-level failure silently no-op.

### 6.F Partial, stale, and offline states (mandatory to consider)
Between "loaded" and "failed" live the states real networks produce:
- **Partial load / partial failure:** when a composite view loads and one widget fails, fail **that widget in place** (its own inline ErrorState + retry), never blank the whole page for one failed panel. A dashboard where one broken tile kills every tile is a bug.
- **Stale / cached / refreshing:** show last-known-good data with a subtle "updating" indicator and a "last updated <time>" stamp; never re-blank to a skeleton on a background refresh (Section 6.B). On refresh failure, keep the stale data and surface a non-blocking "couldn't refresh, showing data from <time>" notice.
- **Offline / disconnected:** detect connection loss, show a persistent non-modal banner, disable or **queue** mutations, and reconcile on reconnect. Never let a user type into a form that silently cannot save.
- **Optimistic update contract:** if you render a mutation before the server confirms, you MUST have a rollback path - restore the prior value and show a clear error if the write fails. An optimistic update with no rollback is a data-integrity Tell.

### 6.G Permission and plan states (product-UI-only, mandatory to consider)
Marketing UI has no concept of these; product UI lives on them:
- **Permission-denied / role-gated**: decide **disabled vs. hidden** deliberately. Hide an action the user can never have; disable (with a reason on hover/focus) an action they could have with a role change. Never show a dead control with no explanation.
- **Read-only mode**: present the same layout with inputs rendered as static values and a clear "read-only" affordance, not greyed-out inputs that look broken.
- **Plan/license-locked**: a locked-feature affordance ("Upgrade to unlock") is a distinct state with its own component - visible, explained, with an upgrade path - not a disabled button. [Keep it consistent with whatever precedent the host app already sets.]

---

## 7. DATA TABLE DEEP-DIVE (The Hardest Product Surface)

Gate depth by DATA_COMPLEXITY. A simple list needs 7.A-7.B; an enterprise grid needs all of it. **Inside a design system, use its `Table` plus the system's plugins/hooks; the mechanics below are the contract those hooks satisfy, and your guide when you are outside one.**

### 7.A Scroll ownership and sticky header (mandatory)
One wrapper owns both axes (`overflow:auto`) with a bounded height; the page never scrolls sideways (Section 4). Sticky header via `position:sticky; top:0` **scoped to that wrapper**. [carbon, ant table-scroll]

### 7.B Frozen / pinned columns (mandatory recipe)
`position:sticky` + explicit `left:0` (or `right:0`) offset + `z-index >= 10` (above the scrolling body) + a **solid, non-transparent background that also covers hover and selected-row states** + an **inset `box-shadow` divider, never a CSS `border`** (borders disappear or double-render under sticky scroll). Miss the solid background and the scrolling content bleeds through the frozen column. [ant, mantine-react-table column-pinning, tanstack]

### 7.C Virtualization (DATA_COMPLEXITY 3)
Virtualize past ~100-200 rows. Required DOM shape: **two wrappers** - outer = viewport-height scrollable, inner = full virtual-content height (a spacer). **Never size the `<table>` element itself to the full virtual height** - it distorts row heights and collapses the sticky header (which cannot escape a too-short parent). [tanstack virtual #640] Do not attach per-row style objects or per-row menu instances during virtual render (perf death); use `columnResizeMode:"onEnd"` unless memoized. [ant, mantine]

### 7.D Pagination vs. infinite scroll vs. load-more (decision tree)
- **Paginate** once an index exceeds ~50 items (concrete Polaris cutoff), and always for "find a specific item / compare distant items / inspect the top few" tasks. [polaris, smashingmagazine]
- **Infinite scroll**: only for exploratory, homogeneous, endless feeds - **never** for search results or comparison tasks. If used, ship `history.pushState()` so the back button restores scroll position (>90% of implementations get this wrong). On mobile, load one larger flat batch (15-30 items), never chunk-lazy-load mid-scroll (fetches during active scroll are unreliable). [nngroup infinite-scrolling, baymard]
- **Load-more button**: the safe middle for finite-but-long lists; user controls the fetch.

### 7.E Selection, bulk actions, and selection persistence
- Row selection supports Shift-click range and select-all. Distinguish "select all N (across pages)" from "select all on this page" in copy. [polaris]
- **Selection persistence (a classic enterprise correctness bug):** preserve selected-row **IDs** across pagination, sort, and filter changes; do not silently drop the selection when the page changes. Show a running "N selected" count that survives navigation.
- During an active bulk operation, disable per-row actions to prevent conflicting mutations.
- **Toolbar action cap: 5 visible primary actions**, then overflow to a menu. [polaris]

### 7.F Filtering, faceting, and search (distinct from each other)
- **Search** (free text) and **filter** (structured predicates) are different controls; do not merge them into one box silently. Match each filter control to its data type (date range, enum multi-select, numeric range). [data-table-mechanics; most systems ship a toolbar-filter component]
- **Applied-filter chips**: show active filters as a removable chip row above the table with a "Clear all," plus (for many facets) a faceted sidebar. This is the now-standard Jira/Linear/Notion pattern; without the chip row the user cannot see or undo what is filtering their data.

### 7.G Cell content
Cells hold ragged real data. Truncate secondary cells per Section 5 (with focus-reachable full text), never identifying cells. Right-align numeric columns and use tabular-nums (Section 4). Empty cell = a consistent "not set" placeholder (an em-dash is banned; use "-" or "Not set"), never a blank that looks like a render bug.

---

## 8. FORMS, VALIDATION & MULTI-STEP FLOWS (Deep-Dive)

### 8.A Label placement
Top-aligned labels by default (fastest to scan, best for localization and mobile). Right-aligned labels only for dense enterprise forms where vertical space is scarce. Left-aligned only to deliberately slow the user down on a careful task. Never right-align labels on a localized product (expansion breaks the column). [lukew web-form, nngroup web-form-design]

### 8.B Validation timing
Validate on **blur** and on **submit**, not on every keystroke of an incomplete value (do not scream "invalid email" at the first character). The exception is a live positive helper like password-strength. Show inline errors next to the field **and** an aggregate error summary at the top on submit, never only one of the two. [nngroup errors-forms, polaris inline-error]

### 8.C Never disable Submit as the only signal (mandatory)
For forms with 5+ fields, **never** make a disabled Submit the only feedback - the user cannot tell what is missing. Let them submit, then show the aggregate error count and focus the first error. A disabled Submit is acceptable only on trivial (<3 field) forms. **Always preserve user input after a failed submit** - never clear the form. [forms-flows, nngroup]

### 8.D Async / remote field validation
Debounce it, **and** cancel superseded requests with `AbortSignal` - an uncancelled slow response can overwrite a newer, correct result (username-availability race). [forms-flows]

### 8.E Autosave (gate by CONSEQUENCE)
- Autosave **per logical field-group**, never whole-form-on-every-keystroke.
- **Never autosave** password, visibility/permission, confidentiality, or financial-impact fields - those require explicit manual confirm (CONSEQUENCE 3).
- Trigger on blur + ~3s after the last keystroke. Show "Saving..." then "Saved <relative time>."
- A failed autosave gets a **persistent** (non-auto-dismissing) toast with retry, never a silent failure.

### 8.F Multi-step flows / wizards
- The step indicator must map to the **real** steps; completed steps are clickable to go back. No fake "Stage 1 / Stage 2" labels - name the actual step. [taste-skill tell parity]
- Fix wizard abandonment by cutting **field count**, not by adding steps. Do not inject mid-flow upsells. [baymard checkout-linear]
- Keep the flow linear; a branching wizard needs a visible map.

### 8.G Destructive / irreversible confirmation (CONSEQUENCE 3, mandatory)
Confirmation dialogs for delete/deploy/charge **default keyboard focus to the safe action (Cancel)**, not the destructive one. Use `role="alertdialog"`, `aria-modal="true"`, and `aria-describedby` pointing at the warning text. For high-consequence deletes, require typing the resource name to enable the destructive button. On close, return focus to the element that opened the dialog (or the next logical element). [w3 alertdialog, radix dialog]

---

## 9. NAVIGATION, OVERLAYS & LAYERING (Deep-Dive)

### 9.A Dialogs / modals
Focus-trap while open, return focus on close, close on Escape, close on overlay click only when non-destructive. `Dialog.Title` and `Dialog.Description` are **never omitted** even if visually hidden (screen readers announce them). [radix dialog, w3 dialog-modal]

### 9.B Toasts / notifications
Default ~5000ms, **pause on hover and focus**, swipe-dismiss threshold ~50px, dismissible manually. Distinguish foreground announcements (user's own action succeeded) from background ones (something changed) for screen-reader priority. Never put a destructive-confirm inside a toast. [radix toast]

### 9.C Menus, dropdowns, tabs, comboboxes
Full keyboard contract: arrow-key navigation, Home/End, type-ahead, roving tabindex (Section 10.D). Tab moves **between** a composite widget and the next content; arrows move **within** it. Menu/tab items that should stay keyboard-reachable use `aria-disabled`, not native `disabled` (which removes them from the tab order). [radix, w3 grid]

### 9.D The z-index / stacking-context system (mandatory, replaces ad-hoc z-index)
- **Assign wide numeric gaps per tier**, defined once as tokens, e.g. base 0, sticky 100, dropdown 1000, sticky-header 1050, overlay/drawer 1100, modal 1200, popover 1300, toast 1400, tooltip 1500. Never hand-tune a single z-index in isolation; change it against the whole scale. Ad-hoc `9999`/`99999` is a Tell.
- **Enumerate every stacking-context trigger** before debugging a layering bug: `position:fixed/sticky` with a z-index, `opacity < 1`, `transform` / `filter` / `will-change` naming a context property, `contain`, `container-type`, `isolation:isolate`, top-layer elements. [mdn stacking-context]
- **Nested stacking contexts are atomic**: a huge z-index on a deeply nested element **cannot** out-rank a shallow ancestor's sibling. If a menu clips behind a header, the fix is the ancestor context, not a bigger number.
- **Overlays layer by open-order**, not static per-type constants: the last-opened overlay wins. Use a layering manager / the platform top-layer (`<dialog>`, popover API) where available.

---

## 10. DENSITY, I18N & ACCESSIBILITY (Deep-Dive)

### 10.A Density as a first-class mode
Offer >= 3 density presets (comfortable / standard / compact) as a real switch that swaps row-height and padding tokens, not a scaled-down zoom. [i18n-a11y-density] Carbon ships 5 row heights; pick the set your DENSITY dial needs.

### 10.B Internationalization text-expansion budget (mandatory)
Design containers with headroom for translation, because English is one of the shortest UI languages:
- German: **+30-40%** typical, up to ~70% worst case.
- French / Russian / Spanish: +20-25%.
- Finnish: up to +100% (doubling).
- CJK: contracts, not expands.
Never hardcode fixed-width text containers (Section 4). Use flex/grid so text reflows instead of clipping. Pseudo-localization (wrap strings in accented padding) is a fast smoke test that catches ~80% of expansion bugs. [crowdin, i18n-a11y-density]

### 10.C RTL
Mirror **directional** icons only (back/forward arrows, chevrons, progress direction). **Never** mirror universal icons (clock, play, checkmark, logos). Numerals keep LTR shaping even inside RTL text. The primary action button moves to the left (the natural end of an RTL reading scan). Progress bars fill right-to-left. [crowdin]

### 10.D The ARIA grid keyboard contract (mandatory for any custom grid/table with focusable cells)
- **Roving tabindex**: exactly one cell has `tabindex="0"`, all others `-1`; the grid container itself is never a tab stop.
- Arrow keys move between cells, **boundary-clamped** (no wrap at row/column edges).
- **Home/End** move within the current row; **Ctrl+Home / Ctrl+End** jump to the grid's first/last cell.
- **Page Up/Down** only in scrollable grids (move ~5 rows).
[w3 grid data-grids] If you use a real design-system Table (Carbon, Fluent, Polaris, Ant), this is handled - do not reinvent it. Reach for the contract only when hand-building a grid.

### 10.E Cross-cutting a11y floors
- Touch targets >= 44-48px (touch), >= 24px (dense desktop). [material3 accessibility]
- `:focus-visible`, never a bare `:focus` that flashes on mouse click; never remove focus outlines without replacing them.
- Every icon-only control has an `aria-label`.
- Locale-aware number/date/currency formatting; never ship ambiguous `01/02/2025`.

---

## 11. ONBOARDING & PROGRESSIVE DISCLOSURE

Dense products overwhelm on first run. Reveal power progressively; earn complexity.

**Progressive disclosure (the default mechanic):**
- Keep advanced controls (bulk edit, column management, saved views, API/webhook config) one interaction away (a "More," an expander, a settings popover), not all on screen at once. Linear's principle: simple to start, grows more powerful. [linear]
- **Rule of thumb: >7 controls in a region is the disclosure trigger.** Group the primary 3-5 actions inline and overflow the rest; surface advanced settings behind a labeled expander, never a mystery-meat gear with no tooltip.
- Disclosure is per-surface, not global: do not hide a control the user just used two clicks ago.

**First-run (mandatory):**
- First run is the **"never-used" empty state** (Section 6.C.1), not a blank grid or a spinner. It states what this surface is in one line and points at the single first action ("Create your first project"), not a menu of ten.
- Seed with sample/demo data only if it is clearly labeled and one-click removable; never leave fake "Acme Inc" rows the user cannot tell from real data.

**Coach marks, tours, checklists (banned unless dismissible):**
- Any coach mark, product tour, or onboarding checklist MUST be skippable on step 1 and dismissible permanently; dismissal persists per user across sessions (never re-fire a dismissed tour). A tour that cannot be skipped, or a checklist with no close affordance, is a **Tell**.
- Max one active tour at a time; never stack a coach mark on top of a modal.
- Tours point at real controls in the real UI; never a fake highlighted screenshot. Return the user to a usable state on exit, not a dead end.
- Segment: returning/experienced users and invited teammates skip the first-run flow; do not re-onboard someone joining an existing populated workspace.

**Empty-to-productive path:** every empty state's CTA leads somewhere that actually creates value in <=3 steps. An onboarding checklist that just links to docs is decoration.

---

## 12. CONTEXT-AWARE PROACTIVITY (Canonical Skeletons to Recognize)

When the Product Read matches one of these, scaffold the whole skeleton, not a fragment:
- **Index/table page**: heading + toolbar (search, filters, primary action, density) + applied-filter chips + Table (sticky header, selection) + pagination footer + the three empty states + error state.
- **List-detail / master-detail**: list region + inspector LayoutPanel that overlays below ~1024px + "nothing selected" empty state.
- **Settings page**: section nav + FormLayout panels + autosave-or-save-bar + a Card only around the danger zone.
- **Multi-step wizard**: real stepper + linear steps + per-step validation + a review step + a non-destructive exit.
- **Dashboard/overview**: KPI tile row (Cards) + widget grid + one or two drill-in Tables (rows).
- **Admin console with bulk actions**: table + selection persistence + bulk action bar (capped at 5 + overflow) + confirmation dialogs.

Full component implementations live in the host system, not duplicated here: reach them via your host system's template/skeleton command or its docs (`references/canonical-sources.md`). Three high-value skeletons are worked in `references/block-skeletons.md` because they encode the contracts most often gotten wrong; treat them as the canonical shape, adapt to the host system.

---

## 13. PERFORMANCE & ACCESSIBILITY GUARDRAILS
- Table load/filter response should feel instant; past ~1s show optimistic/loading feedback, past the thresholds in 6.B escalate.
- Enterprise-grid perf: no per-row style/menu object allocation on render; scoped auto-sizing; `columnResizeMode:"onEnd"` unless memoized; virtualize past ~100-200 rows.
- Motion in product UI is **feedback only**: state transitions, focus movement, a row entering/leaving. No decorative scroll animation, no marquees, no parallax. Respect `prefers-reduced-motion` for everything.
- Core Web Vitals still apply: CLS < 0.1 (skeletons must reserve the real dimensions so content does not jump), INP < 200ms on interactions.

---

## 14. DARK MODE
Token-driven, one theme locked per app (same discipline as taste-skill Section 8/11: no region flips to inverted mid-app). Use the host system's semantic layer tokens (`var(--color-*)`, Carbon `$layer`/`$border-subtle`, etc.), never hardcoded greys. Test tables, frozen columns (the solid background must be a **theme token**, or it bleeds in dark mode), overlays, and focus rings in both modes. Set the theme once at the shell root, never per-section.

---

## 15. PRODUCT-UI AI TELLS (Forbidden Patterns)

Distinct from taste-skill's landing-page tells. These are the signatures of a model faking a product screen. Hard bans unless the brief genuinely demands one.

- **Card soup**: every record wrapped in a Card + Badge. Use rows. (Section 0.C)
- **Fixed-width `<table>` that scrolls the page sideways**: no scroll-owning wrapper. (Section 4)
- **Truncated button label** ("Save chang..."). Size to content. (Section 5.C)
- **Truncated identifying content** (names/IDs/errors) with a hover-only `title`. (Section 5.A-B)
- **`disabled` Submit as the only validation** on a 5+-field form. (Section 8.C)
- **One generic empty state** reused for first-run AND filtered-empty AND load-failure. (Section 6.C-D)
- **"An error occurred"** with no cause, action, or code. (Section 6.D)
- **Skeleton that never resolves**, or a frame-only grey box that does not mirror the real layout. (Section 6.B)
- **Full-page spinner on a cached background refresh** (re-blanking data the user was reading). (Section 6.B)
- **Sticky/frozen column with a transparent background** (content bleeds through on scroll). (Section 7.B)
- **Ad-hoc z-index** (`9999`, `99999`) instead of a tiered token scale. (Section 9.D)
- **Fixed-width badges/labels/tabs** that clip under German/Finnish expansion. (Sections 4, 10.B)
- **Native `disabled` on menu/tab items** that should stay keyboard-reachable (use `aria-disabled`). (Section 9.C)
- **Badge as decoration** and **status dots spammed on every row** (status only, sparingly).
- **Motion for show** in a work tool (decorative scroll/hover animation). (Section 13)
- **Fake step labels** ("Stage 1 / Stage 2"), fake precise numbers, "Jane Doe"/"Acme" placeholder data in a shipped screen.
- **Em-dash (`—`) anywhere visible.** Banned in headers, cells, labels, empty/error copy, tooltips, and as the "not set" cell placeholder. Use a hyphen (`-`). This is the single most-violated Tell; zero tolerance. (taste-skill Section 9.G, house rule)

---

## 16. REFERENCE VOCABULARY (Names the Agent Should Know)
App shell / PageLayout (Header / Content / Pane / Sidebar / Footer) · canonical layouts (list-detail / supporting-pane / feed) · master-detail + inspector · IndexTable / Resource List / DataGrid / Table · frozen (pinned) columns · virtualization · roving tabindex · stacking context · container query · skeleton screen (shape-mirroring) · Blankslate / EmptyState / ErrorState · Overflow / priority-plus · applied-filter chips / faceted search · alertdialog · optimistic vs. pessimistic update · density mode · pseudo-localization · command palette · workspace switcher · job/status tray.

---

## 17. REDESIGN PROTOCOL (Auditing an Existing Dense Screen)
Before touching visual style, audit for the correctness bugs that matter more than aesthetics:
1. **Scroll ownership** violations (page scrolls sideways; nested double-scroll).
2. **Truncation on primary content**; hover-only fallbacks.
3. **Missing state differentiation** (one empty box for three states; no error state; skeleton missing).
4. **Frozen-column bleed-through**; transparent sticky backgrounds.
5. **z-index ad-hockery**; layering bugs from nested stacking contexts.
6. **No i18n buffer**; fixed-width text containers.
7. **Keyboard/a11y gaps**: no roving tabindex, bare `:focus`, icon buttons without labels, disabled submit as only signal.
Fix these first. Only then apply the density/token/visual polish. Preserve the host design system; do not swap Carbon for shadcn as a "redesign."

---

## 18. RELATIONSHIP TO taste-skill + OUT OF SCOPE
- **Hand off to `taste-skill`**: marketing hero sections, landing pages, portfolios, editorial, illustration-heavy brand surfaces. If a screen is half product, half marketing, split it: taste-skill for the marketing sections, this skill for the product surface. Never run both on one component.
- **Hand off to `dataviz`**: chart/graph authoring (color, encoding, axes). This skill covers the table and the dashboard frame around the charts, not the chart internals.
- **Out of scope**: native mobile (iOS/Android) app chrome beyond responsive web (tab bars, native nav) - a different skill's job; flag it, do not silently approximate. Realtime collab primitives (presence, cursors, OT) - different problem class.

---

## 19. FINAL PRE-FLIGHT CHECK

**Run every box. If any fails, the surface is not done.**

- [ ] **Product Read** stated (Section 0.B one-liner)?
- [ ] **Dials** (DENSITY / DATA_COMPLEXITY / CONSEQUENCE) set from the read, not silently baseline?
- [ ] **Frame budgeted in px** before content; shell + landmark regions named (Header/Content/Pane/Sidebar not conflated)?
- [ ] **Rows not cards** for dense data; Card only for widgets; no card soup, no nested cards?
- [ ] **Scroll ownership**: exactly one wrapper per axis, page never scrolls horizontally, sticky scoped to the wrapper?
- [ ] **min-width:0** on every truncating flex text child?
- [ ] **No truncated primary content** (names/IDs/errors/headers) and **no truncated button labels**; every truncation has a focus-reachable full-text fallback?
- [ ] **Line-clamp recipe** complete (all 4 props, no padding on the clamped node)?
- [ ] **Four states designed** (ideal/loading/empty/error) for every data region?
- [ ] **Loading thresholds**: <1s nothing, skeleton mirrors layout, >10s determinate progress, cached refresh never re-blanks?
- [ ] **Three distinct empty states** (first-run / filtered-empty / zero-as-a-win); load failure is an ErrorState with cause + action + code?
- [ ] **Partial/stale/offline states** handled (one failed widget fails in place; cached refresh never re-blanks; offline queues or blocks with notice; optimistic updates have a rollback path)?
- [ ] **Content edge cases**: counts pluralized (0/1/N, no "1 items"); big numbers abbreviated with exact value reachable and never abbreviated where precision matters; missing data has a consistent placeholder distinct from zero/empty?
- [ ] **Permission/plan states** considered (disabled-vs-hidden, read-only, plan-locked) where roles/tiers exist?
- [ ] **Table**: scroll-owning wrapper + bounded height; sticky header; frozen columns have solid theme-token background + inset-shadow divider + z-index; virtualization uses the two-wrapper DOM?
- [ ] **Pagination vs infinite** chosen correctly (paginate >50 / for search; infinite only for feeds with pushState + mobile flat batch)?
- [ ] **Selection persists** across page/sort/filter; bulk toolbar capped at 5 + overflow?
- [ ] **Applied-filter chips** row present when filters exist; search and filter are distinct controls?
- [ ] **Forms**: top labels default; validate on blur+submit; inline + summary errors; input preserved on failed submit; no disabled-submit-as-only-signal on 5+ fields?
- [ ] **Async validation** debounced + AbortSignal-cancelled?
- [ ] **Autosave** per group, not for password/permission/financial fields, with Saving/Saved states + persistent retry on failure?
- [ ] **Destructive confirm** focuses the safe action, `role=alertdialog`, returns focus on close?
- [ ] **Dialogs** trap+return focus, Escape-close, Title/Description present; **toasts** pause on hover, dismissible?
- [ ] **z-index** from a tiered token scale (no 9999); layering bugs traced to stacking contexts, not bigger numbers?
- [ ] **i18n buffer** on every text container (+30-40% DE); no hardcoded fixed-width text; tabular-nums on compared numbers?
- [ ] **RTL** mirrors directional icons only (if RTL in scope)?
- [ ] **Keyboard/a11y**: roving tabindex on custom grids, `:focus-visible`, icon buttons labelled, `aria-disabled` not `disabled` on keyboard-reachable menu items, 44px/24px targets?
- [ ] **Density switch** offered where DENSITY calls for it (mode swap, not zoom)?
- [ ] **Dark mode** one theme locked, frozen-column background is a theme token, tested in both modes?
- [ ] **House system**: props discovered from real docs (nothing invented), no `<div>` for layout, tokens only, Badge for counts only, status via a status indicator?
- [ ] **No product-UI Tells** from Section 15; **zero em-dashes** anywhere visible?
- [ ] **One design system** per app (no Carbon + Fluent mixed)?

If a single box cannot be honestly ticked, fix it before delivering.

---

## References
- `references/block-skeletons.md` - worked reference implementations for the three block contracts most often gotten wrong (index + detail-drawer frame, table scroll/sticky-header/frozen-column CSS contract, truncation contract).
- `references/install-commands.md` - Appendix A: package-manager install commands per host design system.
- `references/canonical-sources.md` - Appendix B: gsearch-verified primary-source URLs backing this skill's rules, grouped by topic.

