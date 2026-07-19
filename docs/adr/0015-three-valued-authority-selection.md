---
status: proposed
---

# Three-valued authority selection: undeterminable authority is distinct from proven conflict and from absent authority

## Context

This ADR **refines** ADR-0005 (explicit binding authority) and ADR-0013 (authority conflict). It does **not** replace or reverse them. It is **necessitated by** the three-valued applicability introduced in ADR-0003 — `Applicable` / `NotApplicable` / `Unknown` — which ADR-0005 and ADR-0013 predate: both reason about bindings that *match* (scope resolves `Applicable`) and are silent on a candidate authoritative binding whose **scope applicability is itself `Unknown`**. Vertical Slice 1's scope-combinator work made that state reachable and recorded it as an open decision (issue #22).

The refinement extends authority selection from two-valued (matches / doesn't) to three-valued selection. It adds no capability, introduces no new closed set, and leaves ADR-0005's authority bound and ADR-0013's proven-conflict and absent-authority cases exactly as they stand.

## Authority Selection Invariant

**A binding whose applicability is `Unknown` is neither counted nor excluded during authority determination.** It is not counted as a definite authority — it cannot establish "exactly one authority governs" and cannot, by itself, constitute a conflict — and it is not excluded — it is not treated as `NotApplicable` or as absent. It remains a **candidate whose unresolved applicability prevents any conclusion that depends on its exclusion.** "This pair is governed by exactly one authority" and "this pair is ungoverned" both require excluding the `Unknown` candidate, so neither may be concluded while it stands. Only a conclusion that does *not* depend on excluding it — a proven conflict already forced by two or more `Applicable` candidates — may be drawn.

Every row of the decision below is a consequence of this invariant.

## Decision

Authority selection resolves each active authoritative binding's scope for a (policy identifier, repository) pair to `Applicable` / `NotApplicable` / `Unknown` at the fixed timestamp (ADR-0003). `NotApplicable` candidates **are recorded in scope evidence but take no part in authority selection**. With A = the count of `Applicable` candidates and U = the count of `Unknown` candidates:

- **A=0, U=0 — ungoverned.** No declared authority applies; the pair carries neither Policy Outcome nor Coverage State and appears only in inventory, binding provenance, and the ungoverned report category (unchanged from ADR-0005 and Slice 1 scenario S4). *Absent* authority — not to be confused with *undeterminable* authority below.
- **A≥2 — proven authority conflict** (ADR-0013, unchanged). Two or more candidates *definitely* apply, so the authority bound is definitely violated: official Policy Outcome `Unknown` and Coverage State `Unknown`, no synthesized requirement set, an authority-conflict finding. The result is forced by the `Applicable` candidates alone; per the invariant, additional `Unknown` candidates cannot change it.
- **A=1 & U≥1, or A=0 & U≥2 — authority undeterminable.** Authority cannot be established: whether a second authority also governs (A=1) or whether any single authority governs (A=0 & U≥2) turns on scope applicability that could not be determined, and the invariant forbids excluding the `Unknown` candidates to reach either conclusion. Official Policy Outcome and Coverage State are both `Unknown` (ADR-0005: preserve the bound by refusing interpretation, never picking a winner; ADR-0013: ambiguous intent is `Unknown` in both dimensions, distinct from absent intent). Distinct from proven conflict (authority is not *known* violated, only *not known* satisfied) and from ungoverned (declared authority exists; only its applicability is undeterminable).
- **A=0 & U=1 — scope-undetermined single candidate** (ADR-0003, Slice 1 scenario S3). A lone authoritative binding whose scope is `CannotDetermine` yields pair-level `Unknown` in both dimensions. No competing authority exists, so no authority finding is emitted — the `Unknown` is fully explained by scope evidence.

## Authority-undeterminable finding

An **authority-undeterminable** finding is emitted only when uncertainty prevents authority selection — specifically when it prevents (a) selecting among two or more candidates (A=0 & U≥2), or (b) confirming that a definitely-`Applicable` candidate is uniquely authoritative (A=1 & U≥1). It is **not** emitted for a single undetermined candidate with no competitor (A=0 & U=1). It enumerates the candidate bindings and, per `Unknown` candidate, the scope attribute(s) that could not be determined. It is a governance finding, not an execution error, and is carried by finding reason and content — it adds no closed set (ADR-0013's no-new-closed-set reasoning applies unchanged).

## Execution Status is determined by incomplete-observation reasons

Execution Status reflects completeness of **observation**, not the presence of `Unknown` outcomes. A pair-level `Unknown` contributes `CompleteWithGaps` **only** when it arose from incomplete observation — a `CannotDetermine` scope/attribute result (ADR-0003). An `Unknown` from **authority ambiguity with all candidate scopes determined** — the proven-conflict case — is a governance finding, not incomplete observation, and keeps Execution Status `Complete`. Consequently:

- Proven conflict (A≥2) stays `Complete` even when additional `Unknown` candidates coexist, because the conflict result is already forced and the undetermined candidates are not decision-relevant to it (report the gap only when the answer depends on what is not known).
- Authority-undeterminable (A=1 & U≥1; A=0 & U≥2) and scope-undetermined (A=0 & U=1) are `CompleteWithGaps`: each `Unknown` depends on a scope value that could not be determined.

## Representation — no new closed set

No new `PolicyOutcome` / `CoverageState` / `ExecutionStatus` value (all reuse `Unknown` / `CompleteWithGaps`); no new finding-type enumeration. The only representational requirement is that completeness accounting distinguish, per `Unknown` pair, **whether it arose from incomplete observation** — which ADR-0010 already mandates ("Unknown counts with reasons"). Slice 1 needs exactly two reasons (incomplete-observation versus authority-ambiguity), and Execution Status is a function of whether any is incomplete-observation. This is the minimum change — expressible as a per-`Unknown` observation-incomplete predicate — and is deliberately **not** a broad `UnknownReason` taxonomy; a wider vocabulary, if ever needed, is a separate decision.

## Consequences

- ADR-0005 and ADR-0013's authority reasoning extends from two-valued (matches / doesn't) to three-valued (Applicable / Unknown / NotApplicable) selection; their proven-conflict and absent-authority cases are unchanged.
- The engine derives Execution Status from incomplete-observation reasons, not from the `Unknown` count — correcting a shortcut valid only while every `Unknown` was scope-caused.
- Issue #22 is resolved by this ADR.
- The next Architecture Baseline carries forward navigation to this ADR from ADR-0005 and ADR-0013; STATUS.md records ADR-0015 among the refinements since Baseline v1 on acceptance.
