# Methodology Validation — Observations

Immutable, append-only evidence about the methodology in practice. See [`README.md`](README.md)
for the subsystem's purpose, authority boundaries, and lifecycle.

**Recording an observation conveys zero methodology or design authority.** An entry is verifiable
evidence and its observed impact only — no recommendation, no remedy, no disposition. Entries are
immutable: each `MO-NNN` is written once and never edited or reused. Disposition lives only in the
review records under [`reviews/`](reviews/); an entry that no review references is unadjudicated.
Any implementation or review participant may append a new entry.

Origin batch: **T0–T5 implementation of Vertical Slice 1 — Observe-Mode Tracer** (Phase 2).

---

## Strengths

### MO-001 — Seam-only testing acted as a regression net
- **Area:** Testing Discipline
- **Kind:** Strength
- **Origin:** T5 implementation, 2026-07-20 (observed across T0–T5)
- **Evidence:** T5 added `src/ghes_governance/validation.py`, a new `bundle_validation` evidence type, and a Failed-Execution path; the 19 pre-existing tests were unmodified and stayed green. Internal refactors during T5 — `_scan_artifact_dir`, and extracting `reporting._item_payload` — changed no test. Tests import only `run_execution`/`derive_reports` (`tests/conftest.py`).
- **Observation:** New external behaviour and internal refactoring were both accommodated without editing existing tests.
- **Impact:** T5 regression risk was low; internal structure changed freely behind the two seams.
- **Related artifacts:** VS1 spec Testing Decisions; `docs/standards/python-coding-standard.md` §5/§12; `tests/conftest.py`.

### MO-002 — The frozen integrity chain yielded determinism and tamper-evidence without extra work
- **Area:** Standards (integrity contract)
- **Kind:** Strength
- **Origin:** T5, 2026-07-20
- **Evidence:** The Failed Execution's two evidence items routed through `write_execution` unchanged; the evidence was byte-identical across two independent stores (`test_failed_execution_evidence_is_byte_deterministic`) and passed `derive_reports`' verify-before-derive (digest, then item hashes) without a bespoke path.
- **Observation:** A new evidence-producing outcome inherited AC-2 determinism and AC-10 tamper-evidence via the existing canonical → manifest → digest chain.
- **Impact:** No integrity or serialization reasoning was required for the new path.
- **Related artifacts:** `docs/standards/python-coding-standard.md` §5/§10; `docs/adr/0009-evidence-logs-reports-retention.md`; `docs/adr/0014-execution-digest-root-commitment.md`; `src/ghes_governance/store.py`, `src/ghes_governance/canonical.py`.

### MO-003 — The Execution Lifecycle section pre-settled the central T5 question
- **Area:** Specification
- **Kind:** Strength
- **Origin:** T5, 2026-07-20
- **Evidence:** Whether an invalid bundle is a `Failed` Execution or a pre-execution refusal was answered by the VS1 spec's Execution Lifecycle section (lines 89–105, including "Desired-state bundle validity is not a precondition… produces a `Failed` Execution… never a refusal") and the AC 12 vs AC 13/AC 15 contrast, with stated rationale ("the difference is structural, not an arbitrary exception").
- **Observation:** The hardest lifecycle decision in T5 was ratified in advance, with reasoning, in the approved specification.
- **Impact:** No halt/decision excursion was needed for the Failed-vs-refusal boundary.
- **Related artifacts:** `docs/specifications/vertical-slice-1-observe-mode-tracer.md` (Execution Lifecycle; AC 12/13/15); `.ai/methodology/decision-gated-implementation-lifecycle.md`.

