# GHES Governance

A governance platform for GitHub Enterprise Server that evaluates repository, organization, and enterprise configuration against version-controlled policies — and, for explicitly selected controls, reconciles exact centrally managed configuration.

## Language

### Governance model

**Policy**:
A versioned, logical grouping of related Requirements under a stable identifier with purpose metadata. Not the smallest unit of evaluation, finding, or relief.
_Avoid_: rule, standard

**Requirement**:
An individually addressable control within a Policy: a stable identifier, a declared Evaluation Strategy, an evaluation definition, an evidence definition, and optional remediation guidance and compatibility prerequisites. The identifier survives policy versions while the meaning is unchanged and is never reused for a materially different control.

**Evaluation Strategy**:
The engine-owned method a Requirement declares for determining its Technical Outcome. Initial strategies: Predicate Evaluation and Desired-State Evaluation. Bindings, modes, outcomes, relief, evidence, and remediation are identical regardless of strategy.

**Predicate Evaluation**:
The Evaluation Strategy that determines compliance by evaluating conditions against observed state.

**Desired-State Evaluation**:
The Evaluation Strategy that determines compliance by comparing Normalized Observed State against a version-controlled desired artifact under a Comparison Profile.

**Comparison Profile**:
The versioned, trusted desired-state content governing a Desired-State Evaluation: compared, ignored, and server-managed fields; normalization, ordering, and default-value handling; unknown-field behavior. Where no rule exists, the comparison result is Unknown.

**Scope Expression**:
The versioned, declarative definition of which enterprises, organizations, or repositories a Policy applies to, written in the core engine's scope-expression language.
_Avoid_: policy scope

**Desired State**:
The Git-authoritative content: policies, scope expressions, policy bindings, governance relief artifacts, attribute-provider configuration, and selected centrally managed configuration. Not an enumeration of every repository's settings.

**Policy Binding**:
The versioned unit that activates governance: an immutable Policy version bound to a Scope Expression with an Enforcement Mode, an Evaluation Role, and an effective period, optionally tagged with a rollout ring. One policy version may operate in different modes across different scopes simultaneously.

**Enforcement Mode**:
The closed set fixed by the core engine — Observe, Plan, Enforce — attached to a Policy Binding, never to a Policy globally. Notification is not a mode.

**Evaluation Role**:
The closed set fixed by the core engine — Authoritative or Shadow — declared explicitly on every Policy Binding, never inferred from version, mode, or dates.

**Authoritative Binding**:
The single active binding per policy and repository that determines the official compliance outcome, remediation planning, enforcement eligibility, and primary audit reporting. Zero means no official compliance interpretation exists; more than one is a configuration error that yields Unknown and a high-visibility finding.

**Shadow Binding**:
A binding evaluated for comparison, pilot analysis, and evidence. It cannot determine the official compliance outcome, produce an executable Remediation Plan, or trigger enforcement.

**Rollout Ring**:
An optional identifier on a Policy Binding grouping bindings into stages of a phased rollout.

**Remediation Plan**:
An immutable, content-hashed, mandatorily expiring artifact describing deterministically ordered operations that would bring noncompliant state into compliance, with preconditions, postconditions, reversibility classes, impact, verification, and rollback procedures. Produced only by an Authoritative Binding in Plan or Enforce mode; valid only against the observed state it was generated from; a modified plan is a new plan.

**Simulated Plan**:
The prospective, never-executable plan produced by a Shadow Binding in Plan mode, labeled as shadow in Evidence.
_Avoid_: calling shadow output a "plan" without qualification

**Plan Approval**:
The governed, immutable authorization to apply one Remediation Plan, bound to its exact content hash. Any material change to the plan invalidates the approval; Enforce mode alone never substitutes for it.

**Standing Remediation Authority**:
An explicit desired-state grant letting a narrowly scoped, pre-approved remediation class execute without per-plan approval. Never inferred from Enforce mode; never available to irreversible, high-impact, or Unknown-reversibility operations.

**Reversibility Class**:
The closed per-operation set — Reversible, PartiallyReversible, Irreversible, Unknown — declared in every Remediation Plan. Unknown is treated conservatively and never receives standing authority.

