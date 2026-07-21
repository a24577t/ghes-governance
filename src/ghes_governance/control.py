"""Execution-control — exclusive execution rights for the Execution boundary (T6, AC 13).

Realizes ADR-0010's "one active execution ... never interleaved" as this slice's single global
lock. The engine is given a mechanism-neutral execution-control directory (configuration) and
acquires exclusive rights by atomically claiming an engine-owned reservation inside it, refusing
when the directory is already occupied.

The reservation marker (its name, type, and contents) and the acquisition and release mechanism
are **private to this module**. The only observable contract is:

- a **non-empty** execution-control directory means exclusive execution rights are unavailable;
- a **completed** acquisition leaves the directory **empty** again (release);
- a **refusal** leaves any pre-existing occupancy **unchanged** (the engine never alters, renames,
  or removes an entry it did not create).
"""

from __future__ import annotations

from pathlib import Path

# Engine-owned reservation marker — private. Its name and type are not part of the contract; the
# observable contract is emptiness/occupancy, not this identifier.
_RESERVATION_NAME = ".execution-reservation"


class ExecutionRightsUnavailable(Exception):
    """Internal signal: exclusive execution rights could not be acquired (control dir occupied)."""


def acquire(control_root: str | Path) -> Path:
    """Atomically acquire exclusive execution rights under ``control_root``; return the reservation.

    Refuses (raises :class:`ExecutionRightsUnavailable`) when the control directory is already
    non-empty — occupied by a prior or foreign holder, or any other entry. Otherwise it claims an
    engine-owned reservation with an atomic, exclusive create, so that even if two requests both
    observe an empty directory only one crosses the boundary (a bare check-then-create would let
    both through). It never alters or removes a pre-existing entry.
    """
    root = Path(control_root)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ExecutionRightsUnavailable(str(root))
    reservation = root / _RESERVATION_NAME
    try:
        reservation.mkdir(exist_ok=False)  # atomic interlock against a racing acquirer
    except FileExistsError as exc:
        raise ExecutionRightsUnavailable(str(root)) from exc
    return reservation


def release(reservation: str | Path) -> None:
    """Release engine-owned rights: remove only the engine's own reservation marker.

    Confined to engine-owned state and idempotent — it never touches any other entry, so the
    control directory is left empty when the engine held the only reservation.
    """
    marker = Path(reservation)
    if marker.exists():
        marker.rmdir()
