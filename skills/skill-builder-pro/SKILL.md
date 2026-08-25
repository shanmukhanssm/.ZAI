---
name: skill-builder-pro
description: >-
  Creates production-grade agent skills following the 14-pattern methodology.
  Specializes in skill authoring — designing workflows, writing Claude-aware
  instructions, enforcing authoring patterns, and producing SKILL.md packages.
  Trigger: "create a skill", "build a skill", "make a new skill", "generate a
  skill", "author a skill", "write a skill for me", "skill-builder pro",
  "i need a skill", "turn this into a skill", "build a SKILL.md", "skill
  authoring", "make me a skill".
  Do NOT use for: general coding tasks, README writing, frontend/backend
  development, editing existing skills (unless asked to create from scratch),
  writing blog posts, or generating configuration files.
allowed-tools: Read, Write, Bash, Glob, Grep, Question, Edit, Task
---

# skill-builder-pro

## The Core Problem This Skill Solves

Claude writes good instructions for itself. But it doesn't know what it doesn't know about skill structure — about what happens when a fresh session loads its instructions cold, about what patterns prevent silent failure, about how a single ambiguous line breaks every downstream invocation. The 14 patterns exist because unpatterned skills fail silently: they work for the happy path and break on the first edge case the author never imagined. A bad skill isn't a bug — it's an AI confidently doing the wrong thing for every future user.

This is the foundational skill because it builds the instruction files that teach other AIs how to teach other AIs. If this skill skips patterns, every downstream skill inherits those gaps. A weak skill-builder produces a weak library.

### What This Skill Masters

skill-builder-pro does not write app code, design UIs, or configure servers. It builds SKILL.md packages — the instruction files that teach AI agents how to perform tasks.

### What This Skill Specializes In

- **Structuring multi-step workflows** that an AI follows reliably — because without explicit sequence and validation gates, Claude guesses the order and skips the checks
- **Writing Claude-aware instructions** — instructions that account for how another AI reads them, because instructions that assume prior context fail silently in a fresh session with no history
- **Enforcing all 14 skill authoring patterns** across generated skills — because patterns are the accumulated wisdom of thousands of skill invocations, and skipping them means your successor inherits your blind spots
- **Detecting and fixing weak instructions, missing examples, and unclear reasoning** — because Claude follows what you wrote, not what you meant, and the gap between intent and instruction is where bugs live
- **Generating production-grade reference files** (scripts, templates, examples, gotchas) — because inline context bloats the skill window at session start while reference files sit at zero cost until loaded
- **Running a 3-stage quality pipeline**: automated validation → AI peer review → manual review — because one pass never catches everything and each stage catches what the previous stage missed

---

## Workflow Execution Checklist

Copy this checklist into the conversation and tick items as you complete them:

- [ ] Step 1: Discovery — examples shown to user, user described their skill need
- [ ] Step 2: Plan + PRD — written to Desktop, presented for review
- [ ] Step 3: User approved → Implementation
       - [ ] Frontmatter + exclusions written (Pattern 1-2)
       - [ ] Context budget + progressive disclosure followed (Pattern 3-4)
       - [ ] Instructions calibrated with examples (Pattern 5-9)
       - [ ] Workflow controls added (Pattern 10-12)
       - [ ] Scripts + allowed-tools configured (Pattern 13-14)
       - [ ] Extra quality rules applied:
             - Every instruction includes WHY
             - Every section has at least 1 concrete example
             - Claude-awareness: "Would another AI with zero conversation history know what to do here?"
- [ ] Step 4a: Self-review — validate-skill.ps1 passed (max 3 retries)
- [ ] Step 4b: AI Peer Review — subagent reviewer rated and submitted suggestions
- [ ] Step 4c: Manual review — user reviewed and approved/fixed

---

## Step 1: Discovery (Examples-First)

Discovery exists because the biggest risk in skill authoring is building the wrong thing well. Examples-first framing gives the user a vocabulary to describe what they want before they commit to a design — a user who's never seen a good skill can't articulate what they need.

This is NOT a questionnaire. You do not ask fixed questions. Instead:

### 1a. Show the user what a good skill looks like

