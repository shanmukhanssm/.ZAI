# .ZAI — Shanmukh's Agent & Skill Library

Custom agents and skills for working with Shanmukh. This repo is the source of truth;
the working clone lives at `/home/z/my-project/desktop/.ZAI/` in the Z.ai workspace.

## Structure

- `agents/<name>/AGENTS.md` — agent definitions
- `agents/<name>/references/` — agent reference files (playbooks, strategy specs, templates)
- `agents/<name>/scripts/` — agent helper scripts (Python 3)
- `skills/<name>/SKILL.md` — skill packages (+ `references/`, `scripts/` as needed)

## Conventions

- Everything Shanmukh must see or download goes to `/home/z/my-project/download/`
- Agent working state (portfolios, data) lives in `/home/z/my-project/download/<agent-name>/`
- New agents and skills are created inside the local clone and pushed here
- Never commit secrets or tokens to this repo
