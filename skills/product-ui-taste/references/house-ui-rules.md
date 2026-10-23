# Product UI house rules

Distilled from design review corrections, pattern research on ChatGPT, Claude, Manus, Perplexity and Linear, and agent message stream rules. Apply them to any product UI you review. Where a rule here conflicts with a recipe in `SKILL.md`, this file wins.

Think of the app like a good restaurant. The guest sees a short menu and one waiter, and the kitchen stays behind the door. A cook who wants to see the kitchen can open the door.

## Target user

The default view serves the least technical person who uses the product. Judge every screen, message and setup step as that person meets it first. Technical users keep everything, one click deeper.

- Copy the register of ChatGPT, Claude and Manus. Check a pattern library such as Mobbin for the same surface type before you design it, and cite the screens.
- Remove nothing for simplicity. Move it to Details or Advanced, and give each item one home.
- Offer a setting "Show technical details by default" for developers.

## Two layers

| Default view | Details or Advanced |
|---|---|
| One plain answer, what to do next, short steps, what failed, what is left | Ids, shas, internal stage names, tool lines, tokens, confidence, file paths, raw logs, server error text |
| Three questions in a form, named by outcome | Every other field, folded under Advanced |
| Sent: "Result posted on PR #57" | Target strings, replaced drafts, internal kinds |

The Details control is a visible labeled button that opens a side panel or a fold. Hide a tab that has no content.

## Words

- Use one term per meaning, taken from the user's own day. Before the build, write a glossary table: today's word, default-view word, Details word.
- Never show internal codes (P1, M0, S1) as labels. Codes stay in code.
- Name choices by outcome: "Most capable for ambitious work", "Asks you first", "Never does it".
- A label names the thing. Delete slogan subtitles ("Nobody waits"). Keep a subtitle only when it adds a fact.
- Section titles are noun phrases. No verb, no question, no sentence.
- Keep screen copy short: page subtitle 10 words or fewer, setting row is a title plus one sentence at most, no group-row notes. The explanation of a rule belongs in the docs.

## Agent messages