From `references/examples-library.md`, show 2-3 complete example skills:
- One simple skill (e.g., commit-formatter)
- One medium skill (e.g., readme-writer)
- One complex skill (e.g., code-reviewer)

Let the user see what a finished, well-structured skill looks like before they describe their own.

### 1b. Ask the user to describe what they want

Simply ask: "Describe what skill you want to build."

### 1c. Extract what you need organically

From their description, identify:
- **What it does** — core purpose in one sentence
- **Who it's for** — beginner, expert, team, personal
- **When to trigger** — exact user phrases that should fire it
- **When NOT to trigger** — near-miss phrases to exclude
- **Workflow complexity** — number of steps, fragile or flexible
- **Output produced** — files, code, text, data
- **Scripts/references needed** — validation, templates, helpers
- **Audience** — personal or shared

### 1d. Ask targeted follow-ups (one at a time)

Only ask if something is genuinely unclear. Examples:
- "You mentioned it should trigger on pull requests — should it also trigger on direct pushes?"
- "You said it validates output — should I include a validation script or just review steps?"
- "Is this for personal use or shared with a team?"

### 1e. Stop at 90% clarity

You do not need 100%. The PRD will catch what you missed during review.

**If the user says "just build it, no questions":** Skip discovery entirely. Document your inferences in the PRD and let the user correct during review.

---

## Step 2: Plan + PRD

Planning exists because building a skill without a PRD guarantees contradictory instructions. The act of writing decisions down reveals assumptions both you and the user are making unconsciously — and those assumptions, left unwritten, become bugs in the generated skill.

From your discovery notes, analyze:

1. **Scripts needed** — Based on workflow complexity. Default language: PowerShell (Windows). Only propose scripts for repeated deterministic operations.
2. **Reference files needed** — Templates, patterns references, gotchas, examples. Only if the skill's domain is broad enough to need them.
3. **Tool mapping** — Map each workflow step to its required tool (Read, Write, Bash, Grep, Glob, Question, Edit, Task).
4. **Platform constraints** — Default: Windows (PowerShell, `$env:USERPROFILE`, forward-slash-compatible paths).
5. **Edge cases** — Identify 3-5 failure modes from the domain and workflow fragility.
6. **Error handling** — Define what happens on failure: retry, report, or abort.

### Write the PRD

Write a PRD document to `$env:USERPROFILE\Desktop\<skill-name>-PRD.md` with this structure:

1. **Executive Summary** — What the skill does and why
2. **Key Decisions** — Each decision with its rationale
3. **File Structure** — Every file and its purpose
4. **Content Plans** — What goes in each file (SKILL.md sections, script logic, reference content)
5. **Size Constraints** — SKILL.md 300-500 lines, description 1024 chars, etc.
6. **14-Pattern Compliance Map** — Table showing pattern coverage
7. **Edge Cases & Failure Modes** — Known risks with mitigations

### Present for Review

Say: "I've written the full plan to your Desktop at [path]. Please review and let me know if you want any changes before I start building."

---

## Step 3: Implementation (Pattern-by-Pattern)

Each pattern implementation follows this format:
- **Why it matters** — one-liner explaining why ignoring this fails
- **Good example** — concrete correct usage
- **Bad example** — concrete wrong usage
- **Instructions** — what to actually do

### Pattern 1: Activation Metadata (Frontmatter)

**Why it matters:** The `description` field is the ONLY signal the skill selector sees at session start. If it doesn't match user phrasing, the skill never loads — even with perfect instructions.

**Good:**
```yaml
name: commit-formatter
description: Formats git commits following Conventional Commits.
Use when user says "format commit", "write a commit message",
"conventional commit", "generate commit".
Do NOT use for README files, changelogs, or release notes.
```

**Bad:**
```yaml
name: commit-formatter
description: Helps with commits.
```

**Instructions:**
- `name`: lowercase, hyphens only, max 64 chars, no leading/trailing/consecutive hyphens
- `description`: Max 1024 chars. Start with WHAT it does. Add 5-10 trigger phrases the user would actually say. Be slightly pushy — Claude undertriggers skills.
- Include 3-5 exclusion/near-miss scenarios
- No XML angle brackets (`<` `>`) in frontmatter — they inject unintended instructions
- Declare `allowed-tools` with the minimal tool set the skill needs
- File must be named exactly `SKILL.md`, case-sensitive

