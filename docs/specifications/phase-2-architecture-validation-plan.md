# Phase 2 Architecture Validation Plan

| Field | Value |
|---|---|
| Type | Phase plan — **not a specification, not agent-ready** |
| Status | Draft for review |
| Date | 2026-07-14 |
| Derived from | The original Vertical Slice 1 specification draft (2026-07-14), re-scoped by the same-day scope review |
| Governs | The full architecture-validation phase (Phase 2) as a sequence of implementation slices |
| Authoritative architecture | Architecture Baseline v1 (`.ai/architecture/architecture-baseline-v1.md`), Architecture Version 1.0.3, ADRs 0001–0015 |

**This document must never be labeled `ready-for-agent` or implemented from directly.** It is the phase-level map: the consolidated definition of what the POC phase demonstrates (the union of the ADR "first vertical slice" / "POC boundary" clauses), decomposed into sequenced slices. The only implementable artifact for the first increment is the separate specification `vertical-slice-1-observe-mode-tracer.md`.

---

## Problem Statement

Enterprise platform and governance teams running GitHub Enterprise Server cannot answer, with evidence, the questions their security and audit functions keep asking: *Which repositories comply with our governance policies? Which intended controls are actually applied? Who accepted which risk, and until when? What would remediation change?* Configuration is spread across thousands of brownfield repositories, checking is manual and unrepeatable, and results cannot be traced to the exact policy version, observed state, and time they were true.

The project has a complete, accepted architecture (Architecture Baseline v1, ADRs 0001–0014) — but it is unvalidated by working software. Until the architecture runs end to end, it is a set of promises: the staged pipeline, the closed outcome sets, the compliance-versus-coverage split, the evidence model, and the dry-run planning model have never been exercised together.

## Phase Goal

A **read-only governance engine** proven against a **synthetic GHES estate** (no real GHES, no writes anywhere), demonstrating every ADR's POC boundary by the end of the phase: discovery and universal inventory; scope resolution under the three-result contract; composite policy evaluation through both evaluation strategies; explicit binding authority including shadow evaluation; capability-matrix compatibility with independent compliance and coverage reporting; the Governance Relief family with loud lifecycle behavior; append-only hashed evidence with manifest traceability; dry-run remediation planning; and reports derived exclusively from stored evidence.

The phase is delivered as **seven sequenced slices**. Each slice is a thin, demoable, independently testable increment that attaches to a seam the previous slices already exercise. Completion of the full sequence — not of any single slice — is what the Architecture Baseline v1 §17 trigger ("Vertical Slice 1 complete") refers to.

## Terminology

This plan governs the **Phase 2 Architecture Validation Sequence** — the canonical name for the full seven-slice read-only architecture-validation scope. The current implementation slice is **Vertical Slice 1 — Observe-Mode Tracer** (Slice 1 of 7), specified separately in `vertical-slice-1-observe-mode-tracer.md`.

The two names exist because both scopes were previously called "Vertical Slice 1". Architecture Baseline v1 predates the split, is immutable, and is not edited: where it says "Vertical Slice 1" (§10 scope, §17 next-baseline trigger), read **Phase 2 Architecture Validation Sequence**. Where this plan and its slice specifications say "Vertical Slice 1", they mean the Observe-Mode Tracer alone. This is a naming reconciliation only — no architectural decision changed, no ADR is affected, and the authority of Baseline v1 is undisturbed. `STATUS.md` records the same mapping.

## Slice Sequence

