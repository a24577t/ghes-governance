# Session Bootstrap Prompt

## Purpose

You are beginning a new working session in an existing enterprise architecture and software project.

Your first responsibility is to understand the current project state before answering questions, recommending changes, creating plans, or modifying files.

The repository is the project’s persistent memory.

Previous chat history is not authoritative and must not be required to continue the project.

This prompt is read-only.

It does not create, modify, rename, move, commit, or delete repository content.

---

# Responsibilities

You must:

1. Identify the current project phase.
2. Locate the latest approved Architecture Baseline.
3. Understand the current architecture at the level necessary for the requested task.
4. Review current status, open items, and relevant detailed decisions.
5. Confirm your understanding before beginning substantive work.

Do not redesign the architecture unless the requested task reveals a genuine contradiction or missing architectural decision.

---

# Reading Order

Read repository artifacts in the following order.

## 1. Current Project Status

Read:

```text
.ai/architecture/STATUS.md
```

Use it to determine:

* current phase;
* latest Architecture Baseline;
* architecture version;
* repository version, when recorded;
* current objective;
* next milestone;
* current blocking conditions or open architectural decisions.

If `STATUS.md` does not exist or conflicts with the repository, report the inconsistency.

Do not create or repair it during bootstrap.

## 2. Latest Architecture Baseline

Locate all files matching:

```text
.ai/architecture/architecture-baseline-v*.md
```

Determine the latest baseline using the baseline version and status recorded inside the documents.

Read only the latest approved or otherwise currently authoritative baseline.

Do not assume that filename ordering alone establishes authority.

Earlier baselines are historical artifacts. Read them only when:

* the current task concerns architectural evolution;
* a change-since-baseline comparison is required;
* the latest baseline explicitly refers the reader to an earlier baseline.

If no Architecture Baseline exists, report that fact and continue using the remaining authoritative artifacts.

## 3. Domain and Terminology

Read, when present:

```text
.ai/architecture/domain-model.md
.ai/architecture/architecture-principles.md
CONTEXT.md
```

Use these documents to understand:

* domain entities and relationships;
* invariants;
* architectural principles;
* approved terminology;
* terms that must be avoided.

Do not redefine established terminology.

## 4. Current Open Items

Read:

```text
.ai/architecture/OPEN_ITEMS.md
```

only if it exists and is identified by `STATUS.md` or the latest baseline as a current authoritative artifact.

Do not treat deferred items as current requirements.

Do not reopen resolved architectural questions.

## 5. Relevant ADRs

Read only the ADRs relevant to the current task.

Use the Architecture Baseline’s ADR index and recommended-reading section to select them.

Read additional ADRs when:

* the current task crosses several architectural domains;
* the baseline lacks sufficient detail;
* an apparent contradiction must be investigated.

Do not automatically read every ADR unless the task is a full architecture review.

## 6. Specifications and Implementation Artifacts

When the current phase or requested task involves specification or implementation, read the relevant artifacts after the architectural material.

Examples include:

```text
specifications/
docs/specifications/
src/
tests/
```

Use actual repository structure rather than assuming these paths exist.

Architecture remains authoritative over specifications.

Specifications remain authoritative over implementation.

---

# Authority Order

Unless a more specific repository rule states otherwise, use this authority order:

1. Accepted ADRs
2. Latest approved Architecture Baseline
3. Domain Model
4. Architecture Principles
5. Approved specifications
6. Proposed ADRs
7. Current `STATUS.md`
8. Historical discovery documents
9. Session summaries and prior chat context

When artifacts conflict:

* identify the conflict;
* cite the affected files and sections;
* do not silently choose a new interpretation;
* do not modify files during bootstrap.

If the repository explicitly defines a different authority order, follow the repository-defined order and report it.

---

# Historical Documents

Treat documents such as the Architecture Discovery Brief and session summaries as historical context.

They explain how the architecture evolved but do not override newer architectural artifacts.

Do not rewrite history during bootstrap.

---

# Architectural Conduct

Preserve established architecture unless evidence requires reconsideration.

When reviewing a task:

* prefer clarification over redesign;
* identify contradictions rather than silently resolving them;
* distinguish architecture questions from specification and implementation questions;
* recommend the smallest change that resolves a genuine gap;
* identify affected ADRs when a new architectural decision is required.

Do not invent missing decisions.

Do not infer authority.

Uncertainty does not grant permission to proceed with destructive or architecture-changing work.

---

# Output

After reading the necessary artifacts, provide a concise **Session Context Report** containing:

## Current State

* Current project phase
* Current objective
* Latest Architecture Baseline
* Architecture version
* Repository version, when recorded
* Next milestone

## Relevant Architecture

Summarize only the architectural concepts relevant to the current task.

Do not reproduce the complete baseline.

## Relevant Sources

List the specific files and ADRs consulted.

## Open or Blocking Items

List only items that affect the current task.

## Readiness

State one of:

* `Ready to Proceed`
* `Ready with Conditions`
* `Not Ready`

Explain any conditions or blockers briefly.

---

# Constraints

Do not:

* modify repository files;
* create documents;
* update `STATUS.md`;
* publish an Architecture Baseline;
* create or change ADRs;
* create specifications;
* create tasks or tickets;
* commit or push changes;
* create tags or releases;
* rely on previous chat history as authoritative context.

This prompt exists only to establish accurate working context for the new session.

---

# Success Criteria

The bootstrap is successful when:

* the current phase and objective are correctly identified;
* the latest authoritative baseline is correctly selected;
* only task-relevant detailed artifacts are read;
* terminology and architectural authority are preserved;
* conflicts and missing information are surfaced;
* no repository content is changed;
* the session can continue without relying on earlier chat history.

