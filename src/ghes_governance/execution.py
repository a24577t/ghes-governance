"""The Execution boundary seam.

One entry point takes an injected Evaluation Timestamp and execution identifier (the
engine never reads a wall clock) and produces, for a synthetic estate: an Inventory of
every discovered repository, per-pair binding provenance, per-requirement findings and an
aggregated Policy Outcome / Coverage State for governed pairs, an Execution Status, an
Execution Manifest, and an external Execution Digest. A pair with no active authoritative
binding is ungoverned (no invented outcome); a pair whose scope applicability is Unknown
reports Unknown outcomes and makes the Execution Status CompleteWithGaps.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import ENGINE_VERSION, control
from .bundle import load_bundle, load_estate
from .canonical import content_hash
from .enums import (
    ApplicabilityOutcome,
    CoverageState,
    ExecutionStatus,
    PolicyOutcome,
    RefusalCategory,
    Severity,
    UnknownClassification,
)
from .errors import BundleError, ConfigurationError, ExecutionRefusedError
from .evaluation import (
    AuthorityConflict,
    AuthorityUndeterminable,
    evaluate_policy,
    explanatory_requirement_outcomes,
    select_authoritative_binding,
)
from .model import (
    binding_provenance_payload,
    bundle_validation_payload,
    evidence_item,
    execution_status_payload,
    findings_payload,
    governance_findings_payload,
    inventory_payload,
    manifest_header,
    policy_results_payload,
)
from .oplog import record_execution_event, record_refusal
from .store import execution_exists, write_execution
from .validation import validate_bundle

_INVENTORY_FIELDS = ("id", "organization", "name", "visibility", "archived", "fork", "ghes_version")


@dataclass(frozen=True)
class ExecutionResult:
    execution_id: str
    status: ExecutionStatus
    execution_dir: Path


def _inventory_record(repo: dict[str, Any]) -> dict[str, Any]:
    if "id" not in repo:
        raise BundleError("estate repository is missing 'id'")
    return {field: repo[field] for field in _INVENTORY_FIELDS if field in repo}


def _pair_provenance(
    policy_id: str, repository_id: str, *, authoritative_binding_count: int
) -> dict[str, Any]:
    return {
        "policy_id": policy_id,
        "repository_id": repository_id,
        "authoritative_binding_count": authoritative_binding_count,
        "governed": authoritative_binding_count > 0,
    }


def _index_policies(policies: list[dict[str, Any]]) -> dict[str, dict[Any, dict[str, Any]]]:
    """Group policy documents by id then declared version.

    Ensures each policy id is processed exactly once per repository and lets a binding's
    declared policy version resolve to its own requirement set — so two documents that share
    an id but carry divergent versions (and divergent requirement sets) coexist without the
    pair being processed once per document.
    """
    indexed: dict[str, dict[Any, dict[str, Any]]] = {}
    for policy in policies:
        policy_id = policy.get("id")
        if policy_id is None:
            raise BundleError("bundle policy is missing 'id'")
        version = policy.get("version")
        versions = indexed.setdefault(policy_id, {})
        if version in versions:
            raise BundleError(
                f"duplicate policy document for policy {policy_id!r} version {version!r}"
            )
        versions[version] = policy
    return indexed


def _policy_for_binding(
    versions: dict[Any, dict[str, Any]], binding: dict[str, Any], policy_id: str
) -> dict[str, Any]:
    """Resolve a binding's declared policy version to its document.

    Fails loud with a contextual ``BundleError`` when the declared version has no matching
    document — the binding is never silently resolved to a different version.
    """
    version = binding.get("policy_version")
    try:
        return versions[version]
    except KeyError:
        raise BundleError(
            f"binding for policy {policy_id!r} declares policy version {version!r} "
            "with no matching policy document"
        ) from None


def _authority_conflict_finding(
    policy_id: str,
    repository_id: str,
    conflicting: list[dict[str, Any]],
    versions: dict[Any, dict[str, Any]],
    repo: dict[str, Any],
) -> dict[str, Any]:
    """A governance-configuration finding for a proven authority conflict.

    Enumerates every conflicting authoritative binding by its stable content identity, its
    declared policy version, and its scope; records each binding's own requirement set and the
    per-requirement outcomes it produces as EXPLANATORY-ONLY evidence — evaluated under that
    binding's version and never contributing to the official pair outcome, accounting, or
    coverage. States that no binding determined the official outcomes, and reports the shared
    and per-binding requirement-set divergence. Requirement sets are never unioned or
    synthesized across versions (ADR-0013 no-synthesis; ADR-0005/0015).
    """
    binding_entries: list[dict[str, Any]] = []
    for binding in conflicting:
        policy_doc = _policy_for_binding(versions, binding, policy_id)
        requirement_ids = [req["id"] for req in policy_doc["requirements"]]
        explanatory = evaluate_policy(policy_doc, repo)["findings"]
        binding_entries.append(
            {
                "binding_id": content_hash(binding),
                "policy_version": binding.get("policy_version"),
                "scope": binding.get("scope"),
                "requirement_ids": requirement_ids,
                # Evaluation owns which findings are evaluated outcomes and how NotApplicable is
                # represented; execution only assembles the projection it returns.
                "explanatory_requirements": explanatory_requirement_outcomes(explanatory),
            }
        )
    return {
        "kind": "authority_conflict",
        "policy_id": policy_id,
        "repository_id": repository_id,
        "official_outcomes_determined": False,
        "conflicting_bindings": binding_entries,
        "requirement_set_divergence": _requirement_set_divergence(binding_entries),
    }


def _requirement_set_divergence(binding_entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Shared vs per-binding-only requirement IDs across the conflicting bindings.

    ``shared`` is the intersection of every binding's requirement set; each ``only_in`` entry
    lists one binding's requirements not shared by all, keyed by that binding's stable
    identity and version. Deterministically sorted; the union is never materialized as a
    synthesized requirement set.
    """
    sets = [set(entry["requirement_ids"]) for entry in binding_entries]
    shared = set.intersection(*sets) if sets else set()
    only_in = [
        {
            "binding_id": entry["binding_id"],
            "policy_version": entry["policy_version"],
            "requirement_ids": sorted(set(entry["requirement_ids"]) - shared),
        }
        for entry in binding_entries
    ]
    return {"shared": sorted(shared), "only_in": only_in}


