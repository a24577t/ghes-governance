# Project Status

Last Updated: 2026-07-20

## Current Phase

Phase 2 — Architecture Validation Sequence (Vertical Slice 1 specification approved; sequence not complete)

## Terminology

Two distinct scopes were both being called "Vertical Slice 1". They are now named separately, and these names are used verbatim in all living artifacts:

- **Phase 2 Architecture Validation Sequence** — the full read-only architecture-validation scope: the union of every ADR's POC boundary, delivered as **seven sequenced slices**. This is what Architecture Baseline v1 §10 ("Current Scope (Vertical Slice 1 — read-only)") describes, and what its §17 next-baseline trigger fires on.
- **Vertical Slice 1 — Observe-Mode Tracer** — the current implementation slice only: Slice 1 of the seven. Specified in `docs/specifications/vertical-slice-1-observe-mode-tracer.md`.

Architecture Baseline v1 is immutable and predates this split; it is **not** edited. Where the baseline says "Vertical Slice 1", read **Phase 2 Architecture Validation Sequence**. This is a naming reconciliation only — no architectural decision changed, and no ADR is affected.

## Completed

- [x] Architecture Discovery (Phase 1)
- [x] Architecture Consolidation
- [x] Ubiquitous Language (`CONTEXT.md`)
- [x] Domain Model
- [x] ADRs 0001–0012 — all **accepted** (2026-07-14)
- [x] ADR-0013, ADR-0014 — refinements, **accepted** (2026-07-15)
- [x] Architecture Principles (12)
- [x] Phase Gate Review — **PASS WITH CONDITIONS** (2026-07-14)
- [x] Architecture Baseline v1 published
- [x] Vertical Slice 1 — Observe-Mode Tracer specification — reviewed and **approved / implementation-ready** (2026-07-16)
- [x] AI-Assisted Engineering Methodology architecture — **accepted** (MADR-0001, MADR-0002, principles P1–P7, lifecycle model, glossary; `.ai/methodology/`), released **v0.3.0**. Project-independent and agent-neutral; does not change the GHES architecture.
- [x] Deterministic collaboration startup — repository maintenance (PR #30, merge `a999298`). Collaborator startup is now **deterministic**: `.ai/collaboration/load-order.md` is the single entry-point manifest → contract (role / authority / prohibitions, now **accepted**) → shared operator-guide S1 → session-bootstrap. Also corrected stale references (Engineering Standards hub Proposed → Adopted; ADR range → 0001–0015) and superseded `.ai/prompts/project/project-lifecycle.md`. Repository-process only; no change to the GHES architecture, methodology, or Architecture Version.
- [x] **Methodology Validation subsystem** introduced (PR #37, merge `630301b`). A first-class `.ai/methodology/validation/` subsystem — a README charter, an immutable append-only `observations.md`, and a `reviews/` scaffold — capturing implementation-derived evidence about the methodology, keeping evidence, adjudication, and authority separate. Observations **MO-001–MO-017** are recorded as **non-authoritative validation evidence**; **MVR-001** subsequently adjudicated **MO-017 → Accepted** (PR #39), and MO-001–MO-016 remain unadjudicated. Repository-process and methodology-design only; changes no GHES platform architecture or Architecture Version and does not advance Phase 2. **T6 remains the active next implementation work item.**
- [x] **Methodology & collaboration maintenance** (PRs #39–#45). A block of **repository-process / documentation** refinements that change no GHES platform architecture or Architecture Version and do not advance Phase 2: **MVR-001** adjudicated observation **MO-017 → Accepted**, making repository artifacts (PR diff / changed files) the **primary** review evidence (PR #39, merge `c567967`); deterministic **Artifact Source Selection** in `session-bootstrap.md` (PR #40, merge `3653b73`); collaboration-contract **artifact-ownership classification** and **self-refinement** behavior, with full role-neutral generalization of the former "Response for Claude" wording (PRs #41–#42, merges `ba994c6` / `12ecdc3`); the **collaboration/repository refresh ownership model** made explicit across the collaboration layer — the repository carries all durable project state and the durable contract (reloaded every session), while **only the refreshed avatar** (`avatar-bootstrap.md`) is manually transferred by the repository owner, and avatar generation belongs to **outgoing-session closeout**, never to incoming startup (PR #44, merge `bd39b06`); and a **repository-transfer readiness gate** on `collaboration-avatar-generator.md` — avatar generation is **refused** (`AVATAR GENERATION REFUSED`, no avatar content) unless the outgoing repository is verified closed-out, reconciled, and current, under a deterministic **PASS/FAIL** contract that **verifies but does not repair** and records the verified repository baseline without making the avatar authoritative for repository state (PR #45, merge `f97dd59`). **T6 remains the active next implementation work item and has not begun.**

## Current Architecture Baseline

`.ai/architecture/architecture-baseline-v1.md` — Baseline v1. The baseline document records Architecture Version 1.0.0; the current Architecture Version is **1.0.3** (see Architecture Refinements Since Baseline v1). Baseline v2 is not published for this refinement.

## Versions

- Architecture Version: 1.0.3 (Baseline v1 records 1.0.0; see Architecture Refinements Since Baseline v1)
- Repository Version: v0.3.0

**Repository Version** tracks the latest repository-wide release tag. It is a single generic field: it does not distinguish product from methodology release streams. Architectural maturity is tracked separately by **Architecture Version** (1.0.3) and **Architecture Baseline** (v1); a repository release does not change either, and Baseline v1 / Architecture Version 1.0.3 remain current. Independent release streams, if ever needed, require explicit version fields or separate repositories — they are not inferred through this field.

### Repository releases

- **v0.3.0** — accepted AI-Assisted Engineering Methodology architecture (`.ai/methodology/`). No change to the GHES architecture.
- **v0.2.0** — architecture refinements ADR-0013 and ADR-0014, and the Vertical Slice 1 — Observe-Mode Tracer specification review.
- **v0.1.1 / v0.1.0** — earlier project releases (Baseline v1 era).

## Architecture Refinements Since Baseline v1

No architectural decisions are open. Baseline v1 §13 ("No architectural decisions are open") remains true, but its §1/§9 ADR range (0001–0012) and §19 Architecture Version (1.0.0) are superseded by the record below. Baseline v1 is immutable and is **not** edited; this section carries the reconciliation.

**ADR-0013 — Authority conflict: no synthesized requirement set.** `docs/adr/0013-authority-conflict-no-synthesized-requirement-set.md`, status **accepted** (2026-07-15). Refines how ADR-0005, ADR-0006, and ADR-0007 interact when more than one active authoritative binding matches a (policy identifier, repository) pair: each conflicting binding is still evaluated but only as explanatory evidence, never as an official governance outcome; requirement sets are never synthesized across conflicting policy versions; the pair's official Policy Outcome and Coverage State are both `Unknown`, the latter by a precedence-0 case decided before requirement-level aggregation. Reverses no accepted ADR, adds no capability, defines no new closed set. Raised by specification review of Vertical Slice 1 — Observe-Mode Tracer.

Applied downstream: Domain Model invariant 4 and header; `CONTEXT.md` (Authoritative Binding, Coverage State); the slice specification (authority selection, story 14, AC 5, S5, reference bundle); phase plan story 16.

**ADR-0014 — Execution Digest: a versioned root commitment to an Execution's evidence.** `docs/adr/0014-execution-digest-root-commitment.md`, status **accepted** (2026-07-15). ADR-0009 names "execution digest" among Authoritative Evidence contents but never defines it, and the term appeared nowhere else in the repository — a specification could not supply it, because the term is architectural. ADR-0014 defines the Execution Digest as the deterministic, versioned root commitment to an Execution's evidence; version 1 is the canonical content hash of the Execution Manifest, and is the only supported computation. The digest is recorded outside the manifest (a manifest containing its own hash is self-referential) and verified during evidence validation before Derived Reports are generated; a recomputed/recorded mismatch fails verification as tamper-suspect, with neither value presumed trustworthy. Raised by specification review of Vertical Slice 1 — Observe-Mode Tracer.

Applied downstream: `CONTEXT.md` (Execution Digest); Domain Model (evidence entities, relationships, header); the slice specification (Solution step 7, Execution boundary and Report Derivation seams, stories 23 and 32, digest recording location and verification point, AC 10, S10).

**ADR-0015 — Three-valued authority selection: undeterminable authority is distinct from proven conflict and from absent authority.** `docs/adr/0015-three-valued-authority-selection.md`, status **accepted** (2026-07-19). Refines ADR-0005 and ADR-0013 for the three-valued applicability of ADR-0003: a candidate authoritative binding whose scope applicability is `Unknown` is neither counted as authority nor excluded; authority-undeterminable — one applicable binding with an undetermined competitor, or two or more undetermined candidates with none applicable — yields a terminal pair-level Policy Outcome and Coverage State `Unknown` with Execution Status `CompleteWithGaps`, distinct from proven conflict (`Complete`) and from absent authority. Introduces the minimal two-member Unknown Classification closed set (`IncompleteObservation` / `GovernanceResult`), from which Execution Status derives. Reverses no accepted ADR; completes a previously-undefined case rather than adding a capability. Resolves issue #22; raised during Vertical Slice 1 T2/T3 implementation.

Applied downstream: `CONTEXT.md` (Authoritative Binding, Execution Status, Unknown Classification); Domain Model (invariant 4, closed-set inventory); the slice specification (authority selection §141, Execution Status rule §137, AC 3, AC 17, story 36, S17, reference bundle). Navigation carry-forward: the next Architecture Baseline links to ADR-0015 from ADR-0005 and ADR-0013 (Baseline v1 is immutable and not edited). This advances the Architecture Version to **1.0.3** — patch, on the same basis as 1.0.1/1.0.2: it completes previously-undefined (three-valued authority selection) and previously-required-but-undefined (ADR-0010's "Unknown counts with reasons") architecture, breaks no conforming implementation (none is built yet), and the new closed set completes an already-required concept rather than adding a capability.

**Architecture Version 1.0.2** — patch, on the same reasoning as 1.0.1. ADR-0013 and ADR-0014 each add no capability, reverse no accepted decision, and create no implementation incompatibility (nothing is built yet). ADR-0014 defines a term ADR-0009 already required rather than introducing a new concept, and its one Domain Model entity row records an architectural fact that was already implied. Both clarify previously under-specified architecture.

**Baseline stays v1.** Baseline v2 is published at the next planned architectural milestone — completion of the Phase 2 Architecture Validation Sequence — not for this clarification. Baselines track project milestones, not every refinement.

**Architecture Versioning Rules — Deferred (revisit after Phase 2 completes; do not act on this now).**

Baseline v1 and its §19 are **not** to be modified while the methodology is still being exercised. The proposal below is recorded so the evidence survives; it is deliberately not applied, because Phase 2 will produce more evidence about what the rules should be, and changing the methodology mid-validation would remove the very evidence we are gathering.

*The evidence so far — the same issue, twice in one review:*

1. **ADR-0013** refined an accepted invariant (Domain Model invariant 4) without changing architectural semantics.
2. **ADR-0014** completed an already-required architectural concept (ADR-0009's undefined "execution digest") without adding new behaviour; the Domain Model gained an entity row because it was **incomplete, not incorrect**.

In both cases Baseline §19 read literally forces a **major** version — because the Domain Model or an invariant was edited — while both are semantically clarifications. Both were classified **patch** (1.0.1, 1.0.2). The root cause: **§19 keys on whether an artifact was edited; it should key on semantic architectural change.**

*Proposed replacement for §19's bump guidance (not applied):*

- **Patch (1.0.x)** — clarification of existing architectural intent; completion of previously implied concepts; contradiction resolution; refinement ADRs that do not change externally observable architectural behaviour.
- **Minor (1.x.0)** — backward-compatible architectural capability additions.
- **Major (x.0.0)** — changes to architectural semantics or invariants that would make a **previously conforming implementation non-conforming**.

The major test is the operational one: it is decidable, where "did the Domain Model change?" is merely observable.

*Proposed ADR taxonomy (not applied):*

- **Discovery ADR** — a Phase 1 architectural decision.
- **Refinement ADR** — a post-baseline clarification discovered during specification or implementation review. When such review exposes a contradiction or gap between accepted ADRs, create a refinement ADR rather than editing accepted ADRs in place; and carry forward navigation from the next baseline, since accepted ADRs cannot point forward to it. ADR-0013 and ADR-0014 are the first two instances of this pattern.

## Current Objective

**Delivered (merged to `main`):** Vertical Slice 1 **T0 — evidence spine** (PR #16), **T1 — smallest governed evaluation** (PR #19), **T2 — scope resolution, three-result contract & Unknown propagation** (PR #23, merge `8420200`), **T3 — scope combinators (`any`/`all`/`not`) under three-valued logic** (PR #24, merge `daa802b`), **T4 — authority conflict & effective periods** (PR #29, merge `496cfad`), and **T5 — full desired-state bundle validation** (PR #35, merge `0557fc8`). Together they establish the two public seams, the frozen execution-integrity contract, a deterministic ungoverned execution, the minimal governed Compliant/Covered path, Cannot-Determine → Unknown applicability propagation, recursive three-valued scope resolution, the full ADR-0015 authority-selection decision table, and whole-bundle desired-state validation producing deterministic Failed Executions; **34 tests green on `main`**.

**T4 detail (delivered, PR #29).** The **ADR-0015 authority-selection decision table is fully implemented and covered** by seam-level tests — every row: ungoverned (A=0/U=0), single-Applicable governed (A=1/U=0), proven conflict (A≥2 → one terminal official Policy/Coverage `Unknown`, `authority_conflict`, `GovernanceResult`, Execution Status `Complete`), authority-undeterminable (A=1/U≥1 and A=0/U≥2 → `Unknown`, `authority_undeterminable`, `IncompleteObservation`, `CompleteWithGaps`), and single-Unknown scope-undetermined (A=0/U=1). **AC 5 / S5 / §147 (proven conflict across divergent policy versions) is implemented**: two overlapping authoritative bindings on divergent versions (v1 `{R1,R2}`, v2 `{R1,R3}`) yield the single terminal official `Unknown` result plus per-binding **explanatory-only** requirement evidence evaluated under each binding's own version, an `authority_conflict` finding recording both binding identities, versions, requirement sets, and the explicit shared / only-in-each requirement-set divergence, and **no synthesized official aggregate** (ADR-0013 no-synthesis exercised, not merely stated); explanatory evidence never reaches official compliance, coverage, or accounting. Execution Status derives from the recorded Unknown Classification. Policy documents are indexed by `(id, version)` so each policy-id × repository pair is processed exactly once and a binding resolves its declared version to its own requirement set; `select_authoritative_binding` fails loud only on genuinely unsupported inputs, and the engine also fails loud with a contextual `BundleError` on a **duplicate policy `(id, version)` document** and on a **binding that references an absent policy version** (full bundle validation is deferred to T5). The **effective-period boundary contract (S7/AC7) is covered by characterization** — `test_effective_periods.py` verifies the half-open `[start, end)` behavior through the seam (active at `effective_start`, inactive at `effective_end`, inactive future-dated); `_binding_active` implements it (T1).

**T5 detail (delivered, PR #35).** Whole-bundle desired-state **validation** runs after the Execution exists but before discovery or evaluation (Execution Lifecycle): a structurally malformed or semantically unsupported bundle — including unsupported content that appears unreferenced, and hidden content other than a `.gitkeep` placeholder — ends the Execution `Failed` with configuration evidence naming every validation error and the offending artifact, and **no** authoritative compliance or coverage results. It is a `Failed` Execution, never a raised error and never a pre-execution refusal. The Failed evidence flows through the frozen integrity chain (canonical evidence → Execution Manifest → external Execution Digest), so a Failed Execution is byte-deterministic and tamper-evident like any other. T5 also folds T4's interim `BundleError` guards (duplicate policy `(id, version)`; a binding referencing an absent policy version) into this Failed path (AC 12 / S12).

**Active next work item:** **T6 — validate execution-creation preconditions and the refusal lifecycle** (Slice 1 of 7). Not started; no branch open. Where T5 fixes the outcome for an *invalid bundle* — a `Failed` Execution that still writes evidence — T6 establishes the distinct **pre-execution refusal** outcomes: a request whose Execution-creation preconditions are unmet is refused before any Execution exists, so no Execution Status is produced and no authoritative evidence is written. The two cases are single-execution rights unavailable (AC 13 / S13) and Execution Identifier reuse (AC 15 / S15). The ticket is authored via the normal spec-derived process when its turn comes.

**T6 entry is gated.** T6 may not begin until: (1) all current maintenance and continuity work is **merged**; (2) the **release boundary is validated** — repository internally consistent, Repository Version `v0.3.0` equal to the latest release tag, test suite green, `STATUS.md` and the Repository Continuity Artifact accurate, links resolving; (3) the **outgoing avatar is generated** from that validated baseline — the readiness-gated `../collaboration/collaboration-avatar-generator.md` returns **PASS**; (4) the repository owner **manually transfers** that avatar into the incoming session; (5) the **incoming session** runs the startup sequence and reports **Context Established**; and (6) the **T6 decision gate is explicitly opened**. Creating an empty T6 branch from the validated `main` does **not** start T6.

**Authoritative standards:** the Engineering Standards hub and Python Coding Standard (`docs/standards/`) are adopted (PR #17) and authoritative.

## Current Validation Sequence

Phase 2 validates the read-only governance architecture through seven sequenced vertical slices. See `phase-2-architecture-validation-plan.md`.

## Current Implementation Slice

**Vertical Slice 1 — Observe-Mode Tracer** (Slice 1 of 7). Specification: `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — **approved, implementation-ready** (`ready-for-agent` candidate).

The thinnest complete execution path through every architectural layer, run manually against a synthetic GHES estate.

Capabilities:

- Desired-state bundle loading and schema validation (at pinned versions)
- Discovery
- Inventory (universal, unconditional)
- Scope Resolution (GitHub-native attribute provider, three-result contract)
- Authoritative binding selection (zero / one / conflict)
- Predicate Evaluation (via strategy dispatch)
- Composite Policy Evaluation
- Compliance aggregation
- Coverage aggregation (structure complete; reasons unreachable until Slices 3–4)
- Evidence (append-only, content-hashed, manifest, execution digest, execution status)
- Derived Reports (from stored evidence only)

No writes.

Delivered by later slices of the sequence, **not** by this slice: Desired-State Evaluation (2), Capability Matrix and Coverage Reasons (3), Governance Relief (4), Shadow Bindings (5), Dry-run Remediation Planning (6), Cross-Execution Operations (7).

## Next Milestones

1. **(methodology track)** Validate the existing methodology prompts against the accepted methodology architecture — temporary; does not advance Phase 2.
2. Continue Vertical Slice 1 — Observe-Mode Tracer implementation: **T6 (execution-creation preconditions & refusal lifecycle) next**, then T7, each reviewed and merged. (T0–T5 delivered.)
3. Continue the Phase 2 Architecture Validation Sequence (Slices 2–7).
4. Publish Architecture Baseline v2 at sequence completion (Baseline v1 §17 trigger).

## Deferred

- Architecture-versioning rules — versioning by semantic change, and the Discovery/Refinement ADR distinction (evidence and proposal recorded under Architecture Refinements Since Baseline v1; revisit after Phase 2)
- Collaboration contract engine-neutrality — generalize the contract's "Response for Claude" handoff wording to a neutral "implementation participant" (recorded during PR #30 final review; not required for deterministic startup; drive by observed operational need)
- Event-driven execution
- Automatic remediation
- Emergency-suspension path definition
- ServiceNow / CMDB integration
- Production evidence storage hardening
- AWS deployment
