# Project Status

Last Updated: 2026-07-19

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

**Delivered:** Vertical Slice 1 **T0 — evidence spine** (PR #16), **T1 — smallest governed evaluation** (PR #19), **T2 — scope resolution, three-result contract & Unknown propagation** (PR #23, merge `8420200`), and **T3 — scope combinators (`any`/`all`/`not`) under three-valued logic** (PR #24, merge `daa802b`) are merged to `main`. Together they establish the two public seams, the frozen execution-integrity contract, a deterministic ungoverned execution, the minimal governed Compliant/Covered path, Cannot-Determine → Unknown applicability propagation, and recursive three-valued scope resolution; 14 tests green.

**Active next work item:** **T4 — authority conflict & effective periods** (Slice 1 of 7). Its blocking governance decision — the `Applicable`+`Unknown` authority-selection semantics, formerly open as **issue #22** — is now **resolved by ADR-0015** (accepted 2026-07-19; Architecture Version 1.0.3), which ratifies three-valued authority selection, the terminal authority-Unknown results, and the Unknown Classification. The proven-conflict and effective-period behavior remain defined by ADR-0005/0013 and ADR-0010. T4 implementation may begin with the first failing seam-level test against the ratified baseline; `select_authoritative_binding` currently fails loud on the undetermined case pending that implementation.

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

1. **(immediate, methodology track)** Validate the existing methodology prompts against the accepted methodology architecture — temporary; does not advance Phase 2.
2. Generate Vertical Slice 1 — Observe-Mode Tracer implementation tickets.
3. Implement and review Vertical Slice 1 — Observe-Mode Tracer.
4. Continue the Phase 2 Architecture Validation Sequence.

## Deferred

- Architecture-versioning rules — versioning by semantic change, and the Discovery/Refinement ADR distinction (evidence and proposal recorded under Architecture Refinements Since Baseline v1; revisit after Phase 2)
- Event-driven execution
- Automatic remediation
- Emergency-suspension path definition
- ServiceNow / CMDB integration
- Production evidence storage hardening
- AWS deployment
