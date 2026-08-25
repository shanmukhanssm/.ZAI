# Gotchas — Skill Authoring Failure Modes

## 1. YAML Frontmatter Is Fragile

**Symptom:** Skill doesn't load. No error, no warning — it's silently skipped.
**Cause:** Invalid YAML in frontmatter (unclosed quotes, tabs, bad indentation, illegal characters).
**Correct response:** Validate frontmatter with a YAML linter before deploying. Use a tool like `yamllint` or paste into yamllint.com. Avoid angle brackets (`<`, `>`) in frontmatter — they can inject unintended instructions into the system prompt.

## 2. Description Is the Only Trigger Signal at Session Start

**Symptom:** Skill has perfect instructions but never activates.
**Cause:** The AI sees only `name` + `description` (~100 tokens) when deciding whether to load the skill. If the description phrasing doesn't match how the user asked, the skill never gets read.
**Correct response:** Write descriptions that mirror real user language. Test with actual user phrasings. Add synonyms in the description field. Don't rely on the body text to sell the skill — it won't be seen.

## 3. AI Undertriggers Skills

**Symptom:** AI keeps handling tasks manually instead of loading the skill.
**Cause:** The default behavior is to NOT use a skill unless the match is obvious. AI errs on the side of skipping.
**Correct response:** Make descriptions slightly pushy. Add explicit trigger phrases like "Use when user says X, Y, or Z." Assume the AI will rationalize NOT loading — counter that with concrete trigger language in both `description` and `when_to_use`.

## 4. `allowed-tools` Is Pre-Authorization, Not Restriction

**Symptom:** Skill loads but AI uses tools not in `allowed-tools`. Users expected restricted behavior.
**Cause:** `allowed-tools` only skips the approval prompt for listed tools. It does NOT block unlisted tools. The AI can still call any tool it has access to.
**Correct response:** Treat `allowed-tools` as a convenience list, not a security boundary. True tool restrictions must be enforced via platform permission rules (e.g., `.opencode/permissions.json`). Document this in your skill so users don't misunderstand.

## 5. Description + `when_to_use` Combined Truncation

**Symptom:** Key trigger phrases or descriptions get cut off.
**Cause:** Combined text of description + `when_to_use` is truncated at 1536 characters. Every sentence competes for limited space.
**Correct response:** Count characters. Lead with the most important activation language. Put secondary triggers later (they'll survive truncation). Avoid filler phrases. Test with `wc -c` to stay within limit.

## 6. Windows vs Unix Paths

**Symptom:** Commands fail on Windows. Script errors about unrecognized paths or missing files.
**Cause:** Skills often default to Unix paths (`/home/user/...`) and bash syntax. The user's platform determines what works.
**Correct response:** Default to Windows (PowerShell). Use forward slashes or escape backslashes. Scripts should use PowerShell cmdlets, not bash. Always note the platform assumption in the skill. Test on both platforms if cross-platform.

## 7. Skill Body Line Limit

**Symptom:** Instructions get corrupted. Claude misses sections or behaves inconsistently.
**Cause:** SKILL.md exceeds 300-500 lines. Long files fragment — Claude may not read the full content, especially in the middle of a session.
**Correct response:** Keep SKILL.md under 300-500 lines. Move detailed instructions to `references/` subfiles. Keep the main file scannable. Use short sections with clear headings.

## 8. Stale Gotchas

**Symptom:** Skill warns about bugs that don't exist or suggests workarounds for already-fixed issues.
**Cause:** Libraries update, APIs change, behavior patches land. A stale gotcha sends Claude chasing a problem that no longer exists.
**Correct response:** Add "last verified" notes with date and version info. Remove or update gotchas that produce false positives. Review periodically. A wrong gotcha is worse than no gotcha.

## 9. Reference Graph Depth

**Symptom:** Claude misses instructions stored in nested reference files.
**Cause:** SKILL.md → references/intermediate.md → details.md creates a chain two or more hops deep. Claude may partially read and miss targets.
**Correct response:** Keep it shallow. SKILL.md → references/details.md is one hop and safe. Two or more hops risks incomplete loading. If you must nest, put critical content in the first hop.

## 10. Conversation History Dependency

**Symptom:** Skill fails or produces nonsense when loaded in a fresh session.
**Cause:** Skill instructions reference "as discussed earlier" or assume pre-existing conversation context that doesn't exist in a new session.
**Correct response:** Every instruction must be self-contained. Assume zero session history. Repeat required context. Never rely on "as mentioned before" patterns. A skill should work identically whether it's the first message or the hundredth.
