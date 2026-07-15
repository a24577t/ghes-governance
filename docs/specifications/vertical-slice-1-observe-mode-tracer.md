# Vertical Slice 1 — Observe-Mode Tracer

| Field | Value |
|---|---|
| Type | Specification (candidate `ready-for-agent` ticket once reviewed) |
| Status | Draft for review — **not published, not yet an issue** |
| Date | 2026-07-14 |
| Parent | `phase-2-architecture-validation-plan.md` (Slice 1 of 7) |
| Authoritative architecture | Architecture Baseline v1, ADRs 0001–0012, `CONTEXT.md`, Domain Model |

## Problem Statement

The accepted architecture (Baseline v1, ADRs 0001–0012) is unvalidated by working software. Every architectural claim — the staged gated pipeline, the fail-loud Unknown propagation, explicit binding authority, engine-owned closed sets and aggregation, authoritative append-only evidence, derived reports — exists only on paper. A governance operator cannot yet run anything, and no schema, seam, or invariant has survived contact with an implementation.

## Solution

The thinnest complete execution path through every architectural layer — a **read-only, Observe-mode tracer** a governance operator runs manually against a synthetic GHES estate:

1. Load and schema-validate an approved desired-state bundle at pinned versions (policies, scope expressions, policy bindings, engine/desired-state configuration).
2. Discover the synthetic estate; enter every repository into the Inventory unconditionally.
3. Resolve scope through the GitHub-native attribute provider under the three-result contract; `CannotDetermine` propagates to `Unknown` applicability.
4. Select the authoritative binding per (policy, repository) — zero, one, or conflict — refusing interpretation on ambiguity.
5. Evaluate one composite policy per requirement through strategy dispatch (`PredicateEvaluation` v1 registered; unknown-strategy selections fail loud into `Unknown` plus a configuration finding).
6. Produce per-requirement findings carrying Technical Outcome, Governance Interpretation (always `None` in this slice), and Requirement Outcome; aggregate Policy Outcome and Coverage State with the engine-owned rules.
7. Write append-only, content-hashed, schema-versioned evidence, an Execution Manifest, and a closed Execution Status with completeness accounting.
8. Separately — from stored evidence only — derive one machine-readable report and one human-readable summary citing the manifests they derive from.

The demo: run the CLI on a fixture, show a noncompliant finding with its full explanation chain, show Unknown propagating end to end, regenerate the report from evidence alone, and show tampering detected by manifest verification.

## User Stories

**Discovery & Inventory**

1. As a platform engineer, I want every discovered repository entered into the Inventory unconditionally, so that governance visibility never depends on policy correctness.
2. As a compliance auditor, I want the Execution to account for repositories that were discovered but not evaluated (with reasons), so that completeness is verifiable rather than assumed.
3. As a platform engineer, I want discovery to run against a synthetic GHES estate fixture (enterprise → organizations → repositories with settings and a declared GHES version), so that the pipeline is proven without touching a production system.

**Scope Resolution**

4. As a governance policy author, I want to scope a policy using deterministic repository attributes (organization, repository name, visibility, archived state, fork status), so that applicability is predictable and explainable.
5. As a governance policy author, I want scope expressions composed from attribute conditions with all/any/not combinators, so that I can target realistic estates without enumerating repositories.
6. As a compliance auditor, I want evidence explaining how each repository's applicability was determined — provider name and version, configuration version, requested attribute, result category, returned value, timestamp — so that every scope decision is reproducible.
7. As a platform engineer, I want an attribute the provider cannot determine to yield `Unknown` applicability rather than being treated as absent, so that uncertainty never silently changes a governance result.
8. As a governance engine developer, I want the attribute provider to distinguish Value Present, Value Absent, and Cannot Determine, so that the three-result contract holds end to end.

**Bindings & Authority**

