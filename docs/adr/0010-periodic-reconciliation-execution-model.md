---
status: accepted
---

# Periodic reconciliation is authoritative; executions declare scope, completeness, and freshness

Periodic reconciliation is the authoritative evaluation mechanism. Reactive (event-driven) execution is an optimization that may reduce detection latency but never replaces periodic reconciliation: the platform's audit guarantee rests on successful periodic evaluation, not on successful event delivery.

**Result authority and the audit guarantee are different things.** A reactive execution with a narrow declared scope may produce authoritative results for the tuples it covers — result authority comes from bindings and the declared scope, never from how the execution was triggered. What reactive execution can never provide is the completeness guarantee: only periodic reconciliation bounds the staleness of every governed tuple, because events can be missed, duplicated, or delayed. Authority is per-tuple; the audit guarantee is per-estate.

## Declared evaluation scope

Every execution explicitly declares its evaluation scope — Enterprise, Organization, Repository, Policy, or Rollout Ring. The scope is part of execution identity and is recorded in evidence. Executions are not required to evaluate the entire enterprise.

**Supersession is tuple-level.** A new execution's authoritative result for a (repository, policy, requirement) tuple replaces the prior authoritative result for that same tuple as the *current* compliance answer — if and only if the tuple lies within the execution's declared scope. Tuples outside the declared scope are untouched. Superseded results are never deleted: evidence is append-only; a superseded result simply stops being current.

**Overlap is defined at the tuple level** (authoritative definition in the glossary): two evaluation scopes overlap when they could select at least one common (repository, policy, requirement) tuple at the same evaluation time.

## Completeness

Execution completeness is an execution-level property recorded in evidence, with a closed status set: `Complete`, `CompleteWithGaps`, `Failed`, plus completeness accounting (discovered, evaluated, Unknown counts with reasons). Unknown results caused by unavailable targets remain visible; one unavailable repository must not suppress evidence for every other repository.

## Freshness

Result freshness is part of governance. Every reported compliance result includes its evaluation timestamp, execution identifier, and result age; reports identify stale evaluations using configurable thresholds. An old compliant result is not equivalent to a recent compliant result.

## Concurrency and API load

One active execution per overlapping evaluation scope; a second is queued or rejected, never interleaved. The governance engine must behave as a well-behaved client of GHES: request budgets, throttling, and concurrency limits belong to the operational contract — **a governance tool must not degrade the platform it protects** (Architecture Principle 12).

## POC boundary

Manual execution; synthetic evaluation; a single execution lock; a complete execution manifest; a configurable request budget (even if simulated). Future implementations may introduce scheduled reconciliation, repository-triggered evaluation, and concurrent non-overlapping executions.
