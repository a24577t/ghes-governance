"""The Report Derivation seam.

Reports are derived exclusively from stored Evidence and require no Execution. This seam
verifies before it derives: it recomputes the Execution Digest from the manifest and
compares it to the sidecar, then verifies every item hash against the manifest, failing
loud on either mismatch (see :mod:`ghes_governance.store`). It reports Compliance and
Coverage as independent dimensions for governed pairs, and surfaces pairs with no
authoritative binding in their own ungoverned category, inventing no outcome for them.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import canonical_bytes, content_hash
from .store import read_verified_execution

REPORT_SCHEMA_VERSION = "1"


@dataclass(frozen=True)
class ReportBundle:
    json_report: dict[str, Any]
    markdown: str


def _item_payload(items: dict[str, dict[str, Any]], kind: str, key: str) -> list[dict[str, Any]]:
    """Return the ``key`` list from evidence item ``kind``'s payload, or ``[]`` when the item is
    absent — a Failed Execution omits the compliance/coverage/provenance items entirely."""
    item = items.get(kind)
    if item is None:
        return []
    value = item["payload"].get(key, [])
    return value if isinstance(value, list) else []


def derive_reports(
    *,
    store_root: str | Path,
    execution_id: str,
    report_dir: str | Path | None = None,
) -> ReportBundle:
    """Derive reports from stored Evidence — the Report Derivation seam.

    Verifies before deriving: recomputes the Execution Digest from the manifest and
    compares it to the sidecar, then verifies each item's content hash against the
    manifest, trusting neither value on mismatch. Derives a machine-readable report and a
    human-readable summary, each citing the manifest; Compliance and Coverage are reported
    as independent dimensions for governed pairs, and pairs with no authoritative binding
    are surfaced as their own ungoverned category. When ``report_dir`` is given, both
    reports are also written there. Requires no Execution — it reads only committed
    Evidence. Raises ``DigestMismatchError`` or ``ItemHashMismatchError`` on a verification
    mismatch, and ``EvidenceUnreadableError`` if the manifest or digest is unreadable.
    """
    manifest, items = read_verified_execution(store_root, execution_id)

    # A Failed Execution (T5 bundle validation) discovers and evaluates nothing, so its
    # evidence carries only the status and the bundle-validation configuration evidence; the
    # compliance/coverage/provenance items are absent and default to empty here.
    status = items["execution_status"]["payload"]
    provenance = _item_payload(items, "binding_provenance", "pairs")
    results = _item_payload(items, "policy_results", "results")
    findings = _item_payload(items, "governance_findings", "findings")
    validation_errors = _item_payload(items, "bundle_validation", "errors")
    ungoverned = [pair for pair in provenance if not pair.get("governed", False)]

    compliance_outcomes = [
        {
            "policy_id": r["policy_id"],
            "repository_id": r["repository_id"],
            "policy_outcome": r["policy_outcome"],
            **(
                {"unknown_classification": r["unknown_classification"]}
                if "unknown_classification" in r
                else {}
            ),
        }
        for r in results
    ]
    coverage_states = [
        {
            "policy_id": r["policy_id"],
            "repository_id": r["repository_id"],
            "coverage_state": r["coverage_state"],
        }
        for r in results
    ]

    json_report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "execution_id": manifest["execution_id"],
        "evaluation_timestamp": manifest["evaluation_timestamp"],
        "engine_version": manifest["engine_version"],
        "execution_status": status["status"],
        "accounting": status["accounting"],
        "compliance": {"outcomes": compliance_outcomes},
        "coverage": {"states": coverage_states},
        "findings": findings,
        "bundle_validation": validation_errors,
        "ungoverned_pairs": ungoverned,
        "citations": {
            "execution_digest": content_hash(manifest),
            "manifest_items": manifest["items"],
        },
    }

    markdown = _render_markdown(json_report)

    if report_dir is not None:
        out = Path(report_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "report.json").write_bytes(canonical_bytes(json_report))
        (out / "summary.md").write_text(markdown, encoding="utf-8")

    return ReportBundle(json_report=json_report, markdown=markdown)


def _render_markdown(report: dict[str, Any]) -> str:
    accounting = report["accounting"]
    lines = [
        f"# Governance Report — Execution {report['execution_id']}",
        "",
        f"- Evaluation timestamp: {report['evaluation_timestamp']}",
        f"- Engine version: {report['engine_version']}",
        f"- Execution status: {report['execution_status']}",
        f"- Discovered: {accounting['discovered']} · "
        f"Evaluated: {accounting['evaluated']} · Unknown: {accounting['unknown']}",
        "",
        "## Compliance and Coverage",
        "",
        "Compliance and Coverage are independent dimensions and are never flattened.",
        "",
    ]
    coverage_by_pair = {
        (c["policy_id"], c["repository_id"]): c["coverage_state"]
        for c in report["coverage"]["states"]
    }
    outcomes = report["compliance"]["outcomes"]
    if outcomes:
        for o in outcomes:
            coverage = coverage_by_pair.get((o["policy_id"], o["repository_id"]), "—")
            lines.append(
                f"- policy `{o['policy_id']}` × repository `{o['repository_id']}`: "
                f"Compliance {o['policy_outcome']} · Coverage {coverage}"
            )
    else:
        lines.append("No governed pair produced a Policy Outcome or Coverage State.")

    if report["bundle_validation"]:
        lines += [
            "",
            f"## Bundle validation ({len(report['bundle_validation'])} error(s))",
            "",
            "The Execution is Failed: the desired-state bundle was rejected before discovery.",
            "",
        ]
        for err in report["bundle_validation"]:
            lines.append(f"- `{err['artifact']}` — {err['code']}: {err['detail']}")

    lines += ["", f"## Ungoverned pairs ({len(report['ungoverned_pairs'])})", ""]
    for pair in report["ungoverned_pairs"]:
        lines.append(f"- policy `{pair['policy_id']}` × repository `{pair['repository_id']}`")

    lines += ["", "## Evidence citations", ""]
    lines.append(f"- Execution digest: `{report['citations']['execution_digest']}`")
    for entry in report["citations"]["manifest_items"]:
        lines.append(f"- `{entry['name']}` sha256 `{entry['sha256']}`")
    lines.append("")
    return "\n".join(lines)
