"""Canonical serialization and content hashing — the base of the integrity contract.

Every evidence item, the Execution Manifest, and the Execution Digest are committed
through these two functions. Canonical form is sorted-key, minimally separated,
UTF-8 JSON so that identical content always produces identical bytes and therefore
identical SHA-256 hashes. This determinism is what makes golden-evidence testing and
tamper detection possible; nothing in the engine may serialize governed content by
another route.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

_UTF8 = "utf-8"


def canonical_bytes(obj: Any) -> bytes:
    """Serialize ``obj`` to canonical JSON bytes.

    Sorted keys, no insignificant whitespace, UTF-8, non-ASCII preserved. Floats are
    rejected: governed content uses integers and strings so that serialization is
    exactly reproducible across platforms.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode(_UTF8)


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hex SHA-256 of ``data``."""
    return hashlib.sha256(data).hexdigest()


def content_hash(obj: Any) -> str:
    """Return the SHA-256 of ``obj``'s canonical serialization."""
    return sha256_hex(canonical_bytes(obj))
