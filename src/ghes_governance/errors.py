"""Engine error types.

The tamper-evidence errors are part of the frozen T0 verification contract. Report
Derivation raises them and derives nothing when either fires; later tickets exercise
these paths with adversarial fixtures but must not redefine the behavior.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .enums import RefusalCategory


class GovernanceEngineError(Exception):
    """Base class for all engine errors."""


class BundleError(GovernanceEngineError):
    """The desired-state bundle or synthetic estate could not be loaded."""


class DeferredCapabilityError(GovernanceEngineError):
    """A ratified capability that is intentionally not built in the current increment was reached.

    Distinct from a bug or an accidental gap: the behavior is defined by the authoritative record
    but its implementation is scheduled for a later increment, and this makes that boundary
    explicit and fail-loud rather than silently mis-handling the case. Example: a per-requirement
    applicability that resolves ``Unknown`` — ratified to yield a requirement ``Unknown`` /
    ``IncompleteObservation`` (ADR-0006, CONTEXT.md) — is deferred here because it requires the
    requirement-level Execution-Status derivation not built in this increment; AC 8b's fixtures use
    only determinable applicability attributes, so this is never reached in delivered behavior."""


class ConfigurationError(GovernanceEngineError):
    """A supplied engine configuration or input is invalid, detected before any Execution side
    effect. Distinct from a Failed Execution (a created Execution that aborts with evidence) and
    from a pre-execution refusal (a governance-semantic AC 13 / AC 15 refusal recorded as an
    operational event): a configuration error creates no Execution and writes nothing at all —
    no execution right, no Evidence, and no operational event.

    Raised, for example, when the Operational Log directory would physically overlap the evidence
    store: the two are separate data classes (ADR-0009) and must occupy disjoint directories."""


class TamperSuspectError(GovernanceEngineError):
    """Evidence validation failed; the evidence set is tamper-suspect.

    Raised during Report Derivation before any report is produced.
    """


class DigestMismatchError(TamperSuspectError):
    """The recomputed Execution Digest disagrees with the recorded digest.

    Neither the manifest nor the recorded digest is presumed trustworthy.
    """


class ItemHashMismatchError(TamperSuspectError):
    """A stored evidence item's content hash no longer matches the Execution Manifest."""

    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        super().__init__(f"evidence item {item_name!r} does not match its manifest hash")


class EvidenceUnreadableError(TamperSuspectError):
    """The Execution Manifest or Execution Digest could not be read or parsed.

    Covers a missing, malformed, unreadable, or invalid manifest/digest commitment
    (raw ``FileNotFoundError``/``OSError``/``json.JSONDecodeError``/``UnicodeDecodeError``
    at the store boundary). Without a readable commitment the evidence set cannot be
    validated, so it is treated as tamper-suspect; the original cause is chained.
    """


class ExecutionRefusedError(GovernanceEngineError):
    """A request was refused before an Execution was created — a pre-execution refusal.

    Raised at the Execution boundary when an Execution-creation precondition is unmet: the
    Execution Identifier is already present in the target evidence store (AC 15), or exclusive
    execution rights are unavailable (AC 13). No Execution exists, so no Execution Status is
    produced and no authoritative Evidence is written; the refusal is recorded only as a
    structured ``ERROR`` event in the Operational Log (ADR-0009's separate data class). Distinct
    from a Failed Execution, which is created and then aborts with configuration evidence.
    """

    def __init__(self, category: RefusalCategory, message: str) -> None:
        self.category = category
        super().__init__(message)
