"""Engine-owned closed sets produced by the evidence spine (ticket T0).

Only the closed sets the ungoverned execution and the evidence spine actually produce
are defined here. Governance closed sets (Technical Outcome, Policy Outcome, Coverage
State, Enforcement Mode, Evaluation Role, and so on) are introduced complete — with
degenerate values — by the ticket that first produces them (T1), not here. No artifact
outside the engine may extend these sets (CONTEXT.md).
"""

from __future__ import annotations

from enum import Enum


class ExecutionStatus(str, Enum):
    """Closed execution-level completeness result recorded in Evidence.

    Reflects completion of observation, not the presence of governance findings.
    The ungoverned tracer completes observation of its declared scope, so it reports
    COMPLETE.
    """

    COMPLETE = "Complete"
    COMPLETE_WITH_GAPS = "CompleteWithGaps"
    FAILED = "Failed"


class SensitivityClassification(str, Enum):
    """Closed label carried by every evidence and log record.

    Constant ``PUBLIC`` in this synthetic slice; the closed set exists so the redaction
    model is present before real data is.
    """

    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"
