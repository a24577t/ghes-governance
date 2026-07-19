"""Evidence data shapes.

These builders construct the plain-dict content that flows through the integrity
contract: Inventory, binding provenance, Execution Status, per-requirement findings, and
per-pair policy results, plus the Execution Manifest header. Findings and policy results
were introduced with the first governed evaluation (T1).
"""

from __future__ import annotations

from typing import Any

from .enums import ExecutionStatus, SensitivityClassification

SCHEMA_VERSION = "1"


def evidence_item(
    kind: str,
    execution_id: str,
    payload: dict[str, Any],
    sensitivity: SensitivityClassification = SensitivityClassification.PUBLIC,
) -> dict[str, Any]:
    """Wrap a payload as a schema-versioned, sensitivity-classified evidence item."""
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": kind,
        "sensitivity": sensitivity.value,
        "execution_id": execution_id,
        "payload": payload,
    }


def manifest_header(
    execution_id: str,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    engine_version: str,
) -> dict[str, Any]:
    """Identity fields of the Execution Manifest; the item list is appended by the store."""
    return {
        "schema_version": SCHEMA_VERSION,
        "execution_id": execution_id,
        "evaluation_scope": evaluation_scope,
        "evaluation_timestamp": evaluation_timestamp,
        "engine_version": engine_version,
    }


def inventory_payload(repositories: list[dict[str, Any]]) -> dict[str, Any]:
    """Every discovered repository, entered unconditionally, sorted by identifier."""
    return {"repositories": sorted(repositories, key=lambda r: r["id"])}


def binding_provenance_payload(pairs: list[dict[str, Any]]) -> dict[str, Any]:
    """Per (policy, repository) pair authority provenance.

    In the ungoverned execution every pair records zero authoritative bindings and is
    therefore not governed — surfaced through provenance and the reports' ungoverned
    category, never as an invented Policy Outcome or Coverage State.
    """
    return {
        "pairs": sorted(pairs, key=lambda p: (p["policy_id"], p["repository_id"]))
    }


def execution_status_payload(
    status: ExecutionStatus,
    discovered: int,
    evaluated: int,
    unknown: int,
) -> dict[str, Any]:
    """Closed Execution Status with discovered / evaluated / Unknown accounting."""
    return {
        "status": status.value,
        "accounting": {
            "discovered": discovered,
            "evaluated": evaluated,
            "unknown": unknown,
        },
    }


def findings_payload(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-requirement findings for governed pairs, sorted for deterministic evidence."""
    return {
        "findings": sorted(
            findings, key=lambda f: (f["policy_id"], f["repository_id"], f["requirement_id"])
        )
    }


def policy_results_payload(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Per governed (policy, repository) pair: aggregated Policy Outcome and Coverage State."""
    return {"results": sorted(results, key=lambda r: (r["policy_id"], r["repository_id"]))}


def governance_findings_payload(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Governance-configuration findings (e.g. authority conflict), sorted deterministically."""
    return {
        "findings": sorted(
            findings, key=lambda f: (f["kind"], f["policy_id"], f["repository_id"])
        )
    }


def bundle_validation_payload(errors: list[dict[str, Any]]) -> dict[str, Any]:
    """Configuration evidence for a Failed Execution (T5): the bundle validation errors and the
    offending content, sorted deterministically (AC 12). No authoritative compliance or
    coverage results accompany a Failed Execution."""
    return {
        "errors": sorted(errors, key=lambda e: (e["code"], e["artifact"], e["detail"]))
    }
