---
status: proposed
---

# Three data classes: authoritative evidence, operational logs, derived reports

Audit readiness does not mean unlimited retention of every log and intermediate event. The platform defines three distinct data classes with different authority, retention, and sensitivity treatment — and desired state, evidence, and reports remain architecturally separate (evidence never lives in the governance repository; policy-author access never implies evidence-write access).

## Data classes

- **Authoritative Evidence** — append-only, authoritative; the information required to explain, reproduce, or audit a governance decision: execution manifest, engine version, policy and binding versions, evaluation timestamp, repository identifier, scope-resolution inputs and outcomes, observed values used by each requirement, requirement/policy/coverage outcomes, accepted exceptions or exclusions, proposed or executed changes, verification results, content hashes and execution digest.
- **Operational Logs** — engine operation and troubleshooting (startup/shutdown, API requests and status, retries, timing, parsing diagnostics, provider errors, debug traces). Never authoritative governance evidence; may have shorter retention.
- **Derived Reports** — human- or machine-readable summaries generated from evidence (compliance dashboards, coverage summaries, exception reports, rollout reports, shadow comparisons). Regenerable and never authoritative; every report references the execution manifests it derives from.

## Minimal but sufficient evidence

Evidence stores only what is necessary to explain and reproduce the decision, verify provenance, and support audit, rollback, and incident investigation. Observed state is normalized to the smallest decision-relevant representation (e.g. `required_approvals observed: 0 / expected: >= 1`), not complete API responses. Complete payloads, source contents, secrets, and unrelated repository data are not automatically retained.

## Retention

Retention is configurable by data class and environment (evidence by execution kind, operational logs by severity, reports, failed executions, security events; POC vs production values). The engine hard-codes no enterprise retention periods; final values derive from legal, compliance, operational, and cost requirements. Stored data supports a retention lifecycle — `Hot → Archived → Expired → Disposed` — where disposal follows an approved retention policy and produces a disposal record or lifecycle audit event where required. Evidence is never deleted merely because the engine no longer needs it operationally.

## Operational logging

Closed severity model: `ERROR` (execution/integrity/write/evidence failures, unresolved compatibility problems), `WARN` (recoverable or governance-significant conditions: retries, unknown results, capability conflicts, expired relief artifacts, conflicting bindings), `INFO` (execution lifecycle and summaries, no verbose payloads), `DEBUG` (temporary troubleshooting, richer detail, still no secrets), `TRACE` (disabled by default; short diagnostic windows in controlled environments only). Production default is `INFO` with targeted temporary elevation; the POC may default to `DEBUG` locally with short retention.

**Evidence is independent of log level**: the engine produces identical authoritative evidence at `INFO` and `DEBUG`, so a cost-saving logging change can never weaken auditability.

## Sensitivity and redaction

Every evidence and log record carries a sensitivity classification: `Public`, `Internal`, `Confidential`, `Restricted`. The POC contains only synthetic public-safe data. Future implementations must support secret/credential redaction, source-content suppression, configurable hashing or tokenization of sensitive identifiers, access controls separate from policy-author access, and sensitivity-based retention. Logs never contain authentication tokens, private keys, secret values, raw credential material, or unnecessarily complete API payloads.

## Tamper evidence proportional to maturity

POC: evidence in a physically separate local directory; every evidence item content-hashed; every execution produces a manifest listing each item and its hash; reports reference the manifest. This gives tamper *detection* without infrastructure. Production may add immutable object storage, retention locks, digital signatures, external digest anchoring, and separate security-account ownership — the evidence model supports these without requiring them in the POC.

## Replayability

Replay relies on the minimum deterministic input set — policy version, binding version, attribute-provider versions, capability-matrix version, normalized observed state, active governance relief artifacts, evaluation timestamp, engine version — not on preserving operational logs.

## POC boundary

The first vertical slice implements separate evidence and log directories, schema-versioned evidence, execution manifest with hashes, configurable log level, configurable retention metadata, no automatic deletion initially, synthetic data only. It does not require S3, Object Lock, signing infrastructure, centralized log aggregation, or long-term retention automation.
