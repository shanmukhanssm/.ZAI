# Anti-Pattern Example: What NOT to do

This is a deliberately broken agent prompt showing common mistakes. Each flaw is annotated with what's wrong and why it matters. Compare against the working examples to see the difference.

---

# AGENTS.md — Helper

~~❌ FLAW 1: Generic identity. "Helper" says nothing about what this agent does. The model has no role to anchor behavior.~~
~~❌ FLAW 2: No system-reminder pre-declaration. Mid-conversation injection won't work — the model may try to respond to reminders as if they're user speech.~~

You are a helpful AI assistant.

~~❌ FLAW 3: No IMPORTANT markers. Safety rules have no extra weight.~~
~~❌ FLAW 4: Rules are vague, not testable.~~

Please be safe and don't do anything harmful.

~~❌ FLAW 5: Tone rules are not testable. "Be professional" is subjective. Model will guess.~~

Be professional and use good formatting.

~~❌ FLAW 6: Prompt chain — rigid step-by-step procedure instead of principles.~~
~~❌ FLAW 7: No error handling guidance. If a step fails, the model doesn't know what to do.~~
~~❌ FLAW 8: No "tool call denied" scenario. Model will retry the same call infinitely.~~

## Instructions

Step 1: Read the file
Step 2: Find the problem
Step 3: Fix it
Step 4: Save the file

~~❌ FLAW 9: Just repeats what the tool definition already says. Wasted tokens.~~
~~❌ FLAW 10: No "instead of" — model might use bash.~~

Use the Read tool.
Use the Write tool.

~~❌ FLAW 11: Knowledge dump — 50 lines of API docs inline.~~
~~❌ FLAW 12: No progressive disclosure. All tokens consumed upfront for rarely-needed info.~~

Here is the complete API documentation:
- Endpoint 1: GET /api/users — returns user list
- Endpoint 2: POST /api/users — creates a user
- ... (48 more lines)

~~❌ FLAW 13: No environment info. Model doesn't know the date, platform, or working directory.~~
~~❌ FLAW 14: No reminders. Safety rules from the top are forgotten by the end due to recency effect.~~

---

## Summary of Flaws

| # | Flaw | Why It Matters | Fix |
|---|---|---|---|
| 1 | Generic identity | Model has no role anchor | Name the role and core purpose in 1-3 sentences |
| 2 | No system-reminder pre-declaration | Model treats injected reminders as user speech | Add pre-declaration line at the top |
| 3 | No IMPORTANT markers | Safety rules have no extra weight | Prefix hard constraints with `IMPORTANT:` |
| 4 | Vague safety rules | Not testable, model ignores | Make every rule true/false testable |
| 5 | Subjective tone rules | "Professional" is undefined | Use concrete: "Do NOT use emojis unless asked" |
| 6 | Prompt chain | Model executes mechanically, freezes on unexpected input | Give principles, not steps |
| 7 | No error handling | Model retries forever or silently gives up | Include "if X fails, do Y" |
| 8 | No tool call denied handling | Model re-attempts the same denied call | Add "don't retry — adjust approach" |
| 9 | Redundant tool instructions | Wastes tokens repeating tool definitions | Only add strategic guidance |
| 10 | No bidirectional constraints | Model doesn't know what to use instead | "Read instead of bash" not just "use Read" |
| 11 | Knowledge dump | Devours context window | Use pointers for on-demand loading |
| 12 | No progressive disclosure | All tokens consumed at session start | Split detailed content into reference files |
| 13 | No environment info | Model guesses platform, date, paths | Include `<env>` block with runtime context |
| 14 | No reminders | Safety rules forgotten (recency effect) | Repeat 2-3 critical rules at the bottom |
