"""Engine error types.

The tamper-evidence errors are part of the frozen T0 verification contract. Report
Derivation raises them and derives nothing when either fires; later tickets exercise
these paths with adversarial fixtures but must not redefine the behavior.
"""

from __future__ import annotations


class GovernanceEngineError(Exception):
    """Base class for all engine errors."""


class BundleError(GovernanceEngineError):
    """The desired-state bundle or synthetic estate could not be loaded."""


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
