---
status: proposed
---

# Policy-first hybrid governance model, not a full desired-state inventory

In a brownfield GHES enterprise, Git cannot practically enumerate the intended configuration of every repository: onboarding cost is excessive, legitimate local differences would be classified as drift, and settings that application teams should own would be centralized. We decided on a deliberate hybrid: **policy evaluation is the default** (Git is authoritative for governance rules, policy scopes, minimum control requirements, accepted deviations/waivers, rollout state, and policy versions/effective dates), and **inventory-style exact desired state is used only for explicitly designated centrally managed controls** (e.g. an org ruleset, a code-security configuration, an Actions allowlist, a centrally maintained reusable workflow, or a designated repository file). GHES remains authoritative for any setting not governed by an active policy.

## Consequences

- The engine must distinguish five states: observed (visibility only), policy-evaluated, centrally managed, accepted deviation, and unknown (cannot evaluate due to access, unsupported GHES capability, or missing environmental information).
- A difference is Noncompliance only when it violates an applicable policy; unmanaged settings are inventoried but never classified as drift.
- Deterministic comparison/reconciliation applies only to centrally managed controls; the design must preserve the ability to add such controls later without redesign.
- The first vertical slice demonstrates policy evaluation (load one policy, load one synthetic repository state, determine applicability, evaluate compliance, produce an explainable result, recommend without applying) — not full repository reconciliation.

## Refinements by later ADRs

This seed model has been refined during discovery: "unknown" became the cross-cutting could-not-determine member of every closed result set rather than a fifth state (ADR-0003, ADR-0006, ADR-0007); "accepted deviation" was renamed to the Governance Relief family with two artifact types, Governance Exception and Governance Exclusion (ADR-0008); "rollout state" is expressed as Policy Bindings with modes and evaluation roles (ADR-0004, ADR-0005); and the first vertical slice is defined cumulatively by ADR-0003 through ADR-0010, superseding the minimal slice sketch above.
