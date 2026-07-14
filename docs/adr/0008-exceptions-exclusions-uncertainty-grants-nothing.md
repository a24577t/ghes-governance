---
status: accepted
---

# Governance Relief: exceptions and exclusions; uncertainty never grants privilege

The Question-1 concept "accepted deviation" was overloaded — it bundled artifacts operating at different pipeline stages, and its name collided with the requirement outcome it produced. The family is renamed **Governance Relief**, with two distinct governed artifact types:

- **Governance Exception** — applies *after* technical evaluation. The requirement is evaluated and the technical result remains visible; governance changes only the interpretation (`Technical: NonCompliant / Interpretation: Exception / Requirement Outcome: Excepted`, ADR-0006).
- **Governance Exclusion** — applies *before* technical evaluation. The requirement would otherwise apply, but governance intentionally defers or excludes evaluation (`Technical: NotEvaluated / Interpretation: Exclusion / Requirement Outcome: Excluded`). This is not `NotApplicable`: NotApplicable remains reserved for logical inapplicability (repository characteristics, platform capability). Coverage reporting distinguishes `GovernanceExclusion` from `CapabilityGap` — "we chose not to yet" is never conflated with "the platform can't."

Excluded requirements are compliance-neutral in aggregation and coverage-significant: they are uncovered with Coverage Reason `GovernanceExclusion`, so a policy may report `Compliance: Compliant / Coverage: PartiallyCovered (GovernanceExclusion)` — never presented as equivalent to full compliance with full coverage (ADR-0007).

## Lifecycle

Every relief artifact carries an explicit lifecycle: `Draft → Approved → Active → Expiring → Expired`, with `Superseded` when replaced by a newer version. Draft and Approved are **governance-process states, not runtime engine states** — the engine never sees a Draft (pre-merge) and treats Approved as content awaiting effectiveness; it derives Active, Expiring, Expired, and Superseded at the fixed evaluation timestamp (ADR-0005).

- **Expiry is mandatory.** The engine rejects an open-ended relief artifact as invalid desired state. How long relief may run is a governance-process concern; that it must end is engine-enforced schema.
- **Expiry is loud.** A relief artifact active in the previous execution and expired in the current one produces a distinct governance finding — accepted risk that lapsed back into unaccepted risk is a reportable event, never a silent recolor. The Expiring state enables proactive governance before lapse.
- **Renewal creates a new immutable version** through the governed Git process (ADR-0002); relief artifacts are never amended in place.

Open detail: whether the Expiring warning threshold is declared per artifact or as a governance-wide default.

## Shadow evaluations apply the same relief

Shadow evaluations apply the same active Governance Relief artifacts as authoritative evaluations, subject to each artifact's declared policy, requirement, binding, version, scope, and effective-period targeting. Shadow evidence records the raw technical result, the governance interpretation, the interpreted result, the relief-artifact reference, and the binding's authoritative or shadow role — so shadow comparisons measure policy-version differences rather than inconsistent governance interpretation.

## Governance scope is not a risk-acceptance mechanism

Reducing an authoritative binding's scope expression is never a sanctioned way to accept risk and is never treated as equivalent to a Governance Exclusion — it carries no expiry and no coverage signal. Scope-reducing changes to authoritative bindings are governance-significant. The future control that watches for them is itself a **Requirement** — evaluating changes to authoritative binding scopes and producing scope-diff findings identifying repositories removed from governance — not a separate subsystem (consistent with ADR-0012's one-engine rule). Historical evidence and prior governance status remain intact when a repository leaves scope. (Requirement recorded now; not implemented in the first slice.)

## Uncertainty never grants privilege

Generalized architectural principle, applied consistently platform-wide:

- A Governance Exception requires a known technical result — an `Unknown` outcome cannot be excepted; the remedy for Unknown is determining the state, not waiving it.
- A Governance Exclusion requires deterministic applicability.
- A relief artifact whose own scope resolution is `Unknown` is not applied, and the failure is loudly evidenced on the artifact itself.
- **Unknown results may never be overridden by governance artifacts.** This is one of the platform's core invariants (Domain Model §5) — it holds for relief, bindings, plans, approvals, and every future governed artifact type.

This extends the fail-loud contracts already adopted for attribute providers (`CannotDetermine` never becomes `Value Absent`, ADR-0003) and capability knowledge (undetermined never becomes unsupported or compliant, ADR-0007) to governance relief itself.
