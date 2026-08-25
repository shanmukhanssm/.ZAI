---
name: exa-research
description: >-
  Deep multi-angle research that finds both obvious and HIDDEN information
  using parallel subagent dispatch — inspired by Exa.ai's semantic discovery
  approach. Dispatches 4-6 parallel research agents each covering a distinct
  angle, cross-references all findings, and surfaces non-obvious gems that
  standard search misses. Trigger: "exa research", "deep research",
  "hidden gems", "find hidden information", "comprehensive research",
  "multi-angle research", "research deeply", "thorough research",
  "discover everything about", "uncover hidden".
  Do NOT use for: simple fact lookups, quick web searches, single-query Q&A,
  code debugging, or checking documentation.
allowed-tools:
  - Read
  - Write
  - Task
  - Question
  - Todowrite
  - Glob
---

# exa-research

## Overview

This skill conducts deep, multi-angle web research inspired by Exa.ai's approach — finding **both obvious and hidden information** through parallel subagent dispatch and cross-agent synthesis.

**Why it works:** A single linear search only shows you one perspective — the top-ranked results for your specific query phrasing. Different angles uncover different parts of the landscape. Direct queries return popular/mainstream results. Niche queries surface community-backed insights. Negation queries reveal criticisms and limitations. Semantic queries find conceptually related content. Cross-referencing across angles tells you which findings are genuine consensus vs. hidden gems only visible from a specific angle.

**How it differs from the deep-researcher agent:** This skill dispatches **4-6 parallel subagents simultaneously** (not sequential searches), each with a dedicated angle and 6-10 queries. After synthesis, it auto-detects coverage gaps and can dispatch **deepening agents** if key subtopics are underexplored. Hidden gems are identified by cross-referencing findings across agents — a finding that appears in only 1-2 agent reports is a candidate hidden gem.

**Important:** This skill loads into a session with zero prior conversation history. Every instruction is written to be self-contained — do not assume any prior discussion, context, or user preferences. If something is unclear, use the Question tool to ask rather than guessing based on assumed context, because guessing with incomplete information produces wrong results that the user has to correct.

## Execution Checklist

- [ ] Topic is specific enough to research (if vague, asked narrowing questions)
- [ ] Generated 4-6 distinct research angles with 6-10 queries each
- [ ] Dispatched all angle subagents in parallel (single message, multiple Task calls)
- [ ] Cross-referenced findings across all agent reports
- [ ] Identified hidden gems (findings in 2 or fewer agent reports)
- [ ] Checked coverage — dispatched deepening agents if gaps found
- [ ] Presented summary with hidden gems section
- [ ] Offered full report generation

## Step Type Legend

Every step in this workflow is tagged with its execution mode:
- `[EXACT]` — Follow literally. Do not modify the procedure.
- `[GUIDED]` — Apply principles using your judgement. Use the template but adapt to context.
- `[QUESTION]` — Stop and ask the user before proceeding. Only continue after getting an answer.

These labels exist because different steps need different levels of precision. The subagent dispatch (EXACT) must not be modified or the parallel speed advantage is lost. The synthesis (GUIDED) needs judgement — no template can cover every possible research finding. The scope clarification (QUESTION) requires user input because guessing a narrow subtopic is worse than asking.

## Workflow

### Step 1: Clarify Scope [QUESTION — if needed]

If the user's topic is too broad, ask 1-2 targeted questions to narrow it. Aim for a topic that can be researched from multiple angles but is not "the entire field of X."

**Example:**
- User: "Research AI"
- You: "That is very broad. Which domain — AI regulation, model capabilities, business applications, or research breakthroughs? Any specific timeframe or depth level?"

If the topic is already specific, proceed immediately. Reason: a focused topic lets each angle generate deep, non-overlapping results rather than surface-level summaries.

### Step 2: Decompose Into 4-6 Angles [GUIDED]

Generate 4-6 research angles. Each angle is a distinct lens on the topic, because different angles reveal different slices of the information landscape. A finding that appears across multiple angles is likely consensus; a finding visible from only one angle is a candidate hidden gem. For each angle, generate 6-10 specific, searchable queries.

**Which angles to use:** Default to 6 angles for most topics. Drop to 4-5 if some angles genuinely do not apply (e.g., "Negation" is irrelevant for a purely factual topic). Drop to 2 (Direct + Niche) only for purely factual questions where multi-angle complexity is wasted. See Gotcha 6.

