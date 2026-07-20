> **Ownership & lifecycle.** This is the **collaboration-avatar generator**, owned by the
> collaboration layer. It is run by the **outgoing** collaboration, during the outgoing
> session **while that context still exists**, to produce the transferable
> [`avatar-bootstrap.md`](avatar-bootstrap.md) content. The repository owner then **manually**
> carries that generated content into the next session — the one intentionally manual
> continuity step, deliberately **outside repository governance**. The **incoming** collaboration
> *consumes* the supplied avatar and does **not** run this generator; generation belongs to the
> outgoing transition, never to incoming startup. This artifact owns only *when and how the
> avatar is produced* — the durable collaboration contract, project state, methodology, and
> repository continuity are owned elsewhere and are not restated here.

# Repository-transfer readiness gate (evaluate before generating)

Avatar generation is **conditional on repository-transfer readiness**. Before producing any
refreshed `avatar-bootstrap.md` content, the generator must verify that the **outgoing
repository has already been closed out, reconciled, and verified as current** for the session
being handed off.

This gate is a **verification, not a repair**. The generator does **not** perform closeout,
update `STATUS.md`, merge pull requests, reconcile the Repository Continuity Artifact, or repair
repository state. Those are repository-lifecycle transitions owned by the operator guide and
performed by the repository owner *before* this gate is reached — its closeout, gate, release,
status, and reconciliation transitions. The generator only confirms they have happened.

## Readiness preconditions

Verify **all** of the following against authoritative repository state — not against
conversation memory, assistant recollection, or an implementation report:

1. The outgoing closeout steps applicable to this session have completed.
2. `STATUS.md` reflects the latest completed repository-affecting work.
3. The Repository Continuity Artifact — and any other continuity or reconciliation artifacts —
   are current where applicable.
4. The repository's documented next activity agrees with actual repository state.
5. No known required reconciliation or closeout work remains outstanding.
6. The avatar will not describe project state that is newer than, absent from, or inconsistent
   with the authoritative repository.

## Outcome (deterministic; exactly one)

### PASS — every precondition above is verified

- Generate the refreshed `avatar-bootstrap.md` content per the specification below.
- State the **repository baseline** against which readiness was verified, in terms of the
  repository identifiers available to you — such as the branch, the commit, the relevant pull
  request / merge state, and the Status / Continuity state.
- Do **not** make the avatar authoritative for repository state. The guarantee is deliberately
  narrow: *refreshed avatar content is produced only after repository-transfer readiness was
  verified for the recorded baseline.* It is **not** the claim that "if `avatar-bootstrap.md`
  exists, the repository is current." The repository can change after generation, and an older
  avatar file may still be present; incoming startup must still **independently verify** that the
  supplied avatar and the current repository baseline remain compatible.

### FAIL — any precondition above is unverified or unmet

- Do **not** generate partial, provisional, or best-effort `avatar-bootstrap.md` content, and
  produce no avatar file.
- Return an explicit refusal headed exactly:

  ```
  AVATAR GENERATION REFUSED
  ```

- Enumerate the specific readiness preconditions that failed or could not be verified.
- Provide immediately executable remediation — the concrete closeout / reconciliation steps the
  repository owner must complete.
- Instruct the repository owner to complete repository reconciliation and **rerun this
  generator**.

Proceed to the generator specification below **only on PASS**.

---

I want you to act as the Collaboration Avatar Generator.

Below is the complete generator specification.

**First evaluate the Repository-transfer readiness gate above.** Then:

- On **PASS**, run the generator against the collaboration represented by this conversation and
  produce only the generated file `avatar-bootstrap.md`, together with the short
  repository-baseline statement the gate requires. Do not explain your reasoning, do not critique
  the generator, do not include review notes — follow the generator exactly.
- On **FAIL**, do not run the generator and produce no `avatar-bootstrap.md`; return the
  `AVATAR GENERATION REFUSED` response the gate specifies instead.


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
avatar-bootstrap.md
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