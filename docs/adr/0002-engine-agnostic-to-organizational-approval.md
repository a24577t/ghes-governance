---
status: accepted
---

# Governance process is separated from governance execution

**Governance process is intentionally separated from governance execution.** That is this ADR's central decision; everything else follows from it.

The engine consumes **Approved Artifacts**: immutable, commit-identified versions of governed desired-state content — policies, scope expressions, policy bindings, governance relief artifacts, attribute-provider configuration, comparison profiles, plan approvals — that have completed the governance repository's governance process. The engine never validates organizational authority; who may merge governed artifacts is delegated to the governance repository's protection model (branch protection, CODEOWNERS, future enterprise integrations), so the approval process can evolve without engine changes and the engine stays portable across organizations.

The merged-Pull-Request-into-a-protected-branch workflow is the **current implementation** of the governance process, not a permanent architectural requirement.

## Consequences

- The engine records provenance but does not judge it. The architectural requirement is **sufficient provenance for audit and replay**: evidence must identify the approved artifact version consumed, its introduction and approval provenance, the evaluated target, the execution identity, and the engine and GHES context. The detailed field enumeration (pull request, commit, approving users recorded as evidence only, timestamps, versions) is specification-level content.
- Governance Relief artifacts (exceptions and exclusions, ADR-0008) follow the identical trust model. The engine evaluates only: does an approved relief artifact exist, is it within scope, is it still valid, has it expired, and which policy and requirement it references (requirement-level targeting per ADR-0006) — never whether the correct individuals approved it.
- The governance repository becomes part of the trusted computing base. It must be the platform's first Centrally Managed State: its protection settings are verified during every periodic reconciliation whose evaluation scope covers it (ADR-0010), and any divergence produces evidence.
