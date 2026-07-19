"""T4 — authority undeterminable (ADR-0015, A=1, U≥1).

Behavior through the two public seams (run_execution → derive_reports). One authoritative
binding definitely applies and a second authoritative binding's applicability is
CannotDetermine for the same (policy, repository) pair. Authority cannot be *established* —
the undetermined candidate is neither counted nor excluded — so the pair is a terminal
Unknown in both dimensions, an authority_undeterminable finding names both candidates and
the undetermined attribute, the one causal Unknown is classified IncompleteObservation,
Execution Status is CompleteWithGaps, no requirement set is evaluated, and the lone
definitely-Applicable binding is never silently selected. Expected values are independent
spec/ADR literals; internal structure is not asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_authority_undeterminable_applicable_plus_cannot_determine(
    tmp_path, undeterminable_mixed_bundle, undeterminable_mixed_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=undeterminable_mixed_bundle,
        estate_path=undeterminable_mixed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    policy_id, repository_id = "policy.baseline", "octo-org/service-h"

    # Terminal Unknown in both dimensions — the lone Applicable binding is NOT silently
    # selected (that would have produced Compliant/Covered).
    assert any(
        o["policy_id"] == policy_id
        and o["repository_id"] == repository_id
        and o["policy_outcome"] == "Unknown"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["policy_id"] == policy_id
        and c["repository_id"] == repository_id
        and c["coverage_state"] == "Unknown"
        for c in report["coverage"]["states"]
    )

    # An authority_undeterminable finding identifies both candidates and the undetermined attribute.
    finding = next(
        (
            f
            for f in report["findings"]
            if f["kind"] == "authority_undeterminable"
            and f["policy_id"] == policy_id
            and f["repository_id"] == repository_id
        ),
        None,
    )
    assert finding is not None
    assert len(finding["candidate_bindings"]) == 2
    assert any(
        "visibility" in c.get("undetermined_attributes", [])
        for c in finding["candidate_bindings"]
    )

    # Exactly one causal Unknown, classified IncompleteObservation (a Cannot-Determine gap).
    assert report["accounting"]["unknown"] == 1
    assert any(
        o["policy_id"] == policy_id
        and o["repository_id"] == repository_id
        and o["unknown_classification"] == "IncompleteObservation"
        for o in report["compliance"]["outcomes"]
    )

    # Observation was incomplete → CompleteWithGaps; no requirement set was evaluated.
    assert report["execution_status"] == "CompleteWithGaps"
    assert report["accounting"]["evaluated"] == 0
