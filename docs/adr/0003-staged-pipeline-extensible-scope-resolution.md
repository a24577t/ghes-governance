---
status: accepted
---

# Staged governance pipeline with extensible scope resolution

Discovery, scope resolution, and policy evaluation are intentionally separate stages with strict gating: every discovered repository enters the inventory unconditionally (observation is universal), evaluation begins only after successful scope resolution, and enforcement depends on successful evaluation. Version 1 scope expressions may reference only deterministic repository attributes available directly from GitHub (organization, repository name, visibility, archived state, fork status). Richer sources — topics, custom properties, GitHub teams, CMDB, ServiceNow, other approved enterprise systems — arrive later as additional attribute providers, rather than as a governance-owned classification model embedded in the engine.

## Extensible provider seam

Scope **semantics** are fixed in the core engine; scope **attribute sources** are extensible behind a constrained provider seam — an engine-owned interface, not a runtime plug-in mechanism.

- The core engine owns the scope-expression language, predicate composition, applicability evaluation, precedence and conflict behavior, explanation of scope results, and the closed applicability outcomes: `Applicable`, `NotApplicable`, `Unknown`. A provider cannot redefine policy meaning or introduce new outcomes. Providers never evaluate policy — they only supply normalized facts; all evaluation and interpretation happen in the core engine.
- An attribute provider must distinguish three results: **value present**, **value absent** (source queried successfully, attribute not set), and **cannot determine** (error, unavailable system, insufficient permission, unsupported capability, ambiguous data). `Cannot determine` is never silently converted into `value absent`; when an attribute required by a scope expression cannot be determined, applicability is `Unknown`.
- Providers are inside the trusted computing base: active providers and their configurations are explicitly declared, versioned, and enter the trusted configuration through the same governed Git process as policies and governance relief artifacts (ADR-0002). Only approved implementations run; arbitrary unaudited runtime code cannot be loaded. The ownership split is explicit: **provider configuration** — which providers are active and how they are configured — is governed desired-state content; **provider implementation** is an engine capability, shipped and versioned with a validated engine release (the same split ADR-0012 applies to evaluation strategies).

## Evidence requirements

Every evaluation records enough to reproduce and explain scope resolution: policy version, scope expression, repository identifier, provider name, provider implementation version (the released implementation shipped with the engine — distinct from configuration), provider configuration version/hash, requested attribute, returned result category, returned value when present, timestamp, and the error or uncertainty reason when the result is `cannot determine`. For external sources whose values change over time, evidence captures the value used at evaluation time rather than relying on later re-query.

## Consequences

- Discovery never depends on policy applicability, so inventory completeness is independent of policy correctness.
- A repository whose applicability or evaluation cannot be determined yields an Unknown result — never assumed compliant or noncompliant. Unknown results surface in reporting as actionable governance work items.
- The first vertical slice implements one GitHub-native attribute provider, the three-result provider contract, one core scope expression, the fixed applicability outcomes, and explainable evidence showing how applicability was determined — with no plug-in loading framework, enterprise metadata, CMDB integration, or organization-specific classification model.
