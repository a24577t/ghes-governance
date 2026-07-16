# Phase Gate Review

## Purpose

Evaluate whether the repository has reached a stable architectural milestone suitable for advancing to the next stage.

Your responsibility is to determine whether the project is ready to advance to the next phase.

This prompt is an architectural review gate.

It evaluates the current state of the repository.

It does **not** modify repository artifacts.

It does **not** redesign the architecture.

It does **not** publish the Architecture Baseline.

It determines whether the current phase has achieved its objectives and whether the repository is ready for the next architectural milestone.

---

# Inputs

Review the repository before beginning.

At minimum review:

- `.ai/architecture/STATUS.md`
- `.ai/architecture/domain-model.md`
- `.ai/architecture/architecture-principles.md`
- `CONTEXT.md`
- `docs/adr/`

When appropriate also review:

- Architecture Discovery Brief
- Current specifications
- Session summaries
- `OPEN_ITEMS.md` (if present)

Review only the artifacts necessary to evaluate the completed phase.

---

# Responsibilities

## 1. Verify Phase Objectives

Determine whether the objectives of the completed phase have been achieved.

Classify each objective as:

- Complete
- Partially Complete
- Deferred
- Not Completed

Explain any incomplete objectives.

---

## 2. Verify Architectural Integrity

Confirm that the repository accurately reflects the approved architecture.

Review:

- ADR consistency
- Domain Model consistency
- Architecture Principles
- Terminology
- Architectural traceability

Identify:

- contradictions
- undocumented architectural changes
- missing architectural decisions
- ambiguity requiring future clarification

Do not redesign the architecture.

---

## 3. Identify Blocking Issues

Identify issues that affect progression to the next phase.

Classify each issue as:

### Blocking

The project should not advance until resolved.

### Non-Blocking

The project may advance.

The issue should be documented or deferred.

Examples include:

- architectural debt
- specification debt
- documentation gaps
- implementation assumptions
- environmental unknowns

---

## 4. Assess Readiness

Determine overall readiness.

Possible outcomes:

- PASS
- PASS WITH CONDITIONS
- FAIL

Definitions:

### PASS

Phase objectives have been achieved.

Architecture remains internally consistent.

No blocking issues remain.

Architecture is ready to advance.

Publication is appropriate if a new architectural milestone has been reached.

### PASS WITH CONDITIONS

The next phase may begin.

Non-blocking issues must be documented and tracked.

Every condition must identify:
- affected repository artifact(s)
- recommended owner
- recommended resolution timing (before publication, during publication, after publication, or next phase)

### FAIL

Blocking issues remain.

The current phase must continue.

Explain the reasoning.

---

## 5. Recommend the Next Phase

Identify the appropriate next phase.

Examples:

- Architecture Discovery
- Architecture Consolidation
- Vertical Slice Specification
- Implementation
- Testing
- Enterprise Pilot

Explain why this is the correct next step.

## 6. Recommended Next Action

Exactly one of:

Publish Architecture Baseline
Continue Architecture Refinement
Begin Specification
Continue Specification Review
Begin Implementation
Produce Project Handof

## 7. Methodology Observations

Capture improvements to the project's engineering process.

These observations are not architectural issues and must not affect the readiness decision.

That keeps methodology evolution separate from architecture evaluation.
---

# Output

Produce a Phase Gate Review containing:

## Current Phase

## Phase Objectives Assessment

## Architecture Integrity Assessment

## Blocking Issues

## Non-Blocking Issues

## Readiness Decision

PASS

PASS WITH CONDITIONS

or

FAIL

## Recommendation

If the decision is:

### PASS

Recommend running:

`publish-architecture-baseline.md`

### PASS WITH CONDITIONS

Recommend documenting the listed conditions during Architecture Baseline publication before advancing.

### FAIL

Recommend continuing the current phase until blocking issues are resolved.

---

# Constraints

Do not:

- modify repository files
- publish an Architecture Baseline
- update STATUS.md
- create ADRs
- redesign the architecture
- generate implementation tasks
- recommend Git tags or releases

This prompt evaluates the repository.

Do not recommend changes solely because a better design is possible. Evaluate only whether the repository satisfies the current architecture.

It never changes repository state.

---

# Success Criteria

The review should answer one question:

**Is the project ready to advance to the next phase?**

The output should provide a clear, well-supported recommendation while preserving the separation between:

- evaluation (this prompt)
- publication (Architecture Baseline)
- implementation (future phases)

The result should leave no ambiguity about whether the next prompt should be executed.