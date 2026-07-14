# Project Release Prompt

## Purpose

A project phase has successfully completed.

The Phase Gate Review has passed.

The Architecture Baseline has been published.

Your responsibility is to determine whether the repository should be released and to recommend all versioning updates required for this milestone.

This prompt does **not** create releases.

It prepares the project for release by ensuring all versioning, documentation, and milestone artifacts remain consistent.

---

# Inputs

Review the repository before beginning.

At minimum review:

- `.ai/architecture/STATUS.md`
- Latest Architecture Baseline
- `.ai/architecture/domain-model.md`
- `.ai/architecture/OPEN_ITEMS.md`
- Phase Gate Review
- Previous releases (if any)

Also review when available:

- RELEASES.md
- CHANGELOG.md
- Git tags
- GitHub Releases

---

# Responsibilities

## 1. Determine Repository Version

Recommend the next repository version using Semantic Versioning.

Guidelines:

### Major

Breaking architectural evolution.

Examples:

- Enterprise deployment
- Multi-instance architecture
- Major governance redesign

### Minor

New architectural capability.

Examples:

- Vertical Slice complete
- GHES integration
- AWS deployment

### Patch

Editorial improvements.

Examples:

- Documentation corrections
- Clarifications
- Typographical fixes

Explain why the recommended version is appropriate.

---

## 2. Determine Architecture Version

Recommend the Architecture Version.

Architecture Version reflects architectural maturity rather than repository maturity.

Examples:

```
1.0
1.1
2.0
```

Explain any version increment.

---

## 3. Verify Architecture Baseline

Confirm:

- latest baseline published
- metadata complete
- supersedes information correct
- next baseline trigger documented

Identify any deficiencies.

---

## 4. Recommend Git Tag

Recommend an annotated Git tag.

Example:

```
v0.1.0
```

Include:

- tag name
- release title
- release description

Do not create the tag.

---

## 5. Recommend GitHub Release

If appropriate, recommend creating a GitHub Release.

Include:

- Release Title
- Summary
- Highlights
- Known Limitations
- Next Phase

Do not publish the release.

---

## 6. Update Release History

If RELEASES.md exists:

Recommend a new release entry.

If it does not exist:

Recommend creating RELEASES.md.

Summarize:

- major accomplishments
- completed phase
- architecture version
- baseline version
- major ADRs
- next milestone

---

## 7. Verify Repository Status

Confirm:

- STATUS.md reflects the new phase
- Current Phase updated
- Previous Phase marked complete

Identify inconsistencies.

---

## 8. Verify Documentation

Confirm that:

- Architecture Baseline exists
- Domain Model is current
- Architecture Principles are current
- ADR Index is current
- Open Items reviewed
- Session Summary archived

Identify missing artifacts.

---

## 9. Release Readiness Assessment

Determine:

- Ready for Release
- Ready with Conditions
- Not Ready

Explain the reasoning.

---

# Deliverables

Produce:

## Repository Version Recommendation

## Architecture Version Recommendation

## Git Tag Recommendation

## GitHub Release Recommendation

## RELEASES.md Update

## Documentation Review

## Remaining Risks

## Next Milestone

---

# Constraints

Do not:

- create Git tags
- publish releases
- modify repository files
- create ADRs
- redesign the architecture

Only review and recommend.

---

# Success Criteria

All project versioning should be internally consistent.

Repository versioning, Architecture Version, Architecture Baseline, Git tags, GitHub Releases, and project documentation should all describe the same milestone.

The project should have a clear transition from one completed phase to the next.

The recommendation should leave the repository ready for an intentional, auditable release.