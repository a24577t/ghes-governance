"""The Execution boundary seam.

One entry point takes an injected Evaluation Timestamp and execution identifier (the
engine never reads a wall clock) and produces, for a synthetic estate: an Inventory of
every discovered repository, per-pair binding provenance, per-requirement findings and an
aggregated Policy Outcome / Coverage State for governed pairs, an Execution Status, an
Execution Manifest, and an external Execution Digest. A (policy, repository) pair with no
active authoritative binding is ungoverned — no outcome is invented for it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import ENGINE_VERSION
from .bundle import load_bundle, load_estate
from .enums import ExecutionStatus
from .errors import BundleError
from .evaluation import evaluate_policy, select_authoritative_binding
from .model import (
    binding_provenance_payload,
    evidence_item,
    execution_status_payload,
    findings_payload,
    inventory_payload,
    manifest_header,
    policy_results_payload,
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
    """Run an Execution and write its Evidence — the Execution boundary seam.

    Inventories every discovered repository unconditionally; for each (policy, repository)
    pair selects the single active authoritative Observe binding and, when one exists,
    evaluates the composite policy to per-requirement findings and an aggregated Policy
    Outcome and Coverage State; a pair with no binding is recorded as ungoverned with no
    invented outcome. Writes append-only Evidence, the Execution Manifest, and the external
    Execution Digest under ``store_root/<execution_id>/`` and returns an ``ExecutionResult``
    with status Complete. The Evaluation Timestamp and execution identifier are injected —
    no wall clock is read. Raises ``BundleError`` if a policy or repository lacks its id.
    """
    bundle = load_bundle(bundle_path)
    estate = load_estate(estate_path)

    repositories = estate["repositories"]
    inventory = inventory_payload([_inventory_record(repo) for repo in repositories])

    pairs: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    evaluated = 0

    for policy in bundle["policies"]:
        policy_id = policy.get("id")
        if policy_id is None:
            raise BundleError("bundle policy is missing 'id'")
        for repo in repositories:
            binding = select_authoritative_binding(
                bundle["bindings"], policy, repo, evaluation_timestamp
            )
            if binding is None:
                pairs.append(
                    {
                        "policy_id": policy_id,
                        "repository_id": repo["id"],
                        "authoritative_binding_count": 0,
                        "governed": False,
                    }
                )
                continue
            pairs.append(
                {
                    "policy_id": policy_id,
                    "repository_id": repo["id"],
                    "authoritative_binding_count": 1,
                    "governed": True,
                }
            )
            evaluation = evaluate_policy(policy, repo)
            findings.extend(evaluation["findings"])
            results.append(
                {
                    "policy_id": policy_id,
                    "repository_id": repo["id"],
                    "policy_outcome": evaluation["policy_outcome"],
                    "coverage_state": evaluation["coverage_state"],
                }
            )
            evaluated += 1

    status = execution_status_payload(
        ExecutionStatus.COMPLETE,
        discovered=len(repositories),
        evaluated=evaluated,
        unknown=0,
    )

    provenance = binding_provenance_payload(pairs)
    finding_evidence = findings_payload(findings)
    result_evidence = policy_results_payload(results)
    items = [
        ("binding-provenance.json", evidence_item("binding_provenance", execution_id, provenance)),
        ("execution-status.json", evidence_item("execution_status", execution_id, status)),
        ("findings.json", evidence_item("findings", execution_id, finding_evidence)),
        ("inventory.json", evidence_item("inventory", execution_id, inventory)),
        ("policy-results.json", evidence_item("policy_results", execution_id, result_evidence)),
    ]
    header = manifest_header(execution_id, evaluation_scope, evaluation_timestamp, engine_version)
    exec_dir = write_execution(store_root, execution_id, header, items)

    return ExecutionResult(
        execution_id=execution_id,
        status=ExecutionStatus.COMPLETE,
        execution_dir=exec_dir,
    )
