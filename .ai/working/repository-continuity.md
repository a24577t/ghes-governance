# Repository Continuity Artifact

**Updated:** 2026-07-19 (post-ADR-0015 acceptance)
**Base:** `main` with T0–T3 merged and **ADR-0015 accepted** (PRs #16, #19, #23, #24, #27) and the methodology refresh (PR #17) adopted. 14 tests green.
**Current branch:** `feat/slice1-t4-authority-conflict`, rebased onto the ADR-0015-accepted baseline.

A temporary, single-use bridge (MADR-0001; `create-repository-continuity.md`). It carries only uncommitted, in-flight intent and **pointers** to authoritative artifacts — never a second copy of committed history. Subordinate to authoritative repository state (the repository always prevails); retired or re-pointed as slices complete.

## Resume Context (pointers, not summaries)

- `.ai/architecture/STATUS.md` — last-stable state, version counters
- Architecture Baseline v1 + `docs/adr/` (0001–0014) — authoritative architecture
- `CONTEXT.md` — ubiquitous language
- `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — approved Slice 1 spec + the T0–T7 breakdown
- `docs/standards/engineering-standards.md` → `python-coding-standard.md` (**authoritative**) + `.claude/skills/tdd/` — applicable standards + required method
- `.ai/methodology/` (lifecycle-model, principles, MADRs) + `.ai/prompts/methodology/operator-guide.md`

## Delivered — pointer only (not restated here)

T0–T3 are committed authoritative history: see `.ai/architecture/STATUS.md` and PRs #16, #19, #23, #24. This artifact does not summarize completed work.

## Work Not Yet Committed / Must Remain Separate

- **`stash@{0}` — README review edits:** a separate task built on the **pre-rebase** README; `main`'s README is a minimal stub, so these must be **re-done against `main`'s README** when the README task resumes. **Do not restore** onto a slice branch. (Content lives in git; not copied here.)
- **`stash@{1}`:** a pre-existing GitHub-Desktop stash on another branch — not ours; leave untouched.
- **`.ai/collaboration/instructor-architect-contract.md`:** an uncommitted working-tree modification carried since before T0; outside every slice's scope, awaiting a one-time decision (commit separately / revert / leave). **Do not stage into a slice.**
- **Deferred methodology maintenance — issue #18** (Information Ownership / P8 + orphan consolidation): a dedicated maintenance PR, never during a slice.

## Recommended Next Activity — T4 Gate (governance decision settled)

Active work item: **T4 — authority conflict & effective periods** (Slice 1 of 7). Its governance decision is **settled** — T4 begins with the first failing seam-level test:

- **Governance decision (formerly issue #22) — RESOLVED by ADR-0015** (accepted 2026-07-19; Architecture Version 1.0.3): three-valued authority selection, the terminal authority-Unknown results, and the Unknown Classification are ratified. Implement as defined; do not re-decide. `select_authoritative_binding` still fails loud on the undetermined case, pending the T4 implementation.
- **Predecessor:** T3 merged and ADR-0015 accepted — satisfied (PR #24; PR #27).
- **Seams (confirm before writing any test):** the two public seams only — `run_execution`, `derive_reports`. No new public seam.
- **Method (required):** Matt Pocock TDD (`.claude/skills/tdd/`) — confirm seams, red before green, minimal implementation, no internal side channels, independent expected values.
- **Standards:** apply the authoritative `python-coding-standard.md`; observe its "in force now" set and enforcement stages.
- **Defined scope (ADR-0005/0013, ADR-0010):** proven authority conflict (≥2 active `Applicable` authoritative bindings → Policy Outcome and Coverage `Unknown`, no synthesized requirement set; the authority-conflict Unknown keeps Execution Status `Complete`, **not** `CompleteWithGaps`); effective-period activation under the fixed evaluation timestamp (half-open intervals).
- **Deferred — do not pull forward:** T5, T6, T7; predicate operators / aggregation precedence; `StrEnum` migration; tooling installation.
- **Authorization:** explicit human go-ahead to begin T4 (after the issue #22 decision).

## Notes

The methodology refresh (standards + bootstrap) is merged and authoritative; the standards are no longer "Proposed."
