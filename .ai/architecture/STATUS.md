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
- [x] Architecture Principles (12)
- [x] Phase Gate Review — **PASS WITH CONDITIONS** (2026-07-14)
- [x] Architecture Baseline v1 published

## Current Architecture Baseline

`.ai/architecture/architecture-baseline-v1.md` — Baseline v1, Architecture Version **1.0.0**

## Versions

- Architecture Version: 1.0.0
- Repository Version: v0.1.1

## Active Architecture Review

One architectural decision is open, so Architecture Baseline v1 §13 ("No architectural decisions are open") is no longer current.

**ADR-0013** — `docs/adr/0013-authority-conflict-no-synthesized-requirement-set.md`, status **proposed**. Refines how ADR-0005, ADR-0006, and ADR-0007 interact when more than one active authoritative binding matches a (policy identifier, repository) pair. Reverses no accepted ADR and adds no closed set. Raised by specification review of Vertical Slice 1 — Observe-Mode Tracer.

Downstream updates (Domain Model invariant 4, `CONTEXT.md`, the slice specification's authority selection / AC 5 / S5, phase plan story 16) are identified but deliberately **unapplied** pending review. Architecture Version remains 1.0.0 until acceptance; whether the invariant-4 refinement is a patch or a major bump under Baseline §19 — which does not distinguish an invariant *changed* from one *clarified* — is decided at acceptance.

## Current Objective

Review and approve the specification for Vertical Slice 1 — Observe-Mode Tracer. Blocked in part on ADR-0013 above: ADRs outrank specifications, so AC 5 and S5 cannot be finalized until it is accepted.

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
