"""AC 4 / Scenario S4 — the ungoverned execution.

Behavior is exercised through the two public seams, run_execution and derive_reports.
Report Derivation verifies stored evidence (digest before item hashes) before it
derives, so a clean store deriving successfully demonstrates the successful
verification path.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import ExecutionStatus
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


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

    # Report Derivation verifies the evidence (digest before item hashes) before it
    # derives; deriving without raising is the successful verification path.
    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # Observation of the declared scope completed: Complete, nothing evaluated.
    assert report["execution_status"] == "Complete"
    assert {k: report["accounting"][k] for k in ("discovered", "evaluated", "unknown")} == {
        "discovered": 2,
        "evaluated": 0,
        "unknown": 0,
    }

    # Every discovered repository is surfaced, and every (policy, repository) pair
    # records zero authoritative bindings and is ungoverned.
    ungoverned = report["ungoverned_pairs"]
    assert {p["repository_id"] for p in ungoverned} == {"octo-org/service-a", "octo-org/service-b"}
    assert all(p["governed"] is False and p["authoritative_binding_count"] == 0 for p in ungoverned)


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
