# Architecture Baseline Publishing Prompt

## Purpose

A major project phase has successfully completed and the Phase Gate Review has determined that the project is ready to advance.

Your responsibility is to publish a new **Architecture Baseline** that becomes the authoritative architectural snapshot for this milestone.

The Architecture Baseline is the primary onboarding document for the project.

It summarizes the approved architecture at a specific point in the project's evolution and provides navigation into the repository.

The Architecture Baseline is:

- NOT an Architecture Discovery artifact
- NOT an ADR
- NOT a Design Document
- NOT a Specification
- NOT an Implementation Guide

It is a **consolidation artifact** that reflects approved architectural decisions.

It must never introduce new architecture.

---

# Inputs

Review the repository before beginning.

At minimum review:

- `.ai/architecture/STATUS.md`
- `.ai/architecture/domain-model.md`
- `.ai/architecture/architecture-principles.md`
- `.ai/architecture/OPEN_ITEMS.md`
- `CONTEXT.md`
- `docs/adr/`

Also review when available:

- Previous Architecture Baseline
- Architecture Discovery Brief
- Phase Gate Review
- Session Summaries
- Roadmap

---

# Determine the Baseline Version

Locate the most recent Architecture Baseline.

Examples:

- architecture-baseline-v1.md
- architecture-baseline-v2.md
- architecture-baseline-v3.md

Publish the next sequential version.

Never overwrite an existing baseline.

Every baseline is immutable and represents an approved architectural milestone.

---

# Responsibilities

## 1. Consolidate the Architecture

Produce a concise but complete description of the approved architecture.

Reference ADRs.

Do not duplicate ADR content.

The baseline is an architectural index.

It is not a replacement for the ADRs.

---

## 2. Preserve Architectural Integrity

Do not introduce:

- new architectural concepts
- new principles
- new ADRs
- new requirements
- new terminology

If contradictions are discovered:

- report them
- identify impacted ADRs
- stop publication

Do not resolve architectural contradictions inside the baseline.

---

## 3. Capture the Current Architecture

Describe:

- Project Mission
- Current Phase
- Architecture Overview
- Governance Model
- Domain Overview
- Architectural Principles
- Current Scope
- Deferred Scope

---

## 4. Record Major Decisions

Summarize the major architectural decisions.

Each decision must reference its governing ADR.

Do not reproduce ADR content.

---

## 5. Record Deferred Work

Summarize:

- deferred capabilities
- future architectural work
- environmental assumptions
- known limitations

Deferred work is informational.

It is not a backlog.

---

## 6. Produce a Change Summary

If a previous baseline exists include:

# Changes Since Previous Baseline

Summarize:

- newly added ADRs
- refined ADRs
- removed assumptions
- completed phases
- newly deferred capabilities
- architectural changes

If this is the first baseline omit this section.

---

## 7. Repository Navigation

Provide a recommended reading order for future engineers and AI assistants.

The baseline becomes the primary onboarding document.

Recommended order:

1. STATUS
2. Latest Architecture Baseline
3. Domain Model
4. Architecture Principles
5. CONTEXT (Glossary)
6. Relevant ADRs
7. Specifications

---

## 8. Architecture Overview Diagram

Include a simple high-level architecture diagram.

Use Mermaid when appropriate.

The objective is orientation rather than implementation detail.

---

## 9. What This Baseline Is

Include a short section explaining:

- what the baseline represents
- what it should be used for
- what documents contain additional detail

---

## 10. What This Baseline Is Not

Explicitly state that this document is not:

- the specification
- the implementation guide
- the discovery brief
- the ADR collection

---

## 11. Recommended Reading

Provide recommended ADRs grouped by topic.

For example:

- Governance
- Evaluation
- Execution
- Evidence
- Remediation

This should help readers quickly locate detailed architectural decisions.

---

## 12. Next Baseline Trigger

Document when the next Architecture Baseline should be published.

Examples:

- Vertical Slice 1 complete
- GHES integration complete
- Enterprise Pilot complete

This establishes the expected architectural lifecycle.

---

# Required Sections

Every Architecture Baseline should contain:

1. Metadata
2. Executive Summary
3. Project Mission
4. Current Phase
5. Architecture Overview
6. Architecture Diagram
7. Architectural Principles
8. Domain Overview
9. ADR Index
10. Current Scope
11. Deferred Scope
12. Repository Navigation
13. Open Architectural Items
14. Recommended Reading
15. What This Baseline Is
16. What This Baseline Is Not
17. Next Baseline Trigger
18. Changes Since Previous Baseline (when applicable)

---

# Metadata

Every baseline should begin with metadata similar to:

- Baseline Version
- Status
- Published Date
- Phase Completed
- Current Phase
- Supersedes
- Superseded By
- Architecture Version
- Related ADRs
- Recommended Repository Release (optional)
  
---

# Constraints

Do not:

- redesign the architecture
- rewrite ADRs
- create specifications
- generate implementation details
- create tickets
- modify architectural history

This document reflects architecture.

It does not evolve architecture.

---

# Output

Publish:

`.ai/architecture/architecture-baseline-v<next>.md`

The document should be suitable for:

- onboarding architects
- onboarding senior engineers
- onboarding AI assistants
- executive technical reviews
- architecture governance reviews

---

# Success Criteria

A knowledgeable engineer should be able to understand the architecture by reading this document before consulting the Domain Model or ADRs.

Every architectural statement must trace back to:

- an approved ADR
- the Domain Model
- the Architecture Principles

If architectural statements cannot be traced, report them rather than inventing new architecture.

The published baseline becomes the authoritative architectural snapshot for the completed project phase.

Future AI sessions should begin by reading the **latest Architecture Baseline** before consulting supporting architecture artifacts.

## Versioning

Every published Architecture Baseline must review versioning.

Determine:

### 1. Baseline Version

Publish the next sequential Architecture Baseline.

Examples:

- architecture-baseline-v1.md
- architecture-baseline-v2.md

### 2. Architecture Version

Recommend the Architecture Version.

Use Semantic Versioning principles:

- Major (2.0) – significant architectural evolution
- Minor (1.1) – incremental architectural capability
- Patch (1.0.1) – editorial or clarification changes only

Explain why the version changed.

### 3. Repository Release

Determine whether the completed phase represents a release milestone.

If appropriate, recommend:

- Git tag (for example `v1.0.0`)
- RELEASES.md update
- CHANGELOG update (if maintained)

Do not create Git tags.

Only recommend release actions.

