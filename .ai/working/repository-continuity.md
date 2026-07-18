# Repository Continuity Artifact

**Updated:** 2026-07-18 (post-T1 merge)
**Base:** `main` with T0 (PR #16) and T1 (PR #19) merged and the methodology refresh (PR #17) adopted.

A temporary, single-use bridge (MADR-0001; `create-repository-continuity.md`). It carries only uncommitted, in-flight intent and **pointers** to authoritative artifacts — never a second copy of committed history. Subordinate to authoritative repository state (the repository always prevails); retired or re-pointed as slices complete.

## Resume Context (pointers, not summaries)

- `.ai/architecture/STATUS.md` — last-stable state, version counters
- Architecture Baseline v1 + `docs/adr/` (0001–0014) — authoritative architecture
- `CONTEXT.md` — ubiquitous language
- `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — approved Slice 1 spec + the T0–T7 breakdown
- `docs/standards/engineering-standards.md` → `python-coding-standard.md` (**authoritative**) + `.claude/skills/tdd/` — applicable standards + required method
- `.ai/methodology/` (lifecycle-model, principles, MADRs) + `.ai/prompts/methodology/operator-guide.md`

## Delivered — pointer only (not restated here)

T0 and T1 are committed authoritative history: see `.ai/architecture/STATUS.md` and PRs #16 and #19. This artifact does not summarize completed work.

## Work Not Yet Committed / Must Remain Separate

- **`stash@{0}` — README review edits:** a separate task built on the **pre-rebase** README; `main`'s README is a minimal stub, so these must be **re-done against `main`'s README** when the README task resumes. **Do not restore** onto a slice branch. (Content lives in git; not copied here.)
- **`stash@{1}`:** a pre-existing GitHub-Desktop stash on another branch — not ours; leave untouched.
- **`.ai/collaboration/instructor-architect-contract.md`:** an uncommitted working-tree modification carried since before T0; outside every slice's scope, awaiting a one-time decision (commit separately / revert / leave). **Do not stage into a slice.**
- **Deferred methodology maintenance — issue #18** (Information Ownership / P8 + orphan consolidation): a dedicated maintenance PR, never during a slice.

## Recommended Next Activity — T2 Implementation-Entry Gate

Active work item: **T2 — scope resolution, three-result contract & Unknown propagation** (Slice 1 of 7). Begin only when **all** hold:

- **Predecessor:** T1 merged to `main` — satisfied (PR #19).
- **Seams (confirm before writing any test):** the two public seams only — `run_execution`, `derive_reports`. No new public seam.
- **Method (required):** Matt Pocock TDD (`.claude/skills/tdd/`) — confirm seams, red before green, minimal implementation, no internal side channels, independent expected values.
- **Standards:** apply the now-authoritative `python-coding-standard.md`; observe its "in force now" set and enforcement stages as stated there.
- **Scope (approved spec, AC 3 / S3):** the GitHub-native attribute provider under the three-result contract (Value Present / Value Absent / Cannot Determine); scope expressions with `all`/`any`/`not` under the shared truth table; a `Cannot Determine` on a required operand → `Unknown` applicability, propagating to Coverage `Unknown` and Execution Status `CompleteWithGaps`; where determined operands alone force the result, that result stands. Do **not** absorb T3 (full predicate / aggregation / combinator-divergent-cell verification) or T4 (authority conflict).
- **Deferred — do not pull forward:** T3, T4, T5, T6, T7; `StrEnum` enum migration; tooling installation.
- **Authorization:** explicit human go-ahead to begin T2.

## Notes

The methodology refresh (standards + bootstrap) is merged and authoritative; the standards are no longer "Proposed."
