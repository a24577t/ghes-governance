"""AC 11 / Scenario S11 — claim-scoped report traceability (citation clause).

Every emitted report claim carries manifest/item citations to the evidence that *materially*
supports it, derived from the verified Execution Manifest, while the report-level citations
index is retained. Support is not 1:1: a governed Policy Outcome / Coverage State aggregates
the per-requirement ``findings`` (ADR-0006/0007), so it cites both ``policy_results`` and
``findings``; a terminal authority Unknown evaluates no requirement and is produced by authority
selection, so it cites ``policy_results`` and ``binding_provenance`` (ADR-0013/0015). Citations
are present-aware — a Failed Execution omits the discovery/evaluation items, so its accounting
cites only ``execution_status``.

Bound to existing stable fixtures; asserted through the two public seams. Citation values are
derived from the verified manifest that Report Derivation already reads — no new evidence item,
no change to the integrity chain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import MANIFEST_NAME, execution_dir

FIXTURES = Path(__file__).parent / "fixtures"


def _run_and_report(store: Path, bundle: Path, estate: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    manifest = json.loads((execution_dir(store, EXECUTION_ID) / MANIFEST_NAME).read_bytes())
    return report, manifest


def _claims(report: dict[str, Any]) -> Iterator[tuple[str, dict[str, Any]]]:
    """Every emitted claim object in the report, tagged with its claim type."""
    for o in report["compliance"]["outcomes"]:
        yield "compliance", o
    for c in report["coverage"]["states"]:
        yield "coverage", c
    for f in report["findings"]:
        yield "finding", f
    for e in report["bundle_validation"]:
        yield "bundle_validation", e
    for u in report["ungoverned_pairs"]:
        yield "ungoverned", u
    yield "accounting", report["accounting"]


# (bundle fixture, estate fixture) → the uniform expected supporting kinds per claim type for
# that fixture. Fixtures are chosen so each claim type is uniform within a run (all governed, or
# all Unknown), avoiding per-pair branching in the test. Expectations are intersected with the
# kinds actually present in the manifest.
CASES: list[tuple[str, str, dict[str, set[str]]]] = [
    (
        "governed",
        "governed",
        {
            "compliance": {"policy_results", "findings"},
            "coverage": {"policy_results", "findings"},
            "accounting": {"execution_status", "inventory", "policy_results"},
        },
    ),
    (
        "conflict-proven",
        "conflict-proven",
        {
            "compliance": {"policy_results", "binding_provenance"},
            "coverage": {"policy_results", "binding_provenance"},
            "finding": {"governance_findings", "binding_provenance"},
            "accounting": {"execution_status", "inventory", "policy_results"},
        },
    ),
    (
        "ungoverned",
        "ungoverned",
        {
            "ungoverned": {"binding_provenance", "inventory"},
            "accounting": {"execution_status", "inventory", "policy_results"},
        },
    ),
    (
        "invalid-malformed-policy",
        "governed",  # Failed executions ignore the estate; any valid estate path serves
        {
            "bundle_validation": {"bundle_validation"},
            "accounting": {"execution_status"},  # inventory/policy_results absent on a Failed run
        },
    ),
]


@pytest.mark.parametrize("bundle_fix,estate_fix,expected", CASES)
def test_every_claim_carries_valid_citations(
    tmp_path: Path, bundle_fix: str, estate_fix: str, expected: dict[str, set[str]]
) -> None:
    store = tmp_path / "store"
    report, manifest = _run_and_report(
        store, FIXTURES / bundle_fix / "bundle", FIXTURES / estate_fix / "estate"
    )
    by_name = {e["name"]: e for e in manifest["items"]}
    present = {e["kind"] for e in manifest["items"]}

    seen: set[str] = set()
    for claim_type, claim in _claims(report):
        seen.add(claim_type)
        cites = claim.get("citations")
        # (1) every emitted claim carries at least one citation
        assert cites, f"{claim_type} claim carries no citations: {claim}"
        cited_kinds: set[str] = set()
        for c in cites:
            # (2) cited item names exist in the verified manifest
            assert c["item"] in by_name, f"{claim_type} cites unknown item {c['item']!r}"
            # (3) cited hashes match the corresponding manifest entry
            assert c["sha256"] == by_name[c["item"]]["sha256"]
            # kind label is internally consistent with the manifest entry it names
            assert c["kind"] == by_name[c["item"]]["kind"]
            cited_kinds.add(c["kind"])
        # (4) citations reference exactly the correct evidence kinds for the claim type
        #     (present-aware: only kinds actually in this Execution's manifest)
        assert cited_kinds == (expected[claim_type] & present)

    # the fixture actually exercised the claim types we wrote expectations for
    assert seen == set(expected)


def test_report_level_citation_index_is_retained(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    report, manifest = _run_and_report(store, governed_bundle, governed_estate)
    assert set(report["citations"]) == {"execution_digest", "manifest_items"}
    assert report["citations"]["manifest_items"] == manifest["items"]


def test_deriving_twice_is_byte_identical_with_citations(
    tmp_path: Path, conflict_bundle: Path, conflict_estate: Path
) -> None:
    store = tmp_path / "store"
    run_execution(
        bundle_path=conflict_bundle,
        estate_path=conflict_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    first = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    second = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    assert first.json_report == second.json_report
    assert first.markdown == second.markdown