def _unknown_result(
    policy_id: str, repository_id: str, classification: str
) -> dict[str, Any]:
    """A terminal Unknown pair result — the causal record carrying its Unknown Classification."""
    return {
        "policy_id": policy_id,
        "repository_id": repository_id,
        "policy_outcome": PolicyOutcome.UNKNOWN.value,
        "coverage_state": CoverageState.UNKNOWN.value,
        "unknown_classification": classification,
    }


def _authority_undeterminable_finding(
    policy_id: str, repository_id: str, undeterminable: AuthorityUndeterminable
) -> dict[str, Any]:
    """A governance finding: authority cannot be established; names every candidate binding
    and, per unresolved candidate, the scope attributes that could not be determined."""
    candidate_bindings = [
        {
            "policy_version": binding.get("policy_version"),
            "scope": binding.get("scope"),
            "applicability": ApplicabilityOutcome.APPLICABLE.value,
        }
        for binding in undeterminable.applicable
    ] + [
        {
            "policy_version": binding.get("policy_version"),
            "scope": binding.get("scope"),
            "applicability": ApplicabilityOutcome.UNKNOWN.value,
            "undetermined_attributes": attributes,
        }
        for binding, attributes in undeterminable.undeterminable
    ]
    return {
        "kind": "authority_undeterminable",
        "policy_id": policy_id,
        "repository_id": repository_id,
        "candidate_bindings": candidate_bindings,
    }


def _write_failed_execution(
    *,
    store_root: str | Path,
    execution_id: str,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    engine_version: str,
    errors: list[dict[str, Any]],
) -> ExecutionResult:
    """Write a Failed Execution: configuration evidence plus a Failed Execution Status (T5).

    Reached when whole-bundle validation rejects the desired state. Discovery and evaluation
    never ran, so the accounting is zero and no inventory, binding-provenance, findings, or
    policy-results are produced — only the validation evidence and the status flow through the
    frozen integrity chain (manifest + external digest). No authoritative compliance or
    coverage results are produced (AC 12).
    """
    status = execution_status_payload(
        ExecutionStatus.FAILED, discovered=0, evaluated=0, unknown=0
    )
    validation = bundle_validation_payload(errors)
    items = [
        ("bundle-validation.json", evidence_item("bundle_validation", execution_id, validation)),
        ("execution-status.json", evidence_item("execution_status", execution_id, status)),
    ]
    header = manifest_header(execution_id, evaluation_scope, evaluation_timestamp, engine_version)
    exec_dir = write_execution(store_root, execution_id, header, items)
    return ExecutionResult(
        execution_id=execution_id, status=ExecutionStatus.FAILED, execution_dir=exec_dir
    )


