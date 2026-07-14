---
status: proposed
---

# Explicit binding authority: authoritative vs shadow, no inferred precedence

When multiple active policy bindings match the same (policy identifier, repository) pair, the engine evaluates every match independently for analytical and rollout visibility — but exactly one explicitly declared **authoritative** binding determines the official compliance outcome, remediation planning, enforcement eligibility, and primary audit reporting. Authority is declared in desired state through a closed evaluation-role model on each binding — `authoritative` or `shadow` — and is never inferred.

## Considered options

A mechanical precedence rule (higher policy version, then more advanced mode, then latest effective start, then binding id) was considered and rejected. Those attributes do not express governance intent: a higher policy version may be an experimental pilot; a more advanced mode should not automatically override a safer mode; a later effective date does not imply broader authority; and a mechanical tiebreaker silently converts a configuration mistake into an enforcement decision.

## Semantics

- **Shadow bindings** are evaluated for comparison, pilot analysis, and evidence. They cannot determine the official compliance outcome, generate an executable remediation plan, or trigger enforcement. A shadow binding in `Plan` mode produces a **simulated plan** — prospective, never executable, and labeled as shadow in evidence.
- Multiple shadow bindings may match one repository; each result is identified by policy version, binding identifier, scope, mode, effective period, and rollout identifier, and remains clearly separated from the authoritative result in reports and evidence.
- **Version rollout**: v1 authoritative enterprise-wide with v2 shadow in a pilot scope lets a repository be officially compliant under v1 while reporting shows it would fail the proposed v2 — explicitly, never flattened into a single result. Promotion is a governed desired-state change that explicitly changes which binding is authoritative.
- **Ambiguity**: per (policy identifier, repository), exactly one active authoritative binding is permitted. Zero means no official compliance interpretation exists for that pair. More than one is a configuration error: the engine must not select one via hidden precedence; no planning or enforcement occurs; the authoritative outcome is `Unknown`; a high-visibility governance-configuration finding is emitted; and evidence identifies every conflicting binding — even if only one of them is in `Enforce` mode. Ambiguity about authority never resolves silently.

## Fixed execution timestamp

At execution start the engine fixes one authoritative evaluation timestamp, used consistently for binding activation, scope evaluation, governance-relief validity, policy applicability, compliance interpretation, and planning eligibility — an execution spanning a time boundary never changes its active binding set midway — and records it in evidence. Effective periods are half-open intervals (`effective_start <= evaluation_timestamp < effective_end`), so one binding can end at the exact instant another begins without boundary overlap. For the POC: the engine process clock provides the timestamp, distributed clock-skew handling is deferred, scheduled activation is not required, and a future-dated binding becomes active during the first execution whose fixed timestamp falls within its effective period.

## First vertical slice

Supports multiple matching bindings, one authoritative binding, zero or more shadow bindings, independent evaluation of all matches, one official compliance outcome, conflict detection for multiple authoritative matches, a fixed execution timestamp, and evidence distinguishing authoritative from shadow results. No enforcement is performed.
