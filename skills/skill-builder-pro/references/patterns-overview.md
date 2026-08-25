# The 14 Skill Patterns — Reference

## Overview

| # | Name | Category | Purpose | Use On |
|---|------|----------|---------|--------|
| 1 | Activation Metadata | Discovery & Selection | Pack `description` with trigger keywords | Every skill |
| 2 | Exclusion Clause | Discovery & Selection | Prevent false-positive activation | Every skill |
| 3 | Context Budget | Context Economy | Minimize tokens on known concepts | Every skill |
| 4 | Progressive Disclosure | Context Economy | SKILL.md as TOC; details in `references/` | Every skill |
| 5 | Control Tuning | Instruction Calibration | Label steps EXACT/GUIDED/FREEFORM | Skills with rigid steps |
| 6 | Explain-the-Why | Instruction Calibration | Replace MUST/ALWAYS with rule + reason | Every skill |
| 7 | Template Scaffold | Instruction Calibration | Ship templates with `{{placeholders}}` | Skills producing output |
| 8 | In-Skill Examples | Instruction Calibration | 2–3 concrete I/O pairs | Every skill |
| 9 | Known Gotchas | Instruction Calibration | Symptom → cause → response | Mature skills |
| 10 | Execution Checklist | Workflow Control | Copyable checklist prevents drift | Multi-step workflows |
| 11 | Self-Correcting Loop | Workflow Control | Produce → validate → fix → re-validate | Generative skills |
| 12 | Plan-Validate-Execute | Workflow Control | Validate plan against rules before acting | Complex/destructive ops |
| 13 | Utility Bundle | Executable Code | Ship reusable scripts | Skills needing tooling |
| 14 | Autonomy Calibration | Executable Code | Pre-approve minimal tool set | Skills needing tool access |

---

## Discovery & Selection

### 1. Activation Metadata
**Purpose:** The `description` frontmatter field is the only selection signal. Pack it with 5–15 trigger phrases matching real user requests. Bad metadata = invisible skill.
- Frontload the most distinctive keywords. List varied example queries. Keep under ~200 chars.
- Avoid generic words ("tool", "code", "project"). End with negative triggers.
- **Mistakes:** Too generic (matches everything). Too narrow (never matches). Not updated as scope evolves.
- **Example:** Good: `"Create agent skills. Use when: 'create a skill', 'make a skill', 'write a skill'. NOT for editing existing skills."` Bad: `"A skill for creating things."`

### 2. Exclusion Clause
**Purpose:** The most important line — what NOT to trigger on. Prevents expensive false-positive activation.
- Place at end of `description`. Be specific about what's excluded. Use strong negative language.
- Sibling skills must exclude each other's jobs.
- **Mistakes:** Omitting it entirely. Vague wording like "use wisely."
- **Example:** Good: `"Do NOT use for editing existing skills, README writing, or general coding."` Bad: `"Only use when appropriate."`

---

## Context Economy

### 3. Context Budget
**Purpose:** Every token crowds out real work. Don't explain what training already covers (HTTP, REST, SQL, git). Tell the agent only what's unique to this task.
- Never define industry-standard concepts or basic syntax. Use bullet points and tables, not paragraphs.
- If a section reads like a textbook, kill it. Mature skill: ~300 lines max.
- **Mistakes:** "Prerequisites" section explaining npm. Multi-paragraph explanations of known flags.
- **Example:** Good: `"Use Express 4 with async-error-handling middleware (not try/catch everywhere)."` Bad: *Three paragraphs on Express basics.*

### 4. Progressive Disclosure
**Purpose:** SKILL.md is a TOC, not the full manual. Push specs, templates, and examples to `references/` files loaded on demand.
- SKILL.md = workflow outline + links. Templates in `references/templates/`, scripts in `references/scripts/`.
- Use descriptive filenames (`deploy-checklist.md`, not `ref_a.md`). Tell agent WHEN to load each file.
- **Mistakes:** Dumping everything into SKILL.md. Cryptic filenames. No "when to load" instruction.
- **Example:** Good: SKILL.md is 10 lines. Step 4: `"Load references/deployment-checklist.md"` Bad: 800-line SKILL.md with everything inlined.

---

## Instruction Calibration

### 5. Control Tuning
**Purpose:** Not every step needs the same freedom. Label EXACT (verbatim), GUIDED (principles, adapt), FREEFORM (judgment). Match control to how much deviation the outcome tolerates.
- Prefix headings: `[EXACT]`, `[GUIDED]`, `[FREEFORM]`.
- EXACT where deviation breaks things. GUIDED is the default. FREEFORM for creative work.
- **Mistakes:** All EXACT (brittle). All FREEFORM (pointless). Inconsistent labeling.
- **Example:** Good: `[EXACT] Step 3: Generate route file` / `[GUIDED] Step 4: Implement logic` / `[FREEFORM] Step 5: Name variables`. Bad: no labels.