def _operational_log_target(log_root: str | Path | None, store_root: str | Path) -> Path:
    """Where operational events (pre-execution refusals and execution-time stage/detail events) are
    written: the given operational-log location, or a default Operational Log directory beside the
    store when none is supplied (a local default). The default is a sibling of the store, always
    outside it; an explicitly supplied ``log_root`` is validated, never silently relocated."""
    return Path(log_root) if log_root is not None else Path(store_root).parent / "operational-log"


def _reject_overlapping_roots(store_root: str | Path, log_target: str | Path) -> None:
    """Reject an Operational Log directory that physically overlaps the evidence store.

    The Operational Log and Authoritative Evidence are separate data classes (ADR-0009) and must
    occupy disjoint directories, so an operational event can never be written inside the evidence
    store. Overlap is any of: the two roots are equal, the log is beneath the store, or the store
    is beneath the log. Checked with path-aware ancestry on resolved paths — never a string-prefix
    comparison, so ``.../store`` and ``.../store-2`` are correctly treated as disjoint. Raised
    before any execution right, Execution, Evidence, or operational event is created; an explicitly
    supplied ``log_root`` is never silently relocated.
    """
    store = Path(store_root).resolve(strict=False)
    log = Path(log_target).resolve(strict=False)
    if store == log or store in log.parents or log in store.parents:
        raise ConfigurationError(
            f"operational log root {str(log)!r} overlaps the evidence store root {str(store)!r}; "
            "the Operational Log and Authoritative Evidence are separate data classes (ADR-0009) "
            "and must occupy disjoint directories — supply a log_root outside the store"
        )


def _correlation_id(
    execution_id: str, evaluation_scope: dict[str, Any], evaluation_timestamp: str
) -> str:
    """Request-envelope correlation key — deterministically derived from the attempted request
    envelope (execution identifier, Evaluation Scope, Evaluation Timestamp).

    It correlates refusal records belonging to the **same attempted request envelope**; it is
    **not** a unique event or per-attempt identifier. Repeated identical attempts therefore share
    the same key, while individual refusal events stay distinct through their separate Operational
    Log records and Evaluation Timestamps. Introduces no wall-clock or RNG dependency (the engine
    reads no clock); the exact derivation is local.
    """
    return content_hash(
        {
            "execution_id": execution_id,
            "evaluation_scope": evaluation_scope,
            "evaluation_timestamp": evaluation_timestamp,
        }
    )


def _refuse_identifier_reuse(
    *,
    log_root: str | Path | None,
    store_root: str | Path,
    execution_id: str,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    engine_version: str,
) -> None:
    """Refuse a request whose Execution Identifier is already present in the store (AC 15).

    Records one structured ``ERROR`` operational refusal event, then raises
    ``ExecutionRefusedError`` — before any Execution-creation side effect, so nothing is written
    below the Execution boundary and the existing execution is left byte-unmodified.
    """
    reason = (
        f"Execution Identifier {execution_id!r} is already present in the target evidence "
        "store; the request is refused before Execution creation (ADR-0009 immutability)."
    )
    record_refusal(
        _operational_log_target(log_root, store_root),
        category=RefusalCategory.IDENTIFIER_REUSE,
        attempted_execution_id=execution_id,
        requested_scope=evaluation_scope,
        timestamp=evaluation_timestamp,
        engine_version=engine_version,
        reason=reason,
        correlation_id=_correlation_id(execution_id, evaluation_scope, evaluation_timestamp),
        existing_execution_id=execution_id,
    )
    raise ExecutionRefusedError(RefusalCategory.IDENTIFIER_REUSE, reason)


