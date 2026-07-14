---
status: accepted
---

# Controlled remediation: Enforce grants eligibility; plans are approved by content hash

An `Enforce` binding establishes **remediation eligibility** only — it never, by itself, authorizes generated plans to execute. The path is always: policy permits remediation → plan is generated → plan is approved → plan is applied. By default, every Remediation Plan is approved as an immutable governed artifact whose approval binds to the exact plan content hash. A change to the target repository/organization, policy or requirement version, observed state, proposed operations or their ordering, rollback instructions, plan expiration, or plan-affecting engine interpretation invalidates the approval: approval of one plan is never approval of a materially different plan.

## Approval artifact and revocation

A **Plan Approval** is a first-class, authorization-constraining artifact (a desired-state entity in the Domain Model and glossary): it grants permission to execute exactly one plan — identified by plan identifier and content hash — and may simultaneously narrow, never widen, how that plan may execute. It records approving provenance, approval time, applicable constraints, and validity. Approval does not modify the plan. Plan Approval may only narrow the approved plan's executable scope and limits. It cannot authorize operations, targets, risk classes, or limits not already permitted by the plan and upstream governance. Numeric limits use the most restrictive applicable value. Approval may be revoked through an **append-only revocation record**. Granting and removing write authority deliberately use **asymmetric channels** — an explicit decision, not an inheritance from ADR-0002:

- **Governed approval authority** — *establishing* permission requires the normal trusted desired-state process (ADR-0002). There is no fast path to granting write authority.
- **Emergency suspension authority** — *removing or pausing* permission may use an explicitly defined emergency suspension path, because revocation is restrictive, not privilege-granting (Principle 10: restrictions may be applied conservatively; authority may not). Approval is deliberate and planned; revocation may be urgent, and an approved plan must not remain usable while an emergency change waits for review and merge. The emergency path must still be authenticated, append-only, and evidenced, and must later be reconciled into the governance repository. It can only reduce authority — it can never grant authority or alter the plan.

**POC boundary and deferral:** for the POC, both approval and revocation use the governed Git process. The concrete definition of the emergency suspension path is **explicitly deferred as a future architectural decision** — recorded here so it is neither silently inherited away nor accidentally implemented ad hoc.

**Authorization validity — including approval status, revocation, expiry, standing authority, and emergency suspension — is revalidated immediately before every write operation.** Revocation does not undo an operation already completed: remaining operations are not attempted, and the execution records a partially completed or authorization-revoked outcome. No transactional rollback is implied (consistent with non-atomic execution).

## Plan identity

Every plan includes: immutable plan identifier; schema version; content hash; policy, requirement, binding, and repository identifiers; source execution identifier; observed-state snapshot or digest; proposed operations in deterministic order; preconditions; expected postconditions; reversibility classification; impact assessment; verification procedure; rollback or compensating-action procedure; creation time; and mandatory expiration. Plans are append-only — a modified plan is a new plan with a new identifier and hash. An expired plan cannot be applied even if previously approved; renewal requires a new immutable plan and approval. Expiration duration is configurable governance policy; the engine owns only the invariant that an expiration exists and is enforced.

**Canonical hash scope.** The plan content hash covers a canonical representation of all fields and referenced artifact digests that can affect authorization, execution, verification, safety, or rollback — nothing authorization-relevant may sit outside the hash.

