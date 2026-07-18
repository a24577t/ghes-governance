"""AC 2 / Scenario S2 — determinism and replay.

Two Executions with identical Execution-boundary inputs, run against independent empty
evidence stores, produce byte-identical evidence including hashes and the manifest. The
store location is test-harness infrastructure; the assertion is byte-identity of content
across the two stores, never of their paths.
"""

from __future__ import annotations

from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.execution import run_execution


def _run(store, bundle, estate) -> None:
    run_execution(
        bundle_path=bundle,
        estate_path=estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )


def test_byte_identical_evidence_across_independent_stores(
    tmp_path, ungoverned_bundle, ungoverned_estate
):
    store_a = tmp_path / "a"
    store_b = tmp_path / "b"
    _run(store_a, ungoverned_bundle, ungoverned_estate)
    _run(store_b, ungoverned_bundle, ungoverned_estate)

    files_a = sorted(
        p.relative_to(store_a) for p in (store_a / EXECUTION_ID).rglob("*") if p.is_file()
    )
    files_b = sorted(
        p.relative_to(store_b) for p in (store_b / EXECUTION_ID).rglob("*") if p.is_file()
    )
    assert files_a == files_b
    assert files_a  # the execution actually wrote evidence

    for rel in files_a:
        assert (store_a / rel).read_bytes() == (store_b / rel).read_bytes(), rel
