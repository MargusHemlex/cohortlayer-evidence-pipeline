import pytest
from disclosure_helpers import cohort, report

from cohortlayer_pipeline.contracts import CohortResult, Evidence, Report
from cohortlayer_pipeline.diff import compare_reports


@pytest.mark.parametrize("reverse", [False, True])
def test_threshold_transition_never_exposes_hidden_statistics(reverse):
    hidden = report(cohort(count=9, estimate=8123.456))
    hidden.comparison.reason_codes = ["HIDDEN_CONCLUSION_SENTINEL"]
    hidden.flags[0].reason_code = "HIDDEN_FLAG_SENTINEL"
    released = report(version="v2")
    before, after = (released, hidden) if reverse else (hidden, released)
    result = compare_reports(before, after)
    serialized = result.model_dump_json()
    assert "8123.456" not in serialized
    assert "HIDDEN_CONCLUSION_SENTINEL" not in serialized
    assert "HIDDEN_FLAG_SENTINEL" not in serialized
    restricted = next(c for c in result.cohort_changes if c.entity_id == "Cohort A")
    assert restricted.change_type == "restricted"
    assert restricted.before is None and restricted.after is None
    assert result.conclusion_changes[0].change_type == "restricted"
    assert result.conclusion_changes[0].before is None


def test_failed_cohort_restricts_conclusions_without_error_details():
    failed = CohortResult(
        cohort_id="Cohort A",
        hypothesis_id="h1",
        dataset_version="v2",
        execution_status="failed",
        disclosure_status="not_applicable",
        reason_codes=["SENTINEL_ADAPTER_RAW"],
    )
    result = compare_reports(report(), report(failed, version="v2"))
    assert "SENTINEL_ADAPTER_RAW" not in result.model_dump_json()
    assert result.conclusion_changes[0].change_type == "restricted"


def test_unchanged_released_report_has_no_semantic_changes():
    result = compare_reports(report(), report())
    assert result.cohort_changes == []
    assert result.evidence_changes == []
    assert result.conclusion_changes == []


def test_released_effect_change_is_visible():
    result = compare_reports(report(), report(cohort(estimate=0.7)))
    change = result.cohort_changes[0]
    assert change.before["effect"]["estimate"] == 0.5
    assert change.after["effect"]["estimate"] == 0.7


def test_evidence_ids_drive_add_remove_and_change():
    def evidence(identity, summary):
        return Evidence(
            evidence_id=identity,
            source="synthetic-source",
            source_record_id=identity,
            source_version="v1",
            study_id_reason="fictional",
            retrieved_at_reason="generated_fixture",
            data_kind="synthetic",
            license_ref="synthetic-fixture",
            summary=summary,
        )

    before, after = report(), report()
    before.reference_evidence = [evidence("same", "old"), evidence("removed", "old")]
    after.reference_evidence = [evidence("same", "new"), evidence("added", "new")]
    result = compare_reports(before, after)
    assert {c.entity_id: c.change_type for c in result.evidence_changes} == {
        "same": "changed",
        "removed": "removed",
        "added": "added",
    }


@pytest.mark.parametrize("mutation", ["scenario", "hypothesis", "duplicate", "cohort_hypothesis"])
def test_incompatible_identity_is_rejected(mutation):
    raw = report().model_dump()
    if mutation == "scenario":
        raw["scenario_id"] = "other"
    elif mutation == "hypothesis":
        raw["hypothesis"]["gene_id"] = "other"
    elif mutation == "duplicate":
        raw["cohorts"][1]["cohort_id"] = "Cohort A"
    else:
        raw["cohorts"][0]["hypothesis_id"] = "other"
    with pytest.raises(ValueError):
        compare_reports(report(), Report.model_validate(raw))
