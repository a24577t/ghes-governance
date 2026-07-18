"""The Report Derivation seam (ticket T0).

Reports are derived exclusively from stored Evidence and require no Execution. This
seam verifies before it derives: it recomputes the Execution Digest from the manifest
and compares it to the sidecar, then verifies every item hash against the manifest,
failing loud on either mismatch (see :mod:`ghes_governance.store`). T0 exercises the
successful verification path; the adversarial tamper fixtures are ticket T7.
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


def derive_reports(
    *,
    store_root: str | Path,
    execution_id: str,
    report_dir: str | Path | None = None,
) -> ReportBundle:
    manifest, items = read_verified_execution(store_root, execution_id)

    provenance = items["binding_provenance"]["payload"]["pairs"]
    status = items["execution_status"]["payload"]
    ungoverned = [pair for pair in provenance if not pair.get("governed", False)]

    json_report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "execution_id": manifest["execution_id"],
        "evaluation_timestamp": manifest["evaluation_timestamp"],
        "engine_version": manifest["engine_version"],
        "execution_status": status["status"],
        "accounting": status["accounting"],
        # Compliance and Coverage are reported as independent dimensions; an ungoverned
        # execution produces neither, and invents no outcome for a pair with no binding.
        "compliance": {"outcomes": []},
        "coverage": {"states": []},
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
        "Compliance and Coverage are independent dimensions. This ungoverned execution",
        "produces no Policy Outcome and no Coverage State — absent an authoritative",
        "binding there is no intended control set to measure.",
        "",
        f"## Ungoverned pairs ({len(report['ungoverned_pairs'])})",
        "",
    ]
    for pair in report["ungoverned_pairs"]:
        lines.append(f"- policy `{pair['policy_id']}` × repository `{pair['repository_id']}`")
    lines += [
        "",
        "## Evidence citations",
        "",
        f"- Execution digest: `{report['citations']['execution_digest']}`",
    ]
    for entry in report["citations"]["manifest_items"]:
        lines.append(f"- `{entry['name']}` sha256 `{entry['sha256']}`")
    lines.append("")
    return "\n".join(lines)
