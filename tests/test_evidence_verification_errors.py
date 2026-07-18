"""CD-2 — verified evidence reading and report derivation must not leak raw stdlib
exceptions when the Execution Manifest or Execution Digest is missing, malformed, or
unreadable.

These failures at the persistence/parsing boundary MUST surface as
``EvidenceUnreadableError`` (a ``TamperSuspectError``), with the original cause chained
(Python Coding Standard §8). Reading the store's commitment files is a legitimate
artifact-contract test: the store's verification behavior is the contract under test
(§12). The T6 duplicate-Execution-Identifier ``FileExistsError`` is out of scope here.
"""

from __future__ import annotations

import json

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.errors import EvidenceUnreadableError
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports
from ghes_governance.store import DIGEST_NAME, MANIFEST_NAME, execution_dir


def _run(store, bundle, estate) -> None:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def test_domain_error_is_not_a_raw_stdlib_type():
    # The translated error must not itself be one of the raw exception types.
    assert not issubclass(EvidenceUnreadableError, (FileNotFoundError, OSError))
    assert not issubclass(EvidenceUnreadableError, ValueError)  # covers JSON/Unicode decode errors


def test_missing_execution_translated_in_verified_read(tmp_path):
    # Nothing written: manifest and digest are absent (FileNotFoundError under the hood).
    with pytest.raises(EvidenceUnreadableError):
        from ghes_governance.store import read_verified_execution

        read_verified_execution(tmp_path / "store", EXECUTION_ID)


def test_missing_execution_translated_in_report_derivation(tmp_path):
    with pytest.raises(EvidenceUnreadableError):
        derive_reports(store_root=tmp_path / "store", execution_id=EXECUTION_ID)


def test_malformed_manifest_translated(tmp_path, ungoverned_bundle, ungoverned_estate):
    store = tmp_path / "store"
    _run(store, ungoverned_bundle, ungoverned_estate)
    (execution_dir(store, EXECUTION_ID) / MANIFEST_NAME).write_bytes(b"{ not valid json")
    with pytest.raises(EvidenceUnreadableError) as excinfo:
        derive_reports(store_root=store, execution_id=EXECUTION_ID)
    assert isinstance(excinfo.value.__cause__, json.JSONDecodeError)  # cause preserved


def test_unreadable_manifest_translated(tmp_path, ungoverned_bundle, ungoverned_estate):
    store = tmp_path / "store"
    _run(store, ungoverned_bundle, ungoverned_estate)
    (execution_dir(store, EXECUTION_ID) / MANIFEST_NAME).write_bytes(b"\xff\xfe not utf-8")
    with pytest.raises(EvidenceUnreadableError) as excinfo:
        derive_reports(store_root=store, execution_id=EXECUTION_ID)
    assert isinstance(excinfo.value.__cause__, UnicodeDecodeError)  # cause preserved


def test_malformed_digest_translated(tmp_path, ungoverned_bundle, ungoverned_estate):
    store = tmp_path / "store"
    _run(store, ungoverned_bundle, ungoverned_estate)
    (execution_dir(store, EXECUTION_ID) / DIGEST_NAME).write_bytes(b"{ not valid json")
    with pytest.raises(EvidenceUnreadableError):
        derive_reports(store_root=store, execution_id=EXECUTION_ID)
