---
status: accepted
---

# Authority conflict: no synthesized requirement set

ADR-0005 requires every matching binding to be evaluated independently, and makes the official outcome `Unknown` when more than one active authoritative binding matches a (policy identifier, repository) pair. It does not define the relationship between those per-binding results, the pair's official requirement outcomes, and the divergent requirement sets that conflicting policy versions may legitimately carry (ADR-0006). ADR-0007 derives Coverage State solely by aggregation over intended requirements, which has no defined input when authority is ambiguous. This ADR refines how ADR-0005, ADR-0006, and ADR-0007 interact in that case. It reverses nothing in them, introduces no new closed set, adds no capability, and defines no new status or property of a binding.

## Considered options

**Synthesize a union of requirement sets across conflicting policy versions** (v1 `{R1, R2}` + v2 `{R1, R3}` → `{R1, R2, R3}`) was considered and rejected. The union is a requirement set no approved policy version declares. Producing official requirement outcomes for it would manufacture an unapproved composite policy, contradicting explicit intent and destroying provenance — the engine would report against a policy shape no one authored or approved.

**Intersect the requirement sets** (→ `{R1}`) was considered and rejected: requirements that a declared authority intended would silently disappear from the estate's answer because two bindings disagreed. Uncertainty would remove a control — Principle 3 and Invariant 2, *uncertainty never grants privilege*.

**Select one binding** by any mechanical rule is the hidden precedence ADR-0005 already forbids.

The rejected options share a root error: treating an authority conflict as a question about *requirements*. It is a question about *authority*. When authority is ambiguous the intended control set is not merely disputed — it is undeterminable, because determining it requires choosing a policy version, which is precisely what is forbidden.

## Semantics

Binding activation, the fixed evaluation timestamp, the refusal to select a winner, and the enforcement and planning consequences of a conflict are governed by ADR-0005 and are not restated here. This ADR adds only the following.

When more than one active authoritative binding matches a (policy identifier, repository) pair:

- **Per-binding evaluation continues**, as ADR-0005 already requires for analytical and rollout visibility. Each matching binding is evaluated independently under its own policy version and requirement set, and its results are recorded as explanatory evidence for that binding.
- **No per-binding result is an official governance outcome.** The ADR-0005 authority bound is unsatisfied, so no official interpretation exists for the pair, and no binding's results become the pair's requirement outcomes.
- **No synthesized requirement set.** The engine never unions, intersects, or otherwise composes requirement sets across conflicting policy versions, and produces no official requirement outcomes for the pair.
- **One official pair-level result**: Policy Outcome `Unknown` and Coverage State `Unknown`. Declared intent exists but is contradictory, so both dimensions genuinely cannot be determined.
- **Coverage precedence-0.** Authority ambiguity means no authoritative intended-control set is determinable, so Coverage State is `Unknown` *before* ADR-0007's requirement-level aggregation runs. This case precedes rules 1–3 and belongs to the same engine-owned coverage rule, preserving ADR-0007's exclusivity — no other mechanism computes coverage. Without it, aggregation over an undeterminable requirement set falls through to rule 3 and reports `Covered`, presenting a configuration error as full coverage.
- **The conflict record extends ADR-0005's.** Beyond the conflicting bindings ADR-0005 already requires evidence to identify, the record carries each binding's policy version, requirement set, and explanatory results; any requirement-set divergence across those versions; and the fact that no binding determined the official requirement outcomes.

**Ambiguous intent and absent intent stay distinct.** Zero authoritative bindings is unchanged: no declared intent means no intended control set, so the pair receives neither a Policy Outcome nor a Coverage State (ADR-0005). Ambiguous intent yields `Unknown` in both dimensions; absent intent yields neither. The two are never conflated, and coverage is the dimension that distinguishes them.

## Why this needs no new closed set

Authority ambiguity is a pair-level failure of the existing authoritative-binding invariant. It is not a new property, status, or eligibility of an individual binding, and it introduces no enumeration.

A conflicting binding's declared Evaluation Role remains truthfully `authoritative` — that is what desired state declares, and the engine does not rewrite declarations. What suppresses official results is not a fact about any binding but a fact about the pair: the ADR-0005 authority bound is unsatisfied, so there is no official interpretation for results to attach to. Evidence expresses this through existing binding authority and evidence relationships — explanatory records exist for each conflicting binding, the pair's official result is `Unknown` in both dimensions, and the governance-configuration finding names the cause — in the same way ADR-0005 already separates shadow results from the authoritative result in reports and evidence. An eligibility enumeration would encode as engine state what the declarations and the invariant already determine.

## Consequences

- ADR-0007's coverage aggregation acquires a precedence-0 case; rules 1–3 are unchanged but are no longer exhaustive on their own.
- Domain Model invariant 4 stops at the compliance dimension and at `Unknown`. It must state the coverage dimension, the relationship between the explanatory evidence recorded for each conflicting binding and the pair's official outcome, and the prohibition on synthesized requirement sets.
- **The next Architecture Baseline must carry forward navigation to this ADR from ADR-0005 and ADR-0007**, recording that ADR-0013 refines their interaction. Neither accepted ADR is edited in place, so nothing points forward from them: a reader of ADR-0007 alone finds coverage rules 1–3 with no indication they are not exhaustive. The pointer belongs in the baseline's ADR index and recommended-reading section, never in the accepted ADRs themselves.
- Conflicting bindings carrying divergent policy versions become a specified, testable case rather than an undefined one.
- Slice 5 (shadow bindings) inherits a settled account of what is and is not an official governance outcome, instead of inventing one.
- The architecture-version and baseline consequences of the invariant-4 refinement are decided at acceptance of this ADR, not by it.
