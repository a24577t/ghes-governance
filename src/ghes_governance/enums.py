"""Engine-owned closed sets.

The evidence-spine sets (``ExecutionStatus``, ``SensitivityClassification``) shipped with
T0 and remain ``str, Enum`` — they are stable artifact-contract values, migrated to
``StrEnum`` only through a behaviour-preserving adoption ticket (Python Coding Standard
§7). The governance closed sets introduced with the first governed evaluation (T1) use
``StrEnum`` and ship complete; several values are only partly reachable in this slice. No
artifact outside the engine may extend these sets (CONTEXT.md).
"""

from __future__ import annotations

from enum import Enum, StrEnum


class ExecutionStatus(str, Enum):
    """Closed execution-level completeness result recorded in Evidence."""

    COMPLETE = "Complete"
    COMPLETE_WITH_GAPS = "CompleteWithGaps"
    FAILED = "Failed"


class SensitivityClassification(str, Enum):
    """Closed label carried by every evidence and log record (constant Public here)."""

    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class EnforcementMode(StrEnum):
    """Closed set attached to a Policy Binding. This slice exercises Observe only."""

    OBSERVE = "Observe"
    PLAN = "Plan"
    ENFORCE = "Enforce"


class EvaluationRole(StrEnum):
    """Closed set declared on every Policy Binding. This slice exercises Authoritative."""

    AUTHORITATIVE = "Authoritative"
    SHADOW = "Shadow"


class TechnicalOutcome(StrEnum):
    """Closed result of technical evaluation of a Requirement — never altered by relief."""

    COMPLIANT = "Compliant"
    NON_COMPLIANT = "NonCompliant"
    UNKNOWN = "Unknown"
    NOT_EVALUATED = "NotEvaluated"


class GovernanceInterpretation(StrEnum):
    """Closed governance overlay on a Technical Outcome (constant None in this slice)."""

    NONE = "None"
    EXCEPTION = "Exception"
    EXCLUSION = "Exclusion"


class RequirementOutcome(StrEnum):
    """Closed interpreted result from Technical Outcome plus Governance Interpretation."""

    COMPLIANT = "Compliant"
    NON_COMPLIANT = "NonCompliant"
    EXCEPTED = "Excepted"
    EXCLUDED = "Excluded"
    UNKNOWN = "Unknown"


class PolicyOutcome(StrEnum):
    """Closed policy-level result aggregated deterministically from Requirement Outcomes."""

    COMPLIANT = "Compliant"
    COMPLIANT_WITH_EXCEPTIONS = "CompliantWithExceptions"
    NON_COMPLIANT = "NonCompliant"
    UNKNOWN = "Unknown"


class CoverageState(StrEnum):
    """Closed policy-level result describing how complete the intended control set is."""

    COVERED = "Covered"
    PARTIALLY_COVERED = "PartiallyCovered"
    UNKNOWN = "Unknown"


class ProviderResult(StrEnum):
    """Closed result set of an attribute lookup — Cannot Determine is distinct.

    Cannot Determine is never converted into Value Absent: a required attribute that
    cannot be determined makes applicability Unknown (ADR-0003).
    """

    VALUE_PRESENT = "ValuePresent"
    VALUE_ABSENT = "ValueAbsent"
    CANNOT_DETERMINE = "CannotDetermine"


class ApplicabilityOutcome(StrEnum):
    """Closed applicability result for scope resolution and per-requirement applicability."""

    APPLICABLE = "Applicable"
    NOT_APPLICABLE = "NotApplicable"
    UNKNOWN = "Unknown"