### MO-004 — The specification delegates concrete encodings to the implementation ticket
- **Area:** DGIL
- **Kind:** Strength
- **Origin:** T5, 2026-07-20
- **Evidence:** The desired-state `schema_version` field name, value, and absence-handling were undefined by `CONTEXT.md`, the domain model, and the ADRs, but the VS1 spec's Implementation Decisions line 137 states "Concrete encoding … is left to the implementation ticket, constrained only by canonical serialization and determinism."
- **Observation:** An explicit specification clause distinguished a local encoding choice from an architecture decision.
- **Impact:** The `schema_version` choice proceeded as a documented local decision rather than triggering a halt.
- **Related artifacts:** `docs/specifications/vertical-slice-1-observe-mode-tracer.md` (Implementation Decisions, line 137); `.ai/methodology/decision-gated-implementation-lifecycle.md` (governing principle).

### MO-005 — Layered review caught real "silent ignoring" defects twice
- **Area:** Review Discipline
- **Kind:** Strength
- **Origin:** T5, 2026-07-20
- **Evidence:** The code-review Spec axis flagged stray non-YAML content silently skipped inside supported directories (fixed in commit `0adebbf`); the subsequent independent quality gate flagged hidden unsupported content (`.relief/`, `.policy-experimental.yaml`) silently accepted by a broad `startswith(".")` skip (fixed in commit `5ed0872`). Both contradicted VS1 spec line 138 ("Silent ignoring or downgrading would infer intent").
- **Observation:** Two distinct incomplete implementations of "no silent ignoring" were caught by two successive review layers.
- **Impact:** Two genuine correctness gaps were removed before merge.
- **Related artifacts:** `code-review` skill; `.ai/methodology/decision-gated-implementation-lifecycle.md` (Verify-diff / Architecture Conformance Review); `docs/specifications/vertical-slice-1-observe-mode-tracer.md` line 138.

### MO-006 — Bootstrap's two-outcome discipline caught recorded-state staleness
- **Area:** Bootstrap
- **Kind:** Strength
- **Origin:** Session start, 2026-07-19
- **Evidence:** Session bootstrap returned Bootstrap Failed because STATUS's Current Objective and the continuity artifact both described T4 / PR #29 as "in review", while PR #29 (merge `496cfad`) and four later PRs (#30, #31, #32, #26) were merged. The "surface divergence, never silently act; Bootstrap Failed → Remediation" rule routed to remediation (PR #34).
- **Observation:** A verifiable precondition detected a real divergence between derived summaries and committed history.
- **Impact:** Work did not proceed on a stale premise; the discrepancy was remediated first.
- **Related artifacts:** `.ai/prompts/methodology/session-bootstrap.md`; `.ai/architecture/STATUS.md`; `.ai/working/repository-continuity.md`; `.ai/methodology/adr/0001-repository-authoritative-continuity.md`.

## Frictions

### MO-007 — "Vertical Slice 1" names two axes, and tickets are a third
- **Area:** Slicing & Ticketing
- **Kind:** Friction
- **Origin:** T5 scoping, 2026-07-20 (the structure predates T5)
- **Evidence:** `STATUS.md` carries a Terminology section reconciling "Phase 2 Architecture Validation Sequence" (7 slices) with "Vertical Slice 1 — Observe-Mode Tracer" (Slice 1 of 7); within Slice 1, tickets are T0–T7. "Seven sequenced slices" and "T0–T7" (eight tickets) both appear.
- **Observation:** Three numbering axes (slices-of-phase, the named Slice 1, tickets-within-slice) coexist and share the "Vertical Slice 1" label.
- **Impact:** Scoping T5 required continuously distinguishing "Slice 1 of 7" from "T5 of T0–T7".
- **Related artifacts:** `.ai/architecture/STATUS.md` (Terminology); `docs/specifications/phase-2-architecture-validation-plan.md`; `docs/specifications/vertical-slice-1-observe-mode-tracer.md`.

