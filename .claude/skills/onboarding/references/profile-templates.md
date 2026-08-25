# Profile document templates

Verbatim markdown templates for the four documents created in onboarding Step 6 (Generate Profile Documents). Fill in the bracketed placeholders when generating each file.

## `00-inbox/MY-PROFILE.md`

```markdown
---
type: profile
created: YYYY-MM-DD
onboarding_completed: true
role_pack: [matched role_id or "custom"]
agent_mode: [solo or team, based on role pack suggestion]
verification_harness: off
tags: ["#profile", "#config", "#cog"]
---

# My COG Profile

## About Me
- **Name**: [Name]
- **Role**: [Job/role/main activity]
- **Role Pack**: [Display name from matched role pack, or "Custom" if no match]
- **Profile Created**: [Date]

## Settings
- **Agent Mode**: [solo/team] *(solo = handle everything directly; team = delegate to specialist sub-agents for deeper results)*
- **Verification Harness**: off *(off = the V-model harness runs only when you ask for it, e.g. `/closed-loop`; on = build tasks default to the `normal`-lane pipeline)*

## Active Projects
[If they mentioned projects:]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 1]]
- [[04-projects/[slug]/PROJECT-OVERVIEW|Project Name 2]]

[If no projects:]
*No active projects yet. Add them anytime by editing this file or running onboarding again.*

## Related
- [[MY-INTERESTS|My Interests & News Sources]]
- [[03-professional/COMPETITIVE-WATCHLIST|Competitive Watchlist]] *(if applicable)*

## Notes
*Feel free to add notes here about your COG usage, preferences, or anything else.*

---

*Edit this file anytime to update your profile. COG reads it when you use skills.*
```

## `00-inbox/MY-INTERESTS.md`

```markdown
---
type: interests
created: YYYY-MM-DD
tags: ["#interests", "#daily-brief", "#config"]
---

# My Interests & News Sources

*These topics guide my daily intelligence briefings.*

## Topics I'm Interested In
- [Topic 1]
- [Topic 2]
- [Topic 3]
- [Topic 4]
- [Topic 5]

## Preferred News Sources
[If sources were mentioned:]
*Where I like to get information:*
- [Source 1]
- [Source 2]
- [Source 3]

[If no sources mentioned:]
*No specific sources set. COG will search broadly for your topics. Add preferred sources here anytime.*

## Notes
*Add any additional context about your interests here.*

---

*Update this file anytime as your interests evolve. Just edit and save—COG will pick up the changes.*
```

## `03-professional/COMPETITIVE-WATCHLIST.md` (only if they mentioned companies/people to track)

```markdown
---
type: competitive-intelligence
created: YYYY-MM-DD
tags: ["#competitive", "#intelligence", "#tracking"]
---

# Competitive Watchlist

*Companies, people, or organizations I'm keeping an eye on.*

## Watching
- [Company/Person 1]
- [Company/Person 2]
- [Company/Person 3]

## Why I'm Tracking Them
*Add context here about why these matter to you or your projects.*

---

*When you mention these in braindumps, COG will automatically extract the intel to your project competitive folders.*
```

## For Each Project: `04-projects/[project-slug]/PROJECT-OVERVIEW.md`

```markdown
---
type: project-overview
project: [project-name]
slug: [project-slug]
created: YYYY-MM-DD
status: active
tags: ["#project", "#overview"]
---

# [Project Name]

## What is this project?
[Brief description - leave for user to fill in]

## Current Status
*What phase are you in? What's happening now?*

## Project Resources
- [[braindumps/|Project Braindumps]]
- [[competitive/|Competitive Intelligence]]
- [[content/|Content & Assets]]
- [[planning/|Planning Documents]]

## Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]

---

*This overview helps COG organize your project-related thoughts and updates.*
```
