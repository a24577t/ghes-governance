"""T4 (option B) — proven authority conflict across DIVERGENT policy versions.

Behavior through the two public seams (run_execution → derive_reports). Two active
authoritative Observe bindings both definitely apply to one (policy, repository) pair but
carry divergent policy versions and requirement sets — v1 {R1, R2} and v2 {R1, R3}
(ADR-0013, ADR-0015; Slice-1 spec AC 5 / §147). The contract:

  * the OFFICIAL pair stays a terminal Policy Outcome / Coverage State ``Unknown`` classified
    ``GovernanceResult``, Execution Status stays ``Complete``, zero OFFICIAL requirement
    evaluations occur, and the pair is governed (never surfaced as ungoverned);
  * each conflicting binding is nonetheless evaluated as EXPLANATORY-ONLY evidence under its
    own version's requirement set (v1 evaluates {R1, R2}; v2 evaluates {R1, R3});
  * the authority-conflict finding records both binding identities, their policy versions,
    each requirement set, and the explicit shared / only-in-each requirement-set divergence,
    and records that no binding determined the official outcomes;
  * NO synthesized union {R1, R2, R3} requirement set and NO official aggregate is produced
    anywhere — ADR-0013's no-synthesis rule is exercised, not merely stated.

Expected values are independent spec/ADR literals; internal structure is not asserted.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports

POLICY_ID = "policy.baseline"
REPO_ID = "octo-org/service-g"
R1 = "req.secret-scanning"    # shared by both versions
R2 = "req.dependency-review"  # only in version 1
R3 = "req.branch-protection"  # only in version 2


def test_divergent_version_conflict_evaluates_explanatory_only_without_synthesis(
    tmp_path, conflict_divergent_bundle, conflict_divergent_estate
):
    store = tmp_path / "store"
    run_execution(
        bundle_path=conflict_divergent_bundle,
        estate_path=conflict_divergent_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # --- The single authority_conflict finding for the pair ----------------------------------
    conflicts = [
        f
        for f in report["findings"]
        if f["kind"] == "authority_conflict"
        and f["policy_id"] == POLICY_ID
        and f["repository_id"] == REPO_ID
    ]
    assert len(conflicts) == 1
    finding = conflicts[0]

    # Records BOTH binding identities (their divergent scopes) and BOTH policy versions.
    by_version = {b["policy_version"]: b for b in finding["conflicting_bindings"]}
    assert set(by_version) == {1, 2}
    assert by_version[1]["scope"] == {
        "equals": {"attribute": "organization", "value": "octo-org"}
    }
    assert by_version[2]["scope"] == {"equals": {"attribute": "name", "value": "service-g"}}

    # Records each binding's own requirement set.
    assert set(by_version[1]["requirement_ids"]) == {R1, R2}
    assert set(by_version[2]["requirement_ids"]) == {R1, R3}

    # Records the explicit shared / only-in-each requirement-set divergence.
    divergence = finding["requirement_set_divergence"]
    assert set(divergence["shared"]) == {R1}
    only_in = {d["policy_version"]: set(d["requirement_ids"]) for d in divergence["only_in"]}
    assert only_in == {1: {R2}, 2: {R3}}

    # Records that no binding determined the official requirement outcomes.
    assert finding["official_outcomes_determined"] is False

    # --- Explanatory-only per-binding requirement evaluations for BOTH versions --------------
    # Each conflicting binding is evaluated under its own version's requirement set and recorded
    # as explanatory evidence — v1 over {R1, R2}, v2 over {R1, R3}, with divergent outcomes.
    expl_v1 = {
        r["requirement_id"]: r["requirement_outcome"]
        for r in by_version[1]["explanatory_requirements"]
    }
    expl_v2 = {
        r["requirement_id"]: r["requirement_outcome"]
        for r in by_version[2]["explanatory_requirements"]
    }
    assert expl_v1 == {R1: "Compliant", R2: "Compliant"}
    assert expl_v2 == {R1: "Compliant", R3: "NonCompliant"}

    # --- OFFICIAL pair: terminal Unknown in both dimensions, no official evaluation -----------
    official_compliance = [
        o
        for o in report["compliance"]["outcomes"]
        if o["policy_id"] == POLICY_ID and o["repository_id"] == REPO_ID
    ]
    assert len(official_compliance) == 1
    assert official_compliance[0]["policy_outcome"] == "Unknown"
    assert official_compliance[0]["unknown_classification"] == "GovernanceResult"

    official_coverage = [
        c
        for c in report["coverage"]["states"]
        if c["policy_id"] == POLICY_ID and c["repository_id"] == REPO_ID
    ]
    assert len(official_coverage) == 1
    assert official_coverage[0]["coverage_state"] == "Unknown"

    assert report["execution_status"] == "Complete"
    assert report["accounting"]["evaluated"] == 0  # zero OFFICIAL requirement evaluations
    assert report["accounting"]["unknown"] == 1
    assert not any(  # governed (authority present, if conflicting) — never ungoverned
        p["policy_id"] == POLICY_ID and p["repository_id"] == REPO_ID
        for p in report["ungoverned_pairs"]
    )

    # --- No synthesized union {R1, R2, R3} requirement set, and no official aggregate ---------
    # Neither binding carries the union, the divergence is never merged into one set, and the
    # official pair stayed Unknown rather than adopting v2's NonCompliant — which a synthesized
    # {R1, R2, R3} evaluation would have produced.
    union = {R1, R2, R3}
    assert set(by_version[1]["requirement_ids"]) != union
    assert set(by_version[2]["requirement_ids"]) != union
    assert official_compliance[0]["policy_outcome"] != "NonCompliant"
