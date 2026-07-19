"""T4 — proven authority conflict: two definitely-Applicable authoritative bindings.

Behavior through the two public seams (run_execution → derive_reports). When two
authoritative bindings both definitely apply to one (policy, repository) pair, authority is
in proven conflict (ADR-0005, ADR-0013, ADR-0015): the pair's official Policy Outcome and
Coverage State are a terminal `Unknown`, an authority-conflict finding is emitted, the one
causal Unknown is classified `GovernanceResult`, Execution Status stays `Complete` (a
conflict is a governance finding, not an observation gap), and no requirement set is
evaluated. Expected values are independent spec/ADR literals; internal structure is not
asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_proven_authority_conflict_is_terminal_unknown_and_stays_complete(
    tmp_path, conflict_bundle, conflict_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=conflict_bundle,
        estate_path=conflict_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    policy_id, repository_id = "policy.baseline", "octo-org/service-g"

    # Terminal Unknown in both independent dimensions.
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

    # An authority-conflict finding is emitted for the pair.
    assert any(
        f["policy_id"] == policy_id
        and f["repository_id"] == repository_id
        and f["kind"] == "authority_conflict"
        for f in report["findings"]
    )

    # Exactly one causal Unknown, classified GovernanceResult (a conflict, not a gap).
    assert report["accounting"]["unknown"] == 1
    assert any(
        o["policy_id"] == policy_id
        and o["repository_id"] == repository_id
        and o["unknown_classification"] == "GovernanceResult"
        for o in report["compliance"]["outcomes"]
    )

    # Execution Status stays Complete; no requirement set is evaluated for the pair.
    assert report["execution_status"] == "Complete"
    assert report["accounting"]["evaluated"] == 0

    # The conflict pair is governed (not absent authority) — never surfaced as ungoverned.
    assert not any(
        p["policy_id"] == policy_id and p["repository_id"] == repository_id
        for p in report["ungoverned_pairs"]
    )