### MO-008 — Ticket definitions are implicit and scattered; no single source
- **Area:** Slicing & Ticketing
- **Kind:** Friction
- **Origin:** T5 scoping, 2026-07-20
- **Evidence:** T5's scope was assembled from the `src/ghes_governance/bundle.py` docstring ("Full structural and semantic bundle validation… is ticket T5"), the continuity artifact ("full bundle validation remains T5"), and `docs/standards/python-coding-standard.md` ("the T6 duplicate-Execution-Identifier… remains deferred"); the mapping T5 = AC 12 + S12 was inferred. A grep of the VS1 spec for "T5"/"T0–T7" returned nothing, though the continuity artifact cited "the T0–T7 breakdown" as being in the spec. A STATUS Next-Milestone read "Generate Vertical Slice 1 implementation tickets" while T0–T4 were already built.
- **Observation:** No per-ticket artifact defines a ticket's scope or acceptance; the T0–T7 breakdown cited as being in the spec is not present there.
- **Impact:** Determining "what exactly is T5" required triangulating three artifacts and confirming an inferred acceptance-criteria mapping.
- **Related artifacts:** `docs/specifications/vertical-slice-1-observe-mode-tracer.md`; `.ai/working/repository-continuity.md`; `docs/standards/python-coding-standard.md`; `.ai/architecture/STATUS.md`.

