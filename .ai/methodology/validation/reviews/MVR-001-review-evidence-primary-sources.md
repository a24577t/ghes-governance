# MVR-001 — Review evidence: repository artifacts are primary review evidence

- **Date:** 2026-07-20
- **Adjudicator:** Eric — human architect and design authority (principle P1)
- **Trigger:** Human decision converting a recorded observation into accepted methodology
- **Observations in scope:** MO-017

Immutable, append-only review record. It references the observation by its stable identifier and never edits it; the authoritative artifact it points to exists in this same reviewed change set, so this record needs no later amendment.

## Dispositions

- **MO-017 → Accepted** → `.ai/prompts/methodology/review-discipline.md` (section *"Review evidence — primary sources"*), extended in this same reviewed change set.

  **Rationale.** Eric has decided that independent architectural and quality-gate reviews must use actual repository artifacts — the PR diff, the changed files, or equivalent repository state — as primary review evidence. An implementation report may support a review but may not substitute for inspecting the repository artifacts, and a final quality-gate PASS is not issued from a summary alone; if the artifacts are unavailable the review remains pending. The authoritative Review Discipline methodology now states this rule; the collaboration contract references it; and the deterministic load order routes review / quality-gate activation to it.

## Notes

The disposition is recorded only here, never in `observations.md`; MO-017 is unchanged. Authority for the rule arises from this Accepted disposition together with the authoritative-artifact change it points to — not from this subsystem itself.