**The Standard Angles:**

| # | Angle | Purpose | Query Style |
|---|-------|---------|-------------|
| 1 | **Direct** | Mainstream understanding, top results | "[topic] overview", "[topic] guide", "what is [topic]" |
| 2 | **Alternative** | Different approaches, competitors, ecosystems | "[topic] alternatives", "other than [topic]", "[topic] vs" |
| 3 | **Negation** | Limitations, downsides, counter-arguments | "[topic] limitations", "[topic] criticism", "[topic] drawbacks" |
| 4 | **Niche** | Forums, obscure sources, underground knowledge | "[topic] reddit", "[topic] forum", "[topic] github" |
| 5 | **Emerging** | Latest developments, trends, predictions | "[topic] 2026 new", "[topic] future", "latest [topic]" |
| 6 | **Semantic** | Conceptually related, non-obvious connections | Think: "what is similar to [topic] but not obviously connected" |

**Adaptation rule:** If a topic genuinely does not fit an angle, merge it with another rather than forcing bad queries. Minimum 4 angles, maximum 6.

**Example: Angles for "Rust programming language"**
1. Direct: "Rust programming guide 2026", "Rust features overview", "Rust vs C++ performance"
2. Alternative: "Rust alternatives Go Zig", "Rust vs Go microservices", "when not to use Rust"
3. Negation: "Rust problems", "Rust compilation time", "Rust complexity complaints"
4. Niche: "Rust reddit learning resources", "Rust github trending projects", "Rust production horror stories"
5. Emerging: "Rust 2026 edition features", "Rust new projects", "Rust in embedded systems latest"
6. Semantic: "systems programming languages momentum 2026", "memory safe languages comparison"

### Step 3: Dispatch Parallel Subagents [EXACT]

For each angle, dispatch a **general** subagent via Task tool with a structured prompt. **Dispatch ALL agents in a single message** (multiple parallel Task calls) to minimize wall-clock time, because sequential dispatch would multiply the total latency by the number of angles (4-6x slower). Since the subagent receives this prompt with zero prior conversation history, every instruction must be fully specified within the prompt — do not assume the subagent knows anything about the topic or the research framework.

**Wait for all subagents to complete before proceeding.** Do not move to Step 4 until every agent has returned or timed out. If a subagent fails, times out, or returns an unparseable report, note the specific angle as a gap and proceed with the remaining agents — do not redispatch, because the re-dispatch would add another full round of latency and the marginal return from one angle is not worth the wall-clock cost. Document the failure in **Gaps Identified** in the final output.

**Subagent failure and rate limiting:** Web search rate limits are common (see Gotcha 7 in references/gotchas.md). If multiple agents hit rate limits simultaneously, the subagent prompt already instructs batching. If rate limits persist, you will see empty or truncated reports — document these as gaps rather than retrying.

**Subagent prompt template:**

```
You are a focused research subagent for "exa-research".
Your specific mission is to research [TOPIC] from the angle of: [ANGLE NAME]

=== YOUR ANGLE ===
[Angle description]

=== QUERIES TO EXECUTE ===
Execute these queries using WebSearch:
1. [query 1]
2. [query 2]
... (6-10 queries)

=== INSTRUCTIONS ===
1. Execute ALL queries. Batch independent queries in parallel.
2. For promising URLs, WebFetch the most relevant to get full content.
3. Cross-reference findings across your queries.
4. Do NOT fabricate sources. Flag suspicious URLs.
5. If a query returns nothing useful, report it as a dead end.

=== OUTPUT FORMAT (return EXACTLY this structure) ===

===SUBAGENT_REPORT===
ANGLE: [angle name]

TOP_FINDINGS:
- [Finding 1] (confidence: HIGH/MEDIUM/LOW) Source: [URL]

UNIQUE_INSIGHTS:
- [Insight 1] Source: [URL]

SOURCES_CONSULTED:
- [URL 1]

DEAD_ENDS:
- [Query that returned nothing]

KEY_QUOTES_OR_DATA:
- "[exact quote]" --- [URL]
===END_REPORT===
```

