# skill-builder-pro — SKILL.md Templates

## 1. Task Skill Template

For step-by-step workflow skills (deploy, commit-formatter, lint-runner).

### Frontmatter

```yaml
---
name: <kebab-case>
description: >-
  <one-line summary. Include trigger phrases the user would actually say.
  Do NOT use for: <near-miss scenarios to exclude>.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---
```
Note: Trigger phrases and exclusions go in `description: >-` (see Pattern 1-2 in the main SKILL.md). There are no separate `triggers` or `exclusions` frontmatter fields — they are not valid opencode frontmatter keys.

### Sections

- **Overview** — one paragraph describing purpose, assumptions, prerequisites
- **Execution Checklist** — copy-tick conditions that must be true before starting
- **Step-by-Step Workflow** — numbered steps with actions, verifications, edge case handling
- **Known Gotchas** — common pitfalls, why they happen, how to avoid them

### Complete Example

```yaml
---
name: commit-formatter
description: >-
  Formats git commit messages to Conventional Commits spec
  (type(scope): description). Trigger: "format commit",
  "write a commit message", "conventional commit".
  Do NOT use for: changelogs, release notes, interactive rebase,
  or amending without review.
allowed-tools:
  - Read
  - Bash
---
```

```markdown
# commit-formatter

## Overview

Validates and reformats staged commit messages against Conventional
Commits (`type(scope): description`). If invalid, rewrites interactively.

## Execution Checklist

- [ ] Staged files match the claimed scope
- [ ] Type is one of: feat, fix, chore, docs, refactor, test, style, perf
- [ ] Description is under 72 characters

## Step-by-Step Workflow

1. **Read the message** — `git log -1 --format=%s%n%n%b HEAD`.
2. **Parse** against regex `^(feat|fix|...)(\(.+\))?!?:\s.+`.
3. **If invalid**, print error and ask for a corrected message.
4. **Rewrite** with `git commit --amend -m "<corrected>"`.

**Examples:**
- `feat(auth): add OAuth2 PKCE flow` — valid
- `fix: handle empty cart checkout` — valid (no scope)
- `Fix the bug` — invalid (lowercase, missing colon)

## Known Gotchas

- Running inside `git rebase` amends wrong commit. Detect with
  `git rev-parse REBASE_HEAD` — abort if set.
- `--allow-empty` produces blank messages. Handle gracefully.
```

---

## 2. Reference Skill Template

For passive style-guide / knowledge-base skills (naming-conventions,
error-handling-patterns). No workflow — just reference material.

### Frontmatter

```yaml
---
name: <kebab-case>
description: >-
  <one-line summary of what this reference defines. Include enough
  context for discovery — e.g., "Defines naming conventions
  for files, variables, APIs, and database schemas.">
allowed-tools: []
---
```

### Sections

- **Purpose** — what this defines and who must follow it
- **Guidelines** — grouped by category (Files, Variables, API, DB, etc.)
- **Examples** — Good vs Bad table with reasons
- **References** — links to style guides, ADRs, source files

### Complete Example

```yaml
---
name: naming-conventions
description: >-
  Language-agnostic naming rules for files, variables, APIs, and database
  schemas. Useful when reviewing code for naming consistency.
allowed-tools: []
---
```

```markdown
# naming-conventions

## Purpose

Defines a single naming convention across all codebases. New code MUST
follow these rules. Reviewers MUST flag violations.

## Guidelines

**Files and directories:**
- Components: `PascalCase.tsx` — e.g. `UserProfile.tsx`
- Backend services: `kebab-case.ts` — e.g. `auth-service.ts`
- Tests: `<name>.test.ts` — mirrors source path

**Variables and functions:**
- Locals: `camelCase` — `const userCount = 0`
- Booleans: prefix with `is`, `has`, `should` — `isLoading`

**API routes:**
- Plural nouns: `/api/v1/users`
- Snake_case query params: `?sort_by=created_at`

**Database:**
- Tables: `snake_case`, plural — `user_sessions`
- FKs: `<singular>_id` — `user_id`

## Examples

| Good | Bad | Reason |
|------|-----|--------|
| `UserProfile.tsx` | `userProfile.tsx` | Components PascalCase |
| `/api/v1/users` | `/api/v1/getUsers` | Resources, not actions |
| `isAuthenticated` | `authenticated` | Missing boolean prefix |

## References

- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- ADR-003: DB naming (`docs/adr/003-db-naming.md`)
```

---

## 3. Hybrid Skill Template

Starts with a workflow, includes a reference section (lookup table, pattern
catalog). Use when a skill needs both procedure and knowledge base.

### Frontmatter

Same as Task Skill (`allowed-tools` required).

### Additional Section

Add `## Reference: <Topic>` after the workflow steps — usually a table
mapping operations to their implementations.

### Complete Example

```yaml
---
name: db-migration
description: >-
  Create, review, apply DB migrations with rollback support.
  Trigger: "create migration", "add migration", "schema change".
  Do NOT use for: seed data scripts, database backups, read-only
  queries, or production deploys.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---
```

```markdown
# db-migration

## Overview

Generates timestamped migration files with paired `up()` and `down()`,
applies them locally, and includes a reference of SQL patterns.

## Execution Checklist

- [ ] Filename has UTC timestamp prefix
- [ ] `down()` exactly reverses `up()` — tested by apply+rollback
- [ ] Destructive ops preceded by SELECT confirmation

## Step-by-Step Workflow

1. **Generate** — `npm run migrate:create <description>`.
2. **Write `up()`** — add schema change. Log affected rows before DROP/ALTER.
3. **Write `down()`** — exact reverse of `up()`. Test.
4. **Apply** — `npm run migrate:up`. Check for errors.
5. **Rollback test** — `npm run migrate:down`. Re-apply after.

**Examples:**
- Add column: `up=addColumn`, `down=dropColumn`
- Rename column: `up=renameColumn('users','name','full_name')`,
  `down=renameColumn('users','full_name','name')`
- New table: `up=createTable`, `down=dropTable`

## Reference: Common Migration Patterns

| Operation | `up()` | `down()` |
|-----------|--------|----------|
| Add column | `addColumn('users', 'avatar_url', 'text')` | `dropColumn('users', 'avatar_url')` |
| Rename column | `renameColumn('users', 'name', 'full_name')` | `renameColumn('users', 'full_name', 'name')` |
| Create index | `createIndex('orders', 'status')` | `dropIndex('orders', 'status')` |
| New table | `createTable('audit_logs', ...)` | `dropTable('audit_logs')` |

## Known Gotchas

- Never edit an already-applied migration — create a new one.
- Timestamps must be UTC (not local) to avoid ordering issues.
- Wrap multi-statement migrations in a transaction block.
```
