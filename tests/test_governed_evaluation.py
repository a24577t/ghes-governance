"""T1 — smallest governed evaluation, through the two public seams.

One repository, one active authoritative Observe binding, one PredicateEvaluation
requirement that holds. The externally meaningful result is Policy Outcome Compliant and
Coverage State Covered for the governed pair, and the pair is not surfaced as ungoverned.
Expected values are independent spec/CONTEXT literals; internal finding structure is not
asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_governed_pair_is_compliant_and_covered(tmp_path, governed_bundle, governed_estate):
    store = tmp_path / "store"
    run_execution(
        bundle_path=governed_bundle,
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    assert any(
        o["policy_id"] == "policy.baseline"
        and o["repository_id"] == "octo-org/service-a"
        and o["policy_outcome"] == "Compliant"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["policy_id"] == "policy.baseline"
        and c["repository_id"] == "octo-org/service-a"
        and c["coverage_state"] == "Covered"
        for c in report["coverage"]["states"]
    )
    # A governed pair is not surfaced in the ungoverned category.
    assert report["ungoverned_pairs"] == []
