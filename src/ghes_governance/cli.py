"""Thin CLI mirroring the two public seams: run an Execution, derive reports.

No network access; the engine writes only beneath the evidence, log, and report
directories it is given. The Evaluation Timestamp and execution identifier are
injected as arguments — the engine never reads a wall clock.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from .execution import run_execution
from .reporting import derive_reports


def _parse_scope(raw: str) -> dict[str, Any]:
    if ":" in raw:
        kind, value = raw.split(":", 1)
        return {"kind": kind, "value": value}
    return {"kind": raw, "value": None}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ghes-governance")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run an Execution through the Execution boundary seam")
    run_p.add_argument("--bundle", required=True)
    run_p.add_argument("--estate", required=True)
    run_p.add_argument("--store", required=True)
    run_p.add_argument("--execution-id", required=True)
    run_p.add_argument("--timestamp", required=True, help="injected Evaluation Timestamp")
    run_p.add_argument("--scope", default="enterprise", help="e.g. enterprise or organization:octo-org")

    rep_p = sub.add_parser("report", help="Derive reports from stored Evidence")
    rep_p.add_argument("--store", required=True)
    rep_p.add_argument("--execution-id", required=True)
    rep_p.add_argument("--out", default=None, help="report output directory")

    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_execution(
            bundle_path=args.bundle,
            estate_path=args.estate,
            evaluation_scope=_parse_scope(args.scope),
            evaluation_timestamp=args.timestamp,
            execution_id=args.execution_id,
            store_root=args.store,
        )
        print(f"Execution {result.execution_id}: {result.status.value}")
        print(f"Evidence: {result.execution_dir}")
        return 0

    if args.command == "report":
        bundle = derive_reports(
            store_root=args.store,
            execution_id=args.execution_id,
            report_dir=args.out,
        )
        if args.out:
            print(f"Reports written to {args.out}")
        else:
            print(bundle.markdown)
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
