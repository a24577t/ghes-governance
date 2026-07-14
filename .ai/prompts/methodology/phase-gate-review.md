# Phase Complete Review

## Purpose

A major project phase has completed.

Your responsibility is to determine whether the project is ready to transition to the next phase.

Do not assume completion because work has stopped.

Verify that the phase objectives have been achieved.

The goal is to establish a controlled phase gate similar to an enterprise architecture review.

---

# Inputs

Review the repository before beginning.

At minimum review:

* `.ai/architecture/STATUS.md`
* `.ai/architecture/architecture-baseline-v1.md`
* `.ai/architecture/domain-model.md`
* `.ai/architecture/architecture-principles.md`
* `.ai/architecture/OPEN_ITEMS.md`
* `CONTEXT.md`
* `docs/adr/`

If applicable, also review:

* Specifications
* Pull Requests
* Session summaries
* Roadmap

---

# Responsibilities

## 1. Verify Phase Objectives

Determine whether the documented objectives for the completed phase were achieved.

List:

* Completed
* Partially Complete
* Deferred
* Not Completed

---

## 2. Architecture Review

Confirm:

* ADRs remain internally consistent.
* Domain Model remains consistent.
* Terminology remains consistent.
* No undocumented architectural changes exist.

Identify any contradictions.

---

## 3. Documentation Review

Verify required documents exist and are current.

Examples include:

* STATUS
* Domain Model
* Architecture Baseline
* Architecture Principles
* ADRs
* Glossary
* Roadmap
* Open Items

Identify anything missing.

---

## 4. Technical Debt

Identify:

* Architectural debt
* Specification debt
* Documentation debt
* Implementation debt

Recommend whether each item should:

* Block progression
* Be deferred
* Become backlog work

---

## 5. Risks

Identify remaining risks.

Classify each as:

* High
* Medium
* Low

Explain whether each risk prevents advancing to the next phase.

---

## 6. Readiness Assessment

Determine the current readiness.

Possible outcomes:

* Not Ready
* Ready with Conditions
* Ready

Explain the reasoning.

---

## 7. Next Phase

Identify the recommended next phase.

Examples:

* Architecture Discovery
* Architecture Consolidation
* Architecture Baseline
* Specification
* Implementation
* Testing
* Enterprise Pilot

Explain why this is the correct next step.

---

## 8. Deliverables

Generate:

* Phase Summary
* Major Accomplishments
* Key Decisions
* Remaining Risks
* Deferred Work
* Lessons Learned
* Recommended Next Actions

---

# Constraints

Do not redesign the architecture.

Do not introduce new architectural concepts.

Do not create implementation tasks.

Do not modify ADR status.

This review is an assessment, not a design session.

---

# Success Criteria

The phase is complete when:

* objectives have been achieved;
* architecture remains internally consistent;
* documentation accurately reflects the current state;
* remaining risks are understood;
* the next phase can begin with confidence.

Provide a recommendation of:

* **Ready**
* **Ready with Conditions**
* **Not Ready**

with clear justification.
