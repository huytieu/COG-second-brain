---
name: auto-research
description: Deep strategic research engine — decomposes questions into parallel research threads, spawns multiple agents, and synthesizes into actionable strategic analysis
metadata:
  roles: product-manager,engineering-lead,founder,all
  keywords: research,auto-research,investigate,strategic analysis,deep dive
  display-name: COG Auto Research
---

# COG Auto Research Skill

## When to Invoke
- User asks a strategic question requiring deep research
- User says "research", "auto-research", "investigate", "strategic analysis", "deep dive into [topic]"
- User wants to understand market forces, competitive dynamics, technology trajectories, or strategic options
- User needs evidence-based analysis with real sources to support decision-making

Inspired by Karpathy's autoresearch — but for strategic thinking instead of ML training.

## Agent Mode Awareness

**Check `agent_mode` in `00-inbox/MY-PROFILE.md` frontmatter:**
- If `agent_mode: team` — use the full parallel agent execution strategy (5-7 agents). This skill benefits massively from team mode.
- If `agent_mode: solo` — run 2-3 sequential research passes with WebSearch/WebFetch, produce a lighter analysis without the full multi-thread structure.

## Command: `/auto-research`

## Input
The user provides a strategic question or topic as the command argument. Examples:
- "If foundation models commoditize, what happens to LLM wrapper companies like Katalon/Scout?"
- "Future of the testing industry as AI capabilities expand"
- "Should we build vs buy vs partner for our AI layer?"
- "What are the strategic options for Scout if OpenAI launches a testing product?"


## Execution Strategy

### Phase 1: Question Decomposition (Orchestrator — 2 minutes)

Break the user's strategic question into 5-7 **research threads** that together will provide a comprehensive answer. Each thread should be:
- **Independent** — can be researched in parallel
- **Specific** — has a clear research objective
- **Complementary** — together they cover the full strategic landscape

**Decomposition framework:**
1. **Market forces** — what macro trends drive this question?
2. **Historical precedent** — has this pattern played out before in other industries?
3. **Player analysis** — who are the key players and what are they doing?
4. **Technology trajectory** — where is the underlying tech heading?
5. **Customer behavior** — what do end-users actually want/do?
6. **Economic model** — what are the unit economics and value capture dynamics?
7. **Emerging tech & architectures** — what concepts, projects, or frameworks are still in development/discussion (pre-mainstream) that could be foundational? Research open-source projects, research papers, GitHub repos, Discord/forum discussions, conference talks, and early-stage tools that are relevant. Examples: novel agent architectures, new testing paradigms, experimental frameworks. These may not have polished docs — dig into READMEs, GitHub issues, Twitter/X threads, blog posts from builders, and academic preprints.
8. **Contrarian view** — what's the strongest argument against the consensus?

Not all threads apply to every question. Pick the 5-7 most relevant. **Thread 7 (Emerging tech) should ALWAYS be included** — the user specifically wants to stay ahead of concepts that aren't mainstream yet.

**Before spawning agents:**
1. Read relevant files from the vault for existing context:
   - `05-knowledge/` for existing frameworks and mental models
   - `04-projects/` for project-specific context if relevant
   - Recent braindumps for the user's existing thinking on this topic
2. State the decomposition to the user so they can course-correct before agents launch

### Phase 2: Parallel Deep Research (Spawn 5-7 Agents Simultaneously)

**CRITICAL: Launch ALL agents in a single message.** Use `run_in_background: true` for all agents.

Each agent gets a detailed prompt following this template:

```
You are a strategic research analyst investigating a specific thread of a larger strategic question.

MAIN QUESTION: [user's original question]
YOUR THREAD: [specific research thread]
EXISTING CONTEXT: [any relevant vault context]

RESEARCH METHODOLOGY:
1. WebSearch for 8-12 high-quality sources (prioritize: research reports, expert analyses, company filings, academic papers, industry publications — NOT listicles or superficial blog posts)
2. For each source found, WebFetch to read the full content and extract key arguments, data points, and frameworks
3. Look for CONFLICTING viewpoints — don't just confirm one narrative
4. Identify specific data points, statistics, and concrete examples
5. Note the credibility and potential bias of each source
6. FOR EMERGING TECH THREADS: Go beyond polished sources. Search GitHub repos (README, issues, discussions), Twitter/X threads from builders, Discord/forum discussions, conference talk summaries, arXiv preprints, and early blog posts. The goal is to surface concepts that are pre-mainstream but technically promising. For each concept found, assess: maturity level, technical approach, relevance to the user's use case, and what it would take to adopt/integrate.

OUTPUT FORMAT (return ALL of this):

## Thread: [thread name]

### Key Findings (3-5 bullet points)
- Finding with source attribution

### Evidence & Data Points
- Specific statistics, market data, examples with sources

### Expert/Notable Perspectives
- Named perspectives from credible voices

### Implications for [user's context]
- What this means specifically for the user's situation

### Confidence Level
- HIGH / MEDIUM / LOW with reasoning

### Sources
- Numbered list of actual URLs consulted
```

**Agent naming convention:** `research-[thread-slug]` (e.g., `research-market-forces`, `research-historical-precedent`)

### Phase 3: Synthesis (Orchestrator — after all agents complete)

Once all agents return, synthesize into a single strategic analysis document:

#### Document Structure:

