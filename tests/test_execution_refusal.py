"""T6 · AC 15 — Execution Identifier reuse is refused (external-seam-only).

Demonstrates the Execution-boundary invariant for identifier reuse: a second request using
an Execution Identifier already present in the target evidence store is refused *before* any
Execution is created. It produces no Execution, no Execution Status, and no new authoritative
Evidence / Manifest / Digest; it leaves the existing execution byte-unmodified and still
derivable; and it records exactly one structured ERROR refusal event in the Operational Log
(ADR-0009's separate data class, never Evidence). Behaviour is asserted only at the two public
seams (run_execution, derive_reports) — no internal helper, store predicate, lock primitive, or
log writer is imported. (spec: Execution Lifecycle §91-105, AC 15 §181; ADR-0009.)
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import ExecutionStatus
from ghes_governance.errors import ExecutionRefusedError
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports

FIXTURES = Path(__file__).parent / "fixtures"


def _snapshot(root: Path) -> dict[str, str]:
    """Relative path -> SHA-256 of every file under ``root`` (hash source independent of the engine)."""
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def _read_events(log_root: Path) -> list[dict[str, Any]]:
    """Every JSON operational-log record found under ``log_root`` (one JSON object per line)."""
    events: list[dict[str, Any]] = []
    if not log_root.exists():
        return events
    for path in sorted(log_root.rglob("*")):
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped:
                    events.append(json.loads(stripped))
    return events


def _run(store: Path, log_root: Path, *, bundle: Path, estate: Path) -> Any:
    return run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
        log_root=log_root,
    )


def test_reuse_is_refused_and_leaves_existing_execution_untouched(
    tmp_path, governed_bundle, governed_estate
):
    store = tmp_path / "store"
    log_root = tmp_path / "operational-log"

    # First request establishes the Execution Identifier.
    _run(store, log_root, bundle=governed_bundle, estate=governed_estate)
    before = _snapshot(store / EXECUTION_ID)
    assert before, "the first execution should have written evidence"
    report_before = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report

    # Second request reuses the identifier — refused before an Execution exists.
    with pytest.raises(ExecutionRefusedError):
        _run(store, log_root, bundle=governed_bundle, estate=governed_estate)

    # No observable side effect below the Execution boundary: the existing execution is
    # byte-identical (no second Execution; no new Status / Evidence / Manifest / Digest) ...
    assert _snapshot(store / EXECUTION_ID) == before
    assert [p.name for p in store.iterdir()] == [EXECUTION_ID], "no second execution directory"
    # ... and remains derivable with unchanged results.
    after_report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    assert after_report == report_before

    # The single required effect of the refusal, outside the boundary: one structured ERROR refusal
    # event. (The first, successful execution also emits execution-time operational events to the
    # same log — a separate data class; refusal events are the ones carrying a refusal ``category``.)
    refusals = [e for e in _read_events(log_root) if "category" in e]
    assert len(refusals) == 1
    event = refusals[0]
    assert event["severity"] == "ERROR"
    assert event["category"] == "identifier-reuse"
    assert event["attempted_execution_id"] == EXECUTION_ID
    assert event["existing_execution_id"] == EXECUTION_ID
    assert event["requested_scope"] == SCOPE
    assert event["timestamp"] == TIMESTAMP
    assert event["engine_version"]
    assert event["reason"]
    assert event["sensitivity"] == "Public"
    assert event["correlation_id"]
    # Never shaped as an Evidence item / Finding / Manifest / Execution.
    assert "payload" not in event
    assert "kind" not in event
    assert "schema_version" not in event


def test_reuse_refusal_correlation_identifier_is_deterministic(
    tmp_path, governed_bundle, governed_estate
):
    store = tmp_path / "store"
    log_root = tmp_path / "operational-log"
    _run(store, log_root, bundle=governed_bundle, estate=governed_estate)

    for _ in range(2):
        with pytest.raises(ExecutionRefusedError):
            _run(store, log_root, bundle=governed_bundle, estate=governed_estate)

    # Two refusal events (execution-time events from the first successful run share the log but
    # carry no refusal ``category``).
    refusals = [e for e in _read_events(log_root) if "category" in e]
    assert len(refusals) == 2
    # Deterministically derived from the request envelope: identical across identical requests,
    # with no wall-clock or RNG dependency.
    assert refusals[0]["correlation_id"] == refusals[1]["correlation_id"]


# --- AC 13: exclusive execution rights unavailable -------------------------------------------
#
# Contention convention (approved Shape): the execution-control directory is mechanism-neutral;
# a NON-EMPTY control directory means exclusive execution rights are unavailable. A seam-only
# test arranges contention by placing any arbitrary, test-owned entry in the control directory.
# A refusal leaves that occupancy unchanged; a completed execution leaves the directory empty.


def _control_entries(control: Path) -> set[str]:
    """Every top-level entry name in the control directory (files and directories)."""
    return {p.name for p in control.iterdir()}


def test_rights_unavailable_is_refused_without_touching_occupancy(
    tmp_path, governed_bundle, governed_estate
):
    store = tmp_path / "store"
    log_root = tmp_path / "operational-log"
    control = tmp_path / "execution-control"
    control.mkdir()
    # An arbitrary, test-owned occupant makes the control directory non-empty => rights unavailable.
    occupant = control / "held-by-another-execution"
    occupant.write_text("test-owned reservation", encoding="utf-8")
    occupancy_before = _snapshot(control)

    with pytest.raises(ExecutionRefusedError):
        run_execution(
            bundle_path=governed_bundle,
            estate_path=governed_estate,
            evaluation_scope=SCOPE,
            evaluation_timestamp=TIMESTAMP,
            execution_id=EXECUTION_ID,
            store_root=store,
            log_root=log_root,
            control_root=control,
        )

    # No observable side effect below the Execution boundary: no Execution directory, Evidence,
    # Manifest, or Digest — no partial or interleaved evidence anywhere in the target store.
    assert not store.exists() or list(store.iterdir()) == []

    # The pre-existing occupancy is byte-for-byte and structurally unchanged (the engine neither
    # altered the occupant nor left a reservation of its own behind).
    assert _snapshot(control) == occupancy_before
    assert _control_entries(control) == {"held-by-another-execution"}
    assert occupant.read_text(encoding="utf-8") == "test-owned reservation"

    # Exactly one structured ERROR rights-unavailable refusal event.
    events = _read_events(log_root)
    assert len(events) == 1
    event = events[0]
    assert event["severity"] == "ERROR"
    assert event["category"] == "rights-unavailable"
    assert event["attempted_execution_id"] == EXECUTION_ID
    assert event["requested_scope"] == SCOPE
    assert event["timestamp"] == TIMESTAMP
    assert event["engine_version"]
    assert event["reason"]
    assert event["sensitivity"] == "Public"
    assert event["correlation_id"]
    assert "payload" not in event
    assert "kind" not in event
    assert "schema_version" not in event


def test_empty_control_directory_permits_execution_and_is_empty_after(
    tmp_path, governed_bundle, governed_estate
):
    store = tmp_path / "store"
    control = tmp_path / "execution-control"
    control.mkdir()  # initially empty => rights available

    result = run_execution(
        bundle_path=governed_bundle,
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
        control_root=control,
    )

    assert result.status is ExecutionStatus.COMPLETE  # a normal Execution ran
    assert (store / EXECUTION_ID).exists()
    # The engine released its own reservation: the control directory is empty again.
    assert list(control.iterdir()) == []


def test_failed_execution_releases_control_directory(tmp_path, governed_estate):
    store = tmp_path / "store"
    control = tmp_path / "execution-control"
    control.mkdir()

    # An invalid bundle produces a Failed Execution (T5) — an Execution that exists, then aborts.
    result = run_execution(
        bundle_path=FIXTURES / "invalid-plan-mode" / "bundle",
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
        control_root=control,
    )

    assert result.status is ExecutionStatus.FAILED
    # Release is guaranteed on every terminating Execution path, including the Failed path.
    assert list(control.iterdir()) == []