Use the "general" subagent type for all agents. Do NOT use "deep-researcher" as the subagent type. Reason: "deep-researcher" subagents run their own internal multi-query research loops, which conflict with exa-research's angle-specific dispatch. A deep-researcher given angle queries would ignore the angle constraint and run its own discovery process, producing overlapping redundant results instead of focused angle-specific findings. Use "general" to keep each subagent focused exclusively on its assigned queries.

### Step 4: Collect and Synthesize [GUIDED]

Once all subagents return results, cross-reference every finding. This cross-referencing is essential because findings from one angle can validate or contradict findings from another — a claim that appears across 3+ angles is much more reliable than one visible from only a single angle.

1. **Build a master list** of all findings from all agents
2. **Deduplicate** — merge findings that refer to the same thing
3. **Track agent coverage** — for each finding, note which agent(s) reported it
4. **Identify consensus** — findings reported by 3+ agents (these are mainstream)
5. **Identify hidden gems** — findings reported by 1-2 agents, especially from Niche, Semantic, or Negation angles that did NOT appear in Direct results

**Synthesis rules:**
- If 3+ agents independently found the same thing: HIGH confidence, label as "Consensus Finding"
- If only 1 agent found it: label as "Hidden Gem"
- If Direct and Negation agents disagree: report the contradiction explicitly
- If Niche agent found something no other agent found: HIGH priority hidden gem

### Step 5: Identify Hidden Gems [GUIDED]

This is the core differentiator from standard research. Explicitly surface findings that would be missed by a single-angle search. Hidden gems are valuable because they represent information that does not rank highly enough for mainstream discovery but still carries genuine insight — forum posts from domain experts, niche technical analyses, emerging trends before they hit mainstream coverage.

**Hidden Gem Criteria:**
- Finding appeared in only 1-2 agent reports
- Finding came from Niche, Semantic, or Negation angle (not Direct)
- Finding contradicts mainstream consensus
- Finding is from an obscure but credible source
- Finding represents an emerging trend not yet covered by mainstream sources

**Example output:**
```
=== HIDDEN GEMS ===
 Hidden Gem 1: [finding] --- Only appeared in Niche angle.
  Source: [URL]
  Why it matters: [why this finding is valuable]

 Hidden Gem 2: [finding] --- Only appeared in Semantic angle.
  Source: [URL]
  Why it matters: [why this finding is valuable]
```

### Step 6: Coverage Check and Deepening [EXACT]

Check if the synthesized findings adequately cover the topic:

- Are there obvious subtopics with ZERO findings?
- Did 2+ agents report the same gap?
- Did any agent return mostly dead ends?

If coverage gaps exist, dispatch 1-2 **deepening agents** (same Task pattern) with 3-5 targeted queries focused on the specific gap. Max 1 deepening iteration — do not recurse indefinitely. Reason: every topic can generate infinite deepening loops (e.g., "the history of X" can keep branching), and beyond one pass the marginal return on context spent drops sharply.

**Deepening prompt:**
```
You are a targeted deepening subagent. The main research on [TOPIC]
found insufficient coverage on: [SPECIFIC GAP]

Execute 3-5 highly targeted queries to fill this gap:
1. [query 1]
2. [query 2]

Return findings in the same ===SUBAGENT_REPORT=== format.
```

### Step 7: Quality Gate [EXACT]

Before presenting results, run these verification checks:

1. **Spot-check URLs.** Pick 3-5 URLs from the Key Sources list. Do the URLs resolve to real pages? Do the domains match known publishers? Flag any suspicious URLs with `[unverified source]`.

2. **Validate recency.** Check the dates on any time-sensitive claims. If a "latest development" cites a 2023 source, downgrade confidence and note the recency gap. Reason: this skill is used for current topics, and stale findings undermine the "hidden gems" value proposition.

3. **Check hidden gem quality.** Review each hidden gem: is it genuinely valuable or just noise? If a hidden gem is from a forum with 3 upvotes and no factual backing, flag it as "low confidence hidden gem."

4. **Confirm gap coverage.** If the user's original question had an obvious subtopic that is missing from all findings, skip deepening (already past Step 6) and note it: "Despite targeted deepening, [subtopic] remains uncovered."

Present results only after these checks pass.

### Step 8: Present Results [GUIDED]

