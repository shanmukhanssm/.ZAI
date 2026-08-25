# Agent Prompt Review Checklist

Derived from Feng Liu's 10-point checklist. Run this against every generated agent prompt. Each item has a WHY so you understand the reasoning, not just the rule.

## Structure

- [ ] **Identity is at the very top** (first section after pre-declaration). Reason: primacy effect — the model internalizes role before processing anything else.
- [ ] **Safety constraints marked with `IMPORTANT:` prefix.** Reason: `IMPORTANT:` tokens are weighted ~2-3x higher by RLHF training — unmarked rules have less compliance.
- [ ] **Safety constraints repeated at the end** (recency reinforcement). Reason: U-shaped attention means model forgets middle content; repeating at the end refreshes the rules.
- [ ] **Clear section separation with `##` headers.** Reason: structured markdown headers get more weight than prose — the model recognizes hierarchy.
- [ ] **Examples wrapped in `<example>` tags.** Reason: without explicit tags, the model may confuse examples with instructions.
- [ ] **`<system-reminder>` tags pre-declared.** Reason: without pre-declaration, the model treats injected reminders as user speech and tries to respond to them.

## Token Budget

- [ ] **Agent prompt < 6,000 tokens** (Feng Liu's guideline). Reason: context degradation starts at 80K tokens — keeping your part lean leaves room for conversation history.
- [ ] **Not repeating information that tool definitions already cover.** Reason: tool definitions are ~11K tokens; repeating them in your prompt wastes budget and adds zero new information.
- [ ] **Domain knowledge uses pointers, not dumps** (on-demand loading). Reason: a full API doc dump burns tokens upfront for information the model may never need.
- [ ] **No verbose lore, backstory, or character development.** Reason: the model doesn't perform better with a detailed origin story — it just needs role + constraints.

## Rule Quality

- [ ] **Every rule is true/false testable.** Reason: "be professional" is subjective and the model will guess. "Do NOT use emojis" is unambiguous.
- [ ] **Hard constraints use absolute language** (`NEVER` / `MUST NOT`). Reason: soft language like "please avoid" is treated as optional by the model.
- [ ] **Soft constraints use recommendation language** (`recommended` / `prefer`). Reason: over-constraining with `NEVER` on everything makes the model brittle — reserve absolutes for safety.
- [ ] **Critical rules explain WHY, not just WHAT.** Reason: a reasoned instruction lets the model adapt to edge cases; a bare imperative breaks on the first deviation.
- [ ] **Bidirectional constraints:** "do X instead of Y" not just "don't do Y". Reason: telling the model what NOT to do without alternatives leaves it guessing.
- [ ] **Both positive and negative examples provided** where applicable. Reason: negative examples prevent specific failure modes that positive examples alone don't address.

## Agent Behavior

- [ ] **Principles given, not rigid step-by-step procedures.** Reason: procedures break on unexpected inputs; principles let the model adapt.
- [ ] **Handles "tool call denied" scenario** (don't brute-force retry). Reason: without this guidance, the model retries the exact same denied call in an infinite loop.
- [ ] **Handles obstacles** (think why it failed, adjust approach). Reason: the model's default behavior on failure is to retry — it needs explicit permission to change strategy.
- [ ] **Context management strategy in place** (summarization threshold or reminder injection). Reason: adherence degrades past 80K tokens — without a refresh strategy, the agent forgets early instructions.

## What NOT to Do

- [ ] **No flattery or superlative adjectives.** Reason: compliments don't improve output quality — they waste tokens.
- [ ] **No redundant "you are a helpful AI" declarations.** Reason: every model already knows it's an AI. Repeating this crowds out useful instructions.
- [ ] **Not written as a prompt chain.** Reason: prompt chains freeze on unexpected input. Agents need adaptive behavior, not fixed pipelines.
- [ ] **No over-engineering** (features nobody asked for). Reason: every additional rule costs tokens and adds constraints the model must navigate — only include what the agent actually needs.
