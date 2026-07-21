"""AC 9 — physical Operational Log / evidence-store separation (configuration validation).

The Operational Log and Authoritative Evidence are distinct data classes (ADR-0009) and must
occupy disjoint filesystem roots, so an operational event can never land inside the evidence
store. ``run_execution`` rejects an overlapping ``(store_root, log_root)`` configuration — the two
resolved roots equal, the log beneath the store, or the store beneath the log — with a
``ConfigurationError`` raised **before** any execution right, Execution, Evidence, or operational
event. Sibling roots remain accepted and preserve the AC 9 invariants. An explicitly supplied
``log_root`` is never silently relocated. Asserted at the ``run_execution`` seam.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import ExecutionStatus, Severity
from ghes_governance.errors import ConfigurationError
from ghes_governance.execution import run_execution
from ghes_governance.store import execution_dir


def _run(store: Path, log_root: Path, bundle: Path, estate: Path) -> object:
    return run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
        log_root=log_root,
        log_level=Severity.DEBUG,
    )


def _wrote_nothing(store: Path, *roots: Path) -> bool:
    """No Execution evidence and no operational-log artifact anywhere under the given roots."""
    if execution_dir(store, EXECUTION_ID).exists():
        return False
    for root in (store, *roots):
        if root.exists() and any(p.name == "operational.log" for p in root.rglob("*")):
            return False
    return True


def test_log_root_equal_to_store_root_is_rejected(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    with pytest.raises(ConfigurationError):
        _run(store, store, governed_bundle, governed_estate)
    assert _wrote_nothing(store, store)


def test_log_root_beneath_store_root_is_rejected(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    log_root = store / "logs"  # nested inside the evidence store
    with pytest.raises(ConfigurationError):
        _run(store, log_root, governed_bundle, governed_estate)
    assert _wrote_nothing(store, log_root)


def test_store_root_beneath_log_root_is_rejected(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    log_root = tmp_path / "logs"
    store = log_root / "store"  # evidence store nested inside the log root
    with pytest.raises(ConfigurationError):
        _run(store, log_root, governed_bundle, governed_estate)
    assert _wrote_nothing(store, log_root)


def test_sibling_roots_are_accepted_and_preserve_ac9_invariants(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    log_root = tmp_path / "operational-log"  # disjoint sibling
    result = _run(store, log_root, governed_bundle, governed_estate)

    assert result.status is ExecutionStatus.COMPLETE
    exec_dir = execution_dir(store, EXECUTION_ID)
    # Evidence under the store; operational events under the disjoint log root.
    assert exec_dir.exists()
    assert (log_root / "operational.log").exists()
    # The log stays outside the evidence store (AC 9 physical separation preserved).
    assert store not in log_root.parents
    assert not any("operational" in p.name.lower() for p in exec_dir.rglob("*"))
