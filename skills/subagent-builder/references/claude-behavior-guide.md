# Claude Behavior Guide

How Claude processes agent prompts — cache strategy, instruction hierarchy, and thinking tags. Use this when designing agent prompts to avoid common pitfalls.

## Prompt Cache Strategy

Claude supports prompt caching where the static prefix of your prompt is cached across requests. This saves 40-60% on input token costs in multi-turn conversations.

### How the 8-section ordering enables caching

The 8-section structure puts static content first and dynamic content last. This is deliberate:

```
Sections 1-7: Static (change rarely or never)  ← Cached
Section 8: Might repeat safety rules           ← Still mostly static
```

Anthropic's cache breakpoints can be set after:
1. The system prompt
2. Tool definitions
3. Project rules (AGENTS.md content)

**What this means for the generated agent:**
- Sections 1-7 (Identity through Environment Info) can be cached across invocations
- Only the user's actual message changes each turn — the prompt prefix stays cached
- If the agent needs dynamic values (date, git status), inject them in the Environment Info section via `<system-reminder>` tags, not by modifying the cached sections

## Instruction Hierarchy

Claude is trained with a priority stack for instructions:

| Priority | Source | Example |
|---|---|---|
| 1 (Highest) | User's explicit instructions | AGENTS.md, direct user requests |
| 2 | Custom system prompt additions | Skill instructions loaded at session start |
| 3 | Default system prompt | Platform's base instructions |
| 4 (Lowest) | Tool definitions | Read, Write, Bash, etc. |

**What this means:**
- AGENTS.md rules override skill instructions. If the user's AGENTS.md says something contradictory to your agent prompt, the AGENTS.md wins.
- `IMPORTANT:` markers are weighted ~2-3x higher than unmarked instructions by Claude's RLHF training. Use them sparingly — if everything is IMPORTANT, nothing is.
- Tool definitions are the lowest priority. Don't rely on tool descriptions to enforce behavioral rules.

### When to use IMPORTANT vs recommended

| Situation | Use | Example |
|---|---|---|
| Safety (irreversible harm) | `IMPORTANT:` + `NEVER` | "IMPORTANT: Never expose credentials." |
| Non-negotiable workflow | `IMPORTANT:` | "IMPORTANT: Plan before executing." |
| Preferred approach | `recommended` / `prefer` | "Prefer Read over bash for file access." |
| Style preference | plain instruction | "Use markdown for formatting." |

## Thinking Tag Policy

Claude 4 Sonnet and Opus produce internal reasoning inside `<thinking>` tags. This is invisible to the user but consumes tokens.

### What can go wrong

1. **Token waste on overthinking.** The agent might produce 2000 tokens of reasoning for a simple file read. This burns context budget and slows response time.

2. **Leakage into output.** If the agent isn't explicit about stripping thinking tags from responses meant for the user, reasoning can leak.

3. **Premature commitment.** The agent might commit to an approach in thinking and then refuse to reconsider even when new evidence appears.

### Guidelines for generated agents

Include these rules in the Core Workflow section of generated agents:

- Keep thinking concise. Use `<thinking>` for task planning and tradeoff analysis, not for narrating every tool call.
- Never include `<thinking>` content in responses shown to the user unless explicitly asked.
- If thinking reveals a mistake, change course — don't double down on the initial plan.
- If token usage is high, reduce thinking verbosity before reducing tool usage.

## Mid-Conversation Injection via system-reminder

`<system-reminder>` tags can be injected at any point in the conversation to remind the agent of critical rules or provide dynamic context.

### Pre-declaration (must be in the agent prompt)

```
Tool results and user messages may include <system-reminder> tags.
They contain useful information and reminders. They are automatically
added by the system and bear no direct relation to the specific tool
results or user messages in which they appear.
```

This tells Claude that reminder tags are system-injected, not user speech — so it doesn't try to respond to them as if a user said something.

### When to inject reminders

| Situation | Reminder content |
|---|---|
| Mode switching | "Plan mode is active. Do NOT execute or modify files." |
| Context refresh | "Remember to verify changes before declaring done." |
| Dynamic context | "Today's date: 2026-06-01. Current branch: main." |
| File change notification | "File X was modified externally. Account for this." |

### Frequency

Don't inject on every message — each tag costs tokens. Inject when:
- The conversation exceeds 80K tokens (adherence starts degrading)
- Switching between modes (e.g., plan → execute)
- Critical external context changes (file modified, branch switched)