### Pattern 2: Exclusion Clause

**Why it matters:** Without exclusions, the skill triggers on tangentially related requests. Ruben Hassid calls this "the single most important line in the description."

**Good:**
```
Do NOT use for: blog articles, newsletters, tweets, long-form content, API documentation, or inline code comments.
```

**Bad:** No exclusion clause — skill fires on every "write" request and conflicts with other skills.

**Instructions:**
- Add 3-5 specific near-miss scenarios that share keywords with this skill
- Keep them narrow enough to disambiguate but broad enough to cover expected overlap
- Update exclusions when adding new skills that share vocabulary

### Pattern 3: Context Budget

**Why it matters:** Every token in your skill crowds out tokens from other skills, conversation history, and the user's message. Waste across 20+ skills means context is half-full before the user speaks.

**Good:**
```markdown
Validate the output is valid JSON before writing to file.
```

**Bad:**
```markdown
JSON (JavaScript Object Notation) is a lightweight data-interchange format...
```

**Instructions:**
- Before writing any sentence, ask: "Does this sentence teach Claude something it doesn't already know?" If no, cut it.
- Use consistent terminology throughout. Never switch between "field / box / element" for the same concept.
- Remove fluff: "Note that...", "It is important to...", "Please ensure that..."
- If a concept is common knowledge (JSON, HTTP, git), do NOT explain it.
- This is baseline discipline for every skill.

### Pattern 4: Progressive Disclosure

**Why it matters:** An 800-line SKILL.md costs the same whether the user uses 1 section or all 8. Reference files cost zero tokens at idle — they load on demand.

**Good:**
```markdown
See `references/templates.md` for output formatting templates.
```

**Bad:** 200 lines of formatting rules inline that the current task doesn't need.

**Instructions:**
- Keep SKILL.md under 300-500 lines
- Move detailed references to `references/` files
- Keep reference graph **shallow** — every file one hop from SKILL.md. Never chain SKILL.md → advanced.md → details.md (Claude mis-routes)
- Files over 200 lines need a table of contents at the top
- Scripts in `scripts/` execute without loading into context

### Pattern 5: Control Tuning

**Why it matters:** Skill authors over-constrain because rigid instructions feel safer. They are not — they just fail differently. Calibrate per action, not per skill.

**Good:**
```markdown
## Step 1: Review output [FREEFORM - use your judgement]
Read the generated skill and decide if quality is acceptable.

## Step 2: Run validator [EXACT - do not modify]
powershell -File scripts/validate.ps1 -Path ./output/

## Step 3: Write PRD [GUIDED - use template from references/]
```
**Bad:** All steps marked EXACT, even the creative/judgement-based ones.

**Instructions:**
- Label each step with its freedom level: `[EXACT]` (literal), `[GUIDED]` (template), `[FREEFORM]` (judgement)
- High freedom → text instructions, "use your judgement"
- Medium freedom → pseudocode or parameterized templates
- Low freedom → exact commands, "do not modify"

### Pattern 6: Explain-the-Why

**Why it matters:** All-caps MUST/ALWAYS/NEVER gives Claude rigid rules with no context. It follows the letter and misses edge cases. A reasoned instruction adapts; a bare imperative breaks.

**Good:**
```
Use constructor injection. Field injection breaks testability because we cannot
mock the field without Spring context. This matters when multiple services
depend on the same repository.
```

**Bad:**
```
MUST use constructor injection. NEVER use field injection.
```

**Instructions:**
- Replace every MUST/ALWAYS/NEVER with rule + reason
- Exception: genuinely fragile operations (irreversible, security-critical) still use clear imperatives, but add one line of WHY
- **Quality Rule 1 enforces this** — every structural/behavioral decision includes WHY

### Pattern 7: Template Scaffold

**Why it matters:** A blank page invites structural drift. Templates with placeholders constrain output to what the consumer expects.

**Good:**
```markdown
## Output — EXACT structure (CI parser reads this)
# [PROJECT] — Audit Report
## Risk Level: [CRITICAL/HIGH/MEDIUM/LOW]
## Findings
- [FINDING]
## Action: [RECOMMENDATION]
Do not reorder fields — parser expects exact field order.
```

