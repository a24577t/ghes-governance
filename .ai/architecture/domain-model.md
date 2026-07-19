# Domain Model — GHES Governance Platform

Consolidation artifact assembled from candidate ADRs 0001–0012 and `CONTEXT.md` (2026-07-13), refined by ADR-0013 and ADR-0014 (2026-07-15). It introduces no new concepts; where this document and an ADR disagree, the ADR is authoritative. Terminology follows `CONTEXT.md` exactly.

---

## 1. Entities

### Desired-state entities (authored, versioned, governed via merged PR — ADR-0002)

| Entity | Identity | Notes |
|---|---|---|
| Policy | stable policy identifier + version | Groups Requirements; never the smallest unit (ADR-0006) |
| Requirement | stable requirement identifier (within policy) | Declares one Evaluation Strategy; identity survives versions while meaning holds (ADR-0006, ADR-0012) |
| Scope Expression | versioned | Written in core scope-expression language (ADR-0003) |
| Policy Binding | binding identifier + binding version | Policy version + Scope Expression + Enforcement Mode + Evaluation Role + effective period (+ Rollout Ring) (ADR-0004, ADR-0005) |
| Governance Relief | artifact identifier + immutable version | Two types: Governance Exception, Governance Exclusion (ADR-0008) |
| Comparison Profile | versioned | Governs Desired-State Evaluation comparison (ADR-0012) |
| Attribute-provider configuration | versioned | Declares active providers and their configuration (ADR-0003) |
| Capability Matrix selection | explicit selection or engine-bundled default | Never silent fallback after failed explicit selection (ADR-0007) |
| Plan Approval | bound to plan content hash | Immutable governed authorization of one Remediation Plan (ADR-0011) |
| Standing Remediation Authority | explicit grant (future) | Never inferred from Enforce; never for irreversible/Unknown-reversibility operations (ADR-0011) |
| Centrally managed artifact | versioned | The exact desired configuration compared by a Desired-State Evaluation requirement (ADR-0001, ADR-0012) |

### Engine-release entities (validated engine capabilities — never runtime-supplied)

Evaluation Strategies (`PredicateEvaluation`, `DesiredStateEvaluation`), attribute-provider implementations, the bundled Capability Matrix, and every closed set: Enforcement Mode, Evaluation Role, Applicability Outcome, Provider Result, Technical Outcome, Governance Interpretation, Requirement Outcome, Policy Outcome, Coverage State, Coverage Reason, NotApplicable Reason, Reversibility Class, Execution Status, Unknown Classification, severity levels, lifecycle states. (ADR-0003, ADR-0012, ADR-0015)

### Produced entities (engine outputs)

| Entity | Identity | Notes |
|---|---|---|
| Execution | execution identifier + declared Evaluation Scope + Evaluation Timestamp | One active per overlapping scope (ADR-0010) |
| Inventory record | repository identifier per Execution | Universal, unconditional at discovery (ADR-0003) |
| Finding | (policy binding, repository, requirement) | Carries Technical Outcome, Governance Interpretation, Requirement Outcome, mode, role (ADR-0006) |
| Remediation Plan | immutable plan identifier + content hash | Append-only; modified plan = new plan (ADR-0011) |
| Simulated Plan | labeled shadow output | Never executable (ADR-0005) |
| Evidence item | content hash + schema version + sensitivity classification | Append-only (ADR-0009) |
| Execution Manifest | 1:1 with Execution | Lists every evidence item + hash; tamper-evidence root (ADR-0009) |
| Execution Digest | 1:1 with Execution Manifest | Versioned root commitment to the Execution's evidence; v1 = canonical content hash of the manifest; recorded outside it; derived, never an independent authority (ADR-0014) |
| Derived Report | regenerable | Cites source manifests; never authoritative (ADR-0009) |

---

## 2. Relationships

