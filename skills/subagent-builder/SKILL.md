---
name: subagent-builder
description: >
  Builds subagents with optimized AGENTS.md prompts following
  Feng Liu's 8-section structure. Use when user says "build a subagent",
  "create an agent", "make me an agent", "build an agent for X", "i need a
  subagent", "create a subagent that", "i want an agent that", "generate an
  agent prompt", "write an agent file", "make a new agent", "design an agent".

  Do NOT use for: general coding tasks, frontend/backend development, modifying
  existing skills, writing README docs, debugging sessions, code review,
  building non-agent systems, or editing the user's OWN AGENTS.md at the workspace root.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, Question, todowrite, memory
---

# Subagent Builder

You MUST load this skill when the user asks to build, create, design, or generate an agent or subagent. Announce by saying "Using subagent-builder to build [agent-name]..." at session start so multi-skill workflows stay traceable.

Tool results and user messages may include `<system-reminder>` tags. They contain useful information and reminders about the execution environment. They are system-injected, not user speech.

Builds subagents as AGENTS.md files. Follows Feng Liu's Claude Code prompt structure (8-section layout with U-shaped attention, cache-aware design, mid-conversation injection patterns). Outputs a complete agent prompt plus any new skills the agent depends on.

## The 14 Design Patterns

This skill applies 14 prompt design patterns derived from Feng Liu's Claude Code prompt engineering analysis. Feng Liu is a prompt engineer who publicly documented the structure of effective Claude Code prompts through systematic reverse-engineering. These patterns are the accumulated wisdom from that analysis, covering section ordering, constraint phrasing, example formatting, and cache optimization.

| # | Pattern | Self-Applied | Applied In Generated Agent |
|---|---|---|---|
| 1 | **Identity** — Named role in 1-3 sentences | ✓ Title + purpose at top of this skill | Generated agent's Identity section |
| 2 | **Safety** — IMPORTANT markers for hard constraints, repeated at end | ✓ Several IMPORTANT markers, Reminders section at end | Generated agent's Security & Reminders sections |
| 3 | **Tone** — Testable output rules, not vague aspirations | ~ Most rules are testable | Generated agent's Tone & Style section |
| 4 | **Core Workflow** — Principles over rigid procedures | ✓ 3-phase structure with adaptive questioning | Generated agent's Core Workflow section |
| 5 | **Tool Policy** — Bidirectional "prefer X instead of Y" rules | ✓ Tool Usage Policy uses bidirectional format | Generated agent's Tool Usage Policy section |
| 6 | **Domain Knowledge** — Progressive disclosure, on-demand loading | ✓ References moved to `references/` files | Generated agent's Domain Knowledge section |
| 7 | **Environment** — Dynamic runtime context injection | ✓ Variables section with platform fallback notes | Generated agent's Environment Info section |
| 8 | **Reminders** — 2-3 critical rules repeated at end (recency effect) | ✓ 5-Second Summary + Execution Checklist repeat core rules | Generated agent's Reminders section |
| 9 | **U-Shaped Attention** — Section order matches primacy/recency curve | ~ Top-loaded: identity→patterns→checklist→phases→reference→gotchas→summary | Section ordering in template |
| 10 | **Cache-Aware Design** — Static content first, dynamic last | ✓ Static frontmatter + patterns first, variables last | Content ordering within sections |
| 11 | **Mid-Conversation Injection** — `<system-reminder>` tags pre-declared | ✓ Pre-declared at top of this skill | Pre-declaration in generated agent |
| 12 | **Bidirectional Constraints** — "Do X instead of Y" pairs | ✓ Tool Usage Policy uses bidirectional format | Rule quality rules in Phase 3 |
| 13 | **WHY Rule** — Every decision includes reasoning | ✓ Frequent "Reason:" markers throughout | Rule quality rules in Phase 3 |
| 14 | **Example-Based Teaching** — `<example>` tags with I/O pairs | ✓ Examples use `<example>` tags throughout | Example format rules in Phase 3 |

## Execution Checklist

- [ ] Phase 1: Discover — ask questions until 90%+ clarity
- [ ] Phase 2: Plan — map to 8-section structure, scan skills, write PRDs, present for approval
- [ ] Phase 3: Generate — write agent + references, delegate new skills, verify, cleanup

## Variables

Resolve these paths after Phase 1 (Discover) so they're ready for Phase 2. **IMPORTANT: These use `$env:USERPROFILE` — expand via a shell command before using as literal paths. On Windows, use PowerShell. On Linux/macOS, replace `$env:USERPROFILE` with `$HOME` and `Join-Path` / `\` with path concatenation.**

