# CohortLayer Evidence Pipeline — version comparison

**SYNTHETIC SOFTWARE EVALUATION — changes are not new scientific evidence.**

Before: `sha256:5938e23ba15ad1ad65711d487143d6cf4971113bf48b7d896753d6ca0c5079fb`

After: `sha256:8e22964e5c122dc98e2e8ff7cd1b6c26eb4593a333d1136362903d6543a54489`

## Reference evidence

### SYNTHETIC:EVIDENCE_1 — changed

```json
{
  "before": {
    "evidence_id": "SYNTHETIC:EVIDENCE_1",
    "source": "Fictional Registry A",
    "source_record_id": "SYNTHETIC:ORIGINAL_1",
    "study_id": "SYNTHETIC:STUDY_1",
    "study_id_reason": null,
    "source_version": "v1",
    "retrieved_at": null,
    "retrieved_at_reason": "generated_fixture",
    "data_kind": "synthetic",
    "source_url": null,
    "license_ref": "MIT; repository-authored synthetic fixture",
    "summary": "Fictional association annotation, not a published finding.",
    "overlap_status": "unknown"
  },
  "after": {
    "evidence_id": "SYNTHETIC:EVIDENCE_1",
    "source": "Fictional Registry A",
    "source_record_id": "SYNTHETIC:ORIGINAL_1",
    "study_id": "SYNTHETIC:STUDY_1",
    "study_id_reason": null,
    "source_version": "v2",
    "retrieved_at": null,
    "retrieved_at_reason": "generated_fixture",
    "data_kind": "synthetic",
    "source_url": null,
    "license_ref": "MIT; repository-authored synthetic fixture",
    "summary": "Fictional reclassification in fixture v2; simulated, not real research.",
    "overlap_status": "unknown"
  }
}
```

### SYNTHETIC:EVIDENCE_2 — added

```json
{
  "before": null,
  "after": {
    "evidence_id": "SYNTHETIC:EVIDENCE_2",
    "source": "Fictional Registry A",
    "source_record_id": "SYNTHETIC:ORIGINAL_2",
    "study_id": null,
    "study_id_reason": "fictional_unassigned_study",
    "source_version": "v2",
    "retrieved_at": null,
    "retrieved_at_reason": "generated_fixture",
    "data_kind": "synthetic",
    "source_url": null,
    "license_ref": "MIT; repository-authored synthetic fixture",
    "summary": "Additional fictional annotation in fixture v2.",
    "overlap_status": "unknown"
  }
}
```

## Fictional cohort results

### Cohort A — changed

```json
{
  "before": {
    "cohort_id": "Cohort A",
    "hypothesis_id": "HYP-001",
    "analysis_version": "synthetic-analysis-v1",
    "dataset_version": "v1",
    "data_kind": "synthetic",
    "execution_status": "succeeded",
    "disclosure_status": "released",
    "population": "Fictional population; not a real cohort",
    "effect": {
      "measure": "beta",
      "estimate": -0.4,
      "ci_lower": -0.5,
      "ci_upper": -0.30000000000000004,
      "standard_error": null,
      "trait_id": "SYNTHETIC:TRAIT_A",
      "unit": "standard_deviation",
      "phenotype_encoding": "higher_value_means_more_trait",
      "contrast_id": "perturbed_vs_baseline",
      "effect_allele": null,
      "reference_allele": null,
      "genome_build": "GRCh38"
    },
    "sample_size": 1000,
    "carrier_count": 80,
    "case_count": 120,
    "adverse_effect": null,
    "reason_codes": []
  },
  "after": {
    "cohort_id": "Cohort A",
    "hypothesis_id": "HYP-001",
    "analysis_version": "synthetic-analysis-v1",
    "dataset_version": "v2",
    "data_kind": "synthetic",
    "execution_status": "succeeded",
    "disclosure_status": "released",
    "population": "Fictional population; not a real cohort",
    "effect": {
      "measure": "beta",
      "estimate": -0.4,
      "ci_lower": -0.5,
      "ci_upper": -0.30000000000000004,
      "standard_error": null,
      "trait_id": "SYNTHETIC:TRAIT_A",
      "unit": "standard_deviation",
      "phenotype_encoding": "higher_value_means_more_trait",
      "contrast_id": "perturbed_vs_baseline",
      "effect_allele": null,
      "reference_allele": null,
      "genome_build": "GRCh38"
    },
    "sample_size": 1000,
    "carrier_count": 80,
    "case_count": 120,
    "adverse_effect": null,
    "reason_codes": []
  }
}
```