- Lead with what happened and what to do next, in first person and everyday words. Two or three short sentences, then one offer.
- No ids, stage names, rule names or tool names in the message body.
- State each count once.
- Render Markdown drafts exactly as the destination renders them (GitHub, Jira, Slack). Screenshot the posted result and judge readability.
- Every reference a person reads carries a short title with the link on it: [Queued checks show at once (#30)](https://github.com/your-org/your-repo/pull/30). In the UI, show a chip as described under External objects.

## Progress and results

- Show long work as 3 to 6 steps in everyday words, with a count, a timer and one live line: "Working, step 3 of 5 · 0:12".
- Fold finished work into one line: "Checked 4 things in 16 s".
- Show no verdict text until the work ends.
- Put the result first: outcome word, one sentence, the cause in words, and one main button named by the outcome ("Review the bug report").
- End a long task as one card: summary, evidence or files, two or three follow-up chips, a one-tap rating.

## Choices and approvals

- A screen asks three questions at most. Preselect the safe choice. Put the rest behind "Later" or Advanced.
- Collapse grids of knobs into one question with three outcome answers, such as "Ask me before anything is posted" (default), "Ask me only for important posts", "Post on its own".
- Ask only when blocked, as one card in the place the user already is. The card says what will happen, where, and who sees it. The button names the action: "Post to PR #58", "Edit", "Don't post".
- Safety checks pass in silence and speak only when one fails.
- Small changes apply at once with Undo. Changes to a plan or anything outward need an approval card.

## Controls

- Never disable or grey out a control. If a precondition is missing, do the precondition and show a one-line notice ("Switched to annual billing"). Validate on submit and keep the button live. Hide a control that never applies.
- Never hide features behind a `…` menu. Use visible labeled buttons, a status pill, inline rename, footer rows.
- Controls never wrap their label: buttons, chips, status pills, tabs. Use `white-space: nowrap`, a shorter word, or one font step down. A wrapped control label is a visual bug.
- Prefer optical alignment to strict pixel alignment.

## Lists

- A list is one bordered block with hairline dividers between rows.
- No colored border or left stripe on any list item: selected, running and status rows included. Selected uses a neutral border and the selected surface background.
- Show status and every categorical value (project, source, kind, risk) with one shared IconLabel pattern. Each value has its own shape and color, so color never carries the meaning alone: passed check green, failed cross red, skipped minus grey, warning amber, timed out clock red, running spinner accent.
- Show icon plus word where the list has room, icon only where it does not, and keep the word in `aria-label`. Decide by the list's own width with a container query; a narrow side panel on desktop counts as limited.
- Draw a signature SVG icon family per product (one stroke weight, one corner style, one grid) when stock icons do not fit. In shadcn projects, start from `pnpm dlx shadcn add @lucide-animated/<name>`.
- Audit and change every list in one pass, never one screen at a time.

## Text overflow

- Never truncate titles, goals or descriptions with an ellipsis and a tooltip. Wrap with `overflow-wrap: anywhere` and let the row grow.
- If a column is too narrow for a name, show another short fact (a date, a count) and keep the full name in `aria-label`.
- A wide table scrolls inside its own wrapper with edge shadows. The page never scrolls sideways.

## Intelligent UI

Chat answers carry working views, the way ChatGPT's Intelligent UI and the Apps SDK do. The model returns typed data; the client renders it with components it owns.

### Visual weight in the stream

| Level | What | Style |
|---|---|---|
| Primary | Answer text, answer blocks, object cards, errors the user can fix | Rich formatting. Only blocks and cards get a border or background. |
| Secondary | Live status line, finished-work summary line, context line ("With: Checkout · PR #57") | Grey text and a small icon. The `›` chevron is the only affordance. |
| Tertiary | Expanded steps | Indented grey text under the summary line |
| Hidden | JSON, raw API data, tool names, sub-agent containers | Details panel or developer console only |

- Only two things earn a container: the user's message and structured output (blocks, object cards). Status, steps and thinking stay as grey text.
- One live status line at a time, updated in place, written as intent ("Reading the ticket..."). Skill loads and agent handoffs stay silent. The line goes away on the first answer token.
- Nesting depth is one: summary line, then a flat list of steps. Sub-agent work reads as the parent's work.
- Show thinking only inside the expanded steps.
- After 30 s add "This is taking longer than usual." After 60 s add a Cancel link.
- Motion: crossfade the status text, pulse the status dot, animate height on expand (200 ms). No progress bars, no bounce. Honour reduced motion.

### Answer blocks

- The model picks a block kind from a fixed registry and fills in data. It never sends HTML or code; the client owns the look and the actions.
- Text carries the judgement, the block carries the records. Show a block only for data that answers the question. Repeating structure becomes a block; prose stays text.
- Every block sits in one hairline frame with a heading and a count, rows with dividers inside. Several objects from one answer form one list.
- Blocks render read-first at their smallest useful size. Inline blocks stay compact; a full view (board, diff, dashboard) opens in the side panel. Nothing opens or expands on its own.
- The server sends a loading block first with skeleton rows shaped like the real ones, then the rows.
- Validate every block on the server and again on the client. Drop invalid rows and keep the valid ones. Allow only `http` and `https` links.
- Unknown or broken data falls back to a table, with the line "Shown as a table because this answer has no matching view yet." A component that throws renders the same rows as a table in place.
- Each action shows its result under the row that started it. A second press while the first runs does nothing.
- Every outward action from a block goes through the approval gate. Actions confirm in the steps line: "Moved SHOP-123 to Done".

## External objects

An object that lives in another system (a Jira ticket, an Xray test case, a GitHub PR, a Linear issue, a Confluence page, a Slack message, a TestRail case) renders the way its own product renders it.

- Copy the source's native anatomy: the fields it shows, their order, its status lozenge colors and shapes, its issue-type and priority icons, its PR state icon and color (open green, merged purple, draft grey, closed red). A Jira ticket looks like a Jira ticket to someone who uses Jira daily.
- Keep the host product's frame, spacing and type around it, so the card sits in the list with the other rows. The content inside the frame follows the source.
- Every external object shows its source's logo icon at the start of the card or row. The logo is how a reader tells our objects from alien ones. Our own objects carry no logo.
- Every id or key (SHOP-142, PROJ-T23, #58) is a link that opens the original item in its own system, in a new tab. Make the whole chip or card clickable, and keep in-app actions as separate labeled buttons.
- An inline reference in text renders as a chip: source logo, key, short title. Never a bare key.
- A pasted link to a known system unfurls into the same card.
- A card for a source with no renderer falls back to a chip with logo, key, title and link.
- Light actions (transition, assign, comment) sit on the card and go through the approval gate. Heavy views open in the side panel.
- Keep the source names, statuses and field names as the source spells them ("In Progress", "To Do", "Story Points").

## Navigation and structure

- One front door: Home is a greeting, one ask box and three starter chips in the user's words.
- Keep four or five top-level places, the same set on the phone bar.
- An inbox uses the Linear layout: list on the left, open item on the right, one item per screen on a phone.
- Group one cause into one row: events from several sources about the same root problem show as one row with the related items inside.
- Settings opens on personal items. Connections and Advanced appear only for admins.
- Maps and coverage views come from observed evidence (pages visited, real screenshots). Static scans only enrich them. Show unseen parts as gaps.
- For management overviews, apply semantic zoom inside the timeline or table. A separate box-canvas view was rejected. See `semantic-zoom.md`.

## Setup

- No wizard before the first task. One question per screen, a skip on every optional step.
- Optional setup lives as a checklist card on Home until it is done.
- A banner appears only when something stops working.
- Ask for notification rights after you say what the user gets, with "Maybe later". Default alerts to "Only what needs me".

## Errors and empty states

- Write each error in three parts: what happened, what to do, one button. Place it where the problem happened. Put server text and `HTTP 500 /api/...` in a Details fold.
- Use three error kinds: offline, server problem, signed out.
- When only an admin can fix it, say so and offer "Copy a message for your admin".
- An empty state is a heading, one sentence on what will appear, and one button when there is a first action. No illustration.

## Verification

- Judge the rendered pixels; a correct DOM can still look wrong. Screenshot at 390x844 and 1440x900, light and dark.
- Check for wrapped controls, clipped text, sideways scroll, overlap and contrast. Fix what you see, then capture again.
