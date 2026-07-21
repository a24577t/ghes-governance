"""Operational Log — the write half of the operational-log data class (ADR-0009).

Operational logs are a data class distinct from Authoritative Evidence: they record engine
operation and troubleshooting under a closed severity model, in a directory physically separate
from the evidence store, and are **never** routed through the execution-integrity chain — no
Execution Manifest, no Execution Digest, no content-hash commitment (Python Coding Standard §5).
A refusal event is never shaped as an Evidence item, Finding, Execution Manifest, or Execution.

This slice records exactly one operational event: the pre-execution refusal (T6). It carries the
fields the specification requires (refusal category, attempted identifier, requested scope,
timestamp, engine version, reason, the existing identifier where safe to disclose, sensitivity
classification, and a correlation identifier) at ``ERROR`` severity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .enums import RefusalCategory, SensitivityClassification, Severity

OPERATIONAL_LOG_NAME = "operational.log"

# Severity ordering for level-threshold filtering (ADR-0009): a configured level admits events at
# that severity and every more-severe one. Lower rank = more severe, so an event is written iff its
# rank does not exceed the configured threshold's rank (INFO admits ERROR/WARN/INFO; DEBUG also
# admits DEBUG). This is the only place the closed severity model is ordered.
_SEVERITY_RANK = {
    Severity.ERROR: 0,
    Severity.WARN: 1,
    Severity.INFO: 2,
    Severity.DEBUG: 3,
    Severity.TRACE: 4,
}


def _passes(severity: Severity, threshold: Severity) -> bool:
    return _SEVERITY_RANK[severity] <= _SEVERITY_RANK[threshold]


def record_refusal(
    log_root: str | Path,
    *,
    category: RefusalCategory,
    attempted_execution_id: str,
    requested_scope: dict[str, Any],
    timestamp: str,
    engine_version: str,
    reason: str,
    correlation_id: str,
    existing_execution_id: str | None = None,
) -> None:
    """Append one structured ``ERROR`` refusal event to the Operational Log under ``log_root``.

    Sensitivity is constant ``Public`` in this synthetic slice (ADR-0009). The record is a plain
    operational event — deliberately not the schema-versioned ``kind``/``payload`` evidence shape,
    so it can never be mistaken for Authoritative Evidence. ``existing_execution_id`` may be
    ``None`` when rights unavailability is known without an attributable conflicting Execution
    (AC 13; see ``execution._acquire_rights_or_refuse``). Closed-set values are serialized to their
    JSON string form here, at the output boundary.
    """
    event = {
        "severity": Severity.ERROR.value,
        "category": category.value,
        "attempted_execution_id": attempted_execution_id,
        "existing_execution_id": existing_execution_id,
        "requested_scope": requested_scope,
        "timestamp": timestamp,
        "engine_version": engine_version,
        "reason": reason,
        "sensitivity": SensitivityClassification.PUBLIC.value,
        "correlation_id": correlation_id,
    }
    root = Path(log_root)
    root.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    with (root / OPERATIONAL_LOG_NAME).open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def record_execution_event(
    log_root: str | Path,
    *,
    severity: Severity,
    threshold: Severity,
    event: str,
    execution_id: str,
    timestamp: str,
    engine_version: str,
    detail: dict[str, Any] | None = None,
) -> None:
    """Append one structured execution-time operational event to the Operational Log under
    ``log_root`` — but only when ``severity`` meets the configured ``threshold`` (ADR-0009 level
    filtering). This is the engine's execution-time observability, distinct from the refusal event.

    An Operational Log is a data class separate from Authoritative Evidence: written beneath
    ``log_root`` only, never under the evidence store and never routed through the execution
    manifest/digest integrity chain — so evidence stays byte-identical at every level. The record
    is a plain operational event (an ``event`` name, not the schema-versioned ``kind``/``payload``
    evidence shape), so it can never be mistaken for Evidence. Deterministic: no wall clock is read;
    the injected Evaluation ``timestamp`` is recorded. Sensitivity is constant ``Public`` in this
    synthetic slice (ADR-0009).
    """
    if not _passes(severity, threshold):
        return
    record: dict[str, Any] = {
        "severity": severity.value,
        "event": event,
        "execution_id": execution_id,
        "timestamp": timestamp,
        "engine_version": engine_version,
        "sensitivity": SensitivityClassification.PUBLIC.value,
        **({"detail": detail} if detail is not None else {}),
    }
    root = Path(log_root)
    root.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, ensure_ascii=False)
    with (root / OPERATIONAL_LOG_NAME).open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
