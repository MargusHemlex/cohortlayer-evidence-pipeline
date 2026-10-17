"""Strict transport contracts shared by the standalone demo modules."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class Hypothesis(Contract):
    hypothesis_id: str
    gene_id: str
    variant_id: str | None = None
    trait_id: str
    genome_build: Literal["GRCh38"] = "GRCh38"
    expected_direction: Literal["positive", "negative"]
    protocol_version: str = "demo-comparison-v1"


class Effect(Contract):
    measure: Literal["beta", "odds_ratio"]
    estimate: float
    ci_lower: float
    ci_upper: float
    standard_error: float | None = None
    trait_id: str
    unit: str
    phenotype_encoding: str
    contrast_id: str
    effect_allele: str | None = None
    reference_allele: str | None = None
    genome_build: str = "GRCh38"

    @model_validator(mode="after")
    def valid_statistics(self) -> "Effect":
        if not self.ci_lower <= self.estimate <= self.ci_upper:
            raise ValueError("invalid_interval")
        if self.standard_error is not None and self.standard_error < 0:
            raise ValueError("invalid_standard_error")
        if self.measure == "odds_ratio" and self.ci_lower <= 0:
            raise ValueError("invalid_ratio")
        if (self.effect_allele is None) != (self.reference_allele is None):
            raise ValueError("incomplete_alleles")
        return self


class CohortResult(Contract):
    cohort_id: Literal["Cohort A", "Cohort B"]
    hypothesis_id: str
    analysis_version: str = "synthetic-analysis-v1"
    dataset_version: Literal["v1", "v2"]
    data_kind: Literal["synthetic"] = "synthetic"
    execution_status: Literal["succeeded", "failed", "timeout"]
    disclosure_status: Literal["released", "suppressed", "not_applicable"]
    population: str = "Fictional population; not a real cohort"
    effect: Effect | None = None
    sample_size: int | None = Field(default=None, ge=0)
    carrier_count: int | None = Field(default=None, ge=0)
    case_count: int | None = Field(default=None, ge=0)
    adverse_effect: Effect | None = None
    reason_codes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def valid_result(self) -> "CohortResult":
        if self.sample_size is not None:
            for count in (self.carrier_count, self.case_count):
                if count is not None and count > self.sample_size:
                    raise ValueError("invalid_count")
        if self.execution_status != "succeeded":
            if self.disclosure_status != "not_applicable":
                raise ValueError("failed_disclosure")
            if any(
                x is not None
                for x in (
                    self.effect,
                    self.adverse_effect,
                    self.sample_size,
                    self.carrier_count,
                    self.case_count,
                )
            ):
                raise ValueError("failed_statistics")
            if not self.reason_codes:
                raise ValueError("failure_reason_required")
        elif self.disclosure_status == "not_applicable":
            raise ValueError("successful_disclosure_required")
        elif self.disclosure_status == "released" and self.effect is None:
            raise ValueError("effect_required")
        elif self.disclosure_status == "suppressed":
            if any(
                x is not None
                for x in (
                    self.effect,
                    self.adverse_effect,
                    self.sample_size,
                    self.carrier_count,
                    self.case_count,
                )
            ):
                raise ValueError("suppressed_statistics")
            if not self.reason_codes:
                raise ValueError("suppression_reason_required")
        return self


class Evidence(Contract):
    evidence_id: str
    source: str
    source_record_id: str
    study_id: str | None = None
    study_id_reason: str | None = None
    source_version: str
    retrieved_at: str | None = None
    retrieved_at_reason: str | None = None
    data_kind: Literal["synthetic", "public_reference"]
    source_url: str | None = None
    license_ref: str
    summary: str
    overlap_status: Literal["known", "possible", "unknown"] = "unknown"

    @model_validator(mode="after")
    def valid_provenance(self) -> "Evidence":
        if self.study_id is None and not self.study_id_reason:
            raise ValueError("study_id_reason_required")
        if self.data_kind == "synthetic":
            if self.retrieved_at is not None or self.retrieved_at_reason != "generated_fixture":
                raise ValueError("synthetic_retrieval")
        elif not self.retrieved_at or not self.source_url:
            raise ValueError("public_provenance_required")
        return self


class Comparison(Contract):
    run_status: Literal["complete", "partial", "failed"]
    comparison_status: Literal["concordant", "conflicting", "inconclusive", "not_evaluable"]
    direction_vs_hypothesis: Literal["matches", "opposes", "mixed", "not_assessable"]
    reason_codes: list[str]


class PhenotypeFlag(Contract):
    cohort_id: Literal["Cohort A", "Cohort B"]
    rule_version: Literal["demo-flag-v1"] = "demo-flag-v1"
    status: Literal["triggered", "not_triggered", "not_assessable"]
    reason_code: str


class Manifest(Contract):
    schema_version: Literal["1.0"] = "1.0"
    input_hash: str
    dataset_version: Literal["v1", "v2"]
    dataset_hash: str
    analysis_version: str
    comparison_version: str
    disclosure_policy_version: str
    disclosure_config_hash: str
    fixture_version: str
    generator_seed: None = None
    generator_reason: Literal["fixed_aggregate_fixture"] = "fixed_aggregate_fixture"
    code_version: str
    source_ids: list[str]


class Report(Contract):
    schema_version: Literal["1.0"] = "1.0"
    data_kind: Literal["synthetic", "mixed"]
    hypothesis: Hypothesis
    scenario_id: str
    comparison: Comparison
    cohorts: list[CohortResult] = Field(min_length=2, max_length=2)
    flags: list[PhenotypeFlag] = Field(min_length=2, max_length=2)
    reference_evidence: list[Evidence]
    manifest_id: str
    manifest: Manifest
    limitations: list[str]


class Change(Contract):
    entity_id: str
    change_type: Literal["added", "removed", "changed", "restricted"]
    before: dict | None = None
    after: dict | None = None


class DiffReport(Contract):
    schema_version: Literal["1.0"] = "1.0"
    data_kind: Literal["synthetic", "mixed"]
    before_manifest_id: str
    after_manifest_id: str
    evidence_changes: list[Change]
    cohort_changes: list[Change]
    conclusion_changes: list[Change]
    limitations: list[str]
