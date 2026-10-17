"""Transparent illustrative comparison, without scientific replication claims."""

from .contracts import CohortResult, Comparison, Hypothesis, PhenotypeFlag


def _unavailable(run_status: str, reason: str) -> Comparison:
    return Comparison(
        run_status=run_status,
        comparison_status="not_evaluable",
        direction_vs_hypothesis="not_assessable",
        reason_codes=[reason],
    )


def compare(hypothesis: Hypothesis, cohorts: list[CohortResult]) -> Comparison:
    """Compare exactly two distinct, already disclosure-filtered cohort results."""
    if len(cohorts) != 2 or {c.cohort_id for c in cohorts} != {"Cohort A", "Cohort B"}:
        raise ValueError("two_distinct_cohorts_required")
    successes = sum(c.execution_status == "succeeded" for c in cohorts)
    if successes == 0:
        return _unavailable("failed", "both_cohorts_failed")
    if successes == 1:
        return _unavailable("partial", "cohort_unavailable")
    if any(c.disclosure_status != "released" or c.effect is None for c in cohorts):
        return _unavailable("complete", "result_not_released")
    a, b = (c.effect for c in cohorts)
    assert a is not None and b is not None
    fields = (
        "measure",
        "trait_id",
        "unit",
        "phenotype_encoding",
        "contrast_id",
        "effect_allele",
        "reference_allele",
        "genome_build",
    )
    if (
        any(getattr(a, field) != getattr(b, field) for field in fields)
        or a.trait_id != hypothesis.trait_id
        or a.genome_build != hypothesis.genome_build
        or any(c.hypothesis_id != hypothesis.hypothesis_id for c in cohorts)
        or (hypothesis.variant_id is not None and a.effect_allele is None)
        or len({c.analysis_version for c in cohorts}) != 1
        or len({c.dataset_version for c in cohorts}) != 1
    ):
        return _unavailable("complete", "incomparable_results")
    null = 0.0 if a.measure == "beta" else 1.0
    if any(e.ci_lower <= null <= e.ci_upper for e in (a, b)):
        return Comparison(
            run_status="complete",
            comparison_status="inconclusive",
            direction_vs_hypothesis="not_assessable",
            reason_codes=["interval_includes_null"],
        )
    positive_a, positive_b = a.ci_lower > null, b.ci_lower > null
    same = positive_a == positive_b
    expected_positive = hypothesis.expected_direction == "positive"
    direction = (
        "mixed" if not same else ("matches" if positive_a == expected_positive else "opposes")
    )
    return Comparison(
        run_status="complete",
        comparison_status="concordant" if same else "conflicting",
        direction_vs_hypothesis=direction,
        reason_codes=["same_direction_intervals" if same else "opposite_direction_intervals"],
    )


def phenotype_flags(cohorts: list[CohortResult]) -> list[PhenotypeFlag]:
    """Evaluate each released fictional adverse-event OR separately."""
    flags = []
    for cohort in cohorts:
        effect = cohort.adverse_effect
        eligible = (
            cohort.execution_status == "succeeded"
            and cohort.disclosure_status == "released"
            and effect is not None
            and effect.measure == "odds_ratio"
            and effect.trait_id == "SYNTHETIC:ADVERSE_EVENT"
        )
        if not eligible:
            status, reason = "not_assessable", "flag_input_unavailable"
        elif effect.ci_lower > 1.0:
            status, reason = "triggered", "interval_above_null"
        else:
            status, reason = "not_triggered", "interval_not_above_null"
        flags.append(PhenotypeFlag(cohort_id=cohort.cohort_id, status=status, reason_code=reason))
    return flags
