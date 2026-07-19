"""T5 — full desired-state bundle validation (AC 12 / S12), through the two public seams.

Bundle validity is not an Execution-creation precondition (Execution Lifecycle): the bundle
is validated *after* the Execution exists but *before* discovery or evaluation. Any
structurally malformed or semantically unsupported bundle content — including unsupported
content that appears unreferenced by any binding — makes the Execution Status ``Failed``,
with configuration evidence naming the validation errors and the offending content and *no*
authoritative compliance or coverage results. This is a ``Failed`` Execution, not a raised
error and not a pre-execution refusal (contrast AC 13 / AC 15, which produce no Status at
all). Behaviour is asserted only at the two public seams (run_execution, derive_reports).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from _boundary import EXECUTION_ID, SCOPE, TIMESTAMP

from ghes_governance.enums import ExecutionStatus
from ghes_governance.execution import run_execution
from ghes_governance.reporting import derive_reports

FIXTURES = Path(__file__).parent / "fixtures"

# (fixture directory, expected validation-error code, offending artifact path relative to the
# bundle root). One row per S12 invalid-bundle variant, plus the two semantic-integrity
# defects AC 12 folds into the Failed path (previously interim BundleError raises in T4).
INVALID_BUNDLES = [
    ("invalid-unparseable", "malformed-artifact", "policies/policy-baseline.yaml"),
    ("invalid-malformed-policy", "malformed-artifact", "policies/policy-baseline.yaml"),
    ("invalid-schema-version", "unsupported-schema-version", "policies/policy-baseline.yaml"),
    ("invalid-plan-mode", "unsupported-enforcement-mode", "bindings/binding-baseline.yaml"),
    ("invalid-shadow-role", "unsupported-evaluation-role", "bindings/binding-baseline.yaml"),
    ("invalid-relief", "unsupported-artifact", "relief"),
    ("invalid-unreferenced-artifact", "unsupported-artifact", "comparison-profiles"),
    ("invalid-stray-in-dir", "unsupported-artifact", "policies/notes.txt"),
    ("invalid-hidden-root-dir", "unsupported-artifact", ".relief"),
    ("invalid-hidden-yaml-in-dir", "unsupported-artifact", "policies/.policy-experimental.yaml"),
    ("invalid-duplicate-policy", "duplicate-policy", "policies/policy-duplicate.yaml"),
    ("invalid-dangling-binding", "dangling-binding-reference", "bindings/binding-baseline.yaml"),
]


@pytest.mark.parametrize("subdir, code, artifact", INVALID_BUNDLES)
def test_invalid_bundle_fails_execution_with_configuration_evidence(
    tmp_path, governed_estate, subdir, code, artifact
):
    store = tmp_path / "store"

    result = run_execution(
        bundle_path=FIXTURES / subdir / "bundle",
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    # An Execution exists and ends Failed — not a raise, not a refusal.
    assert result.status is ExecutionStatus.FAILED

    # Reports derive from the stored evidence and verify it first; a Failed Execution's
    # evidence still verifies, so derivation succeeds without raising.
    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    assert report["execution_status"] == "Failed"

    # No authoritative compliance or coverage results are produced for a Failed Execution.
    assert report["compliance"]["outcomes"] == []
    assert report["coverage"]["states"] == []

    # Configuration evidence identifies the validation error and the offending content.
    errors = report["bundle_validation"]
    assert any(e["code"] == code and e["artifact"] == artifact for e in errors), errors


def test_gitkeep_is_accepted_and_does_not_fail_validation(
    tmp_path, ungoverned_bundle, ungoverned_estate
):
    # A regular `.gitkeep` (present in ungoverned/bundle/bindings/) is a git placeholder, not
    # desired state: it is the one hidden entry validation ignores. Its presence must not make
    # the Execution Failed — only genuinely unsupported hidden content does.
    store = tmp_path / "store"
    result = run_execution(
        bundle_path=ungoverned_bundle,
        estate_path=ungoverned_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    assert result.status is not ExecutionStatus.FAILED

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    assert report["bundle_validation"] == []


def test_failed_execution_evidence_is_byte_deterministic(tmp_path, governed_estate):
    # AC 2 is a standing invariant over every execution; the Failed path ships a new evidence
    # shape (bundle-validation), so verify it too replays byte-identically across independent
    # stores.
    bundle = FIXTURES / "invalid-plan-mode" / "bundle"
    stores = []
    for name in ("a", "b"):
        store = tmp_path / name
        run_execution(
            bundle_path=bundle,
            estate_path=governed_estate,
            evaluation_scope=SCOPE,
            evaluation_timestamp=TIMESTAMP,
            execution_id=EXECUTION_ID,
            store_root=store,
        )
        stores.append(store)

    files_a = sorted(
        p.relative_to(stores[0]) for p in (stores[0] / EXECUTION_ID).rglob("*") if p.is_file()
    )
    files_b = sorted(
        p.relative_to(stores[1]) for p in (stores[1] / EXECUTION_ID).rglob("*") if p.is_file()
    )
    assert files_a == files_b
    assert files_a  # the Failed Execution actually wrote evidence
    for rel in files_a:
        assert (stores[0] / rel).read_bytes() == (stores[1] / rel).read_bytes(), rel


def test_valid_bundle_passes_validation_and_is_not_failed(
    tmp_path, governed_bundle, governed_estate
):
    # Regression guard: validation must not over-reject a valid bundle.
    store = tmp_path / "store"

    result = run_execution(
        bundle_path=governed_bundle,
        estate_path=governed_estate,
        evaluation_scope=SCOPE,
        evaluation_timestamp=TIMESTAMP,
        execution_id=EXECUTION_ID,
        store_root=store,
    )
    assert result.status is ExecutionStatus.COMPLETE

    report = derive_reports(store_root=store, execution_id=EXECUTION_ID).json_report
    assert report["execution_status"] == "Complete"
    assert report["bundle_validation"] == []
