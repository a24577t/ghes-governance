# Architecture Discovery Brief

## Project: GHES Governance Platform

### Document status (2026-07-13)

Architecture discovery is substantially complete. The current model is recorded in `CONTEXT.md` (ubiquitous language) and `docs/adr/0001`–`0012` (candidate ADRs, `status: proposed`). Where this brief and those documents disagree, the ADRs are current. Statements in this brief known to be superseded:

* "Desired state is treated as the source of truth" — superseded by the policy-first hybrid model (ADR-0001): Git is authoritative for governance content, not for every repository's settings.
* The Governance Engine responsibility list — refined into the staged pipeline, policy bindings, evaluation strategies, and controlled remediation (ADR-0003 through ADR-0012).
* "Drift detection" — drift is no longer a first-class concept; see Desired-State Evaluation (ADR-0012).
* The First Vertical Slice section — superseded by the cumulative slice requirements in ADR-0003 through ADR-0011.

### Purpose

This document provides architectural context for discovery.

It is **not** a specification.

It is **not** a design document.

It contains current understanding only.

Nothing in this document should be considered an approved architectural decision unless explicitly identified as one.

Your responsibility is to identify missing information and challenge assumptions—not to implement the solution.

---

# Problem Statement

Large enterprises frequently operate GitHub Enterprise Server (GHES) in brownfield environments with existing development processes, security tooling, and CI/CD platforms.

Security and governance are often implemented inconsistently across organizations and repositories.

The objective of this project is to develop a governance platform capable of helping enterprises improve:

* Security posture
* Governance consistency
* Audit readiness

while minimizing disruption to existing development teams.

---

# Business Objectives

Highest Priority

* Improve enterprise security posture
* Standardize governance
* Improve audit readiness

Secondary Objectives

* Detect configuration drift
* Simplify governance operations
* Improve visibility into repository configuration
* Support future enterprise growth

---

# Current Known Environment

Known

* GitHub Enterprise Server (GHES)
* Brownfield deployment
* Existing CI/CD platform is CircleCI
* AWS is the primary cloud provider
* Security organization sponsors the initiative
* Public GitHub repository for the POC
* Synthetic data only

Unknown

* GHES version
* Existing GitHub Actions usage
* Existing enterprise policies
* Existing runner infrastructure
* Existing organization structure
* Existing security tooling
* Existing repository standards

Do not assume unknown information.

---

# Project Philosophy

The platform should:

* Observe before enforcing
* Prefer native GHES capabilities over custom implementations
* Minimize disruption to development teams
* Preserve existing software delivery
* Require rollback capability
* Generate evidence for governance actions
* Support phased rollout
* Support brownfield adoption

---

# Scope

The project focuses on governance of GitHub Enterprise Server.

The platform should eventually be capable of:

* Repository assessment
* Repository governance
* Organization governance
* Enterprise governance
* Drift detection
* Governance reporting
* Controlled remediation
* Evidence collection
* Rollout management

The first implementation will intentionally be much smaller.

---

# Current Architectural Hypothesis

The current thinking is that the platform consists of several logical components.

## Desired State

Governance is represented as version-controlled desired state stored in Git.

Changes are reviewed through Pull Requests.

Desired state is treated as the source of truth.

---

## Governance Engine

The engine is responsible for:

* Reading desired state
* Reading actual GHES state
* Comparing desired and actual state
* Producing an execution plan
* Applying approved changes
* Verifying results
* Producing governance evidence

---

## Test Environment

Initial testing should use only synthetic repositories and synthetic data.

No production connectivity is required.

---

## AWS Foundation

Future infrastructure may include logging, evidence storage, IAM, networking, and security runners.

Infrastructure design is outside the first implementation.

---

# Out of Scope

The following are intentionally excluded from the initial architecture:

* CircleCI migration
* ServiceNow integration
* CMDB synchronization
* Enterprise ownership model
* Production deployment
* Enterprise runner implementation
* Programming language selection
* Framework selection
* Database selection

These may become future capabilities.

---

# First Vertical Slice

The first implementation should demonstrate only the reconciliation model.

It should:

* Read desired state
* Read synthetic actual state
* Compare both
* Produce a dry-run change plan

It should not:

* Connect to GHES
* Modify repositories
* Require GHAS
* Require runners
* Require AWS
* Require CircleCI

---

# Architectural Constraints

The solution should:

* Be modular
* Be extensible
* Support multiple GHES versions
* Be compatible with brownfield environments
* Avoid unnecessary assumptions
* Separate governance from implementation
* Allow future integrations without redesign

---

# Review Instructions

Use Matt Pocock's **grill-me** skill.

Treat this document only as background context.

Do not accept any proposal as fact simply because it appears in this document.

Your objective is to improve the architecture by identifying missing information.

Do not write code.

Do not generate implementation tasks.

Do not create documentation.

Do not redesign the solution.

Instead:

* Challenge assumptions
* Identify architectural gaps
* Identify risks
* Ask one question at a time
* Explain why the question matters
* Explain which future architectural decisions depend on the answer

Continue until sufficient architectural understanding exists to produce a formal specification.

Do not ask implementation questions.

Focus on business architecture, governance, operational model, platform boundaries, compatibility, rollout, and risk.

Challenge the architecture, not just the document. If you believe a stated assumption is weak, explain why and ask questions that would validate or invalidate it. Do not optimize for agreement; optimize for discovering architectural weaknesses before implementation.
