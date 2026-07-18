"""Evidence-spine data shapes produced by ticket T0.

These builders construct the plain-dict content that flows through the integrity
contract. They deliberately hold only the evidence types the ungoverned execution
produces — Inventory, binding provenance, and Execution Status — plus the Execution
Manifest header. The finding schema and governance closed sets are introduced,
complete-with-degenerate-values, by the ticket that first produces findings (T1).
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
