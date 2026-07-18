"""Evidence store: the write and verify halves of the integrity contract (ticket T0).

Write order is fixed: evidence items first, then the Execution Manifest (the
tamper-evidence root), then the external Execution Digest sidecar recorded beside the
manifest and outside it. Verify order is fixed and content-agnostic: recompute the
digest from the manifest and compare it to the sidecar BEFORE any item hash, trusting
neither value on mismatch, then verify each item's content hash against the manifest.
Later tickets add evidence types that flow through these same functions unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import canonical_bytes, content_hash
from .errors import DigestMismatchError, ItemHashMismatchError

EVIDENCE_DIR = "evidence"
MANIFEST_NAME = "manifest.json"
DIGEST_NAME = "digest.json"
DIGEST_COMPUTATION_VERSION = 1


def execution_dir(store_root: str | Path, execution_id: str) -> Path:
    return Path(store_root) / execution_id


def write_execution(
    store_root: str | Path,
    execution_id: str,
    header: dict[str, Any],
    items: list[tuple[str, dict[str, Any]]],
) -> Path:
    """Write one Execution's evidence, manifest, and digest sidecar.

    ``items`` is a list of (filename, evidence-item) pairs. The evidence directory is
    created fresh; refusing a reused Execution Identifier is ticket T6, so this call
    assumes an empty target and does not overwrite an existing execution.
    """
    exec_dir = execution_dir(store_root, execution_id)
    ev_dir = exec_dir / EVIDENCE_DIR
    ev_dir.mkdir(parents=True, exist_ok=False)

    entries: list[dict[str, Any]] = []
    for name, item in sorted(items, key=lambda pair: pair[0]):
        (ev_dir / name).write_bytes(canonical_bytes(item))
        entries.append({"name": name, "kind": item["kind"], "sha256": content_hash(item)})

    manifest = {**header, "items": sorted(entries, key=lambda e: e["name"])}
    (exec_dir / MANIFEST_NAME).write_bytes(canonical_bytes(manifest))

    digest = {
        "computation_version": DIGEST_COMPUTATION_VERSION,
        "execution_id": execution_id,
        "digest": content_hash(manifest),
    }
    (exec_dir / DIGEST_NAME).write_bytes(canonical_bytes(digest))
    return exec_dir


def read_verified_execution(
    store_root: str | Path, execution_id: str
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Verify then return an Execution's manifest and evidence items keyed by kind.

    Raises :class:`DigestMismatchError` if the recomputed digest disagrees with the
    recorded sidecar (neither trusted), or :class:`ItemHashMismatchError` if any item's
    content no longer matches the manifest. Verification always precedes derivation.
    """
    exec_dir = execution_dir(store_root, execution_id)
    manifest = _load_json(exec_dir / MANIFEST_NAME)
    sidecar = _load_json(exec_dir / DIGEST_NAME)

    recomputed = content_hash(manifest)
    if recomputed != sidecar.get("digest"):
        raise DigestMismatchError(
            "recomputed Execution Digest does not match the recorded digest; "
            "the evidence set is tamper-suspect and neither value is trusted"
        )

    items: dict[str, dict[str, Any]] = {}
    for entry in manifest["items"]:
        path = exec_dir / EVIDENCE_DIR / entry["name"]
        try:
            item = _load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            raise ItemHashMismatchError(entry["name"]) from exc
        if content_hash(item) != entry["sha256"]:
            raise ItemHashMismatchError(entry["name"])
        items[item["kind"]] = item

    return manifest, items


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_bytes().decode("utf-8"))
