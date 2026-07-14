---
status: proposed
---

# Controlled remediation: Enforce grants eligibility; plans are approved by content hash

An `Enforce` binding establishes **remediation eligibility** only — it never, by itself, authorizes generated plans to execute. The path is always: policy permits remediation → plan is generated → plan is approved → plan is applied. By default, every Remediation Plan is approved as an immutable governed artifact whose approval binds to the exact plan content hash. A change to the target repository/organization, policy or requirement version, observed state, proposed operations or their ordering, rollback instructions, plan expiration, or plan-affecting engine interpretation invalidates the approval: approval of one plan is never approval of a materially different plan.

## Plan identity

Every plan includes: immutable plan identifier; schema version; content hash; policy, requirement, binding, and repository identifiers; source execution identifier; observed-state snapshot or digest; proposed operations in deterministic order; preconditions; expected postconditions; reversibility classification; impact assessment; verification procedure; rollback or compensating-action procedure; creation time; and mandatory expiration. Plans are append-only — a modified plan is a new plan with a new identifier and hash. An expired plan cannot be applied even if previously approved; renewal requires a new immutable plan and approval. Expiration duration is configurable governance policy; the engine owns only the invariant that an expiration exists and is enforced.

## Plan validity and optimistic concurrency

A plan is valid only against the state from which it was generated. Immediately before every write the engine re-reads the relevant target state and validates preconditions. On mismatch: do not apply; do not adapt the approved plan dynamically; mark the plan stale; emit a plan-invalidated finding; require a new evaluation and plan. This protects legitimate changes made after planning. Native concurrency mechanisms (object identifiers, revisions, ETags, content hashes) are used where the applicable API supports them.

## Reversibility and prior-state capture

Every operation declares a closed reversibility class: `Reversible` (prior state deterministically restorable), `PartiallyReversible` (compensating action exists, exact restoration not guaranteed), `Irreversible` (prior state not reliably restorable), `Unknown` (treated conservatively; never eligible for standing authority). Irreversible and partially reversible operations are prominently identified in the plan, the approval evidence, and the execution report. Immediately before a write, the engine captures the minimum prior state required to prove what changed, verify the approved precondition, support rollback or compensation, and explain the result — authoritative evidence tied to the exact operation, retaining no unnecessary sensitive or unrelated data.

## Standing remediation authority (future)

Future deployments may define narrowly scoped, pre-approved remediation classes executing without per-plan approval — explicit desired-state configuration identifying: permitted operation class, applicable policy and requirement, permitted target scope, maximum change count, risk classification, verification requirements, rollback requirements, effective period, and approving provenance (e.g. low-risk idempotent operations such as restoring a known Boolean repository setting). Standing authority is never inferred merely because a binding is in `Enforce`; irreversible or high-impact operations never qualify.

## Rollback

Rollback is not an ungoverned bypass. It is a new Remediation Plan — or a predefined rollback plan explicitly linked to the original execution — with its own identifier and content hash, current-state preconditions, operations, approval or valid standing authority, verification, and evidence. A prior-state snapshot does not guarantee it remains safe to restore later; rollback preconditions are checked against current state exactly like forward changes.

## No automatic rollback initially

Verification failure must not automatically trigger a broad rollback cascade: later operations may depend on earlier ones, external actors may have changed state, the rollback itself may fail, and rollback may increase blast radius. Future deployments may permit automatic rollback only for an explicitly approved remediation class that is narrowly scoped, fully reversible, idempotent, independently verifiable, safe to retry, and protected by a small change budget.

## Failure handling

On apply or verification failure: stop dependent operations; record the exact operation state; emit an `EnforcementFailure` finding identifying whether the target is unchanged, changed and verified, changed but unverified, or partially changed; never mark the requirement compliant; never hide the previous compliance result; require operator review or a governed recovery plan. Independent operations may continue only when the plan explicitly declares them independent and the execution remains within its approved failure policy. The initial implementation defaults to fail-stop.

## Change budget

Every enforcement execution carries an explicit change budget — a hard safety boundary, never advisory. It may limit repositories modified, organizations affected, total write operations, concurrent writes, irreversible operations, elapsed execution time, and failed operations. The effective budget is the most restrictive applicable limit among engine safety configuration, environment configuration, policy binding, Remediation Plan, and standing remediation authority. On exhaustion: no additional writes; the execution completes with a budget-exhausted status; remaining operations are reported as not attempted; evidence records the applicable limits and actual consumption.

## Per-operation execution order

Confirm trusted policy and binding → confirm Enforce eligibility → load approved plan or standing authority → validate plan hash and expiry → check change budget → re-read current state → validate preconditions → capture prior state → apply one operation → verify postcondition → record evidence. No dependent operation runs unless the required predecessor verification succeeded.

## Uncertainty never grants write authority

The engine must not apply a change while any required condition is `Unknown`: current target state, plan integrity, authorization, compatibility, reversibility, prerequisite result, or verification ability. This extends ADR-0008's principle — uncertainty never grants privilege — to the write path.

## POC boundary

The POC performs no GitHub writes. It models and tests: Enforce as eligibility rather than implicit approval; immutable Remediation Plans; plan hashes; preconditions and postconditions; mandatory expiration; reversibility classes; prior-state evidence; change budgets; stale-plan invalidation; and enforcement-failure outcomes. Actual apply, verification, rollback, and standing automatic authority are deferred.
