---
status: proposed
---

# Engine consumes approved artifacts and is agnostic to organizational approval

Governance process is intentionally separated from governance execution. The engine treats an approved policy version — a commit that has completed the governance repository's governance process (currently: a merged Pull Request into a protected branch) — as an immutable, trusted input. It never validates organizational authority; who may merge policies and governance relief artifacts is delegated to the governance repository's protection model (branch protection, CODEOWNERS, future enterprise integrations), so the approval process can evolve without engine changes and the engine stays portable across organizations.

## Consequences

- The engine records provenance but does not judge it. Evidence from each evaluation must answer: which policy version was evaluated, which repository, which execution performed it, which Pull Request introduced the policy version, which commit contained it, which users approved the PR (recorded as evidence only), execution timestamp, engine version, and GHES version.
- Governance Relief artifacts (exceptions and exclusions, ADR-0008) follow the identical trust model. The engine evaluates only: does an approved relief artifact exist, is it within scope, is it still valid, has it expired, and which policy and requirement it references (requirement-level targeting per ADR-0006) — never whether the correct individuals approved it.
- The governance repository becomes part of the trusted computing base. It must be the platform's first Centrally Managed State: its protection settings are verified during every periodic reconciliation whose evaluation scope covers it (ADR-0010), and any divergence produces evidence.
