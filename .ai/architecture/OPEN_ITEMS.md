# Open Items

Last updated: 2026-07-14

## Architectural

- **OI-1 — Coverage aggregation rule (finding F2).** Requirement-level coverage contributions exist (`CapabilityGap`, `GovernanceExclusion`), but no rule defines when a policy is `Covered` vs `PartiallyCovered`. Decide whether coverage aggregation is an engine-owned closed rule (parallel to ADR-0006's compliance aggregation) and define it. Impacts ADR-0007.

## ADR amendments pending (dispositioned in principle, not yet folded)

- **OI-2 (F1).** Shadow binding in Enforce mode: resolved by Architecture Principle 9 ("Evaluation Role constrains execution authority") — effective behavior is capped at simulation regardless of declared mode. One-paragraph amendment to ADR-0005 pending.
- **OI-3 (F3).** State explicitly that a Requirement's evaluation-definition *form* is determined by its declared Evaluation Strategy (predicate conditions vs. desired artifact + Comparison Profile). One sentence in ADR-0012 pending.
- **OI-4 (F4).** Record the inference asymmetry — "restrictions may be inferred; authority may not" — in ADR-0011. Captured as Architecture Principle 10 and Domain Model invariant §5.3.

## Specification-level

- Consolidated First Vertical Slice definition (currently cumulative across ADR-0003–0011)
- Scope-expression language syntax
- Schemas: policy/requirement, policy binding, governance relief artifact, remediation plan, comparison profile, evidence items and execution manifest
- Expiring warning threshold: per-artifact vs. governance-wide default (ADR-0008 open detail)
- Retention configuration schema; notification action configuration
- Detailed coverage-reason taxonomy beneath aggregate outcomes
- Reporting personas and primary report formats

## Implementation-level

- Single-execution lock mechanism; content-hash algorithm; evidence directory layout; per-API concurrency mechanics (ETags/revisions); strategy registry seam; simulated request budget

## Environmental validation

- Actual GHES version and capabilities; API authentication model and granted permissions; rate limits; organization structure; topics/custom-property hygiene; existing runner and security tooling

## Deferred by design (recorded in ADRs; informational, not backlog)

- Standing remediation authority; automatic rollback (ADR-0011)
- Event-driven acceleration; concurrent non-overlapping executions (ADR-0010)
- Runtime capability probing as corroboration (ADR-0007)
- Control catalog authoring layer (ADR-0006)
- Scope-diff report control (ADR-0008)
- Evidence hardening: signing, WORM, anchoring, separate ownership (ADR-0009)
- Distributed clock-skew handling (ADR-0005, ADR-0010)
- Federation of policy authorship (discovery Q2)
