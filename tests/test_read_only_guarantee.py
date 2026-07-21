"""AC 14 / Scenario S14 — read-only guarantee.

The engine writes only beneath the evidence, log, and report directories it is given; the
desired-state bundle and synthetic estate directories are byte-unmodified after any
execution — verifiable, as the specification prescribes, by hashing them before and after.

Bound to the existing stable ``governed`` fixture — the richest delivered path (a Complete
Execution that writes real compliance/coverage evidence) — per the increment's constraint to
use existing fixtures rather than the future AC 1 reference fixture. A standing-invariant test
over the two seams; it introduces no production change.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution


def _tree_digest(root: Path) -> dict[str, str]:
    """Map each file's path (relative to ``root``) to the sha256 of its bytes.

    Equality of two such maps proves both content identity and path-set identity — no file
    added, removed, or modified.
    """
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_bundle_and_estate_unmodified_after_execution(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    before_bundle = _tree_digest(governed_bundle)
    before_estate = _tree_digest(governed_estate)
    assert before_bundle and before_estate  # the fixtures actually contain files to protect

    run_execution(
        bundle_path=governed_bundle,
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=tmp_path / "store",
    )

    assert _tree_digest(governed_bundle) == before_bundle
    assert _tree_digest(governed_estate) == before_estate


def test_execution_writes_beneath_the_given_store(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store_root = tmp_path / "store"
    run_execution(
        bundle_path=governed_bundle,
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store_root,
    )

    # Positive half of the guarantee: the evidence the engine produced landed beneath the
    # store directory it was given, not scattered elsewhere.
    execution_files = [p for p in (store_root / EXECUTION_ID).rglob("*") if p.is_file()]
    assert execution_files
