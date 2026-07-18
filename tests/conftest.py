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