**Bad:**
```
Write an audit report.
```

**Instructions:**
- Machine-parsed output → strict template: "do not reorder or reformat"
- Human-consumed → flexible template: "use as a starting point, adapt as needed"
- Use `[PLACEHOLDER]` markers clearly
- Multiple output variants → provide per-variant template or a selection mechanism

### Pattern 8: In-Skill Examples

**Why it matters:** Claude pattern-matches on examples more reliably than it follows prose instructions. Two well-chosen examples communicate more than ten lines of instructions.

**Good:**
```markdown
**Example 1: Standard commit**
Input: "Added user auth with JWT"
Output: feat(auth): implement JWT authentication

**Example 2: Bug fix**
Input: "Fixed login crash on empty fields"
Output: fix(auth): handle empty fields to prevent crash
```

**Bad:** Instructions only, no examples — Claude guesses the format and gets it wrong.

**Instructions:**
- Include 1-3 concrete Input/Output pairs per major section (minimum 1, recommended 2-3 for complex sections)
- Cover expected variation — if all examples share a subtle bias, Claude reproduces it across all invocations
- Label clearly (Example 1, Example 2...) with a short description

### Pattern 9: Known Gotchas

**Why it matters:** Happy-path-only skills fail on edge cases. Tort Mario calls gotchas "the most valuable content of a mature skill."

**Good:**
```markdown
## Known Gotchas
1. **Scanned PDFs return empty text.** Check page content type before
   extraction. Fall back to OCR when text extraction returns zero results.
2. **50MB+ files timeout.** Split into 10MB chunks, process sequentially.
3. **Stale gotchas mislead.** If a gotcha fires with false positives,
   remove or update it — platforms and libraries change.
```

**Bad:** No gotchas section — first real edge case breaks the skill.

**Instructions:**
- Dedicated `## Known Gotchas` section in SKILL.md
- Each gotcha = symptom + cause + correct response
- Derive from domain/workflow fragility identified during discovery
- Include "last verified" note on time-sensitive gotchas

### Pattern 10: Execution Checklist

**Why it matters:** In multi-step procedures, Claude skips validation steps, loses position, or declares done at step 4 of 6. A visible checklist raises the bar for declaring completion.

**Good:**
```markdown
- [ ] Gather project context
- [ ] Analyze changes
- [ ] Write output
- [ ] Quality check
- [ ] Present to user
```

**Bad:** "Follow these steps" with no tick mechanism — Claude tracks steps invisibly and misses them.

**Instructions:**
- Provide a copyable checklist at the top of the workflow section
- Instruct Claude to paste into conversation and tick as completed
- Use for any workflow with 3+ steps
- Overkill for 1-2 step tasks

### Pattern 11: Self-Correcting Loop

**Why it matters:** A single forward pass ships mistakes the skill could have caught. An explicit validate-and-fix loop catches errors before they reach the user.

**Good:**
```markdown
1. Generate the output file
2. Validate: run `powershell -File scripts/validate.ps1 -Path output.json`
3. If validation fails → fix issues → re-run validation
4. Repeat until validation passes (max 3 retries)
5. If still failing after 3 retries, show the user the errors and ask for guidance
```

**Bad:** No validation step — mistakes ship silently.

**Instructions:**
- Define: produce → validate → fix → re-validate → loop until pass
- Include a retry cap (3 attempts) to prevent infinite loops
- Add fallback: if still failing after cap, present to user

### Pattern 12: Plan-Validate-Execute

**Why it matters:** For destructive operations, a "just do it" pass lets errors cascade silently. Validating an intermediate plan before touching real files catches design errors before data loss.

**Good:**
```markdown
### Phase 1: Plan
Generate a JSON plan listing every file to modify, the exact changes, and rollback strategy.

### Phase 2: Validate
Check plan for: conflicting changes, missing files, permission issues, rollback viability.

### Phase 3: Execute
Only proceed if Phase 2 passes. Apply changes one by one. Verify each.
```

**Bad:** Direct execution — errors cascade silently and "undo" is costly or impossible.

**Instructions:**
- Split into three distinct phases with clear stopping points between them
- **Plan:** Describe every change (what, where, how, rollback)
- **Validate:** Check plan against rules, never against real data
- **Execute:** Only if validation passes

