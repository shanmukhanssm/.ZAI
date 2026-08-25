# exa-research - Output Templates

## Summary Template (Step 7)

Use this structure when presenting research results to the user inline.

```
## Research: [Topic]

**Angles explored:** [N] (Direct, Alternative, Negation, Niche, Emerging, Semantic)
**Subqueries executed:** [total across all agents]
**Unique sources consulted:** [total unique URLs]
**Hidden gems found:** [N]

### Consensus Findings (reported by 3+ angles)
1. [Finding] --- [confidence: HIGH/MEDIUM/LOW]
   Source: [URL]
2. [Finding] --- [confidence]
   Source: [URL]

### Hidden Gems (reported by 1-2 angles, non-obvious)

If hidden gems were found:
 Hidden Gem: [Finding]
   Angle: [which angle found it]
   Why hidden: [why standard search would miss this]
   Source: [URL]
   Why matters: [what makes this finding valuable]

If NO hidden gems were found:
No hidden gems — this topic is well-covered by mainstream sources.

### Contradictions Found
- [Claim A] (sources: [URLs]) vs [Claim B] (sources: [URLs])

### Gaps Identified
- [Subtopic or question with insufficient coverage]

### Key Sources
- [URL] --- [angle that found it, what it contains]
- [URL] --- [angle that found it, what it contains]

---

Want a full detailed report saved to file? Say "generate report".
```

## Full Report Template (Step 8)

Use this when the user requests a full saved report. Read this file, then expand findings into the structure below.

```markdown
# Deep Research Report: [Topic]

**Generated:** [current date]
**Method:** exa-research (multi-angle parallel subagent dispatch)
**Angles explored:** [N] (list of angles used)
**Subqueries executed:** [total]
**Unique sources consulted:** [total]

---

## Executive Summary

[2-3 paragraphs summarizing the most important findings]

---

## Consensus Findings

### [Finding 1] (HIGH confidence)
**Reported by:** [N] angles (Direct, Alternative, ...)
**Sources:** [URLs]
[Detailed description of the finding]

### [Finding 2] (HIGH confidence)
**Reported by:** [N] angles
**Sources:** [URLs]
[Detailed description of the finding]

---

## Hidden Gems

### Hidden Gem 1: [Title]
**Discovered by:** [Angle name]
**Why standard search misses this:** [explanation]
**Source:** [URL]
**Confidence:** [HIGH/MEDIUM/LOW]
**Why it matters:** [what makes this finding valuable or interesting]

### Hidden Gem 2: [Title]
**Discovered by:** [Angle name]
**Why standard search misses this:** [explanation]
**Source:** [URL]
**Confidence:** [HIGH/MEDIUM/LOW]
**Why it matters:** [what makes this finding valuable or interesting]

---

## Deep Dive by Angle

### Direct Angle
**Focus:** Mainstream understanding
**Queries executed:** [N]
**Key findings:**
- [Finding]

### Alternative Angle
**Focus:** Different approaches and comparisons
**Queries executed:** [N]
**Key findings:**
- [Finding]

### Negation/Criticism Angle
**Focus:** Limitations, drawbacks, counter-arguments
**Queries executed:** [N]
**Key findings:**
- [Finding]

### Niche/Community Angle
**Focus:** Forums, obscure sources, underground knowledge
**Queries executed:** [N]
**Key findings:**
- [Finding]

### Emerging/Future Angle
**Focus:** Latest developments and trends
**Queries executed:** [N]
**Key findings:**
- [Finding]

### Semantic/Conceptual Angle
**Focus:** Conceptually related connections
**Queries executed:** [N]
**Key findings:**
- [Finding]

---

## Contradictions and Disagreements

| Claim | Supporting Sources | Opposing Sources |
|-------|-------------------|------------------|
| [Claim] | [URLs] | [URLs] |

---

## Gaps and Blind Spots

- [Subtopic or question that was not adequately covered]
- [Reason why it was not covered]
- [Suggestions for further research]

---

## Sources Appendix

| Source URL | Found By Angle | Relevance | Recency |
|-----------|---------------|-----------|---------|
| [URL] | Direct | [high/medium/low] | [date] |
| [URL] | Niche | [high/medium/low] | [date] |
| [URL] | Semantic | [high/medium/low] | [date] |
