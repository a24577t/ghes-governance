"""AC 9 / Scenario S9 — evidence/operational-log independence.

Operational logging is runtime configuration owned by the Operational Log data class
(ADR-0009), a data class distinct from Authoritative Evidence. The engine emits execution-time
operational events filtered by a configured level — DEBUG reveals strictly more than INFO — yet
the authoritative Evidence is byte-identical at every level, governance outcomes are unchanged,
and no operational-log artifact ever enters the evidence store or the Execution Manifest.

Asserted through the ``run_execution`` seam; the operational log is read back as a plain
artifact (its own contract), never through an internal module. Bound to the existing stable
``governed`` fixture.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import Severity
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import MANIFEST_NAME, execution_dir


def _run(store: Path, log_root: Path, level: Severity, bundle: Path, estate: Path) -> None:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
        log_root=log_root,
        log_level=level,
    )


def _events(log_root: Path) -> list[dict[str, Any]]:
    """Execution-time operational events (those carrying an ``event`` field) under ``log_root``."""
    out: list[dict[str, Any]] = []
    if not log_root.exists():
        return out
    for p in sorted(log_root.rglob("*")):
        if p.is_file():
            for line in p.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped:
                    record = json.loads(stripped)
                    if "event" in record:
                        out.append(record)
    return out


def _evidence(store: Path) -> dict[str, bytes]:
    root = execution_dir(store, EXECUTION_ID)
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_debug_is_a_strict_superset_of_meaningful_events(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    _run(tmp_path / "store-info", tmp_path / "log-info", Severity.INFO, governed_bundle, governed_estate)
    _run(
        tmp_path / "store-debug", tmp_path / "log-debug", Severity.DEBUG, governed_bundle, governed_estate
    )
    info = _events(tmp_path / "log-info")
    debug = _events(tmp_path / "log-debug")

    assert info, "INFO emits the major stage events"
    info_names = {e["event"] for e in info}
    debug_names = {e["event"] for e in debug}
    assert info_names < debug_names  # DEBUG is a strict superset of the meaningful event kinds
    assert len(debug) > len(info)  # and strictly more events overall
    assert any(e["severity"] == "DEBUG" for e in debug)  # a DEBUG-only execution-detail event
    assert all(e["severity"] != "DEBUG" for e in info)  # INFO withholds DEBUG detail


def test_evidence_and_outcomes_are_identical_across_levels(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    _run(tmp_path / "store-info", tmp_path / "log-info", Severity.INFO, governed_bundle, governed_estate)
    _run(
        tmp_path / "store-debug", tmp_path / "log-debug", Severity.DEBUG, governed_bundle, governed_estate
    )

    # Authoritative Evidence is byte-identical at INFO and DEBUG.
    assert _evidence(tmp_path / "store-info") == _evidence(tmp_path / "store-debug")

    # Governance outcomes derived from that evidence are identical too.
    info_report = derive_reports(store_root=tmp_path / "store-info", execution_id=EXECUTION_ID).json_report
    debug_report = derive_reports(
        store_root=tmp_path / "store-debug", execution_id=EXECUTION_ID
    ).json_report
    assert info_report == debug_report


def test_operational_log_is_outside_the_evidence_store_and_manifest(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    log_root = tmp_path / "operational-log"
    _run(store, log_root, Severity.DEBUG, governed_bundle, governed_estate)
    exec_dir = execution_dir(store, EXECUTION_ID)

    # The operational log was written, beneath log_root and physically outside the evidence store.
    assert _events(log_root), "execution-time events were written to the operational log"
    assert store not in log_root.parents  # the log directory is not inside the evidence store
    assert not any("operational" in p.name.lower() for p in exec_dir.rglob("*"))

    # And no operational-log artifact appears in the Execution Manifest.
    manifest = json.loads((exec_dir / MANIFEST_NAME).read_bytes())
    assert all("operational" not in e["name"].lower() for e in manifest["items"])