### Pattern 13: Utility Bundle

**Why it matters:** Asking Claude to rewrite a validation script from scratch every invocation is slower, less reliable, and burns tokens on code the user never sees. Ship it once.

**Good:**
```
scripts/
├── validate-skill.ps1      # 14-pattern + quality rules validator
├── create-stub.ps1         # Generates stub skill directory structure
```

**Bad:** No scripts — Claude rewrites the same helpers from scratch each time.

**Instructions:**
- One script = one well-defined purpose
- Scripts must handle common failure modes cleanly — don't dump ambiguity back on Claude
- Constants need justifying comments: `# 30s timeout covers slow VPN connections`
- After running the skill on 3 test cases, if Claude wrote the same helper independently multiple times, promote it to `scripts/`

### Pattern 14: Autonomy Calibration

**Why it matters:** Full default tool set = unnecessary risk for a read-only task. Declare `allowed-tools` to pre-approve only what the skill actually needs.

**Good:**
```yaml
allowed-tools: Read, Grep, Glob       # security audit (read-only)
allowed-tools: Read, Write, Bash      # deploy script
```

**Bad:** No `allowed-tools` declared — full tool set enabled, including tools the skill never uses.

**Instructions:**
- Declare `allowed-tools` with the minimal set the skill needs
- Map each workflow step to its required tool. If no step needs Bash, don't allow Bash.
- **Important:** `allowed-tools` is pre-authorization, not restriction. It reduces approval friction but does NOT block unlisted tools. True restrictions require platform permission rules.

### Pattern Interaction Guidance

Patterns are not isolated — they interact and sometimes conflict. Follow these guidelines when applying multiple patterns together:

**Pattern 3 (Context Budget) vs Pattern 8 (In-Skill Examples):** Examples increase token count. Put 1-2 critical examples inline, move the rest to `references/examples-library.md`. This satisfies Pattern 8 without violating Pattern 3.

**Pattern 4 (Progressive Disclosure) vs Pattern 8:** Use progressive disclosure to push secondary examples to reference files. The SKILL.md stays lean while still providing thorough examples on demand.

**Pattern 7 (Template Scaffold) vs Pattern 10 (Execution Checklist):** Ship the checklist inline in SKILL.md and move output templates to `references/templates.md`. The checklist drives workflow; templates are loaded only when generating output.

**Pattern 11 (Self-Correcting Loop) vs Pattern 12 (Plan-Validate-Execute):** Plan-Validate-Execute is for destructive operations (file writes, migrations); Self-Correcting Loop is for generative operations (code gen, content creation). They are complementary, not alternatives.

For a tabular cross-reference of all 14 patterns, see `references/patterns-overview.md`.

---

## Extra Quality Rules (Beyond 14 Patterns)

### Rule 1: Every Instruction Must Include WHY

Every structural or behavioral decision in the generated skill must include a one-line explanation of WHY.

**Exception:** Self-evident exact commands (`npm install`, `git push`).

**Check:** After writing each section, scan for bare MUST/ALWAYS/NEVER without a following "because" or "since" statement. Fix any you find.

### Rule 2: Every Section Must Have ≥1 Concrete Example

Every major section in the generated skill must include at least one concrete example. Show both "good" and "bad" when possible.

**Check:** Scan the generated SKILL.md — any section without an example gets one added.

### Rule 3: Claude-Awareness Check

Every instruction must account for the fact that another Claude instance will read and execute this skill with zero conversation history.

**Check:** Ask yourself for every section: "Would another Claude with no prior context, no conversation history, and only this file to go on know what to do here?"

---

## Claude-Aware Instruction Principles

Apply these principles when writing every section of a generated skill:

### 1. Assume Zero Conversation History

The generated skill will be loaded in a fresh session. Every instruction must be self-contained. Do not reference "as we discussed earlier" or "as mentioned above" — write for an AI that has only this file. A skill that references prior context loads into a session where no such discussion happened, and Claude, being cooperative, hallucinates the missing context rather than flagging it as undefined.

### 2. Include the Non-Obvious

Your experience (platform quirks, timing issues, common mistakes) is not Claude's experience. Write it down.

