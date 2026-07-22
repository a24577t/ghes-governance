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


class NotApplicableReason(StrEnum):
    """Closed reason category carried by every NotApplicable requirement (ADR-0007), shipped
    complete. ``RepositoryCharacteristic`` and ``PolicyPrecondition`` are reachable in this slice
    and author-declarable; ``PlatformCapabilityUnavailable`` is engine-derived from the Capability
    Matrix (Slice 3) and ships dormant — populated by later work, never a later schema migration
    (RD 3). Providers and policies cannot invent categories (ADR-0007)."""

    REPOSITORY_CHARACTERISTIC = "RepositoryCharacteristic"
    POLICY_PRECONDITION = "PolicyPrecondition"
    PLATFORM_CAPABILITY_UNAVAILABLE = "PlatformCapabilityUnavailable"


class UnknownClassification(StrEnum):
    """Why an Unknown arose, recorded on the causal record; Execution Status derives from it.

    Two members (ADR-0015): ``IncompleteObservation`` (a Cannot-Determine gap) and
    ``GovernanceResult`` (a determined governance verdict, e.g. authority conflict). Only
    ``GovernanceResult`` is emitted in this slice; classifying gap Unknowns is a later step.
    """

    INCOMPLETE_OBSERVATION = "IncompleteObservation"
    GOVERNANCE_RESULT = "GovernanceResult"


class Severity(StrEnum):
    """Closed operational-log severity model (ADR-0009), shipped complete.

    Only ``ERROR`` is reachable in this slice: a pre-execution refusal is an integrity failure
    (ADR-0009 places "execution/integrity/write/evidence failures" at ``ERROR``). The remaining
    levels ship as degenerate values, populated by later work — never a later schema migration.
    """

    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    TRACE = "TRACE"


class RefusalCategory(StrEnum):
    """Why a pre-execution request was refused, recorded on the operational refusal event.

    Both categories are reachable in T6: identifier reuse (AC 15) and exclusive execution rights
    unavailable (AC 13).
    """

    IDENTIFIER_REUSE = "identifier-reuse"
    RIGHTS_UNAVAILABLE = "rights-unavailable"
