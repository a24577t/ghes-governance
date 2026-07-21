"""AC 10 / Scenario S10 — tamper detection at Report Derivation.

Report Derivation verifies before it derives (``store.read_verified_execution``):

(a) **Item mutation** — mutating any stored evidence item makes derivation fail, naming the
    item whose content hash no longer matches the Execution Manifest.
(b) **Coherent manifest mutation** — rewriting an item together with its manifest hash so the
    manifest still verifies against the mutated item makes the *recomputed Execution Digest*
    disagree with the recorded sidecar; derivation fails tamper-suspect and trusts neither the
    manifest nor the digest (ADR-0014). Without (b) the manifest would verify against itself
    and coherent tampering would be undetectable.

Bound to the existing stable ``governed`` fixture (a Complete Execution with real evidence).
The test operates at the evidence-store artifact level through the store's own contract and its
canonical-serialization/content-hash chain — the integrity chain under test (Python Coding
Standard §12). It introduces no production change.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.canonical import canonical_bytes, content_hash
from ghes_governance.errors import DigestMismatchError, ItemHashMismatchError
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import EVIDENCE_DIR, MANIFEST_NAME, execution_dir


def _run(store: Path, bundle: Path, estate: Path) -> None:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_bytes().decode("utf-8"))


def test_item_mutation_fails_naming_the_item(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    _run(store, governed_bundle, governed_estate)
    exec_dir = execution_dir(store, EXECUTION_ID)
    # Manifest items are name-sorted, so items[0] is a deterministic choice of victim.
    target = _load(exec_dir / MANIFEST_NAME)["items"][0]["name"]

    item_path = exec_dir / EVIDENCE_DIR / target
    mutated = _load(item_path)
    mutated["_tamper"] = True  # still valid JSON; different content hash from the manifest's
    item_path.write_bytes(canonical_bytes(mutated))

    # The manifest is untouched, so the digest still verifies; the item-hash layer is what
    # must catch this, and it must identify the offending item by name.
    with pytest.raises(ItemHashMismatchError) as excinfo:
        derive_reports(store_root=store, execution_id=EXECUTION_ID)
    assert excinfo.value.item_name == target


def test_coherent_manifest_mutation_fails_on_digest(
    tmp_path: Path, governed_bundle: Path, governed_estate: Path
) -> None:
    store = tmp_path / "store"
    _run(store, governed_bundle, governed_estate)
    exec_dir = execution_dir(store, EXECUTION_ID)
    manifest = _load(exec_dir / MANIFEST_NAME)
    entry = manifest["items"][0]

    # Mutate the item AND rewrite its manifest hash together, so the item-vs-manifest check
    # would pass — isolating the digest layer. The digest sidecar still commits to the
    # original manifest, so the recomputed digest now disagrees with the recorded one.
    item_path = exec_dir / EVIDENCE_DIR / entry["name"]
    mutated = _load(item_path)
    mutated["_tamper"] = True
    item_path.write_bytes(canonical_bytes(mutated))
    entry["sha256"] = content_hash(mutated)
    (exec_dir / MANIFEST_NAME).write_bytes(canonical_bytes(manifest))

    with pytest.raises(DigestMismatchError):
        derive_reports(store_root=store, execution_id=EXECUTION_ID)
