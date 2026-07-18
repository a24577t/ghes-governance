"""Minimal desired-state bundle and synthetic-estate loading for ticket T0.

T0 parses only what the ungoverned execution needs: the policies (for (policy,
repository) pairs) and any bindings (to confirm none are authoritative), plus the
synthetic estate's repositories. Full structural and semantic bundle validation —
rejecting unsupported or malformed content with a Failed Execution — is ticket T5 and
is intentionally not performed here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import BundleError


def _read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise BundleError(f"could not read {path}: {exc}") from exc


def _load_dir(directory: Path) -> list[dict[str, Any]]:
    if not directory.is_dir():
        return []
    docs: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.yaml")):
        doc = _read_yaml(path)
        if doc is not None:
            docs.append(doc)
    return docs


def load_bundle(bundle_path: str | Path) -> dict[str, list[dict[str, Any]]]:
    """Load the desired-state bundle's policies and bindings."""
    root = Path(bundle_path)
    if not root.is_dir():
        raise BundleError(f"bundle path is not a directory: {root}")
    return {
        "policies": _load_dir(root / "policies"),
        "bindings": _load_dir(root / "bindings"),
    }


def load_estate(estate_path: str | Path) -> dict[str, Any]:
    """Load the synthetic GHES estate fixture."""
    path = Path(estate_path)
    if path.is_dir():
        path = path / "estate.yaml"
    estate = _read_yaml(path)
    if not isinstance(estate, dict) or "repositories" not in estate:
        raise BundleError(f"estate fixture missing 'repositories': {path}")
    return estate
