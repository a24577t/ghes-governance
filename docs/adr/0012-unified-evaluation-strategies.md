---
status: proposed
---

# One engine, multiple evaluation strategies; Drift retired as a first-class concept

Centrally Managed State is not a separate subsystem. The governance engine supports multiple **evaluation strategies**, and every Requirement declares exactly one. The initial strategies:

- **Predicate Evaluation** — determines compliance by evaluating conditions against observed state.
- **Desired-State Evaluation** — determines compliance by comparing normalized observed state against a version-controlled desired artifact.

Everything else is identical across strategies: bindings, modes, evaluation roles, evidence, coverage, exceptions, exclusions, execution, remediation, and change budgets. The engine uses the same closed Technical Outcomes regardless of strategy. No second governance model exists.

**Drift is retired as a first-class domain concept.** "Drift" is simply the common name for a `NonCompliant` technical outcome produced by a Desired-State Evaluation — it participates in the same outcome sets, findings, relief, and remediation as every other noncompliance.

## Comparison Profile

Desired-State Evaluation requires a versioned **Comparison Profile**, which is trusted desired-state content. The profile determines: compared fields, ignored fields, server-managed fields, normalization rules, ordering rules, default-value handling, and unknown-field behavior. Unknown fields do not automatically become drift; they are processed according to the active profile, and where no rule exists the comparison result is `Unknown` — uncertainty neither grants relief (ADR-0008) nor manufactures findings.

## Strategies are engine capabilities, not plug-ins

A strategy implementation is part of a validated engine release, introduced through normal engine development, testing, review, and release processes. Strategies are never dynamically loaded, supplied by deployment configuration or desired-state content, provided as arbitrary scripts, or replaced at runtime by an external implementation. Desired state selects a supported strategy by identifier and supported version; it never provides the implementation.

**Unknown strategy behavior.** A Requirement selecting an unknown strategy identifier, an unsupported strategy version, or a strategy unavailable in the running engine release produces Technical Outcome `Unknown`, a high-visibility governance-configuration finding, and evidence identifying the requested and available strategy versions. The engine never skips the requirement, silently substitutes another strategy, downgrades to a simpler strategy, or treats the requirement as not applicable.

**Invariant strategy contract.** Every strategy: consumes the defined Replay Input Set; produces Normalized Observed State; emits only the engine-owned closed Technical Outcome set; produces an explainable evaluation result; is deterministic for the same inputs and strategy version; and records its identifier and version in Evidence. A strategy never: extends or redefines Technical Outcomes; determines governance interpretation; applies Governance Relief; alters policy aggregation; changes applicability semantics; performs remediation; writes to GHES or another governed system; or makes external approval decisions. Strategies compute technical facts; the core engine owns governance meaning.

**Registry.** The engine maintains an internal strategy registry or equivalent dispatch mechanism. For the POC this is an internal seam only — `PredicateEvaluation` and `DesiredStateEvaluation` — with no dynamic discovery, package loading, or third-party strategy API.

**Evidence and determinism.** Every requirement evaluation records: strategy identifier, strategy version, engine version, normalized inputs or their evidence references, normalized observed state, technical outcome, explanation, and the content hashes required for replay — so an auditor can identify the exact comparison logic used. Determinism applies over the complete captured Replay Input Set: any external data required for evaluation is captured or normalized before strategy execution, so a later replay never depends on re-querying a mutable external system.

## First centrally managed requirement

The governance repository's protection configuration (ADR-0002) remains the first centrally managed control — now modeled exactly like every other Requirement, differing only in its declared evaluation strategy.
