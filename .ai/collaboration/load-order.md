# Collaboration Startup — Load Order

**Type:** collaboration startup manifest. **Owner:** human (Eric), collaboration layer.
**Audience:** the participant assigned the **Instructor / Architect / Reviewer / Quality Gate** function.

This is the **single deterministic entry point** for the collaboration participant. It is engine-neutral: any capable engine — or a human — assigned this function starts here.

This manifest owns **only**: the collaboration entry, the required load order, the required / conditional / on-demand classification, the hand-off into shared project-state startup, and the startup-verification checklist.

It **does not** define — and never restates — methodology or lifecycle rules, architecture or decisions, project state or versions, the implementation workflow, or the role authority and prohibitions themselves. Each of those has its own owner; this manifest only **points** to them. Where this manifest and an owning artifact differ, the owning artifact prevails.

## Start here (required, in order)

1. **This manifest** — you are at the collaboration entry point.
2. **Role, authority, prohibitions** — read the collaboration contract:
   [`instructor-architect-contract.md`](instructor-architect-contract.md). It is the sole owner of what your function is, what authority you hold, and what you must not do. This manifest does not repeat it.
3. **Hand off to shared project-state startup** — from here, startup is shared with every participant and is owned by the methodology, not by this layer:
   - [`../prompts/methodology/operator-guide.md`](../prompts/methodology/operator-guide.md) → **S1**, which runs
   - [`../prompts/methodology/session-bootstrap.md`](../prompts/methodology/session-bootstrap.md) — establishes the current project state and verifies the repository, read-only.
4. **Return** — after bootstrap reports *Context Established*, control returns to the operator-guide to route the next transition, or to your collaborator activity (architecture / review / quality-gate / teaching). This manifest is read **once per session**; it is not re-run.

## Artifact classification

Do not load an artifact merely because it is useful. Load the required chain every session; load the rest only when its situation applies.

**Required every session** — the entry chain above:
- this manifest → the collaboration contract → operator-guide **S1** → session-bootstrap.

**Conditional — load when the situation applies:**
- *Resuming in-flight work* — the Repository Continuity Artifact ([`../working/repository-continuity.md`](../working/repository-continuity.md)) is read *by* session-bootstrap as subordinate context; no separate load.
- *Acting as reviewer* — [`../prompts/methodology/review-discipline.md`](../prompts/methodology/review-discipline.md) (finding classification).
- *Running a phase / quality gate* — [`../prompts/methodology/phase-gate-review.md`](../prompts/methodology/phase-gate-review.md).
- *Architecture / methodology work* — the methodology unit ([`../methodology/`](../methodology/)) and the architecture domain (Baseline, `docs/adr/`, `CONTEXT.md`), reached through the operator-guide — not restated here.
- *Reviewing implementation* — the applicable standards ([`../../docs/standards/engineering-standards.md`](../../docs/standards/engineering-standards.md)) and the active specification.

**On demand — reference only when relevant:**
- Cross-project, engine-neutral collaboration heuristics — [`avatar-bootstrap.md`](avatar-bootstrap.md).
- Historical / evolution records (discovery briefs, session summaries) — explanatory only, never authoritative.

## Transition into shared startup

The boundary between this layer and shared startup is **step 3**. Everything from the operator-guide onward is shared with the implementation participant and owned by the methodology. This manifest neither duplicates nor overrides it: it routes to it and expects control back at step 4.

## Startup verification checklist

A newly assigned collaborator — and Eric, verifying the collaborator — confirm startup was followed correctly when all of these hold:

- [ ] Entered at this manifest (`load-order.md`).
- [ ] Read the collaboration contract and can state the assigned **role**, **authority**, and **prohibitions** from it.
- [ ] Ran the shared operator-guide **S1** → session-bootstrap.
- [ ] Bootstrap reported an outcome — *Context Established* or *Bootstrap Failed* — with its checks; a failure routed to Remediation and did **not** proceed to work.
- [ ] Loaded only the conditional / on-demand artifacts the situation required.
- [ ] Restated no methodology, architecture, project state, or contract authority — pointers only.
