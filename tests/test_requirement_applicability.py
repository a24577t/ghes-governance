"""AC 8b / Scenario S8 — per-requirement NotApplicable capability + aggregation precedence.

A requirement may declare an applicability precondition; when the repository does not satisfy it
the requirement is NotApplicable with a closed reason and is logically excluded — it never reaches
strategy dispatch or predicate evaluation, and it is aggregation-neutral for both Compliance and
Coverage (ADR-0006:34, ADR-0007:30). Reachable reasons: RepositoryCharacteristic and
PolicyPrecondition; PlatformCapabilityUnavailable ships dormant and is not author-declarable.
The reachable Policy Outcomes (Compliant / NonCompliant / Unknown, NonCompliant outranking
Unknown) are exercised as characterization. Asserted through the two public seams.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.errors import BundleError
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import execution_dir

FIXTURES = Path(__file__).parent / "fixtures"


def _run(store: Path, fixture: str) -> None:
    run_execution(
        bundle_path=FIXTURES / fixture / "bundle",
        estate_path=FIXTURES / fixture / "estate",
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def _report(store: Path, fixture: str) -> dict[str, Any]:
    _run(store, fixture)
    return derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report


def _req_findings(store: Path) -> dict[str, dict[str, Any]]:
    path = execution_dir(store, EXECUTION_ID) / "evidence" / "findings.json"
    return {f["requirement_id"]: f for f in json.loads(path.read_bytes())["payload"]["findings"]}


def _evidence(store: Path) -> dict[str, bytes]:
    root = execution_dir(store, EXECUTION_ID)
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


@pytest.mark.parametrize(
    "fixture,expected",
    [
        ("governed", "Compliant"),
        ("noncompliant", "NonCompliant"),
        ("unsupported-strategy", "Unknown"),
        ("noncompliant-outranks-unknown", "NonCompliant"),  # NonCompliant outranks Unknown
    ],
)
def test_reachable_policy_outcomes_and_precedence(
    tmp_path: Path, fixture: str, expected: str
) -> None:
    report = _report(tmp_path / "store", fixture)
    assert report["compliance"]["outcomes"][0]["policy_outcome"] == expected


def test_noncompliant_outranks_unknown_requires_both_requirements(tmp_path: Path) -> None:
    # Prove the *precedence*, not merely the aggregate: assert the requirement set actually contains
    # both the outranked Unknown requirement and the NonCompliant requirement, and that NonCompliant
    # wins. (The aggregate-only assertion would still pass if the Unknown were absent.)
    store = tmp_path / "store"
    report = _report(store, "noncompliant-outranks-unknown")
    outcomes = {f.get("requirement_outcome") for f in _req_findings(store).values()}
    assert "NonCompliant" in outcomes, "the NonCompliant requirement is present"
    assert "Unknown" in outcomes, "the outranked Unknown requirement is present"
    assert report["compliance"]["outcomes"][0]["policy_outcome"] == "NonCompliant"


def test_not_applicable_repository_characteristic_is_neutral(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report = _report(store, "na-repository-characteristic")
    req = _req_findings(store)

    na = req["req.fork-only"]
    assert na["applicability"] == "NotApplicable"
    assert na["not_applicable_reason"] == "RepositoryCharacteristic"
    # NotApplicable never reached strategy dispatch or predicate evaluation.
    assert "technical_outcome" not in na
    assert "requirement_outcome" not in na

    # The applicable requirement is Compliant. The NotApplicable requirement would be NonCompliant
    # if it were evaluated (its predicate fails on this repo) — so its neutrality, not a would-be
    # pass, is what keeps both dimensions clean: Policy Outcome Compliant, Coverage Covered.
    assert req["req.secret-scanning"]["requirement_outcome"] == "Compliant"
    assert report["compliance"]["outcomes"][0]["policy_outcome"] == "Compliant"
    assert report["coverage"]["states"][0]["coverage_state"] == "Covered"
    assert report["execution_status"] == "Complete"


def test_not_applicable_policy_precondition_is_neutral(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report = _report(store, "na-policy-precondition")
    req = _req_findings(store)

    na = req["req.public-only"]
    assert na["applicability"] == "NotApplicable"
    assert na["not_applicable_reason"] == "PolicyPrecondition"
    # NotApplicable never reached strategy dispatch or predicate evaluation.
    assert "technical_outcome" not in na
    assert "requirement_outcome" not in na

    # The applicable requirement is Compliant. The NotApplicable requirement would be NonCompliant
    # if it were evaluated — so its neutrality is what keeps the policy Compliant / Covered.
    assert req["req.secret-scanning"]["requirement_outcome"] == "Compliant"
    assert report["compliance"]["outcomes"][0]["policy_outcome"] == "Compliant"
    assert report["coverage"]["states"][0]["coverage_state"] == "Covered"


def test_dormant_reason_platform_capability_unavailable_is_not_declarable(tmp_path: Path) -> None:
    # PlatformCapabilityUnavailable ships in the closed set but is engine-derived (Slice 3); a
    # policy may not declare it here, so a NotApplicable resolution with it fails loud.
    with pytest.raises(BundleError):
        _run(tmp_path / "store", "na-dormant-reason")


def test_not_applicable_evidence_is_byte_deterministic(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    _run(a, "na-repository-characteristic")
    _run(b, "na-repository-characteristic")
    assert _evidence(a) == _evidence(b)


def test_not_applicable_reporting_is_byte_deterministic(tmp_path: Path) -> None:
    store = tmp_path / "store"
    _run(store, "na-policy-precondition")
    first = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    second = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    assert first.json_report == second.json_report
    assert first.markdown == second.markdown