9. As a governance policy author, I want to activate a policy through a Policy Binding (policy version × scope expression × enforcement mode × evaluation role × effective period), so that rollout state is expressed without cloning policies.
10. As a governance operator, I want an Observe-mode binding to produce findings and evidence but no remediation plan, so that observation is safe by construction.
11. As a governance operator, I want a future-dated binding to become active only when an execution's fixed Evaluation Timestamp falls within its half-open effective period, so that activation never silently depends on merge timing.
12. As a compliance auditor, I want every finding to record the binding version, mode, role, effective period, and the Evaluation Timestamp used, so that evidence is self-explanatory.
13. As a governance operator, I want zero active authoritative bindings for a (policy, repository) pair to produce no official compliance interpretation — neither `Unknown` nor `NotApplicable` — while remaining visible in inventory and binding provenance, so that a normal rollout state is never miscounted as a result.
14. As a governance operator, I want more than one active authoritative binding for a pair to yield `Unknown` and a high-visibility governance-configuration finding identifying every conflicting binding, so that ambiguity about authority never resolves silently.

**Requirements & Evaluation**

15. As a governance policy author, I want a policy to be a composite of individually addressable requirements with stable identifiers, so that findings operate per requirement, never only per policy.
16. As a governance policy author, I want each requirement to declare exactly one evaluation strategy (identifier + version), so that how a technical outcome is computed is explicit and versioned.
17. As a governance policy author, I want Predicate Evaluation to determine compliance by evaluating declared conditions against observed state, so that minimum-control policies work in a brownfield estate.
18. As a governance operator, I want a requirement declaring an unknown strategy identifier or unsupported strategy version to produce Technical Outcome `Unknown` plus a high-visibility configuration finding identifying requested and available versions, so that the engine never silently substitutes or skips.
19. As a compliance auditor, I want Technical Outcome and Governance Interpretation recorded as separate facts on every finding (Interpretation is always `None` in this slice), so that the seam where Governance Relief later attaches exists from the first execution.
20. As a governance operator, I want policy outcomes derived solely by the deterministic engine-owned aggregation (any `NonCompliant` → `NonCompliant`; else any `Unknown` → `Unknown`; else any `Excepted` → `CompliantWithExceptions`; else `Compliant`), so that no other mechanism can compute or override them.
21. As a governance policy author, I want per-requirement applicability with closed `NotApplicable` reasons (`RepositoryCharacteristic` and `PolicyPrecondition` reachable in this slice), so that logical inapplicability is explained and never harms aggregation.
22. As a compliance auditor, I want Coverage State computed by the engine-owned rule and reported independently of compliance (reachable values in this slice: `Covered`, `Unknown`), so that the two dimensions are never flattened.

**Evidence & Execution**

23. As a compliance auditor, I want every execution to produce append-only, schema-versioned, content-hashed evidence items and an Execution Manifest listing each item with its hash, so that tampering is detectable without infrastructure.
24. As a governance operator, I want authoritative evidence identical at every operational log level, so that a cost-saving logging change can never weaken auditability.
25. As a compliance auditor, I want each evaluation's Replay Input Set (policy, binding, and provider versions; normalized observed state; evaluation timestamp; engine version) recorded, so that any result can be reproduced deterministically.
26. As a governance operator, I want every execution to declare its Evaluation Scope as part of execution identity, recorded in evidence, so that later slices can build tuple-level supersession on it.
27. As a governance operator, I want a single-execution lock so that a second concurrent execution is rejected, never interleaved.
28. As a governance operator, I want a closed Execution Status (`Complete` / `CompleteWithGaps` / `Failed`) with discovered/evaluated/Unknown accounting, so that one undeterminable repository never suppresses evidence for the rest.
29. As a compliance auditor, I want every evidence and log record to carry a sensitivity classification (constant `Public` in this synthetic slice), so that the redaction model exists before real data does.
30. As a governance operator, I want observed state stored as Normalized Observed State (observed vs expected, smallest decision-relevant form), so that evidence stays minimal but sufficient.

**Derived Reports**

31. As a governance operator, I want reports derived exclusively from stored evidence — regenerable at any time without rerunning an execution — so that reports are disposable and evidence remains the single source of truth.
32. As a compliance auditor, I want every report claim to cite the execution manifests (and thereby hashed evidence items) it derives from, and report derivation to verify item hashes against the manifest, so that an untraceable or tampered source is detected rather than summarized.
33. As a governance operator, I want reports to show Compliance and Coverage as separate dimensions and to display each result's evaluation timestamp, execution identifier, and result age, flagging results older than a configurable staleness threshold, so that an old answer is never mistaken for a recent one.
34. As a compliance auditor, I want both a machine-readable JSON report and a human-readable summary, so that operators triage and auditors verify from the same evidence.
35. As a governance operator, I want (policy, repository) pairs with zero authoritative bindings surfaced in reporting as their own derived category, so that ungoverned pairs are visible without inventing an outcome for them.

