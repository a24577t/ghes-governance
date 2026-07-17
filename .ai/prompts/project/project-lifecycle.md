AI-Assisted Engineering Lifecycle
Phase 1 — Active Working Session

This is where design, review, implementation, or specification work happens.

ChatGPT

Role:

Architect
Reviewer
Instructor
Methodology owner
Phase gate reviewer
Claude

Role:

Primary implementation agent
Repository editor
Specification writer
Documentation maintainer

Artifacts produced:

ADRs
Specifications
Domain Model
CONTEXT
STATUS
Architecture updates
Implementation

Repository state:

Working

Nothing is authoritative until committed and merged.

Phase 2 — Session Wrap-up

When the planned work for the session is complete.

Run in this order.

Repository Review

Quick check:

clean working tree
commits complete
PR merged (if applicable)
no accidental files
version consistency
Project Handoff

Run:

create-project-handoff.md

Purpose:

Capture only work since the latest published Architecture Baseline that has not yet become authoritative repository state.

Output:

.ai/working/project-handoff.md

If no unpublished work exists:

The handoff should explicitly say:

None.

Phase 3 — New Session Bootstrap

This is the beginning of every ChatGPT or Claude session.

Run:

session-bootstrap.md

Read:

STATUS
Latest Architecture Baseline
Project Handoff (if present)

Only read additional documents when necessary.

This should answer:

Where are we?
What changed?
What remains?
Phase 4 — Milestone Review

When a milestone is believed complete.

Run:

phase-gate-review.md

Possible outcomes:

PASS
PASS WITH CONDITIONS
FAIL

Nothing changes in the repository.

This is purely evaluation.

Phase 5 — Publish Architecture

Only after PASS.

Run:

publish-architecture-baseline.md

Output:

architecture-baseline-vN.md

Update:

STATUS.md

Repository memory becomes authoritative.

The Project Handoff should now be empty or deleted because everything it contained has been published.

Phase 6 — Release Audit

Run:

project-release.md

Verify:

Repository consistency
Architecture consistency
Documentation
Versioning
Release readiness

Recommend:

Repository Version
Git Tag
GitHub Release

No repository changes.

Phase 7 — Repository Release

Human performs:

git tag
git push --tags

GitHub Release

Release notes

Repository milestone complete.

Beginning the Next Milestone

Start over at

Session Bootstrap
ChatGPT Session Lifecycle
Open ChatGPT

↓

Session Bootstrap

↓

Architecture / Review / Teaching

↓

Repository work via Claude

↓

Project Handoff

↓

End ChatGPT session
Claude Session Lifecycle
Open Claude

↓

Session Bootstrap

↓

Repository work

↓

Commit

↓

Push

↓

Project Handoff

↓

End Claude session

Claude never relies on previous conversations.

Everything comes from the repository.

Complete Project Lifecycle
New Session
      │
      ▼
Session Bootstrap
      │
      ▼
Architecture / Specification / Implementation
      │
      ▼
Repository Commits / PR
      │
      ▼
Project Handoff
      │
────── Session Ends ──────
      │
      ▼
New Session
      │
      ▼
Session Bootstrap
      │
      ▼
Continue Work
      │
      ▼
Phase Gate Review
      │
      ├──────── FAIL
      │            │
      │            ▼
      │      Continue Working
      │
      └──────── PASS
                   │
                   ▼
      Publish Architecture Baseline
                   │
                   ▼
          Project Release Audit
                   │
                   ▼
             Git Tag / Release
                   │
                   ▼
          Begin Next Milestone