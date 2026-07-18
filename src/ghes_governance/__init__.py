"""GHES Governance engine — Vertical Slice 1, Observe-Mode Tracer.

Ticket T0 establishes the execution integrity contract: canonical serialization,
evidence-item hashing, the Execution Manifest, the external Execution Digest, and
report-side verification that checks the digest before item hashes and fails loud on
any mismatch, trusting neither value. The contract is content-agnostic and frozen;
later tickets serialize, hash, manifest, and verify new evidence types through it
without redefining it.
"""

ENGINE_VERSION = "0.0.1"

__all__ = ["ENGINE_VERSION"]
