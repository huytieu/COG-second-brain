---
name: release-comms
description: >
  Release communication pipeline for your product: turn a deployment runsheet and a
  GitHub milestone into a customer-facing release note with real screenshots and
  videos, docs updates (including retrofits of articles the release makes stale),
  a Slack announcement draft, and a lightweight marketing package. Use when you say
  "cover today's release", "write the release note", or "/release-comms".
---

# release-comms: release note, docs, announcement and marketing pipeline

**Lane: `full`.** It mutates external state (Slack posts, docs PR, wiki pages), so every post and PR is drafted first and gated on the user's explicit approval. See the `closed-loop` skill.

## Configuration

Fill these in once (`kit.toml`, `.env` or arguments). Placeholders below are examples.

| Setting | Meaning | Example |
|---|---|---|
| `PRODUCT_REPO` | Repo that holds the release milestone | `your-org/your-product` |
| `MILESTONE_PATTERN` | Milestone naming | `Release YYYY-MM-DD` |
| `TEAM_LABEL` | Label that filters the milestone to your team | `team:platform` |
| `RUNSHEET_SOURCE` | Where the deployment runsheet lives | a wiki page, a doc, or a Slack thread |
| `RELEASE_DIR` | Working folder per release | `comms/release-notes/<date>/` |
| `DOCS_REPO` | Local path of the docs repo | `../your-docs` |
| `RELEASE_NOTES_FILE` | Running release-notes page in the docs repo | `docs/release-notes.md` |
| `ANNOUNCE_CHANNEL` | Slack channel for the internal announcement | `#product-releases` |
| `MARKETING_CHANNEL` | Slack channel for the marketing package | `#marketing` |
| `FLAG_SYSTEM` | Feature-flag tool named in the runsheet | any |

## Source-of-truth chain (walk it in order)

1. **Deployment runsheet.** Gives release scope, the milestone link, the PR list per service, feature flags being enabled, the deploy window, and trailing items (merged to QA but not staged). Exclude trailing items from "available now".
2. **GitHub milestone.** The milestone filtered by `TEAM_LABEL` is the release manifest. Issues may still be open, so closed does not equal shipped.
3. **Issue bodies and comments.** This is the media source. Dev-test comments ("Dev test: passed on prod") and QA comments ("Verified PASSED on staging") carry screenshots and demo videos as GitHub attachment URLs. For a private repo these need auth to resolve:
   `curl -sL -H "Authorization: Bearer $(gh auth token)" -o <file> <url>`
   Check the Content-Type with `curl -sI` for the right extension. GitHub videos are usually QuickTime `.mov`. Treat a comment-level "Verified PASSED" as the ship signal, because issues often stay open until a later close step.
4. **Feature flags.** Anything behind a flag in the runsheet gets honest gating language ("rolling out", "enabled per organization").

## Pipeline

### 1. Collect (parallel workers, staging files)
Use one worker per headline cluster plus one sweep worker over the remaining milestone issues. Each worker extracts user-visible changes with verbatim quotes and links, classifies each as user-facing feature, user-facing fix or internal, downloads media into `assets/` with descriptive kebab-case names, writes to `RELEASE_DIR/staging/<cluster>.md`, and returns only a status line. Never paste one worker's output into another's prompt.

### 2. Release note (lead writes, single file)
Write `RELEASE_DIR/release-note-<date>.md`: frontmatter (version, date, milestones, labels), a one-paragraph narrative summary, **Highlights** (bold, benefit-first bullets with issue links), per-feature sections (What's new, Why this matters, What you can do now, Shipped in this capability), Enhancements, Fixes, and an appendix table of shipped issues. See the `generate-release-notes` skill for the base format.

Voice rules:
- Do not write a feature list. Every item says what the user can now do and what pain it removes. Lead with the before/after story where one exists.
- Embed the downloaded screenshots and videos inline next to the feature they prove.
- Disclose known issues plainly with a fix timeline.
- Flag to the user anything user-benefiting found in the sweep that they did not list.
- Frame the release around the opportunity it opens, and sanity-check every number.
- Naming: avoid "v1" or "first version" in customer copy. Call gated first releases "early access". Call UI refreshes "a new look", not "redesign". Describe capabilities as what is now supported, and say when one serves both humans and agents.
- The internal post is the deep dive: same naming, plus issue links, flag names, architecture notes, verification status and known-issue numbers. Marketing copy stays light.

### 3. Docs updates (branch off main, never touch in-flight branches)
Use a git worktree so work in the main checkout is never disturbed:
`git worktree add ../docs-release-<date> -b release-comms/<date> origin/main` (run inside `DOCS_REPO`). Check what exists on `origin/main` before planning edits, because drafts in the checkout may not be merged. Two motions:
- **New or changed feature docs.** Use the `feature-doc` skill for any new article or real screenshot refresh.
- **Retrofit sweep.** Grep the docs for surfaces this release changed: stale screenshots, stale flow text, stale limitations. Always add the release entry to `RELEASE_NOTES_FILE` (heading per date, "What's new" and "Why this matters" for features, enhancements and fixes in collapsible blocks). If unmerged drafts cover the same surface, do not edit them. Flag the needed change to the user for that branch.
The docs PR is a ship gate: the user approves before it opens. To publish the note to a wiki, see the `publish-to-confluence` skill.

### 4. Slack announcement draft (`ANNOUNCE_CHANNEL`)
Format: an announcement line (`:mega: *Product Release Announcement* | <release note link> | Available now`), a channel-wide greeting, then emoji-prefixed bold-name bullets with one benefit sentence each, a known-issue heads-up, and a link to the full release note. Keep it terse. Draft only: the user posts or approves posting.

### 5. Marketing package (`MARKETING_CHANNEL`)
Use a lightweight changelog-thread format, not positioning essays:
1. **Lead post:** "This week's release:" plus a numbered list (`1/ ...`), one line per shipped feature, and one short closing line. No media required.
2. **One detail post per feature:** a hook line (the pain or the punch), 2 to 4 short lines on what it does, the benefit and a use case, an honest caveat if any, and a specific demo video, GIF or screenshot from `assets/` (name the file and note any trim or convert work). Each post reuses cleanly as an X or LinkedIn thread, a Slack lead with thread replies, or a newsletter section.
3. **Media manifest:** each asset marked near-ready, needs trim, or missing (record fresh). The `release-video`, `social-media-kit` and `youtube-video-kit` skills cover producing media.
4. **Suggested channel message** for the people who compile and review the newsletter.
Draft only: gate on the user.

### 5b. Demo videos back to the tickets (optional)
Once demo videos are published somewhere the team can open, write each video link into a "Demo" field on every shipped issue it covers (for example a GitHub Project text field, set through `gh api graphql` with `updateProjectV2ItemFieldValue`). One link per issue. Check an existing value before overwriting it. Verify by re-reading the field.

### 6. Verify (closed loop)
- A fresh-context verifier re-checks release-note claims against the issue links and tags each Verified, Weakened or Falsified. Drop or demote accordingly.
- Media check: every embedded asset exists locally and renders (size above zero, correct extension).
- After any approved Slack post or docs PR, re-fetch the artifact and confirm it matches intent.

## Cockpit
Keep a `session-review.md` in `RELEASE_DIR` (the `review-cockpit` pattern): progress, one card per deliverable, the user's approvals logged. Delete staging files after consolidation.
