"""The Execution boundary seam (ticket T0), ungoverned path.

One entry point takes an injected Evaluation Timestamp and execution identifier (the
engine never reads a wall clock) and produces, for an estate whose repositories match
no authoritative binding: an Inventory of every discovered repository, per-pair binding
provenance recording zero authoritative bindings, an Execution Status of Complete, an
Execution Manifest, and an external Execution Digest. No scope evaluation, predicate
evaluation, or aggregation occurs — those arrive in later tickets.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import ENGINE_VERSION
from .bundle import load_bundle, load_estate
from .enums import ExecutionStatus
from .errors import BundleError
from .model import (
    binding_provenance_payload,
    evidence_item,
    execution_status_payload,
    inventory_payload,
    manifest_header,
)
from .store import write_execution

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


def run_execution(
    *,
    bundle_path: str | Path,
    estate_path: str | Path,
    evaluation_scope: dict[str, Any],
    evaluation_timestamp: str,
    execution_id: str,
    store_root: str | Path,
    engine_version: str = ENGINE_VERSION,
) -> ExecutionResult:
    bundle = load_bundle(bundle_path)
    estate = load_estate(estate_path)

    authoritative = [b for b in bundle["bindings"] if b.get("evaluation_role") == "Authoritative"]
    if authoritative:
        raise BundleError(
            "ticket T0 runs only ungoverned executions; authoritative bindings require T1+"
        )

    repositories = estate["repositories"]
    inventory = inventory_payload([_inventory_record(repo) for repo in repositories])

    pairs: list[dict[str, Any]] = []
    for policy in bundle["policies"]:
        policy_id = policy.get("id")
        if policy_id is None:
            raise BundleError("bundle policy is missing 'id'")
        for repo in repositories:
            pairs.append(
                {
                    "policy_id": policy_id,
                    "repository_id": repo["id"],
                    "authoritative_binding_count": 0,
                    "governed": False,
                }
            )
    provenance = binding_provenance_payload(pairs)

    status = execution_status_payload(
        ExecutionStatus.COMPLETE,
        discovered=len(repositories),
        evaluated=0,
        unknown=0,
    )

    items = [
        ("binding-provenance.json", evidence_item("binding_provenance", execution_id, provenance)),
        ("execution-status.json", evidence_item("execution_status", execution_id, status)),
        ("inventory.json", evidence_item("inventory", execution_id, inventory)),
    ]
    header = manifest_header(execution_id, evaluation_scope, evaluation_timestamp, engine_version)
    exec_dir = write_execution(store_root, execution_id, header, items)

    return ExecutionResult(execution_id=execution_id, status=ExecutionStatus.COMPLETE, execution_dir=exec_dir)
