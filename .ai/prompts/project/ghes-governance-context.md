# GHES Governance Project Context

## Purpose

You are joining an existing enterprise architecture project.

This repository contains the design and implementation of a **GitHub Enterprise Server (GHES) Governance Platform**.

The project is being developed using an AI-assisted architecture methodology inspired by Matt Pocock's workflow, emphasizing architecture discovery, iterative refinement, and vertical-slice delivery.

Your first responsibility is to understand the architecture before proposing changes.

---

# Project Mission

The objective is to build a governance platform that enables a large enterprise to centrally govern GitHub Enterprise Server while minimizing disruption to existing development teams.

The platform is intended to improve:

* Security posture
* Governance consistency
* Audit readiness
* Operational visibility
* Policy compliance

The project is **not** intended to replace existing CI/CD platforms such as CircleCI.

Instead, it complements existing delivery pipelines by providing centralized governance and security capabilities.

---

# Current Phase

Current project phase:

**Phase 2 – Vertical Slice Specification**

Architecture Discovery Phase 1 has been completed.

The architecture baseline has been established.

Future work should build upon the approved architecture rather than redesign it.

---

# Repository Authority

Before making recommendations, review the architecture in the following order:

1. `.ai/architecture/STATUS.md`
2. `.ai/architecture/architecture-baseline-v1.md`
3. `.ai/architecture/domain-model.md`
4. `CONTEXT.md`
5. `.ai/architecture/architecture-principles.md`
6. `.ai/architecture/OPEN_ITEMS.md`
7. `docs/adr/`

The Architecture Discovery Brief is historical context.

If any historical document conflicts with an ADR, Domain Model, or Architecture Baseline, the newer artifact is authoritative.

---

# Current Architecture

The architecture has established the following major concepts.

## Governance

* Policy
* Requirement
* Policy Binding
* Scope
* Attribute Providers
* Evaluation Strategies

## Evaluation

* Predicate Evaluation
* Desired-State Evaluation

The governance engine supports multiple evaluation strategies but remains a single engine.

Evaluation Strategies are engine-owned capabilities and are never runtime plug-ins.

---

## Governance Model

The platform separates:

* Technical evaluation
* Governance interpretation
* Compliance
* Coverage

Governance Relief consists of:

* Governance Exception
* Governance Exclusion

---

## Execution

Periodic reconciliation is the authoritative evaluation mechanism.

Event-driven processing is considered a future optimization.

Execution produces authoritative evidence.

Reports are derived from evidence.

---

## Remediation

The first implementation is read-only.

Enforcement is deferred.

When implemented, remediation is governed through immutable Remediation Plans.

Enforce mode represents remediation eligibility, not automatic write authority.

---

# Architectural Principles

Preserve the following principles unless a contradiction is demonstrated.

* Policy-first governance
* Brownfield-first adoption
* Minimal disruption to application teams
* Explicit intent over inference
* Uncertainty never grants privilege
* Evidence is authoritative
* Reports are derived
* Compliance and Coverage are independent dimensions
* One Governance Engine
* Multiple Evaluation Strategies
* Strategies compute technical facts
* The engine owns governance meaning
* Periodic reconciliation is authoritative
* Event-driven processing is acceleration only
* Evaluation Role constrains execution authority
* Restrictions may be inferred
* Authority may never be inferred

---

# Current Scope

The immediate objective is to produce a specification for the first end-to-end vertical slice.

The first slice remains intentionally small.

Current target capabilities include:

* Synthetic repository inventory
* GitHub-native Attribute Provider
* Scope Resolution
* Predicate Evaluation
* Composite Policy evaluation
* Compliance calculation
* Coverage calculation
* Evidence generation
* Dry-run Remediation Plan generation

No writes to GitHub are performed.

---

# Explicitly Out of Scope

Unless explicitly requested, do not expand the scope into:

* Production deployment
* Enterprise rollout
* AWS infrastructure
* Runner implementation
* ServiceNow integration
* Enterprise authentication
* High availability
* Horizontal scaling
* Event-driven execution
* Automatic remediation
* Performance optimization

These capabilities have intentionally been deferred.

---

# Working Style

Use the repository as the source of truth.

Do not rely on previous chat history.

When reviewing or extending the architecture:

* identify contradictions;
* identify ambiguity;
* identify hidden assumptions;
* identify unnecessary complexity;
* recommend the smallest viable change.

Do not introduce new architectural concepts unless required.

When proposing new architecture:

* explain why;
* identify impacted ADRs;
* preserve the existing Domain Model whenever possible.

---

# Expected Workflow

Follow the project's established methodology.

1. Understand the architecture.
2. Review the Domain Model.
3. Review relevant ADRs.
4. Validate terminology.
5. Produce or review specifications.
6. Review specifications before implementation.
7. Build incrementally using vertical slices.
8. Update architecture artifacts only when architectural decisions change.

Architecture precedes specification.

Specification precedes implementation.

Implementation validates architecture.

---

# Success Criteria

Every deliverable should:

* trace back to an ADR or Domain Model concept;
* preserve architectural consistency;
* maintain the ubiquitous language;
* support auditability and explainability;
* minimize disruption to existing development teams;
* remain suitable for brownfield enterprise adoption.

If architectural uncertainty is encountered, pause and identify the smallest architectural decision required before proceeding.
