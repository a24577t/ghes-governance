---
status: proposed
---

# Policy bindings carry enforcement mode; closed three-mode model

Enforcement mode is a closed semantic model owned by the core engine, and it attaches to a versioned **policy binding** — not to the policy globally:

```text
Policy Version + Scope Expression + Enforcement Mode + Effective Period = Policy Binding
```

A binding identifies at least: policy identifier and immutable version, scope expression, enforcement mode, effective start time, optional effective end time, optional rollout ring or rollout identifier, binding version, and provenance of the approved change. The same policy version may therefore operate simultaneously in different modes across different scopes (e.g. `Enforce` in a synthetic canary scope, `Plan` in a pilot scope, `Observe` across the wider inventory). Policies are never cloned to represent rollout stages.

## The closed mode set

- **Observe** — resolve applicability, evaluate compliance, produce findings and evidence. No target changes; no executable remediation plan.
- **Plan** — all Observe behavior, plus an explainable remediation plan identifying proposed operations, prerequisites, expected impact, risk, verification steps, and rollback requirements. No target changes.
- **Enforce** — evaluation and planning, plus permitting an approved execution process to apply the remediation, verifying the resulting state, and recording execution, verification, failure, and rollback evidence.

Notification is **not** an enforcement mode. Notifications are configurable reporting/workflow outputs that may be produced from any mode (reports, PR comments, GitHub issues, email, messaging platforms, change-management systems), keeping enforcement semantics stable while notification mechanisms vary by deployment.

## Transitions

Mode transitions are trusted desired-state changes following the same governed Git process as policies, governance relief artifacts, and provider configuration (ADR-0002). Transitions work in both directions (`Observe → Plan → Enforce` and back). Promotion is never automatic — elapsed time or successful evaluations alone are insufficient; it requires an approved binding change. Demotion is a first-class operational control and the emergency brake: a policy can be demoted without changing or deleting the underlying policy definition.

## Timing and evidence

Bindings may carry effective dates, but future-dated activation must not silently depend on a Git merge alone. Every evaluation records the binding version, the effective period, the mode active at evaluation time, and the engine time used for that determination — so evidence can distinguish an observed finding, a planned remediation, an enforced change, an excepted or excluded requirement, and an enforcement failure.

## Governance relief applies in every mode

In `Observe` relief artifacts distinguish accepted risk from unresolved findings; in `Plan` they prevent or alter remediation planning; in `Enforce` they prevent an otherwise applicable remediation from executing. A relief artifact is part of compliance interpretation and audit evidence, not merely an enforcement bypass (ADR-0008).

## POC boundary

The first vertical slice implements `Observe` and `Plan` only — a versioned policy, a scope, a policy binding, Observe evaluation, Plan output, and evidence containing the active mode. `Enforce` is represented in the model but performs no write operations.

## Open questions (updated during consolidation)

- Overlapping-binding precedence — **resolved by ADR-0005**: explicit authoritative/shadow evaluation roles, no inferred precedence, ambiguity fails loud.
- Clock uncertainty — largely resolved by ADR-0005's fixed per-execution evaluation timestamp and half-open effective periods; distributed clock-skew handling remains deferred until execution is distributed (executions stay serialized per ADR-0010).
