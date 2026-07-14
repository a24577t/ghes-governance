---
status: proposed
---

# Periodic reconciliation is authoritative; executions declare scope, completeness, and freshness

Periodic reconciliation is the authoritative evaluation mechanism. Reactive (event-driven) execution is an optimization that may reduce detection latency but never replaces periodic reconciliation: the platform's audit guarantee rests on successful periodic evaluation, not on successful event delivery.

## Declared evaluation scope

Every execution explicitly declares its evaluation scope — Enterprise, Organization, Repository, Policy, or Rollout Ring. The scope is part of execution identity and is recorded in evidence. Executions are not required to evaluate the entire enterprise; authoritative results supersede prior results per (repository, policy, requirement) only within the declared scope.

## Completeness

Execution completeness is an execution-level property recorded in evidence, with a closed status set: `Complete`, `CompleteWithGaps`, `Failed`, plus completeness accounting (discovered, evaluated, Unknown counts with reasons). Unknown results caused by unavailable targets remain visible; one unavailable repository must not suppress evidence for every other repository.

## Freshness

Result freshness is part of governance. Every reported compliance result includes its evaluation timestamp, execution identifier, and result age; reports identify stale evaluations using configurable thresholds. An old compliant result is not equivalent to a recent compliant result.

## Concurrency and API load

One active execution per overlapping evaluation scope; a second is queued or rejected, never interleaved. The governance engine must behave as a well-behaved client of GHES: request budgets, throttling, and concurrency limits belong to the operational contract — a governance tool must not degrade the platform it protects.

## POC boundary

Manual execution; synthetic evaluation; a single execution lock; a complete execution manifest; a configurable request budget (even if simulated). Future implementations may introduce scheduled reconciliation, repository-triggered evaluation, and concurrent non-overlapping executions.