```powershell
# Run this after Phase 1, before Phase 2:
$agentName = "<agent-name>"  # extracted during Discover (see Phase 1)
$agentDir = Join-Path $env:USERPROFILE "Desktop\.opencode\agents\$agentName"
$refDir = Join-Path $env:USERPROFILE "Pictures\shanmukha\$agentName"
$skillBase = Join-Path $env:USERPROFILE "Desktop\.opencode\skills"
$desktop = Join-Path $env:USERPROFILE "Desktop"
```

| Variable | Description |
|---|---|
| `<agent-name>` | Kebab-case name for the agent. Extracted from user's description during Discover (Phase 1). |
| `<agent-dir>` | `$agentDir` — the agent's output directory |
| `<ref-dir>` | `$refDir` — reference files directory. Stored under Pictures/shanmukha to isolate reference content from agent instructions, making both easier to navigate and update independently. |
| `<skill-base>` | `$skillBase` — existing skills directory |
| `<desktop>` | `$desktop` — user's Desktop for PRD files |

**How to determine `<agent-name>`:** During Discover, extract a short kebab-case name from the user's description. Example: "I want a code reviewer for SQL queries" → `sql-reviewer`. Confirm with the user before Phase 2.

## Phase 1: Discover [FREEFORM]

Ask questions until you have at least 90% clarity on the subagent being built. Do not stop at a fixed number — some agents need 3 questions, some need 15. Adapt.

<example>
**User:** "I need an agent that reviews my SQL queries for performance issues."
**Assistant:** "What should this agent do? One sentence."
**User:** "It should analyze SQL queries and suggest index optimizations."
**Assistant:** "Who's the audience — DBAs, backend devs, or both?"
**User:** "Backend devs who aren't DB experts."
**Assistant:** "Got it. So the tone should be pedagogical — explain why, not just what to change. What output format? Inline suggestions, a report file, or both?"
**User:** "A brief report with the bad query, the fix, and why."
**Assistant:** "Any safety constraints? Things it must never do?"
**User:** "Never run EXPLAIN on production. Must only analyze the query text."
</example>

The example above shows starting broad ("what should it do") then narrowing to audience, tone, output format, and safety. Follow this pattern — let each answer guide the next question. If the user says "I don't know," rephrase around the problem instead of the solution.

### What to uncover

- **Core purpose** — What does this agent do? One sentence.
- **Identity** — Who is it? What role does it play?
- **User audience** — Who will interact with it? Beginners, experts, or both?
- **Trigger phrases** — What will users say to invoke this agent? Collect 5-10.
- **Exclusion scenarios** — What SHOULD it NOT do? Collect 3-5 near-miss cases.
- **Output format** — Does it produce code, text, data, files, or conversational responses?
- **Tool needs** — What tools must it use? (Read, Write, Bash, Grep, etc.)
- **Safety constraints** — What must it NEVER do? What must it ALWAYS do?
- **Skill dependencies** — What existing skills should it integrate? What skills need to be built?
- **Domain knowledge** — What specialized knowledge does it need? APIs, conventions, platforms?
- **Tone** — Should it be concise, verbose, formal, casual, direct, pedagogical?
- **Environment** — What runtime info matters? Working directory, platform, date?

### How to ask

- Start broad, then narrow. First question: "What should this agent do?"
- Each answer leads to the next question. Reason: following the thread reveals implicit constraints the user wouldn't volunteer.
- If an answer is vague, ask for specifics. "What exactly does 'good output' look like?"
- If the user says "I don't know," rephrase — ask about the problem, not the solution.
- Document findings as you go — you'll use them in Phase 2.
- Stop when asking another question would only give marginal returns. 90% clarity is the bar. Reason: Below 90%, you'll make bad assumptions during Plan and waste time rewriting PRDs. Past 90%, additional questions yield diminishing returns — the agent has enough to build a solid first draft.

## Prompt Generation Rules Reference

