"""Versioned fictional inputs; no scientific database records are redistributed."""

from .contracts import Evidence, Hypothesis

HYPOTHESES = {
    "HYP-001": Hypothesis(
        hypothesis_id="HYP-001",
        gene_id="SYNTHETIC:GENE_A",
        trait_id="SYNTHETIC:TRAIT_A",
        expected_direction="negative",
    ),
    "HYP-002": Hypothesis(
        hypothesis_id="HYP-002",
        gene_id="SYNTHETIC:GENE_B",
        trait_id="SYNTHETIC:TRAIT_B",
        expected_direction="positive",
    ),
    "HYP-003": Hypothesis(
        hypothesis_id="HYP-003",
        gene_id="SYNTHETIC:GENE_C",
        variant_id="SYNTHETIC:VARIANT_C",
        trait_id="SYNTHETIC:TRAIT_C",
        expected_direction="negative",
    ),
}

SCENARIOS = (
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
)
VERSIONS = ("v1", "v2")
FIXTURE_VERSION = "aggregate-fixtures-v1"


def reference_evidence(version: str, scenario_id: str) -> list[Evidence]:
    """Return illustrative source records with explicit original-record identity."""
    records = [
        Evidence(
            evidence_id="SYNTHETIC:EVIDENCE_1",
            source="Fictional Registry A",
            source_record_id="SYNTHETIC:ORIGINAL_1",
            study_id="SYNTHETIC:STUDY_1",
            source_version=version,
            data_kind="synthetic",
            retrieved_at_reason="generated_fixture",
            license_ref="MIT; repository-authored synthetic fixture",
            summary="Fictional association annotation, not a published finding.",
        )
    ]
    if scenario_id == "duplicate":
        # Different database wrapper, identical original record: no extra confirmation.
        records.append(
            records[0].model_copy(
                update={
                    "evidence_id": "SYNTHETIC:EVIDENCE_WRAPPER",
                    "source": "Fictional Registry B",
                }
            )
        )
    if version == "v2" and scenario_id == "update":
        records[0] = records[0].model_copy(
            update={
                "summary": (
                    "Fictional reclassification in fixture v2; simulated, not real research."
                ),
            }
        )
        records.append(
            Evidence(
                evidence_id="SYNTHETIC:EVIDENCE_2",
                source="Fictional Registry A",
                source_record_id="SYNTHETIC:ORIGINAL_2",
                study_id=None,
                study_id_reason="fictional_unassigned_study",
                source_version=version,
                data_kind="synthetic",
                retrieved_at_reason="generated_fixture",
                license_ref="MIT; repository-authored synthetic fixture",
                summary="Additional fictional annotation in fixture v2.",
            )
        )
    return records


def deduplicate_evidence(records: list[Evidence]) -> list[Evidence]:
    """Group exact original identifiers, preserving known overlap on retained records.

    This does not infer participant overlap or statistical independence. The original
    identifier is deliberately different from the source wrapper's local evidence ID.
    """
    by_original: dict[tuple[str, str | None], list[Evidence]] = {}
    for record in records:
        by_original.setdefault((record.source_record_id, record.study_id), []).append(record)
    retained = []
    for group in by_original.values():
        first = sorted(group, key=lambda item: item.evidence_id)[0]
        if len(group) > 1:
            first = first.model_copy(update={"overlap_status": "known"})
        retained.append(first)
    return sorted(retained, key=lambda item: item.evidence_id)