### 6. Explain-the-Why
**Purpose:** Replace MUST/ALWAYS/NEVER with rule + reason. The WHY is the rubric for edge cases the author didn't anticipate.
- Every directive must include "because..." with concrete consequences.
- Write for the agent's reasoning, not compliance.
- **Mistakes:** "Because I said so." Circular reasoning. Explaining trivial things.
- **Example:** Good: `"ALWAYS use parameterized queries because raw interpolation enables SQL injection."` Bad: `"ALWAYS use parameterized queries."`

### 7. Template Scaffold
**Purpose:** Ship templates with `{{placeholders}}` instead of describing output. Reduces drift. Strict templates for machine-parsed output, flexible for human-facing.
- Templates in `references/templates/` — loaded on demand.
- Use `{{PLACEHOLDER}}` for required fields, `[optional]` for optional.
- Machine templates must be syntactically valid as-is.
- **Mistakes:** Too rigid (multiple edits needed). Missing optional sections. No location info.
- **Example:** Good: `def {{name}}({{params}}):\n    """{{desc}}"""\n    {{impl}}`. Bad: paragraph describing "a good function."

### 8. In-Skill Examples
**Purpose:** Claude pattern-matches on examples more reliably than rules. 2–3 concrete I/O pairs demonstrating structure, tone, and quality.
- 2–3 examples spanning simple, typical, edge-case. Show user input and skill output.
- Examples beat rules for style and formatting. Bad examples > no examples.
- **Mistakes:** Examples too similar. No examples at all.
- **Example:** Good: `User: "Create a fetch wrapper" → Skill fills fetch-template.md`. Bad: `"Produce high-quality output."`

### 9. Known Gotchas
**Purpose:** Document real mistakes as symptom → cause → response. Most valuable section of a mature skill — prevents repeating painful errors.
- Three parts: **Symptom**, **Cause**, **Response**. Prioritize costly gotchas (silent failures, infinite loops).
- Add as discovered. No gotchas = not used enough. Place after workflow steps.
- **Mistakes:** Vague ("things might break"). Paranoia-driven (impossible scenarios).
- **Example:** Good: `Symptom: ENOENT. Cause: directory doesn't exist. Response: mkdir -p first.` Bad: `"Make sure directories exist."`

---

## Workflow Control

### 10. Execution Checklist
**Purpose:** Copyable `- [ ]` checklist at workflow top prevents step-skipping (especially across context interruptions).
- At the very top of the workflow. Each item = one-line step summary.
- Visually scannable in 5 seconds. Complex skills can use sub-checklists.
- **Mistakes:** Vague items ("Improve quality"). Too many (> 15). Checklist at the bottom.
- **Example:** Good: `- [ ] 1. Analyze codebase / - [ ] 2. Generate model / - [ ] 3. Create routes`. Bad: no checklist.

### 11. Self-Correcting Loop
**Purpose:** Produce → validate (objective criteria) → fix → re-validate (max 3 retries). Prevents shipping broken output and infinite loops.
- Validation must be checkable (linter, tests, required fields). Cap at 3 retries.
- Fix step references validation output. Manual validation only for subjective criteria.
- **Mistakes:** No retry cap. Subjective criteria (agent always self-approves).
- **Example:** Good: `Generate → Run linter → Fix errors → Re-run → Max 3x → Proceed`. Bad: `"Make sure it's good."`

### 12. Plan-Validate-Execute
**Purpose:** Before touching real data: write a plan → validate against explicit rules → execute only if valid. For complex/destructive operations where mistakes cost.
- **Plan:** Steps, commands, expected outcomes. **Validate:** Check against rules (destructive paths? backups? ordering?). **Execute:** Only if all checks pass.
- Post-execution: verify outcome matches expected.
- **Mistakes:** Skipping validate phase. Vague validation rules. No post-execution verification.
- **Example:** Good: `Plan → Validate (backups? rollback?) → Execute`. Bad: `"Think before you act."`

---

## Executable Code

### 13. Utility Bundle
**Purpose:** Ship reusable scripts instead of rewriting the same logic every session. Parsers, formatters, validators, generators — invoked, not re-derived.
- Scripts in `references/scripts/` with clear names. Self-documenting (usage comment, `--help`).
- Idempotent where possible. Document dependencies at top. Skill tells agent when to run.
- **Mistakes:** Undocumented deps ("command not found"). No confirmation before state changes. Trivial scripts not worth shipping.
- **Example:** Good: `references/scripts/validate-frontmatter.py` run after writing SKILL.md. Bad: telling agent to "write a validation script" every session.

### 14. Autonomy Calibration
**Purpose:** `allowed-tools` pre-approves the minimal tool set. Pre-authorization, not restriction — agent executes without permission prompts.
- List only needed tools. Each entry = tool name + justification.
- For destructive tools, justify what they write/edit/run. Revisit on scope changes.
- **Mistakes:** All tools approved (no safety). Too few (agent blocked). No justifications.
- **Example:** Good: `allowed-tools: [Read: explore] [Write: create files] [Bash: run linters]`. Bad: no list or everything listed.
