"""Offline adapters backed exclusively by fictional aggregate fixtures."""

from pydantic import ValidationError

from .contracts import CohortResult, Effect, Hypothesis

SCENARIOS = frozenset(
    {
        "concordant",
        "conflicting",
        "inconclusive",
        "suppressed",
        "failure",
        "timeout",
        "invalid_output",
        "incomparable",
        "update",
        "duplicate",
        "opposes",
        "flag",
    }
)


def run_adapter(
    cohort_id: str,
    hypothesis: Hypothesis,
    scenario_id: str,
    dataset_version: str,
) -> CohortResult:
    """Return validated, pre-disclosure aggregates; callers must apply disclosure."""
    if cohort_id not in {"Cohort A", "Cohort B"}:
        raise ValueError("unsupported_cohort")
    if scenario_id not in SCENARIOS:
        raise ValueError("unsupported_scenario")
    if dataset_version not in {"v1", "v2"}:
        raise ValueError("unsupported_dataset_version")
    base = dict(
        cohort_id=cohort_id,
        hypothesis_id=hypothesis.hypothesis_id,
        dataset_version=dataset_version,
    )
    is_b = cohort_id == "Cohort B"
    if is_b and scenario_id in {"failure", "timeout"}:
        return CohortResult(
            **base,
            execution_status="timeout" if scenario_id == "timeout" else "failed",
            disclosure_status="not_applicable",
            reason_codes=["adapter_timeout" if scenario_id == "timeout" else "adapter_failure"],
        )
    sign = 1.0 if hypothesis.expected_direction == "positive" else -1.0
    if scenario_id == "opposes" or (is_b and scenario_id == "conflicting"):
        sign *= -1
    estimate = sign * (0.3 if is_b else 0.4)
    if scenario_id == "update" and dataset_version == "v2" and is_b:
        estimate = -estimate
    lower, upper = sorted((estimate - 0.1, estimate + 0.1))
    if scenario_id == "inconclusive" and is_b:
        lower, upper = -0.5, 0.5
    effect = dict(
        measure="beta",
        estimate=estimate,
        ci_lower=lower,
        ci_upper=upper,
        trait_id=hypothesis.trait_id,
        unit="standard_deviation",
        phenotype_encoding="higher_value_means_more_trait",
        contrast_id="alternate_vs_reference" if hypothesis.variant_id else "perturbed_vs_baseline",
        effect_allele="A" if hypothesis.variant_id else None,
        reference_allele="G" if hypothesis.variant_id else None,
        genome_build=hypothesis.genome_build,
    )
    if scenario_id == "incomparable" and is_b:
        effect["unit"] = "fictional_other_unit"
    if scenario_id == "invalid_output" and is_b:
        effect.pop("ci_upper")
    adverse = None
    if scenario_id == "flag":
        adverse = Effect(
            measure="odds_ratio",
            estimate=1.5 if not is_b else 1.1,
            ci_lower=1.2 if not is_b else 1.0,
            ci_upper=1.8 if not is_b else 1.3,
            trait_id="DEMO:ADVERSE_EVENT",
            unit="ratio",
            phenotype_encoding="1=fictional_event",
            contrast_id="perturbed_vs_baseline",
        )
    count = 4 if scenario_id == "suppressed" and dataset_version == "v1" and is_b else 80
    try:
        return CohortResult(
            **base,
            execution_status="succeeded",
            disclosure_status="released",
            effect=effect,
            sample_size=1000,
            carrier_count=count,
            case_count=120,
            adverse_effect=adverse,
        )
    except ValidationError:
        return CohortResult(
            **base,
            execution_status="failed",
            disclosure_status="not_applicable",
            reason_codes=["invalid_output"],
        )
