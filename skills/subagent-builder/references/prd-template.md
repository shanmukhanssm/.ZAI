# PRD Template

Use this template when writing skill PRDs in Phase 2 Step 3. Each skill gets its own PRD file.

```markdown
# <skill-name> — PRD

## 1. Executive Summary

One paragraph describing what the skill does, why it's needed, and what it produces.

## 2. Key Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Output format | [SKILL.md / AGENTS.md / other] | Why this format fits |
| Language/tools | [language, frameworks] | Why these were chosen |
| Key constraint | [specific rule] | Why this constraint matters |

## 3. File Structure

```
skills/<skill-name>/
├── SKILL.md
├── references/
│   └── [reference files if needed]
└── scripts/
    └── [validation scripts if needed]
```

## 4. Content Outline

- What the SKILL.md covers (sections, workflow steps)
- What reference files contain
- What scripts validate

## 5. Edge Cases & Failure Modes

| Edge Case | Mitigation |
|---|---|
| [likely failure] | [how to handle it] |

## 6. Dependencies

- Skills this skill depends on
- Tools it needs access to
- Any platform-specific requirements
```
