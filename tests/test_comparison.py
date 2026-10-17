import pytest

from cohortlayer_pipeline.adapters import run_adapter
from cohortlayer_pipeline.comparison import compare, phenotype_flags
from cohortlayer_pipeline.contracts import CohortResult, Hypothesis


@pytest.fixture
def hypothesis():
    return Hypothesis(
        hypothesis_id="example",
        gene_id="DEMO:GENE",
        trait_id="EFO:0000400",
        expected_direction="positive",
    )


def pair(hypothesis, scenario="concordant"):
    return [run_adapter(c, hypothesis, scenario, "v1") for c in ("Cohort A", "Cohort B")]


@pytest.mark.parametrize(
    "scenario,run,status,direction",
    [
        ("concordant", "complete", "concordant", "matches"),
        ("opposes", "complete", "concordant", "opposes"),
        ("conflicting", "complete", "conflicting", "mixed"),
        ("inconclusive", "complete", "inconclusive", "not_assessable"),
        ("incomparable", "complete", "not_evaluable", "not_assessable"),
        ("failure", "partial", "not_evaluable", "not_assessable"),
        ("timeout", "partial", "not_evaluable", "not_assessable"),
        ("invalid_output", "partial", "not_evaluable", "not_assessable"),
    ],
)
def test_decision_table(hypothesis, scenario, run, status, direction):
    result = compare(hypothesis, pair(hypothesis, scenario))
    assert (result.run_status, result.comparison_status, result.direction_vs_hypothesis) == (
        run,
        status,
        direction,
    )


def test_both_failed(hypothesis):
    results = [
        CohortResult(
            cohort_id=c,
            hypothesis_id="example",
            dataset_version="v1",
            execution_status="failed",
            disclosure_status="not_applicable",
            reason_codes=["adapter_failure"],
        )
        for c in ("Cohort A", "Cohort B")
    ]
    assert compare(hypothesis, results).run_status == "failed"


def test_suppressed_has_no_comparison(hypothesis):
    results = pair(hypothesis)
    results[1] = CohortResult(
        cohort_id="Cohort B",
        hypothesis_id="example",
        dataset_version="v1",
        execution_status="succeeded",
        disclosure_status="suppressed",
        reason_codes=["small_group"],
    )
    assert compare(hypothesis, results).comparison_status == "not_evaluable"


@pytest.mark.parametrize(
    "field,value",
    [
        ("effect_allele", "T"),
        ("genome_build", "GRCh37"),
        ("trait_id", "EFO:other"),
        ("unit", "other"),
        ("phenotype_encoding", "reversed"),
        ("contrast_id", "reversed"),
    ],
)
def test_mismatched_semantics_cannot_claim_concordance(hypothesis, field, value):
    results = pair(hypothesis)
    results[1] = results[1].model_copy(
        update={
            "effect": results[1].effect.model_copy(update={field: value}),
        }
    )
    assert compare(hypothesis, results).comparison_status == "not_evaluable"


@pytest.mark.parametrize(
    "measure,estimate,low,high",
    [
        ("beta", 0.2, 0.0, 0.4),
        ("beta", -0.2, -0.4, 0.0),
        ("odds_ratio", 1.2, 1.0, 1.4),
        ("odds_ratio", 0.8, 0.6, 1.0),
    ],
)
def test_null_endpoint_is_inconclusive(hypothesis, measure, estimate, low, high):
    results = pair(hypothesis)
    for index, result in enumerate(results):
        effect = result.effect.model_copy(
            update={
                "measure": measure,
                "estimate": estimate,
                "ci_lower": low,
                "ci_upper": high,
            }
        )
        results[index] = result.model_copy(update={"effect": effect})
    assert compare(hypothesis, results).comparison_status == "inconclusive"


def test_duplicate_cohort_rejected(hypothesis):
    result = pair(hypothesis)[0]
    with pytest.raises(ValueError, match="two_distinct_cohorts_required"):
        compare(hypothesis, [result, result])


def test_flags_are_independent_and_null_boundary_is_not_triggered(hypothesis):
    assert [f.status for f in phenotype_flags(pair(hypothesis, "flag"))] == [
        "triggered",
        "not_triggered",
    ]
    assert {f.status for f in phenotype_flags(pair(hypothesis))} == {"not_assessable"}
