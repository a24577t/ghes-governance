"""Whole-bundle desired-state validation (ticket T5) — the Failed-Execution gate.

AC 12 / S12 and the "engine refuses desired state it cannot faithfully execute" decision
(phase Recorded Decision 5): the desired-state bundle is validated *after* the Execution
exists but *before* discovery or evaluation (Execution Lifecycle). Validation covers both
**structural validity** (parse, schema shape) and **semantic supportability** (schema
version, enforcement mode, evaluation role, referential integrity) of every artifact, and
rejects any unsupported artifact type present anywhere in the bundle — **whole-bundle, even
when the unsupported content appears unreferenced**, because the engine cannot prove content
irrelevant without understanding its semantics. It never silently ignores or downgrades
unsupported desired state, and it never evaluates or discovers.

``validate_bundle`` returns validation-error records (empty ⇒ valid). The caller records them
as configuration evidence and ends the Execution ``Failed``; it never raises them.

**Local implementation decision (concrete encoding — delegated to the implementation ticket
by the approved specification, Implementation Decisions line 137):** desired-state artifacts
MAY carry a ``schema_version`` field; this release supports ``"1"``. An absent field is
treated as the supported version (backward-compatible with the T0–T4 fixtures, none of which
declare one); a present, differing value is an ``unsupported-schema-version`` defect. The
supported enforcement mode and evaluation role are the engine-owned closed-set values this
slice evaluates (Observe, Authoritative); every other declared member is unsupported here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .enums import EnforcementMode, EvaluationRole

#: Desired-state artifact schema version this engine release supports (local encoding; see
#: module docstring). Absent ⇒ treated as supported; present-and-different ⇒ rejected.
SUPPORTED_SCHEMA_VERSION = "1"

#: The only bundle artifact directories this slice supports. Any other root entry — a relief
#: directory, comparison profiles, a capability matrix, a stray file — is unsupported content
#: and fails validation even when no binding references it.
SUPPORTED_ARTIFACT_DIRS = ("bindings", "policies")


def validate_bundle(bundle_path: str | Path) -> list[dict[str, Any]]:
    """Validate the whole desired-state bundle; return validation-error records (empty ⇒ valid).

    Each record carries a stable ``code``, the offending ``artifact`` (path relative to the
    bundle root, or the root entry name for an unsupported artifact type), and a deterministic
    ``detail``. The engine reads only the bundle; it discovers and evaluates nothing.
    """
    root = Path(bundle_path)
    if not root.is_dir():
        return [_error("bundle-unreadable", str(root), "bundle path is not a directory")]

    errors: list[dict[str, Any]] = []
    errors.extend(_validate_artifact_layout(root))
    policy_versions, policy_errors = _validate_policies(root)
    errors.extend(policy_errors)
    errors.extend(_validate_bindings(root, policy_versions))
    return errors


def _validate_artifact_layout(root: Path) -> list[dict[str, Any]]:
    """Reject any bundle-root entry that is not a supported artifact directory (whole-bundle)."""
    errors: list[dict[str, Any]] = []
    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        if entry.name.startswith("."):
            continue
        if entry.name not in SUPPORTED_ARTIFACT_DIRS or not entry.is_dir():
            errors.append(
                _error(
                    "unsupported-artifact",
                    entry.name,
                    f"unsupported bundle artifact {entry.name!r}; this release supports only "
                    f"{', '.join(SUPPORTED_ARTIFACT_DIRS)}",
                )
            )
    return errors


def _validate_policies(root: Path) -> tuple[dict[str, set[Any]], list[dict[str, Any]]]:
    """Validate each policy document; return the versions declared per policy id and the errors.

    ``versions`` maps policy id → the set of declared ``version`` values, so a binding's
    referential integrity can be checked without re-parsing (a duplicate (id, version) is a
    defect, not a second version).
    """
    errors: list[dict[str, Any]] = []
    versions: dict[str, set[Any]] = {}
    seen: dict[tuple[str, Any], str] = {}

    for path in sorted((root / "policies").glob("*.yaml")):
        artifact = f"policies/{path.name}"
        doc, parse_error = _load_yaml(path, artifact)
        if parse_error is not None:
            errors.append(parse_error)
            continue
        if not isinstance(doc, dict):
            errors.append(
                _error("malformed-artifact", artifact, "policy document is not a mapping")
            )
            continue

        errors.extend(_check_schema_version(doc, artifact))

        policy_id = doc.get("id")
        if not isinstance(policy_id, str) or not policy_id:
            errors.append(_error("malformed-artifact", artifact, "policy is missing a string 'id'"))
            continue

        requirements = doc.get("requirements")
        if not isinstance(requirements, list):
            errors.append(
                _error("malformed-artifact", artifact, "policy 'requirements' must be a list")
            )
        elif any(
            not isinstance(req, dict) or not isinstance(req.get("id"), str) or not req.get("id")
            for req in requirements
        ):
            errors.append(
                _error("malformed-artifact", artifact, "every requirement must carry a string 'id'")
            )

        version = doc.get("version")
        key = (policy_id, version)
        if key in seen:
            errors.append(
                _error(
                    "duplicate-policy",
                    artifact,
                    f"policy id {policy_id!r} version {version!r} is already defined by "
                    f"{seen[key]!r}",
                )
            )
        else:
            seen[key] = artifact
            versions.setdefault(policy_id, set()).add(version)

    return versions, errors


def _validate_bindings(root: Path, policy_versions: dict[str, set[Any]]) -> list[dict[str, Any]]:
    """Validate each binding document: structure, supported mode/role, and referential integrity."""
    errors: list[dict[str, Any]] = []

    for path in sorted((root / "bindings").glob("*.yaml")):
        artifact = f"bindings/{path.name}"
        doc, parse_error = _load_yaml(path, artifact)
        if parse_error is not None:
            errors.append(parse_error)
            continue
        if not isinstance(doc, dict):
            errors.append(
                _error("malformed-artifact", artifact, "binding document is not a mapping")
            )
            continue

        errors.extend(_check_schema_version(doc, artifact))

        policy_id = doc.get("policy")
        if not isinstance(policy_id, str) or not policy_id:
            errors.append(
                _error("malformed-artifact", artifact, "binding is missing a string 'policy'")
            )
        if doc.get("scope") is None:
            errors.append(_error("malformed-artifact", artifact, "binding is missing 'scope'"))

        mode = doc.get("enforcement_mode")
        if mode != EnforcementMode.OBSERVE.value:
            errors.append(
                _error(
                    "unsupported-enforcement-mode",
                    artifact,
                    f"enforcement_mode {mode!r} is not supported; this release evaluates only "
                    f"{EnforcementMode.OBSERVE.value!r} bindings",
                )
            )
        role = doc.get("evaluation_role")
        if role != EvaluationRole.AUTHORITATIVE.value:
            errors.append(
                _error(
                    "unsupported-evaluation-role",
                    artifact,
                    f"evaluation_role {role!r} is not supported; this release evaluates only "
                    f"{EvaluationRole.AUTHORITATIVE.value!r} bindings",
                )
            )

        if isinstance(policy_id, str) and policy_id:
            version = doc.get("policy_version")
            if version not in policy_versions.get(policy_id, set()):
                errors.append(
                    _error(
                        "dangling-binding-reference",
                        artifact,
                        f"binding references policy {policy_id!r} version {version!r} with no "
                        "matching policy document",
                    )
                )

    return errors


def _check_schema_version(doc: dict[str, Any], artifact: str) -> list[dict[str, Any]]:
    version = doc.get("schema_version")
    if version is not None and version != SUPPORTED_SCHEMA_VERSION:
        return [
            _error(
                "unsupported-schema-version",
                artifact,
                f"schema_version {version!r} is not supported; this release supports "
                f"{SUPPORTED_SCHEMA_VERSION!r}",
            )
        ]
    return []


def _load_yaml(path: Path, artifact: str) -> tuple[Any, dict[str, Any] | None]:
    """Parse one artifact, returning ``(document, None)`` or ``(None, malformed-error)``.

    A parse failure is a structural defect recorded as configuration evidence, never raised —
    the Execution already exists and must end ``Failed`` (AC 12), not abort with an exception.
    """
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), None
    except (OSError, yaml.YAMLError):
        return None, _error("malformed-artifact", artifact, "artifact is not well-formed YAML")


def _error(code: str, artifact: str, detail: str) -> dict[str, Any]:
    return {"code": code, "artifact": artifact, "detail": detail}
