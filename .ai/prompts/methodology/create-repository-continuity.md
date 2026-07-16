# Session Handoff Prompt

# Purpose

Determine the latest published Architecture Baseline.

The Project Handoff captures **all project work completed since that baseline that has not yet become authoritative repository state**.

Its purpose is to bridge the gap between the current published Architecture Baseline and the next published Architecture Baseline.

It is a temporary working artifact.

It is not an architecture document.

It is not a specification.

It is not a design document.

It is not a permanent project record.

Once all unpublished work has been incorporated into authoritative repository artifacts, the Project Handoff should be deleted or replaced.

---

# Inputs

Determine the latest published Architecture Baseline.

Review repository work completed since that baseline.

When available review:

- STATUS.md
- Latest Architecture Baseline
- Previous Project Handoff
- Newly created or modified repository artifacts
- Relevant discussion from working sessions

Do not reread architecture already captured by the latest Architecture Baseline unless required to understand unpublished work.

---

# Responsibilities

## 1. Summarize Completed Work

Briefly summarize the significant work completed during the session.

Do not restate architecture already captured in:

- Architecture Baselines
- ADRs
- Domain Model
- STATUS

Reference those artifacts rather than duplicating them.

---

## 2. Identify Unpublished Work

List work that has been discussed but has **not** yet become repository state.

Examples include:

- pending document updates
- pending prompt revisions
- pending ADR reviews
- pending specifications
- pending implementation work

Only include actionable items.

---

## 3. Identify Outstanding Decisions

List architectural or methodological decisions that remain unresolved.

For each item indicate:

- decision required
- recommended next step

If no decisions remain, explicitly state:

> None

---

## 4. Recommend the Next Session

Identify the single best starting point for the next working session.

Examples:

- Review generated Architecture Baseline
- Begin Vertical Slice Specification
- Review Specification Draft
- Continue Architecture Consolidation

Recommend only one primary starting point.

---

## 5. Repository State

Summarize the repository state.

Include:

- Current Phase
- Latest Architecture Baseline
- Architecture Version
- Repository Version (if known)

Do not duplicate STATUS.

Reference it.

---

# Output

Publish:

```
.ai/working/project-handoff.md
```

The document should contain:

# Session Handoff

## Created

Date

## Current Repository State

Reference STATUS.

## Completed Since Last Baseline

Concise summary.

## Work Not Yet Published

Outstanding repository updates.

## Outstanding Decisions

None

or

list of remaining decisions.

## Recommended First Task

One recommended starting point.

## Notes

Optional observations that may help the next session.

---

# Constraints

Do not:

- rewrite architecture
- summarize ADRs
- duplicate the Architecture Baseline
- duplicate STATUS
- redesign the project
- create implementation tasks
- invent future work

The Session Handoff exists only to bridge unfinished work between sessions.

---

# Lifecycle

The Session Handoff is temporary.

Session Bootstrap should read it only if it exists.

Once its contents have been incorporated into authoritative repository artifacts, it should be deleted or replaced by a newer handoff.

It is never authoritative over:

- Architecture Baselines
- ADRs
- Domain Model
- Architecture Principles
- STATUS

---

# Success Criteria

A future Session Bootstrap should be able to read this document in under two minutes and immediately understand:

- what was completed;
- what remains unpublished;
- where work should resume.

The Session Handoff should never become a permanent architecture artifact.