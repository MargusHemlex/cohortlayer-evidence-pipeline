"""Offline CLI. Errors use controlled codes, never raw provider/file payloads."""

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .contracts import (
    CohortResult,
    DiffReport,
    Evidence,
    Hypothesis,
    Manifest,
    Report,
)
from .diff import compare_reports
from .fixtures import HYPOTHESES, SCENARIOS, VERSIONS
from .pipeline import run_demo
from .provenance import OutputConflict, canonical_bytes, content_hash, write_once
from .reporting import render_diff, render_report


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, "error: invalid_arguments (use --help)\n")


def _parser() -> Parser:
    parser = Parser(description="Synthetic evidence software demo; no real cohort access.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List fictional hypotheses and scenarios")
    run = sub.add_parser("run", help="Run two synthetic cohort adapters")
    run.add_argument("--hypothesis", choices=sorted(HYPOTHESES), default="HYP-001")
    run.add_argument("--scenario", choices=SCENARIOS, default="concordant")
    run.add_argument("--version", choices=VERSIONS, default="v1")
    run.add_argument("--output", type=Path, default=Path("demo-output/run"))
    diff = sub.add_parser("diff", help="Compare two exported reports")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--output", type=Path, default=Path("demo-output/diff"))
    schemas = sub.add_parser("schemas", help="Export closed JSON schemas")
    schemas.add_argument("--output", type=Path, default=Path("demo-output/schemas"))
    return parser


def _load_report(path: Path) -> Report:
    if path.stat().st_size > 1_000_000:
        raise ValueError("report_too_large")
    report = Report.model_validate_json(path.read_bytes())
    if content_hash(report.manifest) != report.manifest_id:
        raise ValueError("manifest_mismatch")
    # This release imports only its own predefined synthetic fixture exports.
    # Reconstruct the entire expected report, not merely the manifest checksum.
    # This binds visible values, identities, disclosure, conclusions and provenance.
    # Historical code builds / arbitrary public data need a separately reviewed importer.
    expected = run_demo(
        report.hypothesis.hypothesis_id, report.scenario_id, report.manifest.dataset_version
    )
    if canonical_bytes(report) != canonical_bytes(expected):
        raise ValueError("report_integrity_mismatch")
    return report


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "list":
            print(
                json.dumps(
                    {
                        "data_kind": "synthetic",
                        "hypotheses": sorted(HYPOTHESES),
                        "scenarios": list(SCENARIOS),
                        "versions": list(VERSIONS),
                    },
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "schemas":
            for model in (Hypothesis, Evidence, CohortResult, Manifest, Report, DiffReport):
                write_once(
                    args.output / f"{model.__name__}.schema.json",
                    canonical_bytes(model.model_json_schema()) + b"\n",
                )
            print("schemas_exported")
            return 0
        if args.command == "run":
            report = run_demo(args.hypothesis, args.scenario, args.version)
            manifest_name = report.manifest_id.removeprefix("sha256:") + ".json"
            write_once(
                args.output / "manifests" / manifest_name, canonical_bytes(report.manifest) + b"\n"
            )
            write_once(args.output / "report.json", canonical_bytes(report) + b"\n")
            write_once(args.output / "report.md", render_report(report).encode())
            print(
                f"{report.comparison.run_status}: {report.comparison.comparison_status} (synthetic)"
            )
            return 0 if report.comparison.run_status == "complete" else 3
        before, after = _load_report(args.before), _load_report(args.after)
        diff = compare_reports(before, after)
        write_once(args.output / "diff.json", canonical_bytes(diff) + b"\n")
        write_once(args.output / "diff.md", render_diff(diff).encode())
        print("version_comparison_exported (synthetic demonstration)")
        return 0
    except OutputConflict:
        print("error: output_integrity_conflict", file=sys.stderr)
        return 4
    except (ValueError, ValidationError, OSError):
        print("error: invalid_input_or_output", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
