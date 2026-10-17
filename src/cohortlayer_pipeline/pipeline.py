"""Local orchestration: validate → disclose → compare → serialize."""

from .adapters import run_adapter
from .comparison import compare, phenotype_flags
from .contracts import Manifest, Report
from .disclosure import POLICY_CONFIG, POLICY_VERSION, disclose
from .fixtures import (
    FIXTURE_VERSION,
    HYPOTHESES,
    SCENARIOS,
    VERSIONS,
    deduplicate_evidence,
    reference_evidence,
)
from .provenance import code_identity, content_hash

LIMITATIONS = [
    "SYNTHETIC SOFTWARE EVALUATION: no real cohort access or scientific validation.",
    "Synthetic agreement is not independent replication, causality or clinical safety.",
    "No pooled effect is calculated. The comparison rule is illustrative only.",
    "Count suppression is not a formal privacy guarantee or protection from all inference.",
    "Population transferability is not assessed. Reference records are fictional.",
]


def run_pipeline(hypothesis_id: str, scenario_id: str, dataset_version: str) -> Report:
    if (
        hypothesis_id not in HYPOTHESES
        or scenario_id not in SCENARIOS
        or dataset_version not in VERSIONS
    ):
        raise ValueError("unsupported_pipeline_input")
    hypothesis = HYPOTHESES[hypothesis_id]
    raw = [
        run_adapter(name, hypothesis, scenario_id, dataset_version)
        for name in ("Cohort A", "Cohort B")
    ]
    cohorts = [disclose(result) for result in raw]
    # Only permitted output reaches comparison, flags and reporting.
    reference = deduplicate_evidence(reference_evidence(dataset_version, scenario_id))
    manifest = Manifest(
        input_hash=content_hash(
            {
                "hypothesis": hypothesis.model_dump(mode="json"),
                "scenario_id": scenario_id,
            }
        ),
        dataset_version=dataset_version,
        dataset_hash=content_hash(
            {
                "cohorts": [result.model_dump(mode="json") for result in raw],
                "evidence": [item.model_dump(mode="json") for item in reference],
            }
        ),
        analysis_version="synthetic-analysis-v1",
        comparison_version=hypothesis.protocol_version,
        disclosure_policy_version=POLICY_VERSION,
        disclosure_config_hash=content_hash(POLICY_CONFIG),
        fixture_version=FIXTURE_VERSION,
        code_version=code_identity(),
        source_ids=sorted({record.source_record_id for record in reference}),
    )
    return Report(
        data_kind="synthetic",
        hypothesis=hypothesis,
        scenario_id=scenario_id,
        comparison=compare(hypothesis, cohorts),
        cohorts=cohorts,
        flags=phenotype_flags(cohorts),
        reference_evidence=reference,
        manifest_id=content_hash(manifest),
        manifest=manifest,
        limitations=LIMITATIONS,
    )
