"""AC 6 / Scenario S6 — unknown / unsupported evaluation strategy.

A requirement whose ``(strategy identifier, version)`` is not registered yields Technical Outcome
``Unknown`` (Requirement Outcome ``Unknown``), a high-visibility governance-configuration finding
(``kind: unsupported_strategy``) naming the requested and available pairs, and — because the
unsupported selection is a determined governance verdict, not an observation gap — Execution Status
``Complete`` with the Unknown classified ``GovernanceResult`` (spec §141, §172; story 18;
CONTEXT.md Unknown Classification). Unknown identifier and unsupported version are one behaviour.

Asserted through the two public seams (``run_execution``, ``derive_reports``); bound to new
fixtures that declare an unregistered strategy (no existing fixture does).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import MANIFEST_NAME, execution_dir

FIXTURES = Path(__file__).parent / "fixtures"


def _run_and_report(store: Path, fixture: str) -> tuple[dict[str, Any], dict[str, Any]]:
    run_execution(
        bundle_path=FIXTURES / fixture / "bundle",
        estate_path=FIXTURES / fixture / "estate",
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    manifest = json.loads((execution_dir(store, EXECUTION_ID) / MANIFEST_NAME).read_bytes())
    return report, manifest


def _requirement_findings(store: Path) -> list[dict[str, Any]]:
    exec_dir = execution_dir(store, EXECUTION_ID)
    return json.loads((exec_dir / "evidence" / "findings.json").read_bytes())["payload"]["findings"]


def test_unknown_strategy_identifier_yields_unknown_and_config_finding(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report, _ = _run_and_report(store, "unsupported-strategy")

    # Execution completed (no raise) with status Complete.
    assert report["execution_status"] == "Complete"

    # The requirement's per-requirement finding is Unknown in both dimensions.
    req = _requirement_findings(store)
    assert len(req) == 1
    assert req[0]["technical_outcome"] == "Unknown"
    assert req[0]["requirement_outcome"] == "Unknown"

    # A high-visibility configuration finding names requested and available (strategy, version).
    strategy_findings = [f for f in report["findings"] if f["kind"] == "unsupported_strategy"]
    assert len(strategy_findings) == 1
    finding = strategy_findings[0]
    assert finding["requirement_id"] == "req.unknown-strategy"
    assert finding["requested"] == {"identifier": "NoSuchStrategy", "version": 1}
    assert {"identifier": "PredicateEvaluation", "version": 1} in finding["available"]


def test_unsupported_strategy_version_yields_unknown_and_config_finding(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report, _ = _run_and_report(store, "unsupported-strategy-version")

    assert report["execution_status"] == "Complete"
    strategy_findings = [f for f in report["findings"] if f["kind"] == "unsupported_strategy"]
    assert len(strategy_findings) == 1
    # Same behaviour as the unknown-identifier trigger; the version is what is unregistered.
    assert strategy_findings[0]["requested"] == {"identifier": "PredicateEvaluation", "version": 2}
    req = _requirement_findings(store)
    assert req[0]["technical_outcome"] == "Unknown"


def test_sibling_requirement_evaluates_normally(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report, _ = _run_and_report(store, "mixed-strategy")

    req = {f["requirement_id"]: f for f in _requirement_findings(store)}
    # The registered requirement evaluates normally to Compliant ...
    assert req["req.secret-scanning"]["requirement_outcome"] == "Compliant"
    # ... while the unregistered one is Unknown.
    assert req["req.unknown-strategy"]["requirement_outcome"] == "Unknown"

    # The pair aggregates to Unknown / Unknown (no NonCompliant; one Unknown).
    outcome = report["compliance"]["outcomes"][0]
    assert outcome["policy_outcome"] == "Unknown"
    coverage = report["coverage"]["states"][0]
    assert coverage["coverage_state"] == "Unknown"
    assert report["execution_status"] == "Complete"


def test_unknown_strategy_unknown_is_governance_result_not_a_gap(tmp_path: Path) -> None:
    store = tmp_path / "store"
    report, _ = _run_and_report(store, "unsupported-strategy")

    # A GovernanceResult Unknown never degrades the status to CompleteWithGaps.
    assert report["execution_status"] == "Complete"
    # The Unknown is counted once in the accounting, and the causal requirement record carries
    # its Unknown Classification (spec §141 / CONTEXT.md:159).
    assert report["accounting"]["unknown"] == 1
    req = _requirement_findings(store)
    assert req[0]["unknown_classification"] == "GovernanceResult"


def test_derivation_reports_config_finding_and_is_byte_identical(tmp_path: Path) -> None:
    store = tmp_path / "store"
    run_execution(
        bundle_path=FIXTURES / "unsupported-strategy" / "bundle",
        estate_path=FIXTURES / "unsupported-strategy" / "estate",
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    first = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    second = derive_reports(store_root=store, execution_id=EXECUTION_ID)

    # The config finding is surfaced with an AC 11 citation, and derivation is deterministic.
    finding = [f for f in first.json_report["findings"] if f["kind"] == "unsupported_strategy"][0]
    assert finding["citations"], "the report finding carries claim-scoped citations"
    assert first.json_report == second.json_report
    assert first.markdown == second.markdown
