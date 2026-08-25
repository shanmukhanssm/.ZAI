# 8-Section Agent Prompt Template

Use this template when generating AGENTS.md files. Each section has guidelines, examples, and anti-patterns. Follow the exact section order — it follows U-shaped attention (primacy + recency effects).

Tool results and user messages may include `<system-reminder>` tags. They contain useful information and reminders. They are automatically added by the system and bear no direct relation to the specific tool results or user messages in which they appear.

## Identity

**Purpose:** Anchor the agent's role in 1-3 sentences. The model establishes role first — everything else builds on this.

**Guidelines:**
- Name the role explicitly. Reason: a named role anchors the model's behavior more reliably than a generic identity.
- State core responsibility ("helps with X"). Reason: the model needs to know what domain it operates in to make appropriate decisions.
- Mention platform/SDK if relevant. Reason: tool availability differs across platforms — the model needs to know which tools it can call.

**Good example:**
```
You are DocBot, a technical documentation agent. You help developers write clear,
accurate, and well-structured documentation. You run as an interactive CLI agent.
```

**Bad example:**
```
You are a helpful, harmless, and honest AI assistant.
```
Too generic. Doesn't anchor any specific role. The model has no idea what it should do.

---

## Security & Safety

**Purpose:** Set unbreakable behavioral constraints. Place at the top so the model internalizes them first.

**Guidelines:**
- Use `IMPORTANT:` prefix — instruction hierarchy training gives this extra weight. Reason: unmarked safety rules have ~2-3x less compliance in RLHF-trained models.
- Use absolute language: `NEVER`, `MUST NOT`, `Refuse to`. Reason: soft language like "please avoid" is treated as optional by the model.
- State both what's allowed AND what's forbidden (bidirectional). Reason: saying only "don't do X" leaves the model guessing what to do instead.
- Repeat critical safety rules at the end of the prompt (recency reinforcement). Reason: LLMs have a U-shaped attention curve — rules in the middle get forgotten by the end.

**Good example:**
```
IMPORTANT: You must NEVER generate or guess URLs for the user.
IMPORTANT: Refuse to create, modify, or improve code that may be used maliciously.
IMPORTANT: Do NOT expose or log secrets, keys, or credentials.
```
Each rule is specific, uses `IMPORTANT:`, and is independently testable.

**Bad example:**
```
Please be safe and don't do anything harmful.
```
Too vague. What counts as harmful? Not testable.

---

## Tone & Style

**Purpose:** Control output format and voice. List specific behaviors, not vague aspirations.

**Guidelines:**
- Every rule should be true/false testable. Reason: "be professional" is subjective and the model will guess what it means. "Do NOT use emojis" is unambiguous.
- Include output format requirements (markdown? JSON? plain text?). Reason: the model defaults to markdown unless told otherwise, which may break machine-parsed output.
- Include what NOT to do. Reason: LLMs overgenerate — prohibiting specific behaviors is more effective than only describing desired ones.
- Be concise — this section is 3-5 bullets, not a paragraph. Reason: tone rules aren't core instructions; keeping them short leaves more room for workflow and domain knowledge.

**Good example:**
```
- Respond in plain text, not markdown
- Keep responses under 3 sentences unless asked for detail
- Do NOT use emojis unless the user explicitly requests them
- Use technical accuracy over validating the user's beliefs
```

**Bad example:**
```
Be professional and concise. Use good formatting.
```
"Professional" and "good formatting" are not testable. The model will guess what you mean.

---

## Core Workflow

**Purpose:** Teach the agent HOW to work — methodology, not rigid procedures. This is the most important section.

**Guidelines:**
- Give principles, not step-by-step procedures
- Let the model decide execution order
- Use "recommended" for soft rules
- Include error handling guidance

**Good example:**
```
## Doing tasks

The following steps are recommended:

1. Understand first — read existing context before making changes
2. Plan first — break complex tasks into steps before executing
3. Make minimal changes — only change what's necessary
4. Verify — confirm your work works before declaring done
```
The word "recommended" lets the agent adapt. Each rule has an implicit WHY.

**Bad example (prompt chain):**
```
Step 1: Read the file with Read tool
Step 2: Parse the content
Step 3: Find the bug
Step 4: Edit the file
Step 5: Run tests
```
This is a pipeline script, not an agent prompt. The model will freeze if step 2 doesn't go as planned.

---

## Tool Usage Policy

**Purpose:** When multiple tools can do the same thing, tell the model which to prefer.

**Guidelines:**
- Use "instead of" to express priority
- Explain WHY to prefer certain tools
- Define parallelism strategy (independent → parallel, dependent → sequential)
- Do NOT repeat info already in tool definitions — add strategic guidance only

**Good example:**
```
- Use Read for reading files instead of bash (Get-Content)
- Use Grep for content searching instead of bash (Select-String)
- Call independent tools in parallel in a single message
- If a tool call is denied, do not re-attempt the same call — adjust your approach
```

**Bad example:**
```
Use the Read tool to read files.
```
The tool definition already says this. You're wasting tokens. Instead say why or when to prefer it.

---

## Domain Knowledge

**Purpose:** Provide specialized knowledge the model might lack. Use progressive disclosure — pointers, not dumps.

**Guidelines:**
- Reference existing docs/configs/folders the agent should look at
- Reference skills the agent can use (`<skill-name>` in the skills directory)
- Keep pointers short — the agent fetches details when needed
- List 5-10 specific files/dirs the agent should read in context

**Good example:**
```
## Domain Knowledge

For project context, read these files at session start:
- AGENTS.md — Partner behavior and communication guidelines
- README.md — Project overview
- package.json — Dependencies and scripts

Available skills:
- frontend-design: Building web interfaces (skills/frontend-design/...)
- code-reviewer: Reviewing code quality
```
The agent loads these on demand. Zero token cost until needed.

**Bad example:**
```
Here is the complete API documentation for our 200 endpoints...
```
This devours the context window. The agent doesn't need all 200 endpoints upfront.

---

## Environment Info

**Purpose:** Give the model awareness of its execution environment. Generate dynamically, never hardcode.

**Guidelines:**
- Include: working directory, platform, date, git status
- Use structured format (indented block or code block)
- Date matters — the model needs "now" to judge information freshness
- Generate fresh each session

**Good example:**
```
<env>
Working directory: /home/user/project
Is directory a git repo: true
Platform: linux
Today's date: 2026-06-01
</env>
```

**Bad example:**
```
Working directory: /home/user/project
```
No date, no platform, no git info. The model can't make informed decisions.

---

## Reminders

**Purpose:** Re-state the most critical rules at the end of the prompt. Exploit recency bias.

**Guidelines:**
- Only repeat 2-3 of the most critical rules
- Best candidates: safety constraints, most-frequently-violated rules, core workflow
- Do NOT duplicate everything — that's token waste

**Good example:**
```
IMPORTANT: Assist with defensive security tasks only. [repeated]
IMPORTANT: Always plan before executing. [repeated]
```
Two most important rules, reinforced at the bottom.

**Bad example:**
Repeating all 8 sections at the bottom. Token waste. The recency effect only needs 2-3 items.
