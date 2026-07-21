"""AC 11 / Scenario S11 — report traceability & regeneration (regeneration half only).

Reports are derived exclusively from stored Evidence and require no Execution: deriving twice
from the same store yields identical reports, deriving never mutates the evidence it reads, and
deriving from a store holding no Execution fails loudly rather than fabricating a report
(story 31 / S11).

Scope note — the citation clause is deliberately NOT asserted here. AC 11 also requires that
"every claim carries manifest/item citations." Whether the governing specification mandates
*per-claim* citations or is already satisfied by the existing report-level citation model is
ambiguous in the spec (``per claim`` / ``every claim carries`` in §155/§177 vs. "cite the
execution manifests (and thereby hashed evidence items)" in story 32/§26). Per the approved
AC 11 gate, that clause is held pending clarification and no interpretation is baked into a
test. Bound to the existing stable ``governed`` fixture; introduces no production change.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.errors import EvidenceUnreadableError
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports


def _run(store: Path, bundle: Path, estate: Path) -> None:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def _tree_digest(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_reports_derived_twice_are_identical(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    _run(store, governed_bundle, governed_estate)

    first = derive_reports(store_root=store, execution_id=EXECUTION_ID)
    second = derive_reports(store_root=store, execution_id=EXECUTION_ID)

    assert first.json_report == second.json_report
    assert first.markdown == second.markdown


def test_derivation_does_not_mutate_the_evidence_it_reads(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    _run(store, governed_bundle, governed_estate)
    before = _tree_digest(store / EXECUTION_ID)

    derive_reports(store_root=store, execution_id=EXECUTION_ID)

    # Evidence is the single source of truth; derivation reads it and must leave it untouched.
    assert _tree_digest(store / EXECUTION_ID) == before


def test_derivation_requires_no_execution_fails_loud_on_empty_store(tmp_path: Path) -> None:
    # A fresh store holds no Execution to derive from. Derivation reads stored evidence only
    # (it never runs an execution to fill the gap) and so must fail loudly rather than invent a
    # report — the regeneration contract's failure mode.
    with pytest.raises(EvidenceUnreadableError):
        derive_reports(store_root=tmp_path / "empty-store", execution_id=EXECUTION_ID)
