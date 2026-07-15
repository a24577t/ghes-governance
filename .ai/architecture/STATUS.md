# Project Status

Last Updated: 2026-07-15

## Current Phase

Phase 2 — Architecture Validation Sequence (specification stage)

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
- [x] ADR-0013 — refinement, **accepted** (2026-07-15)
- [x] Architecture Principles (12)
- [x] Phase Gate Review — **PASS WITH CONDITIONS** (2026-07-14)
- [x] Architecture Baseline v1 published

## Current Architecture Baseline

`.ai/architecture/architecture-baseline-v1.md` — Baseline v1. The baseline document records Architecture Version 1.0.0; the current Architecture Version is **1.0.1** (see Architecture Refinements Since Baseline v1). Baseline v2 is not published for this refinement.

## Versions

- Architecture Version: 1.0.1 (Baseline v1 records 1.0.0; see Architecture Refinements Since Baseline v1)
- Repository Version: v0.1.1

## Architecture Refinements Since Baseline v1

No architectural decisions are open. Baseline v1 §13 ("No architectural decisions are open") remains true, but its §1/§9 ADR range (0001–0012) and §19 Architecture Version (1.0.0) are superseded by the record below. Baseline v1 is immutable and is **not** edited; this section carries the reconciliation.

**ADR-0013 — Authority conflict: no synthesized requirement set.** `docs/adr/0013-authority-conflict-no-synthesized-requirement-set.md`, status **accepted** (2026-07-15). Refines how ADR-0005, ADR-0006, and ADR-0007 interact when more than one active authoritative binding matches a (policy identifier, repository) pair: each conflicting binding is still evaluated but only as explanatory evidence, never as an official governance outcome; requirement sets are never synthesized across conflicting policy versions; the pair's official Policy Outcome and Coverage State are both `Unknown`, the latter by a precedence-0 case decided before requirement-level aggregation. Reverses no accepted ADR, adds no capability, defines no new closed set. Raised by specification review of Vertical Slice 1 — Observe-Mode Tracer.

Applied downstream: Domain Model invariant 4 and header; `CONTEXT.md` (Authoritative Binding, Coverage State); the slice specification (authority selection, story 14, AC 5, S5, reference bundle); phase plan story 16.

**Architecture Version 1.0.1** — patch. No new capability, no reversal of an accepted decision, no new domain entity, no new closed set, no implementation incompatibility (nothing is built yet); it clarifies a previously under-specified interaction between existing ADRs.

**Baseline stays v1.** Baseline v2 is published at the next planned architectural milestone — completion of the Phase 2 Architecture Validation Sequence — not for this clarification. Baselines track project milestones, not every refinement.

**Methodology gaps this review exposed** (recorded, not yet acted on):

1. Baseline §19's version rules are too coarse: they do not distinguish an invariant *clarified* from an invariant *changed*, and read literally would have forced 2.0.0 here. Intended refinement — clarification → patch; behavioral change → minor; conceptual-model change or new invariant → major.
2. The methodology has no notion of a **Refinement ADR** as distinct from a discovery ADR. The pattern this review established: when specification review exposes a contradiction or gap between accepted ADRs, create a refinement ADR rather than editing accepted ADRs in place — and carry forward navigation from the next baseline, since the accepted ADRs cannot point forward to it.

## Current Objective

Review and approve the specification for Vertical Slice 1 — Observe-Mode Tracer. ADR-0013 is accepted and its downstream updates are applied; specification review resumes.

## Current Validation Sequence

Phase 2 validates the read-only governance architecture through seven sequenced vertical slices. See `phase-2-architecture-validation-plan.md`.

## Current Implementation Slice

**Vertical Slice 1 — Observe-Mode Tracer** (Slice 1 of 7). Specification: `docs/specifications/vertical-slice-1-observe-mode-tracer.md` — **Draft for review**.

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
- Evidence (append-only, content-hashed, manifest, execution status)
- Derived Reports (from stored evidence only)

No writes.

Delivered by later slices of the sequence, **not** by this slice: Desired-State Evaluation (2), Capability Matrix and Coverage Reasons (3), Governance Relief (4), Shadow Bindings (5), Dry-run Remediation Planning (6), Cross-Execution Operations (7).

## Next Milestones

1. Grill and approve Vertical Slice 1 — Observe-Mode Tracer
2. Generate implementation tickets
3. Implement and review Vertical Slice 1 — Observe-Mode Tracer
4. Continue the Phase 2 Architecture Validation Sequence

## Deferred

- Event-driven execution
- Automatic remediation
- Emergency-suspension path definition
- ServiceNow / CMDB integration
- Production evidence storage hardening
- AWS deployment