| # | Slice | Delivers | Attaches at | Prerequisites |
|---|---|---|---|---|
| 1 | **Observe-Mode Tracer** (spec: `vertical-slice-1-observe-mode-tracer.md`) | One complete execution path: synthetic estate → inventory → scope resolution → single authoritative binding → composite policy → Predicate Evaluation via strategy dispatch → findings → compliance + coverage aggregation → hashed evidence + manifest + status → derived reports | — (establishes both seams) | none |
| 2 | Desired-State Evaluation | `DesiredStateEvaluation` strategy, Comparison Profiles, one synthetic centrally managed artifact, unknown-field behavior | Strategy-dispatch registry (second registered pair) | 1 |
| 3 | Capability Matrix & Coverage Reasons | Versioned matrix, explicit selection with no silent fallback, `PlatformCapabilityUnavailable`, `CapabilityGap` findings, newer-than-validated GHES handling | The per-requirement applicability check | 1 (independent of 2) |
| 4 | Governance Relief & Lifecycle | Exceptions, exclusions, mandatory-expiry validation, Expiring threshold, loud lapse finding (first cross-execution read), `GovernanceExclusion` coverage reason | The `Governance Interpretation` field already on every finding | 1 |
| 5 | Shadow Bindings & Version Rollout | Independent shadow evaluation, role-caps-mode, side-by-side version-rollout comparison, shadow relief application | Authority selection (evaluate non-authoritative matches instead of ignoring them) | 1 (relief aspects require 4) |
| 6 | Dry-run Remediation Planning | Plan mode, immutable plan schema, content hashes, reversibility classes, mandatory expiry, simulated change budgets, Simulated Plans for shadow bindings | Downstream consumer of findings — purely additive | 1 (Simulated Plans require 5) |
| 7 | Cross-Execution Operations | Tuple-level supersession within declared scope, staleness/freshness semantics beyond age display, lock queueing of overlapping executions | Per-execution evidence-store layout established in Slice 1 | 1 |

Ordering within the sequence is adjustable where prerequisites allow (2 and 3 are independent of each other); the tracer is fixed first.

## Recorded Decisions

1. **ADR-0012 sequencing note.** ADR-0012's POC boundary names both `PredicateEvaluation` and `DesiredStateEvaluation`. Deferring the second strategy to Slice 2 is a *sequencing decision within the phase*, not an architecture change: the strategy-dispatch contract ADR-0012 mandates is fully present from Slice 1, and the second strategy lands in the same registry. No ADR amendment is required or implied.
2. **Baseline v2 trigger.** Architecture Baseline v1 §17 fires on "Vertical Slice 1 complete." That trigger is hereby pinned to **completion of the full Phase 2 Architecture Validation Sequence** — implementation validates the architecture only when every ADR's POC boundary has run. It does **not** fire on completion of Vertical Slice 1 — Observe-Mode Tracer (see Terminology).
3. **Full schemas, degenerate values.** All engine-owned closed sets and the complete finding/evidence schemas ship in Slice 1, populated with degenerate values where the producing capability is deferred (Governance Interpretation always `None`; Coverage Reasons `CapabilityGap`/`GovernanceExclusion` unreachable; plan references absent). Later slices populate fields; they never migrate schemas. (ADR-0006 explicitly permits relief to be "modeled in the schema without being fully implemented.")
4. **Seams are fixed for the phase.** Two public seams only — the Execution boundary and Report Derivation (ADR-0009 separation) — established in Slice 1 and reused by every later slice. No slice may introduce a lower public seam.
5. **The engine refuses desired state it cannot faithfully execute.** Before discovery or evaluation begins, the engine validates that every desired-state artifact and every activated semantic feature in the bundle is supported by the running engine release. If any artifact type, schema version, mode, role, or referenced capability cannot be faithfully interpreted, the execution fails before evaluation, emits configuration evidence identifying the unsupported content, and produces no authoritative compliance or coverage results. The rule is whole-bundle: unsupported content is rejected **even when it appears unreferenced**, because the engine cannot reliably prove content irrelevant without understanding its semantics. Silent ignoring or downgrading would infer intent and violate the explicit-intent principle. Accepted consequence: fixture bundles for later slices cannot be run against earlier-slice engines.

## Phase Capability Inventory

The user stories below are preserved verbatim from the original specification draft, each tagged with the slice that delivers it. Together they define phase completion.

**Discovery & Inventory**

1. `[Slice 1]` As a platform engineer, I want every discovered repository entered into the Inventory unconditionally, so that governance visibility never depends on policy correctness.
2. `[Slice 1]` As a compliance auditor, I want the Execution to account for repositories that were discovered but not evaluated (with reasons), so that completeness is verifiable rather than assumed.
3. `[Slice 1]` As a platform engineer, I want discovery to run against a synthetic GHES estate fixture (enterprise → organizations → repositories with settings and a declared GHES version), so that the pipeline is proven without touching a production system.

**Scope Resolution**

