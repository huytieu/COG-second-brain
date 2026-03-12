---
name: publish-to-confluence
description: Publish any markdown file from the vault to Confluence with format conversion and approval gate
roles: [product-manager, engineering-lead, founder]
integrations: [confluence]
---

# COG Publish to Confluence Skill

## When to Invoke
- User wants to publish a document to Confluence
- User says "publish to Confluence", "push to wiki", "send to Confluence", "confluence publish"
- User has a markdown file they want to share with the team on Confluence
- After generating a PRD, release notes, or other document that should go to the wiki

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — no significant benefit for this skill (single sequential operation)
- If `agent_mode: solo` — standard execution

## Command: `/publish-to-confluence`

## Pre-Flight Check

1. **Read `00-inbox/MY-INTEGRATIONS.md`** — Confluence MUST be listed under Active Integrations
   - If Confluence is **not active**: Inform the user and stop.
     ```
     Confluence is not in your active integrations.

     Would you like to:
     a) Set up Confluence integration (I'll add it to MY-INTEGRATIONS.md)
     b) Export the document in a Confluence-compatible format for manual upload
     ```
   - If Confluence is **disabled**: Skip silently per COG conventions. Suggest alternative publishing (HackMD, Notion) if active.

2. **Get current timestamp:** Run `date '+%Y-%m-%d %H:%M'` using Bash

---

## Execution Strategy

### Phase 1: Identify the Source Document

Determine what to publish:

**Option A: User specifies a file path**
```
Read the specified file from the vault.
```

**Option B: User describes the document**
```
Search for matching files:
1. Glob for likely matches in 04-projects/, 05-knowledge/, 01-daily/
2. Present candidates and let user choose
```

**Option C: Just-generated document**
If this skill is invoked right after generating a PRD, release notes, or other document, use that document.

### Phase 2: Configure Publishing Target

Ask the user (if not already provided):

```
Where should this be published in Confluence?

Required:
- Space key: [CUSTOMIZE: YOUR-SPACE-KEY] (or let me search for spaces)
- Parent page: [Page title or ID under which to nest this page]

Optional:
- Page title: [defaults to the document's H1 heading]
- Labels: [Confluence labels to add]
- Publish mode: "create new" or "update existing"
```

**If the user doesn't know the space or parent page:**
```
Use WebFetch to search Confluence:
GET /wiki/rest/api/space?limit=50
- List available spaces for the user to choose

GET /wiki/rest/api/content?spaceKey=[SPACE]&type=page&limit=25
- List pages in the space for parent page selection
```

### Phase 3: Convert Markdown to Confluence Format

Convert the markdown document to Confluence storage format (XHTML):

**Conversion rules:**
| Markdown | Confluence Storage Format |
|----------|--------------------------|
| `# Heading` | `<h1>Heading</h1>` |
| `## Heading` | `<h2>Heading</h2>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `- list item` | `<ul><li>list item</li></ul>` |
| `1. list item` | `<ol><li>list item</li></ol>` |
| `[text](url)` | `<a href="url">text</a>` |
| `` `code` `` | `<code>code</code>` |
| Code blocks | `<ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[...]]></ac:plain-text-body></ac:structured-macro>` |
| Tables | `<table><tbody><tr><th>...</th></tr><tr><td>...</td></tr></tbody></table>` |
| `> blockquote` | `<blockquote><p>quote</p></blockquote>` |
| `---` | `<hr />` |
| `- [ ] task` | `<ac:task-list><ac:task><ac:task-status>incomplete</ac:task-status><ac:task-body>task</ac:task-body></ac:task></ac:task-list>` |
| `- [x] task` | Same with `complete` status |
| YAML frontmatter | Strip entirely (not displayed in Confluence) |

**Important conversion notes:**
- Strip YAML frontmatter — it should not appear in the Confluence page
- Preserve table structure carefully
- Convert relative vault links to plain text (they won't work in Confluence)
- Handle nested lists properly
- Preserve emoji characters as-is

### Phase 4: Preview and Approval Gate

**CRITICAL: NEVER publish without explicit user approval.**

Present a summary to the user:

```
Ready to publish to Confluence:

Document: [filename]
Title: [page title]
Space: [space key]
Parent Page: [parent page title]
Mode: [create new / update existing]
Labels: [labels]

Content preview (first 500 chars):
[preview text]

Estimated page size: [approximate word count]

Proceed with publishing? (yes/no)
```

**Wait for explicit "yes" before proceeding.**

### Phase 5: Publish

#### Create New Page
```
Use WebFetch to POST to Confluence REST API:

POST [CUSTOMIZE: your-confluence-url]/wiki/rest/api/content

Headers:
  Content-Type: application/json
  Authorization: [from configured credentials]

Body:
{
  "type": "page",
  "title": "[page title]",
  "space": { "key": "[SPACE_KEY]" },
  "ancestors": [{ "id": "[PARENT_PAGE_ID]" }],
  "body": {
    "storage": {
      "value": "[converted XHTML content]",
      "representation": "storage"
    }
  },
  "metadata": {
    "labels": [
      { "prefix": "global", "name": "[label]" }
    ]
  }
}
```

#### Update Existing Page
```
First, get the current page to obtain the version number:
GET [CUSTOMIZE: your-confluence-url]/wiki/rest/api/content/[PAGE_ID]?expand=version

Then update:
PUT [CUSTOMIZE: your-confluence-url]/wiki/rest/api/content/[PAGE_ID]

Body:
{
  "type": "page",
  "title": "[page title]",
  "version": { "number": [current_version + 1] },
  "body": {
    "storage": {
      "value": "[converted XHTML content]",
      "representation": "storage"
    }
  }
}
```

### Phase 6: Confirm and Update Vault

After successful publishing:

1. **Confirm to the user:**
   ```
   Published successfully!

   Page: [Title]
   URL: [Confluence page URL]
   Space: [Space Key]
   Version: [version number]
   ```

2. **Update the source vault file** (add published metadata to frontmatter):
   ```yaml
   confluence_url: "[page URL]"
   confluence_page_id: "[page ID]"
   confluence_space: "[space key]"
   published_at: "[timestamp]"
   confluence_version: [version number]
   ```

3. **Log the publication** for future reference.

---

## Re-Publishing (Update Flow)

If the vault file already has `confluence_page_id` in its frontmatter:

```
This document was previously published to Confluence:
  URL: [confluence_url]
  Last published: [published_at]

Would you like to:
a) Update the existing Confluence page (increment version)
b) Create a new page (separate copy)
c) Cancel
```

---

## Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| Confluence not active | Stop and inform user; suggest alternative platforms |
| Confluence API fails | Save the converted XHTML to a file so user can manually paste it |
| Authentication failure | Inform user their Confluence credentials may need refreshing |
| Page already exists (same title) | Ask user: update existing, create with different title, or cancel |
| Very large document | Warn user about page size; suggest splitting into child pages |
| Complex markdown (unsupported elements) | Convert best-effort, warn about any elements that couldn't be converted |

## Error Handling

- **API 403 (Forbidden)**: User may lack write permissions to the target space
- **API 404 (Not Found)**: Space key or parent page ID may be incorrect
- **API 409 (Conflict)**: Page was modified by someone else; fetch latest version and retry
- **Conversion failures**: Fall back to plain text for elements that can't be converted
- **Rate limits**: Retry with backoff
- **Network errors**: Save converted content locally so no work is lost