def run_execution(
    *,
    bundle_path: str | Path,
    estate_path: str | Path,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    execution_id: str,
    store_root: str | Path,
    log_root: str | Path | None = None,
    log_level: Severity = Severity.INFO,
    control_root: str | Path | None = None,
    engine_version: str = ENGINE_VERSION,
) -> ExecutionResult:
    """Run an Execution and write its Evidence — the Execution boundary seam.

    Inventories every discovered repository unconditionally; for each (policy, repository)
    pair selects the single active authoritative Observe binding via three-result scope
    resolution. An applicable binding is evaluated to per-requirement findings and an
    aggregated Policy Outcome and Coverage State; a binding whose scope applicability is
    Unknown yields Unknown in both dimensions and makes the Execution Status
    CompleteWithGaps; a pair with no applying binding is ungoverned with no invented
    outcome. Writes append-only Evidence, the Execution Manifest, and the external
    Execution Digest under ``store_root/<execution_id>/``. The Evaluation Timestamp and
    execution identifier are injected — no wall clock is read. Raises ``BundleError`` if a
    policy or repository lacks its id.

    Bundle validity is not an Execution-creation precondition (Execution Lifecycle): the
    Execution exists, then the desired-state bundle is validated before discovery or
    evaluation. A structurally malformed or semantically unsupported bundle — including
    unsupported content that appears unreferenced — ends the Execution ``Failed`` with
    configuration evidence and no authoritative compliance or coverage results (AC 12),
    never a raised error.

    Two Execution-creation preconditions are enforced **before any Execution exists**, each
    raising ``ExecutionRefusedError`` (no Execution, no Execution Status, no Evidence) and
    recording one structured ``ERROR`` event in the Operational Log: a reused Execution Identifier
    already present in the store (AC 15), and unavailable exclusive execution rights (AC 13). A
    refusal is distinct from a Failed Execution, which is created and then aborts. Optional
    ``log_root`` names the Operational Log directory for both those refusal events and the
    execution-time stage/detail events; optional ``control_root`` names the mechanism-neutral
    execution-control directory used to hold exclusive execution rights. Both default beside the
    store when not supplied.

    ``log_level`` (default ``Severity.INFO``) is runtime configuration of the Operational Log data
    class, not an Execution-boundary input: it selects which execution-time operational events are
    written (INFO major stages; DEBUG adds per-pair detail) and is **not** part of the Replay Input
    Set. Evidence is byte-identical at every level (ADR-0009). This keyword is a backward-compatible
    extension of the seam signature — existing callers are unaffected — and the governance execution
    contract (evidence-determining inputs and outputs) is unchanged.
    """
    # Configuration validation, before any side effect: the Operational Log and the evidence store
    # are separate data classes (ADR-0009) and must occupy disjoint directories. Resolve the log
    # target once and reject an overlapping configuration here — before any execution right,
    # Execution, Evidence, or operational event (including the refusal events below).
    log_target = _operational_log_target(log_root, store_root)
    _reject_overlapping_roots(store_root, log_target)

    # Execution-creation precondition (AC 15): a reused Execution Identifier is refused before
    # any Execution exists — no Execution, no Status, no Evidence; the existing execution is left
    # byte-unmodified. Checked before bundle validation, so a reused identifier is refused
    # regardless of bundle validity (a Failed Execution requires an Execution to exist first — T5).
    if execution_exists(store_root, execution_id):
        _refuse_identifier_reuse(
            log_root=log_root,
            store_root=store_root,
            execution_id=execution_id,
            evaluation_scope=evaluation_scope,
            evaluation_timestamp=evaluation_timestamp,
            engine_version=engine_version,
        )

    # Execution-creation precondition (AC 13): acquire exclusive execution rights before any
    # Execution-creation side effect. Acquisition is atomic, so two requests cannot both cross the
    # boundary; unavailable rights are refused (no Execution). Release is guaranteed on every
    # terminating path below by ``finally`` — success, Failed Execution (T5), or error.
    reservation = _acquire_rights_or_refuse(
        control_root=control_root,
        store_root=store_root,
        log_root=log_root,
        execution_id=execution_id,
        evaluation_scope=evaluation_scope,
        evaluation_timestamp=evaluation_timestamp,
        engine_version=engine_version,
    )
    try:
        return _execute_governed(
            bundle_path=bundle_path,
            estate_path=estate_path,
            evaluation_scope=evaluation_scope,
            evaluation_timestamp=evaluation_timestamp,
            execution_id=execution_id,
            store_root=store_root,
            log_target=log_target,
            log_level=log_level,
            engine_version=engine_version,
        )
    finally:
        control.release(reservation)


