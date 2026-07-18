"""Injected Execution-boundary inputs shared across T0 tests.

Fixed so evidence is byte-deterministic and golden-comparable. Not an engine module —
test infrastructure only.
"""

SCOPE = {"kind": "enterprise", "value": "acme"}
TIMESTAMP = "2026-01-01T00:00:00Z"
EXECUTION_ID = "exec-0001"
