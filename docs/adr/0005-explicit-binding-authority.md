---
status: accepted
---

# Explicit binding authority: authoritative vs shadow, no inferred precedence

When multiple active policy bindings match the same (policy identifier, repository) pair, the engine evaluates every match independently for analytical and rollout visibility — but exactly one explicitly declared **authoritative** binding determines the official compliance outcome, remediation planning, enforcement eligibility, and primary audit reporting. Authority is declared in desired state through a closed evaluation-role model on each binding — `authoritative` or `shadow` — and is never inferred.

## Considered options

A mechanical precedence rule (higher policy version, then more advanced mode, then latest effective start, then binding id) was considered and rejected. Those attributes do not express governance intent: a higher policy version may be an experimental pilot; a more advanced mode should not automatically override a safer mode; a later effective date does not imply broader authority; and a mechanical tiebreaker silently converts a configuration mistake into an enforcement decision.

## Semantics

- **Shadow bindings** are evaluated for comparison, pilot analysis, and evidence. They cannot determine the official compliance outcome, generate an executable remediation plan, or trigger enforcement. A shadow binding in `Plan` mode produces a **simulated plan** — prospective, never executable, and labeled as shadow in evidence.
- Multiple shadow bindings may match one repository; each result is identified by policy version, binding identifier, scope, mode, effective period, and rollout identifier, and remains clearly separated from the authoritative result in reports and evidence.
- **Version rollout**: v1 authoritative enterprise-wide with v2 shadow in a pilot scope lets a repository be officially compliant under v1 while reporting shows it would fail the proposed v2 — explicitly, never flattened into a single result. Promotion is a governed desired-state change that explicitly changes which binding is authoritative.
- **Authority bound (invariant)**: per (policy identifier, repository), **at most one** active authoritative binding is permitted, and an official compliance interpretation is derived from **exactly one** — never from zero, never from more than one. Desired state can violate the bound (two overlapping authoritative bindings can both be merged); the engine preserves the invariant by refusing interpretation, never by picking a winner.
- **Zero authoritative bindings** is a normal rollout state, not an error: no official compliance interpretation exists for that pair. The engine emits neither `Unknown` (no declared intent exists to fail to determine) nor `NotApplicable` (a logical claim that itself requires an authoritative binding to make). The absence remains fully visible through inventory and binding provenance and may surface in reporting as its own derived category.
- **More than one** is a configuration error: the engine must not select one via hidden precedence; no planning or enforcement occurs; the authoritative outcome is `Unknown` (declared intent exists but is contradictory, so it genuinely cannot be determined); a high-visibility governance-configuration finding is emitted; and evidence identifies every conflicting binding — even if only one of them is in `Enforce` mode. Ambiguity about authority never resolves silently.
- **Mode never determines authority**: Enforcement Mode influences behavior only after an authoritative binding has been selected. It never contributes to determining authority.
- **Role caps mode** (Principle 9 — *Evaluation Role constrains execution authority*): a Shadow binding's effective behavior is capped at simulation regardless of its declared mode. A Shadow binding in `Enforce` mode behaves as simulation only and can never execute.

## Fixed execution timestamp

At execution start the engine fixes one authoritative evaluation timestamp, used consistently for binding activation, scope evaluation, governance-relief validity, policy applicability, compliance interpretation, and planning eligibility — an execution spanning a time boundary never changes its active binding set midway — and records it in evidence. Effective periods are half-open intervals (`effective_start <= evaluation_timestamp < effective_end`), so one binding can end at the exact instant another begins without boundary overlap. For the POC: the engine process clock provides the timestamp, distributed clock-skew handling is deferred, scheduled activation is not required, and a future-dated binding becomes active during the first execution whose fixed timestamp falls within its effective period.

## First vertical slice

Supports multiple matching bindings, one authoritative binding, zero or more shadow bindings, independent evaluation of all matches, one official compliance outcome, conflict detection for multiple authoritative matches, a fixed execution timestamp, and evidence distinguishing authoritative from shadow results. No enforcement is performed.
