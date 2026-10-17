import pytest
from disclosure_helpers import cohort

from cohortlayer_pipeline.contracts import CohortResult
from cohortlayer_pipeline.disclosure import disclose


@pytest.mark.parametrize("field", ["carrier_count", "case_count"])
@pytest.mark.parametrize("count", [0, 9, None])
def test_restricted_counts_remove_all_statistics(field, count):
    raw = cohort().model_dump()
    raw[field] = count
    result = CohortResult.model_validate(raw)
    public = disclose(result)
    assert public.disclosure_status == "suppressed"
    for field_name in ("sample_size", "carrier_count", "case_count", "effect", "adverse_effect"):
        assert getattr(public, field_name) is None
    assert public.reason_codes == ["disclosure_input_missing" if count is None else "small_group"]
    assert disclose(public) == public
    assert result.effect is not None  # Pure transformation.


def test_boundary_ten_is_released():
    result = cohort(count=10)
    assert disclose(result) is result


def test_pre_suppressed_reason_cannot_carry_adapter_details():
    result = CohortResult(
        cohort_id="Cohort A",
        hypothesis_id="h1",
        dataset_version="v1",
        execution_status="succeeded",
        disclosure_status="suppressed",
        reason_codes=["private count=3"],
    )
    assert disclose(result).reason_codes == ["small_group"]


def test_failure_has_no_statistics():
    result = CohortResult(
        cohort_id="Cohort A",
        hypothesis_id="h1",
        dataset_version="v1",
        execution_status="timeout",
        disclosure_status="not_applicable",
        reason_codes=["adapter_timeout"],
    )
    assert disclose(result) is result
