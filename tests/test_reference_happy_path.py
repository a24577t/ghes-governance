"""AC 1 / Scenario S1 — the reference happy path, through the two public seams.

The reference desired-state bundle (spec §157) is one composite policy with three addressable
requirements — one Compliant, one NonCompliant, and one Unknown-producing per ADR-0006's slice
clause — one scope expression, and one authoritative Observe binding, run against the reference
synthetic estate of two repositories. In a single execution it proves the load-bearing happy path
(AC 1, §161): a Complete Execution; correct per-requirement Technical / Interpretation / Requirement
outcomes for both governed pairs; the engine-owned aggregate Policy Outcome; a Coverage State of
Covered on the pair whose every *intended* requirement contributes Covered — the Unknown-producing
requirement is NotApplicable on the non-fork repository and drops out of coverage entirely
(ADR-0007:30, "coverage measures intended controls only"); a manifest listing every evidence item
with a verifying hash; and both the JSON and Markdown reports.

The Unknown-producing requirement is genuinely intended, and Unknown, on the fork repository, where
its declared Slice-2 strategy is unregistered — a GovernanceResult, so the Execution stays Complete
rather than degrading to CompleteWithGaps. Because that requirement is intended and Unknown there,
that pair's Coverage is Unknown, not Covered (ADR-0007:35, "otherwise any Unknown → Unknown"): the
two dimensions are asserted independently for each pair, keyed by stable (repository, policy)
identity.

Expected values are independent spec/CONTEXT literals; assertions run only through run_execution and
derive_reports (plus the frozen store contract used by the standing integrity tests).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.canonical import content_hash
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import EVIDENCE_DIR, MANIFEST_NAME, execution_dir

FIXTURES = Path(__file__).parent / "fixtures"
REFERENCE = FIXTURES / "reference"

POLICY = "policy.baseline"
COVERED_REPO = "octo-org/service-a"  # non-fork: every intended requirement contributes Covered
UNKNOWN_REPO = "octo-org/service-b"  # fork: the Unknown-producing requirement is intended here


def _run(store: Path) -> None:
    run_execution(
        bundle_path=REFERENCE / "bundle",
        estate_path=REFERENCE / "estate",
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def _findings(store: Path) -> dict[tuple[str, str], dict[str, Any]]:
    path = execution_dir(store, EXECUTION_ID) / EVIDENCE_DIR / "findings.json"
    return {
        (f["repository_id"], f["requirement_id"]): f
        for f in json.loads(path.read_bytes())["payload"]["findings"]
    }


def test_reference_bundle_happy_path(tmp_path: Path) -> None:
    store = tmp_path / "store"
    _run(store)
    bundle = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    report = bundle.json_report

    # (1) Execution Status Complete: the run's only Unknown is a GovernanceResult (an unregistered
    # strategy), never an observation gap, so observation of the declared scope completed.
    assert report["execution_status"] == "Complete"

    # Index each report dimension by stable pair identity (repository, policy). The compliance and
    # coverage sections carry exactly the two governed pairs — both repositories are governed by the
    # single authoritative binding, and neither section carries non-pair entries.
    compliance = {
        (o["repository_id"], o["policy_id"]): o["policy_outcome"]
        for o in report["compliance"]["outcomes"]
    }
    coverage = {
        (c["repository_id"], c["policy_id"]): c["coverage_state"]
        for c in report["coverage"]["states"]
    }
    expected_pairs = {(COVERED_REPO, POLICY), (UNKNOWN_REPO, POLICY)}
    assert set(compliance) == expected_pairs
    assert set(coverage) == expected_pairs

    findings = _findings(store)

    # --- octo-org/service-a (non-fork): every intended requirement contributes Covered ---
    assert compliance[(COVERED_REPO, POLICY)] == "NonCompliant"  # (5) aggregate Policy Outcome
    assert coverage[(COVERED_REPO, POLICY)] == "Covered"  # (6) Coverage State

    a_secret = findings[(COVERED_REPO, "req.secret-scanning")]
    assert a_secret["technical_outcome"] == "Compliant"
    assert a_secret["governance_interpretation"] == "None"
    assert a_secret["requirement_outcome"] == "Compliant"

    a_branch = findings[(COVERED_REPO, "req.branch-protection")]
    assert a_branch["technical_outcome"] == "NonCompliant"
    assert a_branch["governance_interpretation"] == "None"
    assert a_branch["requirement_outcome"] == "NonCompliant"

    # The third requirement is NotApplicable here (a non-fork repo): it carries an applicability and
    # a closed reason, no Technical/Requirement Outcome, and drops out of coverage (ADR-0007:30).
    a_fork = findings[(COVERED_REPO, "req.fork-network-controls")]
    assert a_fork["applicability"] == "NotApplicable"
    assert a_fork["not_applicable_reason"] == "RepositoryCharacteristic"
    assert "technical_outcome" not in a_fork
    assert "requirement_outcome" not in a_fork

    # --- octo-org/service-b (a fork): the Unknown-producing requirement is intended and Unknown ---
    assert compliance[(UNKNOWN_REPO, POLICY)] == "NonCompliant"  # aggregate Policy Outcome
    # Any intended requirement Unknown makes the pair's Coverage Unknown (ADR-0007:35), so this pair
    # is Covered's counterpart: NonCompliant compliance, Unknown coverage — the two never flattened.
    assert coverage[(UNKNOWN_REPO, POLICY)] == "Unknown"

    b_secret = findings[(UNKNOWN_REPO, "req.secret-scanning")]
    assert b_secret["technical_outcome"] == "Compliant"
    assert b_secret["governance_interpretation"] == "None"
    assert b_secret["requirement_outcome"] == "Compliant"

    b_branch = findings[(UNKNOWN_REPO, "req.branch-protection")]
    assert b_branch["technical_outcome"] == "NonCompliant"
    assert b_branch["governance_interpretation"] == "None"
    assert b_branch["requirement_outcome"] == "NonCompliant"

    # The third requirement is intended here (fork==true) and Unknown — its declared strategy is
    # unregistered, a GovernanceResult that keeps the Execution Complete.
    b_fork = findings[(UNKNOWN_REPO, "req.fork-network-controls")]
    assert b_fork["technical_outcome"] == "Unknown"
    assert b_fork["governance_interpretation"] == "None"
    assert b_fork["requirement_outcome"] == "Unknown"
    assert b_fork["unknown_classification"] == "GovernanceResult"

    # (7) The manifest lists every evidence item, each with a hash that verifies. derive_reports
    # already verified before deriving; re-verify explicitly and prove the manifest is complete
    # against what is actually on disk.
    exec_dir = execution_dir(store, EXECUTION_ID)
    manifest = json.loads((exec_dir / MANIFEST_NAME).read_bytes())
    listed = {entry["name"] for entry in manifest["items"]}
    on_disk = {p.name for p in (exec_dir / EVIDENCE_DIR).iterdir()}
    assert listed == on_disk, "the manifest lists exactly the evidence items on disk"
    for entry in manifest["items"]:
        item = json.loads((exec_dir / EVIDENCE_DIR / entry["name"]).read_bytes())
        assert entry["sha256"] == content_hash(item), f"{entry['name']} hash verifies"

    # (8) A machine-readable JSON report is produced.
    assert isinstance(report, dict) and report["schema_version"] == "1"

    # (9) A human-readable Markdown report is produced.
    assert isinstance(bundle.markdown, str)
    assert bundle.markdown.startswith("# Governance Report")
