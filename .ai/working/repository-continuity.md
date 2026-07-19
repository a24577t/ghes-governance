# Repository Continuity Artifact

**Updated:** 2026-07-19 (post-ADR-0015 acceptance; AC5/S5/§147 divergent-conflict implemented)
**Base:** `main` with T0–T3 merged and **ADR-0015 accepted** (PRs #16, #19, #23, #24, #27) and the methodology refresh (PR #17) adopted. Base main: 14 tests green.
**Current branch:** `feat/slice1-t4-authority-conflict` (PR #29), rebased onto the ADR-0015-accepted baseline. 19 tests green.

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

## Recommended Next Activity — T4 (authority selection & effective periods implemented; final review of PR #29)

Active work item: **T4 — authority conflict & effective periods** (Slice 1 of 7), in review on `feat/slice1-t4-authority-conflict` (PR #29, not merged).

- **ADR-0015 authority-selection decision table — implemented and covered.** Every row has a seam-level test: ungoverned (A=0/U=0), single-Applicable governed (A=1/U=0), proven conflict (A≥2 → `Complete`, `GovernanceResult`, `authority_conflict`), authority-undeterminable (A=1/U≥1 and A=0/U≥2 → `CompleteWithGaps`, `IncompleteObservation`, `authority_undeterminable` naming candidates and their undetermined attributes), single-Unknown scope-undetermined (A=0/U=1). Execution Status derives from the recorded Unknown Classification.
- **AC 5 / S5 / §147 — proven conflict across divergent policy versions — implemented and covered.** A conflict between two authoritative bindings on divergent versions (v1 `{R1,R2}`, v2 `{R1,R3}`) produces one terminal official `Unknown`/`Unknown` (`GovernanceResult`, `Complete`, `evaluated=0`), per-binding **explanatory-only** requirement evidence under each binding's own version, an `authority_conflict` finding recording both binding identities, versions, requirement sets, and the explicit shared / only-in-each requirement-set divergence, and **no synthesized official aggregate** (ADR-0013 no-synthesis exercised). Explanatory evidence never reaches official compliance, coverage, or accounting. Policy documents are indexed by `(id, version)` so each policy-id × repository pair is processed once and a binding resolves its declared version to its own requirement set.
- **New fail-loud guards.** The engine raises a contextual `BundleError` on a **duplicate policy `(id, version)` document** and on a **binding referencing an absent policy version** (full bundle validation remains T5).
- **Effective-period boundary (S7/AC7) — covered by characterization.** `test_effective_periods.py` verifies the half-open `[start, end)` contract through the seam (active at `effective_start`; inactive at `effective_end`; inactive future-dated). `_binding_active` implements the activation (T1).
- **Predecessor:** T3 merged and ADR-0015 accepted — satisfied (PR #24; PR #27).
- **Seams:** the two public seams only — `run_execution`, `derive_reports`. No new public seam.
- **Deferred — do not pull forward:** T5, T6, T7; predicate operators / aggregation precedence; `StrEnum` migration; tooling installation.

## Notes

The methodology refresh (standards + bootstrap) is merged and authoritative; the standards are no longer "Proposed."