4. `[Slice 1]` As a governance policy author, I want to scope a policy using deterministic repository attributes (organization, repository name, visibility, archived state, fork status), so that applicability is predictable and explainable.
5. `[Slice 1]` As a governance policy author, I want scope expressions composed from attribute conditions with all/any/not combinators, so that I can target realistic estates without enumerating repositories.
6. `[Slice 1]` As a compliance auditor, I want evidence explaining how each repository's applicability was determined — provider name and version, configuration version, requested attribute, result category, returned value, timestamp — so that every scope decision is reproducible.
7. `[Slice 1]` As a platform engineer, I want an attribute the provider cannot determine to yield `Unknown` applicability rather than being treated as absent, so that uncertainty never silently changes a governance result.
8. `[Slice 1]` As a governance engine developer, I want the attribute provider to distinguish Value Present, Value Absent, and Cannot Determine, so that the three-result contract holds end to end.

**Bindings, Modes, and Authority**

9. `[Slice 1]` As a governance policy author, I want to activate a policy through a Policy Binding (policy version × scope expression × enforcement mode × evaluation role × effective period), so that rollout state is expressed without cloning policies.
10. `[Slice 6]` As a governance policy author, I want the same policy version bound simultaneously in different modes across different scopes, so that canary, pilot, and estate-wide rollout stages coexist.
11. `[Slice 1]` As a governance operator, I want an Observe-mode binding to produce findings and evidence but no remediation plan, so that observation is safe by construction.
12. `[Slice 6]` As a governance operator, I want a Plan-mode authoritative binding to produce an explainable dry-run Remediation Plan, so that I can see exactly what enforcement would do before ever enabling it.
13. `[Slice 1]` As a governance operator, I want a future-dated binding to become active only when an execution's fixed Evaluation Timestamp falls within its half-open effective period, so that activation never silently depends on merge timing.
14. `[Slice 1]` As a compliance auditor, I want every finding to record the binding version, mode, role, effective period, and the Evaluation Timestamp used, so that evidence distinguishes observed, planned, excepted, and excluded results.
15. `[Slice 1]` As a governance operator, I want zero active authoritative bindings for a (policy, repository) pair to produce no official compliance interpretation — neither `Unknown` nor `NotApplicable` — while remaining visible in inventory and binding provenance, so that a normal rollout state is never miscounted as a result.
16. `[Slice 1]` As a governance operator, I want more than one active authoritative binding for a pair to yield official Policy Outcome and Coverage State of `Unknown`, no plan, and a high-visibility governance-configuration finding identifying every conflicting binding and any requirement-set divergence — with each conflicting binding still evaluated as explanatory evidence but never as an official outcome, and no requirement set synthesized across their policy versions (ADR-0013) — so that ambiguity about authority never resolves silently.
17. `[Slice 5]` As a governance policy author, I want shadow bindings evaluated independently and their results clearly separated from the authoritative result, so that pilot analysis never contaminates the official answer.
18. `[Slice 6, requires 5]` As a governance policy author, I want a shadow binding in Plan mode to produce a Simulated Plan — labeled as shadow, never executable — so that prospective impact is visible without creating executable artifacts.
19. `[Slice 5]` As a governance operator, I want a shadow binding declared in Enforce mode to behave as simulation only, so that the evaluation role always caps the mode.
20. `[Slice 5]` As a governance policy author, I want v1 authoritative estate-wide and v2 shadow in a pilot scope reported side by side per requirement, so that version rollout decisions are informed by explicit comparison, never a flattened result.

**Requirements & Evaluation**