### MO-009 — STATUS and continuity require duplicated manual field-sync each cycle
- **Area:** STATUS/Continuity
- **Kind:** Friction
- **Origin:** T4 and T5 reconciliations, 2026-07-19 / 2026-07-20
- **Evidence:** The post-T4 (PR #34) and post-T5 (PR #36) reconciliations each hand-updated the same fields in two files: the green-test integer (14 → 19 → 34), the delivered-ticket list, the PR list, the Active Next Work Item, and the deferred list. The post-T4 continuity artifact still read "`docs/adr/` (0001–0014)" when the repository was at ADR-0015. The skipped instance after T4 produced the divergence recorded in MO-006.
- **Observation:** Several integers and lists are duplicated across `STATUS.md` and `repository-continuity.md` and are updated by hand after each merge.
- **Impact:** Each merge carries a manual, cross-file sync step; a skipped instance produced a stale, bootstrap-failing baseline.
- **Related artifacts:** `.ai/architecture/STATUS.md`; `.ai/working/repository-continuity.md`; `.ai/prompts/methodology/session-bootstrap.md`.

### MO-010 — Derived prose restates code and spec, and drifts
- **Area:** STATUS/Continuity
- **Kind:** Friction
- **Origin:** T5 reconciliation, 2026-07-20
- **Evidence:** `STATUS.md` carries multi-paragraph "T4 detail" and "T5 detail" summaries restating ADR-0015, the divergent-conflict behaviour, and the validation semantics already present in the spec, the ADRs, the code docstrings, and the tests; writing the "T5 detail" paragraph re-narrated the `validation.py` module docstring and the test file.
- **Observation:** Ticket-detail prose in STATUS duplicates content that also lives in spec, ADR, code, and tests.
- **Impact:** The same behaviour is described in multiple places that must be kept consistent by hand.
- **Related artifacts:** `.ai/architecture/STATUS.md`; `docs/specifications/vertical-slice-1-observe-mode-tracer.md`; `docs/adr/`; `src/ghes_governance/` docstrings; `tests/`.

### MO-011 — Two pull requests per ticket, with an inherent staleness window
- **Area:** Workflow
- **Kind:** Friction
- **Origin:** T4 / T5, 2026-07-19 / 2026-07-20
- **Evidence:** T5 produced an implementation PR (#35) and a separate reconciliation PR (#36); the reconciliation can only land after the implementation merges, leaving STATUS stale between merge `0557fc8` (T5) and merge `c60b076` (reconciliation). The equivalent T4 window is where the divergence in MO-006 arose.
- **Observation:** Documentation is reconciled in a second PR after each implementation PR, so STATUS trails committed reality for a window after every merge.
- **Impact:** A mandatory second PR per ticket, plus a defined interval during which the summaries are known-stale.
- **Related artifacts:** `.ai/architecture/STATUS.md`; `.ai/working/repository-continuity.md`; `CLAUDE.md` (git workflow).

### MO-012 — Fixture valid-baseline is duplicated across scenarios
- **Area:** Testing Discipline
- **Kind:** Friction
- **Origin:** T5, 2026-07-20
- **Evidence:** T5 added 12 `invalid-*` fixture directories under `tests/fixtures/`, most being a valid policy + valid binding + one defect; `policy-baseline.yaml` and `binding-baseline.yaml` were re-emitted across the ~12 directories.
- **Observation:** The scenario-per-directory pattern reproduces the same valid baseline in many fixtures.
- **Impact:** A change to the shared valid baseline would require editing many fixture copies.
- **Related artifacts:** `docs/specifications/vertical-slice-1-observe-mode-tracer.md` (Testing Decisions); `tests/fixtures/`.

### MO-013 — Aspirational-versus-enforced tooling carries a rediscovery cost
- **Area:** Standards
- **Kind:** Friction
- **Origin:** T5, 2026-07-20
- **Evidence:** `docs/standards/python-coding-standard.md` §4 mandates mypy strict, but at Document stage; tooling installation is deferred; mypy was absent from `.venv` (system mypy 2.1.0 was used). Running it surfaced a pre-existing `src/ghes_governance/evaluation.py:131` no-any-return in T2/T3 code (`return next(iter(expression))`).
- **Observation:** A mandated check is neither installed nor passing, and its enforced-versus-documented status must be re-derived per contributor.
- **Impact:** mypy was run manually; a pre-existing violation of the aspired standard exists on `main`.
- **Related artifacts:** `docs/standards/python-coding-standard.md` §2/§4; `pyproject.toml`; `src/ghes_governance/evaluation.py`.

### MO-014 — A boundary case sat on the DGIL halt/proceed line
- **Area:** DGIL
- **Kind:** Friction
- **Origin:** T5, 2026-07-20
- **Evidence:** The DGIL's "genuine decision point" list is authority / applicability / aggregation / integrity; "desired-state bundle format" is not among them. Classifying the `schema_version` encoding as a local decision (proceed) rather than an architecture decision (halt) required interpretation, resolved by the spec's line-137 delegation (MO-004).
- **Observation:** A real case fell between the DGIL's enumerated decision points and required adjudication before the local-versus-architecture classification was clear.
- **Impact:** Determining "proceed, don't halt" took extended reasoning for one T5 sub-decision.
- **Related artifacts:** `.ai/methodology/decision-gated-implementation-lifecycle.md` (governing principle); `docs/specifications/vertical-slice-1-observe-mode-tracer.md` line 137.

## Tradeoffs

### MO-015 — "No silent ignoring, even hidden" was subtle enough to under-implement
- **Area:** Specification
- **Kind:** Tradeoff
- **Origin:** T5, 2026-07-20
- **Evidence:** The VS1 spec line-138 requirement (reject unsupported content whole-bundle, even unreferenced) was violated in two distinct ways during T5 (see MO-005) before being fully met.
- **Observation:** A single ratified requirement admitted two separate incomplete implementations.
- **Impact:** Two review rounds were needed to fully satisfy one requirement.
- **Related artifacts:** `docs/specifications/vertical-slice-1-observe-mode-tracer.md` line 138; MO-005.

### MO-016 — Startup-chain ceremony versus continuing-implementation need
- **Area:** Bootstrap
- **Kind:** Tradeoff
- **Origin:** Session start, 2026-07-19
- **Evidence:** The documented startup chain is load-order → contract → operator-guide S1 → session-bootstrap. For continuing T5 implementation the load-bearing artifacts were the spec, `CONTEXT.md`, the ADRs, the code, and the DGIL. Caveat: this session entered at session-bootstrap, not the top of the chain, so the full chain was not traversed as friction.
- **Observation:** The startup chain targets cold-start collaborator onboarding; a continuing implementation session's load-bearing inputs were a subset of it.
- **Impact:** Recorded with the stated caveat; limited direct evidence.
- **Related artifacts:** `.ai/collaboration/load-order.md`; `.ai/collaboration/instructor-architect-contract.md`; `.ai/prompts/methodology/operator-guide.md`; `.ai/prompts/methodology/session-bootstrap.md`.