Present a structured summary to the user using the summary template from `references/templates.md`. Read it from the file rather than inlining — keeps a single source of truth. The summary template covers: consensus findings, hidden gems, contradictions, gaps, and key sources.

**Expected timing:** For 4-6 parallel agents with 6-10 queries each, expect 2-5 minutes total depending on search latency and rate limits. The first run is the slowest because all agents run in parallel; subsequent runs use cached results for previously visited pages.

### Step 9: Generate Full Report [on user request]

If user says "generate report", "full report", or "save report":

1. Read the report template from `references/templates.md`
2. Expand the summary into the full template structure
3. Write the file: `exa-research-[topic-slug].md` in the current working directory
4. Confirm to the user: "Full report saved to [path]"

## Examples

**Example 1: Complete walkthrough for "exa research how Exa.ai works"**

**Step 1 — Clarify scope:** Topic is already specific enough ("Exa.ai technology"). Proceed.

**Step 2 — Generate 6 angles:**
```
1. DIRECT: "Exa.ai search engine how it works", "Exa AI neural search overview",
   "Exa vector database technology", "Exa embeddings search explained"
2. ALTERNATIVE: "Exa vs Google search comparison", "Exa vs Perplexity vs Tavily",
   "alternatives to Exa AI search", "traditional search vs neural search"
3. NEGATION: "Exa.ai limitations", "Exa search problems", "Exa index size criticism",
   "Exa pricing complaints developers"
4. NICHE: "Exa.ai hacker news discussion", "Exa reddit review", "Exa github issues",
   "Exa discord community", "Exa latent space podcast transcript"
5. EMERGING: "Exa new features 2026", "Exa funding series", "Exa product updates",
   "Exa instant search announcement"
6. SEMANTIC: "neural search engine future", "embedding based web search",
   "next link prediction search", "semantic retrieval for AI agents"
```

**Step 3 — Dispatch 6 parallel subagents with these queries.**

