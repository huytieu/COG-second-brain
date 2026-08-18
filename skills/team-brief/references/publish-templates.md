# Team Brief — Publish Templates

Verbatim implementation snippets for publishing the brief: the HackMD bash pattern (Phase 3.7) and the two Phase 4 Slack message templates (Monday week-start vs. regular day).

## HackMD implementation pattern (Bash)
```bash
# Step 1: Create note
curl -s -X POST 'https://api.hackmd.io/v1/notes' \
  -H "Authorization: Bearer $HACKMD_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"...","readPermission":"owner","writePermission":"owner","commentPermission":"disabled","content":"placeholder"}'

# Step 2: Prepare payload and update
python3 -c "
import json
with open('[CUSTOMIZE: path/to/briefs/]daily-brief-YYYY-MM-DD.md') as f:
    content = f.read()
with open('/tmp/hackmd-payload.json', 'w') as f:
    json.dump({'content': content}, f)
"
curl -s -X PATCH "https://api.hackmd.io/v1/notes/<id>" \
  -H "Authorization: Bearer $HACKMD_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d @/tmp/hackmd-payload.json
```

## Slack message format — Monday (Week Start Brief)
```
:calendar: *Week Start Brief — [DATE] (covering Fri–Sun)*

*Weekend recap:* [X] PRs merged since Friday. [Brief summary of what got done.] :rocket:

*What shipped:*
• [Feature/PR 1 with <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> link] — [1-line description]
• [Feature/PR 2 with link] — [1-line description]
• [Feature/PR 3 with link] — [1-line description]

---

:rotating_light: *Heads up:*
• [Most important alert with PR links and context]
• [Second alert — include who's involved and what's needed]
• [Third alert if relevant]

---

:mag: *Key discussions from Slack:*
• *[Topic 1]:* [2-3 sentence summary of the discussion, decisions made, and any open questions.]
• *[Topic 2]:* [Summary with context]

:clipboard: *Open action items:*
• [Person] — [What they need to do] ([source: meeting/Slack thread])
• [Person] — [What they need to do]

---

:bar_chart: *Product pulse:*
• [X] visitors ([↑/↓X%]), [X] sign-ups, [X] core events ([↑/↓X%]) | [Any notable anomaly]

:chart_with_upwards_trend: *This week's focus:*
• [Key priority or theme for the week]

:zap: *Quick wins:*
• <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> and <...|#YYY> are approved — just need someone to merge.

:link: *Full brief:* [HACKMD_PUBLISH_LINK]
```

## Slack message format — regular days
```
:newspaper: *Daily Brief — [DATE]*

*What shipped:* [X] PRs merged. :rocket:
• [Feature/PR 1 with <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> link] — [1-line description]
• [Feature/PR 2 with link] — [1-line description]

---

:rotating_light: *Heads up:*
• [Alert 1 with PR links, context, and who needs to act]
• [Alert 2 with details]

---

:mag: *Key discussions:*
• *[Topic]:* [2-3 sentence summary — what was discussed, any decisions, open questions.]

:clipboard: *Action items:*
• [Person] — [Task] ([from meeting/Slack])

---

:bar_chart: *Product pulse:* [X] visitors ([↑/↓X%]) | [X] core events ([↑/↓X%]) | [Any notable anomaly]

:zap: *Quick wins:*
• <https://github.com/[CUSTOMIZE: your-org/your-repo]/pull/XXX|#XXX> and <...|#YYY> are approved — just need someone to merge.

:link: *Full brief:* [HACKMD_PUBLISH_LINK]
```
