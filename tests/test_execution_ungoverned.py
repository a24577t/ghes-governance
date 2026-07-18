"""AC 4 / Scenario S4 — the ungoverned execution, plus the successful verification path.

Behavior is exercised only through the two public seams. ``read_verified_execution``
performs the T0 verification (digest before item hashes); a clean store verifies, which
is the successful path T0 demonstrates.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import ExecutionStatus
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import read_verified_execution


def test_ungoverned_execution_completes_with_verified_evidence(
    tmp_path, ungoverned_bundle, ungoverned_estate
):
    store = tmp_path / "store"

    result = run_execution(
        bundle_path=ungoverned_bundle,
        estate_path=ungoverned_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    assert result.status is ExecutionStatus.COMPLETE

    # Successful verification path: a clean store verifies (digest then item hashes).
    manifest, items = read_verified_execution(store, EXECUTION_ID)

    # Every discovered repository is entered into the Inventory unconditionally.
    repos = items["inventory"]["payload"]["repositories"]
    assert {r["id"] for r in repos} == {"octo-org/service-a", "octo-org/service-b"}

    # Each (policy, repository) pair records zero authoritative bindings and is ungoverned.
    pairs = items["binding_provenance"]["payload"]["pairs"]
    assert pairs
    assert all(p["governed"] is False and p["authoritative_binding_count"] == 0 for p in pairs)

    # Observation of the declared scope completed: Complete, nothing evaluated.
    status = items["execution_status"]["payload"]
    assert status["status"] == "Complete"
    assert status["accounting"] == {"discovered": 2, "evaluated": 0, "unknown": 0}


def test_ungoverned_reports_invent_no_governed_outcome(
    tmp_path, ungoverned_bundle, ungoverned_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=ungoverned_bundle,
        estate_path=ungoverned_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    payload = report.json_report

    # Compliance and Coverage are separate dimensions, both empty for an ungoverned run.
    assert payload["compliance"]["outcomes"] == []
    assert payload["coverage"]["states"] == []

    # One policy across two repositories → two ungoverned pairs, surfaced as their own category.
    assert len(payload["ungoverned_pairs"]) == 2
    assert "Ungoverned pairs (2)" in report.markdown

    # Every report carries evidence citations back to the manifest.
    assert payload["citations"]["execution_digest"]
    assert payload["citations"]["manifest_items"]