Each subagent returned a structured report. The Niche agent found a detailed blog post about "Canon" (Exa's search orchestrator) on their engineering blog — not surfaced by Direct queries. The Semantic agent found "exa-d" (their data processing framework) through conceptually related search on "web-scale vector databases."

**Step 4 — Synthesize across all 6 reports:**
- 3 agents (Direct, Alternative, Semantic) all returned "Exa uses embeddings for semantic search" → HIGH confidence consensus
- 2 agents (Direct, Emerging) returned "Exa raised $85M Series B at $2.2B valuation" → HIGH confidence
- Only Niche returned "Canon orchestrator" → Hidden Gem candidate
- Only Semantic returned "exa-d data framework" → Hidden Gem candidate
- Direct and Negation disagreed on pricing: Direct said "affordable API pricing," Negation found "cost scales steeply for production"

**Step 5 — Hidden gems identified:**
- Canon orchestrator (Niche angle): Exa built a DAG-based search pipeline system called Canon
- exa-d data framework (Semantic angle): Exa's petabyte-scale data processing on Lance+S3+Ray
- Latent Space podcast transcript (Niche): Deep CEO interview explaining Neural PageRank

**Step 6 — Coverage check:** Good coverage overall. Deepening not needed.

**Step 7 — Quality gate:** Spot-checked 4 URLs. One had a suspicious future date — flagged as unverified. All others resolved correctly.

**Step 8 — Summary presented:**
```
## Research: Exa.ai Technology

Angles explored: 6 (Direct, Alternative, Negation, Niche, Emerging, Semantic)
Subqueries executed: 42
Unique sources consulted: 31
Hidden gems found: 3

### Consensus Findings
1. Exa uses embeddings-based neural search instead of keyword indexing (HIGH)
2. Raised $85M Series B, valued at $2.2B (HIGH)
3. Used by Cursor, AWS, HubSpot for AI agent search (HIGH)

### Hidden Gems
 Hidden Gem: Canon search orchestrator — Exa's DAG-based pipeline
   Angle: Niche (engineering blog, not in mainstream coverage)
   Why matters: Reveals how Exa handles parallelism, caching,
   cancellation across search requests at scale

 Hidden Gem: exa-d data framework
   Angle: Semantic (conceptually related search on web-scale DBs)
   Why matters: Shows Exa built its own petabyte-scale data
   processing on Lance+S3+Ray — not off-the-shelf infra

 Hidden Gem: Neural PageRank explained (podcast transcript)
   Angle: Niche (Latent Space podcast, 55-min technical interview)
   Why matters: CEO explains link-prediction training objective

### Contradictions
- "Affordable API" (Direct) vs "Costs scale steeply in production" (Negation)

### Gaps
- Limited info on Exa's crawler architecture (only high-level details found)
- One URL flagged as unverified (future date in path)
```

**Step 9 — User said "generate report" → Read `references/templates.md`, expanded into full report, wrote `exa-research-exa-ai-technology.md`.**

**Example 2: Full end-to-end output for "hidden gems about carbon capture technology"**

After dispatching 5 subagents and synthesizing:

```
## Research: Carbon Capture Technology — Hidden Gems

**Angles explored:** 5 (Direct, Negation, Niche, Emerging, Semantic)
**Subqueries executed:** 35
**Unique sources consulted:** 28
**Hidden gems found:** 3

### Consensus Findings (reported by 3+ angles)
1. CCS (carbon capture and storage) is dominated by Climeworks,
   Carbon Engineering, and Global Thermostat (HIGH)
2. Cost remains the primary barrier at $50-200/ton CO2 (HIGH)
3. Most large-scale CCS projects are in oil and gas (HIGH)

### Hidden Gems (non-obvious findings)

 Hidden Gem 1: Direct Ocean Capture (DOC) startups
   Angle: Niche — a startup called Ebb Carbon is piloting
     electrochemical ocean alkalinity enhancement
   Why hidden: Mainstream CCS coverage ignores ocean-based methods.
     Only surfaced in ocean/climate niche forums.
   Source: ebbcarbon.com
   Why matters: Ocean-based capture has lower energy requirements
     than direct air capture and could scale faster.

 Hidden Gem 2: The "energy penalty" of CCS
   Angle: Negation — academic critiques show CCS can increase
     net emissions when powered by fossil fuels
   Why hidden: Most CCS coverage focuses on capture rates, not
     the full lifecycle energy cost.
   Source: [academic paper URL]
   Why matters: This contradicts the "CCS is always good" consensus.

 Hidden Gem 3: Methane capture vs CO2 capture convergence
   Angle: Semantic — several startups are now building combined
     methane + CO2 capture systems
   Why hidden: These are not marketed as "carbon capture" companies,
     so standard keyword search misses them entirely.
   Source: [startup URL]
   Why matters: Short-term climate impact of methane is 80x CO2 —
     combined capture addresses both problems.

### Contradictions Found
- "CCS is essential for climate goals" (Direct sources) vs "CCS
  prolongs fossil fuel dependence" (Negation sources)

### Gaps Identified
- Cost projections for ocean-based capture are absent from all sources
- Niche subagent rate-limited on 2 queries — some community data may
  be missing

### Key Sources
- ebbcarbon.com — Niche angle, ocean capture methodology
- [academic URL] — Negation angle, energy penalty analysis
- [startup URL] — Semantic angle, methane+capture convergence
```

## Known Gotchas

1. **Topic too broad produces shallow results.** Six angles on "AI" each return 10 different subtopics with no depth across any. MUST narrow first. Symptom: every agent returns findings on completely different sub-topics with zero overlap. Fix: ask user to narrow before dispatching.

2. **Subagents may hallucinate sources.** The Task prompt includes verification instructions, but subagents still occasionally fabricate URLs. During synthesis, scan each reported URL — if the domain looks suspicious (unknown .xyz, .top, future date), flag it as `[unverified source]`.

3. **Parallel dispatch consumes significant context.** 6 subagents each returning a report means large context usage. Keep subagent prompts tight (under 500 tokens each, excluding queries). Reference templates rather than inlining them.

4. **Hidden gems might just be noise.** A finding unique to 1 agent is not automatically valuable — it might be incorrect or irrelevant. Apply judgement during synthesis. If a "hidden gem" seems low-quality, note it as "low confidence hidden gem."

5. **Deepening can loop infinitely.** The max 1 iteration cap is critical. If after 1 deepening iteration coverage is still poor, report "gaps remain despite targeted deepening" rather than deepening again.

6. **Some topics lack non-obvious angles.** Factual topics (e.g., "how to center a div") do not benefit from 6-angle research. If the topic is purely factual, skip to a 2-angle approach (Direct + Niche) instead.
