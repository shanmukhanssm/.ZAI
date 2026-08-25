# exa-research - Known Gotchas

## 1. Topic Too Broad

**Symptom:** Every subagent returns findings on completely different sub-topics with zero overlap. No consensus findings emerge.

**Cause:** The topic is too broad (e.g., "AI", "science", "technology"). Each angle queries a different sub-area and nothing connects.

**Fix:** Before dispatching, ask the user to narrow to a specific domain, timeframe, or aspect. If the user says "just do it anyway", accept but note in the summary that results will be shallow.

## 2. Subagent Hallucinates Sources

**Symptom:** A subagent reports URLs with suspicious domains (unknown .xyz, .top, .click), future dates in the path, or article titles that do not match the claimed finding.

**Cause:** LLMs are prone to fabricating citations when asked to "find sources" without concrete search results. This is the most common failure mode in research agents.

**Fix:** During synthesis, critically examine every URL. If a domain is unfamiliar, run a sanity check: does the domain look like a known publisher? Is the URL path realistic? Flag suspicious URLs as `[unverified source]` in the output. Do NOT pass fabricated citations through.

## 3. High Context Consumption from Parallel Agents

**Symptom:** After 6 subagents return, the conversation context is heavily consumed by research reports, leaving little room for synthesis.

**Cause:** 6 agents each returning 500+ words of structured output means 3000+ words of reports before synthesis even begins.

**Fix:**
- Keep subagent prompts under 500 tokens (excluding the query list)
- Ask subagents to return ONLY findings, not methodology explanations
- Do NOT include the full subagent report in the synthesis — extract key data points
- If context is critically low, present a condensed summary instead of the full template

## 4. Hidden Gems Are Actually Noise

**Symptom:** A finding flagged as "hidden gem" turns out to be incorrect, irrelevant, or from a low-quality source.

**Cause:** Uniqueness does not equal quality. A finding that only appeared in 1 agent could be unique because it is wrong, not because it is valuable.

**Fix:** Apply judgement during synthesis:
- Check the source credibility before labeling it a hidden gem
- If the finding contradicts well-established consensus without strong evidence, flag it as "low confidence hidden gem"
- If the finding is from a forum or anonymous source, note the source type
- The "Why it matters" field must justify value, not just describe uniqueness

## 5. Deepening Loops

**Symptom:** After the first deepening iteration, new gaps are found, creating pressure to deepen again, leading to infinite recursion.

**Cause:** Every research topic can generate gaps indefinitely. "The meaning of life" could keep producing new angles forever.

**Fix:** Hard cap at 1 deepening iteration. If coverage is still poor after 1 iteration, report "Gaps remain despite targeted deepening" and stop. The user can manually request more depth.

## 6. Topic Does Not Need Multi-Angle Research

**Symptom:** All 6 angles return essentially the same information. The Negation angle returns nothing. The Semantic angle finds no conceptual connections.

**Cause:** Some topics are purely factual or procedural (e.g., "how to center a div", "what is the capital of France"). These do not have hidden angles worth exploring.

**Fix:** If after Step 2 (angle generation) it is clear the topic is purely factual:
- Skip to a 2-angle approach: Direct + Niche
- Note to the user: "This topic is primarily factual. Using a reduced 2-angle approach."
- If even Niche returns nothing useful, just do Direct and present results simply

## 7. Web Search Rate Limiting

**Symptom:** Subagents report search failures or truncated results due to rate limiting.

**Cause:** Each subagent doing 6-10 queries hits the search provider's rate limits, especially if multiple agents run simultaneously.

**Fix:** The subagent prompt already instructs batching. If rate limits persist:
- Reduce queries per agent to 4-6 instead of 6-10
- If a subagent reports rate limiting, note it as a gap: "Rate limited — some angles may be incomplete"
- Do NOT retry indefinitely — wasted context

## 8. Source Quality Variation Across Angles

**Symptom:** Direct and Emerging angles return high-quality sources (.com, .org, .edu), while Niche angle returns forum posts and social media.

**Cause:** Different angles inherently find different quality tiers. That is by design, but it creates a synthesis challenge.

**Fix:** When synthesizing, note the quality tier of each source. A hidden gem from a forum can still be valuable, but flag it: "Hidden gem from Reddit community — anecdotal, not authoritative." Do NOT mix quality tiers without comment.