def _acquire_rights_or_refuse(
    *,
    control_root: str | Path | None,
    store_root: str | Path,
    log_root: str | Path | None,
    execution_id: str,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    engine_version: str,
) -> Path:
    """Acquire exclusive execution rights (AC 13), or refuse before any Execution exists.

    On unavailable rights, records one ``ERROR`` rights-unavailable operational event and raises
    ``ExecutionRefusedError`` — no Execution is created, and the control directory's occupancy is
    left unchanged (the engine never alters an entry it did not create).
    """
    target_control = (
        Path(control_root)
        if control_root is not None
        else Path(store_root).parent / "execution-control"
    )
    try:
        return control.acquire(target_control)
    except control._ExecutionRightsUnavailable as exc:
        reason = (
            "exclusive execution rights for the declared Evaluation Scope are unavailable "
            f"(execution-control directory {str(target_control)!r} is occupied); the request is "
            "refused before Execution creation."
        )
        # Rights unavailability may be known without an attributable conflicting Execution: an
        # arbitrary pre-existing control-directory occupant need not represent an Execution, and T6
        # performs no attribution — so no conflicting identifier is recorded (existing_execution_id
        # stays None) rather than inferring or inventing an owner (Contract A).
        record_refusal(
            _operational_log_target(log_root, store_root),
            category=RefusalCategory.RIGHTS_UNAVAILABLE,
            attempted_execution_id=execution_id,
            requested_scope=evaluation_scope,
            timestamp=evaluation_timestamp,
            engine_version=engine_version,
            reason=reason,
            correlation_id=_correlation_id(execution_id, evaluation_scope, evaluation_timestamp),
            existing_execution_id=None,
        )
        raise ExecutionRefusedError(RefusalCategory.RIGHTS_UNAVAILABLE, reason) from exc