21. `[Slice 1]` As a governance policy author, I want a policy to be a composite of individually addressable requirements with stable identifiers, so that findings, relief, and comparisons operate per requirement, never only per policy.
22. `[Slice 1]` As a governance policy author, I want each requirement to declare exactly one evaluation strategy (identifier + version), so that how a technical outcome is computed is explicit and versioned.
23. `[Slice 1]` As a governance policy author, I want Predicate Evaluation to determine compliance by evaluating declared conditions against observed state, so that minimum-control policies work in a brownfield estate.
24. `[Slice 2]` As a governance policy author, I want Desired-State Evaluation to compare Normalized Observed State against a version-controlled centrally managed artifact under a Comparison Profile, so that exact-configuration controls use the same pipeline as everything else.
25. `[Slice 2]` As a governance engine developer, I want unknown fields during desired-state comparison processed per the active Comparison Profile — and `Unknown` where no rule exists — so that uncertainty neither grants relief nor manufactures findings.
26. `[Slice 1]` As a governance operator, I want a requirement declaring an unknown strategy identifier or unsupported strategy version to produce Technical Outcome `Unknown` plus a high-visibility configuration finding identifying requested and available versions, so that the engine never silently substitutes or skips.
27. `[Slice 1]` As a compliance auditor, I want Technical Outcome and Governance Interpretation recorded as separate facts on every finding, so that governance artifacts can never rewrite technical truth.
28. `[Slice 1]` As a governance operator, I want policy outcomes derived solely by the deterministic engine-owned aggregation (any `NonCompliant` → `NonCompliant`; else any `Unknown` → `Unknown`; else any `Excepted` → `CompliantWithExceptions`; else `Compliant`), so that no exception ever conceals another requirement's noncompliance.
29. `[Slice 1; PlatformCapabilityUnavailable reachable in Slice 3]` As a governance policy author, I want per-requirement applicability with closed `NotApplicable` reasons (RepositoryCharacteristic, PolicyPrecondition, PlatformCapabilityUnavailable), so that logical inapplicability is explained and never harms aggregation.

**Capability Matrix & Coverage**

30. `[Slice 3]` As a governance operator, I want compatibility resolved against a versioned Capability Matrix — never runtime probing — so that capability answers are reviewable, trusted inputs.
31. `[Slice 3]` As a security lead, I want a requirement whose capability the validated GHES version lacks reported as `NotApplicable / PlatformCapabilityUnavailable`, uncovered with Coverage Reason `CapabilityGap`, and accompanied by a distinct capability-gap finding, so that suppressed security coverage is explicit and auditable.
32. `[Slice 3]` As a governance operator, I want an undeterminable capability (missing matrix entry, undetectable GHES version) to yield `Unknown` — never "unsupported" — so that failure to determine compatibility is never treated as lack of capability.
33. `[Slice 3]` As a governance operator, I want a GHES version newer than the validated matrix to make compatibility-dependent evaluations `Unknown` and be identified in reporting, so that newer platforms are never assumed backward compatible.
34. `[Slice 3]` As a governance operator, I want an explicitly selected matrix that is missing or malformed to produce `Unknown` for affected evaluations rather than a silent fallback to the bundled default, so that desired-state selection authority is respected.
35. `[Slice 1 structure; reasons complete in Slices 3–4]` As a compliance auditor, I want Coverage State (Covered / PartiallyCovered / Unknown) with per-requirement Coverage Reasons reported independently of compliance, so that "compliant but under-covered" is never presented as fully green.

**Governance Relief**

36. `[Slice 4]` As a governance policy author, I want a Governance Exception applied after evaluation to keep the technical result visible while changing only the interpretation (`NonCompliant` / `Exception` / `Excepted`, citing the artifact), so that accepted risk is visible risk.
37. `[Slice 4]` As a governance policy author, I want a Governance Exclusion applied before evaluation to yield `NotEvaluated` / `Exclusion` / `Excluded` and Coverage Reason `GovernanceExclusion`, so that "we chose not to yet" is never conflated with "the platform can't."
38. `[Slice 4]` As a governance operator, I want relief artifacts without an expiry rejected as invalid desired state, so that open-ended risk acceptance is structurally impossible.
39. `[Slice 4]` As a security lead, I want a relief artifact that was active in the previous execution and is expired in the current one to produce a distinct lapse finding, so that risk lapsing back into unaccepted state is loud, never a silent recolor.
40. `[Slice 4]` As a governance operator, I want the Expiring state derived ahead of expiry using a governance-wide default threshold with optional per-artifact override, so that relief can be renewed proactively.
41. `[Slice 4]` As a governance operator, I want an exception against an `Unknown` technical result refused, and a relief artifact whose own scope resolution is `Unknown` left unapplied with loud evidence on the artifact, so that uncertainty never grants privilege.
42. `[Slice 4; shadow aspects require 5]` As a compliance auditor, I want shadow evaluations to apply the same active relief artifacts as authoritative ones (recording raw result, interpretation, and artifact reference), so that shadow comparisons measure policy differences, not interpretation drift.