**Semantics version.** Each plan records the version of the engine-owned remediation interpretation under which it was generated. A change to that interpretation invalidates approval unless compatibility is explicitly established — compatibility is declared, never assumed (consistent with ADR-0012's strategy-version rules).

## Plan validity and optimistic concurrency

A plan is valid only against the state from which it was generated. Immediately before every write the engine re-reads the relevant target state and validates preconditions. On mismatch: do not apply; do not adapt the approved plan dynamically; mark the plan stale; emit a plan-invalidated finding; require a new evaluation and plan. This protects legitimate changes made after planning. Native concurrency mechanisms (object identifiers, revisions, ETags, content hashes) are used where the applicable API supports them.

## Reversibility and prior-state capture

Every operation declares a closed reversibility class: `Reversible` (prior state deterministically restorable), `PartiallyReversible` (compensating action exists, exact restoration not guaranteed), `Irreversible` (prior state not reliably restorable), `Unknown` (treated conservatively; never eligible for standing authority). Irreversible and partially reversible operations are prominently identified in the plan, the approval evidence, and the execution report. Immediately before a write, the engine captures the minimum prior state required to prove what changed, verify the approved precondition, support rollback or compensation, and explain the result — authoritative evidence tied to the exact operation, retaining no unnecessary sensitive or unrelated data.

## Standing remediation authority (future)

**Standing Remediation Authority** is likewise a first-class desired-state entity (Domain Model, glossary, extension points). Future deployments may define narrowly scoped, pre-approved remediation classes executing without per-plan approval — explicit desired-state configuration identifying: permitted operation class, applicable policy and requirement, permitted target scope, maximum change count, risk classification, verification requirements, rollback requirements, effective period, and approving provenance (e.g. low-risk idempotent operations such as restoring a known Boolean repository setting). Standing authority is never inferred merely because a binding is in `Enforce`; irreversible or high-impact operations never qualify.

## Rollback

Rollback is not an ungoverned bypass. It is a new Remediation Plan — or a predefined rollback plan explicitly linked to the original execution — with its own identifier and content hash, current-state preconditions, operations, approval or valid standing authority, verification, and evidence. A prior-state snapshot does not guarantee it remains safe to restore later; rollback preconditions are checked against current state exactly like forward changes.

## No automatic rollback initially

Verification failure must not automatically trigger a broad rollback cascade: later operations may depend on earlier ones, external actors may have changed state, the rollback itself may fail, and rollback may increase blast radius. Future deployments may permit automatic rollback only for an explicitly approved remediation class that is narrowly scoped, fully reversible, idempotent, independently verifiable, safe to retry, and protected by a small change budget.

## Failure handling

A Remediation Plan is not assumed to be transactionally atomic across target APIs: each operation outcome is recorded independently, and the plan outcome is derived from the recorded operation outcomes.

On apply or verification failure: stop dependent operations; record the exact operation state; emit an `EnforcementFailure` finding identifying whether the target is unchanged, changed and verified, changed but unverified, or partially changed; never mark the requirement compliant; never hide the previous compliance result; require operator review or a governed recovery plan. Independent operations may continue only when the plan explicitly declares them independent and the execution remains within its approved failure policy. The initial implementation defaults to fail-stop.

## Change budget

Every enforcement execution carries an explicit change budget — a hard safety boundary, never advisory. It may limit repositories modified, organizations affected, total write operations, concurrent writes, irreversible operations, elapsed execution time, and failed operations. **Constraint composition.** The effective execution constraint set is the **intersection** of all applicable constraints from engine safety configuration, environment configuration, policy binding, Remediation Plan, Plan Approval, and standing remediation authority. For numeric limits, the most restrictive value wins. Constraints may be budgets (maximum operations, repositories, irreversible operations, elapsed time, failures) or eligibility filters (permitted operation types, target scope, execution window, risk or reversibility class). Approval-carried constraints are modeled as **authorization constraints**: their numeric limits feed the change budget; their categorical limits act as eligibility filters. A constraint source can only narrow execution — it can never broaden what any other source permits. This is why mechanical composition is safe here and nowhere else: intersection can only remove permission, never create it. Authority must always be explicit (Architecture Principle 10). On exhaustion: no additional writes; the execution completes with a budget-exhausted status; remaining operations are reported as not attempted; evidence records the applicable limits and actual consumption.

## Per-operation execution order

Confirm trusted policy and binding → confirm Enforce eligibility → load approved plan or standing authority → validate plan hash, expiry, and approval (valid, unrevoked, unsuspended) → check change budget → re-read current state → validate preconditions → capture prior state → apply one operation → verify postcondition → record evidence. No dependent operation runs unless the required predecessor verification succeeded.

## Uncertainty never grants write authority

The engine must not apply a change while any required condition is `Unknown`: current target state, plan integrity, authorization, compatibility, reversibility, prerequisite result, or verification ability. This extends ADR-0008's principle — uncertainty never grants privilege — to the write path.

In full (Principle 10): when authority, approval, applicability, or safety cannot be established, the platform may withhold, suspend, or narrow execution conservatively. It must never infer or expand authority.

## POC boundary

The POC performs no GitHub writes. It models and tests: Enforce as eligibility rather than implicit approval; immutable Remediation Plans; plan hashes; preconditions and postconditions; mandatory expiration; reversibility classes; prior-state evidence; change budgets; stale-plan invalidation; and enforcement-failure outcomes. Actual apply, verification, rollback, and standing automatic authority are deferred.
