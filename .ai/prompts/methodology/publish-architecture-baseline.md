# Architecture Baseline Publishing Prompt

## Purpose

A major project phase has successfully completed.

The Phase Gate Review has determined that the project is ready to advance.

Your responsibility is to publish the approved architectural milestone.

The primary artifact produced is a new **Architecture Baseline** that becomes the authoritative architectural snapshot for the completed phase.

This prompt also prepares the repository for the next project phase by updating the repository's published architectural state.

This prompt assumes the architecture has already been approved.

It does not redesign or re-evaluate the architecture.

---

# Preconditions

Execute this prompt only after:

- Architecture Consolidation is complete.
- Phase Gate Review returned **PASS** or **PASS WITH CONDITIONS**.
- Architectural decisions have been accepted.

If these conditions are not satisfied, stop and report that the repository is not ready for publication.

---

# Inputs

Review the repository before beginning.

At minimum review:

- `.ai/architecture/STATUS.md`
- `.ai/architecture/domain-model.md`
- `.ai/architecture/architecture-principles.md`
- `CONTEXT.md`
- Relevant ADRs
- Phase Gate Review

Also review when available:

- Previous Architecture Baseline
- Architecture Discovery Brief
- Session Summaries

Review only the artifacts necessary to publish the completed architectural milestone.

---

# Determine the Baseline Version

Locate the most recent Architecture Baseline.

Examples:

- architecture-baseline-v1.md
- architecture-baseline-v2.md
- architecture-baseline-v3.md

Publish the next sequential version.

Never overwrite an existing baseline.

Every Architecture Baseline is immutable.

---

# Responsibilities

## 1. Publish the Architecture

Produce a concise but complete description of the approved architecture.

The Architecture Baseline should summarize the architecture without replacing the ADRs.

Reference ADRs.

Do not reproduce ADR content.

Capture:

- Executive Summary
- Project Mission
- Current Phase
- Architecture Overview
- Governance Model
- Domain Overview
- Architecture Principles
- Current Scope
- Deferred Scope
- ADR Index
- Recommended Reading
- Next Baseline Trigger

---

## 2. Preserve Architectural Integrity

Do not introduce:

- new architecture
- new ADRs
- new terminology
- new principles
- new requirements

If contradictions are discovered:

- report them
- identify impacted ADRs
- stop publication

Do not resolve architectural contradictions during publication.

---

## 3. Publish Repository State

Update `STATUS.md` to reflect the newly published architectural milestone.

Update only:

- Completed Phase
- Current Phase
- Current Architecture Baseline
- Architecture Version
- Repository Version (when changed)
- Next Milestone

STATUS.md should remain concise and represent the current repository state.

---

## 4. Prepare Future Sessions

Verify that the repository is ready for a future Session Bootstrap.

Confirm:

- STATUS correctly references the latest Architecture Baseline.
- Repository navigation is correct.
- Architecture artifacts remain internally consistent.
- A new AI session can understand the project without relying on previous conversations.

The repository should become the authoritative project memory.

---

## 5. Repository Publication Recommendation

Determine whether the completed milestone should result in a repository release.

Recommend:

### Architecture Version

Recommend the next Architecture Version.

Examples:

- 1.0
- 1.1
- 2.0

Explain the recommendation.

---

### Repository Version

Recommend the repository version using Semantic Versioning.

Examples:

- v0.1.0
- v0.2.0
- v1.0.0

Explain the recommendation.

---

### Git Tag

If appropriate recommend:

- Annotated Git Tag
- Tag Name

Example:

```
v0.1.0
```

Do not create the tag.

---

### GitHub Release

If appropriate recommend:

- Release Title
- Release Summary

Do not publish the release.

Provide recommendations only.

---

# Required Sections

Every Architecture Baseline should contain:

1. Metadata
2. Executive Summary
3. Project Mission
4. Current Phase
5. Architecture Overview
6. Architecture Diagram
7. Architecture Principles
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

Every Architecture Baseline should begin with metadata similar to:

- Baseline Version
- Status
- Published Date
- Phase Completed
- Current Phase
- Supersedes
- Superseded By
- Architecture Version
- Related ADRs

---

# Repository Navigation

The published Architecture Baseline becomes the primary onboarding document.

Recommended reading order:

1. Latest Architecture Baseline
2. STATUS
3. Domain Model
4. Architecture Principles
5. CONTEXT
6. Relevant ADRs
7. Specifications

---

# Constraints

Do not:

- redesign the architecture
- re-evaluate the architecture
- rewrite ADRs
- create specifications
- generate implementation details
- create implementation tasks
- modify architectural history
- create Git tags
- publish GitHub Releases

This prompt publishes architecture.

It does not evolve architecture.

---

# Output

Publish:

`.ai/architecture/architecture-baseline-v<next>.md`

Update:

`.ai/architecture/STATUS.md`

Provide:

- Architecture Version Recommendation
- Repository Version Recommendation
- Git Tag Recommendation
- GitHub Release Recommendation

Do not perform repository release actions.

---

# Success Criteria

Successful publication means:

- the Architecture Baseline becomes the authoritative onboarding document;
- STATUS accurately reflects the newly published milestone;
- repository navigation is correct;
- the repository is ready for future Session Bootstrap;
- repository version recommendations are complete;
- the repository fully represents the approved architectural state without relying on previous chat history.

The repository should become the authoritative memory of the project.