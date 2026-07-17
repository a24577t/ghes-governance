I want you to act as the Collaboration Avatar Generator.

Below is the complete generator specification.

Run the generator against the collaboration represented by this conversation.

Produce only the generated file:

collaboration-avatar-bootstrap.md

Do not explain your reasoning.
Do not critique the generator.
Do not include review notes.
Follow the generator exactly.


# Collaboration Avatar Generator

## Purpose

Analyze the collaboration represented by the available conversation history and generate a Collaboration Avatar that preserves only the durable evolution of the collaboration itself.

The Collaboration Avatar is a durable collaboration artifact.

It is **not**:

- Project documentation
- Architecture documentation
- Repository Continuity
- Methodology documentation
- Session handoff
- Conversation summary
- Personal notes
- AI memory
- Repository state

Its purpose is to capture only the stable collaboration knowledge that improves future collaboration across sessions, projects, and AI engines.

The Collaboration Avatar represents the collaborator's current best understanding after validating, merging, refining, and retiring candidate collaboration insights.

---

# Design Principles

The generated Collaboration Avatar must:

- Minimize future collaboration startup cost.
- Preserve collaboration knowledge rather than project knowledge.
- Remain independent of any specific repository.
- Remain independent of any specific AI engine.
- Prefer durable heuristics over historical narrative.
- Represent current understanding rather than accumulated history.
- Prefer refinement over accumulation.
- Remain concise enough to load at the beginning of every collaboration.

When uncertain whether something belongs in the Collaboration Avatar, ask:

> "Will this improve future collaboration across different projects?"

If the answer is no, omit it.

---

# Discover

Determine, where applicable:

## Collaboration Function

Identify the enduring collaboration function independent of any specific AI engine.

Describe only the enduring collaboration function that should persist across AI engines.

Capture enduring collaboration functions, not temporary working roles.

---

## Collaboration Knowledge

Identify durable collaboration knowledge that has emerged through experience.

This may include:

- principles;
- heuristics;
- recurring patterns;
- collaboration guidance;
- durable lessons learned.

Prefer concise guidance that consistently improves future collaboration.

Include only knowledge expected to remain valuable across future collaborations.

---

## Mental Model Evolution

Identify significant changes in how the collaboration understands or approaches problems.

Record only changes that influence future collaboration.

Do not document project history.

---

## Abandoned Directions

Identify approaches intentionally abandoned because a better collaboration pattern emerged.

Capture:

- Decision
- Reason
- Revisit criteria

Include only if the guidance remains valuable.

---

## Deferred Questions

Identify unresolved collaboration questions worth revisiting.

Capture:

- Question
- Reason deferred
- Trigger to revisit

Do not include project backlog items.

---

# Exclude

Do NOT include:

- Project architecture
- Repository structure
- ADRs
- STATUS
- Repository Continuity
- Implementation details
- Session summaries
- Conversation transcripts
- Temporary observations
- Brainstorming
- Historical discussion
- Project-specific knowledge
- Personal preferences
- Engine-specific behavior
- Prompt wording
- Duplicate concepts

---

# Boundary Rules

Before promoting any collaboration insight, ask:

1. Is it collaboration knowledge rather than project knowledge?
2. Would it remain true across projects?
3. Is it durable enough to justify inclusion?

If uncertain, omit it.

---

# Editorial Workflow

The Collaboration Avatar is a curated artifact.

The generator is responsible for editorial review rather than conversation summarization.

When generating the Collaboration Avatar, the generator shall:

- identify candidate collaboration insights;
- review all available `avatar-safe:` candidate insights;
- validate every candidate against the Boundary Rules;
- merge overlapping concepts into coherent guidance;
- retire or reject superseded, redundant, or project-specific knowledge; and
- publish a concise Collaboration Avatar representing the current  collaboration.

The generator shall refine collaboration knowledge rather than accumulate it.

The published Collaboration Avatar must represent the current state of the collaboration, not the history of how it evolved.

Prefer observations that are actionable over observations that are merely descriptive.

---

# Collaboration Evolution Practice

The Collaboration Avatar is intended to evolve through use.

During collaboration, actively look for durable improvements to the collaboration itself.

When such an insight is discovered, explicitly mark it during the conversation using:

```
avatar-safe: <candidate collaboration insight>
```

Use `avatar-safe:` only for candidate collaboration knowledge that:

- improves future collaboration;
- is independent of the current project;
- is not already authoritative elsewhere;
- is expected to remain useful across sessions or AI engines.

`avatar-safe:` annotations are candidate insights.

They are not automatically accepted.

During each Collaboration Avatar generation, review every `avatar-safe:` annotation using the Editorial Workflow.

Only promoted collaboration knowledge becomes part of the published Collaboration Avatar.

The generator must review all available avatar-safe: candidate insights before producing the Collaboration Avatar. If candidate insights are maintained outside the current conversation, they must be included in the review.

---

# Validation

Before finalizing the Collaboration Avatar, verify:

- The document represents collaboration rather than project knowledge.
- The document represents current understanding rather than historical accumulation.
- Superseded concepts have been removed or merged.
- Similar concepts have been consolidated.
- The document remains concise enough to be practical as a bootstrap.
- Every published insight passes the Boundary Rules.
- The document can be understood without reference to a specific conversation.

If uncertain, omit it.

---

# Output

Generate:

```
collaboration-avatar-bootstrap.md
```

The Collaboration Avatar should contain only curated collaboration knowledge.

It should:

- improve future collaboration;
- remain independent of projects and AI engines;
- contain only durable collaboration knowledge.

Do not include:

- generator instructions;
- editorial workflow;
- review notes;
- rejected candidates;
- intermediate reasoning;
- conversation summaries;
- superseded concepts.

The published Collaboration Avatar should be concise, internally consistent, and suitable for loading at the beginning of future collaborations.