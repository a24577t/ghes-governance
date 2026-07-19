"""T2 — scope resolution under the three-result contract, and Unknown propagation.

Behavior through the two public seams (run_execution → derive_reports). A scope attribute
that the provider cannot determine — and that the scope result depends on — yields Unknown
applicability, which propagates to an Unknown Policy Outcome and Coverage State, and the
Execution Status is CompleteWithGaps (observation of the declared scope was incomplete).
Expected values are independent spec/CONTEXT literals; internal structure is not asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_cannot_determine_scope_attribute_propagates_to_unknown(
    tmp_path, unknown_scope_bundle, unknown_scope_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=unknown_scope_bundle,
        estate_path=unknown_scope_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # Observation of the declared scope was incomplete → CompleteWithGaps.
    assert report["execution_status"] == "CompleteWithGaps"

    # Unknown applicability propagates to Unknown in both independent dimensions.
    assert any(
        o["policy_id"] == "policy.baseline"
        and o["repository_id"] == "octo-org/service-c"
        and o["policy_outcome"] == "Unknown"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["policy_id"] == "policy.baseline"
        and c["repository_id"] == "octo-org/service-c"
        and c["coverage_state"] == "Unknown"
        for c in report["coverage"]["states"]
    )

    # The one causal Unknown is classified IncompleteObservation; no requirement set is
    # evaluated; no authority finding is emitted (a single undetermined candidate); and the
    # pair is governed — undeterminable applicability, never surfaced as absent authority.
    assert report["accounting"]["evaluated"] == 0
    assert any(
        o["policy_id"] == "policy.baseline"
        and o["repository_id"] == "octo-org/service-c"
        and o["unknown_classification"] == "IncompleteObservation"
        for o in report["compliance"]["outcomes"]
    )
    assert report["findings"] == []
    assert not any(
        p["policy_id"] == "policy.baseline" and p["repository_id"] == "octo-org/service-c"
        for p in report["ungoverned_pairs"]
    )
