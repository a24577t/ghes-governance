"""AC 7 / S7 — half-open effective-period boundary contract (characterization).

Behavior through the two public seams (run_execution → derive_reports). The effective period
is half-open [effective_start, effective_end): at effective_start the binding is active; at
effective_end it is inactive; before effective_start (future-dated) it is inactive. One
authoritative binding per repository, differing only in effective period relative to the
fixed evaluation timestamp, exercises all three boundaries in a single execution. This
characterizes activation behavior implemented since T1; it adds no production behavior.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP  # TIMESTAMP == "2026-01-01T00:00:00Z"

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_half_open_effective_period_boundary_contract(
    tmp_path, effective_period_bundle, effective_period_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=effective_period_bundle,
        estate_path=effective_period_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    pol = "policy.baseline"
    governed = {(o["policy_id"], o["repository_id"]) for o in report["compliance"]["outcomes"]}
    ungoverned = {(p["policy_id"], p["repository_id"]) for p in report["ungoverned_pairs"]}

    # timestamp == effective_start → active → the pair is governed (Compliant/Covered).
    assert (pol, "octo-org/at-start") in governed
    assert (pol, "octo-org/at-start") not in ungoverned
    assert any(
        o["repository_id"] == "octo-org/at-start" and o["policy_outcome"] == "Compliant"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["repository_id"] == "octo-org/at-start" and c["coverage_state"] == "Covered"
        for c in report["coverage"]["states"]
    )

    # timestamp == effective_end → inactive (end exclusive) → the pair is ungoverned.
    assert (pol, "octo-org/at-end") in ungoverned
    assert (pol, "octo-org/at-end") not in governed

    # timestamp precedes effective_start (future-dated) → inactive → the pair is ungoverned.
    assert (pol, "octo-org/future") in ungoverned
    assert (pol, "octo-org/future") not in governed

    # The two inactive-binding pairs invent no outcome and record zero authoritative bindings;
    # observation completed with exactly one repository evaluated.
    assert all(
        p["governed"] is False and p["authoritative_binding_count"] == 0
        for p in report["ungoverned_pairs"]
        if p["repository_id"] in {"octo-org/at-end", "octo-org/future"}
    )
    assert report["execution_status"] == "Complete"
    assert report["accounting"] == {"discovered": 3, "evaluated": 1, "unknown": 0}
