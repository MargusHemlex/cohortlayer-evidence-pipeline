import pytest

from cohortlayer_demo.adapters import SCENARIOS, run_adapter
from cohortlayer_demo.contracts import Hypothesis


@pytest.fixture
def hypothesis():
    return Hypothesis(
        hypothesis_id="example",
        gene_id="DEMO:GENE",
        trait_id="EFO:0000400",
        expected_direction="negative",
    )


@pytest.mark.parametrize("scenario", sorted(SCENARIOS))
@pytest.mark.parametrize("version", ["v1", "v2"])
def test_fixtures_preserve_identity_and_repeat(hypothesis, scenario, version):
    for cohort in ["Cohort A", "Cohort B"]:
        result = run_adapter(cohort, hypothesis, scenario, version)
        assert result.hypothesis_id == hypothesis.hypothesis_id
        assert result.dataset_version == version
        assert result.data_kind == "synthetic"
        assert result == run_adapter(cohort, hypothesis, scenario, version)


@pytest.mark.parametrize(
    "scenario,status,reason",
    [
        ("failure", "failed", "adapter_failure"),
        ("timeout", "timeout", "adapter_timeout"),
        ("invalid_output", "failed", "invalid_output"),
    ],
)
def test_failure_is_sanitized(hypothesis, scenario, status, reason):
    result = run_adapter("Cohort B", hypothesis, scenario, "v1")
    assert result.execution_status == status
    assert result.reason_codes == [reason]
    assert result.effect is result.sample_size is result.adverse_effect is None
    assert result.disclosure_status == "not_applicable"
    assert run_adapter("Cohort A", hypothesis, scenario, "v1").execution_status == "succeeded"


def test_suppression_transition_is_input_to_disclosure(hypothesis):
    a = run_adapter("Cohort B", hypothesis, "suppressed", "v1")
    b = run_adapter("Cohort B", hypothesis, "suppressed", "v2")
    assert a.carrier_count == 4 and b.carrier_count == 80
    assert a.disclosure_status == b.disclosure_status == "released"


@pytest.mark.parametrize(
    "cohort,scenario,version",
    [
        ("real", "concordant", "v1"),
        ("Cohort A", "unknown", "v1"),
        ("Cohort A", "concordant", "v3"),
    ],
)
def test_unknown_fixture_selector_rejected(hypothesis, cohort, scenario, version):
    with pytest.raises(ValueError):
        run_adapter(cohort, hypothesis, scenario, version)
