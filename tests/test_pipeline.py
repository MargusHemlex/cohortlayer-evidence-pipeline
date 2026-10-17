import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from cohortlayer_demo.cli import main
from cohortlayer_demo.contracts import Report
from cohortlayer_demo.fixtures import (
    HYPOTHESES,
    SCENARIOS,
    deduplicate_evidence,
    reference_evidence,
)
from cohortlayer_demo.pipeline import run_demo
from cohortlayer_demo.provenance import OutputConflict, canonical_bytes, content_hash, write_once


@pytest.mark.parametrize("hypothesis", HYPOTHESES)
@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.parametrize("version", ["v1", "v2"])
def test_every_run_validates_and_repeats(hypothesis, scenario, version):
    report = run_demo(hypothesis, scenario, version)
    payload = canonical_bytes(report)
    assert payload == canonical_bytes(run_demo(hypothesis, scenario, version))
    assert Report.model_validate_json(payload) == report
    Draft202012Validator(Report.model_json_schema()).validate(json.loads(payload))
    assert report.manifest_id == content_hash(report.manifest)
    assert report.data_kind == "synthetic"
    assert all(c.data_kind == "synthetic" for c in report.cohorts)


def test_duplicate_reference_is_not_extra_confirmation():
    originals = reference_evidence("v1", "duplicate")
    assert len(originals) == 2
    deduplicated = deduplicate_evidence(originals)
    assert len(deduplicated) == 1
    assert deduplicated[0].overlap_status == "known"


def test_pipeline_suppression_precedes_comparison_and_rendering(capsys):
    from cohortlayer_demo.reporting import render_report

    report = run_demo("HYP-001", "suppressed", "v1")
    hidden = next(c for c in report.cohorts if c.cohort_id == "Cohort B")
    assert hidden.disclosure_status == "suppressed"
    assert hidden.effect is None and hidden.adverse_effect is None
    assert hidden.carrier_count is None and hidden.case_count is None
    assert hidden.sample_size is None
    assert report.comparison.comparison_status == "not_evaluable"
    assert report.comparison.direction_vs_hypothesis == "not_assessable"
    assert report.flags[1].status == "not_assessable"
    assert "Not released" in render_report(report)
    assert capsys.readouterr() == ("", "")


def test_list_command_is_deterministic_and_synthetic(capsys):
    assert main(["list"]) == 0
    first = capsys.readouterr().out
    assert main(["list"]) == 0
    assert capsys.readouterr().out == first
    payload = json.loads(first)
    assert len(payload["hypotheses"]) == 3 and payload["data_kind"] == "synthetic"


def test_manifest_and_output_integrity(tmp_path):
    path = tmp_path / "manifest.json"
    write_once(path, b"one")
    before = path.stat().st_mtime_ns
    write_once(path, b"one")
    assert path.stat().st_mtime_ns == before
    with pytest.raises(OutputConflict):
        write_once(path, b"two")
    assert path.read_bytes() == b"one"


def test_cli_update_workflow_and_conflict(tmp_path, capsys):
    for version in ("v1", "v2"):
        output = tmp_path / version
        args = ["run", "--scenario", "update", "--version", version, "--output", str(output)]
        assert main(args) == 0
        assert main(args) == 0
    assert (
        main(
            [
                "diff",
                str(tmp_path / "v1/report.json"),
                str(tmp_path / "v2/report.json"),
                "--output",
                str(tmp_path / "diff"),
            ]
        )
        == 0
    )
    diff = json.loads((tmp_path / "diff/diff.json").read_bytes())
    assert diff["cohort_changes"] and diff["conclusion_changes"] and diff["evidence_changes"]
    assert main(["run", "--output", str(tmp_path / "v1")]) == 4
    assert "output_integrity_conflict" in capsys.readouterr().err


def test_partial_cli_and_sanitized_invalid_input(tmp_path, capsys):
    assert main(["run", "--scenario", "failure", "--output", str(tmp_path / "partial")]) == 3
    marker = "UNTRUSTED_SENTINEL_29384"
    path = tmp_path / "bad.json"
    path.write_text('{"bad": "' + marker + '"}')
    assert main(["diff", str(path), str(path), "--output", str(tmp_path / "bad")]) == 2
    assert marker not in capsys.readouterr().err


def test_manifest_tampering_rejected(tmp_path):
    report = run_demo("HYP-001", "concordant", "v1").model_dump(mode="json")
    report["manifest"]["code_version"] = "tampered"
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(report))
    assert main(["diff", str(path), str(path), "--output", str(tmp_path / "out")]) == 2


@pytest.mark.parametrize(
    "field",
    [
        "cohort_version",
        "analysis",
        "comparison",
        "flag",
        "effect",
        "hypothesis",
        "source",
    ],
)
def test_edited_report_cannot_reuse_manifest(tmp_path, field):
    report = run_demo("HYP-001", "concordant", "v1").model_dump(mode="json")
    if field == "cohort_version":
        report["cohorts"][0]["dataset_version"] = "v2"
    elif field == "analysis":
        report["cohorts"][0]["analysis_version"] = "other"
    elif field == "comparison":
        report["comparison"]["comparison_status"] = "conflicting"
    elif field == "flag":
        report["flags"][0]["status"] = "triggered"
    elif field == "effect":
        report["cohorts"][0]["effect"]["estimate"] -= 0.01
    elif field == "hypothesis":
        report["hypothesis"]["expected_direction"] = "positive"
    else:
        report["reference_evidence"][0]["summary"] = "fabricated"
    path = tmp_path / "edited.json"
    path.write_text(json.dumps(report))
    assert main(["diff", str(path), str(path), "--output", str(tmp_path / "out")]) == 2


def test_standalone_markdown_preserves_effect_meaning():
    from cohortlayer_demo.reporting import render_report

    report = run_demo("HYP-003", "concordant", "v1")
    rendered = render_report(report)
    effect = report.cohorts[0].effect
    for value in (
        report.cohorts[0].population,
        effect.unit,
        effect.phenotype_encoding,
        effect.contrast_id,
        effect.effect_allele,
        effect.reference_allele,
    ):
        assert value in rendered


def test_schemas_and_static_examples(tmp_path):
    assert main(["schemas", "--output", str(tmp_path)]) == 0
    assert main(["schemas", "--output", str(tmp_path)]) == 0
    schema = json.loads((tmp_path / "Report.schema.json").read_text())
    assert schema["additionalProperties"] is False
    for definition in schema["$defs"].values():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False
    assert Path("docs/specification.et.md").is_file()


def test_checked_in_examples_and_schemas_are_current():
    from cohortlayer_demo.diff import compare_reports
    from cohortlayer_demo.reporting import render_diff, render_report

    before = run_demo("HYP-001", "update", "v1")
    after = run_demo("HYP-001", "update", "v2")
    assert Path("examples/report.json").read_bytes() == canonical_bytes(before) + b"\n"
    assert Path("examples/report.md").read_text() == render_report(before)
    diff = compare_reports(before, after)
    assert Path("examples/diff.json").read_bytes() == canonical_bytes(diff) + b"\n"
    assert Path("examples/diff.md").read_text() == render_diff(diff)
    assert Path("schemas/Report.schema.json").read_bytes() == (
        canonical_bytes(Report.model_json_schema()) + b"\n"
    )