## Implementation Decisions

- **Stack**: Python 3.12+, library-first, thin CLI with two commands mirroring the two seams: run an execution; derive reports. No network access; the engine writes only to its evidence, log, and report directories.
- **Primary seam — the Execution boundary**: one entry point taking (desired-state bundle path, synthetic estate fixture path, declared Evaluation Scope, Evaluation Timestamp, execution identifier, engine configuration) and returning/writing evidence items, the Execution Manifest, and the Execution Status. Timestamp and execution identifier are injected; the engine never reads a wall clock during evaluation.
- **Secondary seam — Report Derivation**: takes (evidence store path, report configuration incl. staleness threshold) and produces the two Derived Reports. It verifies every cited item's hash against its manifest and fails loudly on mismatch — tamper detection is exercised through this seam. No other public seams exist.
- **Full closed sets, degenerate values** (phase Recorded Decision 3): all `CONTEXT.md` closed sets ship complete in this slice — Enforcement Mode, Evaluation Role, Applicability Outcome, Provider Result, Technical Outcome, Governance Interpretation, Requirement Outcome, Policy Outcome, Coverage State, Coverage Reason, NotApplicable Reason, Execution Status, severity levels — and the finding/evidence schemas carry every field, even where only degenerate values are reachable (Interpretation `None`; Coverage Reason only `Unknown`; Requirement Outcome never `Excepted`/`Excluded`). Later slices populate values, never migrate schemas.
- **Aggregation functions complete, branches dormant**: compliance and coverage aggregation implement the full ADR-0006/0007 precedence including branches unreachable in this slice (`CompliantWithExceptions`, `PartiallyCovered`).
- **The engine refuses desired state it cannot faithfully execute** (phase Recorded Decision 5): before discovery or evaluation begins, the bundle loader validates every artifact and every activated semantic feature against this release's capabilities. Bindings in `Plan`/`Enforce` mode, `shadow` evaluation roles, relief artifacts, comparison profiles, capability-matrix selections, or unsupported schema versions cause a loud validation failure (Execution Status `Failed`, configuration evidence identifying the unsupported content, no authoritative compliance or coverage results) — **whole-bundle, even when the unsupported content appears unreferenced**, because the engine cannot reliably prove content irrelevant without understanding its semantics. Silent ignoring or downgrading would infer intent.
- **Strategy dispatch**: an internal registry keyed by (strategy identifier, strategy version); this release registers exactly `PredicateEvaluation` 1.0. Unknown selections produce the ADR-0012 behavior (Technical Outcome `Unknown`, configuration finding naming requested and available pairs). The registry is the seam Slice 2 populates.
- **Predicate definitions (v1)**: declarative conditions over the synthetic repository settings — same operator set as scope expressions (`equals`, `not_equals`, `in`, `matches`) plus numeric comparisons (`at_least`, `at_most`), composed with `all`/`any`/`not`. Evaluation over an undeterminable setting yields `Unknown`, never a default.
- **Scope-expression syntax (v1)**: declarative YAML; closed attribute set (`organization`, `repository_name`, `visibility`, `archived`, `fork`); operators `equals`, `not_equals`, `in`, `matches` (anchored regex); combinators `all`/`any`/`not`.
- **Authority selection**: per (policy identifier, repository), select active authoritative bindings at the fixed timestamp — zero → no official interpretation (pair listed in a distinct evidence record and report category); one → proceed; more than one → Requirement Outcomes `Unknown`, high-visibility governance-configuration finding enumerating all conflicting bindings. No shadow evaluation occurs in this slice (shadow-role bindings are rejected at validation per the decision above).
- **Evidence store**: per-execution directory, physically separate from desired state, operational logs, and reports; canonical (sorted-key, stable-serialization, UTF-8) JSON so content hashes (SHA-256) are byte-deterministic; every item carries schema version and sensitivity classification; the manifest lists every item with its hash and is written last; corrections are new items referencing originals — nothing is ever rewritten.
- **Operational logs**: closed severity model per ADR-0009, configurable level, separate directory; evidence content provably identical across levels.
- **Reports**: one canonical JSON report and one Markdown summary; both cite manifest and item hashes per claim; both show Compliance and Coverage side by side, result age, staleness flags, completeness accounting, and the ungoverned-pairs category.
- **Synthetic estate fixture**: YAML/JSON documents — enterprise, organizations, repositories with the settings the tracer's policies evaluate, a declared synthetic GHES version (recorded in evidence, not consulted — no matrix in this slice), and a fixture mechanism for marking an attribute or setting undeterminable to exercise `CannotDetermine`.
- **Reference desired-state bundle**: one composite policy with at least three requirements (one `Compliant`, one `NonCompliant`, one `Unknown`-producing per ADR-0006's slice clause), one scope expression, one authoritative Observe binding — plus variant bundles for the zero-authoritative, conflicting-authoritative, unknown-strategy, and invalid-bundle scenarios.

## Acceptance Criteria

1. **Happy path**: running an execution on the reference bundle and estate yields Execution Status `Complete`, per-requirement findings with correct Technical/Interpretation/Requirement outcomes, the correct Policy Outcome per the aggregation rule, Coverage State `Covered` for evaluated requirements, a manifest listing every evidence item with a verifying hash, and both reports.
2. **Determinism/replay**: two executions with the identical Replay Input Set (same bundle, fixture, scope, timestamp, execution identifier, engine version) produce byte-identical evidence, including hashes and manifest.
3. **Unknown propagation**: a fixture attribute marked undeterminable yields Provider Result `CannotDetermine` → Applicability `Unknown` → Requirement Outcome `Unknown` → Policy Outcome `Unknown` → Coverage State `Unknown`, all visible in evidence, with the execution completing (status reflects gaps in accounting) and other repositories unaffected.
4. **Zero authoritative bindings**: the pair produces no Policy Outcome of any kind; it appears in the evidence's binding-provenance record and in the reports' ungoverned category.
5. **Authoritative conflict**: two overlapping active authoritative bindings yield Requirement Outcomes `Unknown`, a high-visibility governance-configuration finding enumerating both bindings, and no silent winner.
6. **Unknown strategy**: a requirement declaring an unregistered (strategy, version) pair yields Technical Outcome `Unknown` and a configuration finding naming requested and available pairs; other requirements in the policy evaluate normally.
7. **Half-open effective periods**: with evaluation timestamp exactly at a binding's `effective_start` the binding is active; exactly at `effective_end` it is inactive; before `effective_start` (future-dated) it is inactive.
8. **Aggregation precedence**: fixtures produce each reachable Policy Outcome (`Compliant`, `NonCompliant`, `Unknown`) and demonstrate `NonCompliant` outranking `Unknown`; `NotApplicable` requirements (both reachable reasons) are aggregation-neutral.
9. **Evidence/log independence**: executions at `INFO` and `DEBUG` produce byte-identical evidence.
10. **Tamper detection**: mutating any stored evidence item causes report derivation to fail, identifying the item whose hash no longer matches the manifest.
11. **Report traceability & regeneration**: reports derived twice from the same evidence store are identical; every claim carries manifest/item citations; report derivation requires no execution.
12. **Fail-loud validation**: before discovery or evaluation begins, the engine validates that every desired-state artifact and every activated semantic feature in the bundle is supported by the running engine release. If any artifact type, schema version, mode, role, or referenced capability cannot be faithfully interpreted — including unsupported content that appears unreferenced — the execution fails before evaluation with Execution Status `Failed`, emits configuration evidence identifying the unsupported content, and produces no authoritative compliance or coverage results.
13. **Single-execution lock**: a second execution started while one is running is rejected with a clear error; no interleaved evidence is produced.
14. **Read-only guarantee**: the fixture and bundle directories are unmodified after any execution (verifiable by hashing them before and after); the engine writes only beneath its evidence, log, and report directories.

## Testing Decisions

- **Test only external behavior at the two seams.** A good test feeds a complete scenario (bundle + estate fixture + scope + timestamp + identifier) into the Execution seam and asserts on evidence, manifest, findings, outcomes, and status — or feeds an evidence store into the Report seam and asserts on report content, citations, and hash verification. No test imports internal modules (provider, dispatch, aggregation, scope evaluator); internal refactors must never break tests.
- **Scenario fixtures are the test vocabulary**; each acceptance criterion above maps to at least one fixture directory. Golden-evidence comparison is the primary assertion style, made viable by canonical serialization and injected timestamp/identifier.
- **Standing invariant tests**: determinism (AC 2), evidence/log independence (AC 9), tamper detection (AC 10), traceability (AC 11), read-only guarantee (AC 14), and uncertainty-never-grants-privilege (AC 3 — Unknown never becomes a compliant or noncompliant answer at any layer).
- **Prior art**: none — these are the repository's first tests and establish its conventions (pytest, fixture-directory pattern, golden evidence comparison).

## Test Scenarios

| # | Scenario | Exercises |
|---|---|---|
| S1 | Reference estate, reference bundle, happy path | AC 1, stories 1–6, 9–10, 12, 15–17, 19–23, 25–26, 28–31, 33–34 |
| S2 | Same inputs run twice | AC 2 |
| S3 | Repository with undeterminable attribute | AC 3, stories 7–8 |
| S4 | Repository matching no authoritative binding | AC 4, stories 13, 35 |
| S5 | Two overlapping authoritative bindings | AC 5, story 14 |
| S6 | Requirement declaring unknown strategy version | AC 6, story 18 |
| S7 | Future-dated binding; boundary timestamps at start and end | AC 7, story 11 |
| S8 | Policies engineered for each reachable aggregation outcome, incl. NotApplicable neutrality | AC 8, stories 20–21 |
| S9 | Same execution at INFO vs DEBUG log level | AC 9, story 24 |
| S10 | Evidence item mutated between execution and report derivation | AC 10, stories 23, 32 |
| S11 | Report derived twice; derivation with no prior execution in a fresh store | AC 11, stories 31–32 |
| S12 | Invalid bundle variants: malformed artifact; unsupported schema version; Plan-mode binding; shadow-role binding; relief artifact present; unsupported artifact present but unreferenced by any binding | AC 12 |
| S13 | Concurrent second execution | AC 13, story 27 |
| S14 | Before/after hash of fixture and bundle directories | AC 14 |

## Out of Scope (delivered by later slices — see the Phase 2 Architecture Validation Plan)

- Desired-State Evaluation, Comparison Profiles, centrally managed artifacts (Slice 2)
- Capability Matrix, `PlatformCapabilityUnavailable`, `CapabilityGap`, newer-than-validated GHES handling (Slice 3)
- Governance Relief in any form: exceptions, exclusions, expiry validation, Expiring threshold, lapse findings (Slice 4)
- Shadow bindings, role-caps-mode behavior, version-rollout comparison (Slice 5)
- Plan and Enforce modes, Remediation Plans, Simulated Plans, change budgets (Slice 6)
- Tuple-level supersession, staleness semantics beyond age display, lock queueing (Slice 7)
- Everything in the plan's phase-wide out-of-scope list (writes, real GHES, approvals, plug-ins, hardening, deployment)

## Further Notes

- **ADR-0012 sequencing**: deferring `DesiredStateEvaluation` to Slice 2 is a sequencing decision within the phase, not an architecture change — the dispatch contract ADR-0012 mandates is fully present here (phase Recorded Decision 1).
- **Architectural proof delivered**: this tracer validates the load-bearing skeleton of ADRs 0002–0006, 0009, 0010, and 0012 — the staged gated pipeline, the three-result contract and Unknown propagation, explicit authority with fail-loud ambiguity, engine-owned closed sets and aggregation, authoritative evidence with replay determinism, and derived-report traceability. Every deferred capability attaches to a field, branch, or registry this slice ships with a degenerate value.
- **Baseline v2** is triggered by completion of the full phase sequence, not this slice (phase Recorded Decision 2).
- **Terminology**: implementation and tests use `CONTEXT.md` vocabulary verbatim, including its *Avoid* list.