def _execute_governed(
    *,
    bundle_path: str | Path,
    estate_path: str | Path,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    execution_id: str,
    store_root: str | Path,
    log_target: str | Path,
    log_level: Severity,
    engine_version: str,
) -> ExecutionResult:
    """Run the Execution body once exclusive rights are held: validate the bundle (Failed path,
    T5), then discover, evaluate, and write Evidence. Extracted so ``run_execution`` guarantees
    release of execution rights around every terminating path (success, Failed, or error).

    Emits execution-time operational events to the Operational Log at ``log_target``, filtered by
    ``log_level`` (major stages at INFO; per-pair detail at DEBUG). Logging is a separate data
    class: it never touches Evidence, so the Evidence written here is byte-identical at every
    level (ADR-0009)."""

    def _log(severity: Severity, event: str, detail: dict[str, Any] | None = None) -> None:
        record_execution_event(
            log_target,
            severity=severity,
            threshold=log_level,
            event=event,
            execution_id=execution_id,
            timestamp=evaluation_timestamp,
            engine_version=engine_version,
            detail=detail,
        )

    _log(Severity.INFO, "execution.started")
    validation_errors = validate_bundle(bundle_path)
    if validation_errors:
        _log(Severity.INFO, "execution.failed", {"validation_errors": len(validation_errors)})
        return _write_failed_execution(
            store_root=store_root,
            execution_id=execution_id,
            evaluation_scope=evaluation_scope,
            evaluation_timestamp=evaluation_timestamp,
            engine_version=engine_version,
            errors=validation_errors,
        )

    bundle = load_bundle(bundle_path)
    estate = load_estate(estate_path)

    repositories = estate["repositories"]
    inventory = inventory_payload([_inventory_record(repo) for repo in repositories])
    _log(Severity.INFO, "discovery.completed", {"discovered": len(repositories)})

    pairs: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    governance_findings: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    evaluated = 0
    unknown = 0

    policies_by_id = _index_policies(bundle["policies"])

    for policy_id, versions in policies_by_id.items():
        for repo in repositories:
            _log(
                Severity.DEBUG,
                "pair.processing",
                {"policy_id": policy_id, "repository_id": repo["id"]},
            )
            selection = select_authoritative_binding(
                bundle["bindings"], policy_id, repo, evaluation_timestamp
            )
            if selection is None:
                pairs.append(
                    _pair_provenance(policy_id, repo["id"], authoritative_binding_count=0)
                )
                continue

            if isinstance(selection, AuthorityConflict):
                # Proven conflict → a terminal pair-level Unknown, classified GovernanceResult
                # (not an observation gap, so Execution Status stays Complete), no requirement
                # evaluation, and an authority-conflict finding (ADR-0005/0013/0015).
                pairs.append(
                    _pair_provenance(
                        policy_id,
                        repo["id"],
                        authoritative_binding_count=len(selection.conflicting),
                    )
                )
                results.append(
                    _unknown_result(
                        policy_id, repo["id"], UnknownClassification.GOVERNANCE_RESULT.value
                    )
                )
                governance_findings.append(
                    _authority_conflict_finding(
                        policy_id, repo["id"], selection.conflicting, versions, repo
                    )
                )
                unknown += 1
                continue

            if isinstance(selection, AuthorityUndeterminable):
                # Authority cannot be established (ADR-0015, A=1 & U≥1): a terminal pair-level
                # Unknown classified IncompleteObservation (a Cannot-Determine gap → the status
                # is CompleteWithGaps), no requirement evaluation, and an authority-undeterminable
                # finding naming every candidate and the undetermined attributes.
                candidate_count = len(selection.applicable) + len(selection.undeterminable)
                pairs.append(
                    _pair_provenance(
                        policy_id, repo["id"], authoritative_binding_count=candidate_count
                    )
                )
                results.append(
                    _unknown_result(
                        policy_id, repo["id"], UnknownClassification.INCOMPLETE_OBSERVATION.value
                    )
                )
                governance_findings.append(
                    _authority_undeterminable_finding(policy_id, repo["id"], selection)
                )
                unknown += 1
                continue

            _binding, applicability = selection
            pairs.append(_pair_provenance(policy_id, repo["id"], authoritative_binding_count=1))

            if applicability is ApplicabilityOutcome.UNKNOWN:
                results.append(
                    _unknown_result(
                        policy_id, repo["id"], UnknownClassification.INCOMPLETE_OBSERVATION.value
                    )
                )
                unknown += 1
            else:
                evaluation = evaluate_policy(
                    _policy_for_binding(versions, _binding, policy_id), repo
                )
                findings.extend(evaluation["findings"])
                # Assemble evaluation-produced governance-configuration findings (AC 6 unsupported
                # strategy) into execution evidence; evaluation remains their semantic owner.
                governance_findings.extend(evaluation["governance_findings"])
                results.append(
                    {
                        "policy_id": policy_id,
                        "repository_id": repo["id"],
                        "policy_outcome": evaluation["policy_outcome"],
                        "coverage_state": evaluation["coverage_state"],
                    }
                )
                evaluated += 1
                # Each requirement-level Unknown (a GovernanceResult from an unsupported strategy)
                # is the causal record, counted once even though both Policy Outcome and Coverage
                # State inherit Unknown from it; it never degrades Execution Status (spec §141).
                unknown += sum(1 for f in evaluation["findings"] if "unknown_classification" in f)

    # Execution Status derives from the Unknown Classification recorded on the causal
    # policy-result evidence: only IncompleteObservation Unknowns are observation gaps.
    status_value = (
        ExecutionStatus.COMPLETE_WITH_GAPS
        if any(
            r.get("unknown_classification") == UnknownClassification.INCOMPLETE_OBSERVATION.value
            for r in results
        )
        else ExecutionStatus.COMPLETE
    )
    status = execution_status_payload(
        status_value,
        discovered=len(repositories),
        evaluated=evaluated,
        unknown=unknown,
    )
    _log(Severity.INFO, "evaluation.completed", {"evaluated": evaluated, "unknown": unknown})

    provenance = binding_provenance_payload(pairs)
    finding_evidence = findings_payload(findings)
    conflict_evidence = governance_findings_payload(governance_findings)
    result_evidence = policy_results_payload(results)
    items = [
        ("binding-provenance.json", evidence_item("binding_provenance", execution_id, provenance)),
        ("execution-status.json", evidence_item("execution_status", execution_id, status)),
        ("findings.json", evidence_item("findings", execution_id, finding_evidence)),
        (
            "governance-findings.json",
            evidence_item("governance_findings", execution_id, conflict_evidence),
        ),
        ("inventory.json", evidence_item("inventory", execution_id, inventory)),
        ("policy-results.json", evidence_item("policy_results", execution_id, result_evidence)),
    ]
    header = manifest_header(execution_id, evaluation_scope, evaluation_timestamp, engine_version)
    exec_dir = write_execution(store_root, execution_id, header, items)
    _log(Severity.INFO, "evidence.written", {"items": len(items)})

    return ExecutionResult(
        execution_id=execution_id,
        status=status_value,
        execution_dir=exec_dir,
    )
