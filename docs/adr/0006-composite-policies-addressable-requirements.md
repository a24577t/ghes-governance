---
status: accepted
---

# Composite policies with individually addressable requirements

A policy is a logical grouping of related governance requirements: a stable policy identifier, a policy version, policy-level purpose and descriptive metadata, and one or more individually addressable requirements. The policy is not the smallest evaluation, finding, or relief unit. Each requirement carries a stable requirement identifier, a human-readable name and description, a declared evaluation strategy, an evaluation definition — interpreted by, and taking the form required by, the selected Evaluation Strategy (ADR-0012) — an evidence definition, optional remediation guidance, and optional compatibility prerequisites.

## Stable requirement identity

Requirement identifiers are **immutable**; descriptive metadata (name, description, remediation guidance) may evolve without changing identity, provided the requirement's meaning is unchanged. An identifier is never reused for a materially different control; when a requirement's meaning changes materially it receives a new identifier rather than a redefinition under the old one. This lets shadow comparison (ADR-0005) report per requirement — unchanged, modified, newly introduced, removed, changed evaluation result — instead of relying on the overall policy outcome.

## Unit of evaluation and finding

Evaluation occurs per (policy binding, repository, requirement). Each requirement produces its own evaluation result and, when appropriate, its own finding, identifying: policy identifier and version, requirement identifier, binding identifier, repository, applicability context, observed evidence, expected condition, technical outcome, governance interpretation and relief-artifact reference when applicable, and active enforcement mode. The engine never produces only a flat policy-level finding.

## Outcomes and aggregation

Requirement results separate technical evaluation from governance interpretation (refined by the consistency review and ADR-0008):

- **Technical Outcome** (closed): `Compliant`, `NonCompliant`, `Unknown`, `NotEvaluated` — never altered by governance artifacts.
- **Governance Interpretation** (closed): `None`, `Exception`, `Exclusion` — always citing the Governance Relief artifact applied.
- **Requirement Outcome** (closed, interpreted): `Compliant`, `NonCompliant`, `Excepted`, `Excluded`, `Unknown`.
  - `Excepted` = technically unmet but reinterpreted by an active Governance Exception (`Technical: NonCompliant / Interpretation: Exception`). Both facts remain visible in evidence; never ordinary compliance.
  - `Excluded` = no technical evaluation occurred (`Technical: NotEvaluated / Interpretation: Exclusion`).

The policy-level outcome is derived **solely** by the deterministic, engine-owned aggregation over interpreted Requirement Outcomes — no other mechanism (policy authoring, providers, strategies, reporting) may compute or override it:

1. any requirement `NonCompliant` → policy `NonCompliant` — an exception on one requirement never conceals another requirement's unresolved noncompliance;
2. otherwise any `Unknown` → policy `Unknown`;
3. otherwise any `Excepted` → policy `CompliantWithExceptions`;
4. otherwise `Compliant`.

`Excluded` and `NotApplicable` requirements are aggregation-neutral but coverage-significant (ADR-0007, ADR-0008). Policy outcomes (closed): `Compliant`, `CompliantWithExceptions`, `NonCompliant`, `Unknown`.

## Requirement applicability

Applicability may vary within an applicable policy (repository characteristics, GHES capability, language or ecosystem, feature availability). Each requirement supports a pre-evaluation applicability result — `Applicable`, `NotApplicable`, `Unknown`. `NotApplicable` does not negatively affect aggregation; applicability `Unknown` normally yields a requirement outcome of `Unknown`.

## Governance-relief target

Relief artifacts normally target (policy identifier, requirement identifier, scope or repository target). Relief for one requirement never covers other requirements in the same policy. Whole-policy relief is supported only as an explicit, highly visible form that enumerates or clearly declares that all requirements are included — never the default interpretation of a missing requirement identifier. **Relief changes governance interpretation, never the technical outcome** — a recurring platform principle (ADR-0008): Technical Outcomes are never altered by governance artifacts.

## Future control catalog

A separate reusable control catalog is deferred. If introduced later, it is an authoring and reuse mechanism that compiles or resolves into this same engine-facing model (versioned policy → individually addressable requirements). The engine does not require a catalog for the POC.

## First vertical slice

One composite policy; at least two stable requirement identifiers; one compliant requirement and one noncompliant-or-unknown requirement; independent findings per requirement; deterministic policy-level aggregation; evidence showing both requirement and policy outcomes. Governance-relief processing may be modeled in the schema without being fully implemented.
