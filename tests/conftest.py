"""Shared test fixtures and injected Execution-boundary inputs.

Tests exercise behavior only through the two public seams (Execution boundary, Report
Derivation); no test imports an internal implementation module beyond the seam
entry points and the store contract. The Evaluation Timestamp and execution identifier
are fixed so evidence is byte-deterministic and golden-comparable.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def ungoverned_bundle() -> Path:
    return FIXTURES / "ungoverned" / "bundle"


@pytest.fixture
def ungoverned_estate() -> Path:
    return FIXTURES / "ungoverned" / "estate"


@pytest.fixture
def governed_bundle() -> Path:
    return FIXTURES / "governed" / "bundle"


@pytest.fixture
def governed_estate() -> Path:
    return FIXTURES / "governed" / "estate"


@pytest.fixture
def unknown_scope_bundle() -> Path:
    return FIXTURES / "unknown-scope" / "bundle"


@pytest.fixture
def unknown_scope_estate() -> Path:
    return FIXTURES / "unknown-scope" / "estate"


@pytest.fixture
def combinator_divergent_bundle() -> Path:
    return FIXTURES / "combinator-divergent" / "bundle"


@pytest.fixture
def combinator_divergent_estate() -> Path:
    return FIXTURES / "combinator-divergent" / "estate"


@pytest.fixture
def all_false_unknown_bundle() -> Path:
    return FIXTURES / "combinator-all-false-unknown" / "bundle"


@pytest.fixture
def all_false_unknown_estate() -> Path:
    return FIXTURES / "combinator-all-false-unknown" / "estate"


@pytest.fixture
def not_unknown_bundle() -> Path:
    return FIXTURES / "combinator-not-unknown" / "bundle"


@pytest.fixture
def not_unknown_estate() -> Path:
    return FIXTURES / "combinator-not-unknown" / "estate"


@pytest.fixture
def conflict_bundle() -> Path:
    return FIXTURES / "conflict-proven" / "bundle"


@pytest.fixture
def conflict_estate() -> Path:
    return FIXTURES / "conflict-proven" / "estate"


@pytest.fixture
def undeterminable_mixed_bundle() -> Path:
    return FIXTURES / "undeterminable-mixed" / "bundle"


@pytest.fixture
def undeterminable_mixed_estate() -> Path:
    return FIXTURES / "undeterminable-mixed" / "estate"