**Instead of:** "Validate the file exists."
**Write:** "Validate the file exists. Claude has been observed to hallucinate file paths in complex directory structures — use `Test-Path` to confirm."

### 3. Explain Recovery Paths

Don't just say "validate." Say what to do when validation fails.

Claude's default recovery on any error is to retry with minor variations — the exact wrong behavior when the correct response is to stop and surface the problem to the user. If you don't specify recovery, Claude keeps banging on the same wrong door.

**Example:** "If validation fails, fix the issue and re-run. Max 3 retries. If still failing after 3, present the error to the user with your diagnosis."

### 4. Tell Claude What Claude Gets Wrong

If you've observed Claude hallucinating paths, skipping steps, misreading file structures, or making specific mistakes — document them. This is the highest-leverage information you can include: it costs nothing to write and prevents the exact failure modes that slip past every other quality gate. No amount of "be careful" instructions replaces a documented pattern of what goes wrong.

### 5. Prefer "Do X because Y" Over "Do X"

The WHY lets Claude adapt to unanticipated edge cases. A bare instruction breaks on the first deviation from the happy path. A reasoned instruction gives Claude a rubric for handling novelty.

---

## Step 4: Review Pipeline

The 4a→4b→4c order is deliberate: the script catches format errors first because they're cheap to fix. The AI peer review catches structural issues next because they require thought to fix. The user reviews last because their time is the scarcest resource — by then, the skill is polished enough that they're judging substance, not typos.

After implementation, run these 3 reviews IN ORDER:

### Step 4a: Self-Review (Script)

Run the validation script:
```
powershell -File scripts/validate-skill.ps1 -Path <generated-skill-path>
```

- Fix all issues the script reports
- Re-run until pass (max 3 retries)
- If still failing after 3 retries, show the user the errors and ask for guidance

### Step 4b: AI Peer Review (Subagent)

Deploy a subagent to review the generated skill as an honest, critical peer reviewer:

```
Task the subagent with this prompt:
"You are a brutally honest skill reviewer. Your job is to scrutinize this
newly generated skill and find every flaw. Do NOT be polite — be critical.
Rate each category 1-10 and explain any rating below 7.

Categories:
1. Pattern coverage (1-10) — Are all 14 patterns meaningfully addressed?
2. Example quality (1-10) — Are examples clear, correct, and sufficiently varied?
3. WHY coverage (1-10) — Does every instruction include meaningful reasoning?
4. Claude-awareness (1-10) — Would another AI with zero conversation history understand this?
5. Clarity (1-10) — Is the skill easy to follow from start to finish?

For any rating below 7:
- State exactly what is wrong
- Explain why it matters
- Give a concrete fix

Review these files: [list all generated files]
[Feed the actual file contents to the reviewer]"
```

- Apply any fixes the reviewer suggests that you agree with
- Ignore false positives (the reviewer may be wrong — use your judgement)
- Loop: review → fix → re-review if major issues found (max 2 rounds)

### Step 4c: Manual Review (User)

Present the completed skill to the user with this message:

```
"The skill is built and has passed:
- Step 4a (Self-review): All format checks pass
- Step 4b (AI Peer Review): Rated [X/10] with [N] suggestions applied

Please review the skill at [path] and:
1. Confirm the skill does what you wanted
2. Check the examples make sense to you
3. Let me know if anything needs changing
4. Say 'approve' and I'll consider it done"
```

---

## File Generation Rules

- Every file must be syntactically valid (YAML frontmatter parsable, code runnable)
- Scripts in `scripts/` must handle common failure modes gracefully — because a script that dumps raw error messages on Claude leaves the AI guessing whether to retry, abort, or ask the user
- Reference files over 200 lines must have a table of contents at the top
- Do NOT reference files that don't exist — because Claude does not verify file existence before trying to read; it just fails with an unhelpful error
- Do NOT include placeholder text like "TODO" or "FILL THIS IN" — because Claude treats placeholders as intentional content and ships them to production without flagging them
- For every decision embedded in the generated skill, include the WHY (see Quality Rule 1 above)
- SKILL.md must stay under 500 lines (progressive disclosure). Meta-skills like skill-authoring tools get a relaxed cap of 600 lines — their broader scope inherently requires more instruction.
- `description` in frontmatter must stay under 1024 characters


