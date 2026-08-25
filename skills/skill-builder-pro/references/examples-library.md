# skill-builder-pro — Examples Library

Curated examples shown to users during Step 1 (Discovery) of the skill authoring workflow. Demonstrates what well-structured skills look like before the user describes their own.

## Table of Contents

1. [Complete Skill Examples](#1-complete-skill-examples)
   - [Simple: commit-formatter](#simple-commit-formatter)
   - [Medium: readme-writer](#medium-readme-writer)
   - [Complex: code-reviewer](#complex-code-reviewer)
2. [Frontmatter Examples (Good vs Bad)](#2-frontmatter-examples-good-vs-bad)
3. [Workflow Instruction Examples (Good vs Bad)](#3-workflow-instruction-examples-good-vs-bad)
4. [Explain-the-Why Examples (Before vs After)](#4-explain-the-why-examples-before-vs-after)
5. [Gotcha Examples (Well-written vs Vague)](#5-gotcha-examples-well-written-vs-vague)

---

## 1. Complete Skill Examples

### Simple: commit-formatter

A task skill that reformats git commit messages to Conventional Commits.

```yaml
---
name: commit-formatter
description: >-
  Formats git commit messages to Conventional Commits spec
  (type(scope): description). Trigger: "format commit", "write a
  commit message", "conventional commit", "fix commit message".
  Do NOT use for: changelogs, release notes, interactive rebase,
  or amending without review.
allowed-tools: Read, Bash
---
```

# commit-formatter

Validates staged commit messages against `type(scope): description` and rewrites them if invalid.

## Workflow

1. **Read message** [EXACT] — `git log -1 --format=%s%n%n%b HEAD`
2. **Parse** [EXACT] — Match against `^(feat|fix|chore|docs|refactor|test|style|perf)(\(.+\))?!?:\s.+`
3. **If invalid** [GUIDED] — Print error with reason, ask user for corrected message, rewrite with `git commit --amend -m "<corrected>"`

**Examples:**
- `feat(auth): add OAuth2 PKCE flow` — valid
- `fix: handle empty cart checkout` — valid (no scope)
- `Fix the bug` — invalid (capital F, missing colon)

## Known Gotchas

1. **Rebase context.** Running inside `git rebase` amends wrong commit. Check `git rev-parse REBASE_HEAD` — abort if set.
2. **Blank messages.** `--allow-empty` produces blank messages. Handle gracefully without crashing.
3. **Multi-line bodies.** Only reformat line 1 — preserve the body below it.

---

### Medium: readme-writer

Creates project README.md files from convention-scanned context.

```yaml
---
name: readme-writer
description: >-
  Creates project README.md files by scanning package.json,
  project structure, and conventions. Trigger: "write readme",
  "create readme", "generate documentation", "add readme".
  Do NOT use for: changelogs, API docs generated from code,
  inline comments, blog content, or documentation sites.
allowed-tools: Read, Write, Glob, Grep
---
```

# readme-writer

## Overview

Scans project files and generates a README.md matching the project's language, framework, and conventions. Covers what a new contributor needs in the first 5 minutes — not every detail.

## Execution Checklist

- [ ] Scanned `package.json` (or equivalent) for name, description, scripts, deps
- [ ] Scanned directory structure for key files (config dirs, entry points, test dirs)
- [ ] Checked existing README — preserve manual content, only regenerate stale sections
- [ ] Output fits project conventions (new project vs established repo)

## Workflow

1. **Scrape context** [EXACT] — Glob root dir, read `package.json`, `tsconfig.json`, `Dockerfile`, `Makefile` or equivalents. Read existing README if present.
2. **Analyze project type** [FREEFORM] — Is this a library, service, CLI tool, or monorepo package? Each has different emphasis (CLI tools need install+usage, libraries need API+examples).
3. **Generate sections** [GUIDED] — Use the output template below. Skip sections with no content. Do not repeat what the user can trivially infer.
4. **Write to file** [EXACT] — `Readme.md` at project root. If one exists, merge: preserve manual sections, overwrite stale auto-detectable sections.

## Output Template

```markdown
# [Project Name]

[One-line description]

## Getting Started

```
npm install
npm run dev
```

## Scripts

[npm scripts table: name → description]

## Project Structure

[Key directories and what they contain — 3-5 entries max]

## Tech Stack

[Framework, language, database, testing — only what's used]
```

## Known Gotchas

1. **Mono repos.** Root README is the top-level index. Do not repeat per-package details — link to `packages/*/README.md`.
2. **Existing README overwrite.** Always check before writing. Merge, don't replace.
3. **Empty sections waste space.** No tests? Skip the "Testing" heading entirely — no "TODO" placeholders.
4. **CLI vs library confusion.** CLI tools need `--help` output and global install. Libraries need import examples. Detect from `bin` field in package.json.

---

### Complex: code-reviewer

Reviews pull request changes for security, quality, and correctness.

```yaml
---
name: code-reviewer
description: >-
  Reviews pull requests and code changes for security vulnerabilities,
  quality issues, correctness bugs, and style violations.
  Trigger: "review this code", "review PR", "review changes",
  "code review", "audit changes".
  Do NOT use for: writing code, generating documentation,
  running tests, formatting code, or CI pipeline tasks.
allowed-tools: Read, Grep, Glob, Bash
---
```

# code-reviewer

## Persona

You are a skeptical senior engineer reviewing a teammate's PR. Find real issues before they reach production. Assume good intent but verify everything. Be direct, not polite.

## Execution Checklist

- [ ] Analyzed every changed file for surface-level issues
- [ ] Checked for security vulnerabilities in data handling
- [ ] Verified error handling covers failure paths, not just happy path
- [ ] Checked consistency with existing codebase patterns
- [ ] Written review report with severity ratings

## Workflow

### Phase 1: Analyze [EXACT]

1. Read `git diff` against base branch
2. For each changed file, read the full file (diff alone misses context)
3. Categorize by type: route, service, model, config, test, migration
4. Note imports and dependencies changed

### Phase 2: Report [GUIDED]

Use the output template. Rate findings:

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Security vulnerability or data loss | Must fix before merge |
| HIGH | Correctness bug or major violation | Should fix before merge |
| MEDIUM | Code quality, maintainability | Fix this sprint |
| LOW | Style, naming, minor issues | Consider fixing |

### Phase 3: Suggest [FREEFORM]

For each finding, suggest a concrete fix with code. "This is wrong" is not enough — the author should be able to copy-paste your suggestion.

## Output Template

```markdown
# Code Review — [PR Title]

**Reviewed by:** code-reviewer
**Files reviewed:** [N]
**Severity overview:** [N critical, N high, N medium, N low]

## CRITICAL Findings

### [Finding title]
- **File:** `path/to/file.ts:42`
- **Issue:** [what's wrong]
- **Risk:** [what could happen]
- **Suggestion:** [concrete fix]

## HIGH Findings

...
```

## Known Gotchas

1. **Generated files in diff.** Ignore lockfiles, built assets, generated code. Flag them only if they shouldn't be committed.
2. **False positives from large renames.** If 80% of a file changed due to reformatting, scroll past the noise. Focus on logic changes.
3. **Missing edge cases.** Reviewers consistently miss empty-state, null, and pagination edge cases. Explicitly check these in every handler.
4. **Review fatigue on large PRs.** Over 500 lines changed, spot-check critical paths. Flag that the PR is too large for thorough review.

---

## 2. Frontmatter Examples (Good vs Bad)

### Good: Specific triggers, clear exclusion, tight description

```yaml
name: db-migration
description: >-
  Creates timestamped SQL migration files with up/down pairs,
  validates rollback, and applies locally. Trigger: "create
  migration", "add migration", "write migration", "schema change".
  Do NOT use for: seed data scripts, database backups, read-only
  queries, or production deploys.
```

**Why it works:** Frontloads what it does, lists 4 trigger phrases the user would actually type, excludes 4 near-miss scenarios. Name is kebab-case, under 64 chars.

### Bad: Vague, no exclusions, generic

```yaml
name: code-helper
description: Helps with code.
```

**Why it fails:** "Helps with code" matches everything — linting, testing, writing, debugging. No exclusions means collision with every other skill. Name too generic to disambiguate.

### Bad: Wrong format, unrealistic triggers

```yaml
name: My Cool Skill
description: Only triggers when user says "xyz123 specific thing nobody says".
```

**Why it fails:** Name uses spaces and capital letters (should be `my-cool-skill`). Trigger phrase is something no real user would type. Never activates.

---

## 3. Workflow Instruction Examples (Good vs Bad)

### Good: Freedom labels, specific commands, clear ordering

```markdown
1. **Read config** [EXACT] — `cat .eslintrc.js | head -80`. Do not modify.
2. **Identify violations** [FREEFORM] — Use your judgement. Focus on rules
   that cause runtime errors, not stylistic preferences.
3. **Write fix** [GUIDED] — Run `npx eslint --fix` first. If autofix doesn't
   handle it, rewrite the affected block manually.
4. **Verify** [EXACT] — Run `npm run lint` and confirm zero errors.
```

**Why it works:** Each step has a freedom label. Exact steps say what to run and that it cannot be modified. Freeform steps give judgement criteria. Guided steps show workflow ordering (autofix first, then manual). Verification closes the loop.

### Bad: Ambiguous steps, no tools, no order

```markdown
1. Review the code
2. Find problems
3. Fix them
4. Make sure it's good
```

**Why it fails:** "Review how? Which tool? What kind of problems? Fix how? What does 'good' mean?" An AI with zero conversation history cannot execute this.

---

## 4. Explain-the-Why Examples (Before vs After)

### Example 1: Dependency injection

**Before:**
```
MUST use constructor injection. NEVER use field injection.
```

**After:**
```
Use constructor injection. Field injection breaks testability because
we cannot mock the field without Spring context. Constructor injection
makes dependencies explicit in tests.
```

### Example 2: Security validation

**Before:**
```
ALWAYS validate user input.
```

**After:**
```
Validate all user input at the controller boundary. Unvalidated input
is the root cause of injection attacks (SQL, XSS, command injection).
Use a schema validator library — manual validation is error-prone.
```

### Example 3: Error handling

**Before:**
```
NEVER catch exceptions silently.
```

**After:**
```
Never catch exceptions without logging or rethrowing. Silent catches
hide failures that cascade into hard-to-debug states. If you must
catch, log the error with context and either recover gracefully or
rethrow as a domain exception.
```

---

## 5. Gotcha Examples (Well-written vs Vague)

### Well-written: Symptom, cause, response — all three present

1. **Scanned PDFs return empty text arrays.** OCR-only PDFs have no selectable text layer. Check `page.textContent` length before extraction. If zero, fall back to OCR via `tesseract.js`.
2. **Windows path separator breaks glob patterns.** `\` is an escape character in most glob implementations. Always normalize paths with `path.resolve()` or use forward slashes.
3. **Rate-limited API calls return 429, not 5xx.** Default retry logic only retries 5xx. Add `429` to retry status list and implement exponential backoff.

**Why it works:** Each gotcha has a concrete symptom ("empty text arrays", "breaks glob patterns", "returns 429"), a root cause ("no selectable text layer", "escape character", "not in 5xx range"), and a specific action ("fall back to OCR", "normalize paths", "add 429 to retry list").

### Vague: No symptom, no cause, no action

1. **PDFs might not work.** Handle it.
2. **Windows is weird sometimes.** Be careful with paths.
3. **APIs can rate limit you.** Deal with it.

**Why it fails:** "Handle it" and "Deal with it" are abdications, not instructions. An AI with zero experience of these failures has no idea what to do. A vague gotcha is worse than none — it creates false confidence that the edge case is covered.
