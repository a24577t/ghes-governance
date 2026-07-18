# Repository Continuity Artifact

**Created:** 2026-07-18
**Authored on:** branch `context/methodology-refresh`, off `main` `fa54f66` (T0 merged via PR #16)

A temporary, single-use bridge (MADR-0001; `create-repository-continuity.md`). It carries only uncommitted, in-flight intent and **pointers** to authoritative artifacts — never a second copy of committed history. It is subordinate to authoritative repository state (the repository always prevails) and is retired once its content becomes committed authoritative state.

## Resume Context (pointers, not summaries)

- `.ai/architecture/STATUS.md` — last-stable state, version counters
- Architecture Baseline v1 + `docs/adr/` (0001–0014) — authoritative architecture
- `CONTEXT.md` — ubiquitous language
- `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — approved Slice 1 spec + the T0–T7 breakdown
- `docs/standards/engineering-standards.md` → `python-coding-standard.md` (Status: **Proposed**) + `.claude/skills/tdd/` — applicable standards + required method
- `.ai/methodology/` (lifecycle-model, principles, MADRs) + `.ai/prompts/methodology/operator-guide.md`

## Delivered — pointer only (not restated here)

T0's delivery and its review outcomes are committed authoritative history: see `.ai/architecture/STATUS.md` (records T0 merged) and PR #16 (merge commit `fa54f66`; commits `2ec2b99`/`a4bb6ee`). This artifact deliberately does not summarize completed work.

## Work Not Yet Committed / Must Remain Separate

- **`stash@{0}` — README review edits:** a separate task, intentionally excluded from T0, built on the **pre-rebase** README. `main`'s README is currently a minimal stub, so these edits must be **re-done against `main`'s README** when the README task resumes. **Do not restore** onto this or the T1 branch. (Content lives in git; not copied here.)
- **`stash@{1}`:** a pre-existing GitHub-Desktop stash on another branch — not ours; leave untouched.
- **Python Coding Standard + Engineering Standards hub** (`docs/standards/`): persisted on this branch as **Proposed**; **not authoritative** until adopted through governance (this branch's PR).
- **This refresh branch** (`context/methodology-refresh`): carries the standards, this artifact, the STATUS pointer, and the bootstrap updates; awaiting its own PR + governance adoption.

## Outstanding Decisions

- Governance adoption of the Python Coding Standard + Engineering Standards hub (this branch's PR).
- README authority statement + reconciliation of `stash@{0}` against `main`'s README (separate README task).

## Recommended Next Activity — T1 Implementation-Entry Gate

Active work item: **T1 — smallest governed evaluation → Compliant / Covered** (Slice 1 of 7). Begin only when **all** hold:

- **Predecessor:** T0 merged to `main` — satisfied (`fa54f66`).
- **Seams (confirm before writing any test):** the two public seams only — Execution boundary `run_execution`, Report Derivation `derive_reports`. No new public seam.
- **Method (required from T1):** Matt Pocock TDD (`.claude/skills/tdd/`) — confirm seams, **red before green**, minimal implementation, no internal side channels, independent expected values. Load the tdd skill before writing code.
- **Standards:** apply `python-coding-standard.md` (authoritative once the refresh PR merges); observe its "in force now" set and enforcement stages exactly as stated there — not restated here.
- **Scope (per the approved spec's T0–T7 breakdown):** one repository matched by one active **authoritative Observe** binding, one `PredicateEvaluation` condition → Policy Outcome `Compliant`, Coverage State `Covered`; introduces the minimal finding schema + required closed sets. Do **not** absorb T2/T3 scope.
- **Deferred — do not pull forward:** T6 duplicate-Execution-Identifier refusal; T7 item-level tamper fixtures; `StrEnum` enum migration (adoption ticket, must prove serialization unchanged); tooling installation (Ruff/mypy/coverage/CodeQL/Dependency Review/CI).
- **Authorization:** explicit human go-ahead to begin T1 implementation.

## Notes

Retire this artifact once the refresh branch merges (standards + bootstrap updates become authoritative and STATUS reflects T0-merged / T1-next); a T1 session then re-derives context from STATUS + this artifact + the spec.