```text
Policy 1 ──── * Requirement ──── declares 1 Evaluation Strategy
Requirement (DesiredStateEvaluation) ──── references 1 centrally managed artifact + 1 Comparison Profile
Policy Binding = 1 Policy version × 1 Scope Expression × Mode × Role × effective period
(policy identifier, repository): ≤ 1 active Authoritative Binding; 0..* Shadow Bindings
Governance Relief ──── targets (policy id, requirement id, scope-or-repository)
Execution 1 ──── 1 Execution Manifest ──── 1 Execution Digest (committing to it, stored outside it); 1 ──── * evidence items; 1 ──── * Findings
Finding = (Policy Binding × repository × Requirement) at one Evaluation Timestamp
Remediation Plan ──── from 1 source Execution; Plan Approval ──── binds 1 plan content hash
Rollback plan ──── explicitly links to the original execution (ADR-0011)
Attribute Provider ──── supplies attributes to Scope Resolution (never semantics)
Capability Matrix ──── consulted per compatibility-dependent Requirement evaluation
Derived Report ──── derives from * Execution Manifests
```

---

## 3. Ownership

- **Governance Repository (desired state)** owns every governed artifact listed in §1a. Approval = completion of its governance process (merged PR into protected branch). The repository's own protection configuration is the first centrally managed Requirement (ADR-0002, ADR-0012).
- **Engine release** owns semantics: closed sets, strategy and provider implementations, scope-expression language, aggregation rules, the pipeline. Desired state selects capabilities by identifier/version; it never supplies implementations (ADR-0003, ADR-0012).
- **GHES** remains authoritative for every setting not governed by an active policy (ADR-0001).
- **Evidence store** is architecturally separate from desired state; policy-author access never implies evidence-write access (ADR-0009).
- **Organizational approval hierarchy** is owned outside the platform entirely; the engine records provenance and never validates authority (ADR-0002).

---

## 4. Lifecycles

- **Governed artifact versions** (policies, scope expressions, bindings, relief, profiles): immutable once approved; change = new version; supersession explicit. Draft and Approved are Git-process states; the engine sees only approved content.
- **Governance Relief**: `Draft → Approved → Active → Expiring → Expired`, `Superseded` on replacement. Expiry mandatory and loud (ADR-0008).
- **Policy Binding**: approved → active within its half-open effective period at the fixed Evaluation Timestamp → ended/superseded. Mode transitions bidirectional via governed change; demotion first-class (ADR-0004, ADR-0005).
- **Remediation Plan**: generated → approved (hash-bound) → applied | stale (precondition mismatch) | expired. Never amended (ADR-0011).
- **Execution**: started (timestamp fixed) → `Complete | CompleteWithGaps | Failed` (+ budget-exhausted status when the change budget halts writes) (ADR-0010, ADR-0011).
- **Stored governance data**: `Hot → Archived → Expired → Disposed`, disposal per approved retention policy with disposal record (ADR-0009).

---

## 5. Invariants

