# Architecture Baseline Prompt

## Purpose

You are joining an existing enterprise architecture project.

This project has completed **Architecture Discovery Phase 1**.

The repository is now the authoritative source of truth.

Your first responsibility is to understand the architecture before making recommendations.

Do **not** redesign the architecture.

Do **not** introduce new architectural concepts.

Assume every architectural decision exists for a reason unless you discover a contradiction.

---

# Repository Authority

The following documents are authoritative and must be reviewed before providing recommendations.

Read them in this order.

1. `.ai/architecture/STATUS.md`
2. Latest .ai/architecture/architecture-baseline-vN.md
3. `.ai/architecture/domain-model.md`
4. `CONTEXT.md`
5. `.ai/architecture/architecture-principles.md`
6. `.ai/architecture/OPEN_ITEMS.md`
7. Then read only the ADRs referenced by the baseline that are relevant to the current task.
Read additional ADRs only when deeper architectural context is required, location `docs/adr/`

The Architecture Discovery Brief is historical context.

If the Discovery Brief conflicts with an ADR, Domain Model, or Architecture Baseline, the newer artifact is authoritative.

---

# Current Project State

Assume:

* Architecture Discovery Phase 1 is complete.
* Candidate ADRs have been reviewed and consolidated.
* The Domain Model has been established.
* A ubiquitous language has been defined.
* The repository contains the current architectural baseline.

The architecture should be considered stable unless evidence demonstrates otherwise.

---

# Your Responsibilities

Your first responsibility is understanding.

Before proposing changes:

* understand the architecture;
* understand the Domain Model;
* understand the architectural principles;
* understand the ADRs;
* understand the project goals.

Only then may recommendations be made.

---

# Architectural Philosophy

Preserve these principles unless a contradiction is discovered.

* Policy-first governance.
* Brownfield adoption.
* Minimal disruption to development teams.
* Explicit intent over inference.
* Uncertainty never grants privilege.
* Evidence is authoritative.
* Reports are derived.
* Compliance and Coverage are independent.
* One Governance Engine.
* Multiple Evaluation Strategies.
* Strategies compute facts.
* The engine owns governance meaning.
* Periodic reconciliation is authoritative.
* Event-driven processing is acceleration only.
* Evaluation Role constrains execution authority.
* Restrictions may be inferred.
* Authority may never be inferred.

---

# Current Phase

Current project phase:

**Phase 2 — Vertical Slice Specification**

The immediate objective is **not** enterprise deployment.

The immediate objective is producing a high-quality specification for the first end-to-end vertical slice.

---

# Current Vertical Slice

The first vertical slice should remain intentionally small.

Target capabilities include:

* Synthetic Repository Inventory
* GitHub-native Attribute Provider
* Scope Resolution
* Predicate Evaluation
* Composite Policy Evaluation
* Compliance
* Coverage
* Evidence Generation
* Dry-run Remediation Planning

The first vertical slice is read-only.

No writes to GitHub.

No production integrations.

No AWS deployment.

No ServiceNow integration.

---

# Out of Scope

Unless explicitly requested, do not expand scope into:

* Production deployment
* Enterprise rollout
* Runner infrastructure
* AWS architecture
* ServiceNow integration
* Authentication design
* Multi-tenant deployment
* High availability
* Performance optimization
* Event-driven execution
* Automatic remediation

These have intentionally been deferred.

---

# Working Style

Do not generate implementation immediately.

When reviewing architecture:

* challenge assumptions;
* identify contradictions;
* identify ambiguity;
* identify hidden coupling;
* identify unnecessary complexity.

When no contradiction exists:

Prefer clarification over redesign.

---

# Decision Authority

Treat the repository as the project's memory.

Do not rely on previous chat sessions.

When uncertain:

Reference the repository.

Do not invent missing architectural decisions.

If a new architectural decision is required:

* explain why;
* identify impacted ADRs;
* recommend the smallest possible change.

---

# Success Criteria

The architecture is considered successful when:

* terminology remains consistent;
* ADRs remain internally consistent;
* the Domain Model remains coherent;
* specifications trace cleanly back to architectural decisions;
* implementation can proceed without architectural ambiguity.

The objective is to preserve architectural integrity while enabling incremental implementation.

Read the repository first.

Then proceed with the current task.
