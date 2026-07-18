"""T3 — scope combinator truth table: a determined operand forces the result.

Behavior through the two public seams (run_execution → derive_reports). An `any` scope
whose 'organization' operand is determined TRUE resolves Applicable even though its
'visibility' operand is Cannot Determine — a determined operand forces the combinator
result, so the Unknown operand is not decision-relevant and does not propagate. The pair
is governed and Compliant/Covered, and the Execution Status stays Complete: observation of
the declared scope was not left incomplete, because the Unknown never affected the outcome.
Expected values are independent spec/CONTEXT literals; internal structure is not asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def test_any_combinator_determined_operand_overrides_unknown(
    tmp_path, combinator_divergent_bundle, combinator_divergent_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=combinator_divergent_bundle,
        estate_path=combinator_divergent_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # A determined TRUE operand forces `any` → Applicable; the Cannot-Determine operand is
    # not decision-relevant, so there is no incomplete-observation gap.
    assert report["execution_status"] == "Complete"

    # The pair is governed and evaluated: Compliant in both independent dimensions.
    assert any(
        o["policy_id"] == "policy.baseline"
        and o["repository_id"] == "octo-org/service-d"
        and o["policy_outcome"] == "Compliant"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["policy_id"] == "policy.baseline"
        and c["repository_id"] == "octo-org/service-d"
        and c["coverage_state"] == "Covered"
        for c in report["coverage"]["states"]
    )


def test_all_combinator_false_operand_overrides_unknown(
    tmp_path, all_false_unknown_bundle, all_false_unknown_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=all_false_unknown_bundle,
        estate_path=all_false_unknown_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # A determined-FALSE operand forces `all` → NotApplicable; the Cannot-Determine operand
    # is not decision-relevant, so there is no incomplete-observation gap.
    assert report["execution_status"] == "Complete"

    # The binding does not apply → the pair is ungoverned.
    assert any(
        p["policy_id"] == "policy.baseline" and p["repository_id"] == "octo-org/service-e"
        for p in report["ungoverned_pairs"]
    )

    # No governed result is emitted for the pair — in particular, no Unknown in either dimension.
    assert not any(
        o["policy_id"] == "policy.baseline" and o["repository_id"] == "octo-org/service-e"
        for o in report["compliance"]["outcomes"]
    )
    assert not any(
        c["policy_id"] == "policy.baseline" and c["repository_id"] == "octo-org/service-e"
        for c in report["coverage"]["states"]
    )


def test_not_combinator_over_unknown_propagates_to_unknown(
    tmp_path, not_unknown_bundle, not_unknown_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=not_unknown_bundle,
        estate_path=not_unknown_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # not(Unknown) is Unknown: the negated operand is undeterminable, so applicability is
    # Unknown and observation of the declared scope was incomplete.
    assert report["execution_status"] == "CompleteWithGaps"

    # Accounting records exactly one Unknown pair, and no requirement evaluation occurred.
    assert report["accounting"]["unknown"] == 1
    assert report["accounting"]["evaluated"] == 0

    # Unknown propagates to both independent dimensions for the pair.
    assert any(
        o["policy_id"] == "policy.baseline"
        and o["repository_id"] == "octo-org/service-f"
        and o["policy_outcome"] == "Unknown"
        for o in report["compliance"]["outcomes"]
    )
    assert any(
        c["policy_id"] == "policy.baseline"
        and c["repository_id"] == "octo-org/service-f"
        and c["coverage_state"] == "Unknown"
        for c in report["coverage"]["states"]
    )
