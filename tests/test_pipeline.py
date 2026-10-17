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


def test_schemas_and_static_examples(tmp_path):
    assert main(["schemas", "--output", str(tmp_path)]) == 0
    schema = json.loads((tmp_path / "Report.schema.json").read_text())
    assert schema["additionalProperties"] is False
    for definition in schema["$defs"].values():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False
    assert Path("docs/specification.et.md").is_file()