**Change Budget**:
The hard safety boundary limiting write activity of an enforcement Execution (repositories, organizations, operations, irreversible operations, time, failures). The most restrictive applicable limit wins; exhaustion halts writes and is fully evidenced.

**Evaluation Timestamp**:
The single authoritative timestamp fixed at Execution start, used for binding activation, scope evaluation, relief validity, applicability, compliance interpretation, and planning eligibility. Effective periods are half-open: start inclusive, end exclusive.

### Configuration classes

**Observed State**:
Configuration collected for visibility only, governed by no active Policy. Never classified as noncompliance or drift.

**Policy-Evaluated State**:
Configuration governed by at least one Requirement of an active Policy Binding and evaluated against its minimum requirements or constraints.

**Centrally Managed State**:
Configuration governed by a Requirement using Desired-State Evaluation: Git contains the exact approved artifact, compared deterministically under a Comparison Profile. Not a separate subsystem.

### Governance relief

**Governance Relief**:
The family of governed, scoped, time-bound artifacts that alter governance interpretation of a specific Requirement: a Governance Exception or a Governance Exclusion. Expiry is mandatory; renewal creates a new immutable version; whole-policy coverage must be explicitly declared, never implied.
_Avoid_: accepted deviation, waiver

**Governance Exception**:
A Governance Relief artifact applied after technical evaluation: the Requirement is evaluated, the technical result stays visible, and only the governance interpretation changes. Requires a known technical result — never grantable against Unknown.

**Governance Exclusion**:
A Governance Relief artifact applied before technical evaluation: the Requirement would otherwise apply, but governance intentionally defers or excludes evaluation, so no technical evaluation occurs. Distinct from NotApplicable (logical inapplicability) and from Capability Gap in coverage reporting; requires deterministic applicability.

**Relief Lifecycle**:
The closed state model of a Governance Relief artifact: Draft, Approved, Active, Expiring, Expired, Superseded. Expiry produces a distinct governance finding, never a silent return to NonCompliant.
_Avoid_: deviation lifecycle

### Pipeline

**Discovery**:
The process that finds repositories and collects their state. Never depends on policy applicability.

**Inventory**:
The record of every discovered repository, entered unconditionally at discovery time.

**Scope Resolution**:
Determining whether a repository falls within a Scope Expression, using deterministic attributes. Evaluation begins only after successful scope resolution; enforcement depends on successful evaluation.

**Attribute Provider**:
An engine-executed, versioned capability that supplies repository attributes to Scope Resolution from one source. Providers enrich scope evaluation but cannot redefine its semantics or outcomes.
_Avoid_: scope resolver, attribute source

**Applicability Outcome**:
The closed result set — Applicable, NotApplicable, or Unknown — fixed by the core engine and used both for Scope Resolution and for per-Requirement applicability. NotApplicable never harms aggregation; Unknown applicability normally yields an Unknown compliance outcome.

**Provider Result**:
The closed result set of an attribute lookup: Value Present, Value Absent, or Cannot Determine. Cannot Determine is never converted into Value Absent; a required attribute that cannot be determined makes applicability Unknown.

### Trust and evidence

**Governance Repository**:
The repository holding Desired State; the trusted policy source. Content is approved when it has completed this repository's governance process (currently a merged Pull Request into a protected branch).

**Approved Policy Version**:
An immutable, commit-identified version of a Policy that has completed the Governance Repository's governance process. The only form of policy the engine consumes.

**Execution**:
A single identifiable run of the governance engine that evaluates a declared Evaluation Scope and produces Evidence.

**Evaluation Scope**:
The explicitly declared target set of an Execution — Enterprise, Organization, Repository, Policy, or Rollout Ring. Part of execution identity; authoritative results supersede prior results only within it.

**Execution Status**:
The closed execution-level completeness result recorded in Evidence: Complete, CompleteWithGaps, or Failed, with accounting of discovered, evaluated, and Unknown counts.

**Periodic Reconciliation**:
The authoritative evaluation mechanism: scheduled full evaluation of a scope. Reactive execution may reduce detection latency but never replaces it; the audit guarantee rests on periodic evaluation, not event delivery.

**Result Age**:
The elapsed time since a result's Evaluation Timestamp. Reports flag results stale beyond configurable thresholds; an old compliant result is not equivalent to a recent one.