**Evidence & Execution**

43. `[Slice 1]` As a compliance auditor, I want every execution to produce append-only, schema-versioned, content-hashed evidence items and an Execution Manifest listing each item with its hash, so that tampering is detectable without infrastructure.
44. `[Slice 1]` As a governance operator, I want authoritative evidence identical at every operational log level, so that a cost-saving logging change can never weaken auditability.
45. `[Slice 1]` As a compliance auditor, I want each evaluation's Replay Input Set (policy, binding, provider, and matrix versions; normalized observed state; active relief; evaluation timestamp; engine version) recorded, so that any result can be reproduced deterministically.
46. `[Slice 1 declares scope; supersession in Slice 7]` As a governance operator, I want every execution to declare its Evaluation Scope as part of execution identity, and authoritative results to supersede prior results only per (repository, policy, requirement) tuple within that scope, so that narrow executions never silently invalidate estate-wide answers.
47. `[Slice 1 rejects; Slice 7 queues]` As a governance operator, I want a single-execution lock so that a second overlapping execution is rejected or queued, never interleaved.
48. `[Slice 1]` As a governance operator, I want a closed Execution Status (Complete / CompleteWithGaps / Failed) with discovered/evaluated/Unknown accounting, so that one unavailable repository never suppresses evidence for the rest.
49. `[Slice 1]` As a compliance auditor, I want every evidence and log record to carry a sensitivity classification (all Public in this synthetic slice), so that the redaction model exists before real data does.
50. `[Slice 1]` As a governance operator, I want every reported result to carry its evaluation timestamp, execution identifier, and result age, so that an old compliant answer is never mistaken for a recent one.
51. `[Slice 1]` As a governance operator, I want observed state stored as Normalized Observed State (observed vs expected, smallest decision-relevant form), so that evidence stays minimal but sufficient.

**Dry-run Remediation Planning**

52. `[Slice 6]` As a governance operator, I want each authoritative Plan-mode noncompliance to yield an immutable Remediation Plan — identifier, schema version, content hash, source execution, observed-state digest, deterministic operation order, preconditions, postconditions, per-operation reversibility class, impact, verification, rollback procedure, creation time, mandatory expiration — so that what enforcement would do is fully specified and auditable before write authority exists anywhere.
53. `[Slice 6]` As a security lead, I want the plan content hash to cover every authorization-relevant field, so that approval of one plan can never be approval of a materially different plan.
54. `[All slices]` As a governance operator, I want the engine to perform no writes whatsoever — even for a binding declared in Enforce mode — so that the slice is safe to run anywhere; Enforce is modeled as eligibility only.
55. `[Slice 6]` As a governance engine developer, I want the configured change budget recorded in plan and execution evidence (simulated, never consumed), so that the constraint model is exercised before the write path exists.

**Derived Reports**

56. `[Slice 1]` As a governance operator, I want reports derived exclusively from stored evidence — regenerable at any time without rerunning an execution — so that reports are disposable and evidence remains the single source of truth.
57. `[Slice 1]` As a compliance auditor, I want every report claim to cite the execution manifests (and thereby hashed evidence items) it derives from, so that an untraceable report is recognizably invalid.
58. `[Slice 1]` As a governance operator, I want reports to show Compliance and Coverage as separate dimensions and to flag results stale beyond configurable thresholds, so that summary reading cannot flatten the two facts the architecture keeps apart.
59. `[Slice 1]` As a compliance auditor, I want both a machine-readable report and a human-readable summary, so that operators triage and auditors verify from the same evidence.
60. `[Slice 1]` As a governance operator, I want repositories with zero authoritative bindings surfaced in reporting as their own derived category, so that ungoverned pairs are visible without inventing an outcome for them.

## Phase-Wide Implementation Decisions

These hold across every slice; the owning slice makes each fully real.