1. Merged into the protected governance branch = approved; the engine never validates who approved (ADR-0002).
2. **Uncertainty never grants privilege** — Unknown never satisfies, violates, excuses, or authorizes anything, including writes (ADR-0008, ADR-0011).
3. **Explicit over inferred** — authority, roles, relief, standing write authority, and matrix selection are declared, never derived from version/mode/date heuristics (ADR-0005). Deliberate exception: *restrictions* compose mechanically — the effective execution constraint set is the intersection of all applicable constraints, with the most restrictive numeric limit winning — because inference may only ever remove privilege, never grant it (ADR-0011).
4. At most one active Authoritative Binding per (policy, repository); an official compliance interpretation derives from exactly one. Zero is a normal rollout state producing no official interpretation (neither `Unknown` nor `NotApplicable`) and no Coverage State — absent intent means there is no intended control set to measure. More than one is a configuration error → no enforcement; each conflicting binding is still evaluated, but only as explanatory evidence, never as an official governance outcome; requirement sets are never synthesized across conflicting policy versions; the pair's official Policy Outcome and Coverage State are both `Unknown`, with a high-visibility finding. Ambiguous intent yields `Unknown` in both dimensions; absent intent yields neither. Three-valued applicability refines this (ADR-0015): a candidate authoritative binding whose scope applicability is `Unknown` is neither counted as authority nor excluded, so authority may be *undeterminable* — one applicable binding with an undetermined competitor, or none applicable with two or more undetermined candidates — yielding `Unknown` in both dimensions as a terminal authority-selection result before requirement evaluation, distinct from proven conflict and from absent authority. Enforcement Mode never contributes to determining authority (ADR-0005, ADR-0013, ADR-0015).
5. Observation is universal; evaluation requires scope resolution; enforcement requires evaluation, an Enforce-mode authoritative binding, *and* plan approval or standing authority (ADR-0003, ADR-0011).
6. `CannotDetermine` never becomes `Value Absent`; undetermined capability never becomes unsupported; unknown strategy is never substituted (ADR-0003, ADR-0007, ADR-0012).
7. Technical Outcomes are never altered by governance artifacts; interpretation is a separate overlay (ADR-0006).
8. Compliance and coverage are independent dimensions, never flattened (ADR-0007).
9. Evidence is append-only, minimal-but-sufficient, schema-versioned, identical at every log level; reports are never authoritative (ADR-0009).
10. One fixed Evaluation Timestamp per Execution; half-open effective periods (ADR-0005).
11. Relief and plans must expire; renewal is a new immutable version (ADR-0008, ADR-0011).
12. Change budgets are hard boundaries; plans are precondition-bound and never adapted dynamically (ADR-0011).
13. Scope reduction is not relief; historical evidence survives a repository leaving scope (ADR-0008).
14. The audit guarantee rests on periodic reconciliation, never event delivery (ADR-0010).
15. Write authority is granted only through the governed desired-state process; it may be removed or paused through an explicitly defined emergency suspension path — authenticated, append-only, evidenced, later reconciled — that can only reduce authority. Authorization validity (approval, revocation, expiry, standing authority, suspension) is revalidated before every write operation; revocation never undoes completed operations. The concrete emergency path is a deferred decision — the POC uses the governed process for both grant and removal (ADR-0011).

---

## 6. Extension points

| Extension point | Mechanism | Trust posture |
|---|---|---|
| Attribute Providers | provider interface; three-result contract | Implementation = engine capability; configuration = desired state; inside TCB (ADR-0003) |
| Evaluation Strategies | internal registry; invariant outcome/determinism contract | Release-fixed engine capability; selected by desired state; never runtime-supplied (ADR-0012) |
| Notification actions | configurable outputs from any mode | Not an enforcement mode; mechanism varies by deployment (ADR-0004) |
| Capability Matrix versions | explicit selection | Versioned trusted input; no silent fallback (ADR-0007) |
| Standing Remediation Authority | future desired-state grants per operation class | Narrow, reversible, budgeted; never inferred (ADR-0011) |
| Reactive execution triggers | future acceleration of reconciliation | Never replaces the periodic guarantee (ADR-0010) |
| Control catalog | future authoring layer | Compiles into the same policy→requirement model (ADR-0006) |
| Evidence hardening backends | future (signing, WORM, anchoring) | Model supports without requiring (ADR-0009) |

---

## 7. Event flow (one Execution)

```text
Trigger (manual for POC)
  → fix Evaluation Timestamp; acquire single-execution lock; declare Evaluation Scope
  → load approved desired state at pinned versions
      (policies, bindings, relief, comparison profiles, provider config, matrix selection)
  → Discovery → Inventory (unconditional, universal)
  → per (active binding × repository in scope) …
      Scope Resolution (attribute providers; three-result contract)
        → Applicability Outcome (Applicable | NotApplicable+reason | Unknown)
      → per Requirement:
          capability check (matrix) → Evaluation Strategy executes
            → Technical Outcome (+ Normalized Observed State)
          → Governance Interpretation (relief: exception/exclusion, validity at timestamp)
            → Requirement Outcome
      → policy aggregation → Policy Outcome; coverage assessment → Coverage State (+ Coverage Reasons)
      → Findings (authoritative vs shadow results separated)
      → Plan mode: Remediation Plan (authoritative) / Simulated Plan (shadow)
      → Enforce mode (future writes): per-operation order of ADR-0011
        (plan hash + expiry → budget → re-read → preconditions → prior-state capture
         → apply → verify → evidence)
  → evidence items (hashed) → Execution Manifest → Execution Status + completeness accounting
  → Derived Reports regenerated from evidence (freshness, staleness thresholds)
```