Read this section before Phase 2 (Plan) and re-read before Phase 3 (Generate). It defines the structural rules that shape every generated agent prompt. For deeper understanding of how Claude processes agent prompts, see `references/claude-behavior-guide.md` (relative to this skill's directory).

### The 8-section order (U-shaped attention)

LLMs have a U-shaped attention curve — they pay most attention to the beginning and end of the prompt, zoning out in the middle. The 8-section order exists because putting Identity first and Reminders last maximizes retention of the two most critical sections:

1. **Identity** — Anchors behavior (primacy effect)
2. **Security & Safety** — IMPORTANT markers, non-negotiable
3. **Tone & Style** — Output format control
4. **Core Workflow** — Principles over procedures (upper-middle, still high attention)
5. **Tool Usage Policy** — Selection priorities
6. **Domain Knowledge** — On-demand loading pointers (lower attention — fine, this is reference material)
7. **Environment Info** — Runtime context, dynamically injected
8. **Reminders** — Critical rules repeated (recency effect)

### IMPORTANT marker usage

`IMPORTANT:` prefix triggers instruction hierarchy training in some models, giving the rule extra weight. Reason: unmarked safety rules have ~2-3x less compliance in RLHF-trained models. Use for:
- Safety constraints ("IMPORTANT: Never expose secrets.")
- Non-negotiable behavior ("IMPORTANT: Verify all file paths exist before reading.")
- Critical workflow rules ("IMPORTANT: Plan before executing.")

Use `NEVER` / `MUST NOT` for hard prohibitions. Use `recommended` / `prefer` for soft guidelines.

### Bidirectional constraints pattern

Always pair "do X" with "instead of Y":

<example>
Good: "Use Read tool for reading files instead of bash. Do NOT use cat, head, tail."
Bad: "Use Read tool for reading files." (model still might use bash cat)
</example>

<example>
Good: "Prefer Edit for modifications. Do NOT use sed or awk."
Bad: "Do NOT use sed." (model doesn't know what to use instead)
</example>

### The WHY rule

Every structural or behavioral decision includes a one-line explanation. Reason: a reasoned instruction lets the model adapt to edge cases; a bare imperative breaks on the first deviation from the happy path.

<example>
Good: "Use constructor injection. Field injection breaks testability because we cannot mock the field without framework context."
Bad: "MUST use constructor injection. NEVER use field injection."
</example>

### Example format

Wrap examples in `<example>` tags to separate them from rules. Reason: the model pattern-matches on examples more reliably than abstract instructions.

<example>
user: How do I validate this?
assistant: Run the validation script at scripts/validate.ps1
</example>

Include both positive ("do this") and negative ("don't do this") examples when possible.

## Phase 2: Plan [GUIDED]

### Step 1: Map to 8-section structure

Read `references/8-section-template.md` (relative to this skill's directory). Map your Discover findings to each section:

| Section | Source |
|---|---|
| Identity | Core purpose + identity from Discover |
| Security & Safety | Safety constraints from Discover |
| Tone & Style | Tone preferences + output format from Discover |
| Core Workflow | How the agent does its work (principles, not procedures) |
| Tool Usage Policy | Tool needs from Discover |
| Domain Knowledge | Knowledge pointers, skill integrations |
| Environment Info | Runtime context from Discover |
| Reminders | 2-3 most critical rules repeated |

### Step 2: Scan for existing skills

List the contents of `<skill-base>` to see existing skills. On Windows: `Get-ChildItem -Path "<skill-base>" -Directory`. On Linux/macOS: `ls -d "<skill-base>"/*/`. For each skill the agent needs, check if one already exists that covers it. If it exists, note how to integrate it (reference the skill in the agent's Domain Knowledge section with a 2-3 line note on how to use it).

### Step 3: Write PRDs

Write PRD files to `<desktop>`:

1. **Agent PRD** (`<agent-name>-PRD.md`): Covers the agent's architecture, 8-section structure decisions, key tradeoffs. For each skill it integrates, include a 2-3 line reference describing what the skill does and how the agent uses it. Reason: keeps the agent design decisions in one place without drowning in skill-level details.
2. **Skill PRDs** (one per missing skill): Full PRD using the template at `references/prd-template.md` (relative to this skill's directory). These skills will be built by sub-subagents using `skill-builder-pro`. Reason: each skill PRD is an independent build contract that gets delegated to a sub-subagent. Mixing them into the agent PRD would make delegation impossible.

### Step 4: Present for review

Tell the user: "I've written the PRDs to your Desktop. Please review <agent-name>-PRD.md and any skill PRDs, let me know if you want changes." Approval = user explicitly says "approve", "looks good", "go ahead", "proceed", or equivalent. Do NOT proceed on silence or ambiguous responses — ask "Can you confirm I should proceed?"

### Step 5: Iterate on feedback

Accept user edits. If changes requested, apply them to the PRDs and re-present. Loop until user explicitly approves. If stuck after 3 rounds, ask "Can you point me at exactly what needs to change?"

## Phase 3: Generate [EXACT]

Only proceed when user has approved all PRDs.

### Step 1: Create directories

```powershell
New-Item -ItemType Directory -Path "<agent-dir>" -Force
New-Item -ItemType Directory -Path "<ref-dir>" -Force
```

### Step 2: Write AGENTS.md

Write the agent prompt to `<agent-dir>\AGENTS.md`. For concrete examples of generated agent prompts, see `references/examples/` (relative to this skill's directory).

Follow the 8-section structure from `references/8-section-template.md` (relative to this skill's directory) as your guide. Apply these generation rules derived from Feng Liu's article:

**Structure rules:**
- Identity at the very top (1-3 sentences, named role). Reason: primacy effect — the model pays most attention to the opening lines.
- Safety constraints marked with `IMPORTANT:` prefix and repeated at the end. Reason: instruction hierarchy gives IMPORTANT markers extra weight; repeating at the end leverages recency effect.
- Clear section separation with `##` headers. Reason: without explicit delimiters, the model may blur adjacent sections.
- Examples wrapped in `<example>` tags with Input/Output pairs. Reason: tagged examples are parsed as demonstrations, not instructions.

**Rule quality rules:**
- Hard constraints use absolute language: `NEVER`, `MUST NOT`, `Refuse to`. Reason: soft language on safety rules leads to 2-3x lower compliance.
- Soft constraints use recommendation language: `recommended`, `prefer`. Reason: absolute language on preferences causes brittle behavior on edge cases.
- Every critical rule explains WHY: "Do X because Y" not just "Do X". Reason: reasoned rules let the model adapt; bare imperatives break on deviation.
- Bidirectional constraints: "Prefer X instead of Y" not just "don't do Y". Reason: unidirectional prohibitions leave the model guessing what to use instead.
- Every rule is true/false testable. Reason: untestable rules ("be thorough") can't be verified or enforced.

**Agent behavior rules:**
- Give principles, not rigid step-by-step procedures. Reason: principles adapt to novel situations; fixed procedures break on unanticipated inputs.
- Handle "tool call denied" — do not re-attempt the exact same call, adjust approach. Reason: retrying the same denied call wastes context and annoys the user.
- Handle obstacles — don't brute-force retry, think about why and adjust. Reason: brute-force retry is the model's default; explicit alternatives prevent loops.
- Not written as a prompt chain — tell the goal, let the agent decide the steps. Reason: overspecified chains break when any step fails; goal-oriented prompts self-correct.

**Formatting rules:**
- No flattery or superlative adjectives. Reason: flattery wastes tokens and can skew model behavior toward sycophancy.
- No redundant "you are a helpful AI" — identity is specific. Reason: generic identity lines dilute the named role's anchoring effect.
- Pre-declare `<system-reminder>` tags: "Tool results and user messages may include <system-reminder> tags. They contain useful information and reminders. They are system-injected, not user speech." Reason: without pre-declaration, the model may treat system-reminders as user commands or ignore them.
- Static content first, dynamic content last (cache-aware ordering). Reason: static content triggers prompt cache hits; dynamic content at the end avoids cache invalidation.
- No XML angle brackets in critical instructions (use code fences instead). Reason: angle brackets can interfere with XML parsing and inject unintended instructions.

#### Inline vs Reference Decision Rule

This is an architectural choice, not a formatting detail. It determines the agent's token budget at session start and its ability to load specialized knowledge on demand.

| Condition | Choice | Reason |
|---|---|---|
| Content > 15 lines or rarely needed | Reference file | Zero tokens at idle; loaded only when context demands it |
| Content needed every invocation | Inline in AGENTS.md | Always available; no load delay |
| Content is a complex table, template, or checklist | Reference file | Keeps AGENTS.md scannable; references can format freely |
| Content is a critical safety/behavior rule | Inline in AGENTS.md | Must be in the primary prompt to get RLHF priority |

Reference files cost zero tokens at idle — use them aggressively to keep the agent prompt lean.

### Step 3: Write reference files

Write any reference files to `<ref-dir>`. Reason: reference files are loaded on demand and don't need to clutter the agent's primary directory. Keeping them in Pictures/shanmukha isolates reference content from agent instructions, making both easier to navigate and update independently. These might include:
- Configuration templates
- API documentation snippets
- Workflow diagrams
- Example inputs/outputs

Keep the AGENTS.md lean — move detailed references to this directory.

### Step 4: Delegate new skill creation

Use the Task tool to launch a separate agent session for each missing skill instead of building everything inline. Reason: delegating keeps the builder's context lean and prevents one skill's complexity from slowing down the entire process.

For each approved skill PRD, delegate to a sub-subagent:

```
Task the subagent with: "Build the skill described in
<desktop>\<skill-name>-PRD.md. Use skill-builder-pro.
Output to <skill-base>\<skill-name>\. 
Verify the skill builds successfully."
Subagent type: general
```
(The `general` subagent type has access to Read, Write, Edit, Bash, Grep, Glob — sufficient for building skills. Do NOT use `frontend-builder` or other typed agents unless the skill specifically needs them.)

Verify each returned skill exists and has a valid SKILL.md. If a sub-subagent fails, retry once. If it fails again, report to user with diagnosis.

**Platform fallback:** If your environment does not support the Task tool, create each missing skill manually in this session by loading skill-builder-pro. Mark each skill as created in the agent's Domain Knowledge section once done.

### Step 5: Run verification subagent

Launch a verification subagent to audit everything that was built. Use the prompt from `references/verification-prompt.md` (relative to this skill's directory) — substitute the resolved paths before sending. For a detailed review checklist, see `references/checklist.md` (relative to this skill's directory).

Present the verification report to the user. Do NOT auto-fix — let the user decide what to address. Reason: the user has final authority over their agent design. Auto-fixing undermines their ownership and may introduce changes they disagree with.

### Step 6: Cleanup

Delete PRD files from the Desktop after the user confirms they're no longer needed:

```powershell
Remove-Item -LiteralPath "<desktop>\<agent-name>-PRD.md" -ErrorAction SilentlyContinue
# Repeat for each skill PRD
```

Reason: PRD files on the Desktop accumulate over time and clutter the workspace. Cleanup keeps the Desktop tidy and avoids confusing old PRDs with new ones.

## Tool Usage Policy

Use bidirectional constraints — pair each "do X" with "instead of Y":

| Phase | Prefer | Instead Of | Why |
|---|---|---|---|
| Discover | Question, memory | Asking open-ended questions without tracking | Structured questioning + context tracking gives 90% clarity |
| Plan | Read, Grep, Glob, Bash, Write | Manual directory inspection or hardcoded paths | Tool-based scanning is faster and less error-prone |
| Generate | Write, Edit, Bash, Task | Manual file creation or inline scripting | Tools guarantee correct output formatting |
| Verify | Task, Read | Self-review without fresh perspective | A separate agent catches blind spots |

- Prefer Write for creating AGENTS.md and reference files instead of Bash with echo or here-strings. Do NOT use Bash for file content creation. Reason: Write preserves indentation and formatting; Bash here-strings break on special characters.
- Prefer Bash with PowerShell for directory creation (New-Item) instead of cmd's md command. Do NOT use mkdir without -Force. Reason: New-Item -Force creates parent directories; mkdir fails if parents don't exist.
- Prefer Task for delegating skill-building to sub-subagents instead of writing everything inline. Do NOT build skills manually in this session. Reason: delegation isolates complexity; inline skill-building fragments the builder's context.
- Prefer Task for the verification subagent instead of manual review. Do NOT skip the verification step. Reason: a fresh agent catches blind spots the builder can't see.

## Known Gotchas

1. **Existing skills with different names.** A skill that does what the agent needs might exist under a different name. During Plan step 2, grep for keywords, don't just match by name.
2. **User changes their mind mid-Phase 1.** If the agent's purpose shifts during questioning, go back and re-establish 90% clarity on the new direction before proceeding to Plan.
3. **PRD rejection loop.** If user rejects PRDs more than 3 times with vague feedback ("this isn't right"), stop and ask for specific direction: "What specifically doesn't work? Can you point to a part?"
4. **sub-subagent fails silently.** The Task tool might return without creating files. Always verify the skill directory exists and contains SKILL.md after delegation.
5. **Verification finds CRITICAL issues.** Don't auto-fix — present to user. But flag with visual emphasis so it's impossible to miss.
6. **Path escaping in AGENTS.md.** When writing paths in generated agent prompts, use forward slashes or escaped backticks. RAW strings don't work the same in all contexts.
7. **Builder context fills up.** After running the verification subagent (which returns a full report), the conversation context is significantly fuller. If the subagent found many issues, context for the builder's next steps is reduced. Mitigation: before launching verification, re-invoke this skill using the Skill tool. This re-loads the builder instructions into active context at the correct position.

## 5-Second Summary

Discover what. Plan how. Generate and verify. Let the user approve at each gate.