**Evidence**:
The append-only, authoritative, schema-versioned record produced by an Execution: the minimum needed to explain, reproduce, verify provenance for, and audit a governance decision. Identical regardless of operational log level.

**Operational Log**:
Engine operation and troubleshooting data under a closed severity model (ERROR, WARN, INFO, DEBUG, TRACE). Never authoritative governance evidence; may have shorter retention.

**Derived Report**:
A regenerable human- or machine-readable summary produced from Evidence, citing the Execution Manifests it derives from. Never authoritative — when a report and Evidence disagree, Evidence wins.

**Execution Manifest**:
The per-Execution record listing every evidence item and its content hash; the tamper-evidence root that Derived Reports reference.

**Normalized Observed State**:
The smallest decision-relevant representation of observed configuration stored in Evidence (observed versus expected values), never complete API payloads.

**Sensitivity Classification**:
The closed label carried by every evidence and log record: Public, Internal, Confidential, or Restricted.

**Retention Lifecycle**:
The closed state model for stored governance data — Hot, Archived, Expired, Disposed. Disposal follows an approved retention policy and produces a disposal record.

**Replay Input Set**:
The minimum deterministic inputs that reproduce an evaluation: policy, binding, attribute-provider, and capability-matrix versions; Normalized Observed State; active Governance Relief artifacts; Evaluation Timestamp; engine version.

### Compatibility

**Capability Matrix**:
The versioned, trusted description of which capabilities each validated GHES version supports; the authoritative compatibility source. An absent entry means Unknown, never unsupported; runtime observation may corroborate but never silently overrides it.

**NotApplicable Reason**:
The closed category carried by every NotApplicable requirement: RepositoryCharacteristic, PolicyPrecondition, or PlatformCapabilityUnavailable.

**Coverage Outcome**:
The closed result describing whether intended controls are actually applied — Covered, PartiallyCovered, CapabilityGap, GovernanceExclusion, or Unknown — reported independently of compliance and never flattened into it. Detailed coverage reasons remain available beneath the aggregate.

**Capability Gap**:
A distinct governance finding: an intended control cannot be applied because the validated GHES version lacks the required capability. Compliance may be green while coverage shows the gap.

### Findings

**Finding**:
The recorded outcome of evaluating one Requirement for one repository under one Policy Binding, always interpreted with the Enforcement Mode active at evaluation time. Findings are per-Requirement; flat policy-level-only findings do not exist.

**Technical Outcome**:
The closed result of technical evaluation of a Requirement — Compliant, NonCompliant, Unknown, or NotEvaluated — never altered by governance artifacts.

**Governance Interpretation**:
The closed governance overlay on a Technical Outcome — None, Exception, or Exclusion — always citing the Governance Relief artifact applied.

**Requirement Outcome**:
The closed interpreted result derived from Technical Outcome plus Governance Interpretation: Compliant, NonCompliant, Excepted, Excluded, or Unknown. Excepted is visible accepted risk, never ordinary compliance; Excluded means no technical evaluation occurred.
_Avoid_: AcceptedDeviation (as an outcome name)

**Policy Outcome**:
The closed policy-level result aggregated deterministically from Requirement Outcomes: Compliant, CompliantWithExceptions, NonCompliant, or Unknown. NonCompliant outranks Unknown, which outranks CompliantWithExceptions; Excluded and NotApplicable are aggregation-neutral but coverage-significant.

**Unknown**:
The cross-cutting closed-set member meaning "could not be determined," appearing at every layer: provider results (as CannotDetermine), applicability, requirement and policy outcomes, coverage, and execution accounting. Unknown never satisfies, violates, or excuses a control — uncertainty never grants privilege — and always surfaces as actionable governance work.
_Avoid_: unknown state

**Noncompliance**:
A violation of an applicable Policy by actual configuration. A difference is noncompliance only when a Policy governs it.
_Avoid_: drift (for policy violations)

**Drift**:
Informal name only: the NonCompliant Technical Outcome of a Desired-State Evaluation. Not a first-class concept, outcome, or finding type.
_Avoid_: drift as a distinct domain concept, or as a blanket term for any difference from expectations
