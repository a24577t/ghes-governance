# Repository Continuity Artifact

**Updated:** 2026-07-21 (post methodology/collaboration-maintenance reconciliation; PRs #39–#51 merged; no implementation work in flight).
**Base:** `main` with Vertical Slice 1 **T0–T5 merged** (PRs #16, #19, #23, #24, #29, #35) on the ADR-0015-accepted baseline (PR #27), the methodology + standards refresh adopted (PR #17), the post-T4 status reconciliation (PR #34), and deterministic collaboration startup plus the Decision-Gated Implementation Lifecycle merged (PRs #30–#32, #26). The **Methodology Validation subsystem** was introduced (PR #37, merge `630301b`), followed by a round of methodology/collaboration maintenance (PRs #39–#51; see *Methodology & collaboration maintenance* below). `main` at merge `0ef0cba`: **34 tests green**.

A temporary, single-use bridge (MADR-0001; `create-repository-continuity.md`). It carries only uncommitted, in-flight intent and **pointers** to authoritative artifacts — never a second copy of committed history. Subordinate to authoritative repository state (the repository always prevails); retired or re-pointed as slices complete. It is **not required** for a clean, fully-committed, stable state; this instance records the current resume point only.

## Resume Context (pointers, not summaries)

- `.ai/architecture/STATUS.md` — last-stable state, version counters, and the authoritative current objective
- Architecture Baseline v1 + `docs/adr/` (0001–0015) — authoritative architecture
- `CONTEXT.md` — ubiquitous language
- `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — approved Slice 1 spec (T0–T7 increments)
- `docs/standards/engineering-standards.md` → `python-coding-standard.md` (**adopted, authoritative**) + `.claude/skills/tdd/` — applicable standards + required method
- `.ai/methodology/` (lifecycle-model, decision-gated-implementation-lifecycle, principles, MADRs) + `.ai/prompts/methodology/operator-guide.md`
- `.ai/methodology/validation/` — Methodology Validation subsystem: immutable observations **MO-001–MO-017** (non-authoritative evidence); **MVR-001** has adjudicated **MO-017 → Accepted**; MO-001–MO-016 remain unadjudicated

## In flight

- **This reconciliation** — a docs-only change recording the completed methodology/collaboration maintenance (PRs #39–#51; see *Methodology & collaboration maintenance* below) and the explicit **T6 entry-gate** (see *Recommended Next Activity — T6* below). **No implementation work is in flight**; **T6 remains the active next implementation work item and has not begun**.

## Delivered — pointer only (not restated here)

T0–T5 are committed authoritative history: see `.ai/architecture/STATUS.md` and PRs #16, #19, #23, #24, #29, #35. This artifact does not summarize completed work.

## Methodology & collaboration maintenance (completed)

Committed history (the PRs and `.ai/architecture/STATUS.md`); pointers only, not restated:

- **Review Discipline — MVR-001 (PR #39, merge `c567967`).** The Methodology Validation subsystem's first review accepted **MO-017**: independent reviews use repository artifacts (the PR diff / changed files) as **primary** evidence; an implementation report is supporting context only, and a quality-gate PASS is never issued from a summary alone. Authoritative in `.ai/prompts/methodology/review-discipline.md`.
- **Artifact Source Selection (PR #40, merge `3653b73`).** `session-bootstrap.md` fixes the source of each authoritative artifact deterministically — repository first; an explicitly provided copy only as subordinate transport; never inferred — applying MADR-0001 without reopening it.
- **Collaboration contract — startup ownership (PR #41, merge `ba994c6`).** An **Artifact ownership classification** invariant (classify each loaded artifact by owner; load order is acquisition order, not ownership) and a **Startup completion** terminology clause.
- **Collaboration contract — self-refinement & terminology (PR #42, merge `12ecdc3`).** A **Collaboration self-refinement** behavior (route recurring collaboration improvements into repository-governed refinements), an executable *response directed to the repository owner* conclusion invariant, and full **role-neutral** generalization of the former "Response for Claude" wording.
- **Collaboration/repository refresh model made explicit (PR #44, merge `bd39b06`).** Each artifact now states only the part it owns of the outgoing→incoming session refresh: **repository state and the durable collaboration contract are repository-carried** (the contract reloaded from the repository every session, never hand-carried); **only the refreshed collaboration avatar is manually transferred** by the repository owner (`avatar-bootstrap.md`, intentionally outside repository governance); **avatar generation belongs to outgoing-session closeout** (`collaboration-avatar-generator.md`, run while the outgoing context still exists); and **incoming startup consumes the supplied avatar and verifies repository state read-only** (`load-order.md` → durable contract → operator-guide S1 → `session-bootstrap.md`). The generator was renamed from a misspelled filename (atomic); two empty typo files were left for separate housekeeping.
- **Repository-transfer readiness gate on the avatar generator (PR #45, merge `f97dd59`).** `collaboration-avatar-generator.md` now makes avatar generation **conditional on repository-transfer readiness**. Before emitting refreshed `avatar-bootstrap.md` content it verifies, against **authoritative repository state**, that outgoing closeout is complete, `STATUS.md` and the continuity/reconciliation artifacts are current, the documented next activity agrees with actual state, and the avatar will not describe state newer than / absent from / inconsistent with the repository. The contract is deterministic: **PASS** generates the avatar and records the **verified repository baseline** without making the avatar authoritative for repository state; **FAIL** produces **no** avatar content and returns an explicit `AVATAR GENERATION REFUSED` response with the failed preconditions, executable remediation, and a rerun instruction. The gate **verifies but does not repair** — closeout, status, merge, and reconciliation remain operator-guide transitions. Narrow guarantee: refreshed avatar content is produced only after readiness was verified for the recorded baseline; an existing avatar does **not** imply a current repository, so incoming startup still independently verifies avatar/repository compatibility.
- **Avatar-generator category discipline (PR #46, merge `e564304`).** `collaboration-avatar-generator.md`'s Discover / Editorial / Validation workflow now evaluates collaboration **function, core principles, operational heuristics, practices, current model, abandoned directions, and deferred questions as distinct categories**, replaces narrative "Mental Model Evolution" with a reusable **Current Collaboration Model** category, tightens the **Abandoned-Directions** and **Deferred-Questions** gates, adds an **Output-structure** section, and extends **Exclude** (methodology; duplicated durable contract content) — so a generated avatar preserves both collaboration philosophy and operational discipline. The **ownership & lifecycle header** and the **repository-transfer readiness gate** are unchanged; no avatar was generated.
- **STATUS/continuity reconciliation recording PR #46 (PR #47, merge `6985aa5`).** A docs-only reconciliation folding the avatar-generator category-discipline change (PR #46) into `STATUS.md` and this artifact, and stating the explicit **T6 entry-gate**. No architecture, methodology, or version change.
- **Deterministic avatar output contract + legacy-file removal (PR #48, merge `34f0ac2`).** The generator's PASS path is a deterministic file emission — exactly the Repository-transfer Readiness statement, then the complete `avatar-bootstrap.md` contents; the avatar **is** the file, with no wrapper / artifact / code-fence / alternate presentation. Also removed the obsolete empty legacy file `create-bootstrap.coollaborator.md`. Ownership, readiness gate, editorial workflow, and avatar scope unchanged.
- **Evidence-based readiness gate — Repository Transfer Baseline (PR #49, merge `cf0a27b`).** The gate certifies readiness from repository **evidence**: either direct authoritative repository state, or a deterministic **Repository Transfer Baseline** captured from the actual repository immediately before generation — making the gate implementable by an engine without repository access while preserving repository authority (memory is never authoritative; the gate verifies but never repairs). FAIL triggers are explicit: evidence absent, reconciliation incomplete, authority unestablished, evidence internally inconsistent. Readiness semantics, ownership, authority model, editorial workflow, and output contract unchanged.
- **Two-part incoming-session bootstrap artifact (PR #51, merge `0ef0cba`).** The generated `avatar-bootstrap.md` is now a complete, self-contained artifact in two clearly separated parts: static, generator-owned **Bootstrap Instructions** (how to consume the avatar — supplementary collaboration context only; reconstruct repository state from the authoritative artifacts; the repository prevails on any conflict) then the **Collaboration Avatar** preserved unchanged as the separate durable collaboration-knowledge component. Documentation/output-structure only; no readiness-gate, baseline, ownership, editorial, validation, implementation, or T6 change. The static instructions and generator spec are authoritative in `collaboration-avatar-generator.md` and are not duplicated here.

Vertical Slice 1 **T0–T5 remain complete**; **T6 is the next implementation ticket and has not begun.**

## Recommended Next Activity — T6 (not started)

Next implementation work item: **T6 — validate execution-creation preconditions and the refusal lifecycle** (Slice 1 of 7). T5 fixed the outcome for an invalid bundle (a `Failed` Execution that still writes evidence); T6 establishes the distinct **pre-execution refusal** outcomes — a request refused before any Execution exists, producing no Execution Status and no authoritative evidence — for single-execution rights unavailable (AC 13 / S13) and Execution Identifier reuse (AC 15 / S15).

- **Predecessor:** T5 merged (PR #35) — satisfied.
- **Seams:** the two public seams only — `run_execution`, `derive_reports`. No new public seam.
- **Method:** TDD red-before-green (§12), in force from T1 onward.
- **Deferred — do not pull forward:** T7; predicate operators / aggregation precedence; `StrEnum` migration; tooling installation.

**T6 entry is gated — do not begin T6 before all of the following hold:**

1. all current maintenance and continuity work is **merged** (this reconciliation PR included);
2. the **release boundary is validated** — the repository is internally consistent, Repository Version `v0.3.0` equals the latest release tag, the test suite is green, `STATUS.md` and this artifact are accurate, links resolve, and the documented next activity is coherent;
3. the **outgoing avatar has been generated** from that validated baseline — the readiness-gated `collaboration-avatar-generator.md` returns **PASS** against it (a **FAIL** / `AVATAR GENERATION REFUSED` blocks the transfer);
4. the repository owner (**Eric**) **manually transfers** the generated avatar into the incoming session;
5. the **incoming session executes the repository startup sequence** (`load-order.md` → durable contract → operator-guide **S1** → `session-bootstrap.md`) and reports **Context Established**; and
6. the **T6 decision gate is explicitly opened**.

Creating an empty T6 branch from the validated `main` **does not** start T6: no T6 analysis, tests, code, or commits occur until the six conditions above hold.

## Work Not Yet Committed / Must Remain Separate

- **`stash@{0}` — README review edits:** a separate task built on the **pre-rebase** README; `main`'s README is a minimal stub, so these must be **re-done against `main`'s README** when the README task resumes. **Do not restore** onto a slice branch. (Content lives in git; not copied here.)
- **`stash@{1}`:** a pre-existing GitHub-Desktop stash on another branch — not ours; leave untouched.
- **Deferred methodology maintenance — issue #18** (Information Ownership / P8 + orphan consolidation): a dedicated maintenance PR, never during a slice.

## Notes

The instructor-architect contract is committed and **accepted** — no longer an uncommitted working-tree modification. The standards refresh is merged and authoritative; the Python Coding Standard is **Adopted**, no longer "Proposed."