- **Stack**: Python (3.12+). Library-first design with a thin CLI. No network access anywhere in the phase.
- **Primary seam — the Execution boundary**: (approved desired-state bundle, synthetic observed-state fixture, declared Evaluation Scope, Evaluation Timestamp, engine configuration) → evidence items + Execution Manifest + Execution Status. Timestamp and execution identifier are injectable; the engine never reads a wall clock during evaluation.
- **Secondary seam — Report Derivation**: (evidence store, report configuration) → Derived Reports citing manifests.
- **Desired-state artifact schemas**: YAML, one artifact per file, each carrying schema version, stable identifier, artifact version; bundle directory tree stands in for the Governance Repository at pinned versions; "approved" is modeled as "present in the bundle" (ADR-0002 keeps the process out of band). Validation via published JSON Schema; invalid desired state fails an execution loudly before evaluation.
- **Scope-expression syntax (v1)**: declarative YAML; attribute conditions over the closed v1 attribute set (`organization`, `repository_name`, `visibility`, `archived`, `fork`); operators `equals`, `not_equals`, `in`, `matches` (anchored regex); combinators `all` / `any` / `not`. The engine owns the language.
- **Evidence**: canonical (sorted-key, stable-serialization) JSON; SHA-256 content hashes; per-execution directories physically separate from desired state and operational logs; manifest as tamper-evidence root; corrections are new items referencing originals.
- **Closed sets live in one place**: engine-owned enumerations exactly as named in `CONTEXT.md`; no artifact may extend them.
- **Aggregation** (compliance per ADR-0006, coverage per ADR-0007): engine-owned pure functions; nothing else may compute policy-level outcomes.
- **Expiring threshold** (Slice 4): governance-wide default in desired-state configuration, optional per-artifact override; effective value and source recorded in evidence.
- **Retention**: retention metadata configurable per data class and recorded; no automatic deletion or lifecycle transitions anywhere in the phase.
- **Reporting personas**: governance operator (triage) and compliance auditor (verification); one machine-readable JSON report plus one human-readable summary serve both.
- **Strategy versioning**: the engine release declares supported (strategy identifier, version) pairs; requirements select pairs; unknown/unsupported selections produce the ADR-0012 unknown-strategy behavior.
- **Synthetic estate fixture**: YAML/JSON document set — enterprise, organizations, repositories with evaluated settings, declared synthetic GHES version — including deliberately undeterminable attributes and capabilities.

## Phase-Wide Testing Doctrine

Tests attach only at the two seams; no test imports internal modules. Scenario fixtures are the test vocabulary; each ADR's POC clause becomes at least one scenario in the slice that delivers it. Standing invariant tests: determinism/replay (byte-identical evidence), tamper detection via manifest verification, report-to-manifest traceability, uncertainty-never-grants-privilege, technical-outcomes-never-altered-by-relief, role-caps-mode, and the absence of any write path.

## Out of Scope (entire phase)

- Any write to GHES or any external system; actual Enforce execution, verification, rollback, or change-budget consumption
- Real GHES connectivity, authentication, rate limiting, or API clients
- Plan Approval processing and approval revocation
- The emergency suspension path (deferred architectural decision) and Standing Remediation Authority
- Event-driven/reactive execution, scheduled reconciliation, concurrent non-overlapping executions
- Additional attribute providers (topics, custom properties, teams, CMDB, ServiceNow) and any plug-in loading framework
- Runtime capability probing; the control catalog; the scope-diff Requirement (ADR-0008)
- Evidence hardening (signing, WORM/object lock, external anchoring), centralized log aggregation, retention automation/disposal execution
- Dashboards or notification outputs; report delivery mechanisms
- Production packaging, deployment, AWS infrastructure, high availability, performance work

## Notes

- **STATUS.md discrepancy** — *resolved 2026-07-15*: STATUS.md previously carried a single "Current Vertical Slice" list that conflated the two scopes (it omitted Desired-State Evaluation, which ADR-0012's POC boundary includes, while listing Dry-run Remediation Planning, which Slice 6 delivers). STATUS.md now names both scopes per Terminology: the sequence carries the full capability set — Desired-State Evaluation included, in Slice 2 (see Recorded Decision 1) — and the Observe-Mode Tracer carries only its own. No ADR outranking was required; the lists had different subjects.
- **Terminology**: implementation and tests use `CONTEXT.md` vocabulary verbatim, including its *Avoid* list (no "drift" as a concept, no "waiver", no "accepted deviation").
- Slice specifications after Slice 1 are written when their turn comes (each via the normal spec process, referencing this plan); they are not pre-authored here and nothing in this plan is an agent-ready ticket.
