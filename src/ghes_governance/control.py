"""Execution-control — exclusive execution rights for the Execution boundary (T6, AC 13).

Realizes ADR-0010's "one active execution ... never interleaved" as this slice's single global
lock (scope-aware coordination is deferred beyond T6). The engine is given a mechanism-neutral
execution-control directory (configuration).

The reservation marker (its name, type, and contents) and the acquisition and release mechanism
are **private to this module**. The contract (Contract A) is:

- **Atomic mutual exclusion among governance-engine executions** sharing an execution-control
  directory is guaranteed through the engine's **private reservation identity**: two engine
  executions can never both cross the Execution boundary, so evidence is never interleaved
  (ADR-0010).
- A **pre-existing non-empty** execution-control directory is treated as rights unavailable and is
  refused — this is also the deterministic **AC 13 seam-level test affordance** (a test places an
  arbitrary entry before calling the engine and observes refusal).
- A **refusal** leaves the observed occupancy **unchanged** (the engine never alters, renames, or
  removes an entry it did not create).
- A **completed** Execution leaves the directory **empty** (release).
- **No guarantee** is claimed against arbitrary, differently named external filesystem entries
  created **concurrently during acquisition** — that is outside ADR-0010 (which concerns
  executions), outside the manual/single-process POC boundary, and not portably enforceable with
  standard-library primitives.
"""

from __future__ import annotations

from pathlib import Path

# Engine-owned reservation marker — private. Its name and type are not part of the contract; the
# observable contract is emptiness/occupancy, not this identifier.
_RESERVATION_NAME = ".execution-reservation"


class _ExecutionRightsUnavailable(Exception):
    """Internal signal: exclusive execution rights could not be acquired (control dir occupied)."""


def acquire(control_root: str | Path) -> Path:
    """Atomically acquire exclusive execution rights under ``control_root``; return the reservation.

    Refuses (raises :class:`_ExecutionRightsUnavailable`) when the control directory is already
    non-empty — occupied by a prior or foreign holder, or any other entry. Otherwise it claims an
    engine-owned reservation with an atomic, exclusive create, so that even if two requests both
    observe an empty directory only one crosses the boundary (a bare check-then-create would let
    both through). It never alters or removes a pre-existing entry.
    """
    root = Path(control_root)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise _ExecutionRightsUnavailable(str(root))
    reservation = root / _RESERVATION_NAME
    try:
        reservation.mkdir(exist_ok=False)  # atomic interlock against a racing acquirer
    except FileExistsError as exc:
        raise _ExecutionRightsUnavailable(str(root)) from exc
    return reservation


def release(reservation: str | Path) -> None:
    """Release engine-owned rights: remove only the engine's own reservation marker.

    Confined to engine-owned state and idempotent — it never touches any other entry, so the
    control directory is left empty when the engine held the only reservation.
    """
    marker = Path(reservation)
    if marker.exists():
        marker.rmdir()