```markdown
type: strategic-research
domain: [auto-detect from question]
date: YYYY-MM-DD
question: "[original question]"
threads: [list of research threads]
confidence: [overall confidence HIGH/MEDIUM/LOW]
tags:
  - auto-research
  - strategy
  - [topic tags]
status: complete

# [Strategic Question as Title]

## Executive Summary
3-5 sentences capturing the core insight. Lead with the answer, not the process.

## The Strategic Landscape
Synthesized view across all research threads. Not a thread-by-thread dump — weave findings together into a coherent narrative.

## Key Forces at Play
The 3-4 most important dynamics shaping this question, with evidence from multiple threads.

## Scenarios
### Scenario A: [Most Likely] — X% confidence
What happens, timeline, implications

### Scenario B: [Optimistic/Alternative]
What happens, timeline, implications

### Scenario C: [Worst Case/Disruption]
What happens, timeline, implications

## Emerging Tech & Architectures to Watch
Concepts, projects, and frameworks that are still in development/discussion but could be foundational. For each:
- **What it is:** One-paragraph explanation
- **Maturity:** Pre-alpha / Alpha / Early adoption / Growing community
- **Technical approach:** How it works architecturally
- **Relevance to our use case:** Why it matters for us specifically
- **Adoption path:** What it would take to integrate/adopt — effort, risks, dependencies
- **Key links:** GitHub repo, paper, discussion thread

## Strategic Options
For each option:
- **Description:** What this means concretely
- **Pros:** With evidence
- **Cons:** With evidence
- **Prerequisites:** What needs to be true
- **Timeline:** When to decide/act
- **Emerging tech leverage:** Which emerging concepts from above could strengthen this option

## Recommended Actions
Prioritized, concrete, time-bound action items. Not vague "consider X" — specific "do X by Y because Z."
Include a separate "Tech Bets" subsection: which emerging projects to start experimenting with now, even if they're not production-ready.

## Contrarian View
The strongest argument against the consensus/recommended path. What could make all of this wrong?

## Confidence & Gaps
- What we're confident about and why
- What we couldn't determine and what additional research would help
- Key assumptions that should be monitored

## Sources
Consolidated, deduplicated list of all sources across threads.
```

### Phase 4: Save & Deliver

1. Save the full analysis to `05-knowledge/research/YYYY-MM-DD-[slug].md`
2. If the analysis is long (>3000 words), also create a brief 1-page summary at `05-knowledge/research/YYYY-MM-DD-[slug]-summary.md`
3. Present the Executive Summary + Recommended Actions to the user directly in chat


## Quality Standards

- **No hallucinated sources.** Every claim must trace to a real WebSearch/WebFetch result.
- **Recency matters.** Prioritize sources from the last 6 months. Flag anything older.
- **Bias awareness.** Note when sources have obvious commercial incentives.
- **Specificity over generality.** "The testing tools market is $XX.XB and growing at YY% CAGR" beats "the market is growing."
- **Actionability.** The output should help the user make a decision, not just understand a topic.
- **Intellectual honesty.** If the research is inconclusive, say so. Don't manufacture false confidence.

## Example Decomposition

**Question:** "If generic LLM models get better over time, what's the future for LLM wrapper companies like Katalon or Scout?"

**Threads:**
1. **Foundation model trajectory** — How fast are GPT/Claude/Gemini improving at code understanding, test generation, bug detection? What's the capability curve?
2. **Historical precedent: platform commoditization** — What happened to companies built on top of AWS, iOS, Salesforce, etc. when the platform absorbed their features? Who survived and why?
3. **Testing industry structure** — Current market map, value chain, where margin lives, what buyers actually pay for
4. **Wrapper company strategies** — How are current AI wrapper companies (Jasper, Copy.ai, Cursor, etc.) adapting? What's working?
5. **Enterprise buying behavior** — Do enterprises buy "AI" or do they buy "solutions"? What's the procurement reality?
6. **Emerging tech & architectures** — What pre-mainstream concepts could reshape the landscape? (e.g., novel agent frameworks, new testing paradigms, computer-use agents, browser automation architectures). Search GitHub repos, arXiv, Twitter/X builder threads, Discord communities, conference talks.
7. **Defensibility analysis** — What moats exist for testing-specific AI companies? Data, workflow, integration, brand, switching costs?
8. **Contrarian: wrappers win** — Arguments for why vertical AI companies might actually INCREASE in value as models commoditize

## Runtime Expectations
- Phase 1: ~2 minutes (decomposition + user confirmation)
- Phase 2: ~5-10 minutes (parallel research, longest agent determines total time)
- Phase 3: ~3-5 minutes (synthesis)
- Total: ~10-15 minutes for a comprehensive strategic analysis

## Error Handling

- If a research thread returns low-quality results, note this in the synthesis rather than fabricating depth
- If WebSearch/WebFetch fails for a thread, retry once with alternative search terms, then document the gap
- The user may interrupt during Phase 2 to redirect or add threads
- The skill can be run multiple times on related questions — reference previous research files from `05-knowledge/research/`

## Fallback Behavior

This skill requires WebSearch and WebFetch tools. If these are unavailable:
- Fall back to vault-only analysis using existing `05-knowledge/` content
- Clearly state that no live web research was performed
- Recommend the user run the skill again when web tools are available
