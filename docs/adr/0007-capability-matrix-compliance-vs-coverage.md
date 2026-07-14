---
status: proposed
---

# Versioned capability matrix; compliance and coverage reported separately

Compatibility with multiple GHES versions is resolved against a versioned capability matrix — not runtime probing — and the engine reports two independent dimensions: **compliance** (are the evaluable requirements met?) and **coverage** (are the intended controls actually applied?). A repository may be compliant with every requirement its platform can execute while still lacking intended security controls because the GHES version does not support them; those two facts are never flattened into a single green result.

## Capability knowledge

The matrix describes supported combinations: GHES version; GHES feature or API capability; applicable REST API version; GHAS capability; Actions capability; supported action version and runner/workflow prerequisites where relevant. It is trusted engine input: version-controlled, reviewed, immutable for a released version, and traceable to authoritative GitHub documentation and validation testing.

**Selection authority:** desired-state matrix selection is authoritative when explicitly configured; absent an explicit selection, the engine-bundled default applies. In all cases evidence records the selected matrix identifier, matrix version, matrix content hash, selection source, engine version, GHES version, capability entry consulted, compatibility result, and supporting evidence. An explicitly selected matrix that is missing, malformed, untrusted, or incompatible produces `Unknown` for affected evaluations — the engine never silently falls back to the bundled default after an explicit desired-state selection fails. An absent matrix entry is `Unknown`, not unsupported. Runtime probing is deferred as an authority source; if later added as corroborating observed evidence it must not silently override the matrix — a conflict between observation and matrix yields a capability conflict or `Unknown`, never an inferred answer.

## Version detection and the Unknown rule

The engine obtains the GHES version from a supported server response or administration endpoint when available. If the GHES version, a matrix entry, permission state, runtime capability, or prerequisite data cannot be reliably determined (insufficient permission, connection failure, malformed response, unsupported server, unexpected version format), every dependent requirement produces an `Unknown` applicability or evaluation result. `CannotDetermine` never collapses into capability-unsupported, attribute-absent, not-applicable, or compliance — the same fail-loud contract as attribute providers (ADR-0003). Failure to determine compatibility is never treated as lack of capability.

## NotApplicable reason model

A `NotApplicable` requirement carries a closed reason category — `RepositoryCharacteristic` (e.g. no GitHub Actions workflows exist), `PolicyPrecondition` (e.g. a prerequisite governance classification does not match), `PlatformCapabilityUnavailable` (the validated GHES version does not support the required feature) — optionally accompanied by a human-readable explanation. Providers and policies cannot invent semantic categories.

## Coverage outcome

Alongside compliance outcomes (ADR-0006), intended controls receive a coverage outcome: `Covered`, `PartiallyCovered`, `CapabilityGap`, `GovernanceExclusion` (ADR-0008), `Unknown`. Detailed coverage reasons remain available beneath the primary aggregate outcome. A requirement inapplicable due to `PlatformCapabilityUnavailable` contributes nothing to compliance and contributes `CapabilityGap` to coverage. Policy reporting shows both dimensions; `Compliance: Compliant / Coverage: CapabilityGap` ("all evaluable requirements comply, but one or more intended controls cannot be applied because of a platform limitation") must never share a visual or summary status with full compliance at full coverage.

## Capability gaps are governance findings

A platform-capability gap produces a distinct finding containing: policy and requirement identifiers; repository or organizational scope; detected GHES version; required capability; minimum or validated supporting version when known; capability-matrix version; remediation guidance (such as evaluating a GHES upgrade); evidence timestamp. The engine does not decide whether an upgrade must occur — it makes suppressed security coverage explicit and auditable.

## Newer-than-validated GHES

When the detected GHES version is newer than the validated capability matrix: discovery may continue; reporting continues where safe; compatibility-dependent evaluations become `Unknown`; planning and enforcement for affected requirements are disabled; and the report identifies that the platform version is newer than validated compatibility knowledge. A newer GHES version is never assumed backward compatible.

## First vertical slice

A synthetic GHES version; a small versioned capability matrix; one requirement whose capability is supported; one whose capability is unavailable; one scenario where capability cannot be determined; separate applicability, compliance, and coverage results; evidence recording matrix and GHES versions.
