"""Small independent report builders for output-boundary tests."""

from cohortlayer_demo.contracts import (
    CohortResult,
    Comparison,
    Effect,
    Hypothesis,
    Manifest,
    PhenotypeFlag,
    Report,
)


def cohort(identity="Cohort A", count=20, estimate=0.5, version="v1"):
    return CohortResult(
        cohort_id=identity,
        hypothesis_id="h1",
        dataset_version=version,
        execution_status="succeeded",
        disclosure_status="released",
        sample_size=1000,
        carrier_count=count,
        case_count=20,
        effect=Effect(
            measure="beta",
            estimate=estimate,
            ci_lower=estimate - 0.1,
            ci_upper=estimate + 0.1,
            trait_id="EFO:demo",
            unit="unit",
            phenotype_encoding="higher_is_more",
            contrast_id="contrast-1",
        ),
    )


def report(first=None, version="v1"):
    cohorts = [
        first if first is not None else cohort(version=version),
        cohort("Cohort B", version=version),
    ]
    return Report(
        data_kind="synthetic",
        hypothesis=Hypothesis(
            hypothesis_id="h1",
            gene_id="GENE:demo",
            trait_id="EFO:demo",
            expected_direction="positive",
        ),
        scenario_id="scenario-1",
        comparison=Comparison(
            run_status="complete",
            comparison_status="concordant",
            direction_vs_hypothesis="matches",
            reason_codes=["demo_rule"],
        ),
        cohorts=cohorts,
        flags=[
            PhenotypeFlag(cohort_id=c.cohort_id, status="not_assessable", reason_code="missing")
            for c in cohorts
        ],
        reference_evidence=[],
        manifest_id=f"manifest-{version}",
        manifest=Manifest(
            input_hash="input",
            dataset_version=version,
            dataset_hash="fixture",
            analysis_version="synthetic-analysis-v1",
            comparison_version="demo-comparison-v1",
            disclosure_policy_version="demo-disclosure-v1",
            disclosure_config_hash="config",
            fixture_version=version,
            code_version="test",
            source_ids=[],
        ),
        limitations=["Synthetic test"],
    )
