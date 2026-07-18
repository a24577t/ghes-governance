# Engineering Standards

**Status: Proposed** — this hub and the standards it indexes become authoritative only after adoption through the repository's governance process (PR + review).

A **thin index**. It links to the authoritative source for each area and defines **no rule of its own**; it never duplicates a linked source. Where this hub and a linked source differ, the linked source wins.

| Area | Authoritative source |
|---|---|
| Development process & lifecycle | `.ai/methodology/` (lifecycle-model, principles, MADRs) + `.ai/prompts/methodology/operator-guide.md` |
| Architecture & decisions | Architecture Baseline v1 (`.ai/architecture/`) + `docs/adr/` (0001–0014) + `CONTEXT.md` |
| Reviews | `.claude/skills/code-review/` and `.claude/skills/codebase-design/` |
| Testing method (required from T1 onward) | `.claude/skills/tdd/` |
| Python & language rules | [`python-coding-standard.md`](python-coding-standard.md) |
| Repository governance (Git, tickets, triage) | `CLAUDE.md` + GitHub rulesets (`RequirePR`, `Release Tags`) + `docs/agents/` |

Owned here: only the index.