### Cohort B — changed

```json
{
  "before": {
    "cohort_id": "Cohort B",
    "hypothesis_id": "HYP-001",
    "analysis_version": "synthetic-analysis-v1",
    "dataset_version": "v1",
    "data_kind": "synthetic",
    "execution_status": "succeeded",
    "disclosure_status": "released",
    "population": "Fictional population; not a real cohort",
    "effect": {
      "measure": "beta",
      "estimate": -0.3,
      "ci_lower": -0.4,
      "ci_upper": -0.19999999999999998,
      "standard_error": null,
      "trait_id": "SYNTHETIC:TRAIT_A",
      "unit": "standard_deviation",
      "phenotype_encoding": "higher_value_means_more_trait",
      "contrast_id": "perturbed_vs_baseline",
      "effect_allele": null,
      "reference_allele": null,
      "genome_build": "GRCh38"
    },
    "sample_size": 1000,
    "carrier_count": 80,
    "case_count": 120,
    "adverse_effect": null,
    "reason_codes": []
  },
  "after": {
    "cohort_id": "Cohort B",
    "hypothesis_id": "HYP-001",
    "analysis_version": "synthetic-analysis-v1",
    "dataset_version": "v2",
    "data_kind": "synthetic",
    "execution_status": "succeeded",
    "disclosure_status": "released",
    "population": "Fictional population; not a real cohort",
    "effect": {
      "measure": "beta",
      "estimate": 0.3,
      "ci_lower": 0.19999999999999998,
      "ci_upper": 0.4,
      "standard_error": null,
      "trait_id": "SYNTHETIC:TRAIT_A",
      "unit": "standard_deviation",
      "phenotype_encoding": "higher_value_means_more_trait",
      "contrast_id": "perturbed_vs_baseline",
      "effect_allele": null,
      "reference_allele": null,
      "genome_build": "GRCh38"
    },
    "sample_size": 1000,
    "carrier_count": 80,
    "case_count": 120,
    "adverse_effect": null,
    "reason_codes": []
  }
}
```

## Derived conclusions

### conclusions — changed

```json
{
  "before": {
    "comparison": {
      "run_status": "complete",
      "comparison_status": "concordant",
      "direction_vs_hypothesis": "matches",
      "reason_codes": [
        "same_direction_intervals"
      ]
    },
    "flags": [
      {
        "cohort_id": "Cohort A",
        "rule_version": "pipeline-flag-v1",
        "status": "not_assessable",
        "reason_code": "flag_input_unavailable"
      },
      {
        "cohort_id": "Cohort B",
        "rule_version": "pipeline-flag-v1",
        "status": "not_assessable",
        "reason_code": "flag_input_unavailable"
      }
    ]
  },
  "after": {
    "comparison": {
      "run_status": "complete",
      "comparison_status": "conflicting",
      "direction_vs_hypothesis": "mixed",
      "reason_codes": [
        "opposite_direction_intervals"
      ]
    },
    "flags": [
      {
        "cohort_id": "Cohort A",
        "rule_version": "pipeline-flag-v1",
        "status": "not_assessable",
        "reason_code": "flag_input_unavailable"
      },
      {
        "cohort_id": "Cohort B",
        "rule_version": "pipeline-flag-v1",
        "status": "not_assessable",
        "reason_code": "flag_input_unavailable"
      }
    ]
  }
}
```

## Limitations

- Synthetic evaluation; differences are not new scientific evidence.
- Restricted comparisons disclose no statistics or derived conclusion details.
- Aggregate release is not a formal privacy guarantee.
