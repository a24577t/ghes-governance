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

REFUSAL_LOG_NAME = "operational.log"


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
    with (root / REFUSAL_LOG_NAME).open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
